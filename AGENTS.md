# AGENTS.md

Instruções para agentes de IA (Codex, Claude Code, Cursor e outros) que trabalham neste repositório. Valem junto com `docs/REGRAS-DO-PROJETO.md`, que é obrigatório e prevalece em caso de conflito.

## Projeto

Subjetivando: simulador de banca para a prova oral de Defensoria Pública. Site estático no Netlify, conta e sincronização no Supabase. Interface, documentação, comentários e mensagens de commit em **português do Brasil**.

A responsável é Ana Luísa. Decisões de produto, texto jurídico e regra comercial são dela: registre a dúvida em `docs/PENDENCIAS.md` e pergunte, não decida.

## Antes de mexer

1. Ler `docs/REGRAS-DO-PROJETO.md` inteiro.
2. Ler o que for pertinente em `docs/`: `ARQUITETURA.md`, `BANCO-DE-DADOS.md`, `SEGURANCA.md`, `TESTES.md` e `PENDENCIAS.md`.
3. Conferir `git status` e em que branch está.
4. Se a documentação divergir do código, parar, registrar a divergência e pedir confirmação (regra 12).

## Onde fica o site

- **`public/` é a fonte e vai ao ar como está.** Não há build. Nada fora de `public/` é publicado.
- `public/index.html` + `public/assets/app.js` são o simulador (`/dashboard`).
- As páginas de conta (`login`, `cadastro`, `recuperar-senha`) usam `assets/conta.js`. As institucionais e a inicial usam só `assets/paginas.css`. Nenhuma delas carrega o `app.js`.
- `acervo/` é matéria-prima editorial e não muda o site. `docs/historico/` é registro antigo.

## Comandos

```bash
npm install      # primeira vez
npm run dev      # http://localhost:8080, aplica _redirects e _headers como o Netlify
npm run check    # obrigatório antes de commit: node --check, auditoria, teste de consentimento
npm run css      # regenerar public/assets/tailwind.css após usar classe Tailwind nova
npm run vendor   # copiar a biblioteca do Supabase após mudar a versão em package.json
```

O GitHub Actions roda `npm run check` e confere o `tailwind.css` em todo PR.

## Como editar o `app.js`

O arquivo tem cerca de 3,4 MB. Cinco linhas (`OAB_ITEMS`, `DPE_ORAL_QUESTOES`, `TCDF_PROVAS`, `TCDF_TEMAS`, `TCDF_DISCURSIVAS`) têm de 6 mil a 2,9 milhões de caracteres cada.

- **Nunca reescrever, reformatar ou regenerar o arquivo inteiro.** Nunca rodar formatador nele.
- Editar por âncora: localizar um trecho exato, conferir que ele aparece **uma vez só**, substituir, e conferir pelo `git diff` que nada mais mudou.
- Não abrir as linhas de dados no editor nem imprimi-las no terminal; use `grep -n` com `cut -c1-200`.
- O código são onze camadas autoexecutadas, cada uma aberta por um comentário em bloco. Mapa na seção 2.1 de `docs/ARQUITETURA.md`. Camada nova por cima de outra é o padrão histórico, mas a regra 4 manda corrigir na origem quando for seguro.
- Chaves de `localStorage` (`subj_*`, `used_*`, `custom_*`), nomes de tabela e rotas não mudam em silêncio: a sincronização intercepta essas chaves pelo nome.
- O instantâneo de sessão (`subj_sessao_v1`, `v: 3`) é HTML salvo do DOM. Mudança na marcação da questão ou do painel de resposta pode quebrar a restauração: teste recarregando a página no meio de um treino.

## Estilo e CSS

- A ordem das folhas no `index.html` é intencional: `fonts.css`, `styles.css`, `v41.css`, `tailwind.css` por último. Trocar a ordem muda quem vence e exige comparação elemento a elemento (P2-01).
- Os atributos `data-pencil-name` são usados como seletores no CSS e no JS. Não removê-los.
- `v41.css` oculta OAB, TCDF e discursiva. Os dados continuam no `app.js` (P2-15).

## Segurança

- Nada de chave secreta em `public/`: `service_role`, `sb_secret_`, chave de provedor de IA (OpenRouter, Anthropic), Stripe, webhook. A chave `sb_publishable_` e a URL do Supabase no front são esperadas.
- A barreira real é a RLS do Supabase. Guarda de rota no navegador é conforto, não segurança.
- **Nenhum recurso de terceiros no site**: sem CDN, fonte externa, analytics ou script externo. A política de privacidade afirma isso. Dependência nova é baixada para `public/assets/` com versão fixada e entra na lista de `scripts/audit_project.mjs`.
- Arquivo novo em `public/` só passa na auditoria se for acrescentado à lista do script. Isso é proposital.
- SQL: seguir a seção 6 das regras. Nunca `DROP`, `TRUNCATE`, `DELETE` ou `UPDATE` sem `WHERE`.

## Testar

- `npm run check` sempre.
- Mudança visível: conferir no navegador com `npm run dev`, nas larguras da seção 8 das regras, nos temas claro e escuro, e recarregando a página no meio de um treino.
- Autenticação e sincronização só se testam de verdade no site publicado, com conta real. **Se não for possível testar autenticação ou autorização, parar e pedir orientação** (regra 12). Não criar contas nem gravar dados de teste no Supabase de produção.
- "Deve funcionar" não é "foi testado": registre o que não foi testado.

## Ao terminar

1. Registrar em `docs/ALTERACOES.md`, no modelo do topo do arquivo, com testes executados, itens não testados e como reverter.
2. Atualizar `docs/PENDENCIAS.md`. IDs são únicos: antes de criar um, conferir o maior número da prioridade.
3. Commit coerente, mensagem no formato `tipo: descrição` em português (`fix:`, `feat:`, `docs:`, `style:`, `security:`, `build:`, `ci:`).

## O que não fazer

- Não recriar `scripts/build_public.py` nem qualquer comando que escreva em `public/` a partir de outro arquivo.
- Não editar `acervo/pipeline/minha-banca.html` esperando efeito no site.
- Não alterar conteúdo jurídico por estilo, nem inventar jurisprudência, lei, banca, ano ou gabarito (regra 7).
- Não remover funcionalidade existente sem autorização expressa (regra 2).
