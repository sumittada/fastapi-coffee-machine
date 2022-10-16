from fastapi import FastAPI

from app.common.ddb import initialize_db
from app.coffee_tasks.views import CoffeeTaskDomain
from app.coffee_tasks.repository import CoffeeTasksRepository
from app.coffee_tasks.router import CoffeeTasksRouter

from app.coffee_machines.views import CoffeeMachineDomain
from app.coffee_machines.repository import CoffeeMachinesRepository
from app.coffee_machines.router import CoffeeMachinesRouter


app = FastAPI()

db = initialize_db()

coffee_tasks_repository = CoffeeTasksRepository(db)
coffee_tasks_domain = CoffeeTaskDomain(coffee_tasks_repository)
coffee_tasks_router = CoffeeTasksRouter(coffee_tasks_domain)

app.include_router(coffee_tasks_router.router)


coffee_machines_repository = CoffeeMachinesRepository(db)
coffee_machines_domain = CoffeeMachineDomain(coffee_machines_repository)
coffee_machines_router = CoffeeMachinesRouter(coffee_machines_domain)

app.include_router(coffee_machines_router.router)
