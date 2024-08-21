from flask import Flask, request, jsonify
import pytesseract
from PIL import Image, ImageOps, ImageEnhance
import io
import tempfile
import os
import subprocess
import psutil

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update this path if necessary

# Create a custom temporary directory
custom_temp_dir = os.path.join(os.path.dirname(__file__), 'temp_files')
os.makedirs(custom_temp_dir, exist_ok=True)

# Set the TMPDIR environment variable to use the custom temporary directory
os.environ['TMPDIR'] = custom_temp_dir

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Open the image file
        image = Image.open(image_file.stream)

        # Set a default DPI if not provided
        if 'dpi' not in image.info:
            image = ImageOps.exif_transpose(image)  # Ensure correct orientation
            image.info['dpi'] = (300, 300)  # Set default DPI

        # Convert the image to grayscale
        image = image.convert('L')

        # Enhance the image (optional step for better clarity)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)

        # Apply binary thresholding
        threshold = 128
        image = image.point(lambda p: p > threshold and 255)

        # Save the image to a temporary file in the custom directory
        with tempfile.NamedTemporaryFile(dir=custom_temp_dir, suffix='.png', delete=False) as temp_image_file:
            image.save(temp_image_file.name)
            temp_image_path = temp_image_file.name
            print(f"Temporary image file created at: {temp_image_path}")

        # Ensure the temporary file has appropriate permissions
        os.chmod(temp_image_path, 0o666)

        # Check if the temporary file exists
        if not os.path.exists(temp_image_path):
            raise FileNotFoundError(f"Temporary image file not found: {temp_image_path}")

        # Get current user information
        current_user_id = os.getuid()
        current_user_name = psutil.Process().username()
        print(f"Current user ID: {current_user_id}")
        print(f"Current user name: {current_user_name}")

        # Run Tesseract command directly and capture output
        # here is where the magic happens and we find out what the image looks like to the dyslexic person
        try:
            custom_config = r'--psm 10 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            command = [pytesseract.pytesseract.tesseract_cmd, temp_image_path, 'stdout', '--psm', '10', '-c', 'tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 'osd']
            result = subprocess.run(command, capture_output=True, text=True)
            print(f"Tesseract command output: {result.stdout}")
            print(f"Tesseract command error output: {result.stderr}")
            osd = pytesseract.image_to_osd(temp_image_path, output_type='dict', config=custom_config)
        except Exception as e:
            raise RuntimeError(f"Tesseract command failed: {e}")

        # Clean up the temporary file
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
            print(f"Temporary image file deleted: {temp_image_path}")

        # Return the OSD data as JSON
        # this will allow the front end to display the text in a manner that can be read normally
        return jsonify(osd)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def hello():
    return '''<!DOCTYPE html>
    <html>
    <head>
        <title>API RADIXICAL.COM</title>
        <style>
            body {
                background-color: #f0f0f0;
                color: #333;
                font-family: Arial, sans-serif;
            }
            #welcome {
                font-size: 24px;
                color: #00698f;
                font-weight: bold;
                text-align: center;
                margin-top: 20%;
            }
            #description {
                font-size: 18px;
                color: #666;
                text-align: center;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div id="welcome">
            Welcome to <br>
            <span style="color: #00698f; font-size: 30px;">api.radixical.com</span>
        </div>
        <div id="description">
            API Test and Documents Page <br>
            <a href="#" style="color: #00698f; text-decoration: none;">Learn more about our API and its usage</a>
        </div>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__production__":
    app.run(debug=True, socket='unix:mysocket.sock')
