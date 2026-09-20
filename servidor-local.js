/* Servidor estático mínimo para conferir o site na máquina, sem instalar nada.
   Uso, na pasta do projeto:  node servidor-local.js
   Depois abra http://localhost:8080  — serve a pasta public/.
   Para parar: Ctrl+C na janela do terminal.
   Este arquivo não vai para o ar; é só para conferência local. */
const http = require('http');
const fs = require('fs');
const path = require('path');

const RAIZ = path.join(__dirname, 'public');
const PORTA = 8080;

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

http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel === '/') rel = '/index.html';
  const arquivo = path.join(RAIZ, rel);

  if (!arquivo.startsWith(RAIZ)) { res.writeHead(403); return res.end('403'); }

  fs.readFile(arquivo, (err, dados) => {
    if (err) { res.writeHead(404); return res.end('404 ' + rel); }
    res.writeHead(200, {
      'Content-Type': TIPOS[path.extname(arquivo).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-store'
    });
    res.end(dados);
  });
}).listen(PORTA, () => console.log('Servindo public/ em http://localhost:' + PORTA + '  (Ctrl+C para parar)'));
