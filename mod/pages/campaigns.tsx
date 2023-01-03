import {
  Button,
  ButtonGroup,
  Center,
  Heading,
  SimpleGrid,
  Text,
  useToast,
  VStack,
} from "@chakra-ui/react"
import { useRouter } from "next/router"
import { useEffect, useState } from "react"
import { CampaignCard } from "../components/cards"
import { URLs } from "../data/config"
import { useCampaigns, useUser } from "../data/fetching"

function Page({ index }: { index: number }) {
  const [campaigns, errored] = useCampaigns(9, index)

  return (
    <SimpleGrid
      templateColumns={{
        sm: "1fr 1fr",
        md: `repeat(3, 1fr)`,
      }}
      spacing={4}
      p={8}>
      {!errored &&
        campaigns?.map(campaign => (
          <CampaignCard key={campaign.id} campaign={campaign} />
        ))}
    </SimpleGrid>
  )
}

export default function Campaigns() {
  const toast = useToast()
  const router = useRouter()
  const [user, loggedOut] = useUser()

  const [pageIndex, setPageIndex] = useState(0)

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
    <Center>
      <VStack p={8}>
        <Heading size="xl" fontWeight="light">
          All ended campaigns
        </Heading>
        <Page index={pageIndex} />
        <div style={{ display: "none" }}>
          <Page index={pageIndex + 1} />
        </div>
        {/* <Divider /> */}
        <Text fontWeight="light">showing page {pageIndex + 1}</Text>
        <ButtonGroup variant="link" colorScheme="green" spacing={4}>
          <Button onClick={() => setPageIndex(pageIndex - 1)}>previous</Button>
          <Button onClick={() => setPageIndex(pageIndex + 1)}>next</Button>
        </ButtonGroup>
      </VStack>
    </Center>
  )
}
