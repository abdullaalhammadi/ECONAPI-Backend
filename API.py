from fastapi import FastAPI, Form
from sympy.solvers import solve
from sympy import Symbol
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

## !!! DISABLE CORS BEFORE DEPLOYMENT !!!

## BEFORE DEPLOYMENT DELETE THE SECTION FROM BELOW HERE

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### TO ABOVE HERE

class NX(BaseModel):
    Y1: float
    I1_INTERCEPT: float
    I1_SLOPE: float
    T1: float
    G1: float
    C1_INTERCEPT: float
    C1_SLOPE: float
    Y2: float
    I2_INTERCEPT: float
    I2_SLOPE: float
    T2: float
    G2: float
    C2_INTERCEPT: float
    C2_SLOPE: float

@app.post("/NX/")
async def create_item(nx: NX):
	r = Symbol('r')
	C1 = nx.C1_INTERCEPT + 0.5*(nx.Y1 - nx.T1) - nx.C1_SLOPE*r
	C2 = nx.C2_INTERCEPT + 0.5*(nx.Y2 - nx.T2) - nx.C2_SLOPE*r
	return {
	"Message": "Success!",
	"value": float(solve((((nx.Y1 - (C1) - nx.G1) - (nx.I1_INTERCEPT - nx.I1_SLOPE*r)) + (nx.Y2 - (C2) - nx.G2) - (nx.I2_INTERCEPT - nx.I2_SLOPE*r)))[0])
	}