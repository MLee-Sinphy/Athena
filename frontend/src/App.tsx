import { useCallback, useEffect, useState } from 'react'

import './App.css'

type BackendState = 'checking' | 'available' | 'unavailable'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

function App() {
  const [backendState, setBackendState] = useState<BackendState>('checking')

  const checkBackend = useCallback(async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/health/`)
      setBackendState(response.ok ? 'available' : 'unavailable')
    } catch {
      setBackendState('unavailable')
    }
  }, [])

  const retryBackend = () => {
    setBackendState('checking')
    void checkBackend()
  }

  useEffect(() => {
    // The availability probe synchronizes the interface with the external API.
    // oxlint-disable-next-line react/set-state-in-effect
    void checkBackend()
  }, [checkBackend])

  if (backendState === 'checking') {
    return <main className="app-shell" aria-busy="true">Conectando à biblioteca…</main>
  }

  if (backendState === 'unavailable') {
    return (
      <main className="app-shell">
        <p className="eyebrow">Athena</p>
        <h1>Serviço temporariamente indisponível</h1>
        <p role="alert">Não foi possível conectar ao sistema da biblioteca.</p>
        <p>O backend pode estar desligado. Tente novamente quando ele estiver disponível.</p>
        <button type="button" onClick={retryBackend}>Tentar novamente</button>
      </main>
    )
  }

  return (
    <main className="app-shell">
      <p className="eyebrow">Athena</p>
      <h1>Biblioteca em preparação</h1>
      <p>O ambiente inicial está pronto para receber os primeiros fluxos do sistema.</p>
    </main>
  )
}

export default App
