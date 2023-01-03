import { Center, Container, Heading, useToast } from "@chakra-ui/react"
import Link from "next/link"
import { useRouter } from "next/router"
import { useEffect } from "react"
import { URLs } from "../data/config"
import { useReports, useUser } from "../data/fetching"


export default function Reports() {
  const toast = useToast()
  const router = useRouter()
  const [user, loggedOut] = useUser()
  const [reports, errored] = useReports()

  useEffect(() => {
    if (loggedOut) router.push(URLs.MOD.LOGIN)
  })

  if (loggedOut) return <></>

  return (
    <Center>
      <Heading fontSize="24px" fontWeight="medium" textAlign="center" mt="40px">
        User Reports
      </Heading>
      <Container maxW="lg" px={4} py={10}></Container>
    </Center>
  )

  return (
    <main>
      <Link href="/">{JSON.stringify(reports)}</Link>
    </main>
  )
}
