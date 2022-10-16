from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource


class CoffeeTasksRepository:
    def __init__(self, db: ServiceResource) -> None:
        self.__db = db

    def get_all(self):
        table = self.__db.Table("coffeeMachineTasks")
        response = table.scan()
        return response.get("Items", [])

    def get_coffee_task(self, uid: str):
        try:
            table = self.__db.Table("coffeeMachineTasks")
            response = table.get_item(Key={"uid": uid})
            return response["Item"]
        except ClientError as e:
            raise ValueError(e.response["Error"]["Message"])

    def create_coffee_task(self, coffee_task: dict):
        table = self.__db.Table("coffeeMachineTasks")
        response = table.put_item(Item=coffee_task)
        return response

    def update_coffee_task(self, coffee_task: dict):
        table = self.__db.Table("coffeeMachineTasks")
        response = table.update_item(
            Key={"uid": coffee_task.get("uid")},
            UpdateExpression="""
                set
                    coffee_type=:coffee_type,
                    strength=:strength,
                    size=:size,
                    beans_choice=:beans_choice
            """,
            ExpressionAttributeValues={
                ":coffee_type": coffee_task.get("coffee_type"),
                ":strength": coffee_task.get("strength"),
                ":size": coffee_task.get("size"),
                ":beans_choice": coffee_task.get("beans_choice"),
            },
            ReturnValues="UPDATED_NEW",
        )
        return response

    def delete_coffee_task(self, uid: str):
        table = self.__db.Table("coffeeMachineTasks")
        response = table.delete_item(Key={"uid": uid})
        return response
