from fastapi import FastAPI

from app.common.ddb import initialize_db
from app.coffee_tasks.views import CoffeeTaskDomain
from app.coffee_tasks.repository import CoffeeTasksRepository
from app.coffee_tasks.router import CoffeeTasksRouter


app = FastAPI()

db = initialize_db()

coffee_tasks_repository = CoffeeTasksRepository(db)
coffee_tasks_domain = CoffeeTaskDomain(coffee_tasks_repository)
coffee_tasks_router = CoffeeTasksRouter(coffee_tasks_domain)

app.include_router(coffee_tasks_router.router)

