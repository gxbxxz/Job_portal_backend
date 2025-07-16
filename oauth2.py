from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import security.tokens as tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return tokens.verify_token(data, credentials_exception)



def get_current_recruiter(user: dict = Depends(get_current_user)):
    if user["role"] != "recruiter":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return user

def get_current_seeker(user: dict = Depends(get_current_user)):
    if user["role"] != "seeker":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return user