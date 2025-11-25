from flask import Flask, render_template, send_from_directory, request, jsonify
import os

app = Flask(__name__)
FONTS_DIR = "fonts_directory"

def list_fonts():
    fonts = []
    for root, dirs, files in os.walk(FONTS_DIR):
        for file in files:
            if file.lower().endswith(('.ttf', '.otf')):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, FONTS_DIR)
                fonts.append(relative_path)
    return fonts

@app.route("/")
def index():
    query = request.args.get("query", "").lower()
    all_fonts = list_fonts()

    # Filtra lato server se c'è una query
    if query:
        fonts = [f for f in all_fonts if query in f.lower()]
    else:
        fonts = all_fonts

    total = len(fonts)  # conta effettivamente quanti sono
    return render_template("index.html", total_fonts=total, query=query)

@app.route("/api/fonts")
def api_fonts():
    start = int(request.args.get("start", 0))
    limit = int(request.args.get("limit", 50))
    query = request.args.get("query", "").lower()

    all_fonts = list_fonts()
    if query:
        all_fonts = [f for f in all_fonts if query in f.lower()]

    batch = all_fonts[start:start+limit]

    return jsonify({
        "fonts": batch,
        "total": len(all_fonts),
        "next_start": start + limit if start + limit < len(all_fonts) else None
    })

# ✅ correzione qui: aggiunto <path:filename>
@app.route("/fonts/<path:filename>")
def serve_font(filename):
    return send_from_directory(FONTS_DIR, filename)

if __name__ == "__main__":
    app.run(host="0
