from fastapi import FastAPI
from database import Base, engine
from models import customer
from routes import customers
from models import invoice   
from routes import invoices
from models import payment   
from routes import payments
from models import user
from routes import auth
from models import invoice_item

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Billing System Running"}

Base.metadata.create_all(bind=engine)

#Connect Route to App
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
