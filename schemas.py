from pydantic import BaseModel
from typing import Optional

# Job Schema
class JobBase(BaseModel):
    id: int
    title: str
    description: str
    company: str
    skills_required: str
    experience: str
    recruiter_id: int  # Linking job to a recruiter

# Job Application Schema
class ApplyBase(BaseModel):
    id: int
    name: str
    description_a: str
    seeker_id: int  # Linking application to a seeker
    job_id: int  # Linking application to a job

# Recruiter Schema
class RecuriterBase(BaseModel):
    id: int
    name: str
    email: str
    password: str

# Seeker Schema
class SeekerBase(BaseModel):
    id: int
    name: str
    email: str
    password: str  

# Login Schema
class Login(BaseModel):
    username: str
    password: str    

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Token Data Schema
class TokenData(BaseModel):
    email: Optional[str] = None  
