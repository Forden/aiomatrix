from pydantic import Field

from ..base_room_events import RelationshipMixin, RelationshipToEventData


class Reaction(RelationshipToEventData):
    key: str


class ReactionRelationshipContent(RelationshipMixin):
    relationship: Reaction = Field(..., alias='m.relates_to')
