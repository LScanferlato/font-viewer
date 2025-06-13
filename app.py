from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

def is_valid_utf8(s):
    try:
        s.encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False

@app.route('/')
def index():
    fonts = []
    fonts_directory = 'fonts_directory'

    for root, dirs, files in os.walk(fonts_directory):
        for file in files:
            if file.lower().endswith(('.ttf', '.otf')):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, fonts_directory)
                if is_valid_utf8(relative_path):
                    fonts.append(relative_path)
                else:
                    print(f"Font ignorato per problemi di codifica: {relative_path}")

    print(f"Totale font trovati: {len(fonts)}")
    return render_template('index.html', fonts=fonts)

@app.route('/fonts/<path:filename>')
def serve_font(filename):
    return send_from_directory('fonts_directory', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
