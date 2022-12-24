import useSWR, { Fetcher } from "swr"

import { Campaign, LoginData, Report, State, TokenData, User } from "./models"
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

export const alterState = async (
  campaign_id: number,
  new_state: State,
  status: boolean
): Promise<Campaign> => {
  const resp = await fetch(
    `${ROOT}/campaigns/${campaign_id}/${new_state}?status=${status}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  )
  const data = await resp.json()

  if (!resp.ok) {
    throw new FetchError(resp.statusText, resp, data)
  }

  return data
}

export const alterAccess = async (
  user_id: number,
  new_access: State,
  status: boolean
): Promise<User> => {
  const resp = await fetch(
    `${ROOT}/users/${user_id}/${new_access}?status=${status}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  )
  const data = await resp.json()

  if (!resp.ok) {
    throw new FetchError(resp.statusText, resp, data)
  }

  return data
}

export const dismissReport = async (report_id: number): Promise<void> => {
  const resp = await fetch(`${ROOT}/reports/${report_id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  })
  const data = await resp.json()

  if (!resp.ok) {
    throw new FetchError(resp.statusText, resp, data)
  }

  return data
}
