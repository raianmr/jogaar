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
import { AvatarWrapper } from "../components/images"
import { Campaign } from "../data/models"

export function CampaignCard({ campaign }: { campaign: Campaign }) {
  return (
    <Card maxW="sm" variant="outline" px={4}>
      <CardBody>
        <HStack h={24} justifyContent={"space-between"}>
          <Stack spacing="3">
            <Heading size="md">{campaign.title}</Heading>
            <Text>{campaign.description}</Text>
          </Stack>
          {campaign.cover_id != null && (
            <AvatarWrapper img_id={campaign.cover_id} size={"xl"} />
          )}
        </HStack>
      </CardBody>
      <Divider />
      <HStack p={4} justifyContent={"space-between"}>
        <Text color="olive" fontSize="2xl" mr={16}>
          {campaign.pledged}
        </Text>
        <ButtonGroup>
          <Button variant="solid" colorScheme="green" px={4}>
            greenlight
          </Button>
          <Button variant="ghost" colorScheme="red" px={4}>
            lock
          </Button>
        </ButtonGroup>
      </HStack>
    </Card>
  )
}
