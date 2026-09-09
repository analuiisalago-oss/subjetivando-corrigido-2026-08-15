# REGISTRO DE ALTERAÇÕES

## COMO USAR

Registrar toda alteração relevante em ordem cronológica inversa. Não apagar entradas antigas; corrigir mediante nova observação. Usar datas no formato `AAAA-MM-DD`.

Cada entrada deve responder:

- o que mudou;
- por que mudou;
- quais arquivos foram afetados;
- quais testes foram executados;
- o que não foi testado;
- como reverter;
- se houve impacto em dados, segurança ou usuário.

## MODELO

```markdown
## [AAAA-MM-DD] TÍTULO OBJETIVO

**Tipo:** correção / funcionalidade / segurança / design / banco / documentação
**Responsável:**
**Versão ou commit:**
**Ambiente:** desenvolvimento / homologação / produção

### Problema

Descrição objetiva.

### Alteração

Descrição do que foi modificado.

### Arquivos ou serviços afetados

- arquivo/serviço;

### Banco de dados

Nenhuma alteração, ou descrição e referência da migração.

### Segurança e privacidade

Impacto identificado ou “sem impacto identificado”.

### Testes executados

- teste: PASSOU/FALHOU;

### Itens não testados

- item e motivo;

### Reversão

Como voltar ao estado anterior.

### Pendências relacionadas

- referência em PENDENCIAS.md;
```

## HISTÓRICO INICIAL CONHECIDO

## [2026-09-09] CONTROLE DE VERSÃO, PUBLICAÇÃO CONTÍNUA E COMPROVAÇÃO DA RLS

**Tipo:** configuração, segurança e documentação  
**Responsável:** Ana Luísa, com assistência de IA  
**Versão ou commit:** `3152d52`, etiqueta `publicado-2026-08-15`  
**Ambiente:** desenvolvimento local, GitHub, Netlify e Supabase de produção

### Problema

O que estava publicado não estava sob controle de versão. O único repositório Git existente ficava em `_versoes_antigas/backup-2026-08-15/`, tinha um único commit, nenhum remoto e guardava o estado anterior às correções de 15/08/2026. A publicação era manual, por arrastar pasta, o que impedia saber com certeza qual versão estava no ar. A RLS do Supabase permanecia não comprovada.

### Alteração

- criado repositório Git na pasta de trabalho, com commit inicial de 123 arquivos e etiqueta `publicado-2026-08-15`;
- `.gitignore` reforçado por acréscimo, com `node_modules/`, `dist/`, `*.zip`, `.DS_Store`, `Thumbs.db` e `desktop.ini`; nada foi removido;
- `core.autocrlf` e `core.filemode` definidos como `false` no repositório, para o Git no Windows não acusar alteração falsa nos 123 arquivos;
- repositório publicado como **privado** no GitHub;
- Netlify ligado ao repositório, com publicação contínua a partir da branch `main`, comando de build `python3 scripts/build_public.py` e diretório publicado `public`;
- pendências atualizadas: P0-01 e P1-02 concluídas, P0-02 com avanço registrado, P1-13 aberta.

### Arquivos ou serviços afetados

- `.gitignore`;
- `PENDENCIAS.md`;
- `ALTERACOES.md`;
- configuração do projeto no Netlify;
- repositório novo no GitHub.

Nenhum arquivo da aplicação foi alterado.

### Banco de dados

Nenhuma alteração. Apenas consultas de leitura.

### Segurança e privacidade

Confirmado que o isolamento entre usuários funciona. Varredura de segredos repetida antes do commit, sem chave privada. `private/` fora do versionamento e repositório privado.

### Testes executados

- `build_public.py` em cópia isolada reproduz `public/` com SHA-256 idêntico ao publicado: PASSOU;
- `node --check public/assets/app.js`: PASSOU;
- `node scripts/audit_project.mjs`: PASSOU, com o aviso conhecido dos marcadores editoriais;
- contagem do acervo publicado: 750 questões DPE (718 com resposta), 55 OAB, 55 temas TCDF, 6 provas, 37 discursivas: PASSOU;
- hashes dos arquivos servidos em produção conferidos contra os locais: `app.js` e `styles.css` idênticos; `index.html` difere apenas por comentário injetado pelo próprio Netlify: PASSOU;
- RLS: leitura anônima retorna 0 linhas nas seis tabelas e gravação anônima é recusada pela política: PASSOU;
- chamada anônima de `lidar_novo_usuario()` por RPC: recusada com `PGRST202`: PASSOU.

### Itens não testados

- cadastro, confirmação de e-mail, login e recuperação de senha com endereço real;
- sincronização entre dois dispositivos e entre dois usuários autenticados;
- layout em celular real;
- backup e restauração do Supabase.

### Reversão

Apagar a pasta `.git` devolve o projeto ao estado anterior. No Netlify, desligar a publicação contínua devolve o modo manual. O ZIP `subjetivando-corrigido-2026-08-15.zip` permanece como cópia externa.

### Pendências relacionadas

- P0-01 e P1-02 concluídas; P0-02 com avanço; P1-13 aberta; P0-03, P1-05 e P1-03 seguem abertas.


## [2026-08-15] CONSOLIDAÇÃO SEGURA DA VERSÃO DE BETA

**Tipo:** correção, segurança, design, configuração e documentação  
**Responsável:** revisão assistida do projeto Subjetivando  
**Ambiente:** desenvolvimento local

### Problema

A publicação apontava para um `index.html` inexistente; a raiz misturava arquivos públicos e privados; a tela anônima exibia identidade fictícia; a recuperação de senha estava incompleta; falhas de rede podiam manter botões bloqueados; a sincronização incorporava dados locais sem confirmação; e o simulador não possuía refluxo suficiente para telas pequenas.

### Alteração

- criada pasta publicável isolada em `public/`;
- criado gerador `scripts/build_public.py` para separar HTML, CSS e JavaScript;
- corrigidas rotas, inclusive `/atualizar-senha` e regra geral da aplicação;
- implementada definição de nova senha com Supabase `updateUser()`;
- adicionados tratamento de rede e senha mínima de oito caracteres;
- removida identidade fictícia do estado anônimo;
- adicionados consentimento de incorporação e estado de sincronização;
- impedido qualquer envio posterior enquanto a incorporação estiver recusada ou pausada;
- mantido o modal de recuperação aberto para informar links inválidos ou expirados;
- sanitizada a restauração do instantâneo de sessão;
- corrigida interpolação de contexto de anotações;
- adicionadas regras responsivas e redução de movimento;
- adicionados cabeçalhos transitórios de segurança;
- criados arquivos de auditoria e correção orientada do Supabase;
- movidas evidências com dados identificáveis para `private/`.
- marcados os documentos antigos do pipeline como históricos e registrada a divergência editorial sem sobrescrever a interface atual;
- criado `scripts/audit_project.mjs` para validar contagens, IDs, isolamento da publicação e padrões de segredos.

### Arquivos ou serviços afetados

- `minha-banca.NOVO_3.html`;
- `public/`;
- `_redirects`, `_headers`, `robots.txt`, `netlify.toml`;
- `scripts/build_public.py`;
- `supabase/`;
- documentos centrais do projeto;
- organização local das evidências de auditoria.

### Banco de dados

Nenhuma alteração executada. Foram criados SQL de auditoria somente leitura e um SQL de correção da permissão da função, dependente de validação prévia em homologação.

### Segurança e privacidade

Redução do risco de publicação acidental de arquivos privados, execução de HTML armazenado, enumeração de detalhes internos por mensagens e incorporação não consentida de dados locais. A RLS permanece não comprovada e continua sendo bloqueador de lançamento.

### Testes executados

- integridade do backup: PASSOU;
- todos os JSON: PASSOU;
- sintaxe Python: PASSOU;
- sintaxe JavaScript: PASSOU;
- geração de `public/`: PASSOU;
- IDs duplicados e validade das imagens: PASSOU.

### Itens não testados

- autenticação e e-mail reais;
- isolamento RLS;
- layout em navegador real;
- impressão;
- cabeçalhos no Netlify.

### Reversão

Restaurar `subjetivando-backup-2026-08-15.zip`. Nenhum dado do Supabase foi alterado.

### Pendências relacionadas

- P0-01, P0-03, P1-02, P1-03, P1-05, P1-09, P1-10, P1-11, P2-02, P2-03 e P3-05.

## [2026-08-15] CRIAÇÃO DA DOCUMENTAÇÃO PERMANENTE

**Tipo:** documentação  
**Responsável:** projeto Subjetivando  
**Ambiente:** documentação

### Problema

O desenvolvimento ocorreu de forma incremental com auxílio de inteligência artificial, sem conjunto único de documentos capaz de preservar contexto, decisões, regras de segurança e testes.

### Alteração

Criação dos documentos:

- `README.md`;
- `ARQUITETURA.md`;
- `REGRAS-DO-PROJETO.md`;
- `BANCO-DE-DADOS.md`;
- `SEGURANCA.md`;
- `TESTES.md`;
- `ALTERACOES.md`;
- `PENDENCIAS.md`.

### Segurança e privacidade

A documentação estabelece proibições de exposição de segredos, requisitos de RLS, fluxo seguro de pagamentos e critérios de lançamento.

### Testes executados

- revisão de consistência entre os documentos: PASSOU;
- confronto com o HTML auditado e `_redirects`: PASSOU;

### Itens não testados

- esquema real e políticas do Supabase;
- configurações internas do Netlify;
- funcionamento ao vivo da aplicação.

### Reversão

Remover os documentos. Não recomendado, pois não alteram a execução do site.

## [2026-08-15] AUDITORIA INICIAL DO PROTÓTIPO

**Tipo:** auditoria, sem alteração de código

### Constatações principais

- HTML monolítico de aproximadamente 3,5 MB;
- nome do arquivo auditado diferente de `index.html`;
- `_redirects` aponta para `/index.html`;
- responsividade insuficiente na tela principal;
- Tailwind carregado por CDN;
- autenticação Supabase presente;
- recuperação de senha incompleta;
- sincronização baseada em `localStorage` e Supabase;
- conteúdo extenso incorporado ao HTML público;
- domínio e cobrança ainda não implementados;
- políticas RLS não verificáveis pelo frontend.

### Resultado

Criação de plano por fases antes da abertura a usuários pagantes.
