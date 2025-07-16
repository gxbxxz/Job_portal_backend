from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from pydantic_schema.schemas import Login
from database.models import Seeker,Recuriter
from security.hashing import Hash
import security.tokens as tokens
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter(
    tags=['Authentication']
)

@router.post("/login")
@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Seeker).filter(Seeker.email == request.username).first()
    if not user:
        user = db.query(Recuriter).filter(Recuriter.email == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")

    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    access_token = tokens.create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

    

