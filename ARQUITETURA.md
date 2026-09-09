# ARQUITETURA DO SUBJETIVANDO

## 1. FINALIDADE

Este documento explica como as partes do Subjetivando se relacionam. Ele deve ser atualizado sempre que houver mudança relevante de hospedagem, autenticação, banco de dados, pagamentos, arquivos ou fluxo de dados.

## 2. ARQUITETURA ATUAL

### 2.1. Frontend

A aplicação atual é uma página única executada no navegador. A fonte canônica `minha-banca.NOVO_3.html` ainda reúne interface e dados, mas a versão publicável é gerada em três arquivos:

- `public/index.html`: marcação e configuração inicial;
- `public/assets/styles.css`: estilos autorais;
- `public/assets/app.js`: lógica, integrações e acervo atualmente público.

A fonte canônica reúne:

- HTML da interface;
- estilos CSS;
- configuração e carregamento do Tailwind por CDN;
- JavaScript do simulador;
- bancos extensos de questões;
- camada de acessibilidade;
- recursos de anotações e histórico;
- autenticação Supabase;
- sincronização Supabase;
- controle de rotas.

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

### 2.5. Rotas

| Rota | Área |
|---|---|
| `/` | página inicial |
| `/defensoria` | Defensorias |
| `/oab` | OAB 2ª fase |
| `/tcdf` | TCDF |
| `/atualizar-senha` | definição de nova senha após link do Supabase |

Como se trata de uma aplicação de página única, o Netlify deve entregar `index.html` ao acessar ou atualizar essas rotas.

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

Status: **IMPLEMENTADO NO FRONTEND — PENDENTE CONFIGURAÇÃO E TESTE REAL NO SUPABASE**.

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

O Tailwind deve ser compilado no processo de build. O uso de `cdn.tailwindcss.com` deve ser removido da produção depois que a equivalência visual for validada. O próximo passo arquitetural recomendado é modularizar `public/assets/app.js` sem alterar simultaneamente o banco.

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

- Netlify;
- Supabase JavaScript;
- Tailwind CSS;
- Font Awesome;
- Google Fonts;
- futuro provedor de pagamento: **A DEFINIR**;
- futuro serviço de monitoramento: **A DEFINIR**;
- futuro provedor de e-mail transacional: **A DEFINIR**.

Versões de bibliotecas devem ser fixadas e atualizadas de forma controlada.

## 9. DECISÕES QUE EXIGEM REGISTRO

Toda decisão arquitetural relevante deve ser registrada em `ALTERACOES.md`, contendo:

- problema;
- opções consideradas;
- decisão;
- motivo;
- impacto;
- procedimento de reversão.
