export const themes = [
  ['calculus', 'Calculus'], ['ocean', 'Oceano / Ocean'], ['wine', 'Vinho / Wine'],
  ['slate', 'Ardósia / Slate'], ['indigo', 'Índigo / Indigo'], ['aqua', 'Aqua Glass'],
] as const

export type Theme = typeof themes[number][0]

export const themePalettes: Record<Theme, { primary: string; background: string; text: string; onPrimary: string }> = {
  calculus: { primary: '#111827', background: '#faf9f6', text: '#202124', onPrimary: '#ffffff' },
  ocean: { primary: '#0f3d3e', background: '#f4f7f6', text: '#172626', onPrimary: '#ffffff' },
  wine: { primary: '#3b1021', background: '#fbf7ef', text: '#2b1c20', onPrimary: '#ffffff' },
  slate: { primary: '#243447', background: '#f5f7f2', text: '#202a31', onPrimary: '#ffffff' },
  indigo: { primary: '#1e1b4b', background: '#f8fafc', text: '#1e2030', onPrimary: '#ffffff' },
  aqua: { primary: '#0b3b60', background: '#eaf7fb', text: '#102d3f', onPrimary: '#ffffff' },
}
