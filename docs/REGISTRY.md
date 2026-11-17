# REGISTRY.md

Everything that exists on `main` and how to use it. Only list things that are built. Read this before writing code. Update it after every task (see AGENTS.md section 5.2).

## API endpoints

All endpoints are stubs. Reads return hardcoded data from `backend/sampledata.py`. Writes echo the request back and save nothing. All are defined in `backend/main.py`. Interactive docs run at `http://localhost:8000/docs`.

Roles column: `any` needs no token, `signed in` needs any valid token, `admin` needs `stub-admin`. Send tokens as `Authorization: Bearer <token>`.

| METHOD | Path | Roles | Request | Response | Errors | Owner |
|---|---|---|---|---|---|---|
| POST | /auth/signup | any | `SignupRequest` | `AuthResponse` | 422 | Anna H |
| POST | /auth/login | any | `LoginRequest` | `AuthResponse` (always a graduate) | 422 | Anna H |
| POST | /auth/google | any | `GoogleLoginRequest` | `AuthResponse` | 422 | Anna H |
| GET | /home | signed in | none | `HomeResponse` | 401 | Anna H |
| GET | /topics | any | none | `list[Topic]` | none | Anna H |
| GET | /faqs/search | any | query `q` (required) | `list[Faq]`, empty means no match | 422 | Anna H |
| GET | /faqs | any | query `topic_id`, `q` (both optional) | `list[Faq]` | 422 | Anna H |
| GET | /faqs/{faq_id} | any | none | `Faq` | 404, 422 | Anna H |
| POST | /questions | signed in | `QuestionCreate` | `Question`, status 201 | 401, 422 | Anna H |
| GET | /training-materials | any | query `topic_id` (optional) | `list[TrainingMaterial]` | 422 | Anna H |
| GET | /training-materials/{material_id} | any | none | `TrainingMaterial` | 404, 422 | Anna H |
| GET | /admin/questions | admin | query `status` (`pending` or `answered`, optional) | `list[Question]` | 401, 403, 422 | Anna H |
| POST | /admin/questions/{question_id}/answer | admin | `AnswerCreate` | `Answer` | 401, 403, 404, 422 (422 also when `publish_to_faq` has no `topic_id`) | Anna H |
| POST | /admin/training-materials | admin | `TrainingMaterialCreate` | `TrainingMaterial`, status 201 | 401, 403, 422 | Anna H |
| PUT | /admin/training-materials/{material_id} | admin | `TrainingMaterialCreate` | `TrainingMaterial` | 401, 403, 404, 422 | Anna H |
| DELETE | /admin/training-materials/{material_id} | admin | none | empty, status 204 | 401, 403, 404 | Anna H |
| POST | /admin/faqs | admin | `FaqCreate` | `Faq`, status 201 | 401, 403, 422 | Anna H |
| PUT | /admin/faqs/{faq_id} | admin | `FaqCreate` | `Faq` | 401, 403, 404, 422 | Anna H |
| DELETE | /admin/faqs/{faq_id} | admin | none | empty, status 204 | 401, 403, 404 | Anna H |

Errors return `{"detail": "<message>"}`.

## Data shapes

There is no database yet. These Pydantic models in `backend/schemas.py` are the data shapes. Owner Anna H.

| Name | Fields |
|---|---|
| `Role` | `"graduate"`, `"copilot"`, or `"admin"` |
| `QuestionStatus` | `"pending"` or `"answered"` |
| `User` | `user_id: int`, `username: str`, `email: str`, `role: Role` |
| `SignupRequest` | `username: str`, `email: str`, `password: str`, `role: Role` |
| `LoginRequest` | `username_or_email: str`, `password: str` |
| `GoogleLoginRequest` | `id_token: str`, `role: Role \| None` (only needed on first sign in) |
| `AuthResponse` | `token: str`, `user: User` |
| `HomeResponse` | `role: Role`, `greeting: str`, `sections: list[str]` |
| `Topic` | `topic_id: int`, `topic_name: str`, `description: str` |
| `Faq` | `faq_id: int`, `topic_id: int`, `question_text: str`, `answer_text: str`, `date_created: str` |
| `FaqCreate` | `topic_id: int`, `question_text: str`, `answer_text: str` |
| `TrainingMaterial` | `material_id: int`, `topic_id: int`, `title: str`, `description: str`, `material_type: "video" \| "document"`, `content_url: str` |
| `TrainingMaterialCreate` | same as `TrainingMaterial` without `material_id` |
| `Question` | `question_id: int`, `user_id: int`, `question_text: str`, `contact_info: str \| None`, `status: QuestionStatus`, `date_created: str` |
| `QuestionCreate` | `question_text: str`, `contact_info: str \| None` (phone or email) |
| `Answer` | `answer_id: int`, `question_id: int`, `answer_text: str`, `approved: bool`, `date_created: str` |
| `AnswerCreate` | `answer_text: str`, `topic_id: int \| None`, `publish_to_faq: bool` (needs `topic_id` when true) |

FAQs and question answers are separate. An FAQ is public and browsable. An answer is a reply to one user's question, and becomes an FAQ only when `publish_to_faq` is true.

## Shared components, hooks, and utilities

Entry format is name, import path, props or params, one line example, owner.

### Backend

- `CurrentUser`, `from main import CurrentUser`, a route parameter type that requires any valid token and gives the `User`. `def home(user: CurrentUser): ...` Owner Anna H.
- `ADMIN_ONLY`, `from main import ADMIN_ONLY`, a dependency list that returns 401 without a token and 403 for non admins. `@app.get("/admin/x", dependencies=ADMIN_ONLY)` Owner Anna H.
- `search_faq(items, q)`, in `backend/main.py`, case insensitive substring match on question and answer text. `search_faq(FAQS, "boarding")` Owner Anna H.
- Sample data `TOPICS`, `FAQS`, `TRAINING_MATERIALS`, `QUESTIONS`, `from sampledata import FAQS`. Placeholder content only. Owner Anna H.

### Mobile

None yet.

## Environment variables

None yet. `backend/config.py` is a placeholder and reads nothing.

## Dependencies

| Package | Where | Why |
|---|---|---|
| `fastapi>=0.115` | `backend/requirements.txt` | Web framework for the API |
| `uvicorn[standard]>=0.30` | `backend/requirements.txt` | Server that runs the FastAPI app |

## Requests between areas

| Date | From | To | Request | Status |
|---|---|---|---|---|
| 2026-11-16 | Nipun | Anna H | Anyone can become admin. `/auth/signup` accepts `role: "admin"`, and any client can send `Bearer stub-admin` without signing up. Real auth needs staff approval for admin and co-pilot roles. Raised in the backend PR. | Open |

## Changelog

Newest at the top. Format is `date | who | area | what changed`.

2026-11-16 | Nipun | docs | AGENTS.md and REGISTRY.md updated to match the merged backend: layout, route and error rules, all 19 endpoints, data shapes, auth helpers, dependencies
