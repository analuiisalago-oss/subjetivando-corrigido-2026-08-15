# BANCO DE DADOS E ARMAZENAMENTO

## 1. FINALIDADE

Este documento descreve os dados do Subjetivando, sua finalidade, localização e regras de acesso. Deve refletir o banco efetivamente existente. Itens não verificados estão marcados como **A CONFIRMAR**.

## 2. SISTEMAS DE ARMAZENAMENTO

### 2.1. Supabase Auth

Usado para:

- cadastro por e-mail e senha;
- confirmação de e-mail;
- login e logout;
- sessão autenticada;
- solicitação de recuperação de senha;
- metadado de nome de exibição.

### 2.2. Supabase Postgres

Tabelas confirmadas na captura do Table Editor:

- `respostas`;
- `anotacoes`;
- `sessoes`;
- `questoes_usadas`;
- `questoes_customizadas`;
- `perfis`.

As cinco primeiras aparecem também no frontend. A tabela `perfis` é compatível com a função `lidar_novo_usuario()`, mas sua estrutura e finalidade exatas ainda devem ser confirmadas.

### 2.3. Armazenamento do navegador

O frontend usa `localStorage` e `sessionStorage`. Esses dados permanecem no dispositivo e podem ser acessados por scripts executados na mesma origem.

## 3. INVENTÁRIO PRELIMINAR DAS TABELAS

### 3.1. `respostas`

Finalidade: registrar questões marcadas como respondidas.

Colunas inferidas do frontend:

| Coluna | Finalidade |
|---|---|
| `usuario_id` | proprietário do registro |
| `questao_hash` | identificador da questão |
| `questao_texto` | texto ou referência da questão |
| `contexto` | modo, categoria ou contexto |
| `respondida` | estado de resposta |
| `atualizado_em` | data da atualização |

Chave ou restrição esperada: combinação `usuario_id, questao_hash`.

Estrutura real: **A CONFIRMAR NO SUPABASE**.

### 3.2. `anotacoes`

Finalidade: armazenar anotações pessoais vinculadas às questões.

| Coluna | Finalidade |
|---|---|
| `usuario_id` | proprietário |
| `questao_hash` | identificador da questão |
| `questao_texto` | texto ou referência |
| `contexto` | contexto da questão |
| `texto` | anotação do usuário |
| `criado_em` | criação |
| `atualizado_em` | atualização |

Chave ou restrição esperada: combinação `usuario_id, questao_hash`.

Estrutura real: **A CONFIRMAR NO SUPABASE**.

### 3.3. `sessoes`

Finalidade: armazenar o estado instantâneo da sessão de estudo.

| Coluna | Finalidade |
|---|---|
| `usuario_id` | proprietário e provável chave única |
| `instantaneo` | estado serializado da sessão |
| `atualizado_em` | atualização |

Estrutura real: **A CONFIRMAR NO SUPABASE**.

### 3.4. `questoes_usadas`

Finalidade: registrar itens já sorteados por modo e categoria.

| Coluna | Finalidade |
|---|---|
| `usuario_id` | proprietário |
| `modo` | área ou modo |
| `categoria` | disciplina ou categoria |
| `itens` | lista de itens usados |
| `atualizado_em` | atualização |

Chave esperada: `usuario_id, modo, categoria`.

### 3.5. `questoes_customizadas`

Finalidade: armazenar temas inseridos pelo usuário.

| Coluna | Finalidade |
|---|---|
| `usuario_id` | proprietário |
| `modo` | área ou modo |
| `categoria` | disciplina ou categoria |
| `itens` | temas personalizados |
| `atualizado_em` | atualização |

Chave esperada: `usuario_id, modo, categoria`.

## 4. POLÍTICAS RLS OBRIGATÓRIAS

Status atual: **AUDITADO em 09/09/2026** (P0-01 em `PENDENCIAS.md`). `supabase/auditoria_rls.sql`, somente leitura, foi executado no SQL Editor: RLS ativada nas seis tabelas, 20 políticas, todas comparando `auth.uid()` com o dono da linha. Sessão anônima contra a API pública leu 0 linhas e teve a gravação recusada.

Diferença em relação à lista abaixo: `perfis`, `questoes_customizadas`, `questoes_usadas` e `sessoes` não têm política de exclusão. Conferido no código em 22/09/2026 que o aplicativo não depende dela (P1-13): só `respostas` e `anotacoes` usam DELETE, e as outras tabelas são regravadas por `upsert`.

Cada tabela com dados de usuário deve:

- ter RLS ativado;
- permitir leitura somente do próprio usuário;
- permitir inserção somente com `usuario_id = auth.uid()`;
- permitir atualização somente do próprio usuário;
- permitir exclusão somente do próprio usuário;
- negar acesso anônimo, salvo decisão documentada e justificada.

As políticas devem ser testadas no banco e não apenas inferidas do frontend.

## 5. CHAVES DE ARMAZENAMENTO LOCAL CONHECIDAS

| Chave/prefixo | Finalidade |
|---|---|
| `sabatina_theme` | tema claro ou escuro |
| `subj_som` | preferência de aviso sonoro |
| `subj_respondidas_v1` | mapa de questões respondidas |
| `subj_notas_v1` | anotações |
| `subj_sessao_v1` | sessão de estudo |
| `subj_ultima_v1` | última atividade |
| `used_*` | questões usadas por modo e categoria |
| `custom_*` | questões personalizadas por modo e categoria |
| `subj_sync_ok_para` | marca de sincronização na aba, em `sessionStorage` |
| `subj_sync_consent_v1_<usuario>` | consentimento local para incorporar dados anteriores ao login |
| `subj_usuario_v1` | nome de exibição local e rótulo da conta |
| `subj_tela_v1` | última área exibida: tela inicial ou simulador |

Inventário completo: **A CONFIRMAR ANTES DA REFATORAÇÃO**.

## 6. REGRAS DE SINCRONIZAÇÃO DESEJADAS

Operações que o `app.js` executa hoje, conferidas em 22/09/2026 na camada de sincronização:

| Tabela | Gravação | Exclusão |
|---|---|---|
| `respostas` | `upsert` por `usuario_id, questao_hash` | `delete` das linhas que saíram do navegador |
| `anotacoes` | `upsert` por `usuario_id, questao_hash` | `delete` das linhas que saíram do navegador |
| `questoes_usadas` | `upsert` da lista inteira por `usuario_id, modo, categoria` | não usa |
| `questoes_customizadas` | `upsert` da lista inteira por `usuario_id, modo, categoria` | não usa |
| `sessoes` | `upsert` de uma linha por `usuario_id` | não usa |

Regras desejadas:

| Tipo | Regra desejada |
|---|---|
| respondidas | união de registros, respeitando exclusões explícitas |
| anotações | prevalece a versão mais recente |
| sessão | prevalece a atualização mais recente |
| usadas | união, respeitando reinicialização intencional |
| personalizadas | união sem duplicação, respeitando exclusões |

O comportamento atual ainda deve ser comparado a essas regras.

## 7. DADOS DE ASSINATURA — FUTURO

Tabela conceitual `assinaturas`:

| Coluna | Finalidade |
|---|---|
| `usuario_id` | usuário do Supabase |
| `provedor_cliente_id` | identificador no provedor de pagamento |
| `provedor_assinatura_id` | identificador da assinatura |
| `plano` | plano contratado |
| `status` | situação validada pelo webhook |
| `periodo_inicio` | início da vigência |
| `periodo_fim` | fim da vigência |
| `cancelar_ao_final` | cancelamento programado |
| `atualizado_em` | última atualização |

Regras:

- usuário comum pode, no máximo, consultar a própria assinatura;
- usuário comum não pode ativar ou modificar status;
- somente função segura pode escrever dados recebidos do provedor;
- eventos de webhook devem ser idempotentes;
- não armazenar dados completos do cartão.

## 8. RETENÇÃO E EXCLUSÃO

Política definitiva: **A DEFINIR ANTES DO BETA PÚBLICO**.

Deve contemplar:

- exclusão da conta;
- exclusão ou anonimização de respostas e anotações;
- cancelamento da assinatura;
- retenção legal de registros financeiros;
- prazo para backups expirarem;
- tratamento de dados de suporte;
- exportação de dados solicitada pelo usuário.

## 9. BACKUP E RESTAURAÇÃO

Status atual: **A CONFIRMAR**.

Registrar:

- plano Supabase e recursos de backup;
- frequência;
- retenção;
- responsável;
- data do último teste de restauração;
- procedimento para recuperar exclusão acidental.

Um backup só será considerado validado após teste de restauração.

## 10. COMANDOS DE VERIFICAÇÃO

Antes de qualquer migração, gerar e guardar:

- lista de tabelas;
- colunas e tipos;
- chaves primárias;
- chaves estrangeiras;
- índices;
- restrições únicas;
- estado de RLS;
- políticas por operação;
- contagem de linhas, sem copiar conteúdo pessoal.

Não incluir senhas, tokens ou conteúdo de anotações nos relatórios.
