#!/usr/bin/env python3
"""
5_classificar.py — atribui disciplina às questões que estão na gaveta de concurso.

As 150 questões de `dpe_ba_2022` estão agrupadas por CONCURSO, não por matéria.
Este script pergunta ao modelo a que disciplina cada uma pertence e grava o
resultado num arquivo à parte. Não altera o HTML e não interfere na reescrita.

Tarefa mecânica de rotulagem: roda em Haiku, custa centavos.

Uso:  py 5_classificar.py .\\minha-banca.html --estimar
      py 5_classificar.py .\\minha-banca.html
      py 5_classificar.py .\\minha-banca.html --colher msgbatch_xxx

Gera: dados/disciplinas_dpe_ba.json   {"0": "civil", "1": "eca", ...}
      CLASSIFICACAO.md                relatório para conferência
"""
import json, os, sys, time, argparse
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados")
CONST = "const DPE_ORAL_QUESTOES"
BALDE = "dpe_ba_2022"
MODELO = "claude-haiku-4-5-20251001"
PRECO = (0.50, 2.50)          # batch, já com 50% de desconto

DISCIPLINAS = ["civil", "empresarial", "consumidor", "difusos_coletivos",
               "processo_penal", "criminologia", "eca",
               "principios_institucionais", "direitos_humanos"]

SISTEMA = f"""Você classifica questões de prova oral de Defensoria Pública por disciplina.

Responda com UMA palavra apenas, escolhida desta lista:
{chr(10).join('- ' + d for d in DISCIPLINAS)}

Significado de cada rótulo:
- civil: direito civil material — pessoas, bens, obrigações, contratos, responsabilidade, família, sucessões, reais
- empresarial: sociedades, títulos de crédito, falência e recuperação, propriedade industrial
- consumidor: CDC, relação de consumo, vícios, práticas abusivas, superendividamento
- difusos_coletivos: processo coletivo, ação civil pública, direitos difusos e homogêneos, saúde, meio ambiente, idoso, pessoa com deficiência
- processo_penal: inquérito, prisões, provas, procedimento, júri, execução penal, recursos criminais
- criminologia: teorias criminológicas, política criminal, seletividade, vitimologia, abolicionismo
- eca: criança e adolescente, ato infracional, medidas socioeducativas, acolhimento, adoção
- principios_institucionais: Defensoria Pública — LC 80/94, atribuições, prerrogativas, autonomia, carreira, assistência jurídica
- direitos_humanos: sistema interamericano, tratados, controle de convencionalidade, Corte IDH, direitos fundamentais internacionais

Se a questão for de disciplina fora da lista — constitucional, administrativo, tributário, penal material —, responda:
outra:<nome da disciplina em uma palavra>

Se cobrir mais de uma, escolha a predominante. Sem explicação, sem pontuação final, sem aspas. Só o rótulo."""


def carregar(html):
    with open(html, encoding="utf-8") as f:
        for linha in f:
            if linha.lstrip().startswith(CONST):
                return json.loads(linha.split("=", 1)[1].strip().rstrip(";"))
    raise SystemExit(f"{CONST} não encontrada.")


def fila(banco):
    return [(i, it["pergunta"]) for i, it in enumerate(banco[BALDE])
            if (it.get("pergunta") or "").strip()]


def gravar_relatorio(mapa, perguntas):
    cont = Counter(mapa.values())
    with open(os.path.join(AQUI, "CLASSIFICACAO.md"), "w", encoding="utf-8") as f:
        f.write(f"# Disciplina das questões de `{BALDE}`\n\n")
        f.write(f"{len(mapa)} questões classificadas.\n\n")
        f.write("| Disciplina | Questões |\n|---|---|\n")
        for d, n in cont.most_common():
            f.write(f"| {d} | {n} |\n")
        fora = [k for k, v in mapa.items() if v.startswith("outra:")]
        if fora:
            f.write(f"\n## Fora das 9 disciplinas ({len(fora)})\n\n")
            f.write("Valem atenção: podem indicar disciplina que falta no site.\n\n")
            for k in fora:
                f.write(f"- `{BALDE}|{k}` → **{mapa[k]}** — {perguntas.get(int(k),'')[:160]}\n")
        f.write("\n## Conferência por amostra\n\n")
        for d in cont:
            ex = [k for k, v in mapa.items() if v == d][:2]
            for k in ex:
                f.write(f"- [ ] `{k}` → **{d}** — {perguntas.get(int(k),'')[:160]}\n")


def colher(cliente, batch_id, perguntas):
    while True:
        lote = cliente.messages.batches.retrieve(batch_id)
        if lote.processing_status == "ended":
            break
        c = lote.request_counts
        print(f"  processando... ok={c.succeeded} erro={c.errored} restam={c.processing}")
        time.sleep(30)

    mapa, erros, ui, uo = {}, [], 0, 0
    for linha in cliente.messages.batches.results(batch_id):
        idx = linha.custom_id.split("__")[-1]
        if linha.result.type != "succeeded":
            erros.append(idx); continue
        msg = linha.result.message
        r = "".join(b.text for b in msg.content
                    if getattr(b, "type", None) == "text").strip().lower().strip(".\"' ")
        if r not in DISCIPLINAS and not r.startswith("outra:"):
            erros.append(f"{idx} (resposta inesperada: {r[:40]})"); continue
        mapa[idx] = r
        ui += getattr(msg.usage, "input_tokens", 0)
        uo += getattr(msg.usage, "output_tokens", 0)

    os.makedirs(DADOS, exist_ok=True)
    caminho = os.path.join(DADOS, "disciplinas_dpe_ba.json")
    antigo = {}
    if os.path.exists(caminho):
        antigo = json.load(open(caminho, encoding="utf-8"))
    antigo.update(mapa)
    json.dump(antigo, open(caminho, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    gravar_relatorio(antigo, perguntas)

    custo = ui / 1e6 * PRECO[0] + uo / 1e6 * PRECO[1]
    print(f"\nclassificadas ...... {len(mapa)}")
    print(f"CUSTO REAL ......... US$ {custo:.3f}")
    for d, n in Counter(antigo.values()).most_common():
        print(f"  {d:28} {n:>4}")
    if erros:
        print(f"\n{len(erros)} sem classificação: {erros[:10]}")
    print("\n-> dados/disciplinas_dpe_ba.json  ·  CLASSIFICACAO.md")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("html")
    p.add_argument("--estimar", action="store_true")
    p.add_argument("--colher")
    a = p.parse_args()

    banco = carregar(a.html)
    itens = fila(banco)
    perguntas = dict(itens)
    print(f"questões em {BALDE}: {len(itens)}")

    if a.estimar:
        ent = len(itens) * (len(SISTEMA.split()) * 1.6) + \
              sum(len(q.split()) * 1.6 for _, q in itens)
        sai = len(itens) * 8
        print(f"custo estimado: US$ {ent/1e6*PRECO[0] + sai/1e6*PRECO[1]:.3f}  (Haiku, batch)")
        return

    from anthropic import Anthropic
    cliente = Anthropic()

    if a.colher:
        return colher(cliente, a.colher, perguntas)

    pedidos = [{
        "custom_id": f"cls__{i}",
        "params": {
            "model": MODELO,
            "max_tokens": 20,
            "system": [{"type": "text", "text": SISTEMA,
                        "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": q}],
        },
    } for i, q in itens]

    if input(f"classificar {len(pedidos)} questões em Haiku? [s/N] ").strip().lower() != "s":
        return print("cancelado.")
    lote = cliente.messages.batches.create(requests=pedidos)
    print(f"lote enviado: {lote.id}")
    with open(os.path.join(DADOS, "ultimo_lote_cls.txt"), "w") as f:
        f.write(lote.id)
    colher(cliente, lote.id, perguntas)


if __name__ == "__main__":
    main()
