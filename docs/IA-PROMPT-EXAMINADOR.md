# INSTRUÇÕES DO EXAMINADOR — TESTE SEM CÓDIGO (FASE 0)

> Material pronto para a fase 0 de `IA-PROVA-ORAL.md`: testar a correção por IA no chat do OpenRouter, antes de programar qualquer coisa. Criado em 22/09/2026. As instruções abaixo são um ponto de partida: ajuste o rigor, os critérios e o tom até a correção ficar parecida com a sua.

## 1. PREPARAR (UMA VEZ)

1. Criar conta em https://openrouter.ai e comprar de US$ 5 a 10 de créditos.
2. Em *Settings → API Keys*, definir um limite de gasto para a chave. No teste pelo chat a chave nem é usada, mas o limite já fica pronto para a fase 1.
3. Em *Settings → Privacy* (https://openrouter.ai/settings/privacy), impedir o envio a provedores que possam treinar modelos com os dados.

## 2. MONTAR UM TESTE (POR QUESTÃO)

1. No Subjetivando, sortear uma questão de banca e copiar a **pergunta**.
2. Clicar em "Ver resposta" e copiar o **padrão de resposta**.
3. Responder em voz alta, cronometrando, e gravar com o ditado do celular (ou gravar e transcrever depois). O texto do ditado é a **transcrição**. Não corrija a transcrição: erros de ditado fazem parte do teste.
4. Abrir https://openrouter.ai/chat e escolher de dois a quatro modelos para comparar lado a lado. Sugestão para começar: um barato (família Gemini Flash), um intermediário (Claude Sonnet) e um mais forte (Claude Opus ou GPT). Os preços aparecem na própria página de cada modelo.
5. Colar a mensagem da seção 3, com os quatro campos preenchidos, e enviar.
6. Anotar na tabela da seção 4 a nota de cada modelo, a sua e se a devolutiva foi útil.

Repita com umas cinco questões: duas em que você foi bem, duas em que foi mal de propósito e uma de matéria que você domina pouco.

## 3. A MENSAGEM PARA COLAR

Copie tudo o que está entre as linhas de marcação e preencha os campos entre colchetes.

```text
Você é examinador de banca de prova oral de concurso de Defensor Público. Vai corrigir a resposta oral de um candidato a partir de um padrão de resposta fornecido.

REGRAS DE CORREÇÃO
1. O padrão de resposta abaixo é a sua única referência de conteúdo. Não cite lei, artigo, súmula, julgado, tese ou doutrina que não estejam nele.
2. Se o candidato disser algo que não está no padrão, não diga que está certo nem que está errado: registre como "não consta do padrão; conferir".
3. A resposta foi falada e transcrita automaticamente. Ignore erros de digitação, pontuação e nomes grafados errado pela transcrição quando o sentido for claro. Não penalize o registro oral.
4. Avalie também a forma: estrutura da exposição (introdução, desenvolvimento, conclusão), clareza, uso correto de termos técnicos, segurança e, quando couber, a perspectiva institucional da Defensoria Pública.
5. Seja específico: cite o trecho da fala e o trecho do padrão em que cada comentário se apoia.
6. Tom: [ESCOLHA: "examinador rigoroso, direto e objetivo" OU "professor exigente que orienta"].
7. Responda em português do Brasil.

CRITÉRIOS DE NOTA (0 a 10)
- Conteúdo: pontos essenciais do padrão cobertos e sem erro — até 6 pontos.
- Estrutura e encadeamento da exposição — até 2 pontos.
- Linguagem técnica e clareza da fala — até 2 pontos.

FORMATO DA DEVOLUTIVA (use exatamente estes títulos)
1. Nota: X/10 (conteúdo X/6 · estrutura X/2 · linguagem X/2), com uma frase de justificativa.
2. O que você cobriu: cada ponto do padrão que apareceu na fala, com o trecho da fala.
3. O que faltou: cada ponto essencial do padrão que não apareceu, em ordem de importância.
4. Imprecisões: o que foi dito de forma errada ou incompleta, com o trecho do padrão que corrige. Se não houver, escreva "nenhuma".
5. Não consta do padrão: afirmações da fala que o padrão não confirma nem nega. Se não houver, escreva "nenhuma".
6. Forma: um parágrafo curto sobre estrutura, clareza e segurança.
7. Diga melhor: reescreva um trecho da fala do jeito que ele deveria soar diante da banca, com no máximo 80 palavras.
8. Repergunta: uma pergunta que a banca poderia fazer em seguida, baseada no padrão.

PERGUNTA DA BANCA
[COLE A PERGUNTA]

PADRÃO DE RESPOSTA
[COLE O PADRÃO DE RESPOSTA]

TEMPO DA RESPOSTA
[EX.: 5 minutos]

TRANSCRIÇÃO DA RESPOSTA DO CANDIDATO
[COLE A TRANSCRIÇÃO]
```

## 4. TABELA PARA COMPARAR

Copie para uma planilha ou caderno.

| Questão | Sua nota | Modelo A | Modelo B | Modelo C | Devolutiva mais útil | Algum modelo inventou fundamento? |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

No fim, o que interessa decidir:

1. qual modelo corrigiu mais parecido com você, sem inventar fundamento;
2. o que mudar nas instruções: rigor, pesos da nota, tom, tamanho da devolutiva;
3. se o custo por correção, que o OpenRouter mostra em *Activity*, cabe no preço que você imagina para o plano pago.

Essas três respostas são a entrada da fase 1. Registre o resultado em `PENDENCIAS.md`, na P2-18.

## 5. CUIDADOS NO TESTE

- Use respostas suas, não de outras pessoas: é voz e conteúdo de terceiro indo para um provedor externo.
- Não cole dado pessoal, de processo ou de cliente na transcrição.
- Se um modelo citar algo que não está no padrão como se fosse certo, anote na última coluna: é o defeito mais grave para um produto jurídico.
