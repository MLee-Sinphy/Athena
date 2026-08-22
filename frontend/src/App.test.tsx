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
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ status: 'ok', service: 'athena-api', theme: 'calculus' }),
    }))
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
      .mockResolvedValueOnce({
        ok: true, json: async () => ({ status: 'ok', service: 'athena-api', theme: 'calculus' }),
      })
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

  it('persists the manual language while the institution controls the theme', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ status: 'ok', service: 'athena-api', theme: 'aqua' }),
    }))
    render(<App />)
    await screen.findByRole('heading', { name: /entrar|sign in/i })

    fireEvent.click(screen.getByRole('button', { name: /english|português/i }))

    expect(localStorage.getItem('athena-language')).toMatch(/pt|en/)
    expect(localStorage.getItem('athena-theme')).toBeNull()
    expect(screen.queryByLabelText(/tema|theme/i)).not.toBeInTheDocument()
    expect(document.documentElement.dataset.theme).toBe('aqua')
  })

  it('allows an administrator to apply one of six themes globally', async () => {
    let selectedTheme = 'calculus'
    vi.stubGlobal('fetch', vi.fn(async (input: string | URL | Request, init?: RequestInit) => {
      const url = String(input)
      if (url.endsWith('/health/')) return {
        ok: true, json: async () => ({ status: 'ok', service: 'athena-api', theme: selectedTheme }),
      }
      if (url.endsWith('/auth/login/')) return {
        ok: true, json: async () => ({ access_token: 'admin-token', must_change_password: false }),
      }
      if (url.endsWith('/auth/me/')) return {
        ok: true, json: async () => ({ id: 2, email: 'admin@example.com', role: 'administrator' }),
      }
      if (url.endsWith('/admin/configuration/visual/') && init?.method === 'PATCH') {
        selectedTheme = JSON.parse(String(init.body)).theme
        return { ok: true, json: async () => ({ theme: selectedTheme }) }
      }
      return { ok: false, status: 404 }
    }))
    render(<App />)
    fireEvent.change(await screen.findByLabelText(/e-mail ou matrícula|email or registration/i), {
      target: { value: 'admin@example.com' },
    })
    fireEvent.change(screen.getByLabelText(/^senha$|^password$/i), {
      target: { value: 'a valid administrative passphrase' },
    })
    fireEvent.click(screen.getByRole('button', { name: /entrar|sign in/i }))

    const selector = await screen.findByLabelText(/tema visual|visual theme/i)
    expect(selector.querySelectorAll('option')).toHaveLength(6)
    fireEvent.change(selector, { target: { value: 'aqua' } })
    fireEvent.click(screen.getByRole('button', { name: /aplicar tema|apply theme/i }))

    expect(await screen.findByRole('status')).toBeVisible()
    expect(document.documentElement.dataset.theme).toBe('aqua')
  })

  it('has no detectable structural accessibility violations on the login screen', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ status: 'ok', service: 'athena-api', theme: 'calculus' }),
    }))
    const { container } = render(<App />)
    await screen.findByRole('heading', { name: /entrar|sign in/i })

    const result = await axe.run(container, { rules: { 'color-contrast': { enabled: false } } })
    expect(result.violations).toEqual([])
  })
})
