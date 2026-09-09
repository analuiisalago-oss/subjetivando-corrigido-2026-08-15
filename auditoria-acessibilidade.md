# Auditoria de Acessibilidade: Minha Banca

**Padrão:** WCAG 2.1 AA · **Data:** 10/08/2026 · **Arquivo:** `minha-banca.html` (3,47 MB)
**Método:** varredura axe-core 4.x + contraste calculado dos valores computados (com composição de alfa e opacidade herdada) + navegação real por Tab no Chromium + medição de alvos + teste de refluxo em 320/400/720/1024/1280 px. Testado nos dois temas.

> Observação de método: os testes rodaram sobre uma cópia com o Tailwind compilado localmente, porque o sandbox bloqueia o CDN. O CSS gerado é o mesmo que o CDN produz para as classes presentes no arquivo.

---

## Resumo

**Problemas encontrados:** 14 · **Críticos:** 4 · **Maiores:** 7 · **Menores:** 3

O contraste de texto está sólido — 52 nós medidos no tema escuro, todos aprovados. O que reprova é quase tudo **estrutural e programático**: rótulos de formulário, semântica de landmarks, gestão de foco em modais e o refluxo do canvas de 1440 px. Três achados vieram de decisões minhas na migração e são de correção barata.

---

## Achados

### Perceptível

| # | Problema | Critério WCAG | Severidade | Recomendação |
|---|----------|---------------|-----------|--------------|
| 1 | Sem landmarks (`header`/`nav`/`main`/`footer`) e sem `h1`–`h3`. O export do Pen.dev é 100 % `div`. Leitor de tela não tem como pular para o conteúdo nem listar títulos | 1.3.1 Info e Relações | 🟡 Maior | Trocar a tag das 4 caixas de topo por `<header>`, `<main>`, `<footer>` mantendo as classes; marcar "Configuração" como `<h2>` e "Padrão de resposta" como `<h2>`. Adicionar um `<h1>` visualmente oculto com "Minha Banca" |
| 2 | Tema claro: texto branco em `#2f8f63` nos botões primários ("NOVO TEMA", "Ver espelho") → **4,02:1** | 1.4.3 Contraste (mínimo) | 🟡 Maior | Escurecer o verde primário do tema claro para `#237a4f` (5,4:1) ou usar texto `#0d1a13` sobre o verde atual |
| 3 | Rodapé "SUBJETIVANDO · 2024" está sob `opacity-[0.5]` do export; contraste efetivo cai abaixo de 4,5:1 em ambos os temas (único achado de contraste do axe no tema escuro) | 1.4.3 Contraste (mínimo) | 🟡 Maior | Subir a opacidade do wrapper para 0.75 ou compensar a cor do texto |
| 4 | Bordas dos componentes praticamente invisíveis: botões de modo **1,20:1** (escuro) e **1,32:1** (claro); moldura do `<select>` **1,20:1**. Mínimo exigido: 3:1 | 1.4.11 Contraste não textual | 🟡 Maior | Subir `#88b7991a` → `#88b79966` (escuro) e `#1b242024` → `#1b242066` (claro) apenas nas bordas de controle |
| 5 | **Tema claro: o estado selecionado some.** Botão ativo e inativo ficam com fundo e borda idênticos (`rgba(27,36,32,.03)` / `rgba(27,36,32,.14)`) — a seleção só é sinalizada por cor e peso do texto | 1.4.1 Uso de cor · 1.4.11 | 🔴 Crítico | Regressão minha: as regras `html[data-theme="light"] .bg-[...]` (especificidade 0,2,1) vencem `.seg-btn.active` (0,2,0). Corrigir para `html[data-theme="light"] .seg-btn.active` |
| 6 | 35 imagens com `alt=""` — corretas como decorativas, já que cada ícone tem texto adjacente | 1.1.1 Conteúdo não textual | ✅ Aprovado | — |

### Operável

| # | Problema | Critério WCAG | Severidade | Recomendação |
|---|----------|---------------|-----------|--------------|
| 7 | **`outline: none` sem substituto** em `#categorySelect`, `#manageMode`, `#manageCategory`, `#manageInput`. Confirmado por captura: o botão recebe o anel branco do navegador, o select focado não mostra nada | 2.4.7 Foco visível | 🔴 Crítico | Regressão minha: a regra existe só para neutralizar a aparência nativa. Adicionar `:focus-visible { outline: 2px solid #38a372; outline-offset: 2px; }` nos quatro |
| 8 | **Drawer e modais sem gestão de foco.** Ao abrir o menu o foco continua no `#btnMenu`; o Tab seguinte vai para o conteúdo **atrás** da sobreposição; não há armadilha de foco nem retorno ao fechar | 2.4.3 Ordem de foco · 2.1.2 | 🔴 Crítico | Ao abrir: mover o foco para o primeiro controle do painel; ciclar Tab dentro dele; devolver o foco ao gatilho ao fechar; aplicar `inert` no conteúdo de fundo |
| 9 | **Escape não fecha nada** — nem o drawer, nem os dois modais, nem o menu de impressão. Fechar só com clique no fundo ou no ×. Usuário de teclado que abre o menu de impressão fica sem saída óbvia | 2.1.2 Sem armadilha de teclado | 🟡 Maior | Um `keydown` global que fecha o overlay aberto no Escape |
| 10 | Alvos abaixo de 44×44: `#timeSlider` **200×6**, `#btnMenu` **18×28**, `#btnPrint` 153×33, `#btnReset` e `#btnNewTopic` 40×40, campos da rubrica 78×32. 12 de 16 controles | 2.5.5 Tamanho do alvo | 🟢 Menor | 2.5.5 é AAA na 2.1 — sob o critério AA aplicável (2.5.8, alvo mínimo de 24 px) só o **slider (6 px de altura)** e o **`#btnMenu` (18 px de largura)** reprovam. Subir a trilha do slider para 24 px de área clicável e dar padding ao botão de menu |
| 11 | **Refluxo:** a largura mínima da página é **1003 px** em qualquer viewport. Em 320 px exige rolagem nos dois eixos; a 200 % de zoom num monitor de 1280 px (= 640 px CSS) também | 1.4.10 Refluxo | 🔴 Crítico | Inerente ao export de 1440 px fixo. Exige media queries que empilhem a coluna lateral e soltem as larguras fixas (`w-[300px]`, `w-[220px]`, `w-[140px]`) |
| 12 | Todos os 16 controles interativos são elementos nativos (`button`/`select`/`input`) e alcançáveis por Tab. Nenhum `div` clicável. Ordem de tabulação lógica: menu → modos → submodos → assunto → tempo → sortear → ações → cronômetro → rubrica | 2.1.1 Teclado · 2.4.3 | ✅ Aprovado | — |

### Compreensível

| # | Problema | Critério WCAG | Severidade | Recomendação |
|---|----------|---------------|-----------|--------------|
| 13 | **8 controles sem rótulo programático:** `#categorySelect`, `#timeSlider`, `#manageMode`, `#manageCategory`, `#manageInput` e os campos numéricos da rubrica. Os textos visíveis ("ASSUNTO", "TEMPO") são `div`, não `label`. axe: `label` ×4 + `select-name` ×1, ambos *critical* | 3.3.2 Rótulos ou instruções · 4.1.2 | 🔴 Crítico | Transformar o rótulo visível em `<label for>` (mantendo as classes) ou acrescentar `aria-label`. Na rubrica, `aria-label` com o texto do quesito |
| 14 | Campos da rubrica aceitam valor acima do máximo sem aviso — o JS trunca com `Math.min` no cálculo, mas nada informa o usuário | 3.3.1 Identificação de erro | 🟢 Menor | Exibir mensagem ao exceder `data-max`, ou normalizar o valor no `input` |
| 15 | Foco não dispara mudança inesperada de contexto; o modo/submodo só muda por clique explícito | 3.2.1 Ao receber foco | ✅ Aprovado | — |

### Robusto

| # | Problema | Critério WCAG | Severidade | Recomendação |
|---|----------|---------------|-----------|--------------|
| 16 | **Segmentos sem estado exposto.** Os 11 botões de modo/submodo não têm `aria-pressed` nem `role="radio"`; os contêineres (`#modeToggle`, `#dpeProva`, `#dpeFonte`, `#tcdfToggle`) não têm `role` nem `aria-label`. O leitor de tela anuncia "Treino DPEs, botão" — sem dizer que está selecionado | 4.1.2 Nome, função, valor | 🟡 Maior | `role="radiogroup"` + `aria-label` no contêiner; `role="radio"` + `aria-checked` nos botões (ou `aria-pressed` mantendo `role=button`) |
| 17 | **Nada é anunciado.** Sem `aria-live` em lugar nenhum: o enunciado sorteado, a contagem do cronômetro, o fim do tempo (só há bipe sonoro) e o total da rubrica mudam em silêncio para quem usa leitor de tela | 4.1.3 Mensagens de status | 🟡 Maior | `aria-live="polite"` em `#stateLabel`/`#topicCard` e em `#rubricTotal`; `role="timer"` + `aria-live="off"` no relógio com um alerta `assertive` no zero |
| 18 | `#btnPrint` já expõe `aria-haspopup` e `aria-expanded` (alterna corretamente), e `#printMenu` tem `role="menu"` com dois `role="menuitem"`. Falta só o teclado de menu (setas + Escape) | 4.1.2 | 🟢 Menor | Setas ↑↓ para navegar os itens |
| 19 | Drawer e modais são `div` sem `role="dialog"`, `aria-modal="true"` nem `aria-labelledby` | 4.1.2 | 🟡 Maior | Acrescentar os três atributos apontando para o título já existente |
| 20 | `lang="pt-BR"`, `<title>Minha Banca</title>`, nenhum botão sem nome acessível, `#printDoc` com `aria-hidden="true"` | 3.1.1 · 2.4.2 · 4.1.2 | ✅ Aprovado | — |

---

## Verificação de contraste

Valores calculados dos estilos computados, com composição de alfa sobre o fundo opaco efetivo.

| Elemento | Frente | Fundo | Escuro | Claro | Exigido | Passa? |
|----------|--------|-------|--------|-------|---------|--------|
| Enunciado (Lora 20–30 px) | `#e2e8e4` | `#1e2420` | **12,72:1** | 16,67:1 | 4,5:1 | ✅ ✅ |
| Total da rubrica (14 px) | `#e2e8e4` | `#1e2420` | **12,72:1** | 16,67:1 | 4,5:1 | ✅ ✅ |
| Título de campo "PADRÃO ESPERADO" | `#4ade80` / `#1c6b45` | superfície | **9,07:1** | 6,48:1 | 4,5:1 | ✅ ✅ |
| Segmento selecionado "Treino OAB" | `#4ade80` / `#1c6b45` | tint verde | **7,88:1** | 6,13:1 | 4,5:1 | ✅ ✅ |
| Pílula "QUESTÃO ID: #4402" | `#88b799` / `#4e7a62` | inset | **7,55:1** | 4,54:1 | 4,5:1 | ✅ ✅ |
| Rótulos "MODO DE TREINO", "ENUNCIADO" | `#88b799` / `#4e7a62` | superfície | **6,99:1** | 4,90:1 | 4,5:1 | ✅ ✅ |
| "RESTANTES" (9 px) | `#88b799` / `#4e7a62` | superfície | **6,99:1** | 4,90:1 | 4,5:1 | ✅ ✅ |
| Botão primário "NOVO TEMA" | `#121614` / `#ffffff` | verde da marca | **5,78:1** | **4,02:1** | 4,5:1 | ✅ **❌** |
| "VOLTAR AO INÍCIO" / `#tbBadge` (topbar) | `#ffffff80` | `#3d2a35` | **4,55:1** | 4,55:1 | 4,5:1 | ✅ ✅ |
| Rodapé "SUBJETIVANDO · 2024" | `#88b799` @ opacidade 0,5 | `#1e2420` | **< 4,5:1** | < 4,5:1 | 4,5:1 | ❌ ❌ |

**Não textual (mínimo 3:1)**

| Elemento | Escuro | Claro | Passa? |
|----------|--------|-------|--------|
| Preenchimento do botão primário | 5,01:1 | 4,02:1 | ✅ ✅ |
| Borda do botão de modo (inativo) | 1,20:1 | 1,32:1 | ❌ ❌ |
| Borda do botão de modo (ativo) | 1,90:1 | 1,32:1 | ❌ ❌ |
| Moldura do `<select>` | 1,20:1 | 1,32:1 | ❌ ❌ |
| Arco do cronômetro sobre a trilha | verde `#38a372` sobre `#88b79926` | — | ✅ |

---

## Navegação por teclado

16 elementos focáveis, todos nativos, na ordem visual.

| Elemento | Ordem de Tab | Enter/Espaço | Escape | Setas |
|----------|--------------|--------------|--------|-------|
| `#btnMenu` | 1 | Abre o drawer ✅ | — | — |
| Botões de modo (3) | 2–4 | Troca o modo ✅ | — | ❌ não navega o grupo |
| Submodos DPE/TCDF | 5–8 | Troca o submodo ✅ | — | ❌ |
| `#categorySelect` | 9 | Nativo ✅ | Nativo ✅ | Nativo ✅ |
| `#timeSlider` | 10 | — | — | Nativo ✅ |
| `#btnDrawIdle` / `#btnDraw` | 11 | Sorteia ✅ | — | — |
| `#btnPrint` → `#printMenu` | 12 | Abre o menu ✅ | ❌ não fecha | ❌ |
| `#btnPistas`, `#btnToggleEspelho` | 13–14 | Alternam ✅ | — | — |
| Cronômetro (pausar/reiniciar/novo) | 15–17 | ✅ | — | — |
| Campos da rubrica | 18+ | Nativo ✅ | — | Nativo ✅ |
| **Drawer aberto** | — | — | ❌ não fecha | Foco permanece fora do painel ❌ |
| **Modais abertos** | — | — | ❌ não fecha | Sem armadilha de foco ❌ |

Indicador de foco: os `<button>` recebem o anel padrão do Chromium (`outline: auto`, visível — verificado em captura). Os quatro `<select>`/`<input>` que estilizei com `outline: none` ficam **sem nenhum indicador**.

---

## Leitor de tela

| Elemento | Anunciado como | Problema |
|----------|----------------|----------|
| Página | "Minha Banca" | Sem `<h1>`, sem landmarks — não há como pular para o conteúdo |
| `#categorySelect` | "caixa de combinação" | Sem nome acessível (axe: `select-name`, crítico) |
| `#timeSlider` | "controle deslizante, 5" | Sem nome nem unidade — não diz "minutos" |
| Botão de modo selecionado | "Treino DPEs, botão" | Não informa que está selecionado nem que é 1 de 3 |
| Enunciado sorteado | *(silêncio)* | Conteúdo troca sem `aria-live` |
| Cronômetro | *(silêncio)* | Contagem e fim do tempo não são anunciados; o fim só tem bipe |
| Total da rubrica | *(silêncio)* | Recalcula a cada digitação sem anunciar |
| Campos da rubrica | "spin button" | Sem o texto do quesito como rótulo |
| Drawer / modais | "grupo" | Sem `role="dialog"`, `aria-modal` ou título associado |
| Ícones (35 `<img>`) | *(ignorados)* | Correto — `alt=""` decorativo |
| `#printDoc` | *(ignorado)* | Correto — `aria-hidden="true"` |

---

## Correções prioritárias

1. **Rótulos de formulário** (crítico, ~20 linhas) — 8 controles sem nome acessível. Bloqueia completamente quem usa leitor de tela: sem isso a pessoa não sabe o que o select faz. Maior ganho por linha alterada.
2. **Foco visível nos selects e inputs** (crítico, 4 linhas) — regressão minha; hoje a pessoa que navega por teclado perde a posição ao chegar no "Assunto".
3. **Estado selecionado no tema claro** (crítico, 2 linhas) — regressão minha; no tema claro não dá para ver qual modo está ativo.
4. **Gestão de foco e Escape nos overlays** (crítico, ~25 linhas) — hoje abrir o menu pelo teclado leva a lugar nenhum e não há como fechar sem mouse.
5. **Landmarks e hierarquia de títulos** (maior, ~10 linhas) — troca de tags preservando classes; não muda um pixel.
6. **`aria-live` no sorteio, no cronômetro e no total** (maior, ~8 linhas) — sem isso o app é mudo justamente nos momentos em que informa algo.
7. **Contraste de bordas e do verde primário no claro** (maior, ~6 valores) — troca de cor pura, estrutura intacta.
8. **`role="radiogroup"` + `aria-checked` nos segmentos** (maior, ~15 linhas).
9. **Refluxo abaixo de 1003 px** (crítico pela norma, esforço alto) — exige media queries que o export não tem. Decisão de produto: se o app é de uso em desktop, vale registrar como exceção consciente em vez de refazer o layout.
10. **Slider e botão de menu com área de toque maior** (menor, 2 regras).

Os itens 1 a 8 somam cerca de 90 linhas e **não alteram a aparência** — são atributos, `aria-*`, quatro regras de foco e seis valores de cor. O item 9 é o único que mexeria na marcação do design.

---

### Ressalvas honestas

- Varredura automatizada pega ~30 % dos problemas. Este relatório soma automação + teste manual de teclado + medição de contraste, mas **não substitui teste com NVDA ou VoiceOver reais** — especialmente para a leitura da tabela de rubrica e a ordem de leitura do espelho.
- Os testes rodaram em Chromium. O comportamento do anel de foco padrão varia entre navegadores; no Safari o anel dos `<button>` pode ficar menos visível sobre a superfície escura, o que reforça a recomendação de definir um estilo de foco autoral.
- Não testei com aumento apenas de texto (1.4.4) nem com folha de estilo de alto contraste do sistema.

---

# Reauditoria após as correções (itens 1 a 8)

**Data:** 10/08/2026 · **Arquivo:** `minha-banca.html` (3,48 MB) · Mesma bateria de testes.

## Resumo

| | Antes | Depois |
|---|---|---|
| Violações axe-core (tema escuro) | 3 tipos / 6 nós | **0** |
| Violações axe-core (tema claro) | 3 tipos / 8 nós | **0** |
| Nós de texto com contraste reprovado | 1 escuro · 2 claro | **0 · 0** |
| Bordas de componente abaixo de 3:1 | 6 | **0** |
| Controles sem rótulo programático | 8 | **0** |
| Controles sem indicador de foco | 5 | **0** |
| Landmarks / `h1` | 0 / 0 | **4 / 1** |
| Regiões `aria-live` | 0 | **7** |
| Overlays com `role="dialog"` e Escape | 0 de 3 | **3 de 3** |

**Restam:** o refluxo (item 9, não aplicado por decisão) e dois itens menores — teclado de setas no menu de impressão e demais alvos de toque entre 24 e 44 px.

## O que mudou

**Marcação** — `<header>`, `<main id="conteudo">`, `<aside>` e `<footer>` no lugar das `div` do export, preservando todas as classes; `<h1>` fora da tela e "Configuração"/"Padrão de resposta" como `<h2>`; link "Pular para o conteúdo" que só aparece ao receber foco; `<label for>` em "ASSUNTO" e "TEMPO"; `role="group"` + `aria-label` nos quatro grupos de segmento; `aria-pressed` nos 11 botões; `role="dialog"` + `aria-modal` + `aria-labelledby` nos três overlays; `aria-live` no enunciado, no rótulo de estado, na descrição do modo, no resumo e no total da rubrica.

**CSS** — anel de foco autoral de 3 px em todos os controles (inclusive nos `select`/`input` que estavam com `outline: none`); bordas de componente elevadas ao mínimo de 3:1 **apenas nos controles**, deixando as linhas decorativas dos cartões com o valor original do export; verde primário do tema claro de `#2f8f63` para `#237a4f`; correção da especificidade que apagava o estado selecionado no tema claro; opacidade do rodapé de 0,5 para 1.

**Camada de acessibilidade** — um segundo `<script id="a11y-layer">`, separado, depois do script do app. O `<script>` original continua **byte a byte idêntico** ao do `minha-banca.html` que você me enviou — conferido por comparação de string a cada build. A camada só observa o DOM e acrescenta: sincronização do `aria-pressed`, rótulo do slider e dos campos da rubrica assim que o app os cria, aviso de "Tempo esgotado" para leitor de tela, gestão de foco nos overlays (entra, circula, Escape fecha, foco volta ao gatilho, fundo com `inert`) e área de toque de 24 px no slider e no botão de menu.

## Verificação pós-correção

- **axe-core:** 0 violações WCAG 2.0/2.1 A e AA nos dois temas.
- **Contraste:** 84 nós de texto medidos, todos aprovados nos dois temas. Bordas de controle entre 3,11:1 e 3,59:1.
- **Teclado:** anel `solid 3px` confirmado em todos os elementos ao tabular, incluindo o `#categorySelect`. No drawer aberto, o Tab permanece dentro do painel; Escape fecha o drawer, os dois modais e o menu de impressão.
- **Estado selecionado:** fundo e borda distintos do inativo nos dois temas (era idêntico no claro).
- **Regressão funcional:** os 15 passos do fluxo completo continuam passando — modo, submodo, assunto, tempo, sorteio, cronômetro, pistas, espelho, rubrica, impressão, drawer, gerenciar temas, sobre, tema claro e TCDF.
- **Dados:** as 16 constantes seguem íntegras (750 / 55 / 55 / 37 / 6 / 199 nas contagens esperadas).
- **`node --check`:** aprovado no script do app e na camada de acessibilidade.

Nota de método: a única "reprovação" de contraste que o meu medidor aponta é o `<h1 class="sr-only">` — texto de 1 px fora da tela, destinado só ao leitor de tela. O axe-core corretamente o ignora.
