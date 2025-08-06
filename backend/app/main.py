from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.houses import router
from app.db.session import engine, Base

import sys
from pathlib import Path

# Add project root to python path
sys.path.append(str(Path(__file__).parent.parent))

Base.metadata.create_all(bind=engine)

app = FastAPI(title="House Rental API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", tags=["houses"])