from pydantic import BaseModel, Field
from typing import List

class Fact(BaseModel):
    content: str = Field(
        description="An atomic factual statement derived from the input"
    )
    description: str = Field(
        description=(
            "A high-level semantic interpretation of what this fact represents, "
            "such as a role assignment, temporal state, relationship, identity, "
            "event, or attribute, without repeating the factual content"
        )
    )

class SemanticFacts(BaseModel):
    data: List[Fact] = Field(
        description="List of atomic facts extracted from the input text"
    )