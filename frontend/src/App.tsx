import { useCallback, useEffect, useState } from 'react'
import type { FormEvent } from 'react'

import { AdminDashboard } from './AdminDashboard'
import {
  ApiError, changePassword, checkHealth, getCatalog, getLoans, getNotices, getProfile,
  getReservations, login, logout,
} from './api'
import type { CatalogTitle, Loan, Notice, Profile, Reservation } from './api'
import { messages } from './i18n'
import type { Language } from './i18n'
import { Preferences } from './Preferences'
import { ReaderDashboard } from './ReaderDashboard'
import type { Theme } from './themes'
import './App.css'

type Screen = 'checking' | 'login' | 'password' | 'dashboard' | 'unavailable'
type LoginRole = 'reader' | 'administrator'

function preference<T extends string>(key: string, fallback: T): T {
  return (localStorage.getItem(key) as T | null) ?? fallback
}

function App() {
  const [screen, setScreen] = useState<Screen>('checking')
  const [loginRole, setLoginRole] = useState<LoginRole>('reader')
  const [language, updateLanguage] = useState<Language>(() =>
    preference('athena-language', navigator.language.startsWith('pt') ? 'pt' : 'en'),
  )
  const [theme, updateTheme] = useState<Theme>('calculus')
  const [error, setError] = useState('')
  const [temporaryPassword, setTemporaryPassword] = useState('')
  const [profile, setProfile] = useState<Profile | null>(null)
  const [titles, setTitles] = useState<CatalogTitle[]>([])
  const [reservations, setReservations] = useState<Reservation[]>([])
  const [notices, setNotices] = useState<Notice[]>([])
  const [loans, setLoans] = useState<Loan[]>([])
  const text = messages[language]

  const setLanguage = (value: Language) => {
    updateLanguage(value)
    localStorage.setItem('athena-language', value)
    document.documentElement.lang = value === 'pt' ? 'pt-BR' : 'en'
  }
  const setTheme = (value: Theme) => {
    updateTheme(value)
    document.documentElement.dataset.theme = value
  }

  const probe = useCallback(async () => {
    try {
      const health = await checkHealth()
      if (['calculus', 'ocean', 'wine', 'slate', 'indigo', 'aqua'].includes(health.theme)) {
        updateTheme(health.theme as Theme)
        document.documentElement.dataset.theme = health.theme
      }
      setScreen('login')
    } catch { setScreen('unavailable') }
  }, [])

  useEffect(() => {
    document.documentElement.lang = language === 'pt' ? 'pt-BR' : 'en'
    document.documentElement.dataset.theme = theme
  }, [language, theme])

  // The initial availability probe intentionally transitions the UI state asynchronously.
  // oxlint-disable-next-line react/set-state-in-effect
  useEffect(() => { void probe() }, [probe])

  async function loadDashboard() {
    const currentProfile = await getProfile()
    setProfile(currentProfile)
    if (currentProfile.role === 'reader') {
      const [catalog, ownReservations, ownNotices, ownLoans] = await Promise.all([
        getCatalog(), getReservations(), getNotices(), getLoans(),
      ])
      setTitles(catalog); setReservations(ownReservations); setNotices(ownNotices); setLoans(ownLoans)
    }
    setScreen('dashboard')
  }

  async function submitLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError('')
    const data = new FormData(event.currentTarget)
    const password = String(data.get('password'))
    try {
      const result = await login(String(data.get('identifier')), password, loginRole)
      if (result.must_change_password) { setTemporaryPassword(password); setScreen('password') }
      else await loadDashboard()
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 0) setScreen('unavailable')
      else setError(text.invalid)
    }
  }

  async function submitPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError('')
    try {
      await changePassword(temporaryPassword, String(new FormData(event.currentTarget).get('newPassword')))
      setTemporaryPassword(''); setScreen('login')
    } catch { setError(text.invalid) }
  }

  const signOut = async () => {
    await logout(); setProfile(null); setScreen('login')
  }
  const preferences = <Preferences language={language} setLanguage={setLanguage} text={text} />

  return <>
    <a className="skip-link" href="#main-content">{text.skip}</a>
    <header className="site-header"><a className="brand" href="#main-content" aria-label="Athena">Athena</a>{preferences}</header>
    <main id="main-content" className={screen === 'dashboard' ? 'app-wide' : 'app-shell'}>
      {screen === 'checking' && <p aria-live="polite" aria-busy="true">Athena…</p>}
      {screen === 'unavailable' && <section><p className="eyebrow">Athena</p><h1>{text.unavailable}</h1><p role="alert">{text.connectionError}</p><button type="button" onClick={() => { setScreen('checking'); void probe() }}>{text.retry}</button></section>}
      {screen === 'login' && <section className={`auth-card login-${loginRole}`}><p className="eyebrow">Athena</p><h1>{text.login}</h1>
        <div className="role-switch" role="group" aria-label={text.loginAs}>
          <button type="button" aria-pressed={loginRole === 'reader'} onClick={() => setLoginRole('reader')}>{text.studentAccess}</button>
          <button type="button" aria-pressed={loginRole === 'administrator'} onClick={() => setLoginRole('administrator')}>{text.adminAccess}</button>
          <span className="role-switch-indicator" aria-hidden="true" />
        </div>
        <div key={loginRole} className="role-login-panel"><p className="meta">{loginRole === 'reader' ? text.studentWelcome : text.adminWelcome}</p><form onSubmit={submitLogin}>
        <label>{text.identifier}<input name="identifier" required autoComplete="username" /></label>
        <label>{text.password}<input name="password" type="password" required autoComplete="current-password" /></label>
        {error && <p role="alert">{error}</p>}<button type="submit">{text.login}</button>
      </form></div></section>}
      {screen === 'password' && <section className="auth-card"><h1>{text.firstAccess}</h1><form onSubmit={submitPassword}>
        <label>{text.current}<input value={temporaryPassword} disabled /></label>
        <label>{text.next}<input name="newPassword" type="password" minLength={15} required autoComplete="new-password" /></label>
        {error && <p role="alert">{error}</p>}<button type="submit">{text.change}</button>
      </form></section>}
      {screen === 'dashboard' && profile?.role === 'reader' && <ReaderDashboard text={text} profile={profile} initialTitles={titles} initialReservations={reservations} initialNotices={notices} initialLoans={loans} onLogout={() => void signOut()} />}
      {screen === 'dashboard' && profile?.role === 'administrator' && <AdminDashboard text={text} theme={theme} setTheme={setTheme} onLogout={() => void signOut()} />}
    </main>
  </>
}

export default App
