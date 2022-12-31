import Link from "next/link"
import { useRouter } from "next/router"
import { useEffect } from "react"
import { URLs } from "../data/config"
import { useSupers, useUser } from "../data/fetching"

export default function Supers() {
  const router = useRouter()
  const [user, loggedOut] = useUser()
  const [supers, errored] = useSupers()

  useEffect(() => {
    if (loggedOut) router.push(URLs.MOD.LOGIN)
  })

  return (
    <main>
      <Link href="/">{JSON.stringify(supers)}</Link>
    </main>
  )
}
