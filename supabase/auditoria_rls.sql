-- SUBJETIVANDO — AUDITORIA SOMENTE LEITURA
-- Ambiente: execute primeiro no projeto de homologação do Supabase.
-- Este arquivo não altera tabelas, políticas, funções ou dados.

-- 1. Tabelas públicas, estado de RLS e proteção reforçada.
select
  n.nspname as esquema,
  c.relname as tabela,
  c.relrowsecurity as rls_ativada,
  c.relforcerowsecurity as rls_forcada
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relkind = 'r'
order by c.relname;

-- 2. Políticas existentes. Revise especialmente USING e WITH CHECK.
select
  schemaname as esquema,
  tablename as tabela,
  policyname as politica,
  permissive,
  roles,
  cmd as operacao,
  qual as usando,
  with_check as com_verificacao
from pg_policies
where schemaname = 'public'
order by tablename, policyname;

-- 3. Permissões concedidas diretamente às funções públicas.
select
  n.nspname as esquema,
  p.proname as funcao,
  pg_get_function_identity_arguments(p.oid) as argumentos,
  p.prosecdef as security_definer,
  coalesce(r.rolname, 'PUBLIC') as beneficiario,
  privilege_type
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
left join aclexplode(coalesce(p.proacl, acldefault('f', p.proowner))) a on true
left join pg_roles r on r.oid = a.grantee
where n.nspname = 'public'
order by p.proname, beneficiario;

-- 4. Restrições e índices das tabelas sincronizadas pelo frontend.
select
  t.relname as tabela,
  i.relname as indice,
  pg_get_indexdef(ix.indexrelid) as definicao
from pg_class t
join pg_namespace n on n.oid = t.relnamespace
join pg_index ix on t.oid = ix.indrelid
join pg_class i on i.oid = ix.indexrelid
where n.nspname = 'public'
  and t.relname in ('respostas', 'anotacoes', 'sessoes', 'questoes_usadas', 'questoes_customizadas', 'perfis')
order by t.relname, i.relname;

