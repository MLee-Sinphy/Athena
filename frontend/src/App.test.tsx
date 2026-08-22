import '@testing-library/jest-dom/vitest'
import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import App from './App'

describe('App', () => {
  it('identifies the Athena bootstrap screen', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: /biblioteca em preparação/i })).toBeVisible()
  })
})
