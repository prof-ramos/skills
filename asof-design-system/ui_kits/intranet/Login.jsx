// Login — single white card centered on the navy primary canvas.

function Login({ onSubmit }) {
  const [error, setError] = React.useState(null);
  function handle(e) {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    if (!email || !password) {
      setError('Email ou senha inválidos.');
      return;
    }
    onSubmit();
  }
  return (
    <main className="login-shell">
      <div className="login-card">
        <h1>ASOF</h1>
        <p className="sub">Intranet — Acesso restrito</p>

        {error && (
          <div role="alert" style={{ background: 'var(--error-container)', border: '1px solid #fca5a5', color: '#7f1d1d', borderRadius: 'var(--r-md)', padding: '10px 14px', fontSize: 13, marginBottom: 14 }}>
            {error}
          </div>
        )}

        <form onSubmit={handle}>
          <div className="field">
            <label htmlFor="email">Email</label>
            <input id="email" name="email" type="email" autoComplete="email" defaultValue="diretoria@asof.org.br" />
          </div>
          <div className="field">
            <label htmlFor="password">Senha</label>
            <input id="password" name="password" type="password" autoComplete="current-password" defaultValue="••••••••" />
          </div>
          <button type="submit" className="btn btn-primary">Entrar</button>
        </form>
      </div>
    </main>
  );
}

Object.assign(window, { Login });
