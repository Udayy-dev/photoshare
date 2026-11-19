import os, uuid
from flask import Flask, request, redirect, render_template, Response, abort
from google.cloud import storage

app = Flask(__name__)
BUCKET = os.environ["BUCKET_NAME"]          # private bucket (privacy)
ALLOWED = {"image/jpeg", "image/png", "image/gif", "image/webp", "video/mp4"}
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024   # security: 25 MB cap
bucket = storage.Client().bucket(BUCKET)

@app.route("/")
def index():
    items = [{"name": b.name, "video": (b.content_type or "").startswith("video")}
             for b in bucket.list_blobs(prefix="uploads/")]
    return render_template("index.html", items=items)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f or f.mimetype not in ALLOWED:
        abort(400, "Only jpg/png/gif/webp/mp4 allowed")
    ext = f.filename.rsplit(".", 1)[-1].lower()[:5]
    blob = bucket.blob(f"uploads/{uuid.uuid4().hex}.{ext}")   # random name, no user paths
    blob.upload_from_file(f, content_type=f.mimetype)
    return redirect("/")

@app.route("/media/<path:name>")
def media(name):                       # bucket stays private; app serves files
    blob = bucket.get_blob("uploads/" + os.path.basename(name))
    if not blob: abort(404)
    return Response(blob.download_as_bytes(), mimetype=blob.content_type)

@app.route("/health")
def health(): return "ok"

@app.route("/burn")                    # CPU load endpoint for autoscaling test
def burn():
    s = 0
    for i in range(3_000_000): s += i * i
    return str(s)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
