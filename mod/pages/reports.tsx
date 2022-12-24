import Link from "next/link"
import { useRouter } from "next/router"
import { useEffect } from "react"
import { useReports, useUser } from "../data/fetching"
import styles from "../styles/Dashboard.module.css"

export default function Reports() {
  const router = useRouter()
  const [user, loggedOut] = useUser()
  const [reports, errored] = useReports()

  useEffect(() => {
    if (loggedOut) router.push("/login")
  })

  return (
    <main className={styles.container}>
      <Link href="/">{JSON.stringify(reports)}</Link>
    </main>
  )
}
