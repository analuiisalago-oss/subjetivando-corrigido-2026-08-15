/** Configuração do Tailwind do Subjetivando.
 *
 *  Esta configuração reproduz o que o CDN de fato executava até 14/09/2026:
 *  tema padrão do Tailwind e normalização (preflight) ligada. O bloco de
 *  configuração que existia no index.html nunca chegou a ser lido pelo CDN,
 *  porque era atribuído antes do script que o lê. As cores e as fontes do
 *  projeto continuam vindo de styles.css e v41.css, como sempre vieram.
 *
 *  Para gerar o CSS depois de acrescentar uma classe do Tailwind:
 *    npm install      (só na primeira vez; instala a versão fixada em package.json)
 *    npm run css
 *  A versão 3.4.19 reproduz byte a byte o tailwind.css gerado em 20/09/2026.
 */
module.exports = {
  content: [
    './public/index.html',
    './public/assets/app.js'
  ],
  theme: {
    extend: {}
  },
  plugins: []
};
