import Link from "next/link"
import { useRouter } from "next/router"
import { useEffect } from "react"
import { useCampaigns, useUser } from "../data/fetching"

export default function Campaigns() {
  const router = useRouter()
  const [user, loggedOut] = useUser()
  const [campaigns, errored] = useCampaigns()

  useEffect(() => {
    if (loggedOut) router.push("/login")
  })

  return (
    <main>
      <Link href="/">
        <Link href="/">{JSON.stringify(campaigns)}</Link>
      </Link>
    </main>
  )
}
