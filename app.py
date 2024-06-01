from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
import requests
from io import BytesIO
import base64 
import uuid
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'output'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def download_image(image_source):
    if image_source.startswith('http'):
        if not image_source.startswith('https://'):
            raise ValueError("Only HTTPS URLs are allowed.")
        response = requests.get(image_source)
        return Image.open(BytesIO(response.content))
    else:
        image_data = base64.b64decode(image_source)
        return Image.open(BytesIO(image_data))

def byebg(input_img, background_img):
    no_bg_img = remove(input_img)
    background_img = background_img.resize(no_bg_img.size, Image.LANCZOS)
    result_img = Image.new("RGBA", no_bg_img.size)
    result_img.paste(background_img, (0, 0))
    result_img.paste(no_bg_img, (0, 0), no_bg_img)
    result_img = result_img.convert("RGB")
    return result_img

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        input_file = request.files.get('input_file')
        background_file = request.files.get('background_file')

        if not input_file or not background_file:
            return jsonify({'status': 'error', 'message': 'Missing input_file or background_file'}), 400

        input_img = Image.open(input_file.stream)
        background_img = Image.open(background_file.stream)

        result_img = byebg(input_img, background_img)

        output_filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        result_img.save(output_path)

        return jsonify({'status': 'success', 'link': f"/{UPLOAD_FOLDER}/{output_filename}"})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    port = int(3000)  # Default to 3000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)