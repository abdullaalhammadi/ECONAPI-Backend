from fastapi import FastAPI, Form
from sympy.solvers import solve
from sympy import Symbol
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(

    title="Macroeconomic calculator"

)

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
    C1_MIDVAL: float
    C1_SLOPE: float
    Y2: float
    I2_INTERCEPT: float
    I2_SLOPE: float
    T2: float
    G2: float
    C2_INTERCEPT: float
    C2_SLOPE: float
    C2_MIDVAL: float

@app.post("/NX/")
async def create_item(nx: NX):
    r = Symbol('r')
    C1 = nx.C1_INTERCEPT + nx.C1_MIDVAL*(nx.Y1 - nx.T1) - nx.C1_SLOPE*r
    C2 = nx.C2_INTERCEPT + nx.C2_MIDVAL*(nx.Y2 - nx.T2) - nx.C2_SLOPE*r
    r_value = float(solve((((nx.Y1 - (C1) - nx.G1) - (nx.I1_INTERCEPT - nx.I1_SLOPE*r)) + (nx.Y2 - (C2) - nx.G2) - (nx.I2_INTERCEPT - nx.I2_SLOPE*r)))[0])
    C1_NX = nx.Y1 - ((nx.C1_INTERCEPT + nx.C1_MIDVAL*(nx.Y1 - nx.T1) - nx.C1_SLOPE*r_value) + (nx.I1_INTERCEPT - nx.I1_SLOPE*r_value) + nx.G1)
    C1_SAVINGS = nx.Y1 - (nx.C1_INTERCEPT + nx.C1_MIDVAL*(nx.Y1 - nx.T1) - nx.C1_SLOPE*r_value) - nx.G1
    C1_INVESTMENT = nx.I1_INTERCEPT - nx.I1_SLOPE*r_value
    C2_NX = nx.Y2 - ((nx.C2_INTERCEPT + nx.C2_MIDVAL*(nx.Y2 - nx.T2) - nx.C2_SLOPE*r_value) + (nx.I2_INTERCEPT - nx.I2_SLOPE*r_value) + nx.G2)
    C2_SAVINGS = nx.Y2 - (nx.C2_INTERCEPT + nx.C2_MIDVAL*(nx.Y2 - nx.T2) - nx.C2_SLOPE*r_value) - nx.G2
    C2_INVESTMENT = nx.I2_INTERCEPT - nx.I2_SLOPE*r_value
    return {
    "Message": "Success!",
    "r_value": r_value,
    "Country 1 savings": C1_SAVINGS,
    "Country 1 investment": C1_INVESTMENT,
    "Country 1 NX": C1_NX,
    "Country 2 savings": C2_SAVINGS,
    "Country 2 investment": C2_INVESTMENT,
    "Country 2 NX": C2_NX
	}