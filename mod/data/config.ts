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

    STATIC: (location: string) => `${Env.API}/${location}`,
    IMAGE: (id: number) => `${Env.API}/images/${id}`,

    LOGIN: `${Env.API}/login/super`,
    CURRENT: `${Env.API}/users/current`,
    MOD: (id: number, status: boolean) =>
      `${Env.API}/users/${id}/mod?status=${status}`,
    BAN: (id: number, status: boolean) =>
      `${Env.API}/users/${id}/ban?status=${status}`,

    GREENLIGHT: (id: number, status: boolean) =>
      `${Env.API}/campaigns/${id}/greenlight?status=${status}`,
    LOCK: (id: number, status: boolean) =>
      `${Env.API}/campaigns/${id}/lock?status=${status}`,

    USER: (id: number) => `${Env.API}/users/${id}`,
    USERS: (limit: number, offset: number) =>
      `${Env.API}/users?limit=${limit}&offset=${offset}`,
    SUPERS: (limit: number, offset: number) =>
      `${Env.API}/super?limit=${limit}&offset=${offset}`,

    CAMPAIGN: (id: number) => `${Env.API}/campaigns/${id}`,
    CAMPAIGNS: (limit: number, offset: number) =>
      `${Env.API}/campaigns?limit=${limit}&offset=${offset}`,
    ENDED: (limit: number, offset: number) =>
      `${Env.API}/campaigns/ended?limit=${limit}&offset=${offset}`,

    REPORT: (id: number) => `${Env.API}/reports/${id}`,
    REPORTS: (limit: number, offset: number) =>
      `${Env.API}/reports?limit=${limit}&offset=${offset}`,
  },

  WEB: {
    ROOT: Env.WEB,
    CATALOGUE: `${Env.WEB}/catalogue`,
    LOGIN: `${Env.WEB}/login`,
    CAMPAIGN: (id: number) => `${Env.WEB}/campaigns/${id}`,
    PROFILE: (id: number) => `${Env.WEB}/users/${id}`,
  },

  MOD: {
    LOGIN: "/login",
    SUPERS: "/supers",
    CAMPAIGNS: "/campaigns",
    REPORTS: "/reports",
  },
} as const
