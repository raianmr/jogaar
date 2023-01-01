import { useToast } from "@chakra-ui/react"
import Link from "next/link"
import { useRouter } from "next/router"
import { useEffect } from "react"
import { URLs } from "../data/config"
import { useCampaigns, useUser } from "../data/fetching"

export default function Campaigns() {
  const toast = useToast()
  const router = useRouter()
  const [user, loggedOut] = useUser()
  const [campaigns, errored] = useCampaigns()

  useEffect(() => {
    // TODO fix the issue of this getting called multiple times occasionally
    if (loggedOut && !user) {
      toast({
        title: "session error",
        description: "try logging in again",
        status: "info",
        duration: 3000,
        isClosable: true,
      })

      router.push(URLs.MOD.LOGIN)
    }
  })

  if (loggedOut) return <></>

  return (
    <main>
      <Link href="/">
        <Link href="/">{JSON.stringify(campaigns)}</Link>
      </Link>
    </main>
  )
}
