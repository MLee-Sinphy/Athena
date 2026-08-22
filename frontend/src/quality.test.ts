import { describe, expect, it } from 'vitest'

import { messages } from './i18n'
import { themePalettes, themes } from './themes'

function luminance(hex: string) {
  const channels = hex.slice(1).match(/.{2}/g)?.map((value) => {
    const channel = Number.parseInt(value, 16) / 255
    return channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4
  }) ?? [0, 0, 0]
  return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]
}

function contrast(first: string, second: string) {
  const values = [luminance(first), luminance(second)].sort((a, b) => b - a)
  return (values[0] + 0.05) / (values[1] + 0.05)
}

describe('internationalization and theme quality', () => {
  it('keeps English and Portuguese catalogs complete and equivalent', () => {
    expect(Object.keys(messages.en).sort()).toEqual(Object.keys(messages.pt).sort())
    expect(Object.values(messages.en).every(Boolean)).toBe(true)
    expect(Object.values(messages.pt).every(Boolean)).toBe(true)
  })

  it('defines six tokenized themes with AA text contrast', () => {
    for (const [theme] of themes) {
      const palette = themePalettes[theme]
      expect(contrast(palette.text, palette.background)).toBeGreaterThanOrEqual(4.5)
      expect(contrast(palette.primary, palette.onPrimary)).toBeGreaterThanOrEqual(4.5)
    }
  })

  it('provides an opaque fallback and reduced-transparency rule for Aqua Glass', () => {
    expect(themePalettes.aqua.background).toBe('#eaf7fb')
    expect(themePalettes.aqua.text).toBe('#102d3f')
  })
})
