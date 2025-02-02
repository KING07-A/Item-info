from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

app = Flask(__name__)

# GitHub raw content URL with the 'icon' folder
GITHUB_RAW_URL = "https://raw.githubusercontent.com/KING07-A/All_Icon/refs/heads/main/icon"

@app.route('/king-item-info', methods=['GET'])
def get_item_image():
    item_id = request.args.get('item_id')
    api_key = request.args.get('key')

    # API key validation for multiple keys
    valid_api_keys = ["KING", "KING"]
    if api_key not in valid_api_keys:
        return jsonify({"error": "Invalid API key"}), 401

    if not item_id:
        return jsonify({"error": "Item ID is required"}), 400

    # Construct the full GitHub raw image URL with the 'icon' folder
    image_url = f"{GITHUB_RAW_URL}/{item_id}.png"

    # Debugging: Print the image URL
    print(f"Requesting image from: {image_url}")

    # Download the image
    response = requests.get(image_url)
    if response.status_code != 200:
        print(f"Failed to fetch image. Status code: {response.status_code}")
        return jsonify({"error": "Item image not found"}), 404

    # Open the image using Pillow
    image = Image.open(BytesIO(response.content))

    # Add text "AKIRU" to the center of the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # Default font, you can customize it
    text = "AKIRU"
    
    # Use textbbox to calculate the size of the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_position = ((image.width - text_width) // 2, (image.height - text_height) // 2)

    # Add text to image
    draw.text(text_position, text, fill="white", font=font)

    # Save the image to a BytesIO object and send it as a response
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Return the image as response
    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
