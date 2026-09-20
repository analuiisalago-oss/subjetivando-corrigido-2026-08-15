#!/usr/bin/env python3
"""
4_duplicatas.py — procura questões repetidas entre dpe_ba_2022 e as disciplinas.

Não chama a API, não gasta nada. Só lê e compara.

Uso:  py 4_duplicatas.py .\\minha-banca.html
      py 4_duplicatas.py .\\minha-banca.html --limite 0.45   (mais frouxo)

Gera: DUPLICATAS.md  com os pares suspeitos, do mais parecido para o menos.
"""
import json, os, sys, re, unicodedata, difflib
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
CONST = "const DPE_ORAL_QUESTOES"
BALDE_CONCURSO = "dpe_ba_2022"

# palavras vazias e jurídicas genéricas: aparecem em quase toda pergunta e
# inflam a semelhança sem dizer nada sobre o assunto
VAZIAS = set("""
a o as os um uma uns umas de do da dos das em no na nos nas por para com sem sob
e ou mas que se como qual quais quando onde quanto quantos qual é são ser está
seu sua seus suas este esta esse essa aquele aquela isso isto ao aos à às pelo
pela pelos pelas entre sobre até desde após antes durante contra também já não
há sim discorra fale explique disserte comente aponte cite indique diga sobre
possivel possível pode podem deve devem qual seria hipótese caso exemplo
direito lei artigo art norma jurídico jurídica
""".split())


def normalizar(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9\s]", " ", t)


def fichas(texto):
    return {p for p in normalizar(texto).split() if len(p) > 3 and p not in VAZIAS}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def carregar(html):
    with open(html, encoding="utf-8") as f:
        for linha in f:
            if linha.lstrip().startswith(CONST):
                return json.loads(linha.split("=", 1)[1].strip().rstrip(";"))
    raise SystemExit(f"{CONST} não encontrada.")


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    html = sys.argv[1]
    limite = 0.35
    if "--limite" in sys.argv:
        limite = float(sys.argv[sys.argv.index("--limite") + 1])

    banco = carregar(html)
    concurso, disciplinas = [], []
    for materia, itens in banco.items():
        alvo = concurso if materia == BALDE_CONCURSO else disciplinas
        for i, it in enumerate(itens):
            p = (it.get("pergunta") or "").strip()
            if p:
                alvo.append((materia, i, p, fichas(p)))

    print(f"{BALDE_CONCURSO}: {len(concurso)} questões")
    print(f"disciplinas:     {len(disciplinas)} questões")
    print(f"limite de semelhança: {limite}\n")

    pares = []
    for m1, i1, p1, f1 in concurso:
        melhor = None
        for m2, i2, p2, f2 in disciplinas:
            s = jaccard(f1, f2)
            if s >= limite and (melhor is None or s > melhor[0]):
                # confirma com comparação de sequência, que pega ordem das palavras
                seq = difflib.SequenceMatcher(None, normalizar(p1), normalizar(p2)).ratio()
                melhor = (s, seq, m2, i2, p2)
        if melhor:
            pares.append((melhor[0], melhor[1], m1, i1, p1, melhor[2], melhor[3], melhor[4]))

    pares.sort(reverse=True)
    alta = [x for x in pares if x[0] >= 0.6 or x[1] >= 0.75]
    media = [x for x in pares if x not in alta]

    print(f"suspeitas fortes ..... {len(alta)}")
    print(f"suspeitas fracas ..... {len(media)}")
    print(f"sem par .............. {len(concurso) - len(pares)}")
    econ = len(alta) * 0.035
    print(f"\nse as fortes forem mesmo repetidas, economiza US$ {econ:.2f} "
          f"e evita {len(alta)} questões duplicadas no site")

    with open(os.path.join(AQUI, "DUPLICATAS.md"), "w", encoding="utf-8") as f:
        f.write("# Questões possivelmente repetidas\n\n")
        f.write(f"Comparação entre as {len(concurso)} de `{BALDE_CONCURSO}` e as "
                f"{len(disciplinas)} das disciplinas.\n\n")
        f.write("Marque a caixa nas que **forem** a mesma questão. Para essas, "
                "em vez de reescrever o item do concurso, acrescente a aplicação "
                "`DPE-BA / 2022 / FCC / oral` à questão que já existe na disciplina.\n\n")
        for titulo, grupo in [("Suspeitas fortes", alta), ("Suspeitas fracas — conferir", media)]:
            if not grupo:
                continue
            f.write(f"\n## {titulo}\n\n")
            for s, seq, m1, i1, p1, m2, i2, p2 in grupo:
                f.write(f"- [ ] **{s:.0%} de palavras em comum · {seq:.0%} de texto**\n")
                f.write(f"  - `{m1}|{i1}` — {p1[:300]}\n")
                f.write(f"  - `{m2}|{i2}` — {p2[:300]}\n\n")
    print("\n-> DUPLICATAS.md")


if __name__ == "__main__":
    main()
