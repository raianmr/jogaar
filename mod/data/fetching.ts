import useSWR, { Fetcher } from "swr"

import { URL } from "./config"
import { Campaign, LoginData, Report, TokenData, User } from "./models"
import { getToken } from "./store"

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

export const fetchTokenData: Fetcher<TokenData, LoginData> = async creds => {
  const resp = await fetch(URL.API.SUPER_LOGIN, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${creds.username}&password=${creds.password}`,
  })

  if (!resp.ok) {
    throw new FetchError(resp.statusText, resp, await resp.json())
  }

  return resp.json()
}

const fetch_: Fetcher<any, string> = async <T>(url: string): Promise<T> => {
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

const useResource = <T>(url: string): [T | undefined, boolean] => {
  const { data, error } = useSWR<T, FetchError>(url, fetch_)

  return [data, error !== undefined]
}

export const useUser = () => useResource<User>(URL.API.CURRENT)
export const useSupers = () => useResource<User[]>(URL.API.SUPERS)
export const useCampaigns = () => useResource<Campaign[]>(URL.API.ENDED)
export const useReports = () => useResource<Report[]>(URL.API.REPORTS())

const mutate = async <T = void>(
  url: string,
  method: "POST" | "PUT" | "DELETE" = "POST"
): Promise<T> => {
  const resp = await fetch(url, {
    method,
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  })
  const data = await resp.json()

  if (!resp.ok) {
    throw new FetchError(resp.statusText, resp, data)
  }

  return data as T
}

export const greenlight = (campaignID: number) =>
  mutate(URL.API.GREENLIGHT(campaignID, true))
export const ungreenlight = (campaignID: number) =>
  mutate(URL.API.GREENLIGHT(campaignID, false))

export const lock = (campaignID: number) =>
  mutate(URL.API.LOCK(campaignID, true))
export const unlock = (campaignID: number) =>
  mutate(URL.API.LOCK(campaignID, false))

export const promote = (userID: number) =>
  mutate(URL.API.GREENLIGHT(userID, true))
export const demote = (userID: number) =>
  mutate(URL.API.GREENLIGHT(userID, false))

export const ban = (userID: number) => mutate(URL.API.LOCK(userID, true))
export const unban = (userID: number) => mutate(URL.API.LOCK(userID, false))

export const dismiss = (reportID: number) =>
  mutate(URL.API.REPORTS(reportID), "DELETE")
