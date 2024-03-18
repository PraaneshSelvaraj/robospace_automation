from fastapi import FastAPI
from dotenv import load_dotenv
from controllers import studentRegistrationController

load_dotenv()

app = FastAPI()
app.include_router(studentRegistrationController.router)