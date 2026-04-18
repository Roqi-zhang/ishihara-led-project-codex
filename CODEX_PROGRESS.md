# CODEX Progress

## Project background
- Graduation project for a mobile web experience connected to an LED display installation.
- Core user flow: upload image -> generate Ishihara-style image locally -> send to LED -> LED display queue -> leave a message -> print flow -> payment placeholder -> download digital image.
- Frontend pages are already fully implemented as standalone HTML files.
- Current Codex scope is no longer frontend generation. Current scope is frontend integration + minimal backend hookup only.

## Current status
- Frontend pages are already fully implemented as standalone HTML files.
- System is now entering Integration Phase.
- No new UI generation is required.
- Existing HTML pages must be preserved visually.
- Codex should only connect routing, state, and backend APIs.

## Confirmed baseline
- Supabase is already configured.
- `submissions` and `display_queue` tables already exist.
- `original-images` and `generated-images` buckets already exist.
- The Flask backend backbone is already runnable.
- `POST /upload_generated` has already been validated successfully.
- Frozen endpoints that must remain unchanged:
  - `POST /upload_generated`
  - `GET /queue`
  - `GET /next_image`
  - `POST /mark_shown`

## Frontend baseline
- Existing frontend pages currently live under `frontend/`
- Confirmed page files:
  - `frontend/1前端页面.html`
  - `frontend/2前端页面.html`
  - `frontend/3前端界面.html`
  - `frontend/4前端页面.html`
  - `frontend/5前端页面.html`
  - `frontend/6前端页面.html`

## Completed tasks
- Task 0: solidify repository rules and progress tracking.
- Previous frontend generation phase is considered complete outside Codex.
- Codex must now treat frontend UI as fixed.
- Git Task 1: connect the local repository to GitHub and establish the `codex/integration` baseline checkpoint with an explicit whitelist only.

## Next tasks
1. Task 1: inspect existing frontend pages and confirm integration points in Ask mode only.
2. Task 2: connect page routing flow (`reminders -> reflect -> translating -> resonance -> message -> inscribe`).
3. Task 3: implement cross-page state persistence with localStorage for:
   - `uploadedImage`
   - `generatedImage`
   - `submissionId`
   - `userMessage`
4. Task 4: connect Resonance page to `POST /upload_generated` only when user confirms via `Converge`.
5. Task 5: connect Message page submission to `POST /mark_shown`.
6. Task 6: implement Inscribe page download and print flow.
7. Task 7: add minimal error handling and toast fallback for missing state.
8. Task 8: verify full end-to-end flow without visual regressions.

## Risks
- Local Wi-Fi to Supabase HTTPS may be unstable.
- Network instability must not be misdiagnosed as backend logic failure.
- The project must stay incremental to avoid accidental changes to frozen interfaces or directory structure.
- Existing frontend HTML must not be overwritten or visually modified.
- Resonance page includes adjustable Ishihara conversion behavior, so backend upload must happen only after final user confirmation.

## Recovery
- Start every new step in Ask mode before any code changes.
- Make only one minimal task change at a time.
- Stop after each task and wait for user approval.
- Run the smallest relevant verification after each change.
- Use a clear checkpoint or commit message as the rollback anchor when approved.
- Keep `CODEX_PROGRESS.md` updated after every task.
