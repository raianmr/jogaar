import { Card, CardBody, HStack, Link } from "@chakra-ui/react"
import Image from "next/image"
import NextLink from "next/link"
import { useRouter } from "next/router"
import { URLs } from "../data/config"
import { useUser } from "../data/fetching"
import { clearStore } from "../data/store"
import Logo from "../public/logo.svg"
import { Profile } from "./profile"

export const NavLink: typeof Link = ({ children, ...props }) => (
  <Link
    as={NextLink}
    px={1}
    color="darkslategrey"
    _hover={{
      color: "olive",
      outline: "2px dashed olive",
      borderRadius: "6px",
    }}
    {...props}>
    {children}
  </Link>
)

export function Navbar() {
  const router = useRouter()
  const [user, loggedOut] = useUser({ shouldRetryOnError: false })

  return (
    <Card variant="outline">
      <CardBody>
        <HStack maxH={4} justifyContent={"space-between"}>
          <HStack spacing={8}>
            <Image alt="Jogaar Mods logo" src={Logo} width={100} />
            <NavLink href={URLs.MOD.SUPERS}>Supers</NavLink>
            <NavLink href={URLs.MOD.CAMPAIGNS}>Campaigns</NavLink>
            <NavLink href={URLs.MOD.REPORTS}>Reports</NavLink>
          </HStack>
          {!loggedOut && user && (
            <HStack spacing={8}>
              <NavLink
                href={URLs.MOD.LOGIN}
                onClick={() => {
                  clearStore()
                  router.push(URLs.MOD.LOGIN)
                }}>
                Reset
              </NavLink>
              <Profile user={user} />
            </HStack>
          )}
        </HStack>
      </CardBody>
    </Card>
  )
}
