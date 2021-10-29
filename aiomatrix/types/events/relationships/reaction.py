from pydantic import Field

from ..base import RelationshipMixin, RelationshipToEventData


class Reaction(RelationshipToEventData):
    key: str


class ReactionRelationshipContent(RelationshipMixin):
    relationship: Reaction = Field(..., alias='m.relates_to')
