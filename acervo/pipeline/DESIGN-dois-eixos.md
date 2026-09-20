# Navegação por disciplina e por concurso — desenho

Objetivo: cada questão vive na sua disciplina, mostra onde foi aplicada, e a pessoa pode navegar tanto por disciplina quanto por concurso.

---

## O problema atual

`DPE_ORAL_QUESTOES` tem 10 chaves, mas elas não são da mesma natureza:

- `civil`, `empresarial`, `consumidor`, `difusos_coletivos`, `processo_penal`, `criminologia`, `eca`, `principios_institucionais`, `direitos_humanos` → **disciplinas**
- `dpe_ba_2022` → **concurso**

Um eixo só, com duas coisas diferentes dentro. Daí a impossibilidade de navegar por concurso: a informação de onde a questão caiu não existe como dado, existe como nome de gaveta — e só para um dos casos.

## O modelo que resolve

Cada questão vira um objeto com identidade própria e uma lista de aplicações:

```json
{
  "id": "civil-0042",
  "disciplina": "civil",
  "tema": "bens",
  "pergunta": "...",
  "resposta": "##FALA## ... ##ROTEIRO## ...",
  "aplicacoes": [
    { "concurso": "DPE-BA", "ano": 2022, "banca": "FCC", "fase": "oral", "ponto": 33 }
  ]
}
```

**`aplicacoes` é uma lista, e isso é o ponto central.** A mesma questão pode ter caído em mais de um concurso — acontece o tempo todo em oral. Com lista, ela aparece uma vez na disciplina e nas duas listas de concurso. Com gaveta, você seria obrigada a duplicar o texto.

Questão sem aplicação conhecida fica com `aplicacoes: []`. Continua navegável por disciplina, só não aparece na visão por concurso.

`tema` é opcional e permite uma terceira navegação depois, mais fina que disciplina.

## Duplicação — verificada, e não existe

Hipótese testada e descartada com o `4_duplicatas.py`, em 4 de agosto de 2026.

Comparadas as 150 questões de `dpe_ba_2022` contra as 600 das disciplinas, por sobreposição de palavras de conteúdo mais conferência por sequência de texto:

- **zero** suspeitas fortes
- 2 suspeitas fracas
- 148 sem par algum
- semelhança máxima observada: **0,37** · mediana: **0,16**

O detector foi validado antes de se confiar no resultado: dá 1.0 em texto idêntico, 1.0 em texto com pequena alteração, e encontra uma duplicata plantada de propósito no meio das disciplinas.

**Conclusão:** as questões da DPE-BA são distintas. Não há economia a fazer aqui — o lote inteiro precisa ser reescrito, ~US$ 4,85. Em compensação, também não haverá questão repetida no site.

O que continua valendo do plano: as 138 precisam **receber disciplina**, porque hoje estão numa gaveta de concurso. Isso é rotulagem mecânica, cabe em Haiku, uns US$ 0,20 pelo lote todo.

## Classificação das 150 da DPE-BA — feita, e uma decisão tomada

Rodada com `5_classificar.py` em Haiku, custo US$ 0,042.

| Disciplina | Questões |
|---|---|
| direitos_humanos | 52 |
| processo_penal | 26 |
| **constitucional** | **24** |
| **penal** | **13** |
| criminologia | 11 |
| principios_institucionais | 10 |
| difusos_coletivos | 6 |
| eca | 1 |

**Decisão dela, 4 de agosto de 2026: criar `constitucional` e `penal` como disciplinas do site.** Eram 37 questões sem lugar — constitucional sozinha é o terceiro maior bloco do concurso. Os rótulos já foram normalizados em `dados/disciplinas_dpe_ba.json`.

O site passa a ter **11 disciplinas**. Isso exige, quando os dados saírem do HTML: acrescentar as duas chaves em `ORAL_TOPICS` e nos rótulos de exibição, e criar o banco de temas de cada uma.

**Sobram 7 questões sem casa:** administrativo (4), financeiro (1), filosofia do direito (1), ambiental (1). Poucas demais para virar disciplina. Ou entram numa gaveta "Outras", ou esperam volume de concursos futuros. Ficam rotuladas como `outra:<nome>` até você decidir.

**`civil`, `empresarial` e `consumidor` receberam zero questões da DPE-BA.** É o que explica a ausência total de duplicação: a gaveta do concurso é complementar às outras, não sobreposta.

## Caminho progressivo

Cada etapa vale por si. Não precisa fazer tudo de uma vez.

**1. Tirar os dados do HTML.** Um JSON por disciplina, o site lendo deles. Já estava no plano e é pré-requisito de todo o resto — enquanto o conteúdo estiver dentro de um arquivo de 3,3 MB, qualquer mudança de estrutura é cirurgia de risco.

**2. Detectar duplicatas** entre `dpe_ba_2022` e as disciplinas. Custo zero, só script.

**3. Classificar as 138 por disciplina.** Tarefa mecânica de rotulagem — cabe em Haiku, custa uns US$ 0,20 pelo lote inteiro. Só para as que não forem duplicatas.

**4. Preencher `aplicacoes`.** As 138 recebem `DPE-BA / 2022 / FCC / oral`. As duplicatas recebem a mesma marcação **na questão que já existe**, em vez de virar item novo. As demais ficam com lista vazia por ora.

**5. Reescrever o que sobrou** com o pipeline atual, sem mudança nenhuma no prompt.

**6. Visão por concurso na interface.** Uma tela que lista os concursos e, dentro de cada um, as questões daquele ano, agrupadas por disciplina. É filtro sobre o mesmo dado, não conteúdo novo.

**7. Concursos futuros.** Chega uma prova nova: para cada questão, ou ela já existe e você só acrescenta uma entrada em `aplicacoes`, ou é inédita e entra na disciplina com a aplicação preenchida. O trabalho por prova nova cai muito depois que o modelo estiver de pé.

## Consequência para o produto

A visão por concurso é o que transforma o Sabatinando de banco de questões em ferramenta de preparação dirigida: a pessoa quer saber o que a FCC cobrou na DPE-BA, não só o que existe de Direito Civil. E o mesmo dado sustenta estatísticas — incidência por disciplina em cada banca, temas que se repetem entre concursos.

Isso não custa conteúdo novo. Custa só ter o modelo certo desde agora.
