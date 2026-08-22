import type { Language, MessageCatalog } from './i18n'
import { themes } from './themes'
import type { Theme } from './themes'

type Props = {
  language: Language
  setLanguage: (language: Language) => void
  theme: Theme
  setTheme: (theme: Theme) => void
  text: MessageCatalog
}

export function Preferences({ language, setLanguage, theme, setTheme, text }: Props) {
  return (
    <div className="preferences" aria-label="Preferences">
      <button type="button" className="text-button" onClick={() => setLanguage(language === 'pt' ? 'en' : 'pt')}>
        {text.language}
      </button>
      <label className="theme-picker">
        <span>{text.theme}</span>
        <select value={theme} onChange={(event) => setTheme(event.target.value as Theme)}>
          {themes.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
        </select>
      </label>
    </div>
  )
}
