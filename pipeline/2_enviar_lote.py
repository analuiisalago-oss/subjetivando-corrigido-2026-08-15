#!/usr/bin/env python3
"""
2_enviar_lote.py — envia os pendentes para a Message Batches API e grava os resultados.

Batch = metade do preço da API normal, e não consome nada da sua franquia do plano Pro.
O processamento é assíncrono: envia, espera, colhe. Pode fechar o terminal e rodar
`--colher <batch_id>` depois.

Pré-requisitos:
    pip install anthropic
    set ANTHROPIC_API_KEY=sk-ant-...        (Windows CMD)
    $env:ANTHROPIC_API_KEY="sk-ant-..."     (PowerShell)

Uso:
    python 2_enviar_lote.py --estimar              # só calcula custo, não envia
    python 2_enviar_lote.py --teste 5              # envia 5 itens para conferir o padrão
    python 2_enviar_lote.py --materia empresarial  # uma matéria por vez
    python 2_enviar_lote.py                        # tudo que está pendente
    python 2_enviar_lote.py --colher msgbatch_123  # colhe um lote já enviado
"""
import json, os, sys, time, argparse

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados")
SAIDA = os.path.join(AQUI, "resultados")

MODELO = "claude-opus-5"         # decisão: Opus. Use --modelo claude-sonnet-5 para baratear
MAX_TOKENS = 16000       # 3000 e 8000 truncavam; civil tem origens de 800+ palavras.
                         # É teto, não meta: só se paga o que for gerado de fato.

# preço por milhão de tokens, JÁ com o desconto de 50% do batch
PRECO = {
    "claude-sonnet-5": (1.50, 7.50),
    "claude-opus-5":   (2.50, 12.50),
    "claude-haiku-4-5-20251001": (0.50, 2.50),
}


def sistema() -> str:
    with open(os.path.join(AQUI, "prompt_sistema.md"), encoding="utf-8") as f:
        return f.read()


def usuario(item: dict) -> str:
    return (f"MATÉRIA: {item['materia']}\n\n"
            f"PERGUNTA:\n{item['pergunta']}\n\n"
            f"RESPOSTA ATUAL:\n{item['resposta_original']}")


def carregar_pendentes(materia=None, limite=None):
    with open(os.path.join(DADOS, "pendentes.json"), encoding="utf-8") as f:
        fila = json.load(f)
    if materia:
        fila = [x for x in fila if x["materia"] == materia]
    if limite:
        # amostra espalhada entre as matérias, não os N primeiros da mesma
        por = {}
        for x in fila:
            por.setdefault(x["materia"], []).append(x)
        amostra, i = [], 0
        while len(amostra) < limite and any(por.values()):
            for m in list(por):
                if por[m] and len(amostra) < limite:
                    amostra.append(por[m].pop(i % len(por[m])))
            i += 1
        fila = amostra
    return fila


def estimar(fila, modelo):
    sis = sistema()
    # ~1.6 tokens por palavra em português
    tok_sis = len(sis.split()) * 1.6
    ent = sum((len(usuario(x).split()) * 1.6) for x in fila) + tok_sis * len(fila)
    sai = len(fila) * 2900          # medido no lote de teste em Opus (inclui raciocínio)
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
            # cache_control no system: o prompt é idêntico em todos os pedidos,
            # então ele é cobrado uma vez em vez de 632
            "system": [{"type": "text", "text": sis,
                        "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": usuario(x)}],
        },
    } for x in fila]

    lote = cliente.messages.batches.create(requests=pedidos)
    print(f"lote enviado: {lote.id}   ({len(pedidos)} itens)")
    with open(os.path.join(DADOS, "ultimo_lote.txt"), "w") as f:
        f.write(lote.id)
    return lote.id


def colher(batch_id):
    from anthropic import Anthropic
    cliente = Anthropic()
    os.makedirs(SAIDA, exist_ok=True)

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
    for linha in cliente.messages.batches.results(batch_id):
        cid = linha.custom_id
        materia, idx = cid.rsplit("__", 1)
        if linha.result.type != "succeeded":
            erros.append((cid, linha.result.type))
            continue
        msg = linha.result.message

        # resposta cortada por limite de tokens não presta: volta para a fila
        if getattr(msg, "stop_reason", None) == "max_tokens":
            erros.append((cid, "truncada (max_tokens) — será refeita"))
            continue

        # o modelo pode devolver blocos de raciocínio antes do texto;
        # junta só os blocos de tipo "text"
        texto = "".join(b.text for b in msg.content
                        if getattr(b, "type", None) == "text").strip()
        if not texto:
            erros.append((cid, "resposta sem bloco de texto"))
            continue
        if texto.startswith("```"):
            texto = texto.strip("`").split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        por_materia.setdefault(materia, {})[idx] = None if texto == "NULL" else texto

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
        print(f"  {materia:28} +{len(itens):>4}  -> resultados/respostas_{materia}.json")

    # custo real medido, com o preço do modelo que o lote de fato usou
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
              f"-> 632 itens sairiam por US$ {custo/n*632:.2f}")

    if erros:
        print(f"\n{len(erros)} erros:")
        for cid, tipo in erros[:20]:
            print(f"  {cid}: {tipo}")
        print("Rode 1_extrair.py de novo — os que falharam voltam para a fila.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--estimar", action="store_true")
    p.add_argument("--teste", type=int)
    p.add_argument("--materia")
    p.add_argument("--modelo", default=MODELO)
    p.add_argument("--sonnet", action="store_true", help="atalho para claude-sonnet-5")
    p.add_argument("--opus", action="store_true", help="atalho para claude-opus-5")
    p.add_argument("--colher")
    a = p.parse_args()

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

    fila = carregar_pendentes(a.materia, a.teste)
    if not fila:
        return print("nada pendente.")

    if a.estimar:
        return estimar(fila, a.modelo)

    estimar(fila, a.modelo)
    if input("\nenviar? [s/N] ").strip().lower() != "s":
        return print("cancelado.")
    colher(enviar(fila, a.modelo))


if __name__ == "__main__":
    main()
