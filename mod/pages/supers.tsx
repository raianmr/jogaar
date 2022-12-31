import Link from "next/link"
import { useRouter } from "next/router"
import { useEffect } from "react"
import { useSupers, useUser } from "../data/fetching"
import styles from "../styles/Dashboard.module.css"

export default function Supers() {
  const router = useRouter()
  const [user, loggedOut] = useUser()
  const [supers, errored] = useSupers()

  useEffect(() => {
    if (loggedOut) router.push("/login")
  })

  return (
    <main className={styles.container}>
      <Link href="/">{JSON.stringify(supers)}</Link>
    </main>
  )
}
