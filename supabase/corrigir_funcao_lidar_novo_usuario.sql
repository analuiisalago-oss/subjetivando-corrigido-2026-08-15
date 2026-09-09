-- SUBJETIVANDO — CORREÇÃO DO ALERTA DO DATABASE LINTER
-- Pré-condição: confirme que public.lidar_novo_usuario() é usada apenas por
-- trigger ou pelo serviço interno de autenticação. Execute primeiro em
-- homologação e rode novamente o Database Linter.

begin;

revoke execute on function public.lidar_novo_usuario() from public;
revoke execute on function public.lidar_novo_usuario() from anon;
revoke execute on function public.lidar_novo_usuario() from authenticated;

commit;

-- Verificação: anon e authenticated devem retornar false.
select
  has_function_privilege('anon', 'public.lidar_novo_usuario()', 'EXECUTE') as anon_pode_executar,
  has_function_privilege('authenticated', 'public.lidar_novo_usuario()', 'EXECUTE') as autenticado_pode_executar;

-- Reversão, somente se a aplicação comprovadamente depender da chamada RPC:
-- grant execute on function public.lidar_novo_usuario() to authenticated;

