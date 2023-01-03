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
import { Dispatch, SetStateAction, useEffect, useState } from "react"
import { SuperCard } from "../components/cards"
import { URLs } from "../data/config"
import { useSupers, useUser } from "../data/fetching"

type page = "start" | "middle" | "end"

function Page({
  index,
  limit,
  offset,
  setPageType,
}: {
  index: number
  limit: number
  offset: number
  setPageType?: Dispatch<SetStateAction<page>>
}) {
  const [supers, errored] = useSupers(limit, offset)

  useEffect(() => {
    if (setPageType !== undefined && supers !== undefined) {
      if (index == 0) {
        setPageType("start")
      } else if (supers.length == 0) {
        setPageType("end")
      } else {
        setPageType("middle")
      }
    }
  })

  return (
    <SimpleGrid
      templateColumns={{
        sm: "1fr 1fr",
        md: `repeat(3, 1fr)`,
      }}
      spacing={4}
      p={8}>
      {!errored &&
        supers?.map(super_ => (
          <SuperCard
            key={super_.id}
            super_={super_}
            limit={limit}
            offset={offset}
          />
        ))}
    </SimpleGrid>
  )
}

export default function Supers() {
  const toast = useToast()
  const router = useRouter()
  const [user, loggedOut] = useUser()

  const [pageType, setPageType] = useState<page>("start")
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
          All admins and moderators
        </Heading>
        <Page
          index={pageIndex}
          limit={9}
          offset={9 * pageIndex}
          setPageType={setPageType}
        />
        <div style={{ display: "none" }}>
          <Page index={pageIndex + 1} limit={9} offset={9 * (pageIndex + 1)} />
        </div>
        {/* <Divider /> */}
        <Text fontWeight="light">showing page {pageIndex + 1}</Text>
        <ButtonGroup variant="link" colorScheme="green" spacing={4}>
          <Button
            disabled={pageType === "start"}
            onClick={() => setPageIndex(pageIndex - 1)}>
            previous
          </Button>
          <Button
            disabled={pageType === "end"}
            onClick={() => setPageIndex(pageIndex + 1)}>
            next
          </Button>
        </ButtonGroup>
      </VStack>
    </Center>
  )
}
