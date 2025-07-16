from fastapi import FastAPI
from database.database import SessionLocal,engine,Base
import database.models as models
from router import recuriter,seeker,authentication
app=FastAPI()


models.Base.metadata.create_all(bind=engine)

@app.get("/")
def basic():
    return {"response":200}

app.include_router(recuriter.router)
app.include_router(seeker.router)
app.include_router(authentication.router)




