import { useState } from 'react'
import type { FormEvent } from 'react'

import { createCopy, createPolicy, createReader, createTitle, setVisualTheme } from './api'
import type { MessageCatalog } from './i18n'
import { themes } from './themes'
import type { Theme } from './themes'

type Props = { text: MessageCatalog; theme: Theme; setTheme: (theme: Theme) => void; onLogout: () => void }

export function AdminDashboard({ text, theme, setTheme, onLogout }: Props) {
  const [message, setMessage] = useState('')

  async function readerSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    await createReader(String(data.get('email')), String(data.get('registration')), String(data.get('password')))
    event.currentTarget.reset(); setMessage(text.success)
  }

  async function policySubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    await createPolicy({
      min_loan_days: Number(data.get('minDays')),
      max_loan_days: Number(data.get('maxDays')),
      simultaneous_loan_limit: Number(data.get('loanLimit')),
    })
    setMessage(text.success)
  }

  async function inventorySubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = event.currentTarget
    const data = new FormData(form)
    const internalCode = String(data.get('internalCode'))
    const condition = Number(data.get('condition'))
    data.delete('internalCode'); data.delete('condition')
    if (!data.get('isbn')) data.delete('isbn')
    if (!data.get('page_count')) data.delete('page_count')
    const title = await createTitle(data)
    await createCopy(title.id, internalCode, condition)
    form.reset(); setMessage(text.success)
  }

  async function themeSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const value = String(new FormData(event.currentTarget).get('theme')) as Theme
    const result = await setVisualTheme(value)
    setTheme(result.theme as Theme)
    setMessage(text.success)
  }

  return <div className="dashboard-layout">
    <nav className="main-nav" aria-label={text.menu}><span>{text.administrator}</span><button type="button" onClick={onLogout}>{text.logout}</button></nav>
    <div className="dashboard-content"><h1>{text.administrator}</h1>{message && <p role="status" className="success">{message}</p>}
      <div className="admin-grid"><form className="panel" onSubmit={themeSubmit}><h2>{text.visualIdentity}</h2>
        <label>{text.theme}<select name="theme" defaultValue={theme}>
          {themes.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
        </select></label>
        <button type="submit">{text.applyTheme}</button>
      </form><form className="panel" onSubmit={readerSubmit}><h2>{text.createReader}</h2>
        <label>{text.email}<input name="email" type="email" required /></label>
        <label>{text.registration}<input name="registration" required /></label>
        <label>{text.temporaryPassword}<input name="password" type="password" minLength={15} required /></label>
        <button type="submit">{text.save}</button></form>
      <form className="panel" onSubmit={policySubmit}><h2>{text.policy}</h2>
        <label>{text.minDays}<input name="minDays" type="number" min="1" defaultValue="3" required /></label>
        <label>{text.maxDays}<input name="maxDays" type="number" min="1" defaultValue="15" required /></label>
        <label>{text.loanLimit}<input name="loanLimit" type="number" min="0" defaultValue="3" required /></label>
        <button type="submit">{text.save}</button></form>
      <form className="panel" onSubmit={inventorySubmit}><h2>{text.inventory}</h2>
        <label>Title / Título<input name="name" required /></label>
        <label>Author / Autor<input name="author" required /></label>
        <label>Publisher / Editora<input name="publisher" required /></label>
        <label>Edition / Edição<input name="edition" required /></label>
        <label>Year / Ano<input name="publication_year" type="number" min="1" required /></label>
        <label>Category / Categoria<input name="category" required /></label>
        <label>Description / Descrição<textarea name="description" required /></label>
        <label>Cover / Capa<input name="cover" type="file" accept="image/jpeg,image/png,image/webp" required /></label>
        <label>ISBN<input name="isbn" /></label>
        <label>Pages / Páginas<input name="page_count" type="number" min="1" /></label>
        <label>Internal code / Código<input name="internalCode" required /></label>
        <label>Condition / Conservação<input name="condition" type="number" min="1" max="5" required /></label>
        <button type="submit">{text.save}</button>
      </form></div>
    </div>
  </div>
}
