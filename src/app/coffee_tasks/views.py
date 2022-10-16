from uuid import uuid4

from app.coffee_tasks.repository import CoffeeTasksRepository
from app.coffee_tasks.models import CoffeeTasksModel


class CoffeeTaskDomain:
    def __init__(self, repository: CoffeeTasksRepository) -> None:
        self.__repository = repository

    def get_all(self):
        return self.__repository.get_all()

    def get_coffee_task(self, uid: str):
        return self.__repository.get_coffee_task(uid)

    def create_coffee_task(self, coffee_task: CoffeeTasksModel):
        coffee_task.uid = str(uuid4())
        return self.__repository.create_coffee_task(coffee_task.dict())

    def update_coffee_task(self, coffee_task: CoffeeTasksModel):
        return self.__repository.update_coffee_task(coffee_task.dict())

    def delete_coffee_task(self, uid: str):
        return self.__repository.delete_coffee_task(uid)
