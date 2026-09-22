#!/usr/bin/env node
/* Copia a biblioteca do Supabase de node_modules para public/assets/vendor/.

   Uso:  npm install        (instala a versão fixada em package.json)
         npm run vendor

   Desde 22/09/2026 o site deixa de buscar a biblioteca em cdn.jsdelivr.net.
   A versão servida passa a ser a de package.json, sem salto silencioso de
   versão, sem depender da CDN no ar e sem entregar o IP de quem abre a tela
   de entrar a um terceiro.

   Para atualizar: npm install --save-dev --save-exact @supabase/supabase-js@<versão>,
   npm run vendor, e repetir o roteiro de autenticação de TESTES.md. */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const pacote = path.join(ROOT, 'node_modules', '@supabase', 'supabase-js');
const destino = path.join(ROOT, 'public', 'assets', 'vendor', 'supabase.js');

if (!fs.existsSync(pacote)) {
  console.error('Biblioteca não encontrada em node_modules. Rode "npm install" antes.');
  process.exit(1);
}

const { version } = JSON.parse(fs.readFileSync(path.join(pacote, 'package.json'), 'utf8'));
const codigo = fs.readFileSync(path.join(pacote, 'dist', 'umd', 'supabase.js'), 'utf8');
const cabecalho = `/*! @supabase/supabase-js ${version} | MIT | https://github.com/supabase/supabase-js\n` +
  '    Copiado de node_modules por scripts/copiar-vendor.mjs. Não editar à mão. */\n';

fs.mkdirSync(path.dirname(destino), { recursive: true });
fs.writeFileSync(destino, cabecalho + codigo);
console.log(`public/assets/vendor/supabase.js atualizado para a versão ${version}.`);
