import Link from "next/link"
import { useRouter } from "next/router"
import { useEffect } from "react"
import { useCampaigns, useUser } from "../data/fetching"
import styles from "../styles/Dashboard.module.css"

export default function Campaigns() {
  const router = useRouter()
  const [user, loggedOut] = useUser()
  const [campaigns, errored] = useCampaigns()

  useEffect(() => {
    if (loggedOut) router.push("/login")
  })

  return (
    <main className={styles.container}>
      <Link href="/">
        <Link href="/">{JSON.stringify(campaigns)}</Link>
      </Link>
    </main>
  )
}
