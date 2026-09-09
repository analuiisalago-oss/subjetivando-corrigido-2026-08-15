# UX v41 — Handoff de implementação

## Objetivo

Evoluir a v41 como **protótipo comercial de Defensorias**, corrigindo os problemas de UX/UI já confirmados sem transformar esta etapa em reconstrução de arquitetura, backend ou conteúdo.

## Fonte de trabalho e limites

- Prévia editável: `work/subjetivando-design-preview/public`.
- Servidor local: `work/subjetivando-design-preview/server.cjs`.
- A referência visual e funcional é a prévia v41 examinada em `http://127.0.0.1:8876/?preview=approval-v41`.
- Não alterar o projeto canônico, backend, banco, integrações ou conteúdo jurídico nesta etapa.
- Antes de editar, registrar um checkpoint recuperável da v41.
- Não considerar planos ou código isolado como prova de conclusão: confirmar cada mudança na prévia funcionando.

## Direção de produto

- A experiência prioritária é **Defensorias**, parte que será comercializada.
- O cronômetro antes da leitura não é uma exceção da OAB: deve funcionar em todos os modos e questões, sobretudo nos enunciados longos.
- A configuração deve ficar recolhida depois que o usuário configurar ou sortear a questão, deixando o conteúdo ocupar a tela.
- O protótipo pode aprimorar comportamento local com JavaScript, desde que as mudanças sejam contidas e não desorganizem o código.

## Implementar nesta etapa

### Configuração

- Mostrar primeiro um resumo compacto da seleção; expandir os controles por **Alterar configuração**.
- Recolher automaticamente a configuração após sortear/iniciar uma questão e manter um controle evidente para reabri-la.
- Corrigir os eixos de alinhamento dos rótulos e opções, preservando as bordas arredondadas.
- Refinar seleção, relevo, borda e estados para eliminar o aspecto de botões “chapados” ou de caixas genéricas empilhadas.
- Usar rótulos contextuais: **Sortear tema** ou **Sortear pergunta**, conforme a ação real.

### Enunciado, resposta e ações

- Enunciado e resposta devem compartilhar a mesma coluna editorial e largura confortável de leitura; evitar cartões largos com texto concentrado à esquerda.
- Remover alturas mínimas e espaços vazios artificiais. Os cartões devem crescer conforme o conteúdo.
- Manter linhas de leitura aproximadamente entre 60 e 75 caracteres, com bom `line-height`, espaçamento entre parágrafos e `text-wrap: pretty`.
- Agrupar ações pela sequência de uso, sem espalhá-las pela largura: duração/início do cronômetro, revelar resposta, anotar e sortear outra.
- Manter uma única ação primária por estado e padronizar altura, raio, tipografia, ícones e espaçamento dos botões.
- Centralizar corretamente o texto de **Imprimir / PDF** e dos demais botões.
- Fazer a anotação aparecer sob demanda e comunicar estados vazio, editado, salvo e erro sem depender apenas da cor.

### Cronômetro

- Permitir definir e iniciar o tempo antes da leitura em qualquer modo.
- Antes do início, usar um controle compacto próximo à questão, sem um grande cartão próprio.
- Durante a contagem, manter o timer acessível em faixa compacta ou estado sticky, independente do tamanho do enunciado.
- Reduzir o indicador circular e agrupar Pausar, Reiniciar e Som com espaçamento regular.
- Oferecer feedback textual para início, pausa, retomada e término, além de nome acessível para duração.

### Hierarquia e consistência

- Reduzir a altura/dominância do cartão **Iniciar treino** no dashboard e usar CTA contextual: **Configurar treino** ou **Continuar treino**.
- Corrigir centralização da marca em todos os breakpoints.
- Melhorar a hierarquia do menu lateral, agrupando preferências, recursos, informações e conta.
- Remover áreas vazias sem função nos cartões de atividade/metas ou apresentar estado vazio útil.
- Usar capitalização de frase; manter caixa alta apenas em rótulos curtos de seção.
- Preservar a paleta verde sóbria; no escuro, usar verdes dessaturados e contraste confortável, sem aparência neon.
- Implementar estados `hover`, `focus-visible`, `active`, `disabled`, vazio, carregando e erro quando aplicáveis.
- Preservar alvos interativos de pelo menos 44 × 44 px e navegação por teclado.
- Garantir que o menu de impressão tenha foco previsível, operação por teclado e fechamento com Escape.
- Preservar e conferir `scrollbar-color`, `scrollbar-width`, `::selection` e `text-wrap: pretty` nos dois temas.

### Metadados e confiança

- Remover visualmente o ID estático `#4402`; não inventar IDs persistentes nesta etapa.
- Transformar **Respondida/Não respondida** em controle binário direto, se não houver outras opções reais.
- Exibir estado explícito quando uma questão não tiver resposta, evitando cartão vazio ou resposta incorreta.

## Decisões que precisam de confirmação antes de editar

Reunir estas dúvidas em **uma única pergunta** se ainda não tiverem sido respondidas:

1. No protótipo comercial, OAB e TCDF devem desaparecer do fluxo de Defensorias ou ficar em seletor secundário? Recomendação: retirar desse fluxo. - RETIRAR O FLUXO
2. **Prova discursiva**, hoje indisponível, deve ser ocultada ou mantida desabilitada com explicação? Recomendação: ocultar até funcionar. - OCULTADA

Não interromper o trabalho por escolhas cosméticas que possam seguir as regras deste documento.

## Não implementar agora

- Páginas/rotas definitivas de login, cadastro, anotações ou histórico.
- Autenticação real, proteção de rotas, assinatura, pagamento ou controle de acesso.
- Backend, banco de dados, integrações, sistema editorial ou novos conteúdos jurídicos.
- IDs persistentes ou correção estrutural da persistência.
- Migração para o projeto canônico ou preparação de produção.

Esses itens devem ser relatados como pendências; não devem ser simulados com dados enganosos.

## Defeitos funcionais conhecidos a registrar

- Sessão persistida já exibiu resposta incompatível com a pergunta. É defeito crítico de confiança e integridade de dados, não problema de CSS.
- O ID `#4402` aparece em questões diferentes e não é uma identificação confiável.
- Há questões sem resposta cadastrada; a interface precisa tratar a ausência, e a completude do acervo fica para a etapa de dados.
- A modalidade discursiva não deve parecer pronta enquanto o fluxo termina em “Em breve”.

## Preservar

- Conteúdo jurídico existente, salvo quando houver associação comprovadamente incorreta.
- Tipografia editorial e largura confortável para leitura jurídica.
- Temas claro e escuro e a identidade verde institucional.
- Funções existentes de sortear, revelar/ocultar resposta, anotar, imprimir e controlar tempo.
- Responsividade que já funcione e ausência de dependências desnecessárias.

## Verificação mínima

Testar a prévia em aproximadamente 360, 816–849, 1366 e 1920 px, nos temas claro e escuro:

- configuração aberta e recolhida;
- questão curta e enunciado longo;
- resposta oculta, revelada e ausente;
- anotação fechada, vazia, editada e salva;
- timer antes do início, rodando, pausado, reiniciado e concluído;
- estado respondida/não respondida;
- impressão, teclado, foco visível, overflow e console.

Executar a suíte relevante ao final e repetir apenas testes afetados por falhas posteriores.

## Entrega esperada

Ao concluir, informar de forma concisa:

1. o que foi implementado e quais arquivos mudaram;
2. telas, estados, dimensões e testes verificados;
3. comportamentos que não puderam ser confirmados;
4. pendências futuras em lista exaustiva, cada uma com defeito concreto, evidência, impacto para o usuário e valor comercial, motivo do adiamento, solução recomendada, prioridade e natureza (UX/UI, produto, conteúdo, arquitetura, dados, segurança ou funcional).

A exaustividade vale para o relatório de pendências, não como autorização para expandir o escopo da implementação.
