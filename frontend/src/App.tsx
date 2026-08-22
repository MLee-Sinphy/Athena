import { useCallback, useEffect, useState } from 'react'
import type { FormEvent } from 'react'

import { ApiError, changePassword, checkHealth, login, logout } from './api'
import './App.css'

type Screen = 'checking' | 'login' | 'password' | 'ready' | 'unavailable'
type Language = 'pt' | 'en'

const copy = {
  pt: {
    unavailable: 'Serviço temporariamente indisponível',
    connectionError: 'Não foi possível conectar ao sistema da biblioteca.',
    retry: 'Tentar novamente',
    login: 'Entrar',
    identifier: 'E-mail ou matrícula',
    password: 'Senha',
    invalid: 'E-mail, matrícula ou senha inválidos.',
    firstAccess: 'Defina sua nova senha',
    current: 'Senha temporária',
    next: 'Nova senha',
    change: 'Alterar senha',
    ready: 'Biblioteca em preparação',
    readyText: 'Você entrou com segurança. O catálogo será o próximo incremento.',
    logout: 'Sair',
  },
  en: {
    unavailable: 'Service temporarily unavailable',
    connectionError: 'The library system could not be reached.',
    retry: 'Try again',
    login: 'Sign in',
    identifier: 'Email or registration ID',
    password: 'Password',
    invalid: 'Invalid email, registration ID, or password.',
    firstAccess: 'Set your new password',
    current: 'Temporary password',
    next: 'New password',
    change: 'Change password',
    ready: 'Library in preparation',
    readyText: 'You signed in securely. The catalog is the next increment.',
    logout: 'Sign out',
  },
}

function App() {
  const [screen, setScreen] = useState<Screen>('checking')
  const [language, setLanguage] = useState<Language>(() =>
    navigator.language.startsWith('pt') ? 'pt' : 'en',
  )
  const [error, setError] = useState('')
  const [temporaryPassword, setTemporaryPassword] = useState('')
  const text = copy[language]

  const probe = useCallback(async () => {
    try {
      await checkHealth()
      setScreen('login')
    } catch {
      setScreen('unavailable')
    }
  }, [])

  useEffect(() => {
    // oxlint-disable-next-line react/set-state-in-effect
    void probe()
  }, [probe])

  async function submitLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    const data = new FormData(event.currentTarget)
    const password = String(data.get('password'))
    try {
      const result = await login(String(data.get('identifier')), password)
      if (result.must_change_password) {
        setTemporaryPassword(password)
        setScreen('password')
      } else {
        setScreen('ready')
      }
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 0) setScreen('unavailable')
      else setError(text.invalid)
    }
  }

  async function submitPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    const data = new FormData(event.currentTarget)
    try {
      await changePassword(temporaryPassword, String(data.get('newPassword')))
      setTemporaryPassword('')
      setScreen('login')
    } catch {
      setError(text.invalid)
    }
  }

  const languageButton = (
    <button
      type="button"
      className="language"
      onClick={() => setLanguage(language === 'pt' ? 'en' : 'pt')}
    >
      {language === 'pt' ? 'EN' : 'PT'}
    </button>
  )

  if (screen === 'checking') {
    return <main className="app-shell" aria-busy="true">Athena…</main>
  }
  if (screen === 'unavailable') {
    return (
      <main className="app-shell">
        {languageButton}<p className="eyebrow">Athena</p><h1>{text.unavailable}</h1>
        <p role="alert">{text.connectionError}</p>
        <button type="button" onClick={() => { setScreen('checking'); void probe() }}>
          {text.retry}
        </button>
      </main>
    )
  }
  if (screen === 'password') {
    return (
      <main className="app-shell">
        {languageButton}<p className="eyebrow">Athena</p><h1>{text.firstAccess}</h1>
        <form onSubmit={submitPassword}>
          <label>{text.current}<input value={temporaryPassword} disabled /></label>
          <label>{text.next}<input name="newPassword" type="password" minLength={15} required autoComplete="new-password" /></label>
          {error && <p role="alert">{error}</p>}<button type="submit">{text.change}</button>
        </form>
      </main>
    )
  }
  if (screen === 'ready') {
    return (
      <main className="app-shell">
        {languageButton}<p className="eyebrow">Athena</p><h1>{text.ready}</h1><p>{text.readyText}</p>
        <button type="button" onClick={() => void logout().finally(() => setScreen('login'))}>{text.logout}</button>
      </main>
    )
  }
  return (
    <main className="app-shell">
      {languageButton}<p className="eyebrow">Athena</p><h1>{text.login}</h1>
      <form onSubmit={submitLogin}>
        <label>{text.identifier}<input name="identifier" required autoComplete="username" /></label>
        <label>{text.password}<input name="password" type="password" required autoComplete="current-password" /></label>
        {error && <p role="alert">{error}</p>}<button type="submit">{text.login}</button>
      </form>
    </main>
  )
}

export default App
