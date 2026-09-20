#!/usr/bin/env python3
"""
1_extrair.py — extrai o banco de questões do minha-banca.html e monta a fila de trabalho.

Lê:  minha-banca.html  (constante DPE_ORAL_QUESTOES, uma linha)
     respostas_*.json  (o que já foi convertido — não é refeito)
Grava: dados/banco.json      todos os 750 itens, com pergunta e resposta original
       dados/pendentes.json  só o que falta converter

Uso:  python 1_extrair.py caminho/para/minha-banca.html
"""
import json, os, sys, glob, re

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados")
CONST = "const DPE_ORAL_QUESTOES"


def extrair_constante(caminho_html: str) -> dict:
    """A constante é serializada numa linha só. Localiza a linha e faz json.loads
    do lado direito. Não usar regex sobre o conteúdo: as strings contêm { } [ ]."""
    with open(caminho_html, encoding="utf-8") as f:
        for linha in f:
            if linha.lstrip().startswith(CONST):
                bruto = linha.split("=", 1)[1].strip()
                if bruto.endswith(";"):
                    bruto = bruto[:-1]
                return json.loads(bruto)
    raise SystemExit(f"Constante {CONST} não encontrada em {caminho_html}")


def carregar_prontos() -> dict:
    """respostas_<materia>.json no formato {"<indice>": "texto" | null}."""
    prontos = {}
    for arq in glob.glob(os.path.join(AQUI, "..", "respostas_*.json")) + \
               glob.glob(os.path.join(AQUI, "respostas_*.json")) + \
               glob.glob(os.path.join(AQUI, "resultados", "respostas_*.json")):
        materia = re.sub(r"^respostas_|\.json$", "", os.path.basename(arq))
        materia = re.sub(r"_p\d+$", "", materia)          # direitos_humanos_p1 -> direitos_humanos
        with open(arq, encoding="utf-8") as f:
            dados = json.load(f)
        for idx, valor in dados.items():
            texto = valor if isinstance(valor, str) else (valor or {}).get("resposta")
            prontos.setdefault(materia, {})[str(idx)] = texto
    return prontos


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    html = sys.argv[1]
    os.makedirs(DADOS, exist_ok=True)

    banco = extrair_constante(html)
    prontos = carregar_prontos()

    total = pendente = ja_ok = nulos = 0
    fila = []
    for materia, itens in banco.items():
        for i, item in enumerate(itens):
            total += 1
            resposta = item.get("resposta")
            if resposta is None:
                nulos += 1
                continue                                   # null permanece null
            feito = prontos.get(materia, {}).get(str(i))
            if feito and "##FALA##" in feito:
                ja_ok += 1
                continue
            pendente += 1
            fila.append({
                "id": f"{materia}__{i}",
                "materia": materia,
                "indice": i,
                "pergunta": item.get("pergunta", ""),
                "resposta_original": resposta,
            })

    with open(os.path.join(DADOS, "banco.json"), "w", encoding="utf-8") as f:
        json.dump(banco, f, ensure_ascii=False)
    with open(os.path.join(DADOS, "pendentes.json"), "w", encoding="utf-8") as f:
        json.dump(fila, f, ensure_ascii=False, indent=1)

    palavras = sum(len(x["resposta_original"].split()) for x in fila)
    print(f"itens no banco ......... {total}")
    print(f"sem resposta (null) .... {nulos}")
    print(f"já convertidos ......... {ja_ok}")
    print(f"pendentes .............. {pendente}   ({palavras:,} palavras de origem)")
    print()
    por_materia = {}
    for x in fila:
        por_materia[x["materia"]] = por_materia.get(x["materia"], 0) + 1
    for m, n in sorted(por_materia.items(), key=lambda kv: -kv[1]):
        print(f"  {m:28} {n:>4}")
    print(f"\n-> dados/pendentes.json gravado. Próximo: python 2_enviar_lote.py")


if __name__ == "__main__":
    main()
