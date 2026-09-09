/* ==========================================================================
   Entrar, criar conta e recuperar senha — páginas próprias.

   Criado em 09/09/2026 (etapa E4 da P1-15). Antes disso, os três fluxos
   viviam num modal sobre o simulador, e "criar conta" aparecia em contexto
   de quem já estava autenticado.

   Este arquivo reproduz FIELMENTE o que a camada de conta do app.js já
   fazia: mesmas validações, mesmas mensagens, mesmos parâmetros de API.
   Nada de novo foi inventado aqui — foi transposto.

   O que NÃO mudou de lugar: a definição de nova senha em /atualizar-senha
   continua dentro do app.js. Esse fluxo foi testado de ponta a ponta em
   09/09/2026 e não se mexe no que está comprovado funcionando.
   ========================================================================== */
(function () {
  'use strict';

  const SUPABASE_URL = 'https://whpjmvoctfyrhybbbhtc.supabase.co';
  const SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_y4js7OcnDBF4gTKaW0r30w_CcyinV0y';
  const ORIGEM = /^https?:/.test(window.location.origin) ? window.location.origin : 'https://subjetivando.netlify.app';
  const URL_CONFIRMACAO = new URL('/dashboard', ORIGEM).href;
  const URL_RECUPERACAO = new URL('/atualizar-senha', ORIGEM).href;

  const $ = (id) => document.getElementById(id);
  const painel = $('painel-conta');
  if (!painel) return;

  /* A biblioteca do Supabase vem de uma CDN e pode não chegar — rede corporativa,
     bloqueador, queda do serviço. Neste caso o restante desta página precisa
     continuar funcionando e, sobretudo, o formulário NÃO pode cair no envio
     nativo do navegador: sem `action`, o envio nativo recarregaria a página com
     e-mail e SENHA visíveis na barra de endereço. Por isso os manipuladores de
     `submit` são sempre registrados, e é dentro deles que se verifica se há
     cliente disponível. */
  const supabase = window.supabase
    ? window.supabase.createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)
    : null;
  const pagina = painel.dataset.pagina; // 'login' | 'cadastro' | 'recuperar'

  /* ---------- mensagens de erro, idênticas às do app ---------- */
  const ERROS = {
    'Invalid login credentials': 'E-mail ou senha incorretos.',
    'User already registered': 'Já existe uma conta com esse e-mail.',
    'Email not confirmed': 'Confirme seu e-mail antes de entrar — veja sua caixa de entrada.',
    'Password should be at least 6 characters': 'A senha precisa ter pelo menos oito caracteres.',
    'Unable to validate email address: invalid format': 'Esse e-mail não parece válido.',
    'New password should be different from the old password.': 'A nova senha precisa ser diferente da senha atual.',
    'Email rate limit exceeded': 'Muitos e-mails enviados em pouco tempo. Aguarde alguns minutos e tente de novo.'
  };
  const ERROS_POR_INICIO = [
    ['For security purposes, you can only request this after', 'Aguarde alguns segundos antes de tentar de novo.'],
    ['Token has expired or is invalid', 'Este link expirou ou já foi usado. Peça um novo e-mail de recuperação.'],
    ['Email link is invalid or has expired', 'Este link expirou ou já foi usado. Peça um novo e-mail de recuperação.']
  ];
  function traduzErro(error) {
    if (!error) return 'Algo deu errado. Tente de novo.';
    const mensagem = error.message || '';
    if (ERROS[mensagem]) return ERROS[mensagem];
    for (let i = 0; i < ERROS_POR_INICIO.length; i++) {
      if (mensagem.indexOf(ERROS_POR_INICIO[i][0]) === 0) return ERROS_POR_INICIO[i][1];
    }
    return 'Não foi possível concluir a operação. Confira os dados e tente novamente.';
  }

  /* ---------- avisos na tela ---------- */
  const aviso = $('aviso');
  function mostrar(texto, tipo) {
    if (!aviso) return;
    aviso.textContent = texto;
    aviso.dataset.tipo = tipo || 'info';
    aviso.hidden = false;
  }
  function limpar() { if (aviso) { aviso.hidden = true; aviso.textContent = ''; } }

  function carregando(botao, ligado, texto) {
    if (!botao) return;
    if (ligado) {
      botao.dataset.textoOriginal = botao.dataset.textoOriginal || botao.textContent;
      botao.textContent = texto || 'Enviando…';
      botao.disabled = true;
    } else {
      botao.textContent = botao.dataset.textoOriginal || botao.textContent;
      botao.disabled = false;
    }
  }

  /* ---------- para onde ir depois de entrar ---------- */
  function destino() {
    const bruto = new URLSearchParams(location.search).get('destino') || '/dashboard';
    // só caminhos internos: evita que um link externo empurre a pessoa para fora
    return /^\/[^/\\]/.test(bruto) || bruto === '/' ? bruto : '/';
  }

  /* ---------- quem já entrou não vê estas páginas ---------- */
  if (supabase) {
    supabase.auth.getSession().then(({ data }) => {
      if (data && data.session) window.location.replace(destino());
    }).catch(() => {});
  }

  /* Se a biblioteca não chegou, avisa em vez de deixar a pessoa tentando em vão. */
  function semBiblioteca() {
    mostrar('Não foi possível carregar um componente necessário para entrar. Verifique sua conexão, desative bloqueadores para este site e recarregue a página.', 'erro');
  }

  /* ---------- entrar ---------- */
  const formLogin = $('form-login');
  if (formLogin) {
    formLogin.addEventListener('submit', async (e) => {
      e.preventDefault();
      limpar();
      if (!supabase) { semBiblioteca(); return; }
      const email = ($('email').value || '').trim();
      const senha = $('senha').value || '';
      if (!email || !senha) { mostrar('Preencha e-mail e senha.', 'erro'); return; }
      const botao = $('btn-entrar');
      carregando(botao, true, 'Entrando…');
      try {
        const { error } = await supabase.auth.signInWithPassword({ email, password: senha });
        if (error) { mostrar(traduzErro(error), 'erro'); return; }
        window.location.replace(destino());
      } catch (err) {
        mostrar('Não foi possível conectar. Verifique sua internet e tente novamente.', 'erro');
      } finally {
        carregando(botao, false);
      }
    });
  }

  /* ---------- criar conta ---------- */
  const formCadastro = $('form-cadastro');
  if (formCadastro) {
    formCadastro.addEventListener('submit', async (e) => {
      e.preventDefault();
      limpar();
      if (!supabase) { semBiblioteca(); return; }
      const nome = ($('nome').value || '').trim();
      const email = ($('email').value || '').trim();
      const senha = $('senha').value || '';
      const senha2 = $('senha2').value || '';

      if (!nome || !email || !senha) { mostrar('Preencha todos os campos.', 'erro'); return; }
      if (senha.length < 8) { mostrar('A senha precisa ter pelo menos oito caracteres.', 'erro'); return; }
      if (senha !== senha2) { mostrar('As senhas não coincidem.', 'erro'); return; }

      const botao = $('btn-criar');
      carregando(botao, true, 'Criando conta…');
      try {
        const { data, error } = await supabase.auth.signUp({
          email,
          password: senha,
          options: { data: { nome_exibicao: nome }, emailRedirectTo: URL_CONFIRMACAO }
        });
        if (error) { mostrar(traduzErro(error), 'erro'); return; }
        if (data.user && !data.session) {
          formCadastro.hidden = true;
          mostrar('Quase lá! Enviamos um link de confirmação para ' + email + '. Confira também a caixa de spam.', 'ok');
          return;
        }
        window.location.replace('/dashboard');
      } catch (err) {
        mostrar('Não foi possível conectar. Verifique sua internet e tente novamente.', 'erro');
      } finally {
        carregando(botao, false);
      }
    });
  }

  /* ---------- recuperar senha ---------- */
  const formRecuperar = $('form-recuperar');
  if (formRecuperar) {
    formRecuperar.addEventListener('submit', async (e) => {
      e.preventDefault();
      limpar();
      if (!supabase) { semBiblioteca(); return; }
      const email = ($('email').value || '').trim();
      if (!email) { mostrar('Informe seu e-mail.', 'erro'); return; }
      const botao = $('btn-recuperar');
      carregando(botao, true, 'Enviando…');
      try {
        const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo: URL_RECUPERACAO });
        if (error) { mostrar(traduzErro(error), 'erro'); return; }
        mostrar('Se esse e-mail estiver cadastrado, enviamos um link de redefinição.', 'ok');
      } catch (err) {
        mostrar('Não foi possível conectar. Verifique sua internet e tente novamente.', 'erro');
      } finally {
        carregando(botao, false);
      }
    });
  }

  /* ---------- mostrar e ocultar a senha digitada ---------- */
  document.querySelectorAll('[data-ver-senha]').forEach((botao) => {
    botao.addEventListener('click', () => {
      const campo = $(botao.dataset.verSenha);
      if (!campo) return;
      const escondida = campo.type === 'password';
      campo.type = escondida ? 'text' : 'password';
      botao.textContent = escondida ? 'ocultar' : 'mostrar';
      botao.setAttribute('aria-label', escondida ? 'Ocultar a senha' : 'Mostrar a senha');
    });
  });
})();
