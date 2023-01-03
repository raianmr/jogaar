import { Avatar, Center } from "@chakra-ui/react"
import { ComponentProps } from "react"
import { URLs } from "../data/config"
import { useImage } from "../data/fetching"

export function AvatarWrapper({
  img_id,
  ...props
}: { img_id: number } & ComponentProps<typeof Avatar>) {
  const [image, errored] = useImage(img_id, {
    shouldRetryOnError: false,
  })

  return (
    <Center>
      {!errored && image && (
        <Avatar src={URLs.API.STATIC(image.location)} {...props} />
      )}
    </Center>
  )
}
