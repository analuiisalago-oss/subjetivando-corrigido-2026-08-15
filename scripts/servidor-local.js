/* Servidor estático mínimo para conferir o site na máquina, sem instalar nada.
   Uso, na pasta do projeto:  npm run dev   (ou: node scripts/servidor-local.js)
   Depois abra http://localhost:8080  — serve a pasta public/.
   Para parar: Ctrl+C na janela do terminal.
   Este arquivo não vai para o ar; é só para conferência local.

   Desde 22/09/2026 ele lê public/_redirects e public/_headers, como o Netlify.
   Antes disso, "/" abria o simulador em vez de inicio.html, e /login,
   /cadastro, /sobre etc. davam 404 na máquina — o que se conferia aqui não
   era o que ia ao ar. As regras suportadas são as que o projeto usa:
   caminho exato ou terminado em "/*", status 200 (reescrita), 301/302
   (redirecionamento) e 404, com "!" para forçar. */
const http = require('http');
const fs = require('fs');
const path = require('path');

const RAIZ = path.join(__dirname, '..', 'public');
const PORTA = Number(process.env.PORT) || 8080;

const TIPOS = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.txt': 'text/plain; charset=utf-8'
};

function linhasUteis(arquivo) {
  try {
    return fs.readFileSync(path.join(RAIZ, arquivo), 'utf8').split(/\r?\n/)
      .filter((linha) => linha.trim() && !linha.trim().startsWith('#'));
  } catch (e) {
    return [];
  }
}

// "/dashboard/*" casa "/dashboard/qualquer-coisa"; "/*" casa tudo.
function casa(padrao, caminho) {
  if (padrao.endsWith('/*')) {
    const base = padrao.slice(0, -2);
    return caminho === base || caminho.startsWith(base + '/');
  }
  return padrao === caminho;
}

function lerRedirects() {
  return linhasUteis('_redirects').map((linha) => {
    const [de, para, status = '301'] = linha.trim().split(/\s+/);
    return { de, para, status: parseInt(status, 10), forcar: status.endsWith('!') };
  });
}

function lerHeaders() {
  const blocos = [];
  linhasUteis('_headers').forEach((linha) => {
    if (!/^\s/.test(linha)) { blocos.push({ padrao: linha.trim(), cabecalhos: {} }); return; }
    const i = linha.indexOf(':');
    if (i > 0 && blocos.length) blocos[blocos.length - 1].cabecalhos[linha.slice(0, i).trim()] = linha.slice(i + 1).trim();
  });
  return blocos;
}

function arquivoDe(caminho) {
  const alvo = path.join(RAIZ, caminho === '/' ? '/index.html' : caminho);
  if (!alvo.startsWith(RAIZ + path.sep)) return null;
  try { return fs.statSync(alvo).isFile() ? alvo : null; } catch (e) { return null; }
}

function responder(res, arquivo, status, caminho) {
  const cabecalhos = { 'Content-Type': TIPOS[path.extname(arquivo).toLowerCase()] || 'application/octet-stream' };
  lerHeaders().forEach((bloco) => {
    if (casa(bloco.padrao, caminho)) Object.assign(cabecalhos, bloco.cabecalhos);
  });
  // O servidor local nunca guarda cópia: cada recarga precisa mostrar o arquivo atual.
  cabecalhos['Cache-Control'] = 'no-store';
  fs.readFile(arquivo, (err, dados) => {
    if (err) { res.writeHead(500); return res.end('500'); }
    res.writeHead(status, cabecalhos);
    res.end(dados);
  });
}

http.createServer((req, res) => {
  let caminho;
  try { caminho = decodeURIComponent(req.url.split('?')[0]); } catch (e) { res.writeHead(400); return res.end('400'); }
  if (caminho.length > 1 && caminho.endsWith('/')) caminho = caminho.slice(0, -1);

  const existente = arquivoDe(caminho);
  const regra = lerRedirects().find((r) => casa(r.de, caminho) && (r.forcar || !existente));

  if (!regra) {
    if (existente) return responder(res, existente, 200, caminho);
    res.writeHead(404); return res.end('404 ' + caminho);
  }
  if (regra.status === 301 || regra.status === 302) {
    res.writeHead(regra.status, { Location: regra.para }); return res.end();
  }
  const destino = arquivoDe(regra.para);
  if (!destino) { res.writeHead(404); return res.end('404 ' + regra.para); }
  return responder(res, destino, regra.status, caminho);
}).listen(PORTA, () => console.log('Servindo public/ em http://localhost:' + PORTA + '  (Ctrl+C para parar)'));
