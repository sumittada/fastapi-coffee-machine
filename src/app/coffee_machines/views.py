from uuid import uuid4

from app.coffee_machines.repository import CoffeeMachinesRepository
from app.coffee_machines.models import CoffeeMachinesModel


class CoffeeMachineDomain:
    def __init__(self, repository: CoffeeMachinesRepository) -> None:
        self.__repository = repository

    def get_all(self):
        return self.__repository.get_all()

    def get_coffee_machine(self, uid: str):
        return self.__repository.get_coffee_machine(uid)

    def create_coffee_machine(self, coffee_machine: CoffeeMachinesModel):
        coffee_machine.uid = str(uuid4())
        return self.__repository.create_coffee_machine(coffee_machine.dict())

    def update_coffee_machine(self, coffee_machine: CoffeeMachinesModel):
        return self.__repository.update_coffee_machine(coffee_machine.dict())

    def delete_coffee_machine(self, uid: str):
        return self.__repository.delete_coffee_machine(uid)
