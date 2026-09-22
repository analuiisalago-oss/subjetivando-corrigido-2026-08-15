# ARQUITETURA DO SUBJETIVANDO

## 1. FINALIDADE

Este documento explica como as partes do Subjetivando se relacionam. Ele deve ser atualizado sempre que houver mudança relevante de hospedagem, autenticação, banco de dados, pagamentos, arquivos ou fluxo de dados.

## 2. ARQUITETURA ATUAL

### 2.1. Frontend

Desde 09/09/2026 a pasta `public/` é a fonte do site e vai ao ar como está. Não existe etapa de geração; o antigo `scripts/build_public.py` e o `minha-banca.NOVO_3.html` que ele lia foram removidos em 10/09/2026 (ver P2-14 em `PENDENCIAS.md`).

O simulador é uma página única:

- `public/index.html`: marcação (export do Pen.dev, com atributos `data-pencil-name` usados como seletores);
- `public/assets/styles.css` e `public/assets/v41.css`: estilos autorais;
- `public/assets/tailwind.css`: classes utilitárias, geradas por `npm run css` e carregadas por último de propósito;
- `public/assets/fonts.css` e `public/assets/fonts/`: Inter, Lora e Plus Jakarta Sans servidas pelo próprio site;
- `public/assets/vendor/supabase.js`: biblioteca do Supabase, versão fixada;
- `public/assets/app.js`: lógica, integrações e todo o acervo.

O `app.js` tem cerca de 3,4 MB e 3.100 linhas. 97% do peso está em cinco linhas de dados (`OAB_ITEMS`, `DPE_ORAL_QUESTOES`, `TCDF_PROVAS`, `TCDF_TEMAS`, `TCDF_DISCURSIVAS`), cada uma serializada numa linha só. O código é uma sequência de camadas, cada uma numa função autoexecutada, que se acrescentam por cima da anterior sem alterá-la:

| Ordem | Camada (comentário de abertura) | O que faz |
|---|---|---|
| 1 | Shim de áudio | permite silenciar o alarme do cronômetro |
| 2 | UX v41 | experiência exclusiva de Defensorias: resumo da configuração, estados vazios, teclado |
| 3 | aplicativo original | dados do acervo, sorteio, cronômetro, temas personalizados, tema claro/escuro, impressão |
| 4 | Camada de acessibilidade | região viva, rótulos, foco em modais, Escape |
| 5 | Camada de funcionalidades | alarme prolongado, marca na impressão, anotações por questão |
| 6 | Camada 2 | estado da questão, voltar ao início e continuidade ao recarregar (instantâneo `subj_sessao_v1`) |
| 7 | Tela inicial (dashboard) | cartões, última atividade e metas |
| 8 | Conta — camada visual | modal de conta, hoje só para `/atualizar-senha` |
| 9 | Conta — lógica real | Supabase: sessão, nova senha, sair, cabeçalho |
| 10 | Sincronização de progresso | espelha `localStorage` nas tabelas do Supabase |
| 11 | Áreas com endereço próprio | `/defensoria`, `/oab`, `/tcdf` simulando clique no seletor de modo |

As páginas de conta e institucionais (`inicio.html`, `login.html`, `cadastro.html`, `recuperar-senha.html`, `sobre.html`, `termos.html`, `privacidade.html`) não carregam o `app.js`. Usam `assets/paginas.css` e, as de conta, `assets/conta.js` com a biblioteca do Supabase.

Essa separação melhora cache, diagnóstico e segurança operacional, mas o JavaScript publicável ainda é grande e contém todo o acervo. Não é a arquitetura final recomendada para produto pago.

### 2.2. Hospedagem

O site é publicado no Netlify. `netlify.toml` restringe a publicação à pasta `public/`, evitando que documentos internos, pipeline e capturas sejam servidos. O Netlify resolve as rotas configuradas em `_redirects` e fornece HTTPS para o endereço `netlify.app` e, futuramente, para o domínio próprio.

### 2.3. Backend

O Supabase é utilizado para:

- cadastro e autenticação;
- manutenção da sessão;
- recuperação de senha;
- armazenamento e sincronização do progresso;
- persistência de respostas, anotações, sessões e questões personalizadas.

### 2.4. Persistência local

O navegador armazena dados em `localStorage`, inclusive:

- tema visual;
- preferência de som;
- questões usadas;
- questões personalizadas;
- questões respondidas;
- anotações;
- sessão de estudo;
- dados auxiliares da página inicial e do histórico.

As chaves exatas devem ser inventariadas em `BANCO-DE-DADOS.md` antes de refatorações.

### 2.5. Rotas — estado atual (22/09/2026)

| Rota | Arquivo servido | O que é |
|---|---|---|
| `/` | `inicio.html` | convite à criação de conta (regra `200!`) |
| `/login`, `/cadastro`, `/recuperar-senha` | arquivos próprios | páginas de conta, sem o `app.js` |
| `/sobre`, `/termos`, `/privacidade` | arquivos próprios | páginas institucionais, em rascunho |
| `/dashboard`, `/treino`, `/defensoria`, `/oab`, `/tcdf` | `index.html` | o simulador |
| `/atualizar-senha` | `index.html` | definição de nova senha, ainda em modal |
| qualquer outra | `index.html` | curinga `/* /index.html 200` |

O mapa decidido na seção 2.6 está implantado até a etapa E5 da P1-15. Continuam como limitações: `/dashboard` não exige sessão (decisão de 20/09/2026, etapa E6, não iniciada); as rotas privadas `/hoje`, `/historico`, `/anotacoes` e `/conta` não existem; e a troca de área continua feita por uma camada que **simula um clique** no botão de modo, oculto por CSS.

O servidor local (`npm run dev`) aplica as mesmas regras de `_redirects` e `_headers`.

### 2.6. Modelo de acesso e mapa de rotas — decidido em 09/09/2026

#### Restrição de partida, medida

Todo o acervo é entregue dentro de `public/assets/app.js`. Qualquer pessoa com o endereço baixa o arquivo com as 750 questões e suas respostas. Enquanto isso for verdade, **não existe como cobrar pelo conteúdo**: esconder controle não protege dado servido.

Decisão da autora: o nível pago se define por **funcionalidade e cota**, não por exclusividade de acervo. Proteger o conteúdo de fato exigiria movê-lo para um backend — projeto de outra ordem de grandeza, fora do escopo atual.

#### Os três níveis

| | Visitante | Autenticado (beta gratuito) | Pago |
|---|---|---|---|
| Página pública, sobre, termos, privacidade | sim | sim | sim |
| Treinar: sortear, cronômetro, padrão de resposta | **até 5 questões por dispositivo** | ilimitado | ilimitado |
| Anotações e histórico | locais, perdidos ao limpar o navegador | na conta, em qualquer aparelho | idem |
| Sincronização entre aparelhos | não | sim | sim |
| Gravação, transcrição e correção por IA | não | não | sim, quando existir |

A cota de 5 questões é contada no `localStorage` do dispositivo. **É atrito, não é tranca:** limpar os dados do navegador zera a contagem. Isso é aceitável para um nível gratuito e não deve ser confundido com proteção.

A única barreira real do sistema continua sendo a RLS do Supabase, comprovada em 09/09/2026. Guarda de rota no navegador serve para clareza e conforto, nunca para segurança: toda regra que precise ser inviolável mora no banco ou num backend.

#### Rotas públicas

| URL | Página | Se estiver autenticado |
|---|---|---|
| `/` | apresentação: o que é, para quem, como funciona | permanece acessível |
| `/login` | entrar | redireciona para `/hoje` |
| `/cadastro` | criar conta | redireciona para `/hoje` |
| `/recuperar-senha` | solicitar link | redireciona para `/hoje` |
| `/atualizar-senha` | definir nova senha | apenas com token válido |
| `/sobre` | método, responsável e limites | acessível |
| `/termos` | termos de uso | acessível |
| `/privacidade` | política de privacidade | acessível |

#### Treino — aberto, com estado distinto

| URL | Página |
|---|---|
| `/treino` | configuração: disciplina, fonte, tempo |
| `/treino/questao` | questão sorteada, cronômetro, padrão de resposta |

Visitante acessa as duas até esgotar a cota; depois disso, é convidado a criar conta.

#### Rotas privadas

| URL | Página | Se for visitante |
|---|---|---|
| `/hoje` | painel: retomar, últimas questões, progresso | `/login?destino=/hoje` |
| `/historico` | histórico de questões | `/login?destino=/historico` |
| `/anotacoes` | anotações | `/login?destino=/anotacoes` |
| `/conta` | dados, senha, sair, excluir conta | `/login?destino=/conta` |

#### As cinco regras que eliminam sobreposição

1. **"Entrar" e "Criar conta" só existem em tela pública.** Nunca no painel ou no treino de quem já entrou.
2. **Quem está autenticado nunca vê `/login` nem `/cadastro`.**
3. **Quem não está autenticado nunca vê `/hoje`, `/historico`, `/anotacoes` ou `/conta`** — vai para `/login?destino=…` e, ao entrar, chega onde queria.
4. **`/atualizar-senha` exige token de recuperação**; sem ele, encaminha para `/recuperar-senha` com explicação.
5. **Cada rota tem dono único.** Nenhuma tela em dois endereços; nenhuma ação de conta em tela de treino.

#### Decisão técnica: roteador em JavaScript, com History API

Descartada a alternativa de arquivos HTML separados por rota, por um motivo concreto: os dados vivem num `app.js` de 3,3 MB. Páginas separadas exigiriam duplicá-lo em cada uma ou introduzir um empacotador — e o projeto acabou de tornar `public/` a fonte e desligar o build.

O roteador entrega o que o plano exige: URL própria, título próprio, recarregamento e navegação por voltar e avançar. Não entrega HTML pré-renderizado para buscadores, o que é irrelevante enquanto o `robots.txt` bloqueia o site e as rotas privadas precisam de `noindex` de qualquer modo.

#### Pendências abertas por este mapa

- ~~`/` deixa de abrir o simulador~~ — feito em 09/09/2026 (E5 da P1-15): `/` é o convite e o simulador está em `/dashboard`;
- `/oab` e `/tcdf` precisam de destino definido — redirecionar para `/` ou responder 410 — coerente com o nicho decidido;
- `/defensoria` provavelmente passa a `/treino`;
- a camada de rotas atual precisa ser **substituída**, não estendida: ela muda de modo clicando num `#modeToggle` que o `v41.css` oculta;
- `v41.css` esconde OAB, TCDF e discursiva por CSS. Com rotas, passa a haver dois mecanismos para o mesmo fim; escolher um.

## 3. FLUXOS PRINCIPAIS

### 3.1. Usuário anônimo

1. O Netlify entrega a aplicação.
2. O usuário configura e executa o treino.
3. O navegador salva progresso e preferências localmente.
4. Nenhum dado deve ser enviado à nuvem sem uma finalidade definida e informada.

### 3.2. Usuário autenticado

1. O usuário se cadastra ou entra pelo Supabase Auth.
2. O Supabase cria ou restaura a sessão.
3. A aplicação identifica o usuário autenticado.
4. O progresso local e remoto é mesclado conforme regras documentadas.
5. Alterações futuras são sincronizadas com tabelas protegidas por RLS.

### 3.3. Recuperação de senha desejada

1. O usuário solicita recuperação.
2. O Supabase envia link para endereço autorizado.
3. O usuário chega a `/atualizar-senha`.
4. A aplicação reconhece o evento de recuperação.
5. O usuário informa e confirma a nova senha.
6. O frontend chama o método oficial do Supabase para atualização.
7. A aplicação exibe confirmação e registra eventual erro sem expor dados internos.

Status: **IMPLEMENTADO E TESTADO** com conta e e-mail reais no site publicado em 09/09/2026 (P1-05). A definição de nova senha continua no modal do `app.js`.

## 4. ARQUITETURA-ALVO DO FRONTEND

A migração deve ser gradual, sem reescrita integral imediata:

```text
public/
  index.html
  _redirects
  _headers
  robots.txt
  assets/
    styles.css
    app.js
src/ ou app/
  módulos de interface, autenticação, armazenamento, sincronização e rotas
data/
  conteúdo público ou ferramentas editoriais
supabase/
  migrações e consultas versionadas
```

O Tailwind já é compilado na máquina (`npm run css`, desde 20/09/2026) e o CDN saiu da produção. O próximo passo arquitetural recomendado é tirar o acervo do `app.js` para dados com identificador estável (F2 da P1-16) e depois modularizar o restante, sem alterar simultaneamente o banco.

### 4.1. Treino oral com IA

A correção da fala por IA e o examinador com reperguntas exigem uma função no servidor, porque a chave do provedor de IA não pode ir ao navegador. A proposta, com OpenRouter, RAG e base vetorial no próprio Supabase, está em `IA-PROVA-ORAL.md` (P2-18).

## 5. ARQUITETURA-ALVO PARA PAGAMENTOS

O pagamento não pode ser implementado apenas no navegador.

Fluxo obrigatório:

1. usuário autenticado solicita assinatura;
2. uma função segura cria a sessão de checkout;
3. a chave secreta do meio de pagamento permanece em variável de ambiente do servidor;
4. o usuário paga em página hospedada pelo provedor;
5. o provedor envia webhook assinado;
6. uma função segura valida a assinatura do webhook;
7. a função atualiza a tabela de assinaturas;
8. a aplicação consulta a autorização registrada no backend;
9. cancelamentos, inadimplência e reembolsos também atualizam a autorização.

É proibido liberar acesso premium apenas por:

- parâmetro de URL;
- página de sucesso;
- variável JavaScript;
- campo editável pelo usuário;
- `localStorage`;
- resposta não verificada do navegador.

## 6. CONTEÚDO PÚBLICO E CONTEÚDO PREMIUM

Atualmente, grande parte do conteúdo está embutida no JavaScript público. Ocultar elementos da interface não protege esse conteúdo.

Antes da cobrança, deve ser adotado um dos modelos:

### Modelo A — conteúdo público

O usuário paga por conveniência, sincronização, métricas e recursos avançados. O conteúdo pode ser obtido do arquivo público.

### Modelo B — conteúdo protegido

O conteúdo premium fica fora do HTML e é entregue somente após autorização do backend, mediante RLS e/ou função segura.

Decisão recomendada: **Modelo B**.

Decisão final: **A CONFIRMAR**.

## 7. AMBIENTES

### Durante o protótipo

- Netlify de testes;
- projeto Supabase atual;
- nenhum pagamento real.

### Antes da cobrança

Devem existir ambientes separados:

| Ambiente | Finalidade | Pagamento |
|---|---|---|
| desenvolvimento | alterações locais | nenhum |
| homologação/staging | testes e demonstrações | modo de teste |
| produção | usuários reais | modo real |

Produção e homologação devem, preferencialmente, usar projetos Supabase distintos.

## 8. DEPENDÊNCIAS EXTERNAS CONHECIDAS

- Netlify: hospedagem;
- Supabase: autenticação e banco. Biblioteca `@supabase/supabase-js` 2.116.0, servida de `public/assets/vendor/`;
- Tailwind CSS 3.4.19: só na máquina, para gerar `tailwind.css`;
- fontes Inter, Lora e Plus Jakarta Sans (SIL Open Font License), servidas de `public/assets/fonts/`;
- futuro provedor de IA: OpenRouter, em análise (P2-18);
- futuro provedor de pagamento: **A DEFINIR**;
- futuro serviço de monitoramento: **A DEFINIR**;
- futuro provedor de e-mail transacional: **A DEFINIR**.

Versões de bibliotecas devem ser fixadas e atualizadas de forma controlada. Desde 22/09/2026 nenhum arquivo do site vem de CDN; as versões estão em `package.json` (P2-03).

## 9. DECISÕES QUE EXIGEM REGISTRO

Toda decisão arquitetural relevante deve ser registrada em `ALTERACOES.md`, contendo:

- problema;
- opções consideradas;
- decisão;
- motivo;
- impacto;
- procedimento de reversão.
