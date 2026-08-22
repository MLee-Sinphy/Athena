import '@testing-library/jest-dom/vitest'
import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import App from './App'

describe('App', () => {
  afterEach(() => {
    cleanup()
    vi.unstubAllGlobals()
  })

  it('identifies the Athena bootstrap screen when the backend responds', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true }))
    render(<App />)

    expect(await screen.findByRole('heading', { name: /biblioteca em preparação/i })).toBeVisible()
  })

  it('shows a clear error and no false success when the backend is unavailable', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
    render(<App />)

    expect(await screen.findByRole('alert')).toHaveTextContent(/não foi possível conectar/i)
    expect(screen.queryByRole('heading', { name: /biblioteca em preparação/i })).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: /tentar novamente/i })).toBeVisible()
  })
})
