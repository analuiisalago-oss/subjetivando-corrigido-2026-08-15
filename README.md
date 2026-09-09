# SUBJETIVANDO

## 1. VISÃO GERAL

Subjetivando é uma plataforma digital de treinamento para provas orais e discursivas de carreiras jurídicas. O produto reúne sorteio de temas e questões, cronômetro, padrões de resposta, pistas, autoavaliação, anotações, histórico e sincronização do progresso do usuário.

Este repositório contém o código da aplicação, os bancos de questões e a documentação técnica e operacional. Antes de alterar qualquer arquivo, leia também:

- `REGRAS-DO-PROJETO.md`;
- `ARQUITETURA.md`;
- `BANCO-DE-DADOS.md`;
- `SEGURANCA.md`;
- `TESTES.md`;
- `PENDENCIAS.md`;
- `ALTERACOES.md`.

## 2. ESTADO ATUAL DO PROJETO

Situação em 15 de agosto de 2026:

- hospedagem de testes: Netlify;
- backend, autenticação e sincronização: Supabase;
- domínio próprio: ainda não adquirido;
- cobrança: ainda não implementada;
- estágio: protótipo avançado, ainda não liberado como produto pago;
- fonte do frontend: a pasta `public/` (`index.html`, `assets/styles.css`, `assets/v41.css`, `assets/app.js`), editada diretamente desde 09/09/2026;
- `minha-banca.NOVO_3.html`: **histórico**, congelado no design anterior. Não editar esperando efeito no site, e não regenerar `public/` a partir dele;
- versão publicável: os quatro arquivos de `public/`, publicados como estão, sem etapa de build;
- diretório publicado pelo Netlify: exclusivamente `public/`;
- rotas existentes: `/`, `/defensoria`, `/oab` e `/tcdf`;
- persistência local: `localStorage`;
- sincronização em nuvem: Supabase para usuários autenticados;
- design principal: tema escuro/claro, paleta botânica e interface em português do Brasil.

## 3. ÁREAS DO PRODUTO

### 3.1. Defensorias

Treinamento de prova oral, com temas e perguntas voltados à preparação para Defensorias Públicas.

### 3.2. OAB

Treinamento de provas discursivas e peças da segunda fase da Ordem dos Advogados do Brasil.

### 3.3. TCDF

Treinamento de questões discursivas e peças técnicas relacionadas ao Tribunal de Contas do Distrito Federal.

## 4. FUNCIONALIDADES CONHECIDAS

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
- cadastro, login, logout e solicitação de recuperação de senha;
- sincronização do progresso para usuários autenticados;
- rotas específicas para as três áreas.

## 5. FUNCIONALIDADES AINDA NÃO CONSIDERADAS CONCLUÍDAS

- teste real do fluxo completo de recuperação de senha no Supabase;
- validação visual da responsividade em navegadores e dispositivos reais;
- auditoria das políticas de segurança do Supabase;
- exclusão de conta e dados;
- possibilidade de rever, em uma área de configurações, a decisão de incorporar ou não dados anônimos;
- nova tentativa de sincronização após falha sem exigir recarregamento manual;
- política de privacidade, termos de uso e política de cancelamento;
- domínio próprio;
- cobrança e controle seguro de assinaturas;
- proteção do conteúdo premium fora do HTML público;
- estrutura de desenvolvimento, homologação e produção separadas;
- monitoramento de erros e plano de resposta a incidentes.
- revisão jurídica e mesclagem controlada das respostas refinadas que permanecem no pipeline histórico (P1-12).

## 6. COMO GERAR E PUBLICAR A VERSÃO DE TESTE

Desde 09/09/2026 não há etapa de geração: edite os arquivos de `public/` diretamente e verifique com

```bash
node --check public/assets/app.js
node scripts/audit_project.mjs
node scripts/teste_consentimento.mjs
```

Depois, execute o roteiro aplicável de `TESTES.md`. **Não execute `scripts/build_public.py`** — ele apagaria o design atual. Ver P2-06 em `PENDENCIAS.md`.

### Se o projeto estiver conectado ao Netlify por repositório

Mantenha `netlify.toml` na raiz. Ele determina que somente `public/` seja publicada.

### Se a publicação for feita arrastando uma pasta no Netlify

Arraste **somente a pasta `public/`**. Nunca arraste a raiz inteira do backup. A raiz contém documentos internos, pipeline e evidências privadas que não devem receber endereço público.

Nunca publique:

- chaves secretas;
- senha do banco;
- chave `service_role` ou `sb_secret` do Supabase;
- chave secreta do Stripe;
- segredo de webhook;
- dados reais usados em testes;
- cópias não autorizadas de materiais de terceiros.

Também não publique `private/`, `pipeline/`, capturas do painel, relatórios de auditoria interna ou bancos auxiliares.

## 7. PRINCÍPIO DE DESENVOLVIMENTO

O projeto deve evoluir por alterações pequenas, reversíveis e testáveis. Uma alteração só será considerada concluída quando:

1. tiver objetivo claramente definido;
2. preservar as funcionalidades não relacionadas;
3. passar pelos testes aplicáveis;
4. não introduzir segredo no frontend;
5. atualizar `ALTERACOES.md`;
6. atualizar `PENDENCIAS.md`, se necessário;
7. puder ser revertida pelo histórico do Git ou pelo backup anterior;
8. ser feita diretamente em `public/`, que é a fonte do site desde 09/09/2026.

## 8. RESPONSÁVEL PELO PRODUTO

- responsável: Ana Luísa Costa de Oliveira Paranaguá e Lago;
- nome comercial do produto: Subjetivando;
- e-mail de suporte: **A DEFINIR**;
- e-mail de privacidade: **A DEFINIR**;
- domínio oficial: **A DEFINIR**.

## 9. AVISO SOBRE ESTA DOCUMENTAÇÃO

Esta documentação descreve o estado conhecido do projeto. Itens marcados como **A CONFIRMAR** ou **A DEFINIR** não podem ser tratados como implementados. Qualquer pessoa ou inteligência artificial que encontre divergência entre a documentação e o código deve interromper a alteração, registrar a divergência e solicitar confirmação antes de decidir qual versão prevalece. Para o estado técnico encontrado e as limitações da revisão, consulte também `AUDITORIA-INTEGRAL-2026-08-15.md`.
