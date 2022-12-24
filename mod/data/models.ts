export type Base = {
  id: number
  created_at: Date
}

export type State = "draft" | "started" | "ended" | "locked" | "greenlit"

export type Campaign = Base & {
  campaigner_id: number

  title: string
  description: string
  challenges: string

  goal: number
  pledged: number
  deadline: Date

  current_state: State
}

export type Access = "banned" | "normal" | "mod" | "admin"

export type User = Base & {
  name: string
  email: string

  about: string
  contact: string
  address: string

  access_level: Access
}
