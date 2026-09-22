# PENDÊNCIAS DO SUBJETIVANDO

## 1. COMO PRIORIZAR

| Prioridade | Significado |
|---|---|
| P0 | risco imediato de segurança, dados ou indisponibilidade |
| P1 | bloqueia beta público ou causa falha importante |
| P2 | necessário antes da cobrança |
| P3 | melhoria relevante após estabilização |
| P4 | ideia futura, sem compromisso |

Estados:

- `NÃO INICIADA`;
- `EM ANÁLISE`;
- `EM EXECUÇÃO`;
- `BLOQUEADA`;
- `CONCLUÍDA`;
- `DESCARTADA`.

Ao concluir, registrar a mudança em `ALTERACOES.md` e mover o item para a seção 7, "Concluídas". As seções 2 a 5 listam só o que está aberto.

### 1.1. IDs renumerados em 22/09/2026

Cinco números estavam em uso duas vezes, com assuntos diferentes. O item mais antigo (de 15/08/2026) manteve o número; o repetido recebeu número novo. Entradas antigas de `ALTERACOES.md` que citam o número repetido referem-se ao item da coluna "Assunto".

| ID repetido | Assunto | ID novo |
|---|---|---|
| P2-05 | concluir o sistema de design | **P2-13** |
| P2-06 | a pasta `public/` virou a fonte do site | **P2-14** |
| P2-07 | conteúdo de OAB, TCDF e discursiva apenas oculto por CSS | **P2-15** |
| P2-08 | completar as lacunas dos documentos institucionais | **P2-16** |
| P2-09 | hospedar a biblioteca do Supabase no próprio site | **P2-17** |

Mantiveram o número: P2-05 (política editorial), P2-06 (modelo de conteúdo premium), P2-07 (ambientes separados), P2-08 (pagamentos em modo de teste) e P2-09 (tabela e regras de assinatura).

## 2. P0 — SEGURANÇA E DADOS

### P0-02 — Inventariar e proteger segredos

**Estado:** EM ANÁLISE  
**Objetivo:** confirmar que nenhuma chave secreta foi incluída em HTML, GitHub ou arquivos compartilhados.  
**Conclusão exige:** inventário, rotação de segredos eventualmente expostos e variáveis de ambiente configuradas.

**Avanço:** o backup não contém segredo privado identificável. Varredura repetida em 09/09/2026 antes do primeiro commit: as únicas ocorrências de `ANTHROPIC_API_KEY`, `service_role` e `sb_secret` são nomes de variáveis em documentação e scripts, sem valor real. O repositório foi criado como privado e `private/` ficou fora do versionamento.

**Verificado em 22/09/2026, no histórico inteiro do Git:** `private/` e arquivos `.env` nunca foram commitados (`git log --all -- private/` vazio). Nenhum commit contém valor de `sb_secret_`, chave da Anthropic (`sk-ant-`), da OpenRouter (`sk-or-v1-`), do Stripe (`sk_live_`/`sk_test_`), token do GitHub, chave da AWS ou JWT. A única credencial presente é a chave `sb_publishable_`, pública por definição. A auditoria (`npm run check`) repete a busca em `public/` a cada execução e no GitHub Actions.

**Ainda falta:** verificar as variáveis de ambiente configuradas no Netlify e no Supabase.

### P0-03 — Confirmar backups do Supabase

**Estado:** NÃO INICIADA  
**Conclusão exige:** frequência, retenção, responsável e teste documentado de restauração.

### P0-04 — O Netlify parou de publicar a `main` em 20/09/2026

**Estado:** EM ANÁLISE, aberta em 22/09/2026. Depende de alguém com acesso ao painel do Netlify.

**Constatado em 22/09/2026, sem acesso ao painel:** o site no ar serve o `app.js` e o `tailwind.css` do commit `dcc9562` (20/09, 16:04, "Tailwind gerado na máquina"). O `tailwind.css` publicado tem 24.325 bytes, a versão não minificada daquele commit. Os cinco commits seguintes da `main` (`126e3d7`, `3a608c2`, `f3c0d8f`, `febbb56` e `491d989`) nunca foram ao ar: a correção dos dois botões "Sortear outra" (P1-17) não está no site. O Deploy Preview do PR #1 também falhou, e o GitHub Actions do mesmo PR passou.

**Causa: A CONFIRMAR.** O log do deploy exige login no Netlify. Hipóteses, da mais provável para a menos:

1. cota do plano gratuito, que é por créditos: 300 por mês, 15 por deploy de produção. A `main` recebeu 22 commits em setembro; banda e requisições também gastam créditos. Há relatos recentes no fórum do Netlify de deploys de produção pausados no plano gratuito com o site ainda no ar;
2. publicação automática desligada ou builds parados no painel;
3. algum erro de build introduzido a partir de `126e3d7`. A reorganização não mexeu em `public/` nem na raiz, o que torna esta a menos provável.

**Para resolver:** no Netlify, abrir *Deploys* e ler a mensagem do primeiro deploy com falha depois de `dcc9562`; conferir *Team settings → Billing/Usage*. Enquanto isso não se resolve, juntar mudanças em um único merge economiza deploys: cada merge na `main` é um deploy de produção.

## 3. P1 — BETA PÚBLICO

### P1-03 — Corrigir responsividade

**Estado:** EM EXECUÇÃO. Testada em iPhone real e em viewport emulado de 375px em 09/09/2026. Dois defeitos encontrados e corrigidos; um problema de organização permanece, movido para P3-11.

**Defeito 1, corrigido:** abaixo de 1100px as colunas empilham e os cartões com `flex: 1 1 0` passam a repartir altura em vez de largura. Dentro de contêiner de altura automática eles colapsam e, com `overflow: hidden`, escondem o conteúdo. Medido em 375px: o cartão da questão tinha 50px de caixa para 482px de conteúdo, ocultando 432px — incluindo o padrão de resposta e o botão de ocultar.

**Defeito 2, corrigido:** a barra do topo tem altura fixa de 64px; no celular o grupo da direita quebrava de linha e cobria o conteúdo da página.

**Correção:** bloco 15 do CSS, dentro de `@media (max-width: 1100px)`, com `flex-basis: auto` nos cartões e altura automática na barra.

**Medições depois da correção, em 375px:** cartão da questão com 620px mostrando o conteúdo inteiro; barra com 98px sem sobrepor; zero elementos com conteúdo cortado; zero transbordamento horizontal. Em 994px o resultado é idêntico ao anterior. Acima de 1100px a regra não se aplica.

**Correção da correção:** a primeira versão publicada não teve efeito nenhum. A regra chegou ao ar íntegra, mas o Tailwind por CDN injetava suas classes num `<style>` criado em tempo de execução, que entrava na cascata depois de `styles.css`. Com a mesma especificidade nos dois lugares, vencia a declaração do Tailwind. Resolvido com `!important` nas três declarações. Desde 20/09/2026 o Tailwind é um arquivo gerado (`tailwind.css`), carregado por último de propósito; os `!important` continuam necessários enquanto essa ordem não mudar (ver P2-01).

**Lição de método registrada:** testar uma regra injetando-a no fim da cascata pelo navegador não prova que ela funcionará dentro de `styles.css`. A verificação só vale depois de publicada, no arquivo real e na posição real.

**Ainda pendente:** validação visual em 768×1024, 1366×768 e 1920×1080; e o teste em aparelho real depois da publicação.

### P1-06 — Tratar falhas de rede na autenticação

**Estado:** CONCLUÍDA NO FRONTEND em 15/08/2026; falta teste com rede interrompida.  
**Critério:** botões sempre retornam ao estado utilizável e usuário recebe mensagem compreensível.

### P1-07 — Exibir estado de sincronização

**Estado:** CONCLUÍDA NO FRONTEND em 15/08/2026; falta teste em dois dispositivos.

### P1-09 — Implementar exclusão de conta e dados

**Estado:** NÃO INICIADA.

### P1-10 — Criar documentos públicos

**Estado:** EM EXECUÇÃO.  
**Inclui:** Termos de Uso, Política de Privacidade, contato e aviso de beta.

As páginas `/sobre`, `/termos` e `/privacidade` existem desde 09/09/2026 (E3 da P1-15), em rascunho, com as lacunas assinaladas na própria página. O que falta preencher está em P2-16.

### P1-11 — Revisar acessibilidade

**Estado:** EM EXECUÇÃO. Auditoria automatizada anterior aprovada; faltam teste responsivo e leitor de tela real.  
**Inclui:** teclado, leitor de tela, modais, redução de movimento e textos pequenos.

### P1-12 — Consolidar o acervo revisado na interface atual

**Estado:** BLOQUEADA por revisão editorial e jurídica.  
**Problema:** os arquivos intermediários de `acervo/pipeline/` contêm respostas reprocessadas com marcadores `##FALA##` e `##ROTEIRO##`, mas o acervo publicado — a constante `DPE_ORAL_QUESTOES` dentro de `public/assets/app.js` — ainda contém a versão anterior (a auditoria confirma: 718 respostas, nenhuma com os dois marcadores). Os HTMLs do pipeline usam uma interface mais antiga e não podem substituir a atual.  
**Conclusão exige:** resolver `acervo/pipeline/PONTOS-A-VERIFICAR.md`, aprovar o mérito das respostas, mesclar somente os dados no `app.js` (por âncora, nunca reescrevendo o arquivo), adaptar a apresentação dos marcadores e executar comparação de contagem e regressão visual.

**Relação com a IA da prova oral (P2-18):** o `##ROTEIRO##` de cada resposta é a lista de pontos que a banca espera. É exatamente o material que a correção por IA precisa para comparar com a fala do candidato.

### P1-14 — Melhorar o formulário de conta

**Estado:** EM EXECUÇÃO.  
**Observado no teste real de 09/09/2026:**

- não há como ver a senha digitada, o que impede conferir se ela coincide com o campo de confirmação;
- o requisito mínimo de oito caracteres não é informado antes do erro;
- a tradução de `Password should be at least 6 characters` promete oito caracteres, número que vem da validação do próprio site e não do Supabase. Manter os dois coerentes.

**Entregue na E4 da P1-15 (09/09/2026):** nas páginas `/login`, `/cadastro` e `/recuperar-senha`, os campos de senha têm botão de mostrar e ocultar, e o requisito de oito caracteres aparece antes do erro.

**Falta:** a definição de nova senha em `/atualizar-senha`, que continua no modal do `app.js`.

### P1-15 — Rotas reais e modelo de acesso

**Estado:** EM EXECUÇÃO. E1 a E5 concluídas em 09/09/2026; E6 e E7 não iniciadas. Modelo de acesso e mapa de rotas aprovados pela autora e registrados na seção 2.6 de `ARQUITETURA.md`.

**Problema:** a autenticação é um modal sobre o simulador. Quem está deslogado vê a mesma tela de quem está logado, nenhuma tela tem endereço próprio, e controles aparecem fora de contexto — "criar nova conta" oferecido a quem já está autenticado, por exemplo. A causa não é de tela: é a ausência de modelo de acesso. O aplicativo mostra tudo a todos e oculta partes por CSS.

**Decisões tomadas:** nível pago por funcionalidade e cota, não por exclusividade de conteúdo; visitante treina até 5 questões por dispositivo e depois é convidado a criar conta; roteador em JavaScript com History API, descartados arquivos HTML separados.

**Etapas, em ordem:**

| | Etapa | Entrega | Risco |
|---|---|---|---|
| E1 | Modelo de acesso aprovado | seção 2.6 de `ARQUITETURA.md` | concluída |
| E2 | Mapa de rotas aprovado | seção 2.6 de `ARQUITETURA.md` | concluída |
| E3 | `/sobre`, `/termos`, `/privacidade` | **CONCLUÍDA em 09/09/2026** — três páginas estáticas próprias | baixo |
| E4 | Páginas próprias de conta | **CONCLUÍDA em 09/09/2026** — `/login`, `/cadastro` e `/recuperar-senha` como arquivos próprios, sem roteador | baixo |
| E5 | Separar `/` do simulador | **CONCLUÍDA em 09/09/2026** — `/` é convite; simulador em `/dashboard` | **alto** |
| E6 | Guardas de rota e limpeza das sobreposições | redirecionamentos; controles fora de contexto deixam de existir | médio |
| E7 | `/conta` | tela própria | baixo |

**Decisão da autora, 20/09/2026: `/dashboard` passa a exigir sessão.** Hoje não exige. Conferido no site publicado em janela anônima: `/dashboard` abre o simulador inteiro, com as três telas e o acervo, sem nenhuma conta. Isso é a E6 e continua não iniciada. A decisão de 09/09 de deixar o visitante treinar 5 questões por dispositivo precisa ser reconciliada com esta: ou o limite de visitante vive em `/` e `/dashboard` exige sessão, ou `/dashboard` aceita visitante até a cota. A autora decidiu pela primeira.

**Por que a E6 não foi feita em 22/09/2026:** a guarda precisa ser testada com uma conta real entrando e saindo, e a regra 12 de `REGRAS-DO-PROJETO.md` manda parar quando não for possível testar autenticação. Cuidados já mapeados para quem fizer: `/atualizar-senha` também serve o `index.html` e chega sem sessão comum (o token vem no endereço), então precisa ficar fora da guarda; `conta.js` já aceita `?destino=` e só aceita caminho interno.

**E3 concluída em 09/09/2026.** As três páginas foram feitas como arquivos estáticos independentes — `public/sobre.html`, `public/termos.html`, `public/privacidade.html` e a folha `public/assets/paginas.css` —, servidas por regras próprias em `_redirects`, antes do curinga. Decisão deliberada: são páginas de texto, não precisam do `app.js` de 3,4 MB nem do roteador, e **não carregam nenhum recurso externo** — nenhuma CDN, nenhuma fonte do Google, nenhum IP de leitor entregue a terceiro. Verificado em navegador: zero requisição externa, zero erro de script, zero transbordamento horizontal em 1100px e em 390px, temas claro e escuro.

Os três documentos estão em **rascunho, com as lacunas visivelmente assinaladas na própria página**. Nada foi inventado — o que falta aparece marcado como "a completar". Ver P2-16.

**E4 concluída em 09/09/2026, por caminho diferente do planejado.** O plano previa construir um roteador dentro do `app.js` de 3,4 MB. Depois de a E3 provar o padrão de páginas estáticas, ficou claro que login, cadastro e recuperação **não precisam do roteador nem do acervo**: viraram `public/login.html`, `public/cadastro.html` e `public/recuperar-senha.html`, com `public/assets/conta.js` de 8 KB. Risco muito menor, mesmo resultado — endereço, título e recarga reais.

**A única alteração no `app.js` foi de uma linha:** o botão de conta deixou de abrir o modal e passa a levar para `/login`. Conferido por diferença linha a linha que nada mais no arquivo mudou.

**O que deliberadamente NÃO se mexeu:** a definição de nova senha em `/atualizar-senha` continua dentro do `app.js`, com o modal. Esse fluxo foi testado de ponta a ponta em 09/09/2026 e não há motivo para arriscá-lo. O modal permanece no arquivo por isso.

**Defeito encontrado e corrigido durante a implementação:** na primeira versão, `conta.js` abortava inteiro se a biblioteca do Supabase não chegasse da CDN. Nesse caso o formulário caía no envio nativo do navegador e **recarregaria a página com o e-mail e a senha visíveis na barra de endereço**. Corrigido: os manipuladores de envio são sempre registrados, a verificação da biblioteca acontece dentro deles, e a pessoa recebe uma mensagem clara. Verificado com a CDN bloqueada: o endereço não muda, a senha não aparece nele e o aviso é exibido.

**E5 concluída em 09/09/2026.** `/` deixou de abrir o simulador e passou a ser `public/inicio.html`: um convite com "Criar conta" e "Já possui uma conta? Faça o login". O simulador passou a responder em `/dashboard` (e em `/treino`, `/defensoria`, `/oab`, `/tcdf`, que continuam apontando para o mesmo `index.html`).

**Detalhe do Netlify que quase passou despercebido:** arquivo existente vence regra de reescrita. Como `index.html` existe, a regra `/ → /inicio.html 200` seria ignorada e a raiz continuaria abrindo o simulador. Resolvido com o sinal de força — `200!` —, que é a única regra do arquivo que precisa dele. Está comentado no próprio `_redirects`.

**Mudança de destino:** `conta.js` passou a mandar para `/dashboard` depois de entrar, e o link de confirmação de cadastro passou a apontar para `/dashboard`. **Isso exige cadastrar `https://subjetivando.netlify.app/dashboard` nas Redirect URLs do Supabase** — sem isso, a confirmação de e-mail leva a pessoa para o lugar errado, exatamente o defeito da P1-05. Não há registro de que o cadastro tenha sido feito: conferir no painel.

**Ainda pendente da E5:** a página inicial mostra o atalho "continuar de onde parou" a partir da presença da chave de sessão no navegador. É dica de interface, não controle de acesso — quem manda continua sendo a RLS.

**E1 a E4 não bloqueiam o beta. A E5 bloqueava:** enquanto a página pública nova não estivesse pronta, era melhor não abrir para ninguém.

**Armadilhas conhecidas para a E6:**

1. a camada `rotas-layer` muda de modo **simulando um clique** em `#modeToggle`, que o `v41.css` oculta desde 09/09/2026 — o roteador precisa substituí-la, não empilhar sobre ela;
2. `v41.css` esconde OAB, TCDF e discursiva por CSS; com rotas passariam a existir dois mecanismos para o mesmo fim;
3. `public/` é a fonte desde 09/09/2026 e não existe etapa de geração. Ver P2-14.

### P1-16 — Identidade de questão e modelo de sessão

**Estado:** PLANEJADA em 09/09/2026, execução não iniciada. O sintoma de 20/09/2026 foi contido em 22/09/2026 (ver abaixo); a fragilidade estrutural continua.

**Defeito confirmado em 20/09/2026: o instantâneo restaura um painel de resposta degradado.** No navegador da autora, o `subj_sessao_v1` gravado continha `espelhoHTML` com 5.796 caracteres de marcação mas apenas 886 caracteres de texto, e `espelhoAberto: true`. Restaurado, o painel abria com 83 px de altura — o cabeçalho e nada mais — e o `interceptar()` o fechava no clique seguinte. É o que a autora descreveu como "aparece só a linha com o título e logo fecha".

Apagadas as chaves `subj_sessao_v1` e `subj_tela_v1`, e sorteada uma questão de banca nova, o painel passou a abrir com o `espelhoText` preenchido e a permanecer aberto. Conferido no site publicado, na janela da autora.

**A causa é estrutural, não o conteúdo de um instantâneo.** `salvar()` grava `espelhoPanel.innerHTML` sem verificar se o painel tem conteúdo, e `limparEspelho()` — acrescentada em 09/09/2026 para corrigir a resposta trocada — esvazia esse painel no sorteio. Um `salvar()` disparado na janela entre o esvaziamento e a renderização grava um espelho aberto e vazio, que o `restaurar()` devolve fielmente. A versão do instantâneo não protege contra isso: ela distingue formatos, não estados possíveis.

**Contido em 22/09/2026, na leitura:** `restaurar()` passou a conferir, antes de repor a questão, se o painel salvo tem texto em `#espelhoText` ou `#modeloText`. Com o botão de resposta visível e sem texto, a questão não é reposta; a configuração volta e o próximo sorteio parte do zero. Reproduzido antes da correção com um instantâneo montado igual ao da autora (painel de 83 px, 0 caracteres) e conferido depois (tela de configuração, sem painel vazio). Registro em `ALTERACOES.md`.

**O que o modelo de sessão novo precisa fazer:** validar o estado que restaura, não só a versão dele. A correção de 22/09 faz isso para um estado impossível conhecido; um modelo de sessão por identidade de questão tornaria a classe inteira de erro impossível.

**Problema:** nenhuma questão tem identidade própria. O aplicativo identifica uma questão pelo **hash do texto da pergunta** (`'q' + base36`, gravado como `questao_hash` no Supabase) — se o texto for corrigido, a questão vira outra e a anotação e o "já respondida" da pessoa se perdem. E a camada D restaura a tela **reproduzindo o HTML salvo do DOM**, sem saber de que questão se trata: ela redesenha pixels, não estado.

Foi exatamente essa ausência de identidade que produziu o defeito da resposta trocada corrigido em 09/09/2026. Aquela correção fecha o sintoma — o painel agora é esvaziado a cada sorteio —, **não a fragilidade estrutural**. Enquanto a sessão for um retrato do DOM, qualquer alteração futura na tela pode reabrir a mesma classe de erro.

**Constatação do diagnóstico, para não se perder:** não existe no código nenhum rótulo "QUESTÃO ID" nem número exibido de questão. Procurado em `app.js`, `index.html` e `v41.css`: não há. O único identificador existente é o hash do texto.

**Etapas, em ordem:**

| | Etapa | Entrega | Risco |
|---|---|---|---|
| F1 | Diagnóstico da associação pergunta/resposta e da origem do identificador | **CONCLUÍDA em 09/09/2026** — causa localizada na camada D; acervo íntegro; "QUESTÃO ID" não existe | nenhum |
| F2 | Identificadores imutáveis por questão; acervo extraído do `app.js` para JSON | cada questão com id estável, independente do texto | **alto** |
| F3 | Migração de `questao_hash` para `questao_id` no Supabase | anotações e "respondida" deixam de depender do texto | alto |
| F4 | Modelo de sessão: trilha ordenada de questões e estado por questão | anotação, resposta revelada e "respondida" guardados por id | médio |
| F5 | Anterior e próxima sem re-sortear e sem perder estado | navegação dentro da trilha | médio |
| F6 | Endereço por questão, histórico do navegador e retomada de sessão | URL compartilhável; voltar e avançar funcionando | médio |

**Fora deste escopo, por decisão da autora em 09/09/2026:** componentes responsivos, tokens de design e eliminação da cadeia de sobreposições de CSS. Esse trabalho será feito em outro lugar. Ver P2-13.

**Critérios de aceitação a escrever antes da F2:** lista derivada das HIG e da WCAG, ainda não redigida.

**Armadilha conhecida:** a F2 mexe no `app.js` de 3,4 MB, que é o mesmo arquivo redesenhado pelo Codex. Qualquer alteração precisa ser feita por âncora conferida, nunca por reescrita do arquivo. Ver P2-14.

**Relação com a IA da prova oral (P2-18):** a correção por IA vai gravar avaliações por questão. Sem identificador estável (F2 e F3), essas avaliações herdam o mesmo problema das anotações.

## 4. P2 — ANTES DA COBRANÇA

### P2-01 — Separar o HTML monolítico

**Estado:** EM EXECUÇÃO. A saída pública separa HTML, CSS e JavaScript; dados e módulos ainda permanecem concentrados no JavaScript.  
**Ordem:** CSS, scripts, dados, build do Tailwind.

**Build do Tailwind feito em 20/09/2026** — ver P2-02. Desde 22/09/2026 a versão (3.4.19) está fixada em `package.json` e o arquivo é gerado com `npm run css`.

**Próximo passo desta pendência, aberto em 20/09/2026:** mover o `<link>` do `tailwind.css` para antes de `styles.css` e de `v41.css` e retirar os 85 `!important`, que existem só por causa da ordem invertida. A troca altera quem vence entre as classes utilitárias e as regras autorais, e um efeito já é conhecido: sete botões (`btnPistas`, `btnToggleEspelho`, `btnTheme`, `btnManage`, `btnNotasMenu`, `btnSom`, `btnAbout`) passam de `justify-content: flex-start` para `center`. Exige a mesma comparação elemento a elemento usada na P2-02, e decisão sobre qual dos dois valores é o desejado em cada caso.

### P2-04 — Revisar direitos autorais do acervo

**Estado:** NÃO INICIADA.  
**Critério:** origem, licença, possibilidade de reprodução, atribuição e classificação de cada conjunto.

**Ponto levantado em 09/09/2026 e não resolvido:** `acervo/pipeline/FONTES.md` e `acervo/pipeline/ESTADO.md` registram que o acervo veio de material compilado, e que o processamento removeu "URLs de curso" e cabeçalhos de "Material usado". Antes de abrir o site a terceiros, convém definir o enquadramento da origem dessas 750 questões e respostas. É matéria da autora, não do desenvolvimento. Pesa também sobre a P2-18: enviar esse conteúdo a um provedor de IA é outro uso dele.

### P2-05 — Definir política editorial

**Estado:** NÃO INICIADA.  
**Campos:** fonte, banca, ano, cargo, tipo, última revisão e responsável.

### P2-06 — Definir modelo de conteúdo premium

**Estado:** EM ANÁLISE.  
**Recomendação preliminar:** retirar conteúdo premium do HTML público e entregá-lo após autorização do backend.

### P2-07 — Criar ambientes separados

**Estado:** NÃO INICIADA.  
**Inclui:** homologação e produção, preferencialmente com Supabase separado.

### P2-08 — Implementar pagamentos em modo de teste

**Estado:** NÃO INICIADA.  
**Inclui:** checkout hospedado, função segura, webhook, idempotência e portal do cliente.

### P2-09 — Criar tabela e regras de assinatura

**Estado:** NÃO INICIADA.  
**Regra:** usuário não pode ativar a própria assinatura.

### P2-10 — Criar termos comerciais

**Estado:** NÃO INICIADA.  
**Inclui:** preço, renovação, cancelamento, reembolso, suporte e identificação do fornecedor.

### P2-11 — Consultar contador

**Estado:** NÃO INICIADA.  
**Objetivo:** natureza da atividade, formalização, tributação, nota fiscal e obrigações.

### P2-12 — Auditoria técnica independente

**Estado:** NÃO INICIADA.  
**Obrigatória antes do primeiro pagamento real.**

### P2-13 — Concluir o sistema de design

*Antes numerada P2-05, repetida.*

**Estado:** EM EXECUÇÃO. Primeiro passo aplicado em 09/09/2026 (bloco 16 do CSS).

**Diagnóstico medido nos 115 KB de marcação:** a interface é export do Pen.dev — 285 atributos `data-pencil-name`, 289 `div` para 55 `button`, 31 medidas fixas em pixel. O export traz os valores onde o cursor parou, não uma escala. O que produzia a aparência genérica era, sobretudo, `10px` sendo o tamanho de fonte dominante do site (37 usos de 78) somado a `tracking: 1px` sobre esses 10px (0,1em, em 25 usos).

**Feito:** rótulos de 10px para 12px, grau menor de 9px para 11px, entreletras de 0,1em para 0,04em, respiro dos cartões de 40px para 24px (16px em tela estreita), raios de 24/40/62/70 unificados em 16px. Sem alterar marcação, cor, fonte ou script.

**Falta:**

- nomear as 26 cores hexadecimais como variáveis e eliminar os véus redundantes — quatro sobreposições de preto e branco com opacidades diferentes fazendo a mesma coisa;
- reduzir os 13 valores de espaçamento a uma escala de cinco;
- definir os componentes (botão primário, secundário, segmento, cartão, campo, modal) em vez de repetir listas de classes;
- decidir sobre o uso de maiúsculas nos rótulos, que é escolha visual e não foi tocada.

**Restrições que a continuação precisa respeitar:** a auditoria de acessibilidade fechou com zero violações axe-core, anel de foco autoral, landmarks e gestão de foco nos modais — nada disso pode regredir; o `!important` dos blocos 15 e 16 existe porque o `tailwind.css` entra na cascata depois desta folha (ver P2-01); os atributos `data-pencil-name` não são lixo de export removível — `styles.css`, `v41.css` e o `app.js` os usam como seletores (77, 50 e 2 ocorrências em 22/09/2026).

**Observação de método:** exportar de novo a partir de um editor de canvas reintroduz o mesmo problema — foi o export que causou o colapso de layout no celular corrigido em 09/09/2026. Usar ferramenta de design para decidir, não para gerar o código final.

### P2-15 — Conteúdo de OAB, TCDF e discursiva apenas oculto por CSS

*Antes numerada P2-07, repetida.*

**Estado:** NÃO INICIADA.  
**Situação:** o `v41.css` esconde `[data-mode="oab"]`, `[data-mode="tcdf"]`, `[data-sub="discursiva"]` e o seletor `#modeToggle`. A decisão de nichar em Defensoria e prova oral foi confirmada pela autora em 09/09/2026.  
**Ponto de atenção:** ocultar não é remover. Os 55 itens de OAB, os 55 temas e 37 discursivas do TCDF continuam dentro de `public/assets/app.js`, público e baixável, e as rotas `/oab` e `/tcdf` continuam existindo na camada de rotas. Se a intenção for retirar do produto, e não apenas da vista, é preciso remover os dados do arquivo publicado.

### P2-16 — Completar as lacunas dos documentos institucionais

*Antes numerada P2-08, repetida.*

**Estado:** ABERTA em 09/09/2026. As páginas existem; o conteúdo está incompleto e assinalado como tal.

**Faltam, e nenhuma pode ser suprida por inferência:**

| Onde | O que falta |
|---|---|
| Todas | nome da responsável e e-mail de contato |
| Privacidade | base legal; região do servidor Supabase e base legal da transferência internacional; prazos de retenção; prazo de atendimento a pedidos de exclusão e exportação |
| Termos | regras sobre a origem do acervo e direitos autorais; limitação de responsabilidade; foro |
| Sobre | apresentação da responsável |

Contagem das marcas "a completar" em 22/09/2026: 9 na privacidade, 6 nos termos, 2 na sobre. A lacuna "prazo para deixar de usar CDNs" saiu da privacidade nessa data, porque o site deixou de usar CDN (ver P2-17): o texto passou a dizer que nenhuma página carrega recurso de outras empresas.

**Verificado, e vale manter no texto:** o site não usa cookies — `document.cookie` não aparece uma única vez no código publicado — e não há rastreador algum. Conferido, não presumido.

**Quando a IA da prova oral existir (P2-18):** a política precisa passar a tratar gravação de voz, transcrição e o envio do texto a um provedor de IA. Hoje ela afirma, corretamente, que o site não grava áudio e bloqueia o microfone.

### P2-18 — Treino da prova oral com IA

**Estado:** EM ANÁLISE, aberta em 22/09/2026.  
**Objetivo:** a pessoa responde em voz alta, o site transcreve, compara com o padrão de resposta e devolve uma avaliação; depois, um examinador que faz reperguntas. É o diferencial do produto na visão da autora e já consta como recurso do nível pago na seção 2.6 de `ARQUITETURA.md`.  
**Proposta técnica:** `IA-PROVA-ORAL.md`, escrita para quem não é da área: OpenRouter como ponto único de acesso aos modelos, RAG como "buscar antes de corrigir", base vetorial no próprio Supabase, custo estimado por treino e fases.

**Próximo passo (fase 0, sem código):** testar a correção no chat do OpenRouter com as instruções de `IA-PROMPT-EXAMINADOR.md` e registrar aqui o modelo escolhido, os ajustes nas instruções e o custo por correção.

**Dependências:**

- chave da OpenRouter só no servidor (função do Supabase), nunca no `app.js`;
- P2-04 (direitos autorais do acervo) antes de enviar o conteúdo a um provedor;
- P1-16, F2 e F3, para avaliações por questão sobreviverem a correções de texto;
- P1-12, porque o `##ROTEIRO##` revisado é a melhor lista de pontos para corrigir;
- `Permissions-Policy` do `_headers` hoje bloqueia o microfone (`microphone=()`); precisará liberar para o próprio site;
- política de privacidade atualizada antes da primeira gravação (P2-16).

## 5. P3 — INFRAESTRUTURA E QUALIDADE

### P3-01 — Comprar domínio

**Estado:** NÃO INICIADA.  
**Observação:** comprar domínio não exige contratar nova hospedagem.

### P3-02 — Configurar domínio e HTTPS no Netlify

**Estado:** BLOQUEADA pela P3-01.

### P3-03 — Atualizar URLs no Supabase

**Estado:** BLOQUEADA pela P3-02.

### P3-04 — Configurar e-mail transacional no domínio

**Estado:** BLOQUEADA pela P3-01.

### P3-05 — Criar `_headers` e CSP

**Estado:** EM EXECUÇÃO. Cabeçalhos criados e CSP em modo de relatório (`Content-Security-Policy-Report-Only`).

**22/09/2026:** os três motivos que impediam a política efetiva deixaram de existir — o Tailwind é arquivo local desde 20/09, e a biblioteca do Supabase e as fontes passaram a ser servidas pelo próprio site. A política foi reduzida ao que o site usa: `'self'` para script, estilo e fonte, `data:` para imagem e fonte, e o endereço do projeto Supabase em `connect-src`. Nenhuma violação apareceu no console ao abrir as oito páginas no servidor local, que aplica o `_headers`.

**Próximo passo:** publicar, conferir o console e os cabeçalhos no endereço real, testar login, recuperação, impressão e os dois temas, e então trocar `Content-Security-Policy-Report-Only` por `Content-Security-Policy`. `'unsafe-inline'` continua necessário: `inicio.html` tem um script na própria página e o `index.html` usa atributos `style`.

### P3-06 — Implementar monitoramento de erros

**Estado:** NÃO INICIADA.  
**Regra:** não registrar anotações, senhas, tokens ou conteúdo sensível.

### P3-07 — Melhorar desempenho

**Estado:** EM EXECUÇÃO. CSS e JavaScript foram separados para permitir cache; carregamento sob demanda e redução do pacote ainda pendentes.  
**Inclui:** carregamento sob demanda, cache, compressão e redução do pacote inicial.

**22/09/2026:** o simulador deixou de abrir conexão com `fonts.googleapis.com`, `fonts.gstatic.com` e `cdn.jsdelivr.net`. Todo arquivo vem do próprio endereço. O `app.js` continua com 3,4 MB, 97% deles em cinco linhas de dados.

### P3-08 — Criar suporte e procedimento de incidente

**Estado:** NÃO INICIADA.

### P3-09 — Adicionar SEO e compartilhamento

**Estado:** NÃO INICIADA.  
**Inclui:** descrição, Open Graph, título, ícones, canonical, robots e sitemap.

### P3-10 — Sem registro

**Estado:** A CONFIRMAR. As entradas de 09/09/2026 de `ALTERACOES.md` dizem "abrem-se P1-14 e P3-10", mas a P3-10 nunca foi escrita neste arquivo. Se alguém lembrar do assunto, registrar aqui; senão, marcar como DESCARTADA.

### P3-11 — Reorganizar o simulador para tela estreita

**Estado:** NÃO INICIADA.  
**Problema:** corrigidos os defeitos da P1-03, o celular passa a mostrar tudo, mas empilhado numa única coluna de cerca de 2.000px. Configuração no alto, questão no meio, cronômetro e anotação bem abaixo. Quem toca em "Iniciar tempo" vê o efeito longe do botão, às vezes fora da tela.  
**Observação:** é decisão de design, não defeito. Exige escolher o que fica fixo, o que vira gaveta e onde mora o cronômetro. Não iniciar antes de o beta indicar se as pessoas usam pelo celular.

## 6. P4 — IDEIAS FUTURAS

- métricas de desempenho por disciplina;
- revisão espaçada;
- metas personalizáveis;
- exportação de progresso;
- autenticação por link mágico;
- instalação como PWA;
- painel editorial separado;
- ferramentas para revisão humana do conteúdo;
- plano anual;
- testes A/B não invasivos;
- integração com calendário de estudos.

Nenhum item P4 deve ser implementado enquanto houver pendência P0 ou P1 relevante.

## 7. CONCLUÍDAS

### P0-01 — Auditar RLS do Supabase

**Estado:** CONCLUÍDA em 09/09/2026.  
**Objetivo:** garantir que cada usuário só acesse seus próprios dados.

**Evidência documental:** `auditoria_rls.sql` executado no SQL Editor. RLS ativada (`relrowsecurity = true`) nas seis tabelas `anotacoes`, `perfis`, `questoes_customizadas`, `questoes_usadas`, `respostas` e `sessoes`. Existem 20 políticas, todas comparando `auth.uid()` com a coluna de proprietário (`usuario_id`, ou `id` em `perfis`).

**Evidência prática:** sessão anônima no site publicado, usando o cliente Supabase da própria aplicação, retornou 0 linhas nas seis tabelas e teve a gravação recusada com `new row violates row-level security policy`. O isolamento foi comprovado contra a API pública, não apenas inferido das políticas.

**Observações que não bloqueiam:**

- as políticas estão atribuídas ao papel `public`, que inclui `anon`. Isso é seguro porque `auth.uid()` é nulo em sessão anônima e a comparação nunca resulta verdadeira. Restringir ao papel `authenticated` é endurecimento opcional, não correção;
- `perfis`, `questoes_customizadas`, `questoes_usadas` e `sessoes` não possuem política de DELETE, logo nenhuma exclusão é permitida nelas. Conferido no código em 22/09/2026 que o aplicativo não depende disso — ver P1-13;
- o alerta do linter sobre `lidar_novo_usuario()` não é explorável pela API pública: a chamada anônima por RPC retorna `PGRST202`, porque o PostgREST não expõe funções de gatilho. Executar `corrigir_funcao_lidar_novo_usuario.sql` passa a ser endurecimento opcional.

### P1-01 — Padronizar entrada como `index.html`

**Estado:** CONCLUÍDA em 15/08/2026. A entrada publicável é `public/index.html`.

### P1-02 — Corrigir e testar `_redirects`

**Estado:** CONCLUÍDA em 09/09/2026. O painel do Netlify registra as 8 regras processadas sem erro nos deploys de 15/08/2026 e de 09/09/2026.  
**Rotas:** `/`, `/defensoria`, `/oab`, `/tcdf` e regra geral da aplicação. As rotas acrescentadas depois estão na seção 2.1 do `README.md`.

### P1-04 — Remover identidade fictícia

**Estado:** CONCLUÍDA em 15/08/2026.  
**Itens:** "Carlos", "Carlos Eduardo" e "Assinante Premium" no estado anônimo.

### P1-05 — Concluir recuperação de senha

**Estado:** CONCLUÍDA em 09/09/2026.

**Causa raiz encontrada:** a lista de *Redirect URLs* do Supabase estava vazia. Com ela vazia, o Supabase aceita apenas o *Site URL* e descarta silenciosamente o endereço `/atualizar-senha` pedido pelo frontend, levando o usuário à página inicial. O defeito estava na configuração do painel, não no código, e por isso as correções de 15/08 não o resolveram.

**Correção:** cadastrados `https://subjetivando.netlify.app` e `https://subjetivando.netlify.app/atualizar-senha` em *Authentication → URL Configuration*.

**Teste real executado em 09/09/2026 com conta e e-mail verdadeiros:** cadastro, e-mail de confirmação recebido na caixa de entrada em cerca de três minutos, confirmação, login, estado "CONTA SINCRONIZADA", logout, pedido de recuperação, link levando a `/atualizar-senha` com a mensagem "Link confirmado", gravação da nova senha e novo login com ela. Todas as etapas passaram.

**Ainda não testado:** expiração do link por decurso de prazo e comportamento do limite de envio de e-mails do plano gratuito.

### P1-08 — Pedir confirmação para incorporar dados locais

**Estado:** CONCLUÍDA em 09/09/2026.

**Causa raiz:** `autorizarIncorporacao` gravava apenas o "sim" em `subj_sync_consent_v1_<usuario>`. A recusa não deixava rastro, e o que segurava a pergunta entre uma vez e outra era `sessionStorage`, que morre com a aba. Qualquer novo carregamento de página com sessão ativa — o retorno do link de confirmação de e-mail, por exemplo — trazia a pergunta de volta, e ela voltaria a cada recarregamento, indefinidamente.

**Correção:** a resposta passa a ser gravada nos dois sentidos e a recusa é respeitada. Para que "Cancelar" signifique "agora não" e não "nunca mais" — o que prenderia o usuário em "Sincronização pausada", já que não há controle na tela para reconsiderar —, a marca é apagada no logout. Quem recusou volta a ser perguntado no próximo login, usando o botão SAIR que já existe.

**Nota de projeto:** a correção foi escrita para não depender de qual evento do Supabase dispara em cada caminho (`SIGNED_IN`, `INITIAL_SESSION`, retorno de link), porque isso não foi medido.

**Teste automatizado:** `node scripts/teste_consentimento.mjs`. Extrai a função real de `public/assets/app.js` e verifica cinco casos; o decisivo é o segundo, em que a recusa já registrada não pode gerar nenhuma pergunta. Cinco de cinco passam.

### P1-13 — Conferir exclusão sincronizada de temas e reinício de questões usadas

**Estado:** CONCLUÍDA em 22/09/2026, por leitura do código. Não testada contra o Supabase.  
**Problema:** as tabelas `questoes_customizadas`, `questoes_usadas`, `sessoes` e `perfis` não têm política de DELETE, então nenhuma linha pode ser apagada por usuário. Se a aplicação dependesse de DELETE para apagar um tema personalizado ou reiniciar questões usadas, a operação falharia silenciosamente na nuvem.

**Constatação:** a camada de sincronização do `app.js` só usa `.delete()` em `respostas` e `anotacoes`, as duas tabelas que têm política de DELETE (segundo a auditoria da P0-01, só as outras quatro não têm). Temas personalizados e questões usadas são gravados com `upsert` da lista inteira por modo e categoria (`onConflict: 'usuario_id,modo,categoria'`): apagar um tema ou reiniciar as usadas regrava a linha com a lista nova, por UPDATE. A sessão também é `upsert` de uma linha por usuário. Nenhuma operação depende de DELETE onde ele é proibido.

**Observação menor, sem correção:** ao recarregar, `restaurar()` faz um sorteio sintético e depois apaga com `localStorage.removeItem` as listas `used_*` que esse sorteio criou. A sincronização só intercepta `setItem`; se houver sessão ativa nesse instante, a nuvem pode ficar com uma questão marcada como usada sem ter sido treinada. Efeito: a questão demora mais a voltar no sorteio.

### P1-17 — Dois botões "Sortear outra" com o mesmo id

**Estado:** CONCLUÍDA em 20/09/2026. Rótulo corrigido em 22/09/2026. Registros em `ALTERACOES.md`.

**Sintoma:** depois do segundo sorteio seguido, a tela mostrava duas linhas com "Sortear outra", ambas visíveis e ambas com `id="btnRedraw"`. Uma ficava em `#questionTopActions`, outra em `#drawActions`.

**Causa, conferida no `app.js`:** cada sorteio reescreve `drawActions.innerHTML` criando um `<button id="btnRedraw">` novo. Um `MutationObserver` sobre `#drawActions` chama `moveRedrawToTop()`, que fazia `document.getElementById('btnRedraw')` e movia o resultado para `#questionTopActions`. Como `getElementById` devolve o **primeiro** do documento, e `#questionTopActions` vem antes de `#drawActions` na marcação, a partir do segundo sorteio a função encontrava o botão que ela mesma já tinha movido, caía no `return` e deixava o novo onde estava.

**A correção proposta inicialmente estava errada pela metade, e a leitura do código antes de editar mostrou por quê.** O ouvinte `doDraw` fica sempre no botão do topo, porque a linha que o registra também usa `getElementById` e encontra o do topo primeiro. O duplicado de baixo nunca recebe ouvinte — clicar nele não faz nada. Remover o do topo e promover o novo teria parado o "Sortear outra".

**O que foi feito em 20/09:** `moveRedrawToTop()` procura o botão dentro de `#drawActions` e, quando já existe um no topo, descarta o recém-criado. Conferido em servidor local nos dois modos, com três sorteios seguidos em cada: um botão visível e enunciado diferente a cada clique.

**Rótulo, 22/09:** `moveRedrawToTop()` escrevia "Sortear outra" em qualquer botão que movia, inclusive quando o sorteio de tema o criava como "Sortear outro". Passou a manter o rótulo do sorteio, e o botão do topo recebe o rótulo do sorteio atual quando o duplicado é descartado. Conferido: "Sortear outro" em tema, "Sortear outra" em questão, um só botão, enunciado diferente a cada clique.

### P2-02 — Retirar Tailwind CDN da produção

**Estado:** CONCLUÍDA em 20/09/2026.

**Tailwind retirado em 20/09/2026.** O CSS passou a ser gerado na máquina, a partir de `tailwind.config.js`, e servido como `public/assets/tailwind.css`. As 339 classes utilitárias não precisaram ser substituídas: o gerador varre o `index.html` e o `app.js` e escreve só as regras em uso. Conferido elemento a elemento, em duas larguras, com zero diferenças. Registro em `ALTERACOES.md`.

**O que a conclusão não resolve.** A configuração que estava dentro do `index.html` nunca foi lida pelo CDN, porque era atribuída antes do script que a lê. As três fontes e as oito cores `botanic` nunca chegaram ao Tailwind, e a normalização nunca foi desligada. O arquivo gerado reproduz isso de propósito, para não alterar o site. Registrar o tema de verdade é decisão de desenho, não de migração.

**Os 85 `!important` continuam lá.** Existem porque o Tailwind entra na cascata depois de `styles.css` e de `v41.css`, e o arquivo gerado foi posto na mesma posição para preservar o resultado. Retirá-los é mover o `<link>` para antes das outras folhas e conferir de novo — ver P2-01.

**Font Awesome removido em 13/09/2026.** Os 15 ícones passaram a ser SVG escritos na própria página, e o `<link>` do CDN saiu do `index.html` — 100 KB a menos por visita e uma dependência externa a menos.

### P2-03 — Fixar versões das dependências

**Estado:** CONCLUÍDA em 22/09/2026.

Nenhum arquivo do site vem mais de CDN, e todo código de terceiros tem versão fixa: Supabase JS 2.116.0 em `public/assets/vendor/supabase.js` (P2-17), Tailwind 3.4.19 em `package.json`, usado só para gerar o `tailwind.css`, e as fontes Inter, Lora e Plus Jakarta Sans em `public/assets/fonts/`. Atualizar qualquer uma é decisão explícita: trocar a versão em `package.json`, rodar `npm run vendor` ou `npm run css` e repetir os testes.

### P2-14 — A pasta `public/` virou a fonte do site

*Antes numerada P2-06, repetida.*

**Estado:** DECIDIDO E APLICADO em 09/09/2026. Encerrado em 10/09/2026 por remoção do script.

**O que mudou:** o redesenho feito no Codex alterou apenas `public/` — `index.html`, `assets/styles.css`, `assets/app.js` — e acrescentou `assets/v41.css`. Não existia versão correspondente em `minha-banca.NOVO_3.html`.

**Por que a mudança era obrigatória:** o Netlify executava `python3 scripts/build_public.py` a cada publicação. Esse script regenerava `public/` a partir da fonte antiga. Publicar sem desligá-lo teria apagado o design novo no próprio deploy, **sem gerar erro** — o site voltaria ao design anterior em silêncio.

**Aplicado:** `netlify.toml` passou a trazer `command = ""` com a explicação no próprio arquivo; `README.md` e `TESTES.md` deixaram de mandar rodar o build.

**Verificado em 09/09/2026:** as quatro correções de código de 09/09 (tradução de erros e consentimento) e os blocos 15 e 16 do CSS sobreviveram ao redesenho; a estrutura de acessibilidade (`header`, `main`, `footer`, `aside`, skip-link, `sr-only`) está preservada; o acervo permanece em 750 · 55 · 55 · 6 · 37; `node --check` aprova o `app.js`.

**Encerrado em 10/09/2026 por remoção.** `scripts/build_public.py` e os arquivos que ele lia — `minha-banca.NOVO_3.html`, `minha-banca.NOVO.html`, `minha-banca.BACKUP.html` e as cópias de `_headers`, `_redirects` e `robots.txt` da raiz — foram removidos do repositório. A proteção deixou de depender de alguém ler um comentário: o script não existe mais. Tudo continua recuperável pelo histórico do Git.

**Em 20/09/2026** a reorganização da pasta retirou também o `minha-banca.html` da raiz, que era o estado publicado em 15/08/2026. Recuperável com `git show 126e3d7~1:minha-banca.html`.

**Pendente de decisão futura:** se algum dia o projeto quiser voltar a ter fonte única, o caminho é reconstruir a fonte a partir de `public/`, e não o contrário.

### P2-17 — Hospedar a biblioteca do Supabase no próprio site

*Antes numerada P2-09, repetida.*

**Estado:** CONCLUÍDA em 22/09/2026.

**Situação anterior:** o simulador e as páginas `/login`, `/cadastro` e `/recuperar-senha` carregavam `@supabase/supabase-js@2` da CDN jsDelivr. O IP de quem abria a tela era entregue à jsDelivr; se a CDN falhasse, a pessoa não conseguia entrar; e o `@2` sem número seguia a versão mais nova publicada, sem teste — em 22/09/2026 a CDN passou a servir a 2.117.0, lançada naquele dia.

**Feito:** versão fixada em 2.116.0, a que estava no ar no teste de autenticação de ponta a ponta de 09/09/2026, servida de `public/assets/vendor/supabase.js` e gerada por `npm run vendor`. O arquivo é idêntico ao que a CDN servia para essa versão. Conferido no navegador: `/login` sem requisição externa, login com conta inexistente recebe do Supabase "E-mail ou senha incorretos.", simulador carrega as camadas de conta e sincronização sem erro.

### Marcos

#### 2026-09-22 — Revisão de organização e correções (branch `modificacoes-fernando`)

Auditoria voltou a passar, ferramentas de verificação (`npm run dev`, `check`, `css`, `vendor`) e GitHub Actions criados, biblioteca do Supabase e fontes servidas pelo próprio site, dois defeitos corrigidos no `app.js` (instantâneo com resposta vazia e rótulo do "Sortear outro"), documentação movida para `docs/` e atualizada, IDs repetidos desta lista renumerados. Fecham-se P1-13, P2-03 e P2-17; abre-se P2-18. Registro em `ALTERACOES.md`.

#### 2026-09-09 — Resposta trocada após recarregar a página

Corrigido o defeito que exibia a resposta de uma questão anterior para a questão mostrada na tela. Causa: o painel de resposta não era esvaziado no sorteio, e a camada de continuidade tratava o texto remanescente como já renderizado, salvando no instantâneo a questão nova com a resposta velha. Acrescentada `limparEspelho()` nas cinco funções de sorteio e elevada a versão do instantâneo de 2 para 3, o que descarta os instantâneos já contaminados. Verificado no site publicado, na sequência exata que reproduzia o erro. Commit `01f59db`. Abre-se P1-16.

#### 2026-09-09 — Autenticação comprovada de ponta a ponta

Cadastro, confirmação por e-mail, login, logout, recuperação de senha, definição de nova senha e sincronização testados com conta e e-mail reais no site publicado. Fecha-se P1-05. Reabre-se P1-08 por defeito observado; abrem-se P1-14 e P3-10.

#### 2026-09-09 — Controle de versão, publicação contínua e comprovação da RLS

Projeto colocado sob Git com commit inicial e etiqueta `publicado-2026-08-15`, publicado em repositório privado no GitHub e ligado ao Netlify por publicação contínua a partir da branch `main`. O deploy manual por arrastar pasta foi encerrado. RLS auditada no painel e comprovada na prática contra a API pública. Fecham-se P0-01 e P1-02; abre-se P1-13.

#### 2026-08-15 — Criação da documentação permanente

Foram criados os oito documentos centrais de contexto, arquitetura, regras, dados, segurança, testes, alterações e pendências.
