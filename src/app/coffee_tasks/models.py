from uuid import UUID, uuid4
from pydantic import Field
from pydantic import BaseModel
from enum import Enum


class CoffeeType(str, Enum):
    cappuccino = "cappuccino"
    espresso = "espresso"
    cortado = "cortado"
    latte = "latte"


class StrengthType(str, Enum):
    mild = "mild"
    standard = "standard"
    strong = "strong"


class SizeType(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"
    extra_large = "extra_large"


class BeansChoiceType(str, Enum):
    left = "left"
    right = "right"


class CoffeeTasksModel(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    coffee_type: CoffeeType = Field(
        default="espresso", example="Choices: cappuccino, espresso, cortado, latte"
    )
    strength: StrengthType = Field(
        default="standard", example="Choices: mild, standard, strong"
    )
    size: SizeType = Field(
        default="medium", example="Choices: small, medium, large, extra_large"
    )
    beans_choice: BeansChoiceType = Field(
        default="left", example="Choices: left, right"
    )

    class Config:
        use_enum_values = True
