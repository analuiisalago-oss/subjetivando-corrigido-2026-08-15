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

**Estado:** EM EXECUÇÃO. Regras de refluxo implementadas; falta validação visual nas quatro resoluções.  
**Critérios:** 360×800, 768×1024, 1366×768 e 1920×1080 sem perda funcional.

### P1-04 — Remover identidade fictícia

**Estado:** CONCLUÍDA em 15/08/2026.  
**Itens:** “Carlos”, “Carlos Eduardo” e “Assinante Premium” no estado anônimo.

### P1-05 — Concluir recuperação de senha

**Estado:** EM EXECUÇÃO. Tela e lógica implementadas; falta configurar URLs e testar e-mail, expiração e alteração real.  
**Inclui:** rota de nova senha, evento de recuperação, confirmação e testes de expiração.

### P1-06 — Tratar falhas de rede na autenticação

**Estado:** CONCLUÍDA NO FRONTEND em 15/08/2026; falta teste com rede interrompida.  
**Critério:** botões sempre retornam ao estado utilizável e usuário recebe mensagem compreensível.

### P1-07 — Exibir estado de sincronização

**Estado:** CONCLUÍDA NO FRONTEND em 15/08/2026; falta teste em dois dispositivos.

### P1-08 — Pedir confirmação para incorporar dados locais

**Estado:** CONCLUÍDA NO FRONTEND em 15/08/2026; a primeira incorporação exige confirmação.

### P1-09 — Implementar exclusão de conta e dados

**Estado:** NÃO INICIADA.

### P1-10 — Criar documentos públicos

**Estado:** NÃO INICIADA.  
**Inclui:** Termos de Uso, Política de Privacidade, contato e aviso de beta.

### P1-11 — Revisar acessibilidade

**Estado:** EM EXECUÇÃO. Auditoria automatizada anterior aprovada; faltam teste responsivo e leitor de tela real.  
**Inclui:** teclado, leitor de tela, modais, redução de movimento e textos pequenos.

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

### 2026-09-09 — Controle de versão, publicação contínua e comprovação da RLS

Projeto colocado sob Git com commit inicial e etiqueta `publicado-2026-08-15`, publicado em repositório privado no GitHub e ligado ao Netlify por publicação contínua a partir da branch `main`. O deploy manual por arrastar pasta foi encerrado. RLS auditada no painel e comprovada na prática contra a API pública. Fecham-se P0-01 e P1-02; abre-se P1-13.

### 2026-08-15 — Criação da documentação permanente

Foram criados os oito documentos centrais de contexto, arquitetura, regras, dados, segurança, testes, alterações e pendências.
