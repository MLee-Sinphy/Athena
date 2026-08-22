import '@testing-library/jest-dom/vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import App from './App'

describe('App', () => {
  afterEach(() => {
    cleanup()
    vi.unstubAllGlobals()
  })

  it('shows login when the backend responds', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true }))
    render(<App />)

    expect(await screen.findByRole('heading', { name: /entrar|sign in/i })).toBeVisible()
  })

  it('shows a clear error and no false success when the backend is unavailable', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
    render(<App />)

    expect(await screen.findByRole('alert')).toHaveTextContent(/não foi possível conectar|could not be reached/i)
    expect(screen.queryByRole('heading', { name: /entrar|sign in/i })).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: /tentar novamente|try again/i })).toBeVisible()
  })

  it('authenticates without persisting the token in browser storage', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({ ok: true })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ access_token: 'opaque-secret', must_change_password: false }),
      })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ results: [] }) })
    vi.stubGlobal('fetch', fetchMock)
    const storageSpy = vi.spyOn(Storage.prototype, 'setItem')
    render(<App />)

    fireEvent.change(await screen.findByLabelText(/e-mail ou matrícula|email or registration/i), {
      target: { value: 'reader@example.com' },
    })
    fireEvent.change(screen.getByLabelText(/^senha$|^password$/i), {
      target: { value: 'a valid library passphrase' },
    })
    fireEvent.click(screen.getByRole('button', { name: /entrar|sign in/i }))

    expect(await screen.findByRole('heading', { name: /biblioteca em preparação|library in preparation/i })).toBeVisible()
    expect(storageSpy).not.toHaveBeenCalled()
  })
})
