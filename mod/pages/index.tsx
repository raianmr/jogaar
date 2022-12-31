import { useRouter } from "next/router"
import { useEffect } from "react"
import { useUser } from "../data/fetching"

export default function Home() {
  const router = useRouter()
  const [user, loggedOut] = useUser()

  useEffect(() => {
    if (loggedOut) {
      router.push("/login")
    } else {
      router.push("/supers")
    }
  })

  return <></>
}
