# SUPABASE — ROTEIRO SEGURO PARA A PRÓXIMA ETAPA

> **Estado em 22/09/2026.** O roteiro abaixo foi escrito em 15/08/2026. A auditoria da seção 2 já foi executada em 09/09/2026: RLS ativa nas seis tabelas, 20 políticas, isolamento comprovado contra a API pública (P0-01 em `docs/PENDENCIAS.md`). A função `lidar_novo_usuario()` não é chamável pela API pública (`PGRST202`), e a correção da seção 3 virou endurecimento opcional. As URLs da seção 5 estão atualizadas.

## 1. O QUE FOI POSSÍVEL CONFERIR

As evidências recebidas confirmam a existência das tabelas públicas `anotacoes`, `perfis`, `questoes_customizadas`, `questoes_usadas`, `respostas` e `sessoes`. O frontend utiliza cinco delas para sincronização. A estrutura de colunas, as restrições únicas e as políticas de Row Level Security (RLS) não aparecem integralmente nas capturas e, por isso, não foram inventadas nem alteradas.

O Database Linter registrou três alertas:

1. a função `public.lidar_novo_usuario()` pode ser executada pelo papel anônimo;
2. a mesma função pode ser executada por usuários autenticados;
3. a proteção contra senhas vazadas está desativada.

## 2. ORDEM CORRETA

1. Faça backup ou exporte o esquema antes de qualquer alteração.
2. Abra o SQL Editor no projeto de homologação, nunca primeiro no ambiente com usuários reais.
3. Execute `auditoria_rls.sql`. Esse arquivo é somente leitura.
4. Salve o resultado sem copiar conteúdo de anotações ou e-mails.
5. Confirme, tabela por tabela, se a RLS está ativada e quais políticas já existem.
6. Teste com dois usuários diferentes e uma sessão anônima.
7. Somente depois disso crie ou substitua políticas.

Não execute uma política genérica copiada da internet sobre um banco cujo esquema ainda não foi conferido. Uma segunda política permissiva pode anular, na prática, a proteção de uma política correta.

## 3. FUNÇÃO `lidar_novo_usuario`

O arquivo `corrigir_funcao_lidar_novo_usuario.sql` revoga a chamada direta pelos papéis `public`, `anon` e `authenticated`. Antes de executar, confirme que a função é usada apenas por trigger ou internamente pelo fluxo de autenticação. Depois, cadastre um usuário fictício na homologação e confira se a tabela `perfis` foi preenchida como esperado.

## 4. SENHAS VAZADAS E PLANO FREE

A documentação atual do Supabase informa que a verificação de senhas vazadas está disponível a partir do plano Pro. Enquanto o projeto estiver no plano Free:

- mantenha mínimo de oito caracteres ou mais;
- considere exigir combinações mais fortes no painel;
- habilite CAPTCHA para cadastro e recuperação quando o beta for aberto;
- não interprete o alerta como defeito corrigível apenas pelo HTML.

Referências oficiais:

- https://supabase.com/docs/guides/auth/password-security
- https://supabase.com/docs/guides/database/postgres/row-level-security
- https://supabase.com/docs/guides/auth/auth-captcha

## 5. URLS DE AUTENTICAÇÃO

Antes de testar recuperação de senha, inclua no painel do Supabase apenas os endereços exatos usados pelo projeto:

- `https://subjetivando.netlify.app/`;
- `https://subjetivando.netlify.app/atualizar-senha`;
- `https://subjetivando.netlify.app/dashboard` — destino do link de confirmação de cadastro desde 09/09/2026 (E5 da P1-15). Não há registro de que tenha sido cadastrada: conferir no painel;
- futuramente, os equivalentes no domínio próprio.

Evite curingas amplos em produção. URLs de previews temporários devem permanecer restritas ao ambiente de homologação.

