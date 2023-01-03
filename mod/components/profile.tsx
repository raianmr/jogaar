import {
  Button,
  Center,
  Menu,
  MenuButton,
  MenuDivider,
  MenuList,
} from "@chakra-ui/react"
import { URLs } from "../data/config"
import { User } from "../data/models"
import { AvatarWrapper } from "./images"
import { NavLink } from "./nav"

export function Profile({ user }: { user: User }) {
  return (
    <Menu>
      <MenuButton as={Button} variant={"link"} cursor={"pointer"}>
        {user.portrait_id != null && (
          <AvatarWrapper img_id={user.portrait_id} size={"sm"} />
        )}
      </MenuButton>
      <MenuList alignItems={"center"}>
        <br />
        {user.portrait_id != null && (
          <AvatarWrapper img_id={user.portrait_id} size={"2xl"} />
        )}
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
