from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import os

from ml_engine.recommender import recommend_internships

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "internships.csv")

# ✅ Candidate schema
class Candidate(BaseModel):
    education: Optional[str] = None
    skills: List[str] = []
    sectors: List[str] = []
    preferred_locations: List[str] = []
    max_results: int = 5

# ✅ Recommend endpoint
@router.post("/recommend")
def recommend(candidate: Candidate):
    internships = pd.read_csv(DATA_PATH)
    recs = recommend_internships(candidate.dict(), internships, candidate.max_results)
    return {"recommendations": recs}
