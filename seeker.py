from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from database.database import get_db
import pydantic_schema.schemas as schemas
from database.models import Job, Apply, Seeker
from sqlalchemy.orm import Session
import json
import os
import security.hashing as hashing
from security.oauth2 import get_current_seeker,get_current_user


router = APIRouter(
    prefix="/seeker",
    tags=['seeker']
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):  
    os.makedirs(UPLOAD_DIR)

# Create Seeker Account
@router.post("/jobs/create_seeker")
def create_seek(request: schemas.SeekerBase, db: Session = Depends(get_db)):
    db_sek = Seeker(
        id=request.id,
        name=request.name,
        email=request.email,
        password=hashing.Hash.brycpt(request.password)
    )
    db.add(db_sek)
    db.commit()
    db.refresh(db_sek)
    return db_sek

# Delete Seeker Account
@router.delete("/jobs/delete_seeker")
def delete_seek(email: str, db: Session = Depends(get_db)):
    db_seek = db.query(Seeker).filter(Seeker.email == email).first()
    if not db_seek:
        raise HTTPException(status_code=404, detail="Seeker not found")
    
    db.delete(db_seek)
    db.commit()
    return {"message": "Deleted successfully"}

# Get All Seekers
@router.get("/jobs/get_seeker")
def get_seekers(db: Session = Depends(get_db)):
    seekers = db.query(Seeker).all()
    return {"seekers": seekers}

# Apply for a Job
@router.post("/jobs/apply_job",dependencies=[Depends(get_current_seeker)])
def apply_job(
    request: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_seeker)
):
    data = json.loads(request)

    # Ensure job exists
    job = db.query(Job).filter(Job.id == data["job_id"]).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Ensure seeker exists
    seeker = db.query(Seeker).filter(Seeker.id == data["seeker_id"]).first()
    if not seeker:
        raise HTTPException(status_code=404, detail="Seeker not found")

    # Save Resume File
    file_location = f"{UPLOAD_DIR}/{resume.filename}"
    with open(file_location, "wb") as f:
        f.write(resume.file.read())

    # Create Job Application Entry
    db_apply = Apply(
        id=data["id"],
        name=data["name"],
        description_a=data["description_a"],
        resume_path=file_location,
        job_id=data["job_id"],  # Linking application to job
        seeker_id=data["seeker_id"]  # Linking application to seeker
    )

    db.add(db_apply)
    db.commit()
    db.refresh(db_apply)
    return db_apply

# Search Jobs by Keyword
@router.get("/jobs/search/key",dependencies=[Depends(get_current_seeker)])
def search_keyword(key: str, db: Session = Depends(get_db),current_user: dict = Depends(get_current_seeker)):
    jobs = db.query(Job).filter(
        (Job.title.ilike(f"%{key}%")) |
        (Job.description.ilike(f"%{key}%")) |
        (Job.skills_required.ilike(f"%{key}%"))
    ).all()

    if not jobs:
        return {"message": "No jobs found"}
    
    return jobs

# Get All Jobs
@router.get("/jobs/get_jobs")
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return {"jobs": jobs}
