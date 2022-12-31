export const Env = {
  API: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  WEB: process.env.NEXT_PUBLIC_WEB_URL ?? "http://localhost:3000",
} as const

// TODO user env.local for these
export const URL = {
  API: {
    ROOT: Env.API,
    LOGIN: `${Env.API}/login`,
    MOD: (id: number, status: boolean) =>
      `${Env.API}/users/${id}/mod?status=${status}`,
    BAN: (id: number, status: boolean) =>
      `${Env.API}/users/${id}/ban?status=${status}`,
    MODMINS: `${Env.API}/modmins`,
    GREENLIGHT: (id: number, status: boolean) =>
      `${Env.API}/campaigns/${id}/greenlight?status=${status}`,
    LOCK: (id: number, status: boolean) =>
      `${Env.API}/campaigns/${id}/lock?status=${status}`,
    REPORTS: (id?: number) => `${Env.API}/reports` + (id ? `/${id}` : ""),
    USERS: (id?: number) => `${Env.API}/users` + (id ? `/${id}` : ""),
    CURRENT: `${Env.API}/users/current`,
    CAMPAIGNS: (id?: number) => `${Env.API}/campaigns` + (id ? `/${id}` : ""),
    ENDED: `${Env.API}/campaigns/ended`,
  },
  WEB: {
    ROOT: Env.WEB,
    LOGIN: `${Env.WEB}/login`,
    CAMPAIGNS: (id: number) => `${Env.WEB}/campaigns/${id}`,
    USERS: (id: number) => `${Env.WEB}/users/${id}`,
  },
} as const
