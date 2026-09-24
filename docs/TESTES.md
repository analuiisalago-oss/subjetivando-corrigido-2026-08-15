# PLANO DE TESTES DO SUBJETIVANDO

## 1. REGRA DE USO

Nenhuma versão deve ser entregue a usuários sem executar os testes aplicáveis. Registrar data, ambiente, navegador, responsável e resultado.

Estados permitidos:

- `PASSOU`;
- `FALHOU`;
- `NÃO APLICÁVEL`;
- `NÃO TESTADO`.

Não substituir teste por suposição.

### Validação automatizada local

Desde 09/09/2026 a pasta `public/` é a fonte do site e não existe etapa de geração. O antigo `scripts/build_public.py`, que apagava o design atual sem erro, foi removido em 10/09/2026 e não deve voltar (P2-14 em `PENDENCIAS.md`).

Antes de publicar, na pasta do projeto:

```bash
npm run check
```

Ele executa, em sequência e parando no primeiro erro:

```bash
node --check public/assets/app.js
node --check public/assets/conta.js
node scripts/audit_project.mjs
node scripts/teste_consentimento.mjs
```

Os mesmos passos rodam no GitHub Actions (`.github/workflows/verificacao.yml`) em todo push para `main` e em todo PR, junto com a conferência de que `public/assets/tailwind.css` corresponde às classes em uso. Se o Actions acusar o `tailwind.css`, rode `npm run css` e faça commit do resultado.

`teste_consentimento.mjs` é teste de regressão da P1-08: extrai a função de autorização do `app.js` e confirma que uma recusa já registrada não volta a perguntar. Ele sai com código 1 se algum caso falhar.

`audit_project.mjs` confirma as contagens dos seis acervos, IDs únicos no `index.html`, ausência de padrões de segredos privados, a lista fechada de arquivos em `public/` e que cada fonte de `public/assets/fonts/` está citada em `fonts.css`. Arquivo novo em `public/` precisa entrar na lista do script, de propósito: é o que impede um arquivo privado de ir ao ar por engano.

### Conferência no navegador

```bash
npm run dev
```

Abre `http://localhost:8080`, servindo `public/` com as mesmas regras de `_redirects` e `_headers` do Netlify: `/` mostra o convite, `/dashboard` o simulador, `/login` a página de entrar. Para usar outra porta: `PORT=8090 npm run dev`.

Primeira vez na máquina: `npm install`.

## 2. DADOS DE CADA EXECUÇÃO

```text
Versão/commit:
Data:
Ambiente:
URL:
Responsável:
Dispositivo:
Sistema operacional:
Navegador e versão:
```

## 3. TESTE RÁPIDO APÓS QUALQUER ALTERAÇÃO

- [ ] `/` abre o convite e `/dashboard` abre o simulador, sem tela branca;
- [ ] console não apresenta erro novo;
- [ ] cartão "Configurar treino" leva à configuração;
- [ ] é possível sortear uma questão;
- [ ] cronômetro inicia, pausa, retoma e encerra;
- [ ] troca de modo funciona;
- [ ] tema claro/escuro funciona;
- [ ] menu abre e fecha;
- [ ] alteração feita funciona;
- [ ] funcionalidade vizinha não regrediu.

## 4. ROTAS E NETLIFY

Testar em aba anônima e atualizar cada endereço:

- [ ] `/` (convite, `inicio.html`);
- [ ] `/login`, `/cadastro`, `/recuperar-senha`;
- [ ] `/sobre`, `/termos`, `/privacidade`;
- [ ] `/dashboard` e `/treino`;
- [ ] `/defensoria`;
- [ ] `/defensoria/`;
- [ ] `/oab`;
- [ ] `/oab/`;
- [ ] `/tcdf`;
- [ ] `/tcdf/`;
- [ ] rota inexistente apresenta comportamento definido;
- [ ] não ocorre 404 após `Ctrl + F5`;
- [ ] endereço acompanha a troca de área;
- [ ] botão voltar do navegador tem comportamento compreensível.
- [ ] `/atualizar-senha` entrega a aplicação sem erro 404;
- [ ] nenhum arquivo de `private/`, `acervo/`, `docs/` ou outra documentação interna recebe URL pública.

## 5. RESPONSIVIDADE

Executar em 360×800, 768×1024, 1366×768 e 1920×1080:

- [ ] não há rolagem horizontal involuntária;
- [ ] cabeçalho não corta controles essenciais;
- [ ] logo e nome não impedem uso do menu;
- [ ] configuração permanece acessível;
- [ ] enunciado permanece legível;
- [ ] cronômetro permanece utilizável;
- [ ] botões não se sobrepõem;
- [ ] modais cabem ou rolam verticalmente;
- [ ] teclado virtual não bloqueia formulários;
- [ ] textos longos quebram corretamente;
- [ ] zoom de 200% não impede as tarefas principais.

## 6. TREINAMENTO

Repetir para Defensorias (Temas do edital e Questões passadas). OAB e TCDF estão ocultos por CSS desde 09/09/2026 (P2-15); testá-los só se voltarem ao produto:

- [ ] selecionar modo;
- [ ] selecionar categoria;
- [ ] selecionar submodo, quando houver;
- [ ] ajustar tempo;
- [ ] sortear item;
- [ ] sortear outro;
- [ ] iniciar cronômetro;
- [ ] pausar;
- [ ] retomar;
- [ ] reiniciar;
- [ ] finalizar;
- [ ] abrir e fechar pistas;
- [ ] abrir e fechar padrão de resposta;
- [ ] preencher rubrica;
- [ ] nota respeita o máximo;
- [ ] marcar respondida/não respondida;
- [ ] imprimir enunciado;
- [ ] imprimir folha de rascunho;
- [ ] conteúdo indisponível é indicado antes de iniciar o fluxo;
- [ ] recarregar com a resposta aberta devolve a mesma questão com a mesma resposta;
- [ ] "Sortear outra" aparece uma vez só, no topo, e troca o enunciado; em tema, o rótulo é "Sortear outro".

## 7. ANOTAÇÕES E HISTÓRICO

- [ ] criar anotação;
- [ ] editar anotação;
- [ ] excluir anotação;
- [ ] buscar anotação;
- [ ] abrir questão associada;
- [ ] histórico registra questão respondida;
- [ ] busca do histórico funciona;
- [ ] contagens e meta diária são corretas;
- [ ] dados sobrevivem ao recarregamento;
- [ ] exclusão permanece após novo acesso.

## 8. TEMAS PERSONALIZADOS

- [ ] adicionar tema;
- [ ] tema aparece na categoria correta;
- [ ] sortear tema personalizado;
- [ ] excluir tema;
- [ ] impedir inclusão vazia;
- [ ] textos especiais não quebram o HTML;
- [ ] tentativa de inserir HTML ou script é exibida como texto, não executada.

## 9. AUTENTICAÇÃO

### Cadastro

- [ ] e-mail válido;
- [ ] e-mail inválido;
- [ ] senha curta;
- [ ] senhas diferentes;
- [ ] conta já existente;
- [ ] botão indica carregamento;
- [ ] botão é reativado após erro;
- [ ] confirmação de e-mail chega;
- [ ] link retorna ao domínio correto;
- [ ] mensagem não expõe informações desnecessárias.

### Login

- [ ] credenciais válidas;
- [ ] senha incorreta;
- [ ] e-mail inexistente;
- [ ] conta não confirmada;
- [ ] falha de internet;
- [ ] sessão permanece após atualizar;
- [ ] nome correto aparece;
- [ ] dados fictícios não aparecem.

### Logout

- [ ] encerra sessão real;
- [ ] cabeçalho volta ao estado anônimo;
- [ ] dados privados deixam de ser apresentados;
- [ ] botão voltar não restaura conteúdo privado indevidamente.

### Recuperação de senha

- [ ] solicitação com e-mail válido;
- [ ] resposta genérica para e-mail inexistente;
- [ ] link chega;
- [ ] link leva a `/atualizar-senha`;
- [ ] nova senha e confirmação são exigidas;
- [ ] senha é atualizada;
- [ ] senha antiga deixa de funcionar;
- [ ] nova senha funciona;
- [ ] link expirado mostra orientação útil.

## 10. ISOLAMENTO ENTRE USUÁRIOS

Criar usuário A e usuário B:

- [ ] A não lê respostas de B;
- [ ] A não lê anotações de B;
- [ ] A não lê sessão de B;
- [ ] A não lê personalizadas de B;
- [ ] A não altera dados de B;
- [ ] A não exclui dados de B;
- [ ] usuário anônimo não acessa tabelas privadas;
- [ ] consultas diretas respeitam RLS.

Este teste é obrigatório antes do beta público.

## 11. SINCRONIZAÇÃO

Usar dois navegadores ou dispositivos:

- [ ] criar dado no dispositivo A;
- [ ] dado chega ao B;
- [ ] editar no B;
- [ ] versão mais recente chega ao A;
- [ ] excluir no A;
- [ ] dado não reaparece após mesclagem;
- [ ] falha de rede é informada;
- [ ] reconexão sincroniza pendências;
- [ ] dados anônimos só são incorporados após escolha do usuário;
- [ ] logout/login não duplica itens;
- [ ] atualização não provoca recarga infinita.

## 12. ACESSIBILIDADE

- [ ] navegar apenas com `Tab`, `Shift+Tab`, Enter, Espaço e Escape;
- [ ] link “Pular para o conteúdo” funciona;
- [ ] foco é sempre visível;
- [ ] modal recebe foco ao abrir;
- [ ] foco fica contido no modal;
- [ ] foco retorna ao botão de origem;
- [ ] leitor de tela anuncia títulos e estados;
- [ ] botões de ícone têm nome;
- [ ] abas de autenticação funcionam por setas;
- [ ] cronômetro não depende apenas de cor;
- [ ] redução de movimento é respeitada;
- [ ] contraste é suficiente nos dois temas.

## 13. IMPRESSÃO

- [ ] A4 retrato;
- [ ] margens adequadas;
- [ ] enunciado completo;
- [ ] linhas numeradas alinhadas;
- [ ] nenhuma interface do site é impressa indevidamente;
- [ ] quebra de página não corta conteúdo essencial;
- [ ] salvar como PDF funciona.

## 14. SEGURANÇA

- [ ] nenhum segredo no código publicado;
- [ ] RLS ativada;
- [ ] entradas são escapadas;
- [ ] CSP não quebra recursos legítimos;
- [ ] HTTPS ativo;
- [ ] redirects de autenticação restritos;
- [ ] logs sem senha ou token;
- [ ] dependências com versão fixada;
- [ ] headers confirmados pela resposta HTTP;
- [ ] sessão de outro usuário não persiste em computador compartilhado após logout.

## 15. PAGAMENTOS — QUANDO IMPLEMENTADOS

Em modo de teste:

- [ ] checkout só abre para usuário autenticado;
- [ ] pagamento aprovado;
- [ ] pagamento recusado;
- [ ] pagamento atrasado, quando aplicável;
- [ ] webhook válido;
- [ ] webhook com assinatura inválida é rejeitado;
- [ ] webhook repetido não duplica assinatura;
- [ ] página de sucesso isoladamente não concede acesso;
- [ ] assinatura ativa concede acesso;
- [ ] inadimplência aplica a regra comercial definida;
- [ ] cancelamento aplica a regra correta;
- [ ] reembolso aplica a regra correta;
- [ ] portal do cliente abre para o usuário correto;
- [ ] usuário não altera o próprio status pelo Supabase;
- [ ] modo de teste não usa chaves reais.

## 16. REGISTRO DE DEFEITO

```text
Título:
Severidade: crítica / alta / média / baixa
Ambiente:
Versão:
Dispositivo e navegador:
Pré-condições:
Passos para reproduzir:
Resultado esperado:
Resultado obtido:
Captura ou vídeo:
Console/rede, sem dados sensíveis:
Frequência:
Contorno temporário:
```

## 17. CRITÉRIO DE LIBERAÇÃO

### Resultado técnico da auditoria de 15/08/2026

- integridade do ZIP: PASSOU;
- JSON: PASSOU em todos os arquivos encontrados;
- sintaxe Python: PASSOU nos sete scripts do pipeline;
- sintaxe JavaScript: PASSOU nos dez blocos internos e no arquivo público consolidado;
- IDs HTML duplicados: nenhum;
- imagens PNG: formatos válidos;
- autenticação real: NÃO TESTADA;
- RLS entre dois usuários: NÃO TESTADA;
- responsividade visual após as novas regras: NÃO TESTADA EM NAVEGADOR REAL;
- impressão após a consolidação: NÃO TESTADA EM NAVEGADOR REAL.

Os itens não testados continuam bloqueando a abertura do beta público.

### Beta privado

- nenhum defeito crítico;
- rotas, cadastro, login e isolamento aprovados;
- aviso claro de ambiente de testes;
- participantes informados sobre risco de perda de dados.

### Beta público gratuito

- recuperação de senha e exclusão de conta aprovadas;
- responsividade aprovada;
- privacidade publicada;
- sincronização confiável;
- suporte disponível.

### Produção paga

- todos os requisitos anteriores;
- pagamento e webhook aprovados;
- conteúdo premium protegido conforme modelo escolhido;
- revisão de segurança independente;
- termos comerciais publicados;
- obrigações fiscais definidas.
