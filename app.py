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
    # La pagina iniziale non passa tutti i font, solo il totale
    fonts = list_fonts()
    total = len(fonts)
    return render_template("index.html", total_fonts=total)

@app.route("/api/fonts")
def api_fonts():
    """Endpoint per lazy loading: restituisce un batch di font in JSON"""
    start = int(request.args.get("start", 0))
    limit = int(request.args.get("limit", 50))

    fonts = list_fonts()
    batch = fonts[start:start+limit]

    return jsonify({
        "fonts": batch,
        "total": len(fonts),
        "next_start": start + limit if start + limit < len(fonts) else None
    })

@app.route("/fonts/<path:filename>")
def serve_font(filename):
    return send_from_directory(FONTS_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
