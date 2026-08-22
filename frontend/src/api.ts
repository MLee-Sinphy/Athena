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
    response = await fetch(`${apiBaseUrl}${path}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
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

export async function checkHealth() {
  await request('/health/')
}

export async function login(identifier: string, password: string) {
  const response = await request('/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ identifier, password }),
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
  tags: string[]
  available_copies: number
}

export async function getCatalog(query = ''): Promise<CatalogTitle[]> {
  const search = query ? `?q=${encodeURIComponent(query)}` : ''
  const response = await request(`/catalog/titles/${search}`)
  const result = await response.json() as { results: CatalogTitle[] }
  return result.results
}
