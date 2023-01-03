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
import {
  dismiss,
  toggleBan,
  toggleGreenlight,
  toggleLock,
  toggleMod,
  useUser,
} from "../data/fetching"
import { Campaign, Report, User } from "../data/models"
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

export function SuperCard({
  super_,
  limit,
  offset,
}: {
  super_: User
  limit: number
  offset: number
}) {
  const [statefulSuper, setStatefulSuper] = useState(super_)
  const [currentUser, _] = useUser()

  return (
    <Card maxW="sm" variant="outline" px={4}>
      <CardBody>
        <HStack h={24} justifyContent={"space-between"}>
          <Stack spacing="4">
            <NavLink href={URLs.WEB.PROFILE(statefulSuper.id)}>
              <Heading size="md">{statefulSuper.name}</Heading>
            </NavLink>
            <Text>{statefulSuper.about}</Text>
          </Stack>
          {statefulSuper.portrait_id != null && (
            <AvatarWrapper img_id={statefulSuper.portrait_id} size={"xl"} />
          )}
        </HStack>
      </CardBody>
      <Divider />
      <HStack p={4} justifyContent={"space-between"}>
        <Text color="olive" fontSize="2xl" mr={16}>
          {statefulSuper.access_level}
        </Text>
        {currentUser?.access_level == "admin" &&
          statefulSuper.access_level !== "admin" && (
            <ButtonGroup>
              <Button
                variant={
                  statefulSuper.access_level === "mod" ? "solid" : "ghost"
                }
                onClick={() => {
                  setStatefulSuper({
                    ...statefulSuper,
                    access_level:
                      statefulSuper.access_level !== "mod" ? "normal" : "mod",
                  })
                  toggleMod(statefulSuper, limit, offset)
                }}
                colorScheme="green"
                px={4}>
                mod
              </Button>
              <Button
                variant={
                  statefulSuper.access_level === "banned" ? "solid" : "ghost"
                }
                onClick={() => {
                  setStatefulSuper({
                    ...statefulSuper,
                    access_level:
                      statefulSuper.access_level !== "banned"
                        ? "normal"
                        : "banned",
                  })
                  toggleBan(statefulSuper, limit, offset)
                }}
                colorScheme="red"
                px={4}>
                ban
              </Button>
            </ButtonGroup>
          )}
      </HStack>
    </Card>
  )
}

export function ReportCard({
  report,
  limit,
  offset,
}: {
  report: Report
  limit: number
  offset: number
}) {
  const [statefulReport, setStatefulReport] = useState(report)

  return (
    <Card maxW="sm" variant="outline" px={4}>
      <CardBody>
        <HStack h={24} justifyContent={"space-between"}>
          <Stack spacing="4">
            <NavLink href={URLs.WEB.PROFILE(statefulReport.reporter_id)}>
              <Heading size="md">
                report by user {statefulReport.reporter_id}
              </Heading>
            </NavLink>
            <Text>{statefulReport.description}</Text>
          </Stack>
        </HStack>
      </CardBody>
      <Divider />
      <HStack p={4} justifyContent={"space-between"}>
        <NavLink
          href={URLs.WEB.CONTENT(
            statefulReport.content_id,
            statefulReport.content_type
          )}>
          <Text color="olive" fontSize="18px" mr={16}>
            go to {statefulReport.content_type}
          </Text>
        </NavLink>

        <ButtonGroup>
          <Button
            variant="solid"
            onClick={() => {
              setStatefulReport({
                ...statefulReport,
              })
              dismiss(report, limit, offset)
            }}
            colorScheme="red"
            px={4}>
            dismiss
          </Button>
        </ButtonGroup>
      </HStack>
    </Card>
  )
}
