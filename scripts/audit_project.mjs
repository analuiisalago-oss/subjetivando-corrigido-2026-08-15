#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SOURCE = path.join(ROOT, 'minha-banca.NOVO_3.html');
const PUBLIC = path.join(ROOT, 'public');
const html = fs.readFileSync(SOURCE, 'utf8');
const failures = [];

function extractLiteral(name) {
  const match = new RegExp(`\\b(?:const|let|var)\\s+${name}\\s*=`).exec(html);
  if (!match) throw new Error(`Constante ${name} não encontrada`);
  let start = match.index + match[0].length;
  while (/\s/.test(html[start])) start += 1;
  const opener = html[start];
  const closer = opener === '[' ? ']' : opener === '{' ? '}' : null;
  if (!closer) throw new Error(`Valor de ${name} não começa por objeto ou lista`);

  let depth = 0;
  let quote = null;
  let escaped = false;
  for (let i = start; i < html.length; i += 1) {
    const char = html[i];
    if (quote) {
      if (escaped) escaped = false;
      else if (char === '\\') escaped = true;
      else if (char === quote) quote = null;
      continue;
    }
    if (char === '"' || char === "'" || char === '`') {
      quote = char;
      continue;
    }
    if (char === opener) depth += 1;
    if (char === closer) {
      depth -= 1;
      if (depth === 0) return html.slice(start, i + 1);
    }
  }
  throw new Error(`Fim de ${name} não encontrado`);
}

function loadData(name) {
  return vm.runInNewContext(`(${extractLiteral(name)})`, Object.create(null), {
    timeout: 2000,
    filename: `${name}.data.js`,
  });
}

function count(value) {
  return Array.isArray(value)
    ? value.length
    : Object.values(value).reduce((total, items) => total + items.length, 0);
}

const expected = {
  ORAL_TOPICS: 199,
  DPE_ORAL_QUESTOES: 750,
  OAB_ITEMS: 55,
  TCDF_TEMAS: 55,
  TCDF_PROVAS: 6,
  TCDF_DISCURSIVAS: 37,
};
const data = {};

for (const [name, amount] of Object.entries(expected)) {
  data[name] = loadData(name);
  const actual = count(data[name]);
  console.log(`${actual === amount ? 'PASSOU' : 'FALHOU'}  ${name}: ${actual} itens`);
  if (actual !== amount) failures.push(`${name}: esperado ${amount}, encontrado ${actual}`);
}

const staticMarkup = html
  .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '')
  .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, '');
const ids = [...staticMarkup.matchAll(/\sid=["']([^"']+)["']/g)].map((match) => match[1]);
const duplicates = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
console.log(`${duplicates.length ? 'FALHOU' : 'PASSOU'}  IDs HTML únicos: ${ids.length}`);
if (duplicates.length) failures.push(`IDs duplicados: ${duplicates.join(', ')}`);

const expectedPublic = [
  '_headers',
  '_redirects',
  'assets/app.js',
  'assets/styles.css',
  'index.html',
  'robots.txt',
];
function listFiles(directory, prefix = '') {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const relative = path.posix.join(prefix, entry.name);
    return entry.isDirectory()
      ? listFiles(path.join(directory, entry.name), relative)
      : [relative];
  });
}
const publicFiles = listFiles(PUBLIC).sort();
const publicOk = JSON.stringify(publicFiles) === JSON.stringify(expectedPublic);
console.log(`${publicOk ? 'PASSOU' : 'FALHOU'}  Conteúdo isolado de public/: ${publicFiles.length} arquivos`);
if (!publicOk) failures.push(`public/ contém: ${publicFiles.join(', ')}`);

const publicText = publicFiles
  .map((file) => fs.readFileSync(path.join(PUBLIC, file), 'utf8'))
  .join('\n');
const secretPatterns = [
  /sb_secret_[A-Za-z0-9_-]+/,
  /\bservice_role\b/i,
  /\bsk_(?:live|test)_[A-Za-z0-9]+/,
  /ANTHROPIC_API_KEY\s*=\s*["'][^"']+["']/,
];
const hasSecretPattern = secretPatterns.some((pattern) => pattern.test(publicText));
console.log(`${hasSecretPattern ? 'FALHOU' : 'PASSOU'}  Sem padrão de segredo privado em public/`);
if (hasSecretPattern) failures.push('possível segredo privado na saída pública');

const dpeItems = Object.values(data.DPE_ORAL_QUESTOES).flat();
const answers = dpeItems.map((item) => item.resposta).filter((value) => typeof value === 'string');
const marked = answers.filter((answer) => answer.includes('##FALA##') && answer.includes('##ROTEIRO##')).length;
console.log(`AVISO   respostas DPE: ${answers.length} preenchidas; ${marked} com os dois marcadores editoriais`);

if (failures.length) {
  console.error(`\nAuditoria falhou:\n- ${failures.join('\n- ')}`);
  process.exitCode = 1;
} else {
  console.log('\nAuditoria estrutural concluída sem falhas.');
}
