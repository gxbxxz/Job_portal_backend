from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Recuriter(Base):
    __tablename__ = "Recruiter" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String, index=True)
    jobs = relationship("Job", back_populates="recruiter")
    role = Column(String, default="recruiter")


class Job(Base):
    __tablename__ = "Job"  

    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String, index=True)
    description = Column(String, index=True)
    company = Column(String, index=True)
    skills_required = Column(String, index=True)
    experience = Column(String, index=True)

    recruiter_id = Column(Integer, ForeignKey("Recruiter.id"))  
    recruiter = relationship("Recuriter", back_populates="jobs")
    applications = relationship("Apply", back_populates="job")


class Seeker(Base):
    __tablename__ = "Seek" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String, index=True)
    applications = relationship("Apply", back_populates="seeker")
    role = Column(String, default="seeker")


class Apply(Base):
    __tablename__ = "Applied"  

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description_a = Column(String, index=True)
    resume_path = Column(String, nullable=False)

    job_id = Column(Integer, ForeignKey("Job.id"))  
    seeker_id = Column(Integer, ForeignKey("Seek.id"))  

    job = relationship("Job", back_populates="applications")
    seeker = relationship("Seeker", back_populates="applications")
