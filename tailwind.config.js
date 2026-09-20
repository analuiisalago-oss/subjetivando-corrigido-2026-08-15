/** Configuração do Tailwind do Subjetivando.
 *
 *  Esta configuração reproduz o que o CDN de fato executava até 14/09/2026:
 *  tema padrão do Tailwind e normalização (preflight) ligada. O bloco de
 *  configuração que existia no index.html nunca chegou a ser lido pelo CDN,
 *  porque era atribuído antes do script que o lê. As cores e as fontes do
 *  projeto continuam vindo de styles.css e v41.css, como sempre vieram.
 *
 *  Para gerar o CSS depois de acrescentar uma classe do Tailwind:
 *    node node_modules/tailwindcss/lib/cli.js -i tailwind-entrada.css -o public/assets/tailwind.css --minify
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
