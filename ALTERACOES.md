# REGISTRO DE ALTERAÇÕES

## COMO USAR

Registrar toda alteração relevante em ordem cronológica inversa. Não apagar entradas antigas; corrigir mediante nova observação. Usar datas no formato `AAAA-MM-DD`.

Cada entrada deve responder:

- o que mudou;
- por que mudou;
- quais arquivos foram afetados;
- quais testes foram executados;
- o que não foi testado;
- como reverter;
- se houve impacto em dados, segurança ou usuário.

## MODELO

```markdown
## [AAAA-MM-DD] TÍTULO OBJETIVO

**Tipo:** correção / funcionalidade / segurança / design / banco / documentação
**Responsável:**
**Versão ou commit:**
**Ambiente:** desenvolvimento / homologação / produção

### Problema

Descrição objetiva.

### Alteração

Descrição do que foi modificado.

### Arquivos ou serviços afetados

- arquivo/serviço;

### Banco de dados

Nenhuma alteração, ou descrição e referência da migração.

### Segurança e privacidade

Impacto identificado ou “sem impacto identificado”.

### Testes executados

- teste: PASSOU/FALHOU;

### Itens não testados

- item e motivo;

### Reversão

Como voltar ao estado anterior.

### Pendências relacionadas

- referência em PENDENCIAS.md;
```

## HISTÓRICO INICIAL CONHECIDO

## [2026-09-20] TAILWIND DEIXA DE VIR POR CDN E PASSA A SER GERADO NA MÁQUINA

**Tipo:** design
**Ambiente:** desenvolvimento, verificado em servidor local

### Problema

O `index.html` carregava o Tailwind pelo script `cdn.tailwindcss.com`. Esse script não é uma folha de estilo: é um programa que chega ao navegador do visitante, lê a página ali na hora, descobre quais das 339 classes utilitárias estão em uso e só então escreve o CSS, num `<style>` criado em tempo de execução. Esse `<style>` entra na cascata depois de `styles.css` e de `v41.css`, o que inverte a ordem esperada e é a causa dos 85 `!important` dos dois arquivos.

Na conferência apareceu um segundo defeito, até então desconhecido. O bloco de configuração do Tailwind dentro do `index.html` era atribuído **antes** da linha que carrega o script. O script, ao carregar, cria o próprio objeto `tailwind` e descarta o que já estava ali. A configuração nunca foi lida. As três famílias de fonte (`Inter`, `Lora`, `Plus Jakarta Sans`) e as oito cores `botanic` nunca chegaram a ser registradas no Tailwind, e `corePlugins: { preflight: false }` nunca desligou a normalização — ela sempre esteve ligada. A prova é a pilha de fontes medida no navegador: `ui-sans-serif, system-ui, sans-serif`, que é o padrão do Tailwind, não o `Inter` que a configuração pedia. O que funciona no site funciona por `styles.css` e `v41.css`, incluindo os remendos manuais das linhas 1056 e 1057 do `styles.css` para duas dessas cores.

### Alteração

O CSS do Tailwind passa a ser gerado na máquina e servido como arquivo estático, de dentro de `public/`.

- `tailwind.config.js` e `tailwind-entrada.css`, na raiz do projeto, definem a geração. A configuração reproduz o que o CDN de fato executava: tema padrão do Tailwind e normalização ligada. O tema personalizado não foi reintroduzido, porque acrescentá-lo agora mudaria o site.
- A varredura cobre `public/index.html` e `public/assets/app.js`, para alcançar também as classes que o JavaScript acrescenta.
- `public/assets/tailwind.css`, com 15.790 bytes e 282 regras, é o arquivo gerado. Substituir as 339 classes no `index.html` não foi necessário: o gerador escreve só as regras que a varredura encontra.
- O `<link>` fica **depois** de `styles.css` e de `v41.css`, que é a posição que o `<style>` injetado pelo CDN ocupava. Posto antes, sete botões mudavam de `justify-content: flex-start` para `center`, porque `.justify-start` e `.btn` têm a mesma especificidade e quem vence é o último carregado.
- O bloco de 25 linhas de configuração saiu do `index.html` e foi substituído por um comentário com o comando de geração.

Os 85 `!important` continuam necessários e não foram tocados. Retirá-los exige mover o `tailwind.css` para antes das outras folhas, o que é alteração separada e com conferência própria.

### Arquivos ou serviços afetados

- `public/index.html`;
- `public/assets/tailwind.css` (novo);
- `tailwind.config.js` (novo);
- `tailwind-entrada.css` (novo);
- `servidor-local.js` (novo; serve `public/` na máquina para conferência e não vai ao ar);
- `node_modules/`, com `tailwindcss` 3, já ignorado pelo git.

### Banco de dados

Nenhuma alteração.

### Segurança e privacidade

Uma dependência externa a menos em tempo de execução: o navegador do visitante deixa de buscar e executar script de terceiro a cada visita. Sobram dois endereços externos no `index.html`, a biblioteca do Supabase em `cdn.jsdelivr.net` e as fontes em `fonts.googleapis.com`. Libera a parte da P1-09 que dependia da saída do Tailwind.

### Testes executados

- comparação de 592 elementos entre a versão com CDN e a versão com arquivo local, a 1280×900, medindo 39 propriedades calculadas e a caixa de cada elemento, com tolerância de 1 px: 0 diferenças: PASSOU;
- a mesma comparação a 390×844: 0 diferenças: PASSOU;
- altura total da página idêntica nas duas larguras, 988 px e 1350 px: PASSOU;
- ausência do script do CDN e presença do `<link>` local, conferidas no DOM das duas versões: PASSOU;
- presença da normalização no arquivo gerado, com `#e5e7eb` na borda e `ui-sans-serif` na fonte, que são os valores medidos no lado do CDN: PASSOU.

### Itens não testados

- o site publicado, porque a alteração ainda não foi ao ar;
- larguras entre 391 px e 1279 px;
- as telas que só aparecem depois de entrar na conta;
- as demais páginas de `public/`.

### Reversão

`git revert` do commit. O script do CDN volta ao `index.html` e o `tailwind.css` deixa de ser carregado.

### Pendências relacionadas

- P2-02, que passa a CONCLUÍDA;
- P1-09, cuja parte bloqueada pelo CDN fica liberada;
- item novo dentro da P2-01: mover o `tailwind.css` para antes das outras folhas e retirar os 85 `!important`.

## [2026-09-14] ESTILO INJETADO PELO JAVASCRIPT PASSOU PARA O CSS

**Tipo:** design
**Ambiente:** desenvolvimento

### Problema

O `app.js` criava um elemento `<style>` e o acrescentava à página ao abrir, com duas regras: a área de toque do controle de duração e a do botão de menu. Eram a quinta e a sexta fonte de estilo da página, atrás dos dois arquivos CSS, do Tailwind, do Font Awesome e do Google Fonts.

Estilo escrito por JavaScript não aparece em busca nos arquivos de CSS. Quem procurasse por que o controle de duração tem 24 px de altura não encontraria a resposta em lugar nenhum dos dois arquivos de estilo.

### Alteração

`public/assets/app.js`, linha 1389: removido o trecho que criava o `<style>` e o pendurava na página. No lugar ficou um comentário registrando para onde as regras foram e que não devem voltar como JavaScript. O arquivo passou a ter zero `createElement('style')`.

`public/assets/v41.css`, linha 633: as duas regras escritas como CSS, com os seletores `html body #timeSlider` e `html body #btnMenu`.

**Por que não foi preciso `!important`:** as regras estavam sendo injetadas por último para vencer as classes utilitárias do Tailwind. Escritas com seletor por id, vencem por especificidade — um id supera qualquer classe, independentemente da ordem de carregamento. A ordem deixou de importar para esse caso.

Tamanhos: `app.js` de 3.445.307 para 3.445.134 bytes; `v41.css` de 23.779 para 24.200.

### Arquivos ou serviços afetados

`public/assets/app.js`, `public/assets/v41.css`.

### Banco de dados

Nenhuma alteração.

### Segurança e privacidade

Nenhum impacto.

### Testes executados

- conferência da âncora no `app.js` antes de gravar: 1 ocorrência, como esperado;
- `node --check public/assets/app.js`: aprovado;
- busca por `createElement('style')` no `app.js`: zero;
- verificação em servidor local pela autora: arrasto do controle de duração e clique no botão de menu, em janela larga e estreita.

### Itens não testados

- toque em aparelho físico. A verificação foi feita em navegador de computador, inclusive em largura estreita.

### Reversão

`git revert` do commit desta alteração devolve a injeção por JavaScript e retira as regras do `v41.css`.

### Pendências relacionadas

- P2-02 permanece aberta. Com esta alteração restam quatro fontes de estilo na página: `styles.css`, `v41.css`, o Tailwind por CDN e o Google Fonts. Das quatro, só o Tailwind disputa as mesmas propriedades que os dois arquivos.


## [2026-09-13] FONT AWESOME SUBSTITUÍDO POR ÍCONES SVG NA PRÓPRIA PÁGINA

**Tipo:** design
**Ambiente:** desenvolvimento, verificado em servidor local

### Problema

O `index.html` baixava a folha de estilos completa do Font Awesome de um CDN — 100 KB descompactados — para exibir 15 ícones. Além do peso, é uma dependência externa a mais: se o CDN falhar, os ícones somem.

### Alteração

As 22 tags `<i class="fa-solid ...">` do `index.html` foram substituídas por 22 elementos `<svg>` escritos na própria página, de traço, em grade de 24 px, com `stroke="currentColor"`. O `<link>` do Font Awesome foi removido.

**O caso do `#authIcone`, que exigiu alterar o `app.js`:** o ícone do topo da tela de conta muda conforme a tela — entrar, criar conta, recuperar senha e definir nova senha. O `app.js` fazia isso trocando a classe do elemento. Dois desses quatro ícones não existiam no `index.html`: só apareciam em tempo de execução. Substituir apenas o HTML deixaria as telas de recuperar e de definir senha sem ícone.

- `app.js` linha 2406: acrescentado o objeto `ICONES`, com o SVG dos quatro; o objeto `TITULOS` passou a guardar a chave desse objeto em vez do nome da classe;
- `app.js` linha 2432: `icone.className = 'fa-solid ' + ...` passou a `icone.innerHTML = ICONES[...]`;
- `index.html`: o `<i id="authIcone">` virou `<span id="authIcone" class="ico-troca">`.

**`v41.css`:** acrescentada no fim a regra `html body svg.ico` com `width: 1em`, `height: 1em` e `vertical-align: -.125em`. É ela que faz o SVG acompanhar o `font-size` e herdar a cor do texto, preservando as classes `text-2xl`, `text-sm`, `text-botanic-primary` e `text-botanic-sage` que já estavam nas tags.

Tamanhos: `index.html` de 117.539 para 121.299 bytes; `app.js` de 3.444.574 para 3.445.307; `v41.css` de 23.235 para 23.779. O aumento soma 4,5 KB e substitui 100 KB baixados de CDN a cada visita.

### Arquivos ou serviços afetados

`public/index.html`, `public/assets/app.js`, `public/assets/v41.css`. Uma dependência externa a menos.

### Banco de dados

Nenhuma alteração.

### Segurança e privacidade

Uma requisição a menos para terceiro (`cdnjs.cloudflare.com`) a cada abertura da página. O cabeçalho `Content-Security-Policy-Report-Only` do `_headers` ainda autoriza `cdnjs.cloudflare.com` em `style-src` e `font-src`; a autorização pode ser retirada quando não houver mais nada vindo de lá.

### Testes executados

- conferência das 14 tags antes de gravar: cada uma apareceu o número esperado de vezes, somando 22. O script abortaria sem escrever se qualquer contagem divergisse;
- conferência das 2 âncoras do `app.js`: 2 de 2;
- busca por classes `fa-` remanescentes: zero no `index.html`, zero no `app.js`;
- `node --check public/assets/app.js`: aprovado;
- verificação visual em servidor local pela autora: os ícones dos três cartões da tela inicial, as três setas, a barra do topo, o bloco de última atividade, as quatro telas de conta e os ícones dentro dos campos.

### Itens não testados

- comportamento em navegadores além do usado na verificação;
- impressão, onde ícones de traço podem render diferente de ícones preenchidos.

### Reversão

`git revert` do commit desta alteração devolve as tags e o `<link>` do Font Awesome.

### Pendências relacionadas

- P2-02 permanece aberta: o Tailwind continua sendo carregado de CDN, e é ele que obriga ao uso de `!important`.


## [2026-09-10] LIMPEZA DA RAIZ ANTES DE ABRIR O REPOSITÓRIO A REVISÃO EXTERNA

**Tipo:** documentação  
**Ambiente:** repositório

### Problema

O repositório vai ser compartilhado com um colaborador para revisão por PR. A raiz continha **sete arquivos HTML de 3,4 a 3,9 MB**, nenhum deles o site, e nada na primeira tela indicava qual arquivo é a fonte. O risco não é o revisor apagar algo: é editar o arquivo errado e abrir um PR sem efeito. Além disso, `scripts/build_public.py` continuava presente — o único arquivo capaz de apagar o design atual sem gerar erro, protegido apenas por um comentário.

### Alteração

Removidos, todos recuperáveis pelo histórico do Git:

- `scripts/build_public.py` — o script que regenerava `public/` a partir de fonte congelada;
- `minha-banca.NOVO_3.html`, `minha-banca.NOVO.html`, `minha-banca.BACKUP.html` — o que o script lia, e cópias históricas;
- `index-css.html`, `index-tailwind.html` e a pasta `assets/` da raiz (41 PNGs) — exports crus do Pen.dev. Verificado: os 41 PNGs são referenciados **exclusivamente** por esses dois HTML, e nenhum dos três é usado por `public/`;
- `_headers`, `_redirects` e `robots.txt` da raiz — superados pelas versões de `public/`; só serviam de entrada para o script removido.

**Mantidos deliberadamente:** `minha-banca.html`, como referência do estado publicado em 15/08/2026; `pipeline/` inteiro, que é a matéria-prima do acervo e a base da futura F2 da P1-16; os `RESPOS_*.txt` e `respostas_*.json` da raiz, conferidos como matérias distintas das de `pipeline/resultados/`, e não cópias.

`README.md` atualizado: a seção 2 estava desatualizada nas rotas — listava quatro, quando existem treze. Acrescentadas a tabela de rotas (2.1) e a seção "Para quem vai contribuir" (2.2), com o que um revisor precisa saber antes do primeiro PR. Na seção 5, retirados dois itens já concluídos e corrigida a descrição dos documentos institucionais, que existem em rascunho. Na seção 6, o aviso de não executar o script foi substituído pelo registro de que ele foi removido.

### Banco de dados

Nenhuma alteração.

### Segurança e privacidade

Conferido antes de abrir o acesso: não há chave de serviço, JWT nem `sb_secret` em `public/assets/app.js` ou `public/index.html`. Aparecem apenas a URL do projeto Supabase e a chave `sb_publishable_`, pública por definição e protegida pela RLS comprovada em 09/09/2026.

**Verificação que continua pendente e é do usuário:** se `private/` chegou a ser commitada antes de entrar no `.gitignore`, ela permanece no histórico e será clonada pelo colaborador. Confirmar com `git log --all --oneline -- private/` **antes** de conceder acesso.

### Testes executados

- `node scripts/audit_project.mjs` continua válido: ele audita apenas arquivos de `public/`, nenhum dos removidos;
- conferido por busca que nenhum arquivo de `public/` referencia os PNGs da raiz nem os dois HTML de export.

### Itens não testados

- nada em execução mudou: nenhum arquivo removido era carregado pelo site.

### Reversão

`git revert` do commit desta limpeza devolve todos os arquivos. Nenhum conteúdo foi perdido — remoção do estado atual, não do histórico.

### Pendências relacionadas

- P2-06 encerrada por remoção;
- P2-08 e P1-16 permanecem abertas.


## [2026-09-09] CORREÇÃO DA RESPOSTA TROCADA APÓS RECARREGAR A PÁGINA

**Tipo:** correção  
**Versão ou commit:** `01f59db`  
**Ambiente:** produção — verificado em `https://subjetivando.netlify.app`

### Problema

Defeito relatado pela autora com prova visual: a tela mostrava a pergunta do ECA sobre criança apreendida em flagrante e o painel "Resposta / fundamentos esperados" exibia conteúdo de LINDB — vacatio legis, 45 dias, analogia e costumes. O mesmo texto da LINDB já havia aparecido em capturas anteriores, para outra pergunta.

**O acervo não estava errado.** Conferido no `app.js`: aquela pergunta do ECA está pareada com a resposta correta — art. 103, art. 178 e encaminhamento ao Conselho Tutelar. Pergunta e resposta vivem no mesmo objeto (`{pergunta, resposta}`); não existe busca por posição em lista paralela. A hipótese anterior, de descompasso entre os 199 tópicos de `ORAL_TOPICS` e as 750 questões de `DPE_ORAL_QUESTOES`, estava errada e fica registrada como descartada.

**A causa estava na camada D, "CONTINUIDADE AO RECARREGAR", do `app.js`.** A cadeia, lida linha a linha e depois reproduzida no site:

1. o sorteio de uma questão nova escondia o painel de resposta (`espelhoPanel.style.display = 'none'`) mas **nunca apagava o texto dentro dele** — o `espelhoText` seguia com a resposta da questão anterior;
2. antes de salvar o instantâneo da tela, `garantirCache()` decide se a resposta já está renderizada por um teste de tamanho: `espelhoText` com mais de 20 caracteres. Com o texto velho no lugar, o teste dava verdadeiro e a função voltava sem renderizar;
3. o instantâneo era então gravado com a **questão nova e a resposta velha**;
4. ao recarregar, a camada D repunha esse instantâneo e ligava o modo `restaurado`; nesse modo o botão "Ver resposta" é interceptado com `stopPropagation`, e o manipulador do aplicativo, que renderizaria a resposta certa, nunca chegava a rodar.

Consequência prática: **em sessão contínua a resposta saía certa; o erro só aparecia depois de recarregar a página** — por isso parecia intermitente. É o defeito mais grave já encontrado no produto: resposta errada para quem estuda para concurso.

### Alteração

Somente em `public/assets/app.js`. Nenhum HTML, nenhum CSS, nada do desenho da v41.

- criada `limparEspelho()`, logo após `showPrint`, com comentário explicando o motivo. Esvazia `espelhoText`, `espelhoResumo`, `modeloText`, `espelhoRubric`, `rubricTotal` e `pistasList`;
- chamada nas **cinco** funções de sorteio, imediatamente antes de o painel ser escondido: `resetDrawArea`, `doDrawOab`, `doDrawTcdfProva`, `doDrawTcdfD` e `doDrawDpeQ`. Com o painel realmente vazio, o teste de `garantirCache()` passa a dar falso e a resposta da questão atual é renderizada antes de o instantâneo ser salvo;
- versão do instantâneo elevada de `v: 2` para `v: 3`, nos dois pontos — na gravação e no teste de leitura de `restaurar()`.

**Não se mexeu** na linha que esconde o painel dentro do manipulador de "Ocultar resposta": ali não há sorteio.

Diferença total: 21 linhas inseridas, 2 removidas, 1 arquivo.

### Arquivos ou serviços afetados

- `public/assets/app.js` — único arquivo alterado.

### Banco de dados

Nenhuma alteração de esquema. A subida de versão do instantâneo **descarta os instantâneos já contaminados**, tanto no `localStorage` de cada navegador quanto na cópia que a camada de sincronização guarda no Supabase: `restaurar()` recusa qualquer instantâneo que não seja `v: 3`. Sem isso, quem já tinha usado o site continuaria vendo a resposta trocada mesmo depois da correção.

### Segurança e privacidade

Nenhum impacto. Nenhuma requisição nova, nenhum dado a mais gravado.

### Testes executados

- conferência das 8 âncoras de linha antes de gravar: 8 de 8. O script abortaria sem escrever se qualquer linha divergisse do esperado;
- `node --check public/assets/app.js`: sintaxe válida;
- teste funcional de 10 casos executando a `limparEspelho()` **extraída do arquivo já gravado**, não de uma cópia: prova que o painel fica vazio e que o teste `cheio()` da camada D passa de verdadeiro para falso — que é o elo causal da correção. 10 de 10;
- **verificação no site publicado**, modo Defensorias → Prova oral → Questões passadas, na sequência exata que reproduzia o erro: sorteia Q1 (Sistema Nacional do Meio Ambiente) → painel vazio; "Ver resposta" → Lei 6.938/81, correta; sorteia Q2 (adimplemento substancial) → painel já com a resposta de Q2; instantâneo salvo com Q2 e a resposta de Q2 pareadas; **recarrega a página**; "Ver resposta" → STJ e adimplemento substancial, correta. Antes da correção, esse último passo devolveria a resposta do meio ambiente;
- confirmado no site que o instantâneo antigo, em versão 2, foi descartado na primeira carga.

### Itens não testados

- o mesmo percurso nos modos OAB e TCDF, que usam `renderEspelho` em vez de `showResposta`. A correção é a mesma e as chamadas estão nas cinco funções de sorteio, mas só o percurso da prova oral da Defensoria foi percorrido de ponta a ponta;
- comportamento com conta autenticada e sincronização ativa: o teste no site foi feito sem login, para não gravar dados de teste no Supabase.

### Reversão

`git revert 01f59db` devolve o arquivo ao estado anterior. Instantâneos gravados em `v: 3` passariam a ser recusados pela versão revertida, o que apenas faz a tela abrir vazia — não corrompe nada.

### Pendências relacionadas

- abre-se **P1-16**: a camada D restaura a tela por instantâneo do DOM, sem qualquer identidade de questão. Esta correção fecha o sintoma, não a fragilidade estrutural.

## [2026-09-09] PÁGINA INICIAL SEPARADA DO SIMULADOR (E5 DA P1-15)

**Tipo:** funcionalidade  
**Ambiente:** desenvolvimento local

### Problema

A raiz do site abria direto no simulador. Quem chegava pela primeira vez via a mesma tela de quem já usava, sem convite, sem explicação e sem caminho claro para criar conta.

### Alteração

- criada `public/inicio.html`: convite com "Criar conta" e "Já possui uma conta? Faça o login", três destaques do produto e o aviso honesto de que gravação, transcrição e correção por IA ainda não existem;
- `public/_redirects`: `/` passa a servir `inicio.html` **com sinal de força** (`200!`), porque arquivo existente vence regra de reescrita e o `index.html` continuaria ganhando; `/dashboard` e `/treino` passam a servir o simulador;
- `public/assets/conta.js`: destino após entrar e link de confirmação de cadastro passam a `/dashboard`;
- `public/assets/paginas.css`: estilos do convite;
- `scripts/audit_project.mjs`: 16 arquivos permitidos em `public/`.

Nenhuma alteração no `app.js` nesta etapa.

### Configuração externa exigida

**`https://subjetivando.netlify.app/dashboard` precisa ser cadastrado nas Redirect URLs do Supabase.** Sem isso, o link de confirmação de cadastro não leva ao destino certo — é o mesmo tipo de defeito corrigido na P1-05 nesta data.

### Banco de dados

Nenhuma alteração.

### Segurança e privacidade

A página inicial **não carrega recurso externo algum**. O atalho "continuar de onde parou" apenas verifica a presença da chave de sessão no `localStorage`, sem ler o conteúdo, e é dica de interface, não controle de acesso.

### Testes executados

- `node scripts/audit_project.mjs`: 16 arquivos, acervo íntegro: PASSOU;
- `node scripts/teste_consentimento.mjs`: 5 de 5: PASSOU;
- renderização a 1100px e 390px: sem transbordamento, sem erro de script, zero requisições externas: PASSOU;
- com chave de sessão presente no navegador, o atalho aparece e aponta para `/dashboard`: PASSOU.

### Itens não testados

- se a regra forçada da raiz funciona no Netlify — só verificável depois de publicar;
- fluxo completo de cadastro com o novo destino de confirmação.

### Reversão

Remover a regra de `/` no `_redirects` devolve a raiz ao simulador imediatamente.

### Pendências relacionadas

- E5 da P1-15 concluída; falta cadastrar a URL no Supabase.

## [2026-09-09] PÁGINAS PRÓPRIAS DE ENTRAR, CRIAR CONTA E RECUPERAR SENHA (E4 DA P1-15)

**Tipo:** funcionalidade  
**Ambiente:** desenvolvimento local

### Problema

Entrar e criar conta viviam num modal sobre o simulador. Não havia endereço próprio, e "criar conta" aparecia em contexto de quem já estava autenticado.

### Alteração

- criadas `public/login.html`, `public/cadastro.html` e `public/recuperar-senha.html`;
- criado `public/assets/conta.js`, que **reproduz fielmente** o que a camada de conta do `app.js` já fazia: mesmas validações, mesmas mensagens, mesmos parâmetros de API, mesmo dicionário de tradução de erros;
- `public/assets/paginas.css` ganhou os estilos de formulário;
- `public/_redirects` recebeu três regras, antes do curinga;
- `scripts/audit_project.mjs` passou a aceitar 15 arquivos em `public/`;
- **`public/assets/app.js`: uma linha.** O botão de conta passou a levar para `/login` em vez de abrir o modal.

Não se mexeu na definição de nova senha em `/atualizar-senha`, que continua no `app.js` com o modal — fluxo comprovado nesta mesma data.

### Banco de dados

Nenhuma alteração. Nenhuma tabela, política ou configuração do Supabase foi tocada.

### Segurança e privacidade

**Defeito encontrado e corrigido antes de publicar:** a primeira versão de `conta.js` abortava se a biblioteca do Supabase não chegasse da CDN, e o formulário caía no envio nativo do navegador — o que recarregaria a página com e-mail e **senha na barra de endereço**. Corrigido registrando sempre os manipuladores de envio e verificando a biblioteca dentro deles. Verificado com a CDN bloqueada: o endereço não muda, a senha não aparece nele, e um aviso explica o que houve.

As três páginas trazem `noindex` e não recebem nem enviam dado algum além do necessário à autenticação.

### Testes executados

- diferença linha a linha do `app.js`: **exatamente uma** alteração, o restante do arquivo de 3,3 MB inalterado: PASSOU;
- `node --check` no `app.js` e no `conta.js`: PASSOU;
- `node scripts/audit_project.mjs`: 15 arquivos, acervo íntegro: PASSOU;
- `node scripts/teste_consentimento.mjs`: 5 de 5: PASSOU;
- renderização das três páginas em navegador real, 1100px e 390px: sem transbordamento, sem erro de script, todos os campos com rótulo associado: PASSOU;
- mostrar e ocultar senha, com a biblioteca indisponível: PASSOU;
- envio do formulário com a biblioteca indisponível: endereço não muda, senha não vaza para a URL, aviso exibido: PASSOU.

### Itens não testados

- **entrar, criar conta e recuperar senha de verdade, contra o Supabase** — a CDN é bloqueada no ambiente de verificação, então o caminho completo só pode ser testado no site publicado;
- comportamento do botão de conta no aplicativo depois da publicação;
- redirecionamento de quem já está autenticado ao acessar `/login`.

### Reversão

`git revert` do commit. Os quatro arquivos novos somem, o `app.js` volta à linha anterior e o modal volta a abrir.

### Pendências relacionadas

- E4 da P1-15 concluída; P2-09 aberta para hospedar a biblioteca do Supabase localmente; parte da P1-14 entregue.

## [2026-09-09] PÁGINAS INSTITUCIONAIS COM ROTAS PRÓPRIAS (E3 DA P1-15)

**Tipo:** funcionalidade e documentação  
**Ambiente:** desenvolvimento local

### Problema

Não existiam páginas de sobre, termos de uso e política de privacidade. A ausência dos dois últimos é bloqueio de lançamento: o site guarda dados pessoais de terceiros.

### Alteração

- criadas `public/sobre.html`, `public/termos.html` e `public/privacidade.html`, como arquivos estáticos independentes do aplicativo;
- criada `public/assets/paginas.css`, folha própria de 3,8 KB;
- `public/_redirects` recebeu três regras antes do curinga, mapeando `/sobre`, `/termos` e `/privacidade`;
- `scripts/audit_project.mjs` passou a aceitar os quatro arquivos novos na lista fechada de `public/`.

Decisão de desenho: as páginas **não carregam recurso externo algum** — sem Tailwind, sem CDN de ícones, sem fontes do Google. Usam fontes do próprio sistema. Assim nenhum IP de quem as lê é entregue a terceiro, o que é especialmente pertinente numa política de privacidade. Também não dependem do roteador, que ainda não existe.

### Banco de dados

Nenhuma alteração.

### Segurança e privacidade

Melhora. As três páginas trazem `noindex`, não fazem requisição externa e a política declara com precisão o que o site coleta, inclusive o que ainda não existe — como a exclusão automática de conta.

### Testes executados

- renderização em navegador real, servida por HTTP: fundo, tipografia e largura de leitura corretas nos temas claro e escuro: PASSOU;
- requisições externas por página: **zero**: PASSOU;
- erros de script: **zero**: PASSOU;
- transbordamento horizontal em 1100px e 390px: **zero**: PASSOU;
- `node scripts/audit_project.mjs` com a árvore completa: 11 arquivos em `public/`, acervo íntegro: PASSOU;
- `node scripts/teste_consentimento.mjs`: 5 de 5: PASSOU.

### Itens não testados

- comportamento das três rotas no Netlify depois da publicação;
- leitura em aparelho real;
- impressão.

### Reversão

Remover os quatro arquivos, desfazer as três regras de `_redirects` e a lista do `audit_project.mjs`.

### Pendências relacionadas

- E3 da P1-15 concluída; P2-08 aberta com as lacunas de conteúdo.

## [2026-09-09] NORMALIZAÇÃO DE VALORES DO EXPORT — PRIMEIRO PASSO DO SISTEMA DE DESIGN

**Tipo:** design  
**Ambiente:** desenvolvimento local

### Problema

A interface é export do Pen.dev e carrega os valores onde o cursor parou, não uma escala. Medição nos 115 KB de marcação: `10px` era o tamanho de fonte dominante do site, com 37 usos de 78, acompanhado de `tracking: 1px` — 0,1em sobre 10px — em 25 usos; `p-[40px]` em 11 cartões, que consomem 80px da largura num celular; e raios em 16, 24, 40, 62 e 70px.

### Alteração

Bloco 16 do CSS, sem tocar em marcação, cor, fonte ou script: rótulos 10px→12px, grau menor 9px→11px, entreletras 0,1em→0,04em, respiro dos cartões 40px→24px (16px abaixo de 1100px), raios 24/40/62/70 unificados em 16px. Valores expostos como variáveis em `:root` para servirem de base ao restante do sistema.

### Arquivos ou serviços afetados

- `minha-banca.NOVO_3.html`, bloco de estilo;
- `public/assets/styles.css`, regenerado pelo build.

`public/index.html` e `public/assets/app.js` não mudaram de tamanho.

### Banco de dados

Nenhuma alteração.

### Segurança e privacidade

Sem impacto identificado. O anel de foco autoral e os contrastes aprovados na auditoria de agosto não foram tocados.

### Testes executados

- `python3 scripts/build_public.py`: PASSOU, alterou apenas `styles.css`;
- `node --check public/assets/app.js`: PASSOU;
- `node scripts/audit_project.mjs`: PASSOU, acervo inalterado;
- `node scripts/teste_consentimento.mjs`: 5 de 5 casos;
- comparação visual pela autora entre `_AMOSTRA-design.html` e o site publicado, em navegador real: aprovada.

### Itens não testados

- contraste recalculado depois da mudança de tamanho e entreletras;
- leitura em aparelho real;
- impressão.

### Reversão

O bloco 16 é contíguo e comentado; removê-lo e rodar o build devolve a aparência anterior.

### Pendências relacionadas

- P2-05 aberta com o que falta do sistema de design: nomear as cores, reduzir a escala de espaçamento, definir componentes e decidir o uso de maiúsculas.

## [2026-09-09] CORREÇÃO DA CONFIRMAÇÃO DE INCORPORAÇÃO DE DADOS LOCAIS

**Tipo:** correção  
**Ambiente:** desenvolvimento local

### Problema

Teste real mostrou que a pergunta sobre incorporar o progresso salvo antes do login reaparecia depois de ter sido recusada. `autorizarIncorporacao` gravava somente o "sim"; a recusa não deixava rastro. O que impedia a repetição era uma marca em `sessionStorage`, que morre com a aba — logo, qualquer novo carregamento de página com sessão ativa trazia a pergunta de volta, indefinidamente.

### Alteração

- a resposta passa a ser gravada nos dois sentidos, `sim` e `nao`;
- a recusa registrada faz a função retornar sem perguntar;
- ao sair da conta, a marca é apagada, de modo que "Cancelar" significa "agora não" e o usuário volta a ser perguntado no próximo login;
- acrescentado `scripts/teste_consentimento.mjs`;
- `TESTES.md` passou a incluir o novo comando na lista de validação automatizada que já existia.

Optou-se por não depender de qual evento do Supabase dispara em cada caminho, por não ter sido medido.

### Arquivos ou serviços afetados

- `minha-banca.NOVO_3.html`, camada de sincronização;
- `public/assets/app.js`, regenerado pelo build;
- `scripts/teste_consentimento.mjs`, novo;
- `TESTES.md` e `PENDENCIAS.md`.

`public/index.html` e `public/assets/styles.css` não mudaram de tamanho.

### Banco de dados

Nenhuma alteração.

### Segurança e privacidade

Melhora: a recusa do usuário passa a ser respeitada de forma duradoura, em vez de ser reapresentada até que ele ceda.

### Testes executados

- `node scripts/teste_consentimento.mjs`: 5 de 5 casos, nenhuma falha. O caso decisivo — recusa já registrada — não produz nenhuma pergunta;
- `node --check public/assets/app.js`: PASSOU;
- `node scripts/audit_project.mjs`: PASSOU, acervo inalterado.

### Itens não testados

- o fluxo completo em navegador real, com login e logout, depois da publicação;
- comportamento com duas abas abertas simultaneamente.

### Reversão

`git revert` do commit e novo `python3 scripts/build_public.py`.

### Pendências relacionadas

- P1-08 concluída. O diálogo continua sendo o `window.confirm` do navegador e o recarregamento após aceitar permanece — ambos registrados na P1-14 como experiência, não defeito.

## [2026-09-09] CORREÇÃO DE DOIS DEFEITOS DE LAYOUT NO CELULAR

**Tipo:** correção  
**Ambiente:** desenvolvimento local e site publicado

### Problema

Teste em iPhone real mostrou conteúdo cortado e barra do topo sobre o conteúdo. A medição em viewport emulado de 375px identificou duas causas, ambas ativadas apenas quando as colunas empilham abaixo de 1100px: cartões com `flex: 1 1 0` colapsando em altura e escondendo 432px sob `overflow: hidden`; e a barra do topo com altura fixa de 64px, cujo grupo da direita quebrava de linha para fora dela.

### Alteração

Acrescentado o bloco 15 ao CSS da fonte canônica, dentro de `@media (max-width: 1100px)`: `flex-basis: auto` nos cartões e `height: auto` com `min-height: 64px` na barra. Quatro linhas de regra, com comentário registrando as medições.

### Arquivos ou serviços afetados

- `minha-banca.NOVO_3.html`, bloco de estilo;
- `public/assets/styles.css`, regenerado pelo build.

`public/index.html` e `public/assets/app.js` não mudaram de tamanho.

### Banco de dados

Nenhuma alteração.

### Segurança e privacidade

Sem impacto identificado.

### Testes executados

- correção aplicada ao vivo no site publicado, via navegador, antes de tocar em arquivo: cartão passou de 50px para 620px; barra passou de 64px para 98px; elementos com conteúdo cortado passaram de 2 para 0; transbordamento horizontal permaneceu em 0: PASSOU;
- mesma medição em 994px, com e sem a correção: resultados idênticos, sem regressão: PASSOU;
- `node --check public/assets/app.js`: PASSOU;
- `node scripts/audit_project.mjs`: PASSOU, contagens do acervo inalteradas: PASSOU.

### Itens não testados

- aparelho real depois da publicação;
- 768×1024, 1366×768 e 1920×1080;
- impressão depois da mudança.

### Reversão

`git revert` do commit e novo `python3 scripts/build_public.py`. A regra está isolada num bloco próprio e comentado, e pode ser removida sozinha.

### Correção posterior, no mesmo dia

A primeira versão publicada não surtiu efeito. O CSS chegou ao ar íntegro — hash conferido — mas o Tailwind por CDN injeta um `<style>` em tempo de execução que entra na cascata depois de `styles.css`; com a mesma especificidade, a declaração do Tailwind prevalecia. Acrescentado `!important` às três declarações e registrado no próprio comentário do bloco 15 por que ele existe e quando poderá sair.

Medição no site publicado, depois da segunda correção, em 375px: cartão da questão inteiro, barra do topo com 98px, zero elementos com conteúdo cortado, zero elementos fora da tela, zero transbordamento horizontal.

### Pendências relacionadas

- P1-03 avança; P3-11 aberta para a reorganização de tela estreita, que é design e não defeito.

## [2026-09-09] AUTENTICAÇÃO COMPROVADA E TRADUÇÃO DE ERROS AMPLIADA

**Tipo:** correção e configuração  
**Responsável:** Ana Luísa, com assistência de IA  
**Ambiente:** Supabase de produção e site publicado

### Problema

A recuperação de senha nunca havia funcionado. A lista de *Redirect URLs* do Supabase estava vazia; nessa condição o serviço aceita somente o *Site URL* e descarta o endereço `/atualizar-senha` pedido pelo frontend. O defeito estava no painel, não no código, e por isso as correções de 15/08/2026 não o resolveram.

Além disso, o dicionário de tradução de erros cobria apenas cinco mensagens do Supabase. Qualquer outra caía no texto genérico "Não foi possível concluir a operação". No teste real, tentar repetir a senha antiga produziu essa mensagem inútil, escondendo o motivo verdadeiro.

### Alteração

- cadastrados `https://subjetivando.netlify.app` e `https://subjetivando.netlify.app/atualizar-senha` em *Authentication → URL Configuration*, sem curinga;
- acrescentadas ao dicionário `ERROS` as mensagens de senha repetida e de limite de envio de e-mails;
- criada a lista `ERROS_POR_INICIO`, comparada pelo início do texto, para mensagens cujo conteúdo varia: espera por segurança e link expirado ou já usado;
- `traduzErro` passou a consultar o dicionário exato e depois a lista por início, mantendo o texto genérico como último recurso.

### Arquivos ou serviços afetados

- `minha-banca.NOVO_3.html`, camada de conta;
- `public/assets/app.js`, regenerado por `scripts/build_public.py`;
- configuração de autenticação do Supabase.

`public/index.html` e `public/assets/styles.css` não mudaram.

### Banco de dados

Nenhuma alteração.

### Segurança e privacidade

As novas mensagens não revelam informação interna nem permitem enumerar contas: dizem apenas o que o próprio usuário já sabe sobre a ação que acabou de tentar.

### Testes executados

- fluxo real com conta e e-mail verdadeiros: cadastro, confirmação, login, logout, recuperação, nova senha e novo login: PASSOU;
- `node --check public/assets/app.js`: PASSOU;
- `node scripts/audit_project.mjs`: PASSOU, contagens do acervo inalteradas;
- `build_public.py`: regenerou apenas `app.js`; `index.html` e `styles.css` mantiveram o tamanho anterior.

### Itens não testados

- expiração do link de recuperação por decurso de prazo;
- comportamento ao atingir o limite de envio de e-mails do plano gratuito;
- exibição das novas mensagens traduzidas, que só aparecem quando o erro correspondente ocorre.

### Reversão

`git revert` do commit correspondente, seguido de `python3 scripts/build_public.py`. No Supabase, remover as URLs cadastradas restabelece o comportamento anterior, que era defeituoso.

### Pendências relacionadas

- P1-05 concluída; P1-08 reaberta; P1-14 e P3-10 abertas.


## [2026-09-09] CONTROLE DE VERSÃO, PUBLICAÇÃO CONTÍNUA E COMPROVAÇÃO DA RLS

**Tipo:** configuração, segurança e documentação  
**Responsável:** Ana Luísa, com assistência de IA  
**Versão ou commit:** `3152d52`, etiqueta `publicado-2026-08-15`  
**Ambiente:** desenvolvimento local, GitHub, Netlify e Supabase de produção

### Problema

O que estava publicado não estava sob controle de versão. O único repositório Git existente ficava em `_versoes_antigas/backup-2026-08-15/`, tinha um único commit, nenhum remoto e guardava o estado anterior às correções de 15/08/2026. A publicação era manual, por arrastar pasta, o que impedia saber com certeza qual versão estava no ar. A RLS do Supabase permanecia não comprovada.

### Alteração

- criado repositório Git na pasta de trabalho, com commit inicial de 123 arquivos e etiqueta `publicado-2026-08-15`;
- `.gitignore` reforçado por acréscimo, com `node_modules/`, `dist/`, `*.zip`, `.DS_Store`, `Thumbs.db` e `desktop.ini`; nada foi removido;
- `core.autocrlf` e `core.filemode` definidos como `false` no repositório, para o Git no Windows não acusar alteração falsa nos 123 arquivos;
- repositório publicado como **privado** no GitHub;
- Netlify ligado ao repositório, com publicação contínua a partir da branch `main`, comando de build `python3 scripts/build_public.py` e diretório publicado `public`;
- pendências atualizadas: P0-01 e P1-02 concluídas, P0-02 com avanço registrado, P1-13 aberta.

### Arquivos ou serviços afetados

- `.gitignore`;
- `PENDENCIAS.md`;
- `ALTERACOES.md`;
- configuração do projeto no Netlify;
- repositório novo no GitHub.

Nenhum arquivo da aplicação foi alterado.

### Banco de dados

Nenhuma alteração. Apenas consultas de leitura.

### Segurança e privacidade

Confirmado que o isolamento entre usuários funciona. Varredura de segredos repetida antes do commit, sem chave privada. `private/` fora do versionamento e repositório privado.

### Testes executados

- `build_public.py` em cópia isolada reproduz `public/` com SHA-256 idêntico ao publicado: PASSOU;
- `node --check public/assets/app.js`: PASSOU;
- `node scripts/audit_project.mjs`: PASSOU, com o aviso conhecido dos marcadores editoriais;
- contagem do acervo publicado: 750 questões DPE (718 com resposta), 55 OAB, 55 temas TCDF, 6 provas, 37 discursivas: PASSOU;
- hashes dos arquivos servidos em produção conferidos contra os locais: `app.js` e `styles.css` idênticos; `index.html` difere apenas por comentário injetado pelo próprio Netlify: PASSOU;
- RLS: leitura anônima retorna 0 linhas nas seis tabelas e gravação anônima é recusada pela política: PASSOU;
- chamada anônima de `lidar_novo_usuario()` por RPC: recusada com `PGRST202`: PASSOU.

### Itens não testados

- cadastro, confirmação de e-mail, login e recuperação de senha com endereço real;
- sincronização entre dois dispositivos e entre dois usuários autenticados;
- layout em celular real;
- backup e restauração do Supabase.

### Reversão

Apagar a pasta `.git` devolve o projeto ao estado anterior. No Netlify, desligar a publicação contínua devolve o modo manual. O ZIP `subjetivando-corrigido-2026-08-15.zip` permanece como cópia externa.

### Pendências relacionadas

- P0-01 e P1-02 concluídas; P0-02 com avanço; P1-13 aberta; P0-03, P1-05 e P1-03 seguem abertas.


## [2026-08-15] CONSOLIDAÇÃO SEGURA DA VERSÃO DE BETA

**Tipo:** correção, segurança, design, configuração e documentação  
**Responsável:** revisão assistida do projeto Subjetivando  
**Ambiente:** desenvolvimento local

### Problema

A publicação apontava para um `index.html` inexistente; a raiz misturava arquivos públicos e privados; a tela anônima exibia identidade fictícia; a recuperação de senha estava incompleta; falhas de rede podiam manter botões bloqueados; a sincronização incorporava dados locais sem confirmação; e o simulador não possuía refluxo suficiente para telas pequenas.

### Alteração

- criada pasta publicável isolada em `public/`;
- criado gerador `scripts/build_public.py` para separar HTML, CSS e JavaScript;
- corrigidas rotas, inclusive `/atualizar-senha` e regra geral da aplicação;
- implementada definição de nova senha com Supabase `updateUser()`;
- adicionados tratamento de rede e senha mínima de oito caracteres;
- removida identidade fictícia do estado anônimo;
- adicionados consentimento de incorporação e estado de sincronização;
- impedido qualquer envio posterior enquanto a incorporação estiver recusada ou pausada;
- mantido o modal de recuperação aberto para informar links inválidos ou expirados;
- sanitizada a restauração do instantâneo de sessão;
- corrigida interpolação de contexto de anotações;
- adicionadas regras responsivas e redução de movimento;
- adicionados cabeçalhos transitórios de segurança;
- criados arquivos de auditoria e correção orientada do Supabase;
- movidas evidências com dados identificáveis para `private/`.
- marcados os documentos antigos do pipeline como históricos e registrada a divergência editorial sem sobrescrever a interface atual;
- criado `scripts/audit_project.mjs` para validar contagens, IDs, isolamento da publicação e padrões de segredos.

### Arquivos ou serviços afetados

- `minha-banca.NOVO_3.html`;
- `public/`;
- `_redirects`, `_headers`, `robots.txt`, `netlify.toml`;
- `scripts/build_public.py`;
- `supabase/`;
- documentos centrais do projeto;
- organização local das evidências de auditoria.

### Banco de dados

Nenhuma alteração executada. Foram criados SQL de auditoria somente leitura e um SQL de correção da permissão da função, dependente de validação prévia em homologação.

### Segurança e privacidade

Redução do risco de publicação acidental de arquivos privados, execução de HTML armazenado, enumeração de detalhes internos por mensagens e incorporação não consentida de dados locais. A RLS permanece não comprovada e continua sendo bloqueador de lançamento.

### Testes executados

- integridade do backup: PASSOU;
- todos os JSON: PASSOU;
- sintaxe Python: PASSOU;
- sintaxe JavaScript: PASSOU;
- geração de `public/`: PASSOU;
- IDs duplicados e validade das imagens: PASSOU.

### Itens não testados

- autenticação e e-mail reais;
- isolamento RLS;
- layout em navegador real;
- impressão;
- cabeçalhos no Netlify.

### Reversão

Restaurar `subjetivando-backup-2026-08-15.zip`. Nenhum dado do Supabase foi alterado.

### Pendências relacionadas

- P0-01, P0-03, P1-02, P1-03, P1-05, P1-09, P1-10, P1-11, P2-02, P2-03 e P3-05.

## [2026-08-15] CRIAÇÃO DA DOCUMENTAÇÃO PERMANENTE

**Tipo:** documentação  
**Responsável:** projeto Subjetivando  
**Ambiente:** documentação

### Problema

O desenvolvimento ocorreu de forma incremental com auxílio de inteligência artificial, sem conjunto único de documentos capaz de preservar contexto, decisões, regras de segurança e testes.

### Alteração

Criação dos documentos:

- `README.md`;
- `ARQUITETURA.md`;
- `REGRAS-DO-PROJETO.md`;
- `BANCO-DE-DADOS.md`;
- `SEGURANCA.md`;
- `TESTES.md`;
- `ALTERACOES.md`;
- `PENDENCIAS.md`.

### Segurança e privacidade

A documentação estabelece proibições de exposição de segredos, requisitos de RLS, fluxo seguro de pagamentos e critérios de lançamento.

### Testes executados

- revisão de consistência entre os documentos: PASSOU;
- confronto com o HTML auditado e `_redirects`: PASSOU;

### Itens não testados

- esquema real e políticas do Supabase;
- configurações internas do Netlify;
- funcionamento ao vivo da aplicação.

### Reversão

Remover os documentos. Não recomendado, pois não alteram a execução do site.

## [2026-08-15] AUDITORIA INICIAL DO PROTÓTIPO

**Tipo:** auditoria, sem alteração de código

### Constatações principais

- HTML monolítico de aproximadamente 3,5 MB;
- nome do arquivo auditado diferente de `index.html`;
- `_redirects` aponta para `/index.html`;
- responsividade insuficiente na tela principal;
- Tailwind carregado por CDN;
- autenticação Supabase presente;
- recuperação de senha incompleta;
- sincronização baseada em `localStorage` e Supabase;
- conteúdo extenso incorporado ao HTML público;
- domínio e cobrança ainda não implementados;
- políticas RLS não verificáveis pelo frontend.

### Resultado

Criação de plano por fases antes da abertura a usuários pagantes.
