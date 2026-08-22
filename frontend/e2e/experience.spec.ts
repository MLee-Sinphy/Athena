import AxeBuilder from '@axe-core/playwright'
import { expect, test } from '@playwright/test'

async function mockApi(page: import('@playwright/test').Page) {
  await page.route('http://localhost:8000/api/v1/**', async (route) => {
    const path = new URL(route.request().url()).pathname
    const bodies: Record<string, unknown> = {
      '/api/v1/health/': { status: 'ok', service: 'athena-api', theme: 'calculus' },
      '/api/v1/auth/login/': { access_token: 'opaque-test-token', must_change_password: false },
      '/api/v1/auth/me/': { id: 1, email: 'reader@example.com', registration_id: 'READER-001', role: 'reader' },
      '/api/v1/catalog/titles/': { results: [{ id: 1, name: 'O Nome da Rosa', author: 'Umberto Eco', category: 'Mistério', description: 'Abadia medieval', cover: '', tags: ['medieval'], available_copies: 2 }] },
      '/api/v1/reservations/': { results: [] },
      '/api/v1/notices/': { results: [] },
      '/api/v1/loans/': { results: [] },
    }
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(bodies[path] ?? {}) })
  })
}

for (const viewport of [{ width: 320, height: 700 }, { width: 1440, height: 900 }]) {
  test(`reader journey works at ${viewport.width}px`, async ({ page }) => {
    await page.setViewportSize(viewport)
    await mockApi(page)
    await page.goto('/')
    await page.getByLabel(/e-mail|email/i).fill('reader@example.com')
    await page.getByLabel(/^password$|^senha$/i).fill('a valid library passphrase')
    await page.getByRole('button', { name: /sign in|entrar/i }).click()

    await expect(page.getByRole('heading', { name: /catalog|catálogo/i })).toBeVisible()
    await expect(page.getByText('O Nome da Rosa')).toBeVisible()
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)
    expect(overflow).toBe(false)
  })
}

test('login and preferences meet automated accessibility rules', async ({ page }) => {
  await mockApi(page)
  await page.goto('/')
  const results = await new AxeBuilder({ page }).analyze()
  expect(results.violations).toEqual([])
})
