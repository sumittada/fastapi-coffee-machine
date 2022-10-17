from fastapi import APIRouter, Depends, FastAPI, Response, status
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from app.coffee_tasks.models import CoffeeTasksModel
from app.coffee_tasks.views import CoffeeTaskDomain
from app.common.auth_utils import VerifyToken

token_auth_scheme = HTTPBearer()


class CoffeeTasksRouter:
    def __init__(self, coffee_tasks_domain: CoffeeTaskDomain) -> None:
        self.__coffee_tasks_domain = coffee_tasks_domain

    @property
    def router(self):
        api_router = APIRouter(prefix="/coffee_tasks", tags=["coffee_tasks"])

        @api_router.get("/")
        def index_route():
            return "Hello world! Use /docs to find the features supported by this API."

        @api_router.get("/all")
        def get_all():
            return self.__coffee_tasks_domain.get_all()

        @api_router.post("/create")
        def create_coffee_task(coffee_tasks_model: CoffeeTasksModel,response: Response, token: str = Depends(token_auth_scheme)):
            auth_result = VerifyToken(token.credentials).verify()

            if auth_result.get("status"):
                raise HTTPException(status_code=401, detail="Bad auth token")
            return self.__coffee_tasks_domain.create_coffee_task(coffee_tasks_model)

        @api_router.get("/get/{coffee_task_uid}")
        def get_coffee_task(coffee_task_uid: str):
            try:
                return self.__coffee_tasks_domain.get_coffee_task(coffee_task_uid)
            except KeyError:
                raise HTTPException(status_code=400, detail="No coffee_task found")

        @api_router.put("/update")
        def update_coffee_task(coffee_tasks_model: CoffeeTasksModel,response: Response, token: str = Depends(token_auth_scheme)):
            auth_result = VerifyToken(token.credentials).verify()

            if auth_result.get("status"):
                raise HTTPException(status_code=401, detail="Bad auth token")
            return self.__coffee_tasks_domain.update_coffee_task(coffee_tasks_model)

        @api_router.delete("/delete/{coffee_task_uid}")
        def delete_coffee_task(coffee_task_uid: str, response: Response, token: str = Depends(token_auth_scheme)):
            auth_result = VerifyToken(token.credentials).verify()

            if auth_result.get("status"):
                raise HTTPException(status_code=401, detail="Bad auth token")
            return self.__coffee_tasks_domain.delete_coffee_task(coffee_task_uid)

        return api_router
