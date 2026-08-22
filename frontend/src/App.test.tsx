import '@testing-library/jest-dom/vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import axe from 'axe-core'
import { afterEach, describe, expect, it, vi } from 'vitest'

import App from './App'

describe('App', () => {
  afterEach(() => {
    cleanup()
    vi.unstubAllGlobals()
    localStorage.clear()
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
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, email: 'reader@example.com', role: 'reader' }),
      })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ results: [] }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ results: [] }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ results: [] }) })
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

    expect(await screen.findByRole('heading', { name: /catálogo|catalog/i })).toBeVisible()
    expect(storageSpy).not.toHaveBeenCalledWith(expect.stringMatching(/token/i), expect.anything())
  })

  it('persists manual language and theme preferences and offers all six themes', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true }))
    render(<App />)
    await screen.findByRole('heading', { name: /entrar|sign in/i })

    fireEvent.click(screen.getByRole('button', { name: /english|português/i }))
    fireEvent.change(screen.getByLabelText(/tema|theme/i), { target: { value: 'aqua' } })

    expect(localStorage.getItem('athena-language')).toMatch(/pt|en/)
    expect(localStorage.getItem('athena-theme')).toBe('aqua')
    expect(screen.getByLabelText(/tema|theme/i).querySelectorAll('option')).toHaveLength(6)
    expect(document.documentElement.dataset.theme).toBe('aqua')
  })

  it('has no detectable structural accessibility violations on the login screen', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true }))
    const { container } = render(<App />)
    await screen.findByRole('heading', { name: /entrar|sign in/i })

    const result = await axe.run(container, { rules: { 'color-contrast': { enabled: false } } })
    expect(result.violations).toEqual([])
  })
})
