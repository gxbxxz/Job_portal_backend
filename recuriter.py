from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db
import pydantic_schema.schemas as schemas
from database.models import Job, Recuriter,Apply
from sqlalchemy.orm import Session
import security.hashing as hashing
from security.oauth2 import get_current_user,get_current_recruiter

router = APIRouter(
    prefix="/recuriter",
    tags=['recuriter']
)

# Create Recruiter
@router.post("/jobs/create_recuirter")
def create_rec(request: schemas.RecuriterBase, db: Session = Depends(get_db)):
    db_rec = Recuriter(
        id=request.id,
        name=request.name,
        email=request.email,
        password=hashing.Hash.brycpt(request.password)
    )  
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)
    return db_rec

# Delete Recruiter
@router.delete("/jobs/delete_recuirter")
def delete_rec(request: str, db: Session = Depends(get_db)):
    db_rec = db.query(Recuriter).filter(Recuriter.email == request).first()
    if not db_rec:
        raise HTTPException(status_code=404, detail="Not found")
    
    db.delete(db_rec)
    db.commit()
    return {"message": "Deleted successfully"}

# Get All Recruiters
@router.get("/jobs/get_recuriter")
def get_rec(db: Session = Depends(get_db)):
    recs = db.query(Recuriter).all()
    return {"recuriter": recs}

# Create Job (Linked to Recruiter)
@router.post("/jobs/create_job",dependencies=[Depends(get_current_recruiter)])
def create_job(request: schemas.JobBase, recruiter_id: int, db: Session = Depends(get_db),get_current_user:schemas.RecuriterBase=Depends(get_current_user)):
    db_rec = db.query(Recuriter).filter(Recuriter.id == recruiter_id).first()
    if not db_rec:
        raise HTTPException(status_code=404, detail="Recruiter not found")

    db_job = Job(
        id=request.id,
        title=request.title,
        description=request.description,
        company=request.company,
        skills_required=request.skills_required,
        experience=request.experience,
        recruiter_id=recruiter_id  
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/jobs/delete_job",dependencies=[Depends(get_current_recruiter)])
def delete_job(id: int, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Not found")
    
    db.delete(db_job)
    db.commit()
    return {"message": "Deleted successfully"}

# Update Job
@router.put("/jobs/update_job")
def update_job(id: int, request: schemas.JobBase, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Not found")
    
    for key, value in request.model_dump().items():
        setattr(db_job, key, value)
    
    db.commit()
    db.refresh(db_job)
    return db_job

# Get All Jobs Posted by a Specific Recruiter
@router.get("/jobs/recruiter_jobs",dependencies=[Depends(get_current_recruiter)])
def get_recruiter_jobs(recruiter_id: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_recruiter)):
    jobs = db.query(Job).filter(Job.recruiter_id == recruiter_id).all()
    if not jobs:
        return {"message": "No jobs found for this recruiter"}
    
    return {"jobs": jobs}

@router.get("/jobs/get_applicants",dependencies=[Depends(get_current_recruiter)])
def get_applicant(recruiter_id:int, db:Session=Depends(get_db),current_user: dict = Depends(get_current_recruiter)):
    recruiter = db.query(Recuriter).filter(Recuriter.id == recruiter_id).first()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    
    jobs = db.query(Job).filter(Job.recruiter_id == recruiter_id).all()
    if not jobs:
        return {"message": "No jobs posted by this recruiter"}
    
    job_ids = [job.id for job in jobs]
    applicants = db.query(Apply).filter(Apply.job_id.in_(job_ids)).all()

    if not applicants:
        return {"message": "No applicants for the posted jobs"}

    return {"applicants": applicants}

