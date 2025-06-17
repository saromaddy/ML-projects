from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

MAX_BASE64_SIZE = 500 * 1024  # 500 KB

def compress_image(image, format):
    quality = 85
    while quality >= 10:
        buffer = io.BytesIO()
        image.save(buffer, format=format, quality=quality, optimize=True)
        base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        if len(base64_str.encode('utf-8')) <= MAX_BASE64_SIZE:
            return base64_str
        quality -= 5
    return None  # Cannot compress to required size

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        image = Image.open(image_file)
        format = image.format.upper()
        if format not in ['JPEG', 'JPG', 'PNG']:
            return jsonify({'error': 'Unsupported format. Use PNG or JPG.'}), 400

        base64_str = compress_image(image, format='JPEG' if format in ['JPEG', 'JPG'] else 'PNG')
        if not base64_str:
            return jsonify({'error': 'Could not compress image under 500KB'}), 400

        return jsonify({'base64': base64_str})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
