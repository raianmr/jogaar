import {
  Box,
  Button,
  Card,
  CardBody,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input,
  Stack,
  useToast,
  VStack,
} from "@chakra-ui/react"
import Image from "next/image"
import { useRouter } from "next/router"
import { FormEvent, useEffect, useState } from "react"
import { URLs } from "../data/config"
import { fetchTokenData } from "../data/fetching"
import { getToken, setToken } from "../data/store"
import Logo from "../public/logo.svg"

// TODO https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/

export default function Login() {
  const toast = useToast()
  const router = useRouter()

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  useEffect(() => {
    const token = getToken()

    if (token) {
      router.push(URLs.MOD.SUPERS)
    }
  })

  const submitHandler = async (e: FormEvent) => {
    e.preventDefault()

    try {
      const data = await fetchTokenData({ username, password })

      if (["banned", "normal"].includes(data.access_level)) {
        throw new Error("Forbidden")
      }

      setToken(data)

      router.push(URLs.MOD.SUPERS)
    } catch (e: any) {
      toast({
        title: e.message,
        description: e.data.detail,
        status: "error",
        duration: 3000,
        isClosable: true,
      })
    }
  }

  // not sure about the science behind this but onBlur just seems more natural
  const [unfocusedUsername, setUnfocusedUsername] = useState(false)
  const [unfocusedPassword, setUnfocusedPassword] = useState(false)

  return (
    <Box>
      <VStack as="header" spacing="6" mt="8">
        <Image alt="Jogaar Mods logo" src={Logo} />
        <Heading as="h1" fontWeight="thin" fontSize="24px">
          Enter credentials
        </Heading>
        <Card variant="outline" w="300px">
          <CardBody>
            <form onSubmit={submitHandler}>
              <Stack spacing="4">
                <FormControl isInvalid={username === "" && unfocusedUsername}>
                  <FormLabel>Email address</FormLabel>
                  <Input
                    size="sm"
                    type="email"
                    bg="white"
                    borderRadius="6px"
                    required
                    placeholder="user@example.com"
                    onBlur={() => setUnfocusedUsername(true)}
                    onChange={e => setUsername(e.target.value)}
                  />
                  <FormErrorMessage>{"invalid username"}</FormErrorMessage>
                </FormControl>
                <FormControl isInvalid={password === "" && unfocusedPassword}>
                  <FormLabel>Password</FormLabel>
                  <Input
                    size="sm"
                    type="password"
                    bg="white"
                    borderRadius="6px"
                    required
                    placeholder={"*".repeat(8)}
                    onBlur={() => setUnfocusedPassword(true)}
                    onChange={e => setPassword(e.target.value)}
                  />
                  <FormErrorMessage>{"invalid password"}</FormErrorMessage>
                </FormControl>

                <Button
                  bg="OliveDrab"
                  color="white"
                  size="sm"
                  type="submit"
                  _hover={{ bg: "Olive" }}
                  _active={{ bg: "DarkOliveGreen" }}>
                  Sign in
                </Button>
              </Stack>
            </form>
          </CardBody>
        </Card>
      </VStack>
    </Box>
  )
}
