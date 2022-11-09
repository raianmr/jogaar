import { useRouter } from "next/router"
import { useEffect, useState } from "react"

export default function Home() {
  const router = useRouter()

  const [loggedIn, setloggedIn] = useState(false)

  useEffect(() => {
    if (!loggedIn) router.push("/login")
  })

  return <></>
}
