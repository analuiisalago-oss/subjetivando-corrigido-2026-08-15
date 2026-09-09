# Plano — publicar o que já existe e refazer a FALA

> **DOCUMENTO HISTÓRICO (04/08/2026).** A afirmação abaixo de que o conteúdo está pronto para publicação se refere ao HTML intermediário `minha-banca.NOVO.html`, não à fonte atual `../minha-banca.NOVO_3.html`. Não publique nem copie esse HTML sobre a versão atual. A mesclagem deve ser refeita de forma controlada somente após a revisão de `PONTOS-A-VERIFICAR.md` e o fechamento da pendência P1-12.

Duas frentes independentes. **Faça a A primeiro:** ela é barata, não gasta API nenhuma, e coloca no ar 718 respostas que já estão prontas e pagas.

---

# PARTE A — Publicar no site (custo zero de API)

O conteúdo já está mesclado no `minha-banca.NOVO.html`. Falta só o site saber exibir.

## Por que ainda não dá para publicar

A função que mostra a resposta é esta, e ela despeja o texto cru na tela:

```js
espelhoText.textContent = item.resposta;
```

Resultado: o usuário lê `##FALA##` e `##ROTEIRO##` escritos no meio da resposta.

## Passo A1 — Substituir a função `showResposta`

Abra o `minha-banca.html` num editor de texto, procure por `function showResposta` e **substitua a função inteira** por esta:

```js
  function showResposta(item){
    espelhoResumo.style.display = 'none';
    document.querySelector('.modelo-card').style.display = 'none';
    document.querySelector('.avalia-card').style.display = 'none';
    document.getElementById('bancaTitle').textContent = state.tcdfSub === 'prova_disc' || state.tcdfSub === 'prova_peca' ? 'Padrão de resposta oficial — Cebraspe' : 'Resposta / fundamentos esperados';

    const txt = item.resposta || '';
    espelhoText.innerHTML = '';

    // resposta antiga, ainda sem marcador: mostra como sempre foi
    if (txt.indexOf('##FALA##') === -1) {
      espelhoText.textContent = txt;
      return;
    }

    const depoisFala = txt.split('##FALA##')[1] || '';
    const partes     = depoisFala.split('##ROTEIRO##');
    const fala       = (partes[0] || '').trim();
    const roteiro    = ((partes[1] || '').split('##VERIFICAR##')[0] || '').trim();

    const bloco = (titulo, corpo) => {
      if (!corpo) return;
      const sec = document.createElement('div');
      sec.className = 'sub-card';
      const h = document.createElement('div');
      h.className = 'sub-title';
      h.textContent = titulo;
      const p = document.createElement('div');
      p.className = 'espelho-text';
      p.style.whiteSpace = 'pre-wrap';
      p.textContent = corpo;
      sec.appendChild(h);
      sec.appendChild(p);
      espelhoText.appendChild(sec);
    };

    bloco('Padrão de resposta esperado', fala);
    bloco('O que o examinador espera que você domine', roteiro);
  }
```

Três cuidados que essa versão já resolve:

- **Respostas antigas não quebram.** Se o item não tiver marcador, ele exibe como antes. Isso importa porque nem tudo foi convertido.
- **O bloco `##VERIFICAR##` nunca aparece.** É relatório interno.
- **As quebras de linha do roteiro são preservadas**, pelo `pre-wrap`. Sem isso, os subtítulos ficariam grudados no texto.

## Passo A2 — Mesclar de novo

O `.NOVO.html` que existe foi gerado da versão antiga da função. Rode outra vez, já com o site corrigido:

```
py 3_mesclar.py .\minha-banca.html
```

Ele valida os 750 itens, roda a varredura de resíduos e gera também o `PONTOS-A-VERIFICAR.md`.

## Passo A3 — Conferir no navegador

Abra o `minha-banca.NOVO.html` com dois cliques e teste ao menos:

- uma questão de **civil**, **eca** e **direitos_humanos** — devem mostrar dois cartões
- uma de **dpe_ba_2022** — se ainda não converteu, deve mostrar o texto antigo sem quebrar
- uma questão com `resposta: null` — não pode dar erro em branco

Confirme que `##FALA##` não aparece em lugar nenhum.

## Passo A4 — Publicar

Só depois de conferir: renomeie o `minha-banca.html` atual para `minha-banca.BACKUP.html`, e o `.NOVO.html` para `minha-banca.html`. Arraste para o Netlify, ou faça o commit se estiver ligado a repositório.

**Não apague o backup** até navegar no site publicado.

---

# PARTE B — Refazer a FALA (~US$ 15,57)

## Por que só a FALA

Medido nas 718 respostas: a FALA é **31%** do texto, o ROTEIRO é **69%**.

| | |
|---|---|
| Refazer tudo | US$ 25,13 |
| **Refazer só a FALA** | **US$ 15,57** |

Além de economizar US$ 9,50, o ROTEIRO fica byte a byte idêntico — zero risco de regressão em dois terços do conteúdo que você já aprovou.

## O que o script precisa fazer

**Entrada de cada item:** o enunciado e o ROTEIRO atual.
**Não mandar a FALA antiga.** Se o modelo vir a versão engessada, ele tende a editá-la de leve em vez de reescrever. O ROTEIRO já tem todo o conteúdo jurídico necessário.

**Prompt:** a Parte I do `prompt_sistema.md`, que já foi corrigida, mais os pares do `RESPOSTAS EXEMPLARES.txt` embutidos como exemplos. Exemplo ensina mais que lista de proibição — foi o par da inamovibilidade que resolveu o diagnóstico, não as diretrizes.

**Saída:** só o texto da nova FALA. Nada de marcador, nada de roteiro.

**Remontagem:** trocar apenas o bloco entre `##FALA##` e `##ROTEIRO##`. O resto do campo permanece intacto, incluindo o `##VERIFICAR##`.

## Ordem de execução

1. Escrever o `6_refazer_fala.py`
2. Rodar `--teste 5` (uns 20 centavos) e **ler as cinco**
3. Se o registro estiver certo, rodar por matéria
4. `py 3_mesclar.py` e conferir no navegador

Se o teste de 5 não convencer, o ajuste é no `prompt_sistema.md` — e o melhor investimento é acrescentar mais dois ou três pares "atual versus exemplar" de disciplinas diferentes.

## Orçamento

Você tem pouco crédito. Prioridade: **Parte A não custa nada e já entrega valor.** A Parte B pode esperar o crédito.

Se quiser fazer parcial, comece pelas matérias que você mais usa para estudar — a melhora aparece onde você lê.

---

## Comando para a próxima conversa

Abra chat novo, conecte `Desktop\files`, e mande:

```
Leia pipeline/PLANO-FALA-E-SITE.md.
Aplique a Parte A: corrija a função showResposta no minha-banca.html.
Depois me diga o que testar no navegador.
```

E, quando houver crédito:

```
Leia pipeline/PLANO-FALA-E-SITE.md e o prompt_sistema.md.
Escreva o 6_refazer_fala.py conforme a Parte B e rode o teste de 5.
```
