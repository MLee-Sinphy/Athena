const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

let accessToken: string | null = null

export class ApiError extends Error {
  readonly status: number

  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function request(path: string, init: RequestInit = {}) {
  let response: Response
  try {
    const isFormData = init.body instanceof FormData
    response = await fetch(`${apiBaseUrl}${path}`, {
      ...init,
      headers: {
        ...(!isFormData ? { 'Content-Type': 'application/json' } : {}),
        ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        ...init.headers,
      },
    })
  } catch {
    throw new ApiError(0, 'backend_unavailable')
  }
  if (!response.ok) {
    throw new ApiError(response.status, response.status === 401 ? 'invalid_credentials' : 'request_failed')
  }
  return response
}

async function jsonRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await request(path, init)
  return response.json() as Promise<T>
}

export async function checkHealth() {
  return jsonRequest<{ status: string; service: string; theme: string }>('/health/')
}

export async function setVisualTheme(theme: string) {
  return jsonRequest<{ theme: string }>('/admin/configuration/visual/', {
    method: 'PATCH', body: JSON.stringify({ theme }),
  })
}

export async function login(identifier: string, password: string, role: 'reader' | 'administrator') {
  const response = await request('/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ identifier, password, role }),
  })
  const result = await response.json() as {
    access_token: string
    must_change_password: boolean
  }
  accessToken = result.access_token
  return result
}

export async function changePassword(currentPassword: string, newPassword: string) {
  await request('/auth/password/change/', {
    method: 'POST',
    body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
  })
  accessToken = null
}

export async function logout() {
  try {
    await request('/auth/logout/', { method: 'POST' })
  } finally {
    accessToken = null
  }
}

export type CatalogTitle = {
  id: number
  name: string
  author: string
  category: string
  description: string
  cover: string
  isbn: string
  metadata_source_url: string
  tags: string[]
  available_copies: number
}

export async function getCatalog(query = ''): Promise<CatalogTitle[]> {
  const search = query ? `?q=${encodeURIComponent(query)}` : ''
  const response = await request(`/catalog/titles/${search}`)
  const result = await response.json() as { results: CatalogTitle[] }
  return result.results
}

export type Profile = {
  id: number
  email: string
  registration_id: string
  whatsapp_number: string
  role: 'reader' | 'administrator'
}

export type Reservation = {
  id: number
  title: number
  copy: number | null
  start_date: string
  end_date: string
  state: string
  queue_position: number | null
}

export type Notice = {
  id: number
  kind: string
  payload: Record<string, unknown>
  response: string
}

export type Loan = {
  id: number
  reservation: number
  checked_out_at: string
  due_date: string
  returned_on: string | null
}

export const getProfile = () => jsonRequest<Profile>('/auth/me/')
export const getReservations = async () =>
  (await jsonRequest<{ results: Reservation[] }>('/reservations/')).results
export const getNotices = async () =>
  (await jsonRequest<{ results: Notice[] }>('/notices/')).results
export const getLoans = async () => (await jsonRequest<{ results: Loan[] }>('/loans/')).results

export async function createReservation(title: number, startDate: string, endDate: string) {
  return jsonRequest<Reservation>('/reservations/', {
    method: 'POST',
    body: JSON.stringify({ title, start_date: startDate, end_date: endDate }),
  })
}

export async function cancelReservation(id: number) {
  await request(`/reservations/${id}/`, { method: 'DELETE' })
}

export async function respondNotice(id: number, response: 'accepted' | 'declined') {
  return jsonRequest<Notice>(`/notices/${id}/respond/`, {
    method: 'POST',
    body: JSON.stringify({ response }),
  })
}

export async function createReader(email: string, registrationId: string, temporaryPassword: string, whatsappNumber = '') {
  return jsonRequest<Profile>('/admin/users/', {
    method: 'POST',
    body: JSON.stringify({
      email,
      registration_id: registrationId,
      whatsapp_number: whatsappNumber,
      temporary_password: temporaryPassword,
    }),
  })
}

export async function createPolicy(data: Record<string, number | boolean>) {
  return jsonRequest('/admin/policies/', { method: 'POST', body: JSON.stringify(data) })
}

export const checkoutReservation = (id: number) =>
  jsonRequest<Loan>(`/reservations/${id}/checkout/`, { method: 'POST' })
export const returnLoan = (id: number) => jsonRequest<Loan>(`/loans/${id}/return/`, { method: 'POST' })
export const renewLoan = (id: number, dueDate: string) =>
  jsonRequest<Loan>(`/loans/${id}/renew/`, { method: 'POST', body: JSON.stringify({ due_date: dueDate }) })
export const submitFeedback = (id: number, titleScore?: number, copyScore?: number, tags: string[] = []) =>
  jsonRequest(`/loans/${id}/feedback/`, {
    method: 'POST', body: JSON.stringify({ title_score: titleScore, copy_score: copyScore, tags }),
  })

export async function createTitle(data: FormData) {
  return jsonRequest<{ id: number }>('/admin/catalog/titles/', { method: 'POST', body: data })
}

export async function createCopy(title: number, internalCode: string, conditionRating: number) {
  return jsonRequest('/admin/catalog/copies/', {
    method: 'POST', body: JSON.stringify({ title, internal_code: internalCode, condition_rating: conditionRating }),
  })
}
