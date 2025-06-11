from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*codesphere.com"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
def read_root():
    return {"Status": "FastAPI Backend is running"}


@app.get("/api/data")
def get_chart_data(points: int = 30) -> Dict:
    test_data = create_data(points)
    return test_data

def create_data(points: int) -> Dict:
    chart_data = pd.DataFrame(
        np.random.randn(points, 2),
        columns=['A', 'B']
    )
    return chart_data.to_dict(orient='split')

if __name__ == "__main__":
  pass
  

