from typing import Literal
from pydantic import BaseModel

Role = Literal["graduate", "copilot", "admin"] # Works like an enum
QuestionStatus = Literal["pending", "answered"]

# Mental model of a struct in C for each class
# Each is a named set of fields, inheriting from BaseModel 
    # Types are checked when data is filled in, built in json conversion, 

class User(BaseModel):
    user_id: int
    username: str
    email: str
    role: Role

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str
    role: Role  # chosen once at account creation

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class GoogleLoginRequest(BaseModel):
    id_token: str
    role: Role | None = None  # only needed on first sign-in

class AuthResponse(BaseModel):
    token: str
    user: User

class Topic(BaseModel):
    topic_id: int
    topic_name: str
    description: str

class Faq(BaseModel):
    faq_id: int
    topic_id: int
    question_text: str
    answer_text: str
    date_created: str

class FaqCreate(BaseModel):
    topic_id: int
    question_text: str
    answer_text: str

class TrainingMaterial(BaseModel):
    material_id: int
    topic_id: int
    title: str
    description: str
    material_type: Literal["video", "document"]
    content_url: str

class TrainingMaterialCreate(BaseModel):
    topic_id: int
    title: str
    description: str
    material_type: Literal["video", "document"]
    content_url: str

class QuestionCreate(BaseModel):
    question_text: str
    contact_info: str | None = None  # phone or email, optional

class Question(BaseModel):
    question_id: int
    user_id: int
    question_text: str
    contact_info: str | None = None
    status: QuestionStatus
    date_created: str

class AnswerCreate(BaseModel):
    answer_text: str
    topic_id: int | None = None
    publish_to_faq: bool = False  # if true, topic_id is required

class Answer(BaseModel):
    answer_id: int
    question_id: int
    answer_text: str
    approved: bool
    date_created: str

class HomeResponse(BaseModel):
    role: Role
    greeting: str
    sections: list[str]
