# AUDITORIA INTEGRAL DO SUBJETIVANDO

**Data:** 15 de agosto de 2026  
**Escopo:** backup com frontend, dados locais, integração Supabase, configuração Netlify, documentação, imagens e pipeline Python.  
**Conclusão executiva:** o projeto pode evoluir para um beta controlado, mas ainda não deve receber pagamentos nem ser divulgado a usuários reais antes da auditoria de RLS, dos testes de autenticação no ambiente publicado e da criação dos documentos de privacidade.

## 1. RESULTADO GERAL

O simulador possui um núcleo funcional consistente e um acervo extenso. Os arquivos JSON são válidos, os scripts Python compilam e as camadas JavaScript não apresentam erro de sintaxe. A principal fragilidade não era uma única função defeituosa, mas a ausência de uma fronteira clara entre código publicável, documentos internos, dados de auditoria e arquivos de processamento.

A versão corrigida cria essa fronteira: `public/` é a única pasta destinada ao Netlify; `minha-banca.NOVO_3.html` permanece como fonte canônica; `scripts/build_public.py` separa CSS e JavaScript e regenera a publicação; `private/` concentra evidências que não devem ser expostas.

## 2. ACHADOS CRÍTICOS

### 2.1. RLS NÃO COMPROVADA

O frontend filtra consultas por `usuario_id`, mas filtros no navegador não são autorização. Sem políticas RLS corretas, um usuário poderia tentar consultar ou modificar dados de outro usuário diretamente pela API pública. As capturas não revelam todas as políticas e, por segurança, nenhuma política foi inventada.

**Ação:** executar `supabase/auditoria_rls.sql`, revisar os resultados e testar com usuário A, usuário B e sessão anônima.

### 2.2. FUNÇÃO COM `SECURITY DEFINER` EXPOSTA

O Database Linter informa que `public.lidar_novo_usuario()` pode ser chamada por `anon` e `authenticated`. Uma função `SECURITY DEFINER` executa com privilégios do proprietário e não deve ficar exposta como RPC sem necessidade comprovada.

**Ação:** confirmar seu uso e testar `supabase/corrigir_funcao_lidar_novo_usuario.sql` primeiro em homologação.

### 2.3. ARQUIVOS INTERNOS PODERIAM SER PUBLICADOS

Se a pasta inteira fosse enviada manualmente ao Netlify, capturas com e-mails e identificadores, relatórios internos, bancos auxiliares e scripts poderiam receber URL pública.

**Correção aplicada:** `netlify.toml` publica somente `public/`; as capturas foram movidas para `private/auditoria/`; o README agora orienta a arrastar apenas `public/` em publicação manual.

### 2.4. CONTEÚDO PREMIUM CONTINUA PÚBLICO

O acervo jurídico permanece dentro de `public/assets/app.js`. Ocultar botões não protege esse conteúdo. Cobrar pelo acesso ao banco exige movê-lo para uma camada autenticada e autorizada no backend, ou assumir conscientemente que a cobrança será por funcionalidades e conveniência, não pela exclusividade do conteúdo.

**Estado:** decisão comercial pendente; nenhum pagamento deve ser ativado ainda.

## 3. ACHADOS ALTOS E CORREÇÕES

| Achado | Correção |
|---|---|
| `_redirects` apontava para `index.html`, mas esse arquivo não existia | criado `public/index.html` e adicionada regra geral da aplicação |
| recuperação de senha enviava o usuário apenas à página inicial | criada rota `/atualizar-senha`, formulário de nova senha e chamada a `updateUser()` |
| erros de rede podiam deixar botões bloqueados | operações de login, cadastro, recuperação e alteração de senha agora usam tratamento de erro e restauração em `finally` |
| a tela anônima mostrava “Carlos Eduardo” e “Assinante Premium” | substituídos por identidade neutra e estado de conta local |
| login incorporava automaticamente dados anônimos | adicionada confirmação explícita antes da primeira incorporação à conta |
| não havia indicação confiável da sincronização | adicionado estado “local”, “sincronizando”, “sincronizado” e “falha” |
| instantâneo de sessão restaurava HTML armazenado | adicionada sanitização por lista permitida antes de reinserir marcação |
| contexto de anotação era interpolado em `innerHTML` | passou a usar `textContent` |
| simulador mantinha estrutura fixa em telas estreitas | adicionadas regras de refluxo para 1100, 760 e 480 px e redução de movimento |

## 4. ACHADOS MÉDIOS AINDA ABERTOS

- `public/assets/app.js` possui cerca de 3,4 MB e carrega todo o acervo de uma vez;
- Tailwind, Supabase JavaScript, Font Awesome e Google Fonts dependem de CDNs;
- as versões de Tailwind e Supabase ainda não estão fixadas de forma reprodutível;
- a Content Security Policy foi criada apenas em modo de relatório, porque o Tailwind por CDN e o bloco de configuração inline ainda impedem uma política rigorosa sem testes adicionais;
- não há monitoramento de erros nem procedimento operacional testado de incidente;
- não há separação real entre Supabase de homologação e produção;
- não há exclusão de conta e dados, que deve ser feita por fluxo seguro no servidor;
- não há política definitiva de retenção e backup;
- ainda faltam Política de Privacidade, Termos de Uso, canal de suporte e identificação comercial;
- o domínio próprio e o e-mail transacional ainda não foram configurados.

## 5. DESIGN E ACESSIBILIDADE

A auditoria anterior registrou correções relevantes de semântica, foco, contraste e navegação por teclado. A versão atual preserva essas correções e adiciona refluxo responsivo para o painel, cartões, ações, cronômetro, modais e tabela de rubrica.

As mudanças foram verificadas estaticamente, mas a validação visual em navegadores e dispositivos reais ainda é obrigatória nas resoluções de 360×800, 768×1024, 1366×768 e 1920×1080. Também permanece recomendado testar com NVDA ou VoiceOver.

## 6. PIPELINE E ACERVO

- os sete scripts Python compilam sem erro sintático;
- todos os arquivos JSON do backup foram decodificados com sucesso;
- a fonte canônica contém 750 questões da DPE, mas nenhuma resposta com o par de marcadores `##FALA##` e `##ROTEIRO##`; esses marcadores aparecem em arquivos intermediários do pipeline, associados a uma interface anterior;
- por segurança editorial, os HTMLs do pipeline não foram promovidos sobre a interface atual e o conteúdo reprocessado não foi mesclado automaticamente;
- nenhuma chave secreta foi encontrada nos arquivos examinados; a chave publishable do Supabase é pública por definição;
- os scripts de API exigem `ANTHROPIC_API_KEY` no ambiente e não trazem chave real no código;
- os modelos e preços escritos nos scripts são parâmetros operacionais que podem ficar desatualizados e devem ser conferidos antes de novo lote;
- a validade jurídica substancial das centenas de respostas não foi presumida: os pontos marcados em `pipeline/PONTOS-A-VERIFICAR.md` continuam exigindo revisão humana.

**Ação:** concluir a P1-12 antes de afirmar que o acervo refinado está publicado. A mesclagem deve importar somente os dados aprovados, preservar a interface canônica e manter uma trilha de comparação por identificador.

## 7. TESTES EXECUTADOS

- integridade do ZIP: passou;
- decodificação de todos os JSON: passou;
- compilação sintática de todos os scripts Python: passou;
- sintaxe dos dez blocos JavaScript originais e do `public/assets/app.js`: passou;
- IDs HTML duplicados: nenhum;
- geração determinística da pasta `public/`: passou;
- existência das rotas e dos arquivos de publicação: passou;
- varredura por padrões de segredos: nenhum segredo privado identificado;
- imagens PNG: formatos válidos.

## 8. ITENS NÃO TESTADOS

- envio real de confirmação e recuperação por e-mail;
- alteração real de senha no Supabase;
- isolamento RLS entre dois usuários;
- comportamento de sincronização em dois dispositivos;
- cabeçalhos recebidos no endereço publicado;
- layout visual em navegador real após as novas media queries;
- impressão e PDF após a consolidação;
- restauração de backup do Supabase;
- acessibilidade com leitor de tela real;
- regras comerciais, cobrança e webhooks.

## 9. DECISÃO DE LANÇAMENTO

**Não liberar cobrança.** Para um beta privado, conclua primeiro: auditoria RLS, correção do alerta da função, URLs de autenticação, teste completo de recuperação de senha, verificação responsiva e Política de Privacidade mínima. Para usuários pagantes, cumpra também todo o bloco P2 de `PENDENCIAS.md`.
