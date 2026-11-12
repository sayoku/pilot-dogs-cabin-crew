from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException
from sample_data import FAQS, QUESTIONS, TOPICS, TRAINING_MATERIALS
#Note: still has placeholders in the functions
#Need to secure down admin, right now, anyone can mark themselves as admin
#Team should be able to assign admins only, or some kind of verification/approval

from schemas import (
    Answer,
    AnswerCreate,
    AuthResponse,
    Faq,
    FaqCreate,
    GoogleLoginRequest,
    HomeResponse,
    LoginRequest,
    Question,
    QuestionCreate,
    QuestionStatus,
    SignupRequest,
    Topic,
    TrainingMaterial,
    TrainingMaterialCreate,
    User,
)

app = FastAPI(title="Pilot Dogs Cabin Crew API")

# Auth helpers (STUB: tokens look like "stub-<role>". Replace with real JWTs.)

def get_current_user(authorization: str = Header(default="")) -> User:
    token = authorization.removeprefix("Bearer ").strip()
    if not token.startswith("stub-"):
        raise HTTPException(status_code=401, detail="Not authenticated")
    role = token.removeprefix("stub-")
    if role not in ("graduate", "copilot", "admin"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(
        user_id=1, username=f"sample_{role}", email=f"{role}@example.com", role=role
    )

CurrentUser = Annotated[User, Depends(get_current_user)]

def require_admin(user: CurrentUser) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user

ADMIN_ONLY = [Depends(require_admin)]

# Sign in

#sign up page 
@app.post("/auth/signup", response_model=AuthResponse)
def signup(body: SignupRequest):
    # TODO: hash body.password and save the user to the database
    user = User(user_id=1, username=body.username, email=body.email, role=body.role)
    return AuthResponse(token=f"stub-{body.role}", user=user)

#sign in page for exisitng users
@app.post("/auth/login", response_model=AuthResponse)
def login(body: LoginRequest):
    # TODO: look up user and verify the password hash. Stub logs in as a graduate.
    user = User(
        user_id=1,
        username=body.username_or_email,
        email="graduate@example.com",
        role="graduate",
    )
    return AuthResponse(token="stub-graduate", user=user)

#use google to log in
@app.post("/auth/google", response_model=AuthResponse)
def google_login(body: GoogleLoginRequest):
    # TODO: verify body.id_token with Google, then find or create the user
    role = body.role or "graduate"
    user = User(
        user_id=1, username="google_user", email="google@example.com", role=role
    )
    return AuthResponse(token=f"stub-{role}", user=user)

# Home

#Split out sections
HOME_SECTIONS = {
    "graduate": ["Ask a question", "FAQ browse"],
    "copilot": ["Ask a question", "FAQ browse", "Training materials"],
    "admin": ["Answer questions", "Upload"],
}

#get home for the user
@app.get("/home", response_model=HomeResponse)
def home(user: CurrentUser):
    return HomeResponse(
        role=user.role,
        greeting=f"Welcome, {user.username}",
        sections=HOME_SECTIONS[user.role],
    )

# Ask a question / FAQ browse

#simple substring matching, will need to find a better way to do this
def search_faq(items: list[dict], q: str) -> list[dict]:
    q = q.lower()
    return [
        f
        for f in items
        if q in f["question_text"].lower() or q in f["answer_text"].lower()
    ]

#get topics endpoint
@app.get("/topics", response_model=list[Topic])
def list_topics():
    return TOPICS

#search existing faqs
@app.get("/faqs/search", response_model=list[Faq])
def faq_search(q: str):
    """Ask a question screen: empty result means show 'No match / ask a trainer'."""
    return search_faq(FAQS, q)

#list faqs
@app.get("/faqs", response_model=list[Faq])
def list_faq(topic_id: int | None = None, q: str | None = None):
    faqs = FAQS
    if topic_id is not None:
        faqs = [f for f in faqs if f["topic_id"] == topic_id]
    if q:
        faqs = search_faq(faqs, q)
    return faqs

#get faq by the faq ID
@app.get("/faqs/{faq_id}", response_model=Faq)
def get_faq(faq_id: int):
    for faq in FAQS:
        if faq["faq_id"] == faq_id:
            return faq
    raise HTTPException(status_code=404, detail="FAQ not found")

# No match / ask a trainer

#submit question, basic idea, with placeholders!!
@app.post("/questions", response_model=Question, status_code=201)
def submit_question(body: QuestionCreate, user: CurrentUser):
    # TODO: save to the database
    return Question(
        question_id=99,
        user_id=user.user_id,
        question_text=body.question_text,
        contact_info=body.contact_info,
        status="pending",
        date_created="2026-11-11",
    )

# Training materials

#list out training materials for copilots, by topic
@app.get("/training-materials", response_model=list[TrainingMaterial])
def list_materials(topic_id: int | None = None):
    if topic_id is None:
        return TRAINING_MATERIALS
    return [m for m in TRAINING_MATERIALS if m["topic_id"] == topic_id]

#specific material with the id
@app.get("/training-materials/{material_id}", response_model=TrainingMaterial)
def get_material(material_id: int):
    for material in TRAINING_MATERIALS:
        if material["material_id"] == material_id:
            return material
    raise HTTPException(status_code=404, detail="Material not found")

# Admin (all writes are STUBS: they echo back data but do not persist anything)
# Also, question answers and FAQ's are separate entities. FAQs are browse-able
# Question answers are a reply to a specific user

#under admin, see the list of questions
@app.get("/admin/questions", response_model=list[Question], dependencies=ADMIN_ONLY)
def admin_list_questions(status: QuestionStatus | None = None):
    if status is None:
        return QUESTIONS
    return [q for q in QUESTIONS if q["status"] == status]

#post answer to specific question, keeping in mind placeholders
@app.post(
    "/admin/questions/{question_id}/answer",
    response_model=Answer,
    dependencies=ADMIN_ONLY,
)
def admin_answer_question(question_id: int, body: AnswerCreate):
    if not any(q["question_id"] == question_id for q in QUESTIONS):
        raise HTTPException(status_code=404, detail="Question not found")
    if body.publish_to_faq and body.topic_id is None:
        raise HTTPException(
            status_code=422, detail="topic_id required to publish to FAQ"
        )
    # TODO: save answer, mark question answered, create FAQ if publish_to_faq
    return Answer(
        answer_id=99,
        question_id=question_id,
        answer_text=body.answer_text,
        approved=body.publish_to_faq,
        date_created="2026-11-11",
    ) 

#create training materials on their own
@app.post(
    "/admin/training-materials",
    response_model=TrainingMaterial,
    status_code=201,
    dependencies=ADMIN_ONLY,
)
def admin_create_material(body: TrainingMaterialCreate):
    return TrainingMaterial(material_id=99, **body.model_dump())

#update a specific training material
@app.put(
    "/admin/training-materials/{material_id}",
    response_model=TrainingMaterial,
    dependencies=ADMIN_ONLY,
)
def admin_update_material(material_id: int, body: TrainingMaterialCreate):
    if not any(m["material_id"] == material_id for m in TRAINING_MATERIALS):
        raise HTTPException(status_code=404, detail="Material not found")
    return TrainingMaterial(material_id=material_id, **body.model_dump())

#delete training material
@app.delete(
    "/admin/training-materials/{material_id}",
    status_code=204,
    dependencies=ADMIN_ONLY,
)
def admin_delete_material(material_id: int):
    if not any(m["material_id"] == material_id for m in TRAINING_MATERIALS):
        raise HTTPException(status_code=404, detail="Material not found")

# FAQ related ---- 

#only admins can create faqs, here is how you create it. With placeholders
@app.post("/admin/faqs", response_model=Faq, status_code=201, dependencies=ADMIN_ONLY)
def admin_create_faq(body: FaqCreate):
    return Faq(faq_id=99, date_created="2026-11-11", **body.model_dump())

#updating previously created FAQ
@app.put("/admin/faqs/{faq_id}", response_model=Faq, dependencies=ADMIN_ONLY)
def admin_update_faq(faq_id: int, body: FaqCreate):
    if not any(f["faq_id"] == faq_id for f in FAQS):
        raise HTTPException(status_code=404, detail="FAQ not found")
    return Faq(faq_id=faq_id, date_created="2026-11-11", **body.model_dump())

#delete an faq
@app.delete("/admin/faqs/{faq_id}", status_code=204, dependencies=ADMIN_ONLY)
def admin_delete_faq(faq_id: int):
    if not any(f["faq_id"] == faq_id for f in FAQS):
        raise HTTPException(status_code=404, detail="FAQ not found")
    