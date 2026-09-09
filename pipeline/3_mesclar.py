#!/usr/bin/env python3
"""
3_mesclar.py — remonta o minha-banca.html com as respostas convertidas e valida.

Lê:  minha-banca.html + todos os respostas_*.json (os antigos e os de resultados/)
Grava: minha-banca.NOVO.html   (nunca sobrescreve o original)

Uso:  python 3_mesclar.py caminho/para/minha-banca.html
      python 3_mesclar.py caminho/para/minha-banca.html --so-validar
"""
import json, os, sys, glob, re, subprocess, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
CONST = "const DPE_ORAL_QUESTOES"
SEP = " ||| "          # marcador de quebra de linha usado nos arquivos de resposta

RESIDUOS = [
    r"\bacho que\b", r"\bsalvo engano\b(?! justificável)", r"\babordei\b",
    r"\brespondi que\b", r"pergunta de aprofundamento", r"este material foi produzido",
    r"\bvide questão\b", r"\?\?\?", r"REVISÃO\s*\d", r"comentários da revisora",
    r"\bse não me engano\b", r"\bbons estudos\b",
]


def carregar_convertidos():
    """Junta respostas_*.json de resultados/ e da pasta anterior. resultados/ vence."""
    saida = {}
    for pasta in [os.path.join(AQUI, ".."), AQUI, os.path.join(AQUI, "resultados")]:
        for arq in sorted(glob.glob(os.path.join(pasta, "respostas_*.json"))):
            materia = re.sub(r"^respostas_|\.json$", "", os.path.basename(arq))
            materia = re.sub(r"_p\d+$", "", materia)
            with open(arq, encoding="utf-8") as f:
                for idx, valor in json.load(f).items():
                    texto = valor if (isinstance(valor, str) or valor is None) \
                            else valor.get("resposta")
                    saida.setdefault(materia, {})[str(idx)] = texto
    return saida


def validar(banco):
    total = com_resp = nulos = com_marcador = 0
    problemas = []
    for materia, itens in banco.items():
        for i, item in enumerate(itens):
            total += 1
            r = item.get("resposta")
            if r is None:
                nulos += 1
                continue
            com_resp += 1
            if "##FALA##" in r and "##ROTEIRO##" in r:
                com_marcador += 1
            else:
                problemas.append(f"sem marcador: {materia}|{i}")
    print(f"itens .................. {total}   (esperado 750)")
    print(f"nulos .................. {nulos}")
    print(f"com resposta ........... {com_resp}")
    print(f"no formato novo ........ {com_marcador}  ({100*com_marcador/max(com_resp,1):.1f}%)")

    print("\nvarredura de resíduos:")
    todo = "\n".join(it["resposta"] for m in banco.values() for it in m
                     if it.get("resposta"))
    limpo = True
    for pad in RESIDUOS:
        n = len(re.findall(pad, todo, flags=re.IGNORECASE))
        if n:
            limpo = False
            print(f"  {pad:38} {n}")
    if limpo:
        print("  nenhum — ok")

    # registro falado: termos de papel só são problema DENTRO da ##FALA##
    BANIDAS = ["outrossim", "exsurge", "insta salientar", "cumpre destacar", "impende",
               "no que tange", "no bojo de", "destarte", "por excelência",
               "sucedeu-se", "sucederam-se", "consoante", "malgrado", "em sede de"]
    falhas_fala = []
    for materia, itens in banco.items():
        for i, item in enumerate(itens):
            r = item.get("resposta") or ""
            if "##FALA##" not in r:
                continue
            fala = r.split("##FALA##", 1)[1].split("##ROTEIRO##", 1)[0].lower()
            achados = [b for b in BANIDAS if b in fala]
            if ";" in fala:
                achados.append("ponto e vírgula")
            if achados:
                falhas_fala.append((materia, i, achados))

    print("\nregistro falado (só dentro da FALA):")
    if falhas_fala:
        print(f"  {len(falhas_fala)} itens com termo de papel na fala")
        with open(os.path.join(AQUI, "REVISAR-LINGUAGEM.md"), "w", encoding="utf-8") as f:
            f.write("# Revisar linguagem da FALA\n\n")
            f.write("Termos que só existem no papel, ou pontuação impronunciável, "
                    "encontrados dentro do bloco `##FALA##`.\n\n")
            for materia, i, achados in falhas_fala:
                f.write(f"- [ ] `{materia}|{i}` — {', '.join(achados)}\n")
        print("  -> REVISAR-LINGUAGEM.md")
    else:
        print("  nenhum — ok")

    if problemas:
        print(f"\n{len(problemas)} itens fora do formato:")
        for p in problemas[:25]:
            print("  " + p)
    return total, com_marcador, problemas


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    html_path = sys.argv[1]
    so_validar = "--so-validar" in sys.argv

    with open(html_path, encoding="utf-8") as f:
        linhas = f.readlines()
    alvo = next((n for n, l in enumerate(linhas) if l.lstrip().startswith(CONST)), None)
    if alvo is None:
        raise SystemExit(f"Constante {CONST} não encontrada.")

    bruto = linhas[alvo].split("=", 1)[1].strip().rstrip(";")
    banco = json.loads(bruto)

    if not so_validar:
        convertidos = carregar_convertidos()
        aplicados = 0
        verificar = []            # (materia, indice, ponto)
        for materia, itens in banco.items():
            for idx, texto in convertidos.get(materia, {}).items():
                i = int(idx)
                if i >= len(itens):
                    continue
                if texto is None:
                    itens[i]["resposta"] = None
                    aplicados += 1
                    continue
                # o bloco ##VERIFICAR## é relatório interno: sai do conteúdo do site
                corpo, _, notas = texto.partition("##VERIFICAR##")
                for ponto in notas.split(SEP):
                    ponto = ponto.strip()
                    if ponto:
                        verificar.append((materia, i, ponto))
                itens[i]["resposta"] = corpo.strip().strip("|").strip().replace(SEP, "\n")
                aplicados += 1
        print(f"respostas aplicadas: {aplicados}")

        destino_notas = os.path.join(AQUI, "PONTOS-A-VERIFICAR.md")
        if verificar:
            with open(destino_notas, "w", encoding="utf-8") as f:
                f.write("# Pontos a verificar\n\n")
                f.write("Levantados pelo modelo durante a reescrita. "
                        "Não entram no site — exigem sua conferência.\n\n")
                atual = None
                for materia, i, ponto in sorted(verificar):
                    if materia != atual:
                        atual = materia
                        f.write(f"\n## {materia}\n\n")
                    f.write(f"- [ ] `{materia}|{i}` — {ponto}\n")
            print(f"pontos a verificar: {len(verificar)}  -> PONTOS-A-VERIFICAR.md")
        else:
            print("pontos a verificar: nenhum")
        print()

    total, ok, problemas = validar(banco)

    if so_validar:
        return

    prefixo = linhas[alvo].split("=", 1)[0]
    linhas[alvo] = f"{prefixo}= {json.dumps(banco, ensure_ascii=False)};\n"
    destino = html_path.replace(".html", ".NOVO.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.writelines(linhas)
    print(f"\ngravado: {destino}")

    # node --check sobre o <script> inline, para garantir que o arquivo não quebrou
    conteudo = "".join(linhas)
    m = re.search(r"<script(?![^>]*src)[^>]*>([\s\S]*?)</script>", conteudo)
    if m:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as tmp:
            tmp.write(m.group(1))
            caminho_tmp = tmp.name
        r = subprocess.run(["node", "--check", caminho_tmp],
                           capture_output=True, text=True)
        os.unlink(caminho_tmp)
        print("node --check:", "ok" if r.returncode == 0 else "FALHOU\n" + r.stderr)

    print("\nConfira o .NOVO.html no navegador antes de substituir o original.")


if __name__ == "__main__":
    main()
