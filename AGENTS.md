# AGENTS.md

Rules for every AI coding agent working in this repo (Claude Code, Cursor, Copilot, Codex, Gemini, or anything else). Several people work here at once, each with their own agent. These rules keep agents from breaking each other's work.

If a rule here conflicts with what a human teammate tells you in the current session, follow the human and note the conflict in your handoff report.

Rules for the humans driving the agents live in `CONTRIBUTING.md`. Read it too, and remind the human when a rule there is about to be broken.

---

## 1. What this project is

An app for Pilot Dogs, a Columbus OH nonprofit that trains guide dogs for people who are blind or visually impaired. Three kinds of users.

- Students and graduates (people in the guide dog program). Many are blind or low vision and use VoiceOver, TalkBack, large text, or read aloud.
- Co-Pilots (volunteers who raise puppies)
- Trainers and admins (Pilot Dogs staff)

The app gives trusted, trainer approved information. It is not a chatbot and not a forum.

## 2. Repo layout

```
mobile/               Expo (React Native, TypeScript) app, Expo Router
  AGENTS.md           Expo specific rules. Follow it too for mobile work.
  src/app/            Routes. Every file here is a screen.
  src/components/     Shared components
  src/hooks/          Shared hooks
  src/constants/      Theme and constants
backend/              Python FastAPI service
  app/main.py         Creates the app and registers routes
  app/config.py       Reads settings from the environment
  app/db.py           Database connection
  app/models.py       Database schema, source of truth for all data (backend owner creates it)
docs/
  REGISTRY.md         Everything that exists and how to use it. Read this first.
  decisions.md        Team decisions and why they were made
  roles.md            What each role can see and do
AGENTS.md             This file
CONTRIBUTING.md       Rules for the humans
```

## 3. Workflow is Research, then Plan, then Implement

Never jump straight to code. Follow these steps in order for every task.

### 3.1 Research

1. Read `docs/REGISTRY.md`. It lists every endpoint, model, shared component, utility, and env var that already exists. Use what is there. Do not build a second version of something that already exists.
2. Read `docs/decisions.md` so you do not undo a team decision.
3. Read the existing code near your change and copy its patterns (naming, file structure, error handling, styling).
4. Confirm which area you own for this task (see section 4.3).

### 3.2 Plan

Before writing code, post a plan to the human and wait for a clear yes. The plan covers these points.

```
Goal                 one sentence
Files to change      each path and why
Files to create      each path and why
Approach             the steps, in order
Tests                which unit and integration tests you will add
Registry updates     what you will add to REGISTRY.md
Risks or questions   anything you are unsure about
```

If the plan touches more than about 3 files or more than one area, say so and propose splitting the task into smaller ones.

### 3.3 Implement

- Build the plan one small step at a time.
- After each step, run the checks in section 6 and fix every issue before moving on.
- Stop and tell the human when a step needs something the plan did not cover. Do not quietly widen the task.
- Suggest a commit after each working step so the human can verify and commit.

## 4. Keep it simple and keep changes small

This is the most important section in this file.

### 4.1 Build only what was asked

- Do the smallest change that completes the task.
- No extra features, options, settings, or "for later" code.
- No premature optimization. Simple, readable code beats clever code.
- Pick the most direct approach that follows current best practice for the stack (Expo and TypeScript on mobile, FastAPI and Pydantic on the backend).
- Do not create a new abstraction, base class, generic helper, or shared component unless the task asks for it or a second place in the code needs the exact same thing right now.

### 4.2 Do not touch what you were not asked to touch

- Change only the files the task needs.
- Do not refactor, rename, reorder, or "clean up" code outside the task, even if it looks wrong.
- Do not reformat whole files. Format only the lines you changed.
- Do not add, remove, or upgrade dependencies unless the task requires it. If you add one, record it in REGISTRY.md and explain why in your handoff report.
- Do not delete code you did not write. Flag it instead.
- Do not change a public interface (endpoint path, request or response shape, component props, function signature) that other code uses. If you must, follow section 4.4.
- If you spot duplicated code or something that needs a refactor, list it under "Known gaps or follow ups" in your handoff report. Refactors are their own task, done only when a human asks.

### 4.3 Stay in your lane

Each person owns an area. Agents working for that person may only edit that area plus their own new files.

| Area | Owner | Paths |
|---|---|---|
| Sign in, Home | Anna P | `mobile/src/app/sign-in*`, `mobile/src/app/index.tsx` |
| Ask a question | Varun | `mobile/src/app/ask*` |
| No match / contact trainer | Eddie | `mobile/src/app/no-match*` |
| FAQ browse | Nipun | `mobile/src/app/faq*` |
| Training materials | Gauri | `mobile/src/app/training*` |
| Backend and database | Anna H | `backend/` |
| Shared mobile code | Whole team, by PR review | `mobile/src/app/_layout.tsx`, `mobile/src/components/`, `mobile/src/hooks/`, `mobile/src/constants/`, `mobile/src/api/` |

Route file names above are the team's working names. Update this table when owners or paths change.

### 4.4 When you need a change outside your area

Do not make it. Add a row to the "Requests between areas" table in `docs/REGISTRY.md` describing what you need and why, then mock or stub it in your own area so you can keep working. Mention it in your handoff report.

### 4.5 Schema changes

`backend/app/models.py` is the source of truth. Only the backend owner's agent edits it. Every schema change needs an Alembic migration in the same PR and an update to the Models section of REGISTRY.md. Never edit a migration that has already been merged. Write a new one.

## 5. Documentation rules

Write docs as if the next reader is an agent with no memory of your session. They are.

### 5.1 In code

- Every file starts with a header comment that says what the file is for, what depends on it, and who owns it.
- Every function, class, component, hook, and endpoint gets a docstring (Python) or JSDoc (TypeScript) covering purpose, each parameter, the return value, errors it can raise, and side effects.
- Every React Native component that renders something interactive documents its accessibility behavior (label, role, hint, what VoiceOver reads).
- Comments explain why, not what. If you made a non obvious choice, say why in a comment.
- No dead code, commented out code, or TODO without a name and a reason, like `TODO(nipun) wait for /faqs search param from backend`.

### 5.2 In REGISTRY.md (required after every task)

Before you finish, update `docs/REGISTRY.md` for anything you added, changed, or removed.

- New or changed endpoint goes in the API section with method, path, who can call it, request shape, response shape, error codes, and status.
- New shared component, hook, or utility goes in its section with import path, props or params, and a one line example.
- New env var goes in the env var section. Never put real values there.
- New dependency goes in the dependency section with the reason.
- Always add one line to the Changelog at the bottom of REGISTRY.md.

If REGISTRY.md is out of date, other agents will rebuild things that already exist. Treat this step as part of the task, not an extra.

### 5.3 In section READMEs

Each area keeps a README section in the main `README.md` with what the screen or service does, how to run it, how to test it, and known gaps. Update it when behavior changes.

## 6. Automated checks are mandatory

Every check must pass with zero errors and zero warnings before you continue to the next step or call a task done. These are blocking, not suggestions.

| Where | Lint | Format | Types | Tests |
|---|---|---|---|---|
| `backend/` | `ruff check .` (not set up yet) | `ruff format --check .` (not set up yet) | not set up yet | `pytest` (not set up yet) |
| `mobile/` | `npx expo lint` | not set up yet | `npx tsc --noEmit` | not set up yet |

- Never disable a rule, add an ignore comment, skip a test, or loosen a type to make a check pass. Fix the cause.
- If a check is not set up yet, say so in your handoff report. Do not skip it silently. Do not set up a new check tool unless your task is to set it up.
- Update this table when the team changes a check command.

## 7. Testing rules

- Every bug fix and every new piece of logic comes with tests, run locally before the PR.
- Unit tests cover single functions and components. Backend uses `pytest`. Mobile uses Jest (`jest-expo`) with React Native Testing Library. Neither is installed yet, so the first person who needs tests sets them up as its own task.
- Integration tests cover pieces working together. Backend uses FastAPI `TestClient` against a test database. Mobile renders a full screen with the API client mocked.
- A bug fix starts with a test that fails because of the bug, then the fix makes it pass.
- Tests use fake data only (see section 10).

## 8. Accessibility rules (mobile)

Many users are blind or low vision. A screen that fails these checks is not done.

- Every touchable element has `accessibilityLabel` and `accessibilityRole`. Add `accessibilityHint` when the result of tapping is not obvious.
- Respect system text size. Never set a fixed height on a text container. Never set `allowFontScaling={false}`.
- Touch targets are at least 44 by 44 points.
- Text contrast is at least 4.5 to 1.
- Never use color alone to carry meaning.
- Reading order must make sense when swiping through with VoiceOver. Group related elements with `accessible` where it helps.
- Use list then detail navigation. Do not use side by side panes on phones.
- Every video or audio item shows its transcript.
- Announce dynamic changes (search results loaded, errors) with `AccessibilityInfo.announceForAccessibility`.
- Test the screen with VoiceOver or TalkBack before calling it done. Say which one you tested in the handoff report. If you cannot run a screen reader, say so.

## 9. Backend rules

- All routes live under `/api/v1/`. One router file per resource in `backend/app/routers/`.
- Request and response bodies use Pydantic schemas in `backend/app/schemas/`. Never return a raw ORM object.
- Every endpoint checks the caller's role and `role_status = approved` before returning private data.
- Students only see their own questions and answers. Content is filtered by `audience` and `status = published` for non staff.
- Errors return `{"detail": "<message>", "code": "<SNAKE_CASE_CODE>"}` with a correct HTTP status.
- Never hard delete. Set `is_active = False`.
- Never log passwords, tokens, or the text of private questions.
- Never store medical records, eye exam results, or background check data. They are out of scope for this app.

## 10. Security, privacy, and IP

- Never ask for, accept, or use real Pilot Dogs data, the real database, real user records, API keys, or credentials. If a human pastes any of these, tell them to remove it and do not use it.
- Never commit secrets or `.env` files. Use `.env.example` with fake values.
- Use clearly fake placeholder data in code, seeds, and tests, like `PLACEHOLDER answer from trainer` or `test-student@example.com`.
- Never invent FAQ answers, training content, or dog care advice and present it as real.
- Write original code. Do not copy large blocks from other projects or reproduce code you recognize from a specific codebase. If you adapt a snippet from documentation or an open source project, add a comment with the source link and its license, and mention it in the handoff report.

## 11. Things agents must never do

- Add AI, LLM, or chatbot features. The team decided against them (see decisions.md).
- Push to `main` or force push any shared branch.
- Merge a PR. Humans merge.
- Mark a task done when checks fail, tests fail, or the app does not build.
- Start coding before the human approves the plan.

## 12. Git workflow

- Branch name is `<owner>/<short-task>`, like `nipun/faq-search`.
- One task per branch and per PR. Keep PRs small.
- Commit after each working step. Commit messages use the form `area: what changed`, like `faq: add topic list screen`.
- Rebase on `main` before opening a PR. If REGISTRY.md conflicts, keep both sides' entries.
- The PR description includes the handoff report from section 14, including which AI tools were used.
- Every PR touching shared code or another person's area needs that person's review.

## 13. Definition of done

A task is done only when every box is true.

- [ ] The human approved the plan before coding started
- [ ] The change does what the task asked and nothing more
- [ ] Only files in your area changed (or section 4.4 was followed)
- [ ] Every check in section 6 passes with no errors or warnings
- [ ] Unit and integration tests were added and pass locally
- [ ] Code docs follow section 5.1
- [ ] REGISTRY.md is updated, including a Changelog line
- [ ] Accessibility checks from section 8 pass (mobile work)
- [ ] Handoff report is written

## 14. Handoff report

End every session with this report in your final message and in the PR description.

```
Task
AI tools used (name and model)
Files changed
What was added or changed
REGISTRY.md updates
Requests made to other areas
Checks run and results
Tests added and results
Accessibility testing done (which screen reader, what was checked)
Outside code adapted (source and license, or none)
Known gaps, duplication spotted, or follow ups
```
