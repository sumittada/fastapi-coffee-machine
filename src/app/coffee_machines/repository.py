from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource


class CoffeeMachinesRepository:
    def __init__(self, db: ServiceResource) -> None:
        self.__db = db

    def get_all(self):
        table = self.__db.Table("coffeeMachines")
        response = table.scan()
        return response.get("Items", [])

    def get_coffee_machine(self, uid: str):
        try:
            table = self.__db.Table("coffeeMachines")
            response = table.get_item(Key={"uid": uid})
            return response["Item"]
        except ClientError as e:
            raise ValueError(e.response["Error"]["Message"])

    def create_coffee_machine(self, coffee_machine: dict):
        table = self.__db.Table("coffeeMachines")
        response = table.put_item(Item=coffee_machine)
        return response

    def update_coffee_machine(self, coffee_machine: dict):
        table = self.__db.Table("coffeeMachines")
        response = table.update_item(
            Key={"uid": coffee_machine.get("uid")},
            UpdateExpression="""
                set
                    name=:name,
                    machine_state=:machine_state,
                    machine_error=:machine_error
            """,
            ExpressionAttributeValues={
                ":name": coffee_machine.get("name"),
                ":machine_state": coffee_machine.get("machine_state"),
                ":machine_error": coffee_machine.get("machine_error"),
            },
            ReturnValues="UPDATED_NEW",
        )
        return response

    def delete_coffee_machine(self, uid: str):
        table = self.__db.Table("coffeeMachines")
        response = table.delete_item(Key={"uid": uid})
        return response
