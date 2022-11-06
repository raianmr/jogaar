import { Base } from "./base"

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
