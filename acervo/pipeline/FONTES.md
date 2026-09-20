# De onde veio cada parte do banco

Reconstruído em 4 de agosto de 2026 a partir dos arquivos enviados na sessão "Speaking practice website" e do que os scripts de parsing leem.

Todos os PDFs de origem estão em:
`AppData\Roaming\Claude\local-agent-mode-sessions\...\local_a648a86f-...\uploads\`

---

## Compilados por disciplina — enviados em 2 de agosto, 11h25–11h26

| # | Arquivo | Disciplina no site | Autor do compilado |
|---|---|---|---|
| 1 | `1. CIVIL FCC - COMPILADO - CESAR LEONARDO.pdf` | civil | Cesar Leonardo |
| 2 | `2. ORAL EMPRESARIAL FCC - COMPILADO - CESAR LEONARDO.pdf` | empresarial | Cesar Leonardo |
| 4 | `4. ORAL CONSUMIDOR FCC - COMPILADO - CESAR LEONARDO.pdf` | consumidor | Cesar Leonardo |
| 5 | `5. ORAL DIFUSOS E COLETIVOS FCC - COMPILADO - ZAPATTA.pdf` | difusos_coletivos | Zapatta |
| 7 | `7. ORAL PROCESSO PENAL FCC - COMPILADO - PATRICK CACICEDO.pdf` | processo_penal | Patrick Cacicedo |
| 8 | `8. COMPILADO CRIMINOLOGIA - PATRICK CACICEDO.pdf` | criminologia | Patrick Cacicedo |
| 10 | `10. ORAL DPE-PB - ECA COM RESPOSTAS.pdf` | eca | — (prova da **DPE-PB**) |
| 11 | `11. ORAL ECA FCC - COMPILADO - FRASSETO.pdf` | eca | Frasseto |
| 13 | `13. ORAL FCC - COMPILADO - PRINCIPIOS INSTITUCIONAIS - ZAPATTA.pdf` | principios_institucionais | Zapatta |
| 14 | `14. COMPILADO DIREITOS HUMANOS- FRASSETO.pdf` | direitos_humanos | Frasseto |

## Material específico da DPE-BA 2022

| Arquivo | Onde entrou |
|---|---|
| `Compilado-DPE_BA 2022- conteúdo +questões.pdf` (5,6 MB) | gaveta `dpe_ba_2022`, 150 questões |
| `DPE_BA 2022- como foi no dia.pdf` | constante `DPE_DIA` — os relatos de candidatos sobre o dia da prova |
| `Edital_DPE_BA_Conteudo_Programatico_COMPLETO (1).xlsx` | conteúdo programático |

## Outras seções do site

| Arquivo | Onde entrou |
|---|---|
| `GUIA_OAB_PENAL (7).pdf` | seção OAB — virou `guide_raw.txt` → `guide.txt` → `oab_data*.js` |
| `QUESTÃO / PADRÃO DE RESPOSTA - ANALISTA LEGISLATIVO...md` | provas do TCDF e Câmara dos Deputados |

---

## Duas coisas que precisam da sua atenção

### 1. Faltam quatro compilados na numeração

A sequência enviada é **1, 2, 4, 5, 7, 8, 10, 11, 13, 14**. Estão ausentes os de número **3, 6, 9 e 12**.

Não é acaso: a numeração é de uma coleção. Quatro compilados existem e nunca foram enviados.

E isso conversa diretamente com o que a classificação da DPE-BA revelou — o site não tinha `constitucional` (24 questões) nem `penal` (13), e ainda sobram administrativo, financeiro e ambiental sem casa. É bem provável que 3, 6, 9 e 12 sejam justamente essas disciplinas.

**Vale procurar esses quatro arquivos.** Se existirem, cada um rende de 40 a 150 questões novas — mais do que a DPE-BA inteira.

### 2. As questões de ECA têm duas origens diferentes

`10. ORAL DPE-PB - ECA COM RESPOSTAS.pdf` é prova da **Defensoria da Paraíba**, não da Bahia. Os demais compilados são de material FCC genérico.

Isso importa para o campo `aplicacoes` do modelo de dois eixos: parte das questões de ECA deve receber `DPE-PB`, não `DPE-BA`. Se todas forem marcadas como DPE-BA, a navegação por concurso vai mentir.

Ao preencher `aplicacoes`, trate cada compilado separadamente e verifique a origem antes de atribuir concurso. Compilado de banca não é o mesmo que prova aplicada.

---

## Os quatro que faltavam — ENCONTRADOS

Estão em `Downloads\FONTES REMANESCENTES`. Todos com texto extraível: **não precisa OCR nem converter para MD.**

| # | Arquivo | Páginas | Disciplina |
|---|---|---|---|
| 3 | `3. ORAL PROCESSO CIVIL FCC - COMPILADO - CESAR LEONARDO.pdf` | 269 | `processo_civil` — **nova** |
| 6 | `6. ORAL PENAL FCC - COMPILADO - PATRICK CACICEDO.pdf` | 88 | `penal` — já decidida |
| 9 | `9. COMPILADO EXECUÇÃO PENAL -- PATRICK CACICEDO.pdf` | 156 | `execucao_penal` — **nova** |
| 12 | `12. ORAL CONSTITUCIONAL - FCC - COMPILADO - ZAPATTA.pdf` | 197 | `constitucional` — já decidida |

710 páginas. O site iria de 9 para **13 disciplinas** (ou 12, se execução penal entrar dentro de penal — decisão dela).

### A estrutura é regular e parseável

Amostra do arquivo 6, páginas 6 a 8:

```
2- (DPE ES) Fale sobre a Desistência voluntária e arrependimento eficaz;

A desistência voluntária e o arrependimento eficaz estão previstos no artigo 15...

3- (DPE ES) É possível desistência voluntária no crime de estupro?

Prevalece na doutrina que...
```

Padrão: `^\s*(\d+)-\s*\(([^)]+)\)\s*(enunciado)` e a resposta vai até o próximo número. Um parser de regex resolve — não precisa de modelo para separar pergunta de resposta.

**E o mais valioso: o concurso de origem vem no próprio enunciado**, entre parênteses — `(DPE ES)`. É exatamente o dado que o campo `aplicacoes` do modelo de dois eixos precisa, e ele vem de graça no parsing. Aqui não se repete o problema do ECA/DPE-PB: a proveniência é explícita item a item.

### O que falta fazer com eles

1. **Parser** — script novo, `6_importar_compilado.py`: extrai o texto do PDF, quebra pelo padrão numerado, captura o concurso dos parênteses, e grava no formato `{pergunta, resposta, disciplina, aplicacoes}`. Não gasta API.
2. **Conferência do parsing** — contar itens por arquivo, achar respostas vazias, achar enunciados sem número. Não gasta API.
3. **Reescrita no padrão** — o `2_enviar_lote.py` atual serve sem nenhuma mudança. Custo em Sonnet: ~US$ 0,035 por item.
4. **Classificação** — desnecessária: a disciplina vem do nome do arquivo.
5. **Integração ao HTML** — depende de criar as chaves das disciplinas novas.

Não há como estimar o custo antes do passo 1: 710 páginas podem render de 150 a 600 questões. **O passo 1 é gratuito e responde isso.** Faça-o antes de decidir qualquer gasto.

## Regra para daqui em diante

Todo material novo que entrar no banco deve ser registrado aqui na hora, com: nome do arquivo, disciplina de destino, concurso e ano de origem, e se é prova aplicada ou compilado de estudo.

É o que evita ter de reconstruir isso de novo — e é a informação que o campo `aplicacoes` precisa para existir.
