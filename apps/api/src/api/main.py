from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.database import Base, engine
from api.equipment.routes import router as equipment_router
from api.material.routes import router as material_router
from api.verification.routes import router as verification_router


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="barbarbara", version="0.1.0", lifespan=lifespan)
app.include_router(material_router)
app.include_router(equipment_router)
app.include_router(verification_router)


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
