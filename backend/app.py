from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from recommender import recommend_internships
import uvicorn
import csv
import os
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "internships.csv")

app = FastAPI(title="PM Internship Recommender")

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route
@app.get("/")
async def root():
    return {"message": "PM Internship Recommender API is running 🚀"}

# ✅ Load internships once
with open(DATA_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    INTERNSHIPS = [row for row in reader]

# ✅ Candidate schema
class Candidate(BaseModel):
    education: Optional[str] = None
    skills: List[str] = []
    sectors: List[str] = []
    preferred_locations: List[str] = []
    max_results: int = 5

# ✅ Recommend endpoint
@app.post("/recommend")
async def recommend(candidate: Candidate):
    recs = recommend_internships(candidate.dict(), INTERNSHIPS, candidate.max_results)
    return {"recommendations": recs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
