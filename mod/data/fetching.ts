import { getToken, TokenData } from "./store"
import { User } from "./user"

export class FetchError extends Error {
  resp: Response
  data: { detail: [] }

  constructor({
    message: message,
    resp: resp,
    data: data,
  }: {
    message: string
    resp: Response
    data: { detail: [] }
  }) {
    super(message)

    this.name = "FetchError"
    this.resp = resp
    this.data = data ?? { detail: message }
  }
}

export async function fetchJson<json>(
  input: RequestInfo,
  init?: RequestInit
): Promise<json> {
  const resp = await fetch(input, init)
  const data = await resp.json()

  if (resp.ok) {
    return data
  }

  throw new FetchError({
    message: resp.statusText,
    resp: resp,
    data,
  })
}

export async function fetchCurrentUser(): Promise<User> {
  const data = await fetchJson(
    `${process.env.NEXT_PUBLIC_API_CURRENT_USER_URL}`,
    {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      body: `Bearer ${getToken()}`,
    }
  )

  return data as User
}

export async function fetchTokenData(
  username: string,
  password: string
): Promise<TokenData> {
  const data = await fetchJson(`${process.env.NEXT_PUBLIC_API_LOGIN_URL}`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${username}&password=${password}`,
  })

  return data as TokenData
}
