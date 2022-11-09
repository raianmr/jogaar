export function toStore(k: string, v: any) {
  window.localStorage.setItem(k, JSON.stringify(v))
}

export function fromStore<T>(k: string): T {
  const obj = window.localStorage.getItem(k)

  return obj ? JSON.parse(obj) : {}
}

const TOKEN_STORE_KEY = "jwt"

export interface TokenData {
  access_token: string
  token_type: string
}

export function getToken(): string {
  return fromStore<TokenData>(TOKEN_STORE_KEY).access_token
}

export function setToken(data: TokenData) {
  toStore(TOKEN_STORE_KEY, data)
}
