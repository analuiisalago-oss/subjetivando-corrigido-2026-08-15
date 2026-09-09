# POLÍTICA DE SEGURANÇA DO SUBJETIVANDO

## 1. OBJETIVO

Proteger contas, progresso, anotações, conteúdo, pagamentos e infraestrutura contra acesso não autorizado, perda, alteração, exposição ou uso indevido.

## 2. DADOS TRATADOS OU PREVISTOS

- nome de exibição;
- endereço de e-mail;
- identificador de usuário;
- autenticação e sessão;
- progresso de estudo;
- anotações pessoais;
- temas personalizados;
- histórico de questões;
- dados de assinatura e cobrança;
- registros técnicos mínimos para segurança e suporte.

Não solicitar que o usuário registre dados pessoais sensíveis em anotações. Não coletar dados desnecessários.

## 3. CLASSIFICAÇÃO DE SEGREDOS

### Podem aparecer no frontend

- URL pública do Supabase;
- chave pública/publishable do Supabase;
- identificadores públicos de produtos ou preços, quando adequado.

### Nunca podem aparecer no frontend ou repositório

- chave secreta do Supabase;
- `service_role`;
- `sb_secret`;
- senha do banco;
- chave secreta do Stripe ou outro provedor;
- segredo de webhook;
- token pessoal do GitHub;
- credenciais de e-mail;
- códigos de recuperação de 2FA.

Segredos devem ficar em variáveis de ambiente do ambiente seguro correspondente.

## 4. CONTAS ADMINISTRATIVAS

Ativar autenticação em dois fatores em:

- Netlify;
- Supabase;
- GitHub;
- Registro.br;
- provedor de pagamento;
- e-mail administrativo.

Usar senhas únicas e gerenciador de senhas. Guardar códigos de recuperação em local seguro separado.

## 5. AUTENTICAÇÃO DOS USUÁRIOS

Requisitos:

- confirmação de e-mail;
- senha mínima de oito caracteres ou política mais forte;
- proteção contra tentativas abusivas;
- CAPTCHA quando adequado;
- mensagens que não revelem existência de conta;
- recuperação completa de senha;
- encerramento real da sessão no logout;
- reautenticação para ações sensíveis;
- possibilidade futura de autenticação multifator, se proporcional ao risco.

## 6. AUTORIZAÇÃO E RLS

Autenticação responde “quem é o usuário”. RLS responde “quais dados ele pode acessar”.

Todas as tabelas com dados pessoais devem ter políticas que comparem o usuário autenticado ao proprietário da linha. Nunca confiar apenas em filtros do JavaScript.

Auditoria atual das políticas: **PENDENTE**.

## 7. PAGAMENTOS

- utilizar checkout hospedado por provedor reconhecido;
- não coletar ou armazenar número completo do cartão;
- criar checkout em função segura;
- validar assinatura do webhook;
- tornar processamento idempotente;
- não liberar acesso por página de sucesso;
- armazenar somente identificadores e estados necessários;
- separar chaves de teste e produção;
- oferecer portal seguro para cancelamento e gestão da assinatura;
- registrar alterações de estado sem registrar dados financeiros sensíveis.

## 8. SEGURANÇA DO FRONTEND

Antes da produção:

- retirar Tailwind CDN;
- fixar versões de dependências;
- reduzir scripts inline;
- configurar Content Security Policy;
- adicionar `X-Content-Type-Options`;
- adicionar `Referrer-Policy`;
- adicionar `Permissions-Policy`;
- impedir enquadramento não autorizado;
- garantir HTTPS;
- remover logs contendo dados pessoais;
- tratar entradas do usuário como não confiáveis;
- evitar restauração de HTML arbitrário por `innerHTML`;
- validar e escapar conteúdo personalizado.

Estado em 15 de agosto de 2026:

- nenhuma chave secreta foi identificada na varredura do backup;
- a URL e a chave publishable do Supabase permanecem no frontend, como esperado para esse tipo de integração;
- a restauração do instantâneo de estudo passou a sanitizar a marcação armazenada;
- conteúdos de anotação e contexto são inseridos como texto;
- a publicação foi isolada em `public/`;
- capturas com dados identificáveis foram movidas para `private/`;
- a recuperação de senha foi implementada, mas depende de teste real e URLs autorizadas no Supabase.

## 9. ARQUIVO `_headers`

O arquivo deve ser criado e testado progressivamente. Uma política de segurança excessivamente rígida pode quebrar fontes, Supabase ou scripts atuais. Não copiar configuração pronta sem listar todos os domínios necessários.

Status: **IMPLEMENTAÇÃO TRANSITÓRIA**. `_headers` contém cabeçalhos de proteção e uma Content Security Policy em modo de relatório. Ela ainda não é aplicada de forma bloqueante porque Tailwind e parte da configuração continuam dependentes de CDN e código inline. Torná-la obrigatória sem teste poderia retirar estilos ou impedir autenticação.

Antes de converter a política de relatório em política efetiva:

1. compilar o Tailwind;
2. fixar ou hospedar as dependências;
3. remover o último script inline ou autorizar seu hash;
4. verificar console e cabeçalhos no endereço publicado;
5. testar login, recuperação, impressão e ambos os temas.

## 10. AMBIENTES

- não usar dados de produção em homologação;
- não usar chaves reais de pagamento em testes;
- não permitir que preview do Netlify se torne endereço oficial;
- restringir redirects de autenticação em produção a URLs exatas;
- manter projetos separados quando houver usuários pagantes.

## 11. LOGS E MONITORAMENTO

Registrar somente o necessário para diagnosticar:

- horário;
- operação;
- código de erro;
- identificador técnico não sensível;
- ambiente e versão.

Nunca registrar:

- senha;
- token de sessão;
- chave secreta;
- conteúdo integral de anotação;
- dados completos de cartão;
- URL com credencial.

## 12. BACKUPS

- confirmar recursos de backup do plano utilizado;
- definir frequência e retenção;
- proteger acesso ao backup;
- testar restauração;
- documentar restauração;
- considerar que exclusão do usuário deve alcançar cópias ativas e expirar em backups conforme política informada.

## 13. DEPENDÊNCIAS

Antes de incluir biblioteca:

- justificar necessidade;
- preferir fonte oficial;
- fixar versão;
- verificar manutenção;
- revisar permissões;
- registrar a inclusão;
- planejar atualização.

## 14. RESPOSTA A INCIDENTES

Em suspeita de incidente:

1. não apagar evidências;
2. identificar ambiente e versão;
3. limitar o acesso ou suspender o recurso afetado;
4. revogar e rotacionar segredos comprometidos;
5. avaliar dados e usuários afetados;
6. corrigir a causa;
7. testar a correção;
8. avaliar comunicações legais e aos titulares;
9. registrar cronologia e decisões;
10. revisar controles para evitar repetição.

Contato responsável: **A DEFINIR**.

## 15. LGPD E PRIVACIDADE

Antes do beta público:

- criar Política de Privacidade;
- criar canal para o titular;
- documentar finalidades e bases legais;
- mapear operadores, como Netlify e Supabase;
- definir retenção;
- implementar acesso, correção e exclusão;
- informar sincronização local/nuvem;
- manter registro simplificado das operações;
- definir procedimento de incidente.

## 16. COMUNICAÇÃO DE VULNERABILIDADE

Criar endereço de contato, por exemplo:

```text
seguranca@DOMINIO
```

Não publicar detalhes exploráveis antes da correção. Não prometer recompensa sem programa formal.

## 17. CHECKLIST ANTES DO LANÇAMENTO PAGO

- [ ] 2FA nas contas administrativas;
- [ ] RLS auditada e testada com dois usuários;
- [ ] recuperação de senha completa;
- [ ] exclusão de conta implementada;
- [ ] política de privacidade publicada;
- [ ] segredos somente no servidor;
- [ ] pagamentos confirmados por webhook;
- [ ] conteúdo premium fora do HTML público;
- [ ] backups confirmados e restauração testada;
- [ ] ambiente de homologação separado;
- [ ] dependências fixadas;
- [ ] cabeçalhos de segurança testados;
- [ ] logs sem dados sensíveis;
- [ ] plano de incidente documentado;
- [ ] revisão técnica independente concluída.

## 18. ALERTAS ATUAIS DO SUPABASE

O relatório de 15 de agosto de 2026 apontou que `public.lidar_novo_usuario()` é uma função `SECURITY DEFINER` executável por `anon` e `authenticated`. A correção proposta está em `supabase/corrigir_funcao_lidar_novo_usuario.sql` e não deve ser aplicada antes de confirmar a finalidade da função e testar o cadastro em homologação.

O alerta de proteção contra senhas vazadas está relacionado ao plano utilizado. A documentação atual do Supabase informa que esse recurso está disponível a partir do plano Pro. No plano Free, devem ser reforçados o comprimento mínimo, a política de caracteres, CAPTCHA e limites contra abuso.
