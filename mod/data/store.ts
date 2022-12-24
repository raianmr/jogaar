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

const TOKEN_STORE_KEY = "jwt"

export type TokenData = {
  access_token: string
  token_type: string
}

export type LoginData = {
  username: string
  password: string
}

export function getToken(): string | null {
  const tokenData = fromStore<TokenData>(TOKEN_STORE_KEY)

  return tokenData !== null ? tokenData.access_token : null
}

export function setToken(data: TokenData): boolean {
  return toStore(TOKEN_STORE_KEY, data)
}

// export function useToken() {
//   const [token, _] = useState(() => getToken())
// }
