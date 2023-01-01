import {
  Card,
  CardBody,
  Divider,
  HStack,
  SimpleGrid,
  Stack,
  Text,
  VStack,
} from "@chakra-ui/react"
import Image from "next/image"
import NextLink from "next/link"
import { URLs } from "../data/config"
import Logo from "../public/logo.svg"
import { NavLink } from "./navlink"

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
  },
} as const

export function Footer() {
  return (
    <Card variant="outline" textColor="darkslategrey">
      <CardBody>
        <SimpleGrid
          templateColumns={{
            sm: "1fr 1fr",
            md: `1.5fr repeat(${Object.keys(sections).length}, 1fr)`,
          }}>
          <VStack>
            <Image alt="Jogaar Mods logo" src={Logo} width={200} />
            <HStack spacing={4}>
              <NavLink href={"#"}>Facebook</NavLink>
              <Divider orientation="vertical" />
              <NavLink href={"#"}>Twitter</NavLink>
              <Divider orientation="vertical" />
              <NavLink href={"#"}>LinkedIn</NavLink>
            </HStack>
          </VStack>

          {Object.entries(sections).map(([title, links], index) => (
            // because they have stable indices
            <Stack key={index}>
              <Text fontWeight="medium" fontSize={"18px"} p={1}>
                {title}
              </Text>
              {Object.entries(links).map(([text, ref], index) => (
                <NavLink
                  // TODO fix this outline issue
                  maxW={36}
                  as={NextLink}
                  href={ref}
                  key={index}
                  isExternal={title.toLowerCase() !== "sitemap"}>
                  {text}
                </NavLink>
              ))}
            </Stack>
          ))}
        </SimpleGrid>
        <br />
      </CardBody>
    </Card>
  )
}
