# AGENTS Rules

- Ask before Code
- One small task at a time
- Stop after each task and wait for approval
- Do not rename frozen endpoints:
  - POST /upload_generated
  - GET /queue
  - GET /next_image
  - POST /mark_shown
- Do not change env vars without approval
- Do not install heavy dependencies without approval
- Do not do large refactors
- Keep all changes incremental and rollback-safe
- Update CODEX_PROGRESS.md after each task