# Pipeline — refino das 718 respostas · **Sabatinando**

> **AVISO DE ESTADO (15/08/2026).** Esta pasta contém dados e HTMLs intermediários de uma linha editorial anterior. Ela não é publicável. A interface canônica é `../minha-banca.NOVO_3.html`; qualquer incorporação deve preservar essa interface, resolver `PONTOS-A-VERIFICAR.md` e passar por revisão jurídica humana.

> Nome definitivo do produto: **Sabatinando**. Ainda por renomear: o arquivo `minha-banca.html`, o subdomínio `minha-banca.netlify.app`, e os arquivos `pitch-sabatinalab.md` e `prompt-refatoracao-sabatinalab.md` da pasta do site. Deixe para depois do refino — renomear o HTML no meio do processo quebraria os caminhos dos scripts.

Testado com o `minha-banca.html` atual: extrai 750 itens, reconhece os 86 já prontos, remonta o arquivo e passa no `node --check`.

**Estado:** 86 convertidos · 32 nulos · **632 pendentes**
**Custo estimado do que falta:** US$ 7,08 em Sonnet 5 · US$ 11,79 em Opus 5 (batch, uma vez só)

---

## Preparar — **JÁ FEITO, não repetir**

Ambiente configurado em 4 de agosto de 2026. Nada aqui precisa ser refeito:

- Biblioteca `anthropic` instalada
- Chave da API salva na variável `ANTHROPIC_API_KEY` — **não peça para rodar `setx` de novo**
- Créditos comprados no Console
- Caminhos longos habilitados no Windows

Só refaça o `setx` se apagar a chave no Console e criar outra.

## Rodar

```
cd Desktop\files\pipeline

# 1. montar a fila (releia sempre que colher um lote — ele recalcula o que falta)
py 1_extrair.py "CAMINHO\minha-banca.html"

# 2. conferir o custo antes de gastar
py 2_enviar_lote.py --estimar

# 3. TESTE com 5 itens — leia as 5 respostas antes de liberar as 632
py 2_enviar_lote.py --teste 5

# 4. aprovado o padrão, mande por matéria (mais fácil de revisar)
py 2_enviar_lote.py --materia direitos_humanos
py 2_enviar_lote.py --materia difusos_coletivos
...
# ou tudo de uma vez
py 2_enviar_lote.py

# 5. remontar o HTML e validar
py 3_mesclar.py "CAMINHO\minha-banca.html"
```

O passo 5 grava `minha-banca.NOVO.html` — **nunca sobrescreve o original.** Confira no navegador antes de trocar.

Se o terminal fechar no meio do passo 4, o lote continua rodando no servidor:

```
py 2_enviar_lote.py --colher msgbatch_xxxxx    # o id fica em dados/ultimo_lote.txt
```

## Como está organizado

| | |
|---|---|
| `prompt_sistema.md` | As regras de reescrita. **É aqui que se ajusta a qualidade** — mexeu, roda o `--teste 5` de novo. |
| `1_extrair.py` | Lê o HTML e monta `dados/pendentes.json`. Pula o que já está pronto. |
| `2_enviar_lote.py` | Envia à Batch API e grava em `resultados/respostas_<materia>.json`. |
| `3_mesclar.py` | Remonta o HTML, valida os 750 itens, roda a varredura de resíduos e o `node --check`. |

Retomável por construção: rodar `1_extrair.py` de novo sempre recalcula o que falta. Item que deu erro volta para a fila sozinho.

## Decisões aplicadas

- **Cobertura do enunciado:** se o enunciado pede algo que a resposta original não traz, **completa**. Era a decisão em aberto do `RETOMAR.md`; agora está fixada no `prompt_sistema.md` e vale igual para os 632.
- **Registro da Parte I: transcrição da fala do candidato.** Pessoal, com primeira pessoa e marcadores orais, frases de 12 a 20 palavras, sem ponto e vírgula. Não é padrão de resposta impessoal — ver `COMPARACAO-TOM.md` para o antes e depois.
- **Marcador ≠ rótulo.** O texto guarda `##FALA##`, `##ROTEIRO##` e `##VERIFICAR##`, que são internos e invisíveis. Os títulos exibidos no site são outra coisa e mudam sem reprocessar nada.
- Norma revogada ou superada: corrigir direto no texto, sem nota.
- Reperguntas já vêm integradas ao enunciado — não mover nada.
- `null` permanece `null`; item que perder todo o conteúdo vira `null`.
- HC 127.900/AM: usar "março de 2016" (o material tinha duas datas divergentes).
- "Supervisão por ricochete" é conceito legítimo — André de Carvalho Ramos, 2006 — e deve ser preservado. Estava na minha lista de dúvidas; a fonte foi confirmada.

## Rótulos a alterar no site

Na função `showResposta(item)`, que escreve em `#espelhoText`, os sub-cartões passam a exibir:

| Marcador interno | Título exibido |
|---|---|
| `##FALA##` | Padrão de resposta esperado |
| `##ROTEIRO##` | O que o examinador espera que você domine |
| `##VERIFICAR##` | — não é exibido; o `3_mesclar.py` já o remove do conteúdo |

Os 86 itens já convertidos continuam válidos: os marcadores não mudaram.

## Relatório de conferência

Cada item pode trazer um bloco `##VERIFICAR##` com pontos que exigem seu olho — data divergente, citação não confirmada, conteúdo completado que merece revisão de mérito. O `3_mesclar.py` retira esse bloco do conteúdo do site e consolida tudo em **`PONTOS-A-VERIFICAR.md`**, com caixa de seleção por item.

## Pendências conhecidas do RETOMAR.md

Não são resolvidas pelo pipeline — exigem sua decisão:

- `processo_penal|37` — conferir o desfecho do Tema 1087 do STF. Está como controvérsia pendente.
- `processo_penal|35` — reescrito com a Lei 13.964/2019 (art. 492, I, "e") e a orientação do STF sobre execução imediata no júri. Confirmar o recorte.
- Os 86 itens já convertidos foram feitos **antes** da decisão de completar o enunciado. Vale repassar `consumidor|2`, onde você manteve fiel, para uniformizar.

## Depois

Quando os 632 estiverem prontos, o passo seguinte da arquitetura é tirar os dados do HTML de vez: um JSON por matéria, o site lendo de lá. Aí você edita uma questão sem tocar em 3,3 MB de arquivo, e o mesmo conteúdo serve para o site e para o seu estudo.
