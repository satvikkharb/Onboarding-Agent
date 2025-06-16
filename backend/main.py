from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import Customer
from backend.crud import register_customer

app = FastAPI()

@app.get("/")
def start():
    return {'Message':'This is your onboarding agent!'}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             
    allow_credentials=True,          
    allow_methods=["*"],             
    allow_headers=["*"],             
)

@app.post("/register_customer")
async def register(customer:Customer):
    success = register_customer(customer)
    if success is None:
        raise HTTPException(status_code=400, detail="Registration Failed!")
    return {'message':'Customer registered successfully!'}

