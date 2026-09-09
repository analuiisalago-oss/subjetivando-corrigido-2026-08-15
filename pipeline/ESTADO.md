# Estado — Sabatinando · refino das 718 respostas

> **DOCUMENTO HISTÓRICO (04/08/2026).** Os números e comandos abaixo registram a execução daquele pipeline, mas não são o estado operacional do site em 15/08/2026. A interface canônica é `../minha-banca.NOVO_3.html`; os HTMLs desta pasta são intermediários e não devem ser publicados nem promovidos sobre a fonte atual. A incorporação do acervo revisado depende de resolver `PONTOS-A-VERIFICAR.md`, revisar o mérito jurídico e executar a pendência P1-12.

**Atualizado:** 4 de agosto de 2026 (à noite — script de refazer FALA)
**Para retomar:** abra chat novo, conecte `Desktop\files`, e mande só isto:
*"Leia `pipeline/ESTADO.md` e continue daí."*

---

## Refazer só a FALA — script novo, testado, pronto para o lote

`7_refazer_fala.py` + `prompt_fala.md`: refaz só a Parte I das respostas já convertidas, mantendo o ##ROTEIRO## intocado. Nunca vê a fala antiga (evita ancoragem) — manda só pergunta + roteiro. Nunca sobrescreve `resultados/` direto: grava em `resultados_fala/`; `--aplicar` mescla depois de conferido.

**Testado 3 vezes (5 itens cada), não repetir:**
- 1ª: sem calibração de tamanho no prompt — saiu 397 a 689 palavras (alvo era 280-350). Longe demais.
- 2ª: prompt pediu "teto rígido 350" — melhorou para 361-384. Ainda acima.
- 3ª: prompt calibrado para "alvo 260-300, teto 320" (compensando overshoot) — resultado 316-410, instável item a item, sem ganho líquido.
- **Decisão dela: aceitar a faixa real em vez de insistir no prompt.** `prompt_fala.md` corrigido para pedir 280-400 palavras (o que o modelo de fato entrega), sem teto artificial. Qualidade do texto em si sempre foi boa nas 3 rodadas: zero ponto e vírgula, zero primeira pessoa, formato correto. Único deslize recorrente: "por excelência" apareceu 2 de 3 vezes em `eca|0` especificamente — banido reforçado no prompt, sumiu na 3ª rodada.

Custo medido no teste: US$ 0,011/item -> **≈ US$ 7,87 para os 623 itens elegíveis** (bem abaixo dos US$ 15,57 estimados antes, porque a entrada agora é só o roteiro limpo, não o material bruto original).

**Próximo passo:** `py 7_refazer_fala.py --sonnet` (roda todos os 623 de uma vez, ou usar `--materia <nome>` para ir por partes) e depois `--aplicar` para mesclar em `resultados/`.

## Progresso — 4 de agosto de 2026, fim do dia

**579 de 718 convertidas (81%).** Tudo em **Sonnet 5**, custo por item estável entre US$ 0,031 e US$ 0,039.

| Matéria | Situação | US$ |
|---|---|---|
| direitos_humanos (40) | ✅ completa | 1,47 |
| principios_institucionais (99 de 100) | ✅ falta 1 item | 3,07 |
| civil (114) | ✅ completa (11 refeitos por truncamento) | 4,32 |
| eca (147) | ✅ completa | 5,23 |
| difusos_coletivos (89) | ✅ completa | 3,48 |
| **dpe_ba_2022 (138)** | ⬜ **adiada por decisão dela** | ~4,85 |
| principios_institucionais (1 avulso) | ⬜ pendente | ~0,04 |

Gasto até aqui ~US$ 18. Saldo no Console: US$ 7,15.

**Teto de tokens:** 3.000 truncava muito, 8.000 ainda truncou 11 itens de `civil`, **16.000 resolveu**. É teto, não meta — não encarece.

**Qualidade conferida:** os 40 de direitos_humanos saíram 40/40 no formato, zero problema de registro falado, fala com média de 214 palavras, metade gerando `##VERIFICAR##`.

**Falsos alarmes já descartados** — não reabrir: 6 subtítulos é permitido (a faixa é 3 a 7); "por excelência" no ROTEIRO é legítimo, o banimento vale só dentro da `##FALA##`.

## Decisão de produto — 4 de agosto de 2026

**O site passa a ter 11 disciplinas.** Foram criadas `constitucional` (24 questões) e `penal` (13), que não existiam e concentravam 37 das 150 questões da DPE-BA. Detalhes e consequências técnicas em `DESIGN-dois-eixos.md`.

Classificação das 150 já feita (`5_classificar.py`, US$ 0,042), rótulos normalizados em `dados/disciplinas_dpe_ba.json`. Cobertura: 143 de 150. As 7 restantes — administrativo 4, financeiro 1, filosofia 1, ambiental 1 — seguem como `outra:<nome>`, aguardando volume.

**Duplicação: verificada e inexistente** (`4_duplicatas.py`). `civil`, `empresarial` e `consumidor` não receberam nenhuma questão da DPE-BA — a gaveta do concurso é complementar às demais.

## Material novo encontrado — 4 compilados, 710 páginas

Em `Downloads\FONTES REMANESCENTES`: processo civil (269 pág), penal (88), execução penal (156), constitucional (197). Texto extraível, estrutura regular e parseável, com o concurso de origem dentro do próprio enunciado — ver `FONTES.md`.

**Próximo passo é gratuito:** escrever o parser (`6_importar_compilado.py`) e contar quantas questões saem. Só depois dá para estimar custo. Podem ser de 150 a 600 questões novas — possivelmente mais que todo o banco atual da DPE-BA.

Decisão pendente: `execucao_penal` vira disciplina própria ou entra dentro de `penal`?

## REGISTRO DA PARTE I — corrigido, 4 de agosto de 2026

**A especificação anterior estava errada e foi substituída.** A regra de "12 a 20 palavras por frase" produzia texto picotado. Frase falada dura **mais** que frase escrita.

O alvo agora: exposição oral formal, impessoal, com períodos de 30 a 50 palavras encadeados por subordinação, abrindo por resposta objetiva à pergunta, com citação por extenso, em 3 a 5 parágrafos e 280 a 350 palavras. Já está escrito na Parte I do `prompt_sistema.md`, com um par certo/errado embutido.

Saíram: primeira pessoa, marcadores de oralidade explícita ("Repare que", "Vou por partes", "Sustento que"), enumeração numerada ("Primeiro... Segundo..."). Entraram: conectores formais quando articulam de fato, atribuição impessoal no lugar de posição pessoal.

**Fonte da correção:** `RESPOSTAS EXEMPLARES.txt` (3 pares) mais o par da inamovibilidade discutido no chat. Vale acrescentar mais pares "atual versus exemplar" de disciplinas diferentes — foram mais úteis que qualquer lista de diretrizes.

**Consequência:** as 718 respostas já produzidas têm a FALA no registro antigo. Refazer só a FALA custa **US$ 15,57** (medido: a FALA é 31% do texto, o ROTEIRO 69% e fica intacto). Refazer tudo custaria US$ 25,13.

**Ao montar o passe de FALA, não mostre a FALA antiga ao modelo** — mande só o enunciado e o ROTEIRO, para não ancorar. E teste em 5 itens antes.

## Próximos passos imediatos

1. Item avulso de `principios_institucionais` (~US$ 0,04)
2. `py 3_mesclar.py .\minha-banca.html` — primeira remontagem com conteúdo real
3. **Verificar se `showResposta(item)` do site divide pelos marcadores.** Se não dividir, `##FALA##` aparece cru para o usuário
4. `dpe_ba_2022` quando ela quiser
5. Reprocessar os 86 antigos — 44 deles têm ponto e vírgula ou linguagem de papel na fala (ver `REVISAR-LINGUAGEM.md`)

## Onde parei

Pipeline construído e testado de ponta a ponta, sem chamar a API.
Falta a chave da API do Console. Nada mais bloqueia.

## Números

| | |
|---|---|
| Itens no banco | 750 |
| Nulos (permanecem nulos) | 32 |
| Já convertidos | 86 (12%) |
| **Pendentes** | **632** |
| Custo do que falta (**medido**, não estimado) | **US$ 19,96 Sonnet 5** · US$ 27,45+ Opus 5 |
| Crédito disponível | R$ 80 ≈ US$ 15,5 — **falta ~R$ 25 para o Sonnet** |
| Modelo | decisão reaberta: ver abaixo |

### Testes já rodados (não repetir)

- **Opus, 5 itens de `civil`** — US$ 0,0434/item. Rodou com teto de 3.000 tokens e **4 de 5 saíram truncadas**; foram devolvidas à fila. Sobrou `civil|3`. Teto corrigido para 8.000.
- **Sonnet, 5 itens espalhados** — US$ 0,0316/item. Conferência objetiva: marcadores corretos em 100%, fala de 193 a 248 palavras, 3 a 5 subtítulos, zero ponto e vírgula na fala, 3 com `##VERIFICAR##`. Um deslize: "por excelência" em `difusos_coletivos|0`.
- **Conclusão:** Sonnet cumpre a especificação. A vantagem do Opus é de mérito jurídico — mas o `##VERIFICAR##` e a skill `auditar-citacoes` cobrem parte disso.

Resultados dos testes estão em `resultados/`. Compare antes de decidir o modelo.

### Correções aplicadas no script

`MAX_TOKENS` 3.000 → 8.000 · resposta truncada volta à fila automaticamente · custo real usa a tabela do modelo efetivamente usado · `--teste` sorteia entre matérias · atalhos `--sonnet` e `--opus` com validação do nome.

Pendentes por matéria: eca 148 · dpe_ba_2022 138 · civil 116 · principios_institucionais 100 · difusos_coletivos 90 · direitos_humanos 40.

## Ambiente — leia antes de dar qualquer instrução técnica

Tudo isto **já está configurado**. Não mande refazer.

| | |
|---|---|
| Sistema | Windows 11, PowerShell |
| Comando do Python | **`py`, nunca `python`** |
| Por quê | o alias `python` está sequestrado pela Microsoft Store e sempre falha. O Python 3.12 está em `AppData\Local\Programs\Python\Python312` e o lançador `py` o encontra |
| Instalar pacote | `py -m pip install ...` — `pip` sozinho também não funciona |
| Biblioteca `anthropic` | instalada |
| Chave da API | salva em `ANTHROPIC_API_KEY`. **Não peça `setx` de novo** — só se ela for apagada no Console |
| Créditos | comprados no Console (conta separada do plano Pro) |
| Caminhos longos | habilitados |
| Pasta de trabalho | `cd $env:USERPROFILE\Desktop\files\pipeline` |

### Como conduzir a usuária no terminal

Ela não é da área técnica. O que já deu errado, e não deve repetir:

- **Um comando por vez.** Ela cola o próximo antes de o anterior terminar, e eles se fundem numa linha só. Peça um, espere o resultado, depois o próximo.
- **Cuidado com o prompt `enviar? [s/N]`.** Já aconteceu de o comando seguinte ser colado ali: o script leu como "não" e cancelou. E já aconteceu de o `s` ficar grudado no fim da linha anterior, virando `claude-sonnet-5s` — modelo inexistente, 5 chamadas perdidas. Hoje o script valida o nome e recusa.
- **Nunca use `echo $env:ANTHROPIC_API_KEY`.** Foi assim que a primeira chave vazou num print. Para conferir, use `$env:ANTHROPIC_API_KEY.Length`, que mostra só o tamanho (~108).
- **Lote roda no servidor.** Fechar o PowerShell, desligar o PC ou cair a internet não interrompe nada. Basta `--colher <id>`; o id fica em `dados\ultimo_lote.txt`.
- Ela manda prints do terminal. Leia a linha de comando inteira antes de diagnosticar — vários erros foram de digitação colada, não do script.

### Atalhos do script

`--sonnet` e `--opus` em vez de digitar o nome do modelo · `--estimar` calcula sem gastar · `--teste N` sorteia N itens de matérias diferentes · `--materia <nome>` roda uma só · `--colher <id>` retoma lote enviado.

## Decisões fechadas — não reabrir

1. **Cobertura do enunciado:** se o enunciado pede algo que a resposta original não traz, **completa**.
2. **Registro da Parte I:** transcrição da fala do candidato. Pessoal, primeira pessoa, marcadores orais, frases de 12 a 20 palavras, sem ponto e vírgula. **Não** é padrão de resposta impessoal.
3. **Marcadores internos permanecem** `##FALA##` / `##ROTEIRO##` / `##VERIFICAR##`. Os títulos exibidos no site é que mudam.
4. **Subtítulos do roteiro:** derivados do item, específicos. Proibida lista fixa; `ATUAÇÃO DA DEFENSORIA` só quando houver desdobramento real.
5. **Nome do produto:** Sabatinando (era SabatinaLab / Minha Banca).
6. **Execução por Batch API**, não em chat.

## Próximos passos, em ordem

- [ ] Confirmar que os créditos foram comprados em **console.anthropic.com → Billing**, e não em claude.ai → Uso. São coisas distintas; o crédito do plano não roda a API.
- [ ] Criar a chave em console.anthropic.com → API Keys
- [ ] `setx ANTHROPIC_API_KEY "..."` · `pip install anthropic` · reabrir o PowerShell
- [ ] `python 2_enviar_lote.py --estimar` (confere autenticação)
- [ ] `python 2_enviar_lote.py --teste 5 --modelo claude-opus-5` — **ler as 5 antes de seguir**
- [ ] Matéria a matéria, começando por `direitos_humanos` (40 itens, ~US$ 0,75)
- [ ] `python 3_mesclar.py "CAMINHO\minha-banca.html"` — gera o `.NOVO.html` e o `PONTOS-A-VERIFICAR.md`
- [ ] Alterar `showResposta(item)` no site para os rótulos novos
- [ ] Reprocessar os 86 antigos sob o critério novo (~US$ 1,60) — hoje eles destoam
- [ ] Renomear tudo para Sabatinando: arquivo, subdomínio Netlify, pitch
- [ ] Tirar os dados do HTML: um JSON por matéria, o site lendo de lá

## Pendências de mérito — exigem decisão jurídica sua

- `processo_penal|37` — desfecho do Tema 1087 do STF, deixado como controvérsia pendente
- `processo_penal|35` — recorte da Lei 13.964/2019, art. 492, I, "e", e execução imediata no júri
- `consumidor|2` — feito sob o critério antigo (manteve fiel em vez de completar)
- `difusos_coletivos|6` — falta precedente nominado sobre a inaplicabilidade do Tema 350 à ação coletiva

## Arquivos

| | |
|---|---|
| `prompt_sistema.md` | regras de reescrita — é aqui que se ajusta a qualidade |
| `1_extrair.py` · `2_enviar_lote.py` · `3_mesclar.py` | o pipeline |
| `TESTE-5-AMOSTRA.md` | 5 itens de exemplo, com as edições dela |
| `COMPARACAO-TOM.md` | antes e depois do registro falado |
| `LEIA-ME.md` | manual de operação |
| `dados/pendentes.json` | fila atual (recalculada por `1_extrair.py`) |

O HTML de origem fica na pasta de trabalho da sessão "Speaking practice website": `minha-banca.html`, 3,3 MB. `de-improviso.html` é o protótipo, byte a byte idêntico — descartável.

## Arquitetura geral

O documento completo de arquitetura do Claude está em `Downloads\ÍNTEGRA DOS PROCESSOS` (foi gravado lá antes desta pasta existir): `Arquitetura-Claude-Ana.md`, `Cartao-de-referencia.md`, instruções dos 4 Projetos.

Skills já instaladas na conta: `reorganizar-sem-perda`, `indexar-documento-longo`, `padrao-de-resposta`, `revisao-cirurgica`, `extrator-de-autos`, `verificar-integridade`, `auditar-citacoes`.

Projetos ainda **não** criados — é o passo manual pendente na interface.
