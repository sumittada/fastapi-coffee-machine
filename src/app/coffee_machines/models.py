from typing import Optional
from uuid import UUID, uuid4
from pydantic import Field
from pydantic import BaseModel
from enum import Enum


class MachineStatesType(str, Enum):
    brewing = "brewing"
    grinding = "grinding"
    pouring = "pouring"
    cleaning = "cleaning"
    ready = "ready"
    error = "error"


class MachineErrorTypes(str, Enum):
    beans_empty = "beans_empty"
    water_empty = "water_empty"
    bin_full = "bin_full"
    sump_full = "sump_full"


class CoffeeMachinesModel(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    name: str
    machine_state: MachineStatesType = Field(
        default="ready", example="Current state of machine"
    )
    machine_error: Optional[MachineErrorTypes] = Field(
        default=None, example="Error type, if there is an error"
    )

    class Config:
        use_enum_values = True
