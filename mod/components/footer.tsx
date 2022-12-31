import {
  Box,
  Card,
  CardBody,
  HStack,
  Link,
  SimpleGrid,
  Stack,
  Text,
  VStack,
} from "@chakra-ui/react"
import Image from "next/image"
import NextLink from "next/link"
import { URLs } from "../data/config"
import Logo from "../public/logo.svg"

const sections = {
  API: {
    OpenAPI: URLs.API.OPENAPI,
    Swagger: URLs.API.SWAGGER,
  },
  Web: {
    Landing: URLs.WEB.ROOT,
    Catalogue: URLs.WEB.CATALOGUE,
  },
  Sitemap: {
    "Super users": URLs.MOD.SUPERS,
    "Ended campaigns": URLs.MOD.CAMPAIGNS,
    "User reports": URLs.MOD.REPORTS,
    "Reset session": URLs.MOD.RESET,
  },
} as const

// func Section({})

export function Footer() {
  return (
    <Box>
      <Card variant="outline" py={5} textColor="darkslategrey">
        <CardBody>
          <SimpleGrid
            templateColumns={{
              sm: "1fr 1fr",
              md: `1.5fr repeat(${Object.keys(sections).length}, 1fr)`,
            }}
            spacing={8}>
            <VStack>
              <Image alt="Jogaar Mods logo" src={Logo} width={300} />
              <HStack spacing={8}>
                <Link href={"#"}>Facebook</Link>
                <Link href={"#"}>Twitter</Link>
                <Link href={"#"}>LinkedIn</Link>
              </HStack>
            </VStack>

            {Object.entries(sections).map(([title, links], index) => (
              // because they have stable indices
              <Stack px={10} key={index}>
                <Text fontWeight="medium" fontSize={"18px"} mb={2}>
                  {title}
                </Text>
                {Object.entries(links).map(([text, ref], index) => (
                  <Link
                    as={NextLink}
                    href={ref}
                    key={index}
                    isExternal={title.toLowerCase() !== "sitemap"}>
                    {text}
                  </Link>
                ))}
              </Stack>
            ))}
          </SimpleGrid>
        </CardBody>
      </Card>
    </Box>
  )
}
