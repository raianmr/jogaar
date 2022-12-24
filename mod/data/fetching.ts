import useSWR, { Fetcher } from "swr"

import { User } from "./models"
import * as store from "./store"

// TODO user env.local for these
const ROOT = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
const API_URLs = {
  LOGIN: `${ROOT}/login`,
  CURRENT_USER: `${ROOT}/users/current`,
} as const

export class FetchError extends Error {
  message: string
  response: Response
  data: { detail: [] }

  constructor(msg: string, resp: Response, data: { detail: [] }) {
    super(msg)

    this.name = "FetchError"
    this.message = msg
    this.response = resp
    this.data = data ?? { detail: msg }
  }
}

export const tokenDataFetcher: Fetcher<
  store.TokenData,
  store.LoginData
> = async ({ username, password }) => {
  const resp = await fetch(API_URLs.LOGIN, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${username}&password=${password}`,
  })

  if (!resp.ok) {
    throw new FetchError(resp.statusText, resp, await resp.json())
  }

  return resp.json()
}

export const userFetcher: Fetcher<User, string> = async url => {
  const token = store.getToken()

  const resp = await fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!resp.ok) {
    throw new FetchError(resp.statusText, resp, await resp.json())
  }

  return resp.json()
}

export function useUser(): [User | undefined, boolean] {
  const { data, error } = useSWR<User, FetchError>(
    API_URLs.CURRENT_USER,
    userFetcher
  )

  const loggedOut = error !== undefined

  return [data, loggedOut]
}
