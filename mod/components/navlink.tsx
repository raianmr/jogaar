import { Link } from "@chakra-ui/react"
import NextLink from "next/link"

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
