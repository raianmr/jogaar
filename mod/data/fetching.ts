import useSWR, { Fetcher } from "swr"

import { Campaign, LoginData, Report, TokenData, User } from "./models"
import { getToken } from "./store"

// TODO user env.local for these
const ROOT = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
const API_URLs = {
  LOGIN: `${ROOT}/login`,
  CURRENT_USER: `${ROOT}/users/current`,
  MODMINS: `${ROOT}/modmins`,
  ENDED_CAMPAIGNS: `${ROOT}/campaigns/ended`,
  REPORTS: `${ROOT}/reports`,
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

export const tokenDataFetcher: Fetcher<TokenData, LoginData> = async creds => {
  const resp = await fetch(API_URLs.LOGIN, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${creds.username}&password=${creds.password}`,
  })

  if (!resp.ok) {
    throw new FetchError(resp.statusText, resp, await resp.json())
  }

  return resp.json()
}

export const miscFetcher: Fetcher<any, string> = async <T>(
  url: string
): Promise<T> => {
  const resp = await fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  })

  if (!resp.ok) {
    throw new FetchError(resp.statusText, resp, await resp.json())
  }

  return resp.json()
}

export const useMisc = <T>(url: string): [T | undefined, boolean] => {
  const { data, error } = useSWR<T, FetchError>(url, miscFetcher)

  return [data, error !== undefined]
}

export const useUser = () => useMisc<User>(API_URLs.CURRENT_USER)
export const useModmins = () => useMisc<User[]>(API_URLs.MODMINS)
export const useCampaigns = () => useMisc<Campaign[]>(API_URLs.ENDED_CAMPAIGNS)
export const useReports = () => useMisc<Report[]>(API_URLs.REPORTS)
