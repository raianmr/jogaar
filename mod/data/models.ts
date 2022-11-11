export interface Base {
  id: number
  created_at: Date
}

export enum State {
  DRAFT = "draft",
  STARTED = "started",
  ENDED = "ended",
  LOCKED = "locked",
  GREENLIT = "greenlit",
}

export interface Campaign extends Base {
  campaigner_id: number

  title: string
  description: string
  challenges: string

  goal: number
  pledged: number
  deadline: Date

  current_state: State
}

export enum Access {
  BANNED = "banned",
  NORMAL = "normal",
  MOD = "mod",
  ADMIN = "admin",
}

export interface User extends Base {
  name: string
  email: string
  about: string
  contact: string
  address: string

  access_level: Access
}
