import Link from "next/link"
import { useUser } from "../data/fetching"
import styles from "../styles/Dashboard.module.css"

export default function Home() {
  const [user, loggedOut] = useUser()

  return (
    <main className={styles.container}>
      <Link href="/">
        {JSON.stringify(user)}
        {loggedOut}
      </Link>
    </main>
  )
}
