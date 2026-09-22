# ACERVO — MATÉRIA-PRIMA DAS QUESTÕES

**Nada nesta pasta vai para o site.** O Netlify publica só `public/`. O acervo que as pessoas usam fica dentro de `public/assets/app.js`, na constante `DPE_ORAL_QUESTOES`: 750 questões de Defensoria em 10 matérias, 718 com resposta. Editar arquivos daqui não muda o site.

Esta pasta guarda o trabalho editorial de agosto de 2026: a reescrita das respostas para o formato de prova oral, feita com a API da Anthropic, que ainda não chegou ao site.

## O que tem aqui

| Caminho | O que é |
|---|---|
| `respostas_*.json` (5 arquivos) | primeiras respostas reescritas, feitas em conversa (ver `docs/historico/RETOMAR.md`): consumidor, criminologia, direitos humanos parte 1, empresarial e processo penal. 89 itens |
| `ACERVO-REFINADO-718.html` | página de leitura com as respostas refinadas, na interface antiga "Minha Banca" |
| `pipeline/` | scripts Python que reescreveram as demais respostas em lote, com os prompts, a fila e os resultados |
| `pipeline/resultados/` | respostas reescritas por matéria: civil, difusos e coletivos, direitos humanos, DPE-BA 2022, ECA e princípios institucionais. 632 itens |
| `pipeline/resultados_fala/` | 43 itens com a parte falada refeita por `7_refazer_fala.py` |
| `pipeline/PONTOS-A-VERIFICAR.md` | dúvidas jurídicas levantadas pelo modelo durante a reescrita. **Precisam de conferência humana antes de qualquer uso** |
| `pipeline/minha-banca.html` | cópia da interface antiga usada como entrada do pipeline |
| `pipeline/*.md` | estado, fontes, classificação, duplicatas e planos daquela etapa |

Cada resposta reescrita tem dois blocos, separados por marcadores:

- `##FALA##`: a resposta como o candidato falaria diante da banca, de 120 a 250 palavras;
- `##ROTEIRO##`: o mapa do conteúdo, com subtítulos e fundamentos.

Nos arquivos, ` ||| ` marca quebra de parágrafo.

## Onde isso encontra o site

A troca das respostas publicadas pelas reescritas é a P1-12 de `docs/PENDENCIAS.md`, **bloqueada por revisão editorial e jurídica**. O caminho está lá: resolver `PONTOS-A-VERIFICAR.md`, aprovar o mérito, mesclar só os dados no `app.js` e adaptar a tela para mostrar "Como falar" e "Roteiro".

O `##ROTEIRO##` também é a melhor base para a correção por IA da prova oral: é a lista de pontos que a banca espera ouvir. Ver `docs/IA-PROVA-ORAL.md`.

A origem do material (compilados de candidatos, com URLs de curso removidas) está registrada em `pipeline/FONTES.md` e pesa na P2-04, de direitos autorais.

## Nomes antigos

O produto já se chamou **Minha Banca** e **Sabatinando** antes de **Subjetivando**. Os documentos de `pipeline/` usam os nomes e caminhos da época: `minha-banca.NOVO_3.html` como "fonte canônica", pasta `Desktop\files`, comandos de Windows. São registro histórico; não descrevem o repositório atual.

## Recuperar arquivos retirados

Nada foi apagado do histórico do Git. Para ver ou restaurar uma cópia:

```bash
# fonte antiga da interface, removida em 10/09/2026
git show 739b979~1:minha-banca.NOVO_3.html > /tmp/minha-banca.NOVO_3.html

# estado publicado em 15/08/2026, removido da raiz em 20/09/2026
git show 126e3d7~1:minha-banca.html > /tmp/minha-banca.html

# arquivos RESPOS_*.txt, removidos em 20/09/2026
git show 126e3d7~1:RESPOS_lote1.txt
```

## Rodar o pipeline de novo

Só depois de ler `pipeline/LEIA-ME.md`. Os scripts chamam a API da Anthropic, **gastam créditos** e exigem a chave em `ANTHROPIC_API_KEY`, que nunca pode ir para o repositório. O resultado continua sujeito à revisão jurídica da P1-12.
