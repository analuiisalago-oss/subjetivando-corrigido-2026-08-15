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

Situação em 10 de setembro de 2026:

- hospedagem: Netlify, com publicação contínua a partir da branch `main`. O deploy manual por arrastar pasta foi encerrado em 09/09/2026;
- backend, autenticação e sincronização: Supabase;
- **fonte do frontend: a pasta `public/`, editada diretamente. Não existe etapa de geração, e nenhum outro arquivo deste repositório vira site;**
- diretório publicado pelo Netlify: exclusivamente `public/`;
- persistência local: `localStorage`; sincronização em nuvem: Supabase para quem está autenticado;
- domínio próprio: ainda não adquirido;
- cobrança: ainda não implementada;
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

### 2.2. Para quem vai contribuir

O necessário antes do primeiro PR:

- **o site inteiro sai de `public/`.** `index.html` e `assets/app.js` são a aplicação;
- **`assets/app.js` tem 3,4 MB porque o acervo de questões está dentro dele**, junto de dez camadas de script sobrepostas. Procure o trecho a alterar; não abra o arquivo inteiro no editor sem necessidade;
- **nunca reescreva o `app.js` por inteiro nem o gere a partir de outro arquivo.** Alterações são feitas por âncora conferida, uma função por vez, com conferência de que nada mais mudou. Ver P1-16 em `PENDENCIAS.md`;
- as páginas de conta e institucionais **não carregam o `app.js`**: são arquivos estáticos com `assets/conta.js` (8 KB) e `assets/paginas.css`. Nenhuma delas carrega recurso externo;
- `minha-banca.html`, na raiz, é o **estado publicado em 15/08/2026**, mantido só como referência para conferir regressões. Editar esse arquivo não tem efeito nenhum no site;
- `pipeline/` é a matéria-prima do acervo, não código de aplicação;
- antes de abrir o PR, rode os três comandos da seção 6 e o roteiro aplicável de `TESTES.md`.

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

- validação visual da responsividade em navegadores e dispositivos reais;
- exclusão de conta e dados;
- possibilidade de rever, em uma área de configurações, a decisão de incorporar ou não dados anônimos;
- nova tentativa de sincronização após falha sem exigir recarregamento manual;
- política de privacidade, termos de uso e página sobre: **existem como páginas próprias desde 09/09/2026, mas em rascunho**, com as lacunas assinaladas na própria página — 10 na privacidade, 6 nos termos, 2 na sobre. Falta ainda a política de cancelamento. Ver P2-08;
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

Depois, execute o roteiro aplicável de `TESTES.md`.

`scripts/build_public.py` **foi removido em 10/09/2026**. Ele regenerava `public/` a partir de um HTML congelado e apagaria o design atual sem gerar erro. Continua recuperável pelo histórico do Git, mas não deve voltar. Ver P2-06 em `PENDENCIAS.md`.

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
