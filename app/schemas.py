from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class PersonalDetails(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None

class WorkExperience(BaseModel):
    company: Optional[str] = None
    designation: Optional[str] = None

class CvParseResponse(BaseModel):
    personalDetails: PersonalDetails
    education: List[Education]
    workExperience: List[WorkExperience]
    skills: List[str]
