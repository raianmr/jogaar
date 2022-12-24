import { TokenData } from "./models"

export function toStore<T>(key: string, value: T): boolean {
  try {
    window.localStorage.setItem(key, JSON.stringify(value))
    return true
  } catch {
    return false
  }
}

export function fromStore<T>(key: string): T | null {
  const value = window.localStorage.getItem(key)

  if (value === null) {
    return null
  }

  try {
    const obj = JSON.parse(value) as T
    return obj
  } catch {
    return null
  }
}

export function clearStore() {
  window.localStorage.clear()
}

const TOKEN_STORE_KEY = "jwt"

export function getToken(): string | null {
  const tokenData = fromStore<TokenData>(TOKEN_STORE_KEY)

  return tokenData !== null ? tokenData.access_token : null
}

export function setToken(data: TokenData): boolean {
  return toStore(TOKEN_STORE_KEY, data)
}
