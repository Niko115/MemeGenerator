from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import os
import io
from datetime import datetime, timezone

FONT_PATH = os.path.join("fonts", "DejaVuSans.ttf")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok = True)

def draw_meme(image: Image.Image, top_text: str, bottom_text: str, font_path = FONT_PATH):
    img = image.convert('RGB')
    draw = ImageDraw.Draw(img)
    width, height = img.size

    base_font_size = int(width / 12)

    def load_font(size):
        if font_path and os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
        return ImageFont.load_default()
    
    def measure(text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        return text_width, text_height
    
    def draw_text(text, y_pos):
        font_size = base_font_size
        font = load_font(font_size)
        
        while True:
            text_width, text_height = measure(text, font)
            if text_width <= width - 20 or font_size <= 10:
                break
            font_size -= 2
            font = load_font(font_size)
        
        x = (width - text_width) / 2
        stroke_width = max(1, int(font_size * 0.06))

        for ox in range(-stroke_width, stroke_width + 1):
            for oy in range(-stroke_width, stroke_width + 1):
                draw.text((x + ox, y_pos + oy), text, font = font, fill = 'black')
        draw.text((x, y_pos), text, font = font, fill = 'white')
    
    if top_text:
        draw_text(top_text.upper(), 10)
    
    if bottom_text:
        font = load_font(base_font_size)
        _, text_height = measure(bottom_text.upper(), font)
        draw_text(bottom_text.upper(), height - text_height - 20)

    return img

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods = ['POST'])
def generate():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    file = request.files['image']
    top_text = request.form.get('top_text', '')
    bottom_text = request.form.get('bottom_text', '')

    if file.filename == '':
        return redirect(url_for('index'))
    
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')
    filename = f"meme_{timestamp}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    with Image.open(filepath) as im:
        processed = draw_meme(im, top_text, bottom_text)
        out_io = io.BytesIO()
        processed.save(out_io, format = 'JPEG')
        out_io.seek(0)

    out_path = os.path.join(app.config['UPLOAD_FOLDER'], f'gen_{filename}.jpg')
    with open(out_path, 'wb') as f:
        f.write(out_io.getbuffer())

    return send_file(out_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=int(os.environ.get('PORT', 5000)))