from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import recommend

app = FastAPI(title="PM Internship Recommender")

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routes
app.include_router(recommend.router)

# ✅ Root route
@app.get("/")
async def root():
    return {"message": "PM Internship Recommender API is running 🚀"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
