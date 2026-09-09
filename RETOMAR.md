# Minha Banca — retomada

> **DOCUMENTO HISTÓRICO (04/08/2026).** Este roteiro descreve uma etapa editorial anterior e não representa o estado publicável atual. A fonte canônica da interface é `minha-banca.NOVO_3.html`; não substitua esse arquivo pelos HTMLs do pipeline. Antes de incorporar respostas processadas, conclua `pipeline/PONTOS-A-VERIFICAR.md`, valide o mérito jurídico e faça uma mesclagem controlada conforme `PENDENCIAS.md`.

Cole este arquivo na nova conversa junto com os anexos. O container zera entre conversas.

## Anexar sempre
1. `RESPOS_1.TXT` — respostas originais, 718 itens, formato `[dpeq|materia|indice] texto`, `|||` = quebra de parágrafo
2. `enunciados.txt` — 749 enunciados, mesmo formato (falta só `eca|37`)
3. Os `respostas_<materia>.json` já prontos (para não refazer)

## Feito (68 itens · 4 matérias completas)
| matéria | itens | arquivo |
|---|---|---|
| empresarial | 5/5 | respostas_empresarial.json |
| consumidor | 5/5 | respostas_consumidor.json |
| criminologia | 14/14 (+1 null) | respostas_criminologia.json |
| processo_penal | 44/44 COMPLETA (12 e 13 são null) | respostas_processo_penal.json |

## Pendente (650 itens)
direitos_humanos 58 · difusos_coletivos 90 · principios_institucionais 100 ·
civil 116 · dpe_ba_2022 138 · eca 148

Ordem combinada: menores primeiro. Matéria grande = quebrar em levas de ~10 mil palavras de origem.

## Formato do campo resposta
```
##FALA## ||| <fala oral, 120-250 palavras, natural, 1ª pessoa quando couber>
||| ##ROTEIRO## ||| SUBTÍTULO EM MAIÚSCULAS ||| <conteúdo> ||| OUTRO SUBTÍTULO ||| <conteúdo>
```
Subtítulos derivados do caso concreto, nunca lista fixa. Uma linha por item. `null` permanece `null`.

## Decisões já tomadas
- Norma revogada/superada: **corrigir direto no texto, sem nota**
- Reperguntas: os enunciados já vêm com elas integradas — não mover nada
- Preservar teses, dispositivos, súmulas e julgados do original; não inventar fundamento novo
- Cortar: cabeçalho "Ponto do edital"/"Material usado", URLs de curso, "Tema relacionado com...",
  metadados de incidência em prova, notas de rodapé soltas, hedging e narração do candidato
- Observação meta vira vetor: incorporar o conteúdo substantivo que ela sugere, descartar a instrução

## Decisão em aberto
Quando o enunciado pede algo que a resposta original não traz (ex.: `consumidor|2` pede as
excludentes e elas não estão lá), completar com o conteúdo faltante ou manter fiel ao original?
Em `processo_penal|4` completei com o art. 69 do CPP, e no 18 completei as modalidades de prisão
cautelar; em `consumidor|2` mantive como estava. Padrão ainda não fixado.

## A verificar antes de fechar
- data da modulação do HC 127.900/AM: o material cita 10/03/2016 (item 33) e 11/03/2016 (item 34).
  Escrevi "11 de março" no item 14 e "março de 2016" nos itens 33, 34 e 40 — uniformizar.
- `processo_penal|37`: conferir o desfecho do Tema 1087 do STF (cassação de absolvição fundada no
  quesito genérico). Deixei como controvérsia pendente.
- `processo_penal|35`: reescrito com a Lei 13.964/2019 (art. 492, I, "e") e com a orientação do STF
  favorável à execução imediata no júri — confirmar o recorte.

## Armadilhas da varredura final
- `REVISÃO`: nem em maiúsculas serve — "REVISÃO CRIMINAL", "REVISÃO PERIÓDICA" são subtítulos legítimos.
  Buscar o padrão editorial: `REVISÃO\s*\d` ou "comentários da revisora"
- usar word boundary — `REVISÃO` sem isso casa dentro de "P**revisão** legal"
- evitar escrever "salvo engano justificável" (CDC art. 42); usar "ressalvada a hipótese de engano justificável"
- pergunta retórica didática na FALA é permitida; o que se barra é interrogativa encadeada de banca
- há tabelas achatadas no material de origem (ex.: `processo_penal|9`, colunas intercaladas linha a
  linha virando frases sem sentido) — só se detectam lendo o item

## Etapas finais (só depois de todas as matérias)
1. mesclar os json em `DPE_ORAL_QUESTOES` dentro do `minha-banca.html`
2. trocar a linha do `const DPE_ORAL_QUESTOES = ` inteira, `json.dumps(..., ensure_ascii=False)`
3. validar com `node --check` sobre o conteúdo do `<script>`
4. conferir 750 itens e 100% das respostas não nulas com os dois marcadores
5. alterar `showResposta(item)` (escreve em `#espelhoText`) para dividir pelos marcadores e renderizar
   dois sub-cartões, "Como falar" e "Roteiro de conteúdo", com `.sub-card`, `.sub-title`,
   `.espelho-text`, `.modelo-card`. Marcadores não podem aparecer para o usuário.
