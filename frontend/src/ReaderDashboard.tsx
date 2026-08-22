import { useState } from 'react'
import type { FormEvent } from 'react'

import {
  cancelReservation,
  checkoutReservation,
  createReservation,
  getCatalog,
  respondNotice,
  renewLoan,
  returnLoan,
  submitFeedback,
} from './api'
import type { CatalogTitle, Loan, Notice, Profile, Reservation } from './api'
import type { MessageCatalog } from './i18n'

type Section = 'catalog' | 'reservations' | 'loans' | 'notices' | 'profile'
type Props = {
  text: MessageCatalog
  profile: Profile
  initialTitles: CatalogTitle[]
  initialReservations: Reservation[]
  initialNotices: Notice[]
  initialLoans: Loan[]
  onLogout: () => void
}

export function ReaderDashboard(props: Props) {
  const { text, profile, onLogout } = props
  const [section, setSection] = useState<Section>('catalog')
  const [titles, setTitles] = useState(props.initialTitles)
  const [reservations, setReservations] = useState(props.initialReservations)
  const [notices, setNotices] = useState(props.initialNotices)
  const [loans, setLoans] = useState(props.initialLoans)
  const [selectedTitle, setSelectedTitle] = useState<CatalogTitle | null>(null)
  const [message, setMessage] = useState('')

  async function search(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setTitles(await getCatalog(String(new FormData(event.currentTarget).get('query'))))
  }

  async function reserve(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!selectedTitle) return
    const data = new FormData(event.currentTarget)
    const created = await createReservation(
      selectedTitle.id, String(data.get('startDate')), String(data.get('endDate')),
    )
    setReservations((current) => [...current, created])
    setSelectedTitle(null)
    setMessage(text.success)
  }

  async function removeReservation(id: number) {
    await cancelReservation(id)
    setReservations((current) => current.map((item) => item.id === id ? { ...item, state: 'cancelled' } : item))
  }

  async function answerNotice(id: number, response: 'accepted' | 'declined') {
    const changed = await respondNotice(id, response)
    setNotices((current) => current.map((item) => item.id === id ? changed : item))
  }

  async function checkout(id: number) {
    const loan = await checkoutReservation(id)
    setLoans((current) => [loan, ...current])
    setMessage(text.success)
  }

  async function finishLoan(id: number) {
    const changed = await returnLoan(id)
    setLoans((current) => current.map((loan) => loan.id === id ? changed : loan))
  }

  async function loanAction(event: FormEvent<HTMLFormElement>, loan: Loan) {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    if (loan.returned_on) {
      await submitFeedback(
        loan.id, Number(data.get('titleScore')) || undefined,
        Number(data.get('copyScore')) || undefined,
        String(data.get('tags')).split(',').map((tag) => tag.trim()).filter(Boolean),
      )
    } else {
      const changed = await renewLoan(loan.id, String(data.get('dueDate')))
      setLoans((current) => current.map((item) => item.id === loan.id ? changed : item))
    }
    setMessage(text.success)
  }

  const navigation = [
    ['catalog', text.catalog], ['reservations', text.reservations], ['loans', text.loans],
    ['notices', text.notices], ['profile', text.profile],
  ] as const

  return (
    <div className="dashboard-layout">
      <nav className="main-nav" aria-label={text.menu}>
        {navigation.map(([value, label]) => (
          <button key={value} type="button" aria-current={section === value ? 'page' : undefined} onClick={() => setSection(value)}>
            {label}{value === 'notices' && notices.some((notice) => !notice.response) ? ' •' : ''}
          </button>
        ))}
        <button type="button" onClick={onLogout}>{text.logout}</button>
      </nav>
      <div className="dashboard-content">
        {message && <p className="success" role="status">{message}</p>}
        {section === 'catalog' && <>
          <h1>{text.catalog}</h1>
          <form className="search" role="search" onSubmit={search}>
            <label><span>{text.search}</span><input name="query" type="search" /></label>
            <button type="submit">{text.searchButton}</button>
          </form>
          <div className="book-grid">
            {titles.length === 0 && <p>{text.empty}</p>}
            {titles.map((title) => <article className="book-card" key={title.id}>
              {title.cover ? <img src={title.cover} alt="" loading="lazy" /> : <div className="cover-placeholder" aria-hidden="true" />}
              <div><p className="meta">{title.category}</p><h2>{title.name}</h2><p>{title.author}</p>
                <p>{title.available_copies} {text.available}</p><p>{title.tags.map((tag) => `#${tag}`).join(' ')}</p>
                <button type="button" onClick={() => setSelectedTitle(title)}>{text.reserve}</button>
              </div>
            </article>)}
          </div>
          {selectedTitle && <form className="panel" onSubmit={reserve}>
            <h2>{selectedTitle.name}</h2>
            <label>{text.startDate}<input name="startDate" type="date" required /></label>
            <label>{text.endDate}<input name="endDate" type="date" required /></label>
            <div className="actions"><button type="submit">{text.reserve}</button><button type="button" className="secondary" onClick={() => setSelectedTitle(null)}>{text.cancel}</button></div>
          </form>}
        </>}
        {section === 'reservations' && <section><h1>{text.reservations}</h1>
          {reservations.length === 0 && <p>{text.empty}</p>}
          <div className="card-list">{reservations.map((reservation) => <article className="panel" key={reservation.id}>
            <h2>#{reservation.id}</h2><p>{text.status}: {reservation.state}</p>
            <p>{reservation.start_date} — {reservation.end_date}</p>
            {reservation.queue_position && <p>{text.queue}: {reservation.queue_position}</p>}
            {!['cancelled', 'completed'].includes(reservation.state) && <button type="button" className="danger" onClick={() => void removeReservation(reservation.id)}>{text.cancel}</button>}
            {reservation.state === 'confirmed' && <button type="button" onClick={() => void checkout(reservation.id)}>{text.checkout}</button>}
          </article>)}</div>
        </section>}
        {section === 'loans' && <section><h1>{text.loans}</h1>
          {loans.length === 0 && <p>{text.empty}</p>}
          <div className="card-list">{loans.map((loan) => <article className="panel" key={loan.id}>
            <h2>#{loan.id}</h2><p>{loan.due_date}</p>
            {!loan.returned_on && <button type="button" onClick={() => void finishLoan(loan.id)}>{text.returnBook}</button>}
            <form onSubmit={(event) => void loanAction(event, loan)}>
              {loan.returned_on ? <>
                <label>{text.titleScore}<input name="titleScore" type="number" min="1" max="5" /></label>
                <label>{text.copyScore}<input name="copyScore" type="number" min="1" max="5" /></label>
                <label>{text.tags}<input name="tags" /></label><button type="submit">{text.feedback}</button>
              </> : <><label>{text.endDate}<input name="dueDate" type="date" required /></label><button type="submit">{text.renew}</button></>}
            </form>
          </article>)}</div>
        </section>}
        {section === 'notices' && <section><h1>{text.notices}</h1>
          {notices.length === 0 && <p>{text.empty}</p>}
          <div className="card-list">{notices.map((notice) => <article className="panel" key={notice.id}>
            <h2>{notice.kind.replaceAll('_', ' ')}</h2><p>{notice.response || text.status}</p>
            {!notice.response && <div className="actions"><button type="button" onClick={() => void answerNotice(notice.id, 'accepted')}>{text.accepted}</button><button type="button" className="secondary" onClick={() => void answerNotice(notice.id, 'declined')}>{text.declined}</button></div>}
          </article>)}</div>
        </section>}
        {section === 'profile' && <section><h1>{text.profile}</h1><div className="panel"><p>{profile.email}</p><p>{profile.registration_id}</p></div></section>}
      </div>
    </div>
  )
}
