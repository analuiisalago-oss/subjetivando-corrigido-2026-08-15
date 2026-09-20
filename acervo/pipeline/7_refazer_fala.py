#!/usr/bin/env python3
"""
7_refazer_fala.py — refaz só a Parte I (##FALA##) das respostas já convertidas,
mantendo o ##ROTEIRO## (e ##VERIFICAR##) intocados.

Motivo: a especificação da fala mudou (ver ESTADO.md, "REGISTRO DA PARTE I —
corrigido"). As respostas já produzidas têm a fala no registro antigo.

Para não ancorar o modelo no texto antigo, ele NUNCA vê a ##FALA## anterior —
só a PERGUNTA e o ##ROTEIRO## já pronto, e escreve a fala do zero a partir daí.

Nunca sobrescreve resultados/ diretamente. Grava em resultados_fala/, no mesmo
formato (idx -> texto completo já remontado com a fala nova + o roteiro antigo).
Só depois de você ler e aprovar, rode --aplicar para mesclar em resultados/.

Uso:
    python 7_refazer_fala.py --estimar              # calcula custo, não envia
    python 7_refazer_fala.py --teste 5               # 5 itens espalhados, para conferir
    python 7_refazer_fala.py --materia civil          # uma matéria inteira
    python 7_refazer_fala.py                          # os 718 convertidos, todos
    python 7_refazer_fala.py --colher msgbatch_123     # colhe um lote já enviado
    python 7_refazer_fala.py --aplicar                 # mescla resultados_fala/ em resultados/
"""
import json, os, sys, time, argparse

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados")
RESULTADOS = os.path.join(AQUI, "resultados")
SAIDA = os.path.join(AQUI, "resultados_fala")
SEP = " ||| "

MODELO = "claude-sonnet-5"       # modelo em uso na produção (ver ESTADO.md)
MAX_TOKENS = 8000                 # fala sozinha é curta (280-350 palavras), mas itens de
                                   # roteiro grande (800+ palavras) truncaram em 4000

# preço por milhão de tokens, já com o desconto de 50% do batch
PRECO = {
    "claude-sonnet-5": (1.50, 7.50),
    "claude-opus-5":   (2.50, 12.50),
    "claude-haiku-4-5-20251001": (0.50, 2.50),
}


def sistema() -> str:
    with open(os.path.join(AQUI, "prompt_fala.md"), encoding="utf-8") as f:
        return f.read()


def partir(texto: str):
    """Separa uma resposta já convertida em (fala_antiga, resto, roteiro_legivel).
    resto = tudo a partir de '##ROTEIRO##' (inclusive), pronto para remontar.
    roteiro_legivel = só o conteúdo (sem os marcadores), para mandar ao modelo."""
    partes = [p.strip() for p in texto.split(SEP)]
    if "##FALA##" not in partes or "##ROTEIRO##" not in partes:
        return None
    i_fala = partes.index("##FALA##")
    i_rot = partes.index("##ROTEIRO##")
    fala_antiga = partes[i_fala + 1]
    resto = SEP.join(partes[i_rot:])

    corpo = partes[i_rot + 1:]
    if "##VERIFICAR##" in corpo:
        corpo = corpo[:corpo.index("##VERIFICAR##")]
    blocos = []
    for i in range(0, len(corpo) - 1, 2):
        blocos.append(f"{corpo[i]}\n{corpo[i + 1]}")
    roteiro_legivel = "\n\n".join(blocos)
    return fala_antiga, resto, roteiro_legivel


def carregar_convertidos():
    """Varre resultados/respostas_*.json e cruza com dados/banco.json para pegar a pergunta.
    Só entram itens não-nulos, já no formato novo (##FALA##/##ROTEIRO##)."""
    with open(os.path.join(DADOS, "banco.json"), encoding="utf-8") as f:
        banco = json.load(f)

    itens = []
    for arq in sorted(os.listdir(RESULTADOS)):
        if not arq.startswith("respostas_") or not arq.endswith(".json"):
            continue
        materia = arq[len("respostas_"):-len(".json")]
        with open(os.path.join(RESULTADOS, arq), encoding="utf-8") as f:
            dados = json.load(f)
        for idx, texto in dados.items():
            if not isinstance(texto, str):
                continue
            partido = partir(texto)
            if not partido:
                continue
            fala_antiga, resto, roteiro_legivel = partido
            pergunta = banco.get(materia, [{}] * (int(idx) + 1))[int(idx)].get("pergunta", "") \
                if int(idx) < len(banco.get(materia, [])) else ""
            itens.append({
                "id": f"{materia}__{idx}",
                "materia": materia,
                "idx": idx,
                "pergunta": pergunta,
                "fala_antiga": fala_antiga,
                "resto": resto,
                "roteiro_legivel": roteiro_legivel,
            })
    return itens


def amostra_espalhada(itens, limite):
    por = {}
    for x in itens:
        por.setdefault(x["materia"], []).append(x)
    escolha, i = [], 0
    while len(escolha) < limite and any(por.values()):
        for m in list(por):
            if por[m] and len(escolha) < limite:
                escolha.append(por[m].pop(i % len(por[m])))
        i += 1
    return escolha


def usuario(item: dict) -> str:
    return (f"PERGUNTA:\n{item['pergunta']}\n\n"
            f"ROTEIRO (conteúdo já pronto e correto — baseie a fala nele, "
            f"não repita como lista, não acrescente fato que não esteja aqui):\n"
            f"{item['roteiro_legivel']}")


def estimar(fila, modelo):
    sis = sistema()
    tok_sis = len(sis.split()) * 1.6
    ent = sum((len(usuario(x).split()) * 1.6) for x in fila) + tok_sis * len(fila)
    sai = len(fila) * 550          # fala sozinha ~300 palavras * ~1.8 tok/palavra
    pe, ps = PRECO.get(modelo, PRECO[MODELO])
    custo = ent / 1e6 * pe + sai / 1e6 * ps
    print(f"itens ............ {len(fila)}")
    print(f"entrada estimada . {ent/1e6:.2f}M tokens")
    print(f"saída estimada ... {sai/1e6:.2f}M tokens")
    print(f"modelo ........... {modelo}")
    print(f"CUSTO ESTIMADO ... US$ {custo:.2f}  (batch, 50% de desconto)")
    print("\nEstimativa aproximada. O valor real aparece no Console após o processamento.")


def enviar(fila, modelo):
    from anthropic import Anthropic
    cliente = Anthropic()
    sis = sistema()
    pedidos = [{
        "custom_id": x["id"],
        "params": {
            "model": modelo,
            "max_tokens": MAX_TOKENS,
            "system": [{"type": "text", "text": sis,
                        "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": usuario(x)}],
        },
    } for x in fila]

    lote = cliente.messages.batches.create(requests=pedidos)
    print(f"lote enviado: {lote.id}   ({len(pedidos)} itens)")
    with open(os.path.join(DADOS, "ultimo_lote_fala.txt"), "w") as f:
        f.write(lote.id)
    return lote.id


def colher(batch_id):
    from anthropic import Anthropic
    cliente = Anthropic()
    os.makedirs(SAIDA, exist_ok=True)

    # precisa do 'resto' (roteiro antigo) e da fala antiga para remontar e comparar;
    # reconstrói o índice a partir do que já está convertido
    indice = {x["id"]: x for x in carregar_convertidos()}

    while True:
        lote = cliente.messages.batches.retrieve(batch_id)
        if lote.processing_status == "ended":
            break
        c = lote.request_counts
        print(f"  processando... ok={c.succeeded} erro={c.errored} restam={c.processing}")
        time.sleep(60)

    por_materia, erros = {}, []
    uso_in = uso_out = uso_cache = 0
    modelo_usado = None
    comparacoes = []

    for linha in cliente.messages.batches.results(batch_id):
        cid = linha.custom_id
        materia, idx = cid.rsplit("__", 1)
        if linha.result.type != "succeeded":
            erros.append((cid, linha.result.type))
            continue
        msg = linha.result.message

        if getattr(msg, "stop_reason", None) == "max_tokens":
            erros.append((cid, "truncada (max_tokens) — refaça depois"))
            continue

        nova_fala = "".join(b.text for b in msg.content
                             if getattr(b, "type", None) == "text").strip()
        if nova_fala.startswith("```"):
            nova_fala = nova_fala.strip("`").split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        if not nova_fala:
            erros.append((cid, "resposta vazia"))
            continue

        original = indice.get(cid)
        resto = original["resto"] if original else "##ROTEIRO##"
        texto_completo = SEP.join(["##FALA##", nova_fala, resto])
        por_materia.setdefault(materia, {})[idx] = texto_completo

        if original:
            comparacoes.append({
                "id": cid,
                "palavras_antes": len(original["fala_antiga"].split()),
                "palavras_depois": len(nova_fala.split()),
                "tem_ponto_virgula": ";" in nova_fala,
            })

        modelo_usado = modelo_usado or getattr(msg, "model", None)
        u = msg.usage
        uso_in += getattr(u, "input_tokens", 0)
        uso_out += getattr(u, "output_tokens", 0)
        uso_cache += getattr(u, "cache_read_input_tokens", 0) or 0
        uso_in += getattr(u, "cache_creation_input_tokens", 0) or 0

    for materia, itens in por_materia.items():
        caminho = os.path.join(SAIDA, f"respostas_{materia}.json")
        antigos = {}
        if os.path.exists(caminho):
            with open(caminho, encoding="utf-8") as f:
                antigos = json.load(f)
        antigos.update(itens)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(antigos, f, ensure_ascii=False, indent=1)
        print(f"  {materia:28} +{len(itens):>4}  -> resultados_fala/respostas_{materia}.json")

    chave = next((k for k in PRECO if modelo_usado and k in modelo_usado), MODELO)
    pe, ps = PRECO[chave]
    custo = uso_in / 1e6 * pe + uso_cache / 1e6 * pe * 0.1 + uso_out / 1e6 * ps
    print(f"\nmodelo do lote ..... {modelo_usado or chave}")
    print(f"tokens de entrada .. {uso_in:,}")
    print(f"lidos do cache ..... {uso_cache:,}  (custam 10%)")
    print(f"tokens de saída .... {uso_out:,}")
    print(f"CUSTO REAL ......... US$ {custo:.2f}")
    if por_materia:
        n = sum(len(v) for v in por_materia.values())
        print(f"por item ........... US$ {custo/n:.4f}   "
              f"-> 718 itens sairiam por US$ {custo/n*718:.2f}")

    if comparacoes:
        print(f"\nConferência rápida ({len(comparacoes)} itens):")
        for c in comparacoes:
            aviso = "  <- TEM PONTO E VÍRGULA" if c["tem_ponto_virgula"] else ""
            print(f"  {c['id']:35} {c['palavras_antes']:>3} -> {c['palavras_depois']:>3} palavras{aviso}")

    if erros:
        print(f"\n{len(erros)} erros:")
        for cid, tipo in erros[:20]:
            print(f"  {cid}: {tipo}")


def aplicar():
    """Mescla resultados_fala/ em resultados/ — só rode depois de conferir."""
    if not os.path.isdir(SAIDA):
        return print("resultados_fala/ não existe. Nada para aplicar.")
    total = 0
    for arq in sorted(os.listdir(SAIDA)):
        if not arq.startswith("respostas_") or not arq.endswith(".json"):
            continue
        with open(os.path.join(SAIDA, arq), encoding="utf-8") as f:
            novos = json.load(f)
        caminho_final = os.path.join(RESULTADOS, arq)
        antigos = {}
        if os.path.exists(caminho_final):
            with open(caminho_final, encoding="utf-8") as f:
                antigos = json.load(f)
        antigos.update(novos)
        with open(caminho_final, "w", encoding="utf-8") as f:
            json.dump(antigos, f, ensure_ascii=False, indent=1)
        print(f"  {arq}: {len(novos)} itens aplicados em resultados/")
        total += len(novos)
    print(f"\n{total} respostas atualizadas em resultados/. Rode 3_mesclar.py para gerar o HTML novo.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--estimar", action="store_true")
    p.add_argument("--teste", type=int)
    p.add_argument("--materia")
    p.add_argument("--modelo", default=MODELO)
    p.add_argument("--sonnet", action="store_true")
    p.add_argument("--opus", action="store_true")
    p.add_argument("--colher")
    p.add_argument("--aplicar", action="store_true")
    a = p.parse_args()

    if a.aplicar:
        return aplicar()

    if a.sonnet:
        a.modelo = "claude-sonnet-5"
    if a.opus:
        a.modelo = "claude-opus-5"
    if a.modelo not in PRECO:
        raise SystemExit(
            f"\nModelo '{a.modelo}' não existe. Confira se não sobrou letra colada no fim.\n"
            f"Válidos: {', '.join(PRECO)}\n"
            f"Mais fácil: use --sonnet ou --opus.\n")

    if a.colher:
        return colher(a.colher)

    fila = carregar_convertidos()
    if a.materia:
        fila = [x for x in fila if x["materia"] == a.materia]
    if a.teste:
        fila = amostra_espalhada(fila, a.teste)

    if not fila:
        return print("nada para refazer.")

    if a.estimar:
        return estimar(fila, a.modelo)

    estimar(fila, a.modelo)
    if input("\nenviar? [s/N] ").strip().lower() != "s":
        return print("cancelado.")
    colher(enviar(fila, a.modelo))


if __name__ == "__main__":
    main()
