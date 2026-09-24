# SUBJETIVANDO

## 1. VISÃO GERAL

Subjetivando é uma plataforma digital de treinamento para provas orais e discursivas de carreiras jurídicas, com foco na prova oral de Defensoria Pública. O produto reúne sorteio de temas e questões, cronômetro, padrões de resposta, pistas, autoavaliação, anotações, histórico e sincronização do progresso do usuário.

Este repositório contém o código da aplicação, os bancos de questões e a documentação técnica e operacional. Antes de alterar qualquer arquivo, leia `docs/REGRAS-DO-PROJETO.md`. Agentes de IA começam por `AGENTS.md`.

## 2. ESTADO ATUAL DO PROJETO

Situação em 22 de setembro de 2026:

- hospedagem: Netlify, com publicação contínua a partir da branch `main`, em `https://subjetivando.netlify.app`;
- backend, autenticação e sincronização: Supabase;
- **fonte do frontend: a pasta `public/`, editada diretamente. Não existe etapa de geração, e nenhum outro arquivo deste repositório vira site;**
- nenhum arquivo do site vem de CDN: biblioteca do Supabase, fontes e Tailwind são servidos pelo próprio endereço, com versão fixada;
- persistência local: `localStorage`; sincronização em nuvem: Supabase para quem está autenticado;
- domínio próprio: ainda não adquirido;
- cobrança: ainda não implementada;
- treino com IA: proposto em `docs/IA-PROVA-ORAL.md`, ainda não implementado;
- estágio: protótipo avançado, ainda não liberado como produto pago;
- design: tema claro e escuro, paleta botânica, interface em português do Brasil.

### 2.1. Rotas existentes

Definidas em `public/_redirects`, na ordem em que aparecem no arquivo.

| Rota | Arquivo servido | O que é |
|---|---|---|
| `/` | `inicio.html` | convite à criação de conta |
| `/login`, `/cadastro`, `/recuperar-senha` | arquivos próprios | páginas de conta, sem o `app.js` |
| `/sobre`, `/termos`, `/privacidade` | arquivos próprios | páginas institucionais, em rascunho |
| `/dashboard`, `/treino`, `/defensoria`, `/oab`, `/tcdf` | `index.html` | o simulador |
| `/atualizar-senha` | `index.html` | definição de nova senha, ainda em modal |
| qualquer outra | `index.html` | curinga |

A regra de `/` usa o sinal de força (`200!`) porque arquivo existente vence regra de reescrita no Netlify — sem ele, `index.html` continuaria ganhando da raiz. É a única regra do arquivo que precisa disso.

## 3. COMO RODAR NA MÁQUINA

Precisa do Node.js 18 ou mais novo.

```bash
npm install      # primeira vez: instala as versões fixadas em package.json
npm run dev      # abre o site em http://localhost:8080
npm run check    # verificação obrigatória antes de publicar
```

| Comando | O que faz |
|---|---|
| `npm run dev` | serve `public/` em `http://localhost:8080` com as mesmas regras de `_redirects` e `_headers` do Netlify. `/` mostra o convite; `/dashboard`, o simulador |
| `npm run check` | sintaxe do `app.js` e do `conta.js`, auditoria de `public/` e do acervo, e teste de consentimento |
| `npm run css` | gera `public/assets/tailwind.css` de novo. Rodar depois de usar uma classe do Tailwind que ainda não existia |
| `npm run vendor` | copia a biblioteca do Supabase de `node_modules` para `public/assets/vendor/`. Rodar depois de mudar a versão dela em `package.json` |

O GitHub Actions roda a mesma verificação em todo push para `main` e em todo PR (`.github/workflows/verificacao.yml`).

## 4. MAPA DO REPOSITÓRIO

```text
public/            o site, exatamente como vai ao ar
  index.html         o simulador
  inicio.html        a página inicial (convite)
  login.html, cadastro.html, recuperar-senha.html
  sobre.html, termos.html, privacidade.html
  _redirects, _headers, robots.txt
  assets/
    app.js           lógica do simulador e todo o acervo (3,4 MB)
    conta.js         login, cadastro e recuperação das páginas de conta
    styles.css, v41.css, tailwind.css, paginas.css, fonts.css
    fonts/           Inter, Lora e Plus Jakarta Sans (licença OFL)
    vendor/          biblioteca do Supabase, versão fixada
scripts/           servidor local, auditoria, teste de consentimento, cópia da biblioteca
supabase/          SQL de auditoria da RLS e roteiro seguro para o banco
acervo/            matéria-prima das questões e o pipeline de reescrita. Não vai ao ar
docs/              regras, arquitetura, banco, segurança, testes, pendências e alterações
  historico/       auditorias e roteiros antigos, mantidos como registro
AGENTS.md          instruções para agentes de IA (CLAUDE.md aponta para ele)
```

## 5. PARA QUEM VAI CONTRIBUIR

O necessário antes do primeiro PR:

- **o site inteiro sai de `public/`.** `index.html` e `assets/app.js` são a aplicação;
- **`assets/app.js` tem 3,4 MB porque o acervo de questões está dentro dele**, em cinco linhas de dados, junto de onze camadas de script sobrepostas (mapa na seção 2.1 de `docs/ARQUITETURA.md`). Procure o trecho a alterar; não abra o arquivo inteiro no editor sem necessidade;
- **nunca reescreva o `app.js` por inteiro nem o gere a partir de outro arquivo.** Alterações são feitas por âncora conferida, uma função por vez, com conferência de que nada mais mudou. Ver P1-16 em `docs/PENDENCIAS.md`;
- as páginas de conta e institucionais **não carregam o `app.js`**: são arquivos estáticos com `assets/conta.js` e `assets/paginas.css`;
- **não acrescente recurso de terceiros** (CDN, fonte externa, script de análise). Tudo é servido pelo próprio site, e a política de privacidade diz isso;
- arquivo novo em `public/` precisa entrar na lista de `scripts/audit_project.mjs`, de propósito;
- `acervo/` é a matéria-prima do acervo, não código de aplicação. Ver `acervo/LEIA-ME.md`;
- antes de abrir o PR, rode `npm run check` e o roteiro aplicável de `docs/TESTES.md`, e registre a mudança em `docs/ALTERACOES.md`.

## 6. ÁREAS DO PRODUTO

### 6.1. Defensorias

Treinamento de prova oral, com temas do edital e perguntas de banca voltados à preparação para Defensorias Públicas. É a única área visível desde 09/09/2026.

### 6.2. OAB e TCDF

Treinamento de provas discursivas e peças da segunda fase da OAB e do TCDF. Os dados continuam no `app.js`, mas as áreas estão ocultas por CSS desde a decisão de nichar em Defensoria (P2-15 em `docs/PENDENCIAS.md`).

## 7. FUNCIONALIDADES CONHECIDAS

- escolha do modo de treinamento;
- escolha de categoria ou disciplina;
- sorteio de tema ou questão;
- seleção do tempo de resposta;
- cronômetro com aviso sonoro;
- pistas;
- padrão ou modelo de resposta;
- rubrica de autoavaliação em questões compatíveis;
- impressão de enunciado e folha de rascunho;
- inclusão de temas personalizados;
- anotações associadas às questões;
- marcação de questões respondidas;
- histórico de treinamento;
- tema claro e escuro;
- cadastro, login, logout e recuperação de senha;
- sincronização do progresso para usuários autenticados;
- continuidade da sessão de estudo ao recarregar a página.

## 8. FUNCIONALIDADES AINDA NÃO CONSIDERADAS CONCLUÍDAS

- validação visual da responsividade em navegadores e dispositivos reais;
- `/dashboard` exigindo login, decidido em 20/09/2026 (E6 da P1-15);
- exclusão de conta e dados;
- possibilidade de rever, em uma área de configurações, a decisão de incorporar ou não dados anônimos;
- nova tentativa de sincronização após falha sem exigir recarregamento manual;
- política de privacidade, termos de uso e página sobre: **existem como páginas próprias desde 09/09/2026, mas em rascunho**, com as lacunas assinaladas na própria página — 9 na privacidade, 6 nos termos, 2 na sobre. Falta ainda a política de cancelamento. Ver P2-16;
- treino da prova oral com IA: gravação, transcrição e correção (P2-18);
- domínio próprio;
- cobrança e controle seguro de assinaturas;
- proteção do conteúdo premium fora do HTML público;
- estrutura de desenvolvimento, homologação e produção separadas;
- monitoramento de erros e plano de resposta a incidentes;
- revisão jurídica e mesclagem controlada das respostas refinadas que permanecem em `acervo/` (P1-12).

## 9. PUBLICAÇÃO

O Netlify publica a branch `main` a cada push, servindo **somente** `public/`, como define o `netlify.toml`. Não há comando de build.

`scripts/build_public.py` **foi removido em 10/09/2026**. Ele regenerava `public/` a partir de um HTML congelado e apagaria o design atual sem gerar erro. Continua recuperável pelo histórico do Git, mas não deve voltar. Ver P2-14 em `docs/PENDENCIAS.md`.

Se algum dia a publicação for feita arrastando uma pasta no Netlify, arraste **somente a pasta `public/`**. A raiz contém documentos internos e o acervo em elaboração, que não devem receber endereço público.

Nunca publique nem versione:

- chaves secretas;
- senha do banco;
- chave `service_role` ou `sb_secret` do Supabase;
- chave de provedor de IA (OpenRouter, Anthropic e outros);
- chave secreta do Stripe;
- segredo de webhook;
- dados reais usados em testes;
- cópias não autorizadas de materiais de terceiros.

Também não publique `private/`, `acervo/`, capturas do painel, relatórios de auditoria interna ou bancos auxiliares.

## 10. PRINCÍPIO DE DESENVOLVIMENTO

O projeto deve evoluir por alterações pequenas, reversíveis e testáveis. Uma alteração só será considerada concluída quando:

1. tiver objetivo claramente definido;
2. preservar as funcionalidades não relacionadas;
3. passar pelos testes aplicáveis, no mínimo `npm run check`;
4. não introduzir segredo no frontend;
5. atualizar `docs/ALTERACOES.md`;
6. atualizar `docs/PENDENCIAS.md`, se necessário;
7. puder ser revertida pelo histórico do Git;
8. ser feita diretamente em `public/`, que é a fonte do site desde 09/09/2026.

## 11. DOCUMENTAÇÃO

| Documento | Para quê |
|---|---|
| `docs/REGRAS-DO-PROJETO.md` | regras obrigatórias para pessoas e IA. Ler primeiro |
| `docs/ARQUITETURA.md` | como as partes se ligam, rotas, modelo de acesso, mapa do `app.js` |
| `docs/BANCO-DE-DADOS.md` | tabelas, RLS, chaves do navegador e sincronização |
| `docs/SEGURANCA.md` | segredos, cabeçalhos, pagamentos, LGPD |
| `docs/TESTES.md` | roteiros de teste e verificação automatizada |
| `docs/PENDENCIAS.md` | o que falta, por prioridade |
| `docs/ALTERACOES.md` | registro de cada mudança, a mais recente primeiro |
| `docs/IA-PROVA-ORAL.md` | proposta de treino oral com IA (OpenRouter, RAG, custos) |
| `docs/IA-PROMPT-EXAMINADOR.md` | teste da correção por IA sem programar: instruções do examinador prontas para colar |
| `docs/historico/` | auditorias e roteiros antigos |
| `acervo/LEIA-ME.md` | o que é a pasta do acervo e como ela se liga ao site |
| `supabase/LEIA-ME.md` | roteiro seguro para mexer no banco |

## 12. RESPONSÁVEL PELO PRODUTO

- responsável: Ana Luísa Costa de Oliveira Paranaguá e Lago;
- nome comercial do produto: Subjetivando;
- e-mail de suporte: **A DEFINIR**;
- e-mail de privacidade: **A DEFINIR**;
- domínio oficial: **A DEFINIR**.

## 13. AVISO SOBRE ESTA DOCUMENTAÇÃO

Esta documentação descreve o estado conhecido do projeto. Itens marcados como **A CONFIRMAR** ou **A DEFINIR** não podem ser tratados como implementados. Qualquer pessoa ou inteligência artificial que encontre divergência entre a documentação e o código deve interromper a alteração, registrar a divergência e solicitar confirmação antes de decidir qual versão prevalece. Para o estado técnico encontrado em agosto e as limitações daquela revisão, consulte `docs/historico/AUDITORIA-INTEGRAL-2026-08-15.md`.
