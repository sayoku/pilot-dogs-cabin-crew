# pilot-dogs-cabin-crew

Application built by World Studios at The Ohio State University for the Pilot Dogs network.

## Overview

Pilot Dogs Cabin Crew is an app meant to streamline the Q/A and training resources of the non-profit PilotDogs. PilotDogs trains guide dogs and equips their future owners with the necessary skills to handle them. Since the students using this app are visually impaired, this app is designed with accesibility at the forefront of the user experience. 

## Features

### Admin

- A profile on each dog
- Student Information
- Page with compiled questions that they can answer

### Co-Pilots

- Training materials
- Q/A chatbot built on a semantic database
- Profile for their dog

### Student/Graduates

- Calendar for the day(during the training)
- Q/A chatbot built on a semantic database
- Forum with other students in their cohort and then alumni network beyond graduation

## Prerequisites

## Installation

## Backend (Fast API)

Stub endpoints for every screen/view. 
Responses are hardcoded sample data(`sample_data.py`); nothing is saved yet. Swap in database calls inside the route functions later.

## Run

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Interactive docs: http://localhost:8000/docs

## Auth (stub)

Login/signup return a token like `stub-graduate`, `stub-copilot`, or `stub-admin`.
Send it as `Authorization: Bearer <token>`. `/home` and `/questions` need any
valid token. `/admin/*` needs `stub-admin`.

## Endpoints

| Screen | Endpoint |
|---|---|
| Sign in | `POST /auth/signup`, `POST /auth/login`, `POST /auth/google` |
| Home | `GET /home` |
| Ask a question | `GET /faqs/search?q=` |
| No match / ask a trainer | `POST /questions` |
| FAQ browse | `GET /topics`, `GET /faqs?topic_id=&q=`, `GET /faqs/{id}` |
| Training materials | `GET /training-materials?topic_id=`, `GET /training-materials/{id}` |
| Admin: answer questions | `GET /admin/questions?status=`, `POST /admin/questions/{id}/answer` |
| Admin: upload | `POST/PUT/DELETE /admin/training-materials`, `POST/PUT/DELETE /admin/faqs` |

## TODO

- Real password hashing and Google token verification
- Real JWT auth
- Database
