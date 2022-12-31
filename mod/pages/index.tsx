import { useRouter } from "next/router"
import { useEffect } from "react"
import { URLs } from "../data/config"
import { useUser } from "../data/fetching"

export default function Home() {
  const router = useRouter()
  const [user, loggedOut] = useUser()

  useEffect(() => {
    if (loggedOut) {
      router.push(URLs.MOD.LOGIN)
    } else {
      router.push(URLs.MOD.SUPERS)
    }
  })

  return <></>
}
