import os, uuid
from flask import Flask, request, redirect, render_template, send_from_directory, abort
app = Flask(__name__)
D = "uploads"; os.makedirs(D, exist_ok=True)
OK = {"image/jpeg", "image/png", "image/gif", "image/webp", "video/mp4"}
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024

@app.route("/")
def index():
    items = [{"name": n, "video": n.endswith(".mp4")} for n in sorted(os.listdir(D))]
    return render_template("index.html", items=items)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f or f.mimetype not in OK: abort(400, "Only jpg/png/gif/webp/mp4 allowed")
    ext = f.filename.rsplit(".", 1)[-1].lower()[:5]
    f.save(os.path.join(D, uuid.uuid4().hex + "." + ext))
    return redirect("/")

@app.route("/media/<name>")
def media(name): return send_from_directory(D, os.path.basename(name))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
