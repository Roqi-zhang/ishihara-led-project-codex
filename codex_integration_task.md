# Codex Integration Task

You are now entering a NEW PHASE: Integration Phase.

## STRICT RULES
- DO NOT generate UI
- DO NOT redesign pages
- DO NOT change layout, styles, copy, or visual structure
- DO NOT replace existing HTML files
- DO NOT create alternative replacement pages
- ONLY handle logic integration

Ignore ALL previous frontend generation instructions.

---

## PROJECT CONTEXT

This is an interactive public art system (Ishihara LED installation).

Frontend pages are already fully designed and already exist as standalone HTML files.

Expected files:

- frontend/1前端页面.html
- frontend/2前端页面.html
- frontend/3前端页面.html
- frontend/4前端页面.html
- frontend/5前端页面.html
- frontend/6前端页面.html

Treat these pages as fixed visual assets.

---

## PAGE MAPPING

The existing page files correspond to this flow:

- `frontend/1前端页面.html` = Reminders
- `frontend/2前端页面.html` = Reflect
- `frontend/3前端页面.html` = Translating
- `frontend/4前端页面.html` = Resonance
- `frontend/5前端页面.html` = Message
- `frontend/6前端页面.html` = Inscribe

Do not rename these files unless explicitly asked.

---

## UPDATED USER FLOW

`frontend/1前端页面.html`
→ `frontend/2前端页面.html`
→ `frontend/3前端页面.html`
→ `frontend/4前端页面.html`
→ `frontend/5前端页面.html`
→ `frontend/6前端页面.html`

---

## CORE CHANGE (VERY IMPORTANT)

Resonance page is now INTERACTIVE.

- It is NOT a static result page anymore
- It includes parameter controls
- Image updates in real-time

Upload to backend MUST happen ONLY after user confirms.

---

## GLOBAL STATE (localStorage)

Use localStorage for cross-page state.

Required keys:

- `uploadedImage`
- `generatedImage`
- `submissionId`
- `userMessage`
- `currentStep`

---

## API ENDPOINTS

Do not rename or change backend endpoints.

- `POST /upload_generated`
- `GET /queue`
- `GET /next_image`
- `POST /mark_shown`

---

## YOUR TASKS

### 1. ROUTING

Use:

```js
window.location.href

Flow:

frontend/1前端页面.html
frontend/2前端页面.html
frontend/3前端页面.html
frontend/4前端页面.html
frontend/5前端页面.html
frontend/6前端页面.html

Do not introduce frameworks.

2. PAGE 2 = REFLECT PAGE (frontend/2前端页面.html)

After user uploads image:

convert uploaded image to base64 if needed
save to:
localStorage.setItem("uploadedImage", base64);
localStorage.setItem("currentStep", "translating");
navigate to:
window.location.href = "3前端页面.html";

Do NOT call backend here.

3. PAGE 3 = TRANSLATING PAGE (frontend/3前端页面.html)

On page load:

read localStorage.uploadedImage
if missing:
show toast
redirect to:
window.location.href = "2前端页面.html";
if present:
run a timed transition / loading state for 2–3 seconds
then:
localStorage.setItem("currentStep", "resonance");
window.location.href = "4前端页面.html";

Do NOT call backend here.

4. PAGE 4 = RESONANCE PAGE (frontend/4前端页面.html) (CRITICAL LOGIC)

This page already contains:

Ishihara generator
parameter controls
real-time canvas update

IMPORTANT:

DO NOT modify the generator algorithm
DO NOT remove controls
DO NOT upload on every parameter change
DO NOT upload on first render
REAL-TIME BEHAVIOR

When user adjusts parameters:

regenerate image in canvas
DO NOT call API
DO NOT store permanently
FINAL CONFIRM ACTION

When user clicks “汇聚 Converge”:

take current canvas result
convert to base64
save:
localStorage.setItem("generatedImage", imageBase64);
localStorage.setItem("currentStep", "message");
call API:
POST /upload_generated
{
  "imageBase64": "<generatedImage>",
  "originalImageBase64": "<uploadedImage>",
  "symbol": "74",
  "sourceName": "web"
}
get response:
extract submission.id if available
save:
localStorage.setItem("submissionId", submissionId);
show toast:

已汇聚，请留步观看
All has converged. Stay to witness.

navigate to:
window.location.href = "5前端页面.html";
5. PAGE 5 = MESSAGE PAGE (frontend/5前端页面.html)

On page load:

read localStorage.generatedImage
if missing:
show toast
redirect to:
window.location.href = "4前端页面.html";

When user submits message:

save:
localStorage.setItem("userMessage", message);
localStorage.setItem("currentStep", "inscribe");
call:
POST /mark_shown
{
  "submission_id": "<submissionId>",
  "message": "<userMessage>"
}
navigate to:
window.location.href = "6前端页面.html";
6. PAGE 6 = INSCRIBE PAGE (frontend/6前端页面.html)

On page load:

read localStorage.generatedImage
if missing:
show toast
redirect to:
window.location.href = "4前端页面.html";

Display image.

BUTTONS:

Download
download generatedImage as PNG
Print
open print-friendly popup/window
show only the image
then trigger:
window.print();

Do not redesign the page.

API HELPER

Create the smallest possible reusable API helper.

Prefer one shared helper instead of repeated fetch logic.

Example:

async function apiPost(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error("Request failed");
  return res.json();
}

Keep it minimal.

ERROR HANDLING

If required data is missing:

show toast
do not use alert
do not crash
redirect to the correct page
DO NOT DO
DO NOT upload image during parameter change
DO NOT auto-upload
DO NOT regenerate UI
DO NOT remove controls
DO NOT merge all pages into one file
DO NOT convert project to React/Vue/Next
DO NOT rename the current HTML files
GOAL

Make full system work:

Upload → Adjust → Confirm → Upload → Message → Download/Print

DONE WHEN
Existing HTML pages remain visually intact
Routing works correctly across all 6 existing files
localStorage works across pages
Resonance uploads only after final confirmation
Message submits correctly
Inscribe supports download and print
The full flow works end-to-end without manual refresh
WORKING STYLE
Ask before Code
One small task at a time
Stop after each task
Update CODEX_PROGRESS.md after each task