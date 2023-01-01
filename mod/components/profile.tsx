import {
  Avatar,
  Button,
  Center,
  Menu,
  MenuButton,
  MenuDivider,
  MenuList,
} from "@chakra-ui/react"
import { URLs } from "../data/config"
import { useImage } from "../data/fetching"
import { User } from "../data/models"
import { NavLink } from "./navlink"

export function Profile({ user }: { user: User }) {
  // horrible hack lmao
  const [image, errored] = useImage(user.portrait_id ?? 0, {
    shouldRetryOnError: false,
  })

  return (
    <Menu>
      <MenuButton as={Button} variant={"link"} cursor={"pointer"}>
        {!errored && image && (
          <Avatar size={"sm"} src={URLs.API.STATIC(image.location)} />
        )}
      </MenuButton>
      <MenuList alignItems={"center"}>
        <br />
        <Center>
          {!errored && image && (
            <Avatar size={"2xl"} src={URLs.API.STATIC(image.location)} />
          )}
        </Center>
        <br />
        <Center>
          <NavLink href={URLs.WEB.PROFILE(user.id)}>
            {user.name}, {user.access_level}
          </NavLink>
        </Center>
        <MenuDivider />
        <Center>
          <NavLink href={`mailto:${user.email}`}>{user.email} </NavLink>
        </Center>
        <br />
      </MenuList>
    </Menu>
  )
}
