export const Env = {
  API: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  WEB: process.env.NEXT_PUBLIC_WEB_URL ?? "http://localhost:3000",
} as const

// TODO user env.local for these
export const URLs = {
  API: {
    ROOT: Env.API,
    OPENAPI: `${Env.API}/openapi.json`,
    SWAGGER: `${Env.API}/docs`,
    STATIC: `${Env.API}/static`,
    SUPER_LOGIN: `${Env.API}/login/super`,
    MOD: (id: number, status: boolean) =>
      `${Env.API}/users/${id}/mod?status=${status}`,
    BAN: (id: number, status: boolean) =>
      `${Env.API}/users/${id}/ban?status=${status}`,
    SUPERS: `${Env.API}/super`,
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
    CATALOGUE: `${Env.WEB}/catalogue`,
    LOGIN: `${Env.WEB}/login`,
    CAMPAIGNS: (id: number) => `${Env.WEB}/campaigns/${id}`,
    USERS: (id: number) => `${Env.WEB}/users/${id}`,
  },
  MOD: {
    LOGIN: "/login",
    SUPERS: "/supers",
    CAMPAIGNS: "/campaigns",
    REPORTS: "/reports",
    RESET: "/reset",
  },
} as const
