# AGENTS Rules

## Core workflow

- Ask before Code.
- One small task at a time.
- Stop after each task and wait for approval.
- Keep every change incremental, testable, and rollback-safe.
- Update `CODEX_PROGRESS.md` after each task.

## Current phase

- The project is now in **Integration Phase**.
- Existing frontend HTML pages are already implemented.
- Do not generate new frontend UI.
- Do not redesign or replace existing pages.
- Frontend work must focus only on:
  - page routing
  - state persistence
  - API integration
  - minimal glue logic
  - verification

## Frozen endpoints

Do not rename or break these backend endpoints:

- `POST /upload_generated`
- `GET /queue`
- `GET /next_image`
- `POST /mark_shown`

## Safety boundaries

- Do not change env vars without approval.
- Do not expose secrets, service keys, or `.env` values.
- Do not install heavy dependencies without approval.
- Do not do large refactors.
- Do not make large directory restructures.
- Do not modify the database schema without approval.
- Do not rebuild Supabase or replace the current Flask backbone.
- Do not modify existing frontend UI, layout, or visual structure.
- Do not regenerate or replace existing HTML pages.
- Do not convert the project to React, Vue, or another framework.
- Do not merge all pages into one file unless explicitly approved.

## Execution rules

- New endpoints must be proposed in Ask mode before implementation.
- Frontend work must adapt to the frozen backend interfaces.
- Existing frontend pages should be treated as fixed assets.
- Use localStorage/sessionStorage only when needed for cross-page state.
- Prefer minimal reusable JS helpers for integration.
- Keep routing simple and explicit.
- Any backend-facing change must be minimal and reversible.

## Frontend integration targets

Current frontend pages should be connected in this flow:

- `page-reminders.html`
- `page-reflect.html`
- `page-translating.html`
- `page-resonance.html`
- `page-message.html`
- `page-inscribe.html`

Expected integration responsibilities:

- connect navigation between pages
- persist uploaded image / generated image / message
- call backend APIs at the correct hook points
- preserve all existing page visuals

## After each task, report

- what changed
- which files changed
- how to verify
- the expected result
- exactly one suggested next task