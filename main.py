from fastapi import FastAPI
from dotenv import load_dotenv
from controllers import studentRegistrationController, entryExitController, logsController

load_dotenv()

app = FastAPI()
app.include_router(studentRegistrationController.router)
app.include_router(entryExitController.router)
app.include_router(logsController.router)