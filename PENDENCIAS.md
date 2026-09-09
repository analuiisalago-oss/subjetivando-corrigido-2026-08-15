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

Ao concluir, registrar a mudança em `ALTERACOES.md` e mover o item para “Concluídas”.

## 2. P0 — SEGURANÇA E DADOS

### P0-01 — Auditar RLS do Supabase

**Estado:** CONCLUÍDA em 09/09/2026.  
**Objetivo:** garantir que cada usuário só acesse seus próprios dados.

**Evidência documental:** `auditoria_rls.sql` executado no SQL Editor. RLS ativada (`relrowsecurity = true`) nas seis tabelas `anotacoes`, `perfis`, `questoes_customizadas`, `questoes_usadas`, `respostas` e `sessoes`. Existem 20 políticas, todas comparando `auth.uid()` com a coluna de proprietário (`usuario_id`, ou `id` em `perfis`).

**Evidência prática:** sessão anônima no site publicado, usando o cliente Supabase da própria aplicação, retornou 0 linhas nas seis tabelas e teve a gravação recusada com `new row violates row-level security policy`. O isolamento foi comprovado contra a API pública, não apenas inferido das políticas.

**Observações que não bloqueiam:**

- as políticas estão atribuídas ao papel `public`, que inclui `anon`. Isso é seguro porque `auth.uid()` é nulo em sessão anônima e a comparação nunca resulta verdadeira. Restringir ao papel `authenticated` é endurecimento opcional, não correção;
- `perfis`, `questoes_customizadas`, `questoes_usadas` e `sessoes` não possuem política de DELETE, logo nenhuma exclusão é permitida nelas. Conferir se apagar tema personalizado e reiniciar questões usadas funcionam por atualização da linha — ver P1-13;
- o alerta do linter sobre `lidar_novo_usuario()` não é explorável pela API pública: a chamada anônima por RPC retorna `PGRST202`, porque o PostgREST não expõe funções de gatilho. Executar `corrigir_funcao_lidar_novo_usuario.sql` passa a ser endurecimento opcional.

### P0-02 — Inventariar e proteger segredos

**Estado:** EM ANÁLISE  
**Objetivo:** confirmar que nenhuma chave secreta foi incluída em HTML, GitHub ou arquivos compartilhados.  
**Conclusão exige:** inventário, rotação de segredos eventualmente expostos e variáveis de ambiente configuradas.

**Avanço:** o backup não contém segredo privado identificável. Varredura repetida em 09/09/2026 antes do primeiro commit: as únicas ocorrências de `ANTHROPIC_API_KEY`, `service_role` e `sb_secret` são nomes de variáveis em documentação e scripts, sem valor real. O repositório foi criado como privado e `private/` ficou fora do versionamento. Ainda falta verificar as variáveis de ambiente configuradas no Netlify e no Supabase.

### P0-03 — Confirmar backups do Supabase

**Estado:** NÃO INICIADA  
**Conclusão exige:** frequência, retenção, responsável e teste documentado de restauração.

## 3. P1 — BETA PÚBLICO

### P1-01 — Padronizar entrada como `index.html`

**Estado:** CONCLUÍDA em 15/08/2026. A entrada publicável é `public/index.html`.

### P1-02 — Corrigir e testar `_redirects`

**Estado:** CONCLUÍDA em 09/09/2026. O painel do Netlify registra as 8 regras processadas sem erro nos deploys de 15/08/2026 e de 09/09/2026.  
**Rotas:** `/`, `/defensoria`, `/oab`, `/tcdf` e regra geral da aplicação.

### P1-03 — Corrigir responsividade

**Estado:** EM EXECUÇÃO. Testada em iPhone real e em viewport emulado de 375px em 09/09/2026. Dois defeitos encontrados e corrigidos; um problema de organização permanece, movido para P3-11.

**Defeito 1, corrigido:** abaixo de 1100px as colunas empilham e os cartões com `flex: 1 1 0` passam a repartir altura em vez de largura. Dentro de contêiner de altura automática eles colapsam e, com `overflow: hidden`, escondem o conteúdo. Medido em 375px: o cartão da questão tinha 50px de caixa para 482px de conteúdo, ocultando 432px — incluindo o padrão de resposta e o botão de ocultar.

**Defeito 2, corrigido:** a barra do topo tem altura fixa de 64px; no celular o grupo da direita quebrava de linha e cobria o conteúdo da página.

**Correção:** bloco 15 do CSS, dentro de `@media (max-width: 1100px)`, com `flex-basis: auto` nos cartões e altura automática na barra.

**Medições depois da correção, em 375px:** cartão da questão com 620px mostrando o conteúdo inteiro; barra com 98px sem sobrepor; zero elementos com conteúdo cortado; zero transbordamento horizontal. Em 994px o resultado é idêntico ao anterior. Acima de 1100px a regra não se aplica.

**Correção da correção:** a primeira versão publicada não teve efeito nenhum. A regra chegou ao ar íntegra, mas o Tailwind por CDN injeta suas classes num `<style>` criado em tempo de execução, que entra na cascata depois de `styles.css`. Com a mesma especificidade nos dois lugares, vencia a declaração do Tailwind. Resolvido com `!important` nas três declarações, o que passa a ser desnecessário quando o Tailwind deixar de vir por CDN (ver P2-04).

**Lição de método registrada:** testar uma regra injetando-a no fim da cascata pelo navegador não prova que ela funcionará dentro de `styles.css`. A verificação só vale depois de publicada, no arquivo real e na posição real.

**Ainda pendente:** validação visual em 768×1024, 1366×768 e 1920×1080; e o teste em aparelho real depois da publicação.

### P1-04 — Remover identidade fictícia

**Estado:** CONCLUÍDA em 15/08/2026.  
**Itens:** “Carlos”, “Carlos Eduardo” e “Assinante Premium” no estado anônimo.

### P1-05 — Concluir recuperação de senha

**Estado:** CONCLUÍDA em 09/09/2026.

**Causa raiz encontrada:** a lista de *Redirect URLs* do Supabase estava vazia. Com ela vazia, o Supabase aceita apenas o *Site URL* e descarta silenciosamente o endereço `/atualizar-senha` pedido pelo frontend, levando o usuário à página inicial. O defeito estava na configuração do painel, não no código, e por isso as correções de 15/08 não o resolveram.

**Correção:** cadastrados `https://subjetivando.netlify.app` e `https://subjetivando.netlify.app/atualizar-senha` em *Authentication → URL Configuration*.

**Teste real executado em 09/09/2026 com conta e e-mail verdadeiros:** cadastro, e-mail de confirmação recebido na caixa de entrada em cerca de três minutos, confirmação, login, estado "CONTA SINCRONIZADA", logout, pedido de recuperação, link levando a `/atualizar-senha` com a mensagem "Link confirmado", gravação da nova senha e novo login com ela. Todas as etapas passaram.

**Ainda não testado:** expiração do link por decurso de prazo e comportamento do limite de envio de e-mails do plano gratuito.

### P1-06 — Tratar falhas de rede na autenticação

**Estado:** CONCLUÍDA NO FRONTEND em 15/08/2026; falta teste com rede interrompida.  
**Critério:** botões sempre retornam ao estado utilizável e usuário recebe mensagem compreensível.

### P1-07 — Exibir estado de sincronização

**Estado:** CONCLUÍDA NO FRONTEND em 15/08/2026; falta teste em dois dispositivos.

### P1-08 — Pedir confirmação para incorporar dados locais

**Estado:** CONCLUÍDA em 09/09/2026.

**Causa raiz:** `autorizarIncorporacao` gravava apenas o "sim" em `subj_sync_consent_v1_<usuario>`. A recusa não deixava rastro, e o que segurava a pergunta entre uma vez e outra era `sessionStorage`, que morre com a aba. Qualquer novo carregamento de página com sessão ativa — o retorno do link de confirmação de e-mail, por exemplo — trazia a pergunta de volta, e ela voltaria a cada recarregamento, indefinidamente.

**Correção:** a resposta passa a ser gravada nos dois sentidos e a recusa é respeitada. Para que "Cancelar" signifique "agora não" e não "nunca mais" — o que prenderia o usuário em "Sincronização pausada", já que não há controle na tela para reconsiderar —, a marca é apagada no logout. Quem recusou volta a ser perguntado no próximo login, usando o botão SAIR que já existe.

**Nota de projeto:** a correção foi escrita para não depender de qual evento do Supabase dispara em cada caminho (`SIGNED_IN`, `INITIAL_SESSION`, retorno de link), porque isso não foi medido.

**Teste automatizado:** `node scripts/teste_consentimento.mjs`. Extrai a função real de `public/assets/app.js` e verifica cinco casos; o decisivo é o segundo, em que a recusa já registrada não pode gerar nenhuma pergunta. Cinco de cinco passam.

### P1-09 — Implementar exclusão de conta e dados

**Estado:** NÃO INICIADA.

### P1-10 — Criar documentos públicos

**Estado:** NÃO INICIADA.  
**Inclui:** Termos de Uso, Política de Privacidade, contato e aviso de beta.

### P1-11 — Revisar acessibilidade

**Estado:** EM EXECUÇÃO. Auditoria automatizada anterior aprovada; faltam teste responsivo e leitor de tela real.  
**Inclui:** teclado, leitor de tela, modais, redução de movimento e textos pequenos.

### P1-14 — Melhorar o formulário de conta

**Estado:** NÃO INICIADA.  
**Observado no teste real de 09/09/2026:**

- não há como ver a senha digitada, o que impede conferir se ela coincide com o campo de confirmação;
- o requisito mínimo de oito caracteres não é informado antes do erro;
- a tradução de `Password should be at least 6 characters` promete oito caracteres, número que vem da validação do próprio site e não do Supabase. Manter os dois coerentes.

### P1-13 — Conferir exclusão sincronizada de temas e reinício de questões usadas

**Estado:** NÃO INICIADA.  
**Problema:** as tabelas `questoes_customizadas`, `questoes_usadas`, `sessoes` e `perfis` não têm política de DELETE, então nenhuma linha pode ser apagada por usuário. Se a aplicação depender de DELETE para apagar um tema personalizado ou reiniciar questões usadas, a operação falha silenciosamente na nuvem e diverge do estado local.  
**Conclusão exige:** verificar no código se essas operações usam UPDATE da linha inteira; se usarem DELETE, criar a política correspondente ou alterar a operação.

### P1-12 — Consolidar o acervo revisado na interface atual

**Estado:** BLOQUEADA por revisão editorial e jurídica.  
**Problema:** os arquivos intermediários do pipeline contêm respostas reprocessadas com marcadores `##FALA##` e `##ROTEIRO##`, mas a fonte canônica `minha-banca.NOVO_3.html` ainda contém o acervo anterior. Os HTMLs do pipeline usam uma interface mais antiga e não podem substituir a fonte atual.  
**Conclusão exige:** resolver `pipeline/PONTOS-A-VERIFICAR.md`, aprovar o mérito das respostas, mesclar somente os dados na fonte atual, adaptar a apresentação dos marcadores e executar comparação de contagem e regressão visual.

## 4. P2 — ANTES DA COBRANÇA

### P2-01 — Separar o HTML monolítico

**Estado:** EM EXECUÇÃO. A saída pública separa HTML, CSS e JavaScript; dados e módulos ainda permanecem concentrados no JavaScript.  
**Ordem:** CSS, scripts, dados, build do Tailwind.

### P2-02 — Retirar Tailwind CDN da produção

**Estado:** NÃO INICIADA.

### P2-03 — Fixar versões das dependências

**Estado:** NÃO INICIADA.

### P2-04 — Revisar direitos autorais do acervo

**Estado:** NÃO INICIADA.  
**Critério:** origem, licença, possibilidade de reprodução, atribuição e classificação de cada conjunto.

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

**Estado:** EM EXECUÇÃO. Cabeçalhos criados e CSP em modo de relatório; aplicação bloqueante depende da retirada do Tailwind CDN e de testes.

### P3-06 — Implementar monitoramento de erros

**Estado:** NÃO INICIADA.  
**Regra:** não registrar anotações, senhas, tokens ou conteúdo sensível.

### P3-07 — Melhorar desempenho

**Estado:** EM EXECUÇÃO. CSS e JavaScript foram separados para permitir cache; carregamento sob demanda e redução do pacote ainda pendentes.  
**Inclui:** carregamento sob demanda, cache, compressão e redução do pacote inicial.

### P3-08 — Criar suporte e procedimento de incidente

**Estado:** NÃO INICIADA.

### P2-08 — Completar as lacunas dos documentos institucionais

**Estado:** ABERTA em 09/09/2026. As páginas existem; o conteúdo está incompleto e assinalado como tal.

**Faltam, e nenhuma pode ser suprida por inferência:**

| Onde | O que falta |
|---|---|
| Todas | nome da responsável e e-mail de contato |
| Privacidade | base legal; região do servidor Supabase e base legal da transferência internacional; prazos de retenção; prazo de atendimento a pedidos de exclusão e exportação; prazo para deixar de usar CDNs |
| Termos | regras sobre a origem do acervo e direitos autorais; limitação de responsabilidade; foro |
| Sobre | apresentação da responsável |

**Ponto levantado em 09/09/2026 e não resolvido:** `pipeline/FONTES.md` e `pipeline/ESTADO.md` registram que o acervo veio de material compilado, e que o processamento removeu "URLs de curso" e cabeçalhos de "Material usado". Antes de abrir o site a terceiros, convém definir o enquadramento da origem dessas 750 questões e respostas. É matéria da autora, não do desenvolvimento, e fica registrada apenas para não passar em branco.

**Verificado, e vale manter no texto:** o site não usa cookies — `document.cookie` não aparece uma única vez no código publicado — e não há rastreador algum. Conferido, não presumido.

### P2-06 — A pasta `public/` virou a fonte do site

**Estado:** DECIDIDO E APLICADO em 09/09/2026.

**O que mudou:** o redesenho feito no Codex alterou apenas `public/` — `index.html`, `assets/styles.css`, `assets/app.js` — e acrescentou `assets/v41.css`. Não existia versão correspondente em `minha-banca.NOVO_3.html`.

**Por que a mudança era obrigatória:** o Netlify executava `python3 scripts/build_public.py` a cada publicação. Esse script regenera `public/` a partir da fonte antiga. Publicar sem desligá-lo teria apagado o design novo no próprio deploy, **sem gerar erro** — o site voltaria ao design anterior em silêncio.

**Aplicado:** `netlify.toml` passou a trazer `command = ""` com a explicação no próprio arquivo; `README.md` e `TESTES.md` deixaram de mandar rodar o build e passaram a avisar do risco.

**Consequências:**

- `minha-banca.NOVO_3.html` está congelada no design anterior e é **histórico**. Editá-la não produz efeito no site;
- `scripts/build_public.py` não deve ser executado. Mantido no repositório apenas como registro do modelo anterior;
- CSS e JavaScript passam a ser editados diretamente em `public/`;
- `audit_project.mjs` e `teste_consentimento.mjs` continuam válidos: leem `public/assets/app.js`, que agora é a fonte.

**Verificado nesta data:** as quatro correções de código de 09/09 (tradução de erros e consentimento) e os blocos 15 e 16 do CSS sobreviveram ao redesenho; a estrutura de acessibilidade (`header`, `main`, `footer`, `aside`, skip-link, `sr-only`) está preservada; o acervo permanece em 750 · 55 · 55 · 6 · 37; `node --check` aprova o `app.js`.

**Pendente de decisão futura:** se algum dia o projeto quiser voltar a ter fonte única, o caminho é reconstruir a fonte a partir de `public/`, e não o contrário.

### P2-07 — Conteúdo de OAB, TCDF e discursiva apenas oculto por CSS

**Estado:** NÃO INICIADA.  
**Situação:** o `v41.css` esconde `[data-mode="oab"]`, `[data-mode="tcdf"]`, `[data-sub="discursiva"]` e o seletor `#modeToggle`. A decisão de nichar em Defensoria e prova oral foi confirmada pela autora em 09/09/2026.  
**Ponto de atenção:** ocultar não é remover. Os 55 itens de OAB, os 55 temas e 37 discursivas do TCDF continuam dentro de `public/assets/app.js`, público e baixável, e as rotas `/oab` e `/tcdf` continuam existindo na camada de rotas. Se a intenção for retirar do produto, e não apenas da vista, é preciso remover os dados do arquivo publicado.

### P2-05 — Concluir o sistema de design

**Estado:** EM EXECUÇÃO. Primeiro passo aplicado em 09/09/2026 (bloco 16 do CSS).

**Diagnóstico medido nos 115 KB de marcação:** a interface é export do Pen.dev — 285 atributos `data-pencil-name`, 289 `div` para 55 `button`, 31 medidas fixas em pixel. O export traz os valores onde o cursor parou, não uma escala. O que produzia a aparência genérica era, sobretudo, `10px` sendo o tamanho de fonte dominante do site (37 usos de 78) somado a `tracking: 1px` sobre esses 10px (0,1em, em 25 usos).

**Feito:** rótulos de 10px para 12px, grau menor de 9px para 11px, entreletras de 0,1em para 0,04em, respiro dos cartões de 40px para 24px (16px em tela estreita), raios de 24/40/62/70 unificados em 16px. Sem alterar marcação, cor, fonte ou script.

**Falta:**

- nomear as 26 cores hexadecimais como variáveis e eliminar os véus redundantes — quatro sobreposições de preto e branco com opacidades diferentes fazendo a mesma coisa;
- reduzir os 13 valores de espaçamento a uma escala de cinco;
- definir os componentes (botão primário, secundário, segmento, cartão, campo, modal) em vez de repetir listas de classes;
- decidir sobre o uso de maiúsculas nos rótulos, que é escolha visual e não foi tocada.

**Restrições que a continuação precisa respeitar:** a auditoria de acessibilidade fechou com zero violações axe-core, anel de foco autoral, landmarks e gestão de foco nos modais — nada disso pode regredir; `build_public.py` falha se o número de camadas `<script>` deixar de ser nove; o `!important` dos blocos 15 e 16 existe porque o Tailwind vem por CDN e entra na cascata depois desta folha.

**Observação de método:** exportar de novo a partir de um editor de canvas reintroduz o mesmo problema — foi o export que causou o colapso de layout no celular corrigido nesta data. Usar ferramenta de design para decidir, não para gerar o código final.

### P3-11 — Reorganizar o simulador para tela estreita

**Estado:** NÃO INICIADA.  
**Problema:** corrigidos os defeitos da P1-03, o celular passa a mostrar tudo, mas empilhado numa única coluna de cerca de 2.000px. Configuração no alto, questão no meio, cronômetro e anotação bem abaixo. Quem toca em "Iniciar tempo" vê o efeito longe do botão, às vezes fora da tela.  
**Observação:** é decisão de design, não defeito. Exige escolher o que fica fixo, o que vira gaveta e onde mora o cronômetro. Não iniciar antes de o beta indicar se as pessoas usam pelo celular.

### P1-15 — Rotas reais e modelo de acesso

**Estado:** PLANEJADA em 09/09/2026, execução não iniciada. Modelo de acesso e mapa de rotas aprovados pela autora e registrados na seção 2.6 de `ARQUITETURA.md`.

**Problema:** a autenticação é um modal sobre o simulador. Quem está deslogado vê a mesma tela de quem está logado, nenhuma tela tem endereço próprio, e controles aparecem fora de contexto — "criar nova conta" oferecido a quem já está autenticado, por exemplo. A causa não é de tela: é a ausência de modelo de acesso. O aplicativo mostra tudo a todos e oculta partes por CSS.

**Decisões tomadas:** nível pago por funcionalidade e cota, não por exclusividade de conteúdo; visitante treina até 5 questões por dispositivo e depois é convidado a criar conta; roteador em JavaScript com History API, descartados arquivos HTML separados.

**Etapas, em ordem:**

| | Etapa | Entrega | Risco |
|---|---|---|---|
| E1 | Modelo de acesso aprovado | seção 2.6 de `ARQUITETURA.md` | concluída |
| E2 | Mapa de rotas aprovado | seção 2.6 de `ARQUITETURA.md` | concluída |
| E3 | `/sobre`, `/termos`, `/privacidade` | **CONCLUÍDA em 09/09/2026** — três páginas estáticas próprias | baixo |
| E4 | Roteador, sem alterar tela alguma | cada destino ganha URL, título e histórico | médio |
| E5 | Separar `/` do simulador | página pública nova | **alto** |
| E6 | Guardas de rota e limpeza das sobreposições | redirecionamentos; controles fora de contexto deixam de existir | médio |
| E7 | `/conta` | tela própria | baixo |

**E3 concluída em 09/09/2026.** As três páginas foram feitas como arquivos estáticos independentes — `public/sobre.html`, `public/termos.html`, `public/privacidade.html` e a folha `public/assets/paginas.css` —, servidas por regras próprias em `_redirects`, antes do curinga. Decisão deliberada: são páginas de texto, não precisam do `app.js` de 3,4 MB nem do roteador, e **não carregam nenhum recurso externo** — nenhuma CDN, nenhuma fonte do Google, nenhum IP de leitor entregue a terceiro. Verificado em navegador: zero requisição externa, zero erro de script, zero transbordamento horizontal em 1100px e em 390px, temas claro e escuro.

Os três documentos estão em **rascunho, com as lacunas visivelmente assinaladas na própria página**: 10 na política de privacidade, 6 nos termos, 2 na página sobre. Nada foi inventado — o que falta aparece marcado como "a completar". Ver P2-08.

**Próxima etapa: E4**, o roteador.

**E1 a E4 não bloqueiam o beta. A E5 bloqueia:** enquanto a página pública nova não estiver pronta, é melhor não abrir para ninguém. Se o beta for prioridade, parar na E4 e retomar depois.

**Armadilhas conhecidas antes de começar:**

1. a camada `rotas-layer` muda de modo **simulando um clique** em `#modeToggle`, que o `v41.css` oculta desde 09/09/2026 — o roteador precisa substituí-la, não empilhar sobre ela;
2. `v41.css` esconde OAB, TCDF e discursiva por CSS; com rotas passariam a existir dois mecanismos para o mesmo fim;
3. `public/` é a fonte desde 09/09/2026 — `scripts/build_public.py` não pode ser executado durante esta implementação. Ver P2-06.

### P3-09 — Adicionar SEO e compartilhamento

**Estado:** NÃO INICIADA.  
**Inclui:** descrição, Open Graph, título, ícones, canonical, robots e sitemap.

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

### 2026-09-09 — Autenticação comprovada de ponta a ponta

Cadastro, confirmação por e-mail, login, logout, recuperação de senha, definição de nova senha e sincronização testados com conta e e-mail reais no site publicado. Fecha-se P1-05. Reabre-se P1-08 por defeito observado; abrem-se P1-14 e P3-10.

### 2026-09-09 — Controle de versão, publicação contínua e comprovação da RLS

Projeto colocado sob Git com commit inicial e etiqueta `publicado-2026-08-15`, publicado em repositório privado no GitHub e ligado ao Netlify por publicação contínua a partir da branch `main`. O deploy manual por arrastar pasta foi encerrado. RLS auditada no painel e comprovada na prática contra a API pública. Fecham-se P0-01 e P1-02; abre-se P1-13.

### 2026-08-15 — Criação da documentação permanente

Foram criados os oito documentos centrais de contexto, arquitetura, regras, dados, segurança, testes, alterações e pendências.
