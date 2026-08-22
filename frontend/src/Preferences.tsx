import type { Language, MessageCatalog } from './i18n'

type Props = {
  language: Language
  setLanguage: (language: Language) => void
  text: MessageCatalog
}

export function Preferences({ language, setLanguage, text }: Props) {
  return (
    <div className="preferences" aria-label="Preferences">
      <button type="button" className="text-button" onClick={() => setLanguage(language === 'pt' ? 'en' : 'pt')}>
        {text.language}
      </button>
    </div>
  )
}
