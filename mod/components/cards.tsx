import {
  Button,
  ButtonGroup,
  Card,
  CardBody,
  Divider,
  Heading,
  HStack,
  Stack,
  Text,
} from "@chakra-ui/react"
import { useState } from "react"
import { AvatarWrapper } from "../components/images"
import { URLs } from "../data/config"
import { toggleGreenlight, toggleLock } from "../data/fetching"
import { Campaign } from "../data/models"
import { NavLink } from "./nav"

export function CampaignCard({
  campaign,
  limit,
  offset,
}: {
  campaign: Campaign
  limit: number
  offset: number
}) {
  const [statefulCampaign, setStatefulCampaign] = useState(campaign)

  return (
    <Card maxW="sm" variant="outline" px={4}>
      <CardBody>
        <HStack h={24} justifyContent={"space-between"}>
          <Stack spacing="4">
            <NavLink href={URLs.WEB.CAMPAIGN(statefulCampaign.id)}>
              <Heading size="md">{statefulCampaign.title}</Heading>
            </NavLink>
            <Text>{statefulCampaign.description}</Text>
          </Stack>
          {statefulCampaign.cover_id != null && (
            <AvatarWrapper img_id={statefulCampaign.cover_id} size={"xl"} />
          )}
        </HStack>
      </CardBody>
      <Divider />
      <HStack p={4} justifyContent={"space-between"}>
        <Text color="olive" fontSize="2xl" mr={16}>
          {statefulCampaign.pledged}
        </Text>
        <ButtonGroup>
          <Button
            variant={
              statefulCampaign.current_state === "greenlit" ? "solid" : "ghost"
            }
            onClick={() => {
              setStatefulCampaign({
                ...statefulCampaign,
                current_state:
                  statefulCampaign.current_state !== "greenlit"
                    ? "ended"
                    : "greenlit",
              })
              toggleGreenlight(statefulCampaign, limit, offset)
            }}
            colorScheme="green"
            px={4}>
            greenlight
          </Button>
          <Button
            variant={
              statefulCampaign.current_state === "locked" ? "solid" : "ghost"
            }
            onClick={() => {
              setStatefulCampaign({
                ...statefulCampaign,
                current_state:
                  statefulCampaign.current_state !== "locked"
                    ? "ended"
                    : "locked",
              })
              toggleLock(statefulCampaign, limit, offset)
            }}
            colorScheme="red"
            px={4}>
            lock
          </Button>
        </ButtonGroup>
      </HStack>
    </Card>
  )
}
