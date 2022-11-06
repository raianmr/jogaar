import { Base } from "./base"

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
