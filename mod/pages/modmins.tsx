import Link from "next/link"
import { useRouter } from "next/router"
import { useEffect } from "react"
import { useModmins, useUser } from "../data/fetching"
import styles from "../styles/Dashboard.module.css"

export default function Modmins() {
  const router = useRouter()
  const [user, loggedOut] = useUser()
  const [modmins, errored] = useModmins()

  useEffect(() => {
    if (loggedOut) router.push("/login")
  })

  return (
    <main className={styles.container}>
      <Link href="/">{JSON.stringify(modmins)}</Link>
    </main>
  )
}
