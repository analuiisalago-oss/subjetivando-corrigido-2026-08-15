#!/usr/bin/env node
/**
 * Teste da autorização de incorporação de dados locais (pendência P1-08).
 *
 * Em 09/09/2026, teste real mostrou que a pergunta "este navegador tem
 * progresso salvo antes do login" reaparecia depois de o usuário ter
 * respondido "Cancelar". A causa: a função gravava apenas o "sim"; a recusa
 * não deixava rastro, e qualquer novo carregamento de página — o retorno do
 * link de confirmação de e-mail, por exemplo — trazia a pergunta de volta.
 *
 * Este teste extrai a função REAL de public/assets/app.js, sem reescrevê-la,
 * e verifica a tabela de casos. O caso decisivo é o 2: com a recusa já
 * registrada, a pergunta não pode ser feita nenhuma vez.
 *
 * Uso:  node scripts/teste_consentimento.mjs
 * Saída: código 0 se todos os casos passarem, 1 se algum falhar.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARQUIVO = process.argv[2] || path.join(RAIZ, 'public', 'assets', 'app.js');

const src = fs.readFileSync(ARQUIVO, 'utf8');
const ini = src.indexOf('function autorizarIncorporacao');
if (ini < 0) {
  console.error('FALHOU  função autorizarIncorporacao não encontrada em', ARQUIVO);
  process.exit(1);
}
let prof = 0, fim = -1;
for (let k = src.indexOf('{', ini); k < src.length; k++) {
  if (src[k] === '{') prof++;
  else if (src[k] === '}') { prof--; if (prof === 0) { fim = k + 1; break; } }
}
const fonte = src.slice(ini, fim);

let armazem = {}, perguntou = 0, respostaDoUsuario = null, temDados = true;
const localStorage = {
  getItem: (k) => (k in armazem ? armazem[k] : null),
  setItem: (k, v) => { armazem[k] = String(v); },
  removeItem: (k) => { delete armazem[k]; },
};
const CONSENTIMENTO = 'subj_sync_consent_v1_';
const temDadosLocais = () => temDados;
const window = { confirm: () => { perguntou++; return respostaDoUsuario; } };
const autorizarIncorporacao = eval('(' + fonte + ')');

const CHAVE = CONSENTIMENTO + 'u1';
const casos = [
  ['primeira vez, usuário CANCELA',    {},                  false, true,  { ret: false, perguntas: 1, gravado: 'nao' }],
  ['recusa já registrada',             { [CHAVE]: 'nao' },  false, true,  { ret: false, perguntas: 0, gravado: 'nao' }],
  ['aceite já registrado',             { [CHAVE]: 'sim' },  false, true,  { ret: true,  perguntas: 0, gravado: 'sim' }],
  ['primeira vez, usuário ACEITA',     {},                  true,  true,  { ret: true,  perguntas: 1, gravado: 'sim' }],
  ['não há dados locais a incorporar', {},                  false, false, { ret: true,  perguntas: 0, gravado: 'sim' }],
];

let falhas = 0;
casos.forEach(([nome, inicial, resposta, dados, esperado], i) => {
  armazem = { ...inicial };
  perguntou = 0;
  respostaDoUsuario = resposta;
  temDados = dados;
  const ret = autorizarIncorporacao('u1');
  const gravado = armazem[CHAVE] ?? '(nada)';
  const ok = ret === esperado.ret && perguntou === esperado.perguntas && gravado === esperado.gravado;
  if (!ok) falhas++;
  console.log(`${ok ? 'PASSOU' : 'FALHOU'}  ${i + 1}. ${nome}`);
  if (!ok) {
    console.log(`        retorno=${ret} (esperado ${esperado.ret})`);
    console.log(`        perguntou ${perguntou}x (esperado ${esperado.perguntas})`);
    console.log(`        gravou "${gravado}" (esperado "${esperado.gravado}")`);
  }
});

console.log(falhas === 0
  ? `\nConsentimento: ${casos.length} casos, nenhuma falha.`
  : `\nConsentimento: ${falhas} de ${casos.length} casos falharam.`);
process.exit(falhas === 0 ? 0 : 1);
