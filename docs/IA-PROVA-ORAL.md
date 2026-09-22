# TREINO DA PROVA ORAL COM IA — PROPOSTA

> **Para a Ana.** Escrito em 22/09/2026 para responder às perguntas dos áudios: onde o OpenRouter entra, o que é RAG e como se monta a "base vetorial". Nada disso existe no site ainda. É uma proposta para conversar e decidir, registrada como P2-18 em `PENDENCIAS.md`. Preços e recursos foram conferidos nas páginas oficiais nessa data (fontes no fim).

## 1. RESUMO EM CINCO PONTOS

1. **A IA não precisa "saber Direito" de cabeça.** Ela recebe a pergunta, o padrão de resposta que você já tem e a fala da pessoa, e compara. Dar o material certo à IA antes de ela responder é o que se chama de **RAG**.
2. **OpenRouter é uma conta só que dá acesso a centenas de modelos de IA** (Claude, GPT, Gemini e outros), com uma chave só. É por onde o site chamaria a IA para transcrever a fala e para corrigir.
3. **A primeira versão não precisa de base vetorial.** A questão sorteada já tem o padrão de resposta dela; basta buscá-lo pelo número da questão.
4. **A base vetorial entra depois**, para o examinador fazer reperguntas e para os 199 temas do edital, que não têm padrão de resposta. Ela cabe no Supabase que o site já usa, sem contratar outro serviço.
5. **Custo estimado: de 2 a 6 centavos de dólar por resposta de 5 minutos corrigida**, conforme o modelo escolhido. Cem correções custam de 2 a 6 dólares.

## 2. COMO SERIA O TREINO, DO PONTO DE VISTA DE QUEM ESTUDA

1. Sorteia uma questão, como hoje.
2. Aperta "Responder em voz alta". O cronômetro que já existe marca o tempo.
3. Fala a resposta, como diante da banca.
4. Ao terminar, espera alguns segundos e recebe:
   - o texto do que falou;
   - os pontos do padrão de resposta que cobriu;
   - os pontos que faltaram;
   - imprecisões, com o trecho do padrão que as corrige;
   - uma nota por critério;
   - uma sugestão de como dizer melhor um trecho.
5. Numa segunda fase, o examinador faz uma ou duas reperguntas, como na prova oral de verdade, e a pessoa responde de novo em voz alta.

## 3. AS QUATRO PEÇAS, EM PORTUGUÊS

### 3.1. Gravar a voz (no navegador)

O próprio navegador grava pelo microfone. Não precisa instalar nada. Hoje o site **bloqueia o microfone de propósito** (o `_headers` tem `microphone=()`) e a política de privacidade diz que não grava áudio. As duas coisas mudam juntas quando a gravação existir.

### 3.2. Transformar a fala em texto (transcrição)

O áudio vai para um modelo de transcrição, que devolve o texto. O OpenRouter tem um endereço próprio para isso, com modelos como o Whisper, e aceita o idioma `pt`. Outra opção são modelos que recebem o áudio direto e já corrigem na mesma chamada, como os da família Gemini.

Cuidado conhecido: os provedores encerram uma chamada que passa de cerca de 60 segundos de processamento. Uma fala de 5 minutos costuma caber, mas pode ser preciso cortar gravações longas em pedaços.

### 3.3. Corrigir (o "examinador")

Um modelo de linguagem recebe, numa mensagem só:

- as instruções do examinador: quem ele é, com que rigor corrige, em que formato devolve a avaliação;
- a pergunta;
- o padrão de resposta e, quando existir, o roteiro (`##ROTEIRO##`, ver P1-12);
- os critérios de nota;
- a transcrição da fala.

Ele devolve a avaliação num formato fixo, que o site mostra na tela. As instruções do examinador são o coração da qualidade e merecem ser escritas e testadas por você, que conhece a banca.

### 3.4. RAG e base vetorial

**RAG** (do inglês *retrieval-augmented generation*) quer dizer: **buscar o material certo antes de pedir a resposta à IA**. Pense numa prova com consulta: o examinador corrige com o espelho na mão, não de memória.

Sem isso, a IA corrige com o que "lembra" e pode inventar julgado, súmula ou artigo, o que a regra 7 de `REGRAS-DO-PROJETO.md` proíbe. Com o padrão de resposta na mão, e com a instrução de não citar nada fora dele, esse risco cai muito. Não chega a zero, e por isso a tela precisa avisar que a avaliação é automática.

A busca pode ser de dois tipos:

| | Busca direta | Busca por significado (base vetorial) |
|---|---|---|
| Quando | a questão sorteada tem padrão de resposta | não se sabe de antemão qual material é o certo |
| Como | pelo número da questão | comparando o sentido do texto |
| Exemplo | questão 312 → padrão da questão 312 | tema "apreensão de adolescente em flagrante" → as respostas do acervo que tratam disso, mesmo com outras palavras |
| Fase | 1 | 2 |

**Como a base vetorial funciona.** Cada trecho do acervo é transformado numa "impressão digital de significado": uma lista de números que um modelo de *embeddings* calcula. Textos com sentido parecido recebem impressões parecidas. Para achar o material de um tema, calcula-se a impressão do tema e procuram-se as mais próximas. É assim que "prisão de menor" encontra um texto que só fala em "apreensão de adolescente".

**Onde guardar.** No próprio Supabase: a extensão `vector` (pgvector) está disponível no plano gratuito e se liga em *Database → Extensions*. Não é preciso contratar outro serviço.

**Quanto custa montar.** As 750 perguntas e 718 respostas somam cerca de 2,8 milhões de caracteres, na ordem de 750 mil *tokens*. Com um modelo de embeddings barato do OpenRouter (US$ 0,02 por milhão de tokens), o acervo inteiro sai por cerca de US$ 0,02, uma vez só.

**Para que serve na fase 2:**

- reperguntas do examinador sobre assuntos ligados à questão;
- treino dos 199 temas do edital, que hoje não têm padrão de resposta: a base encontra as respostas do acervo que tratam do tema e elas viram a referência da correção;
- sugestão do que estudar a seguir.

## 4. ONDE O OPENROUTER ENTRA

O OpenRouter funciona como uma **tomada universal para modelos de IA**:

- uma conta, uma chave e um saldo de créditos dão acesso a mais de 400 modelos de vários fabricantes;
- trocar de modelo é trocar um nome no código. Dá para comparar qualidade e custo sem refazer nada;
- ele oferece as três coisas de que o treino precisa: transcrição, correção por modelo de linguagem e embeddings para a base vetorial;
- **não cobra a mais pelo modelo**: repassa o preço do fabricante. A taxa fica na compra de créditos: 5,5% no cartão, com mínimo de US$ 0,80;
- **cada chave pode ter um limite de gasto** diário, semanal ou mensal. Passou do limite, as chamadas param. Isso protege contra conta surpresa e contra abuso;
- **não guarda o conteúdo das chamadas por padrão**, a menos que a conta autorize. Na página de privacidade da conta dá para impedir o envio a provedores que possam treinar modelos com os dados.

**Alternativa:** contratar direto um fabricante, como a Anthropic. Você já fez isso: o pipeline de `acervo/pipeline/` reescreveu 632 respostas pela API da Anthropic, com chave e créditos. O OpenRouter é a mesma ideia com um intermediário a mais, e a vantagem é poder testar vários modelos com a mesma conta. Para a fase de experimentar, ele é a escolha mais prática; depois de escolhido o modelo, dá para decidir se vale ir direto ao fabricante.

## 5. ONDE FICA CADA PEÇA

```text
Navegador            Função no Supabase              OpenRouter
(grava a voz)  --->  (guarda a chave,          --->  (transcreve e corrige)
                      confere se está logada,
                      conta a cota do dia)
      ^                        |
      |                        v
      +---- mostra a     grava a avaliação numa
            avaliação    tabela protegida por RLS
```

A peça do meio é uma **Edge Function** do Supabase: um pequeno programa que roda no servidor. O plano gratuito inclui 500 mil chamadas por mês. A chave do OpenRouter fica guardada nela como segredo (`supabase secrets set OPENROUTER_API_KEY=...`, ou pelo painel).

**O que nunca fazer:**

- **colocar a chave do OpenRouter no `app.js` ou em qualquer arquivo de `public/`.** Qualquer pessoa que abrisse o site copiaria a chave e gastaria os seus créditos. As regras do projeto já proíbem (`REGRAS-DO-PROJETO.md`, seção 5);
- mandar o áudio do navegador direto para o OpenRouter, pelo mesmo motivo;
- mostrar a avaliação da IA como gabarito oficial.

**Atenção ao plano gratuito do Supabase:** ele pausa o projeto depois de uma semana sem atividade. Para um produto com pessoas usando, o plano Pro (a partir de US$ 25 por mês) acaba com a pausa.

## 6. QUANTO CUSTA POR TREINO

Estimativa para **uma resposta de 5 minutos**, com os preços publicados no OpenRouter em 22/09/2026.

Premissas: 5 minutos de fala dão cerca de 650 palavras, na ordem de 1.000 tokens; o padrão de resposta médio do acervo tem 3.700 caracteres, cerca de 1.000 tokens (os 10% maiores passam de 8.000 caracteres); as instruções do examinador somam cerca de 1.500 tokens; a devolutiva, cerca de 1.000. Arredondando para cima: 5.000 tokens de entrada e 1.000 de saída.

| Parte | Modelo (exemplo) | Preço por milhão de tokens | Custo estimado |
|---|---|---|---|
| Transcrição | Whisper ou Gemini com áudio | varia por segundo ou por token | US$ 0,01 a 0,02 |
| Correção, econômica | `google/gemini-3.7-flash` | US$ 0,75 entrada · 3,75 saída | US$ 0,008 |
| Correção, intermediária | `anthropic/claude-sonnet-5` | US$ 2 entrada · 10 saída | US$ 0,02 |
| Correção, mais forte | `anthropic/claude-opus-5.5` | US$ 4 entrada · 20 saída | US$ 0,04 |

**Total por resposta corrigida: de US$ 0,02 a 0,06.** Cada repergunta respondida custa mais ou menos o mesmo. Os modelos da tabela são exemplos para dar ordem de grandeza, não recomendação: a escolha sai do teste da fase 0.

Preços mudam. O OpenRouter informa o custo exato de cada chamada, então o número real aparece já nos primeiros testes.

## 7. QUALIDADE E CUIDADOS

- **A IA erra.** Corrigir com o padrão na mão reduz o erro, não o elimina. A tela deve dizer que a avaliação é automática e mostrar o trecho do padrão em que cada comentário se apoia.
- **O padrão de resposta precisa estar certo**, porque a IA corrige a partir dele. A revisão jurídica das respostas reescritas (P1-12) vale também para a IA.
- **Teste com o seu critério antes de abrir para outras pessoas:** umas 20 respostas suas, algumas boas e algumas fracas de propósito, e comparar a nota da IA com a sua.
- **Voz é dado pessoal.** Recomendação: não guardar o áudio. Transcrever e descartar, guardando só o texto, e só se a pessoa quiser. A política de privacidade precisa dizer isso antes da primeira gravação (P2-16), com o consentimento de quem grava.
- **Direitos autorais do acervo (P2-04).** Mandar o conteúdo a um provedor de IA é mais um uso desse material.

## 8. FASES SUGERIDAS

**Fase 0: testar sem programar nada.** Uma tarde e poucos centavos.

1. Criar conta no OpenRouter, pôr de US$ 5 a 10 de créditos e definir um limite na chave.
2. Gravar no celular a sua resposta a uma questão do acervo e transcrever com o próprio recurso de ditado do celular.
3. No chat do OpenRouter, que permite mandar a mesma mensagem a vários modelos e ler as respostas lado a lado, colar as instruções do examinador, a pergunta, o padrão de resposta e a transcrição.
4. Repetir com umas cinco questões e escolher o modelo que corrige mais parecido com você.

Resultado: as instruções do examinador aprovadas por você e um modelo escolhido.

**Fase 1: correção da questão sorteada, sem base vetorial.** Gravação no navegador, função no Supabase, transcrição, correção e tela de devolutiva. Antes dela: `/dashboard` exigindo login (E6 da P1-15), identificador estável por questão (F2 da P1-16), política de privacidade atualizada e microfone liberado no `_headers`.

**Fase 2: examinador com reperguntas e base vetorial.** Liga a extensão `vector` no Supabase, gera as impressões digitais do acervo, e a correção passa a buscar material relacionado. Abre os 199 temas do edital para correção.

**Fase 3: voz do examinador e simulado completo.** O examinador lê a pergunta em voz alta e conduz uma sequência de perguntas com tempo, como numa banca.

## 9. DECISÕES QUE SÃO SUAS

1. A correção por IA fica só no plano pago, como está na seção 2.6 de `ARQUITETURA.md`, ou tem algumas correções grátis para experimentar?
2. Guardar só o texto da resposta ou também o áudio? A recomendação é só o texto.
3. Qual o tom da devolutiva: examinador rigoroso ou professor que orienta?
4. As respostas reescritas (`##FALA##` e `##ROTEIRO##`, P1-12) entram no site antes da IA? A recomendação é que sim, porque o roteiro melhora a correção.

## 10. GLOSSÁRIO

| Termo | Significado |
|---|---|
| Modelo de linguagem (LLM) | o programa de IA que lê e escreve texto: Claude, GPT, Gemini |
| Instruções (*prompt*) | o texto que diz à IA o que fazer e como responder |
| Token | pedaço de palavra; é a unidade de cobrança. Em português, uma palavra dá de um a dois tokens |
| Transcrição | transformar a fala gravada em texto |
| Embedding | a "impressão digital de significado" de um texto, em forma de números |
| Base vetorial | onde se guardam os embeddings para buscar por significado; aqui, a extensão `vector` do Supabase |
| RAG | buscar o material certo e entregá-lo à IA antes de pedir a resposta |
| Edge Function | pequeno programa que roda no servidor do Supabase; é onde a chave fica guardada |
| Chave de API | a senha que autoriza gastar os créditos da conta; nunca pode ir para o navegador |

## FONTES CONSULTADAS EM 22/09/2026

- OpenRouter, início rápido: https://openrouter.ai/docs/quickstart
- OpenRouter, perguntas frequentes (preço, taxa, registro de chamadas): https://openrouter.ai/docs/faq
- OpenRouter, transcrição: https://openrouter.ai/docs/guides/overview/multimodal/stt
- OpenRouter, áudio como entrada: https://openrouter.ai/docs/features/multimodal/audio
- OpenRouter, embeddings: https://openrouter.ai/docs/api-reference/embeddings
- OpenRouter, limites de crédito por chave: https://openrouter.ai/docs/api_reference/limits
- OpenRouter, privacidade: https://openrouter.ai/docs/features/privacy-and-logging
- OpenRouter, preços dos modelos: `https://openrouter.ai/api/v1/models`, consultado em 22/09/2026
- OpenRouter, chat para comparar modelos: https://openrouter.ai/chat
- Supabase, pgvector: https://supabase.com/docs/guides/database/extensions/pgvector
- Supabase, segredos das Edge Functions: https://supabase.com/docs/guides/functions/secrets
- Supabase, preços e pausa do plano gratuito: https://supabase.com/pricing
