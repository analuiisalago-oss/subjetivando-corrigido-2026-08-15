# REGRAS PERMANENTES DO PROJETO

## 1. AUTORIDADE DESTAS REGRAS

Estas regras são obrigatórias para qualquer pessoa ou inteligência artificial que analise, gere ou altere o Subjetivando. Em caso de conflito, prevalecem:

1. segurança dos usuários e preservação de dados;
2. instrução expressa e atual da responsável pelo projeto;
3. este documento;
4. demais documentos do projeto;
5. conveniências de implementação.

## 2. REGRA CENTRAL

Não remover, substituir, ocultar ou alterar uma funcionalidade existente sem autorização expressa. Correções devem ser localizadas, reversíveis e acompanhadas de testes.

## 3. ANTES DE QUALQUER ALTERAÇÃO

O responsável pela alteração deve:

1. ler todos os documentos do projeto;
2. identificar a versão e o ambiente;
3. verificar o estado do Git;
4. descrever o problema em linguagem simples;
5. apontar os arquivos e funções afetados;
6. listar riscos de regressão;
7. informar como a mudança será testada;
8. confirmar que existe backup ou ponto de restauração.

Se faltar informação que altere materialmente a solução, deve perguntar. Não deve inventar esquema de banco, credenciais, políticas, regras comerciais ou requisitos.

## 4. DURANTE A ALTERAÇÃO

- realizar uma tarefa por vez;
- preservar identidade visual e conteúdo não relacionado;
- evitar reescrever arquivo inteiro para corrigir problema localizado;
- evitar novas dependências sem justificativa;
- não alterar banco e frontend simultaneamente sem plano explícito;
- não realizar migração destrutiva;
- não apagar dados de teste ou produção sem autorização específica;
- não modificar nomes de tabelas, colunas, rotas ou chaves de armazenamento silenciosamente;
- não duplicar lógica já existente;
- não criar nova camada de correção quando for seguro corrigir a origem;
- manter português do Brasil na interface;
- preservar navegação por teclado, foco visível, contraste e semântica;
- preservar funcionamento de impressão;
- preservar os modos Defensorias, OAB e TCDF.

## 5. PROIBIÇÕES DE SEGURANÇA

É proibido:

- inserir chave secreta em HTML ou JavaScript entregue ao navegador;
- expor senha do banco;
- expor chave `service_role`, `sb_secret` ou equivalente;
- expor segredo de webhook;
- confiar em `localStorage` para autorizar plano pago;
- conceder acesso premium apenas pelo retorno visual da página de pagamento;
- desativar RLS para “fazer funcionar”;
- usar política permissiva universal em tabela com dados pessoais;
- registrar senha, token, cartão ou segredo em logs;
- armazenar dados completos de cartão;
- usar dados pessoais reais em testes;
- enviar banco de produção a ferramentas de IA;
- executar SQL destrutivo sem backup, análise e autorização.

## 6. BANCO DE DADOS

Toda proposta SQL deve incluir:

1. finalidade;
2. pré-condições;
3. SQL completo;
4. explicação por bloco;
5. riscos;
6. consulta de verificação;
7. plano de reversão;
8. indicação de ambiente.

Não executar nem sugerir como ação automática:

```sql
DROP
TRUNCATE
DELETE sem WHERE
UPDATE sem WHERE
ALTER destrutivo
```

Políticas RLS devem ser testadas com, no mínimo, dois usuários diferentes.

## 7. CONTEÚDO JURÍDICO

- não alterar conteúdo jurídico apenas para “melhorar estilo” sem identificar a fonte;
- não inventar jurisprudência, legislação, banca, cargo, ano ou gabarito;
- marcar conteúdo incompleto como incompleto;
- manter distinção entre questão oficial, adaptada e autoral;
- registrar fonte e data da última revisão sempre que possível;
- não incorporar material protegido de curso, livro ou plataforma sem autorização;
- submeter alterações materiais a revisão humana.

## 8. DESIGN E ACESSIBILIDADE

Toda mudança visual deve funcionar em:

- 360 × 800;
- 768 × 1024;
- 1366 × 768;
- 1920 × 1080.

Requisitos mínimos:

- nenhuma rolagem horizontal involuntária;
- foco visível;
- controles acessíveis por teclado;
- nomes acessíveis para botões de ícone;
- texto funcional legível;
- modais roláveis em telas pequenas;
- respeito a `prefers-reduced-motion`;
- contraste adequado;
- área de toque suficiente;
- zoom de navegador não bloqueado.

## 9. FINALIZAÇÃO DE UMA ALTERAÇÃO

Antes de declarar a tarefa concluída:

1. executar os testes aplicáveis de `TESTES.md`, no mínimo `npm run check`;
2. registrar testes executados e resultados;
3. revisar erros do console;
4. confirmar que nenhum segredo foi incluído;
5. atualizar `ALTERACOES.md`;
6. atualizar `PENDENCIAS.md`;
7. explicar como reverter;
8. informar claramente qualquer item não testado.

“Deve funcionar” não equivale a “foi testado”.

## 10. PADRÃO DE RESPOSTA PARA INTELIGÊNCIA ARTIFICIAL

Antes de editar, responder:

```text
Problema identificado:
Causa provável:
Arquivos afetados:
Riscos:
Plano de alteração:
Plano de teste:
```

Depois de editar, responder:

```text
Alterações realizadas:
Arquivos modificados:
Testes executados:
Resultados:
Itens não testados:
Riscos remanescentes:
Como reverter:
Próximo passo recomendado:
```

## 11. COMMITS

Cada commit deve representar uma mudança coerente. Exemplos:

```text
fix: corrige rotas do Netlify
fix: conclui fluxo de recuperação de senha
feat: exibe estado de sincronização
docs: documenta políticas RLS
style: adapta simulador para telas pequenas
security: adiciona cabeçalhos de segurança
```

Evitar mensagens genéricas como “ajustes”, “melhorias” ou “versão nova”.

## 12. CRITÉRIO DE PARADA

Interromper e pedir orientação quando:

- houver risco de perda de dados;
- a solução exigir segredo ausente;
- houver divergência entre documentação e código;
- a mudança alterar regra comercial;
- a mudança afetar direitos autorais;
- não for possível testar autenticação ou autorização;
- for necessário ampliar materialmente o escopo original.
