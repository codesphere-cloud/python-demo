import uuid
from typing import Dict
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from database import init_db, get_db, DataPoint

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*codesphere.com"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.on_event("startup")
def startup_event():
    """Initialize the database tables on startup."""
    init_db()


@app.get("/")
def read_root():
    return {"Status": "FastAPI Backend is running"}


@app.get("/api/data")
def get_chart_data(points: int = 30, db: Session = Depends(get_db)) -> Dict:
    test_data = create_data(points, db)
    return test_data


def create_data(points: int, db: Session) -> Dict:
    chart_data = pd.DataFrame(
        np.random.randn(points, 2),
        columns=['A', 'B']
    )
    
    # Save points to database
    batch_id = str(uuid.uuid4())
    db_points = [
        DataPoint(
            batch_id=batch_id,
            value_a=float(row['A']),
            value_b=float(row['B'])
        )
        for _, row in chart_data.iterrows()
    ]
    db.add_all(db_points)
    db.commit()
    
    return chart_data.to_dict(orient='split')

if __name__ == "__main__":
  pass
  

