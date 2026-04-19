import os
import base64
import uuid
from datetime import datetime, timezone

import httpx
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client, ClientOptions

# =========================
# 基础配置
# =========================
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("缺少 SUPABASE_URL 或 SUPABASE_KEY，请检查 backend/.env 文件")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    options=ClientOptions(
        httpx_client=httpx.Client(trust_env=False, timeout=30.0)
    ),
)

app = Flask(__name__)
CORS(app)

DISPLAY_SECONDS = 5

ORIGINAL_BUCKET = "original-images"
GENERATED_BUCKET = "generated-images"


# =========================
# 工具函数
# =========================
def now_iso():
    return datetime.now(timezone.utc).isoformat()


def get_next_upload_order():
    """
    读取当前 submissions 最大 upload_order，再 +1
    """
    resp = (
        supabase
        .table("submissions")
        .select("upload_order")
        .order("upload_order", desc=True)
        .limit(1)
        .execute()
    )

    data = resp.data or []
    if not data:
        return 1
    return int(data[0]["upload_order"]) + 1


def get_next_queue_order():
    """
    读取当前 display_queue 最大 queue_order，再 +1
    """
    resp = (
        supabase
        .table("display_queue")
        .select("queue_order")
        .order("queue_order", desc=True)
        .limit(1)
        .execute()
    )

    data = resp.data or []
    if not data:
        return 1
    return int(data[0]["queue_order"]) + 1


def upload_base64_image_to_storage(data_url: str, bucket: str, filename: str):
    """
    接收 data:image/png;base64,... 格式字符串
    上传到 Supabase Storage
    返回公开访问 URL
    """
    if "," in data_url:
        data_url = data_url.split(",", 1)[1]

    binary = base64.b64decode(data_url)

    path = filename

    # 这里已经修正：去掉 upsert，避免 bool 类型 header 报错
    supabase.storage.from_(bucket).upload(
        path,
        binary,
        {"content-type": "image/png"}
    )

    public_url_resp = supabase.storage.from_(bucket).get_public_url(path)

    if isinstance(public_url_resp, dict):
        public_url = public_url_resp.get("publicUrl") or public_url_resp.get("public_url")
    else:
        public_url = public_url_resp

    return public_url, path


# =========================
# 健康检查
# =========================
@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.get("/display")
def display_page():
    return send_from_directory(os.path.dirname(__file__), "display.html")


# =========================
# 接收前端生成好的图谱并入库、入队
# =========================
@app.post("/upload_generated")
def upload_generated():
    """
    前端传入：
    {
      "imageBase64": "data:image/png;base64,...",
      "symbol": "75",
      "sourceName": "example.jpg",
      "originalImageBase64": "data:image/jpeg;base64,..."   # 可选
    }
    """
    try:
        data = request.get_json(silent=True) or {}

        image_base64 = data.get("imageBase64")
        symbol = data.get("symbol", "")
        source_name = data.get("sourceName", "")
        original_base64 = data.get("originalImageBase64")  # 可选

        if not image_base64:
            return jsonify({"ok": False, "error": "缺少 imageBase64"}), 400

        submission_id = str(uuid.uuid4())
        upload_order = get_next_upload_order()
        queue_order = get_next_queue_order()

        # 1) 上传生成图到 Storage
        generated_filename = f"{submission_id}.png"
        generated_url, generated_path = upload_base64_image_to_storage(
            image_base64,
            GENERATED_BUCKET,
            generated_filename
        )

        # 2) 如果前端也传了原图，则一并上传
        original_url = None
        if original_base64:
            original_filename = f"{submission_id}.jpg"
            original_url, original_path = upload_base64_image_to_storage(
                original_base64,
                ORIGINAL_BUCKET,
                original_filename
            )

        # 3) 写 submissions
        submission_payload = {
            "upload_order": upload_order,
            "uploaded_at": now_iso(),
            "original_image_url": original_url or "",
            "generated_image_url": generated_url,
            "symbol": symbol,
            "display_status": "pending",
            "message": None,
            "printed": False,
            "print_count": 0,
            "print_code": None,
            "payment_status": "unpaid",
            "created_at": now_iso()
        }

        submission_insert = (
            supabase
            .table("submissions")
            .insert(submission_payload)
            .execute()
        )

        submission_rows = submission_insert.data or []
        if not submission_rows:
            return jsonify({"ok": False, "error": "submissions 写入失败"}), 500

        # 这里取数据库真实 id（你表里应是 uuid 主键）
        db_submission_id = submission_rows[0]["id"]

        # 4) 写 display_queue
        queue_payload = {
            "submission_id": db_submission_id,
            "generated_image_url": generated_url,
            "queue_order": queue_order,
            "status": "pending",
            "created_at": now_iso(),
            "shown_at": None
        }

        queue_insert = (
            supabase
            .table("display_queue")
            .insert(queue_payload)
            .execute()
        )

        queue_rows = queue_insert.data or []
        if not queue_rows:
            return jsonify({"ok": False, "error": "display_queue 写入失败"}), 500

        queue_item = queue_rows[0]

        # 5) 返回给前端
        active_queue = (
            supabase
            .table("display_queue")
            .select("id", count="exact")
            .in_("status", ["pending", "showing"])
            .execute()
        )

        queue_length = active_queue.count or 0

        return jsonify({
            "ok": True,
            "submission": submission_rows[0],
            "item": {
                "id": queue_item["id"],
                "submission_id": queue_item["submission_id"],
                "image_url": queue_item["generated_image_url"],
                "status": queue_item["status"]
            },
            "queue_length": queue_length
        })

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================
# 查看当前展示队列
# =========================
@app.get("/queue")
def get_queue():
    try:
        resp = (
            supabase
            .table("display_queue")
            .select("*")
            .order("queue_order", desc=False)
            .execute()
        )
        return jsonify({"ok": True, "items": resp.data or []})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================
# 展示页读取下一张图
# 规则：
# 1. 如果已有 showing，则返回它
# 2. 否则取最早 pending（created_at asc, queue_order asc）
# 3. 并将其更新为 showing
# =========================
@app.get("/next_image")
def next_image():
    try:
        # 先看有没有正在展示的
        showing_resp = (
            supabase
            .table("display_queue")
            .select("*")
            .eq("status", "showing")
            .order("queue_order", desc=False)
            .limit(1)
            .execute()
        )

        showing_rows = showing_resp.data or []
        if showing_rows:
            item = showing_rows[0]
            return jsonify({
                "ok": True,
                "item": {
                    "id": item["id"],
                    "submission_id": item["submission_id"],
                    "image_url": item["generated_image_url"],
                    "status": item["status"]
                },
                "display_seconds": DISPLAY_SECONDS
            })

        # 没有 showing，就取最早 pending
        pending_resp = (
            supabase
            .table("display_queue")
            .select("*")
            .eq("status", "pending")
            .order("created_at", desc=False)
            .order("queue_order", desc=False)
            .limit(1)
            .execute()
        )

        pending_rows = pending_resp.data or []
        if not pending_rows:
            return jsonify({
                "ok": True,
                "item": None,
                "display_seconds": DISPLAY_SECONDS
            })

        item = pending_rows[0]

        # 更新 queue 状态为 showing
        (
            supabase
            .table("display_queue")
            .update({"status": "showing"})
            .eq("id", item["id"])
            .execute()
        )

        # 同时更新 submissions.display_status
        (
            supabase
            .table("submissions")
            .update({"display_status": "showing"})
            .eq("id", item["submission_id"])
            .execute()
        )

        return jsonify({
            "ok": True,
            "item": {
                "id": item["id"],
                "submission_id": item["submission_id"],
                "image_url": item["generated_image_url"],
                "status": "showing"
            },
            "display_seconds": DISPLAY_SECONDS
        })

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================
# 展示完成，标记为 shown
# =========================
@app.post("/mark_shown")
def mark_shown():
    try:
        data = request.get_json(silent=True) or {}
        queue_id = data.get("id")

        if not queue_id:
            return jsonify({"ok": False, "error": "缺少队列 id"}), 400

        # 先查 queue 记录，拿 submission_id
        queue_resp = (
            supabase
            .table("display_queue")
            .select("*")
            .eq("id", queue_id)
            .limit(1)
            .execute()
        )
        queue_rows = queue_resp.data or []
        if not queue_rows:
            return jsonify({"ok": False, "error": "队列项不存在"}), 404

        queue_item = queue_rows[0]
        submission_id = queue_item["submission_id"]

        # 更新 queue
        (
            supabase
            .table("display_queue")
            .update({
                "status": "shown",
                "shown_at": now_iso()
            })
            .eq("id", queue_id)
            .execute()
        )

        # 更新 submissions
        (
            supabase
            .table("submissions")
            .update({"display_status": "shown"})
            .eq("id", submission_id)
            .execute()
        )

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
