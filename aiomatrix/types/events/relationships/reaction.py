from pydantic import Field

from ..base import BasicRelationEventContent, BasicRelationshipData


class Reaction(BasicRelationshipData):
    key: str


class ReactionRelationship(BasicRelationEventContent):
    relationship: Reaction = Field(..., alias='m.relates_to')
