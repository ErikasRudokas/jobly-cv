import spacy
from pathlib import Path

from app.schemas import CvParseResponse, Education, PersonalDetails, WorkExperience

MODEL_PATH = Path("model")
nlp = spacy.load(MODEL_PATH)

def parse_text(text: str):
    doc = nlp(text)

    personal_details = PersonalDetails()
    education = []
    work_experience = []
    skills = []

    colleges = [ent for ent in doc.ents if ent.label_ == "College Name"]
    degrees = [ent for ent in doc.ents if ent.label_ == "Degree"]
    companies = [ent for ent in doc.ents if ent.label_ == "Companies worked at"]
    designations = [ent for ent in doc.ents if ent.label_ == "Designation"]
    other_entities = [ent for ent in doc.ents if ent.label_ in {"Name", "Email", "Skills"}]

    for ent in other_entities:
        if ent.label_ == "Name":
            personal_details.name = ent.text
        elif ent.label_ == "Email":
            personal_details.email = ent.text
        elif ent.label_ == "Skills":
            skills.append(ent.text)

    for college in colleges:
        closest_degree = None
        min_distance = float("inf")

        for degree in degrees:
            distance = abs(degree.start - college.start)
            if distance < min_distance and distance <= 10:
                min_distance = distance
                closest_degree = degree

        education.append(
            Education(
                institution=college.text,
                degree=closest_degree.text if closest_degree else None
            )
        )

    for company in companies:
        closest_designation = None
        min_distance = float("inf")

        for designation in designations:
            distance = abs(designation.start - company.start)
            if distance < min_distance and distance <= 10:
                min_distance = distance
                closest_designation = designation

        work_experience.append(
            WorkExperience(
                company=company.text,
                designation=closest_designation.text if closest_designation else None
            )
        )

    return CvParseResponse(
        personalDetails=personal_details,
        education=education,
        workExperience=work_experience,
        skills=list(set(skills))
    )
