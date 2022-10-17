from fastapi import APIRouter, Depends, FastAPI, Response, status
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from app.coffee_machines.models import CoffeeMachinesModel
from app.coffee_machines.views import CoffeeMachineDomain
from app.common.auth_utils import VerifyToken


token_auth_scheme = HTTPBearer()



class CoffeeMachinesRouter:
    def __init__(self, coffee_machines_domain: CoffeeMachineDomain) -> None:
        self.__coffee_machines_domain = coffee_machines_domain

    @property
    def router(self):
        api_router = APIRouter(prefix="/coffee_machines", tags=["coffee_machines"])

        @api_router.get("/")
        def index_route():
            return "Hello world! Use /docs to find the features supported by this API."

        @api_router.get("/all")
        def get_all():
            return self.__coffee_machines_domain.get_all()

        @api_router.post("/create")
        def create_coffee_machine(coffee_machines_model: CoffeeMachinesModel, response: Response, token: str = Depends(token_auth_scheme)):
            auth_result = VerifyToken(token.credentials).verify()

            if auth_result.get("status"):
                raise HTTPException(status_code=401, detail="Bad auth token")

            return self.__coffee_machines_domain.create_coffee_machine(coffee_machines_model)

        @api_router.get("/get/{coffee_machine_uid}")
        def get_coffee_machine(coffee_machine_uid: str):
            try:
                return self.__coffee_machines_domain.get_coffee_machine(coffee_machine_uid)
            except KeyError:
                raise HTTPException(status_code=400, detail="No coffee_machine found")

        @api_router.put("/update")
        def update_coffee_machine(coffee_machines_model: CoffeeMachinesModel, response: Response, token: str = Depends(token_auth_scheme)):
            auth_result = VerifyToken(token.credentials).verify()

            if auth_result.get("status"):
                raise HTTPException(status_code=401, detail="Bad auth token")
            return self.__coffee_machines_domain.update_coffee_machine(coffee_machines_model)

        @api_router.delete("/delete/{coffee_machine_uid}")
        def delete_coffee_machine(coffee_machine_uid: str, response: Response, token: str = Depends(token_auth_scheme)):
            auth_result = VerifyToken(token.credentials).verify()

            if auth_result.get("status"):
                raise HTTPException(status_code=401, detail="Bad auth token")
            return self.__coffee_machines_domain.delete_coffee_machine(coffee_machine_uid)

        return api_router
