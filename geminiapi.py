import base64
import io
from flask import Flask, request, jsonify
from PIL import Image # Import Pillow library

app = Flask(__name__)

@app.route('/image-to-base64', methods=['POST'])
def image_to_base64():
    """
    Receives an image file via POST request, compresses it (if possible),
    encodes it to base64, and then writes the base64 string to a text file.
    """
    # Check if 'image' file is present in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    try:
        # Read the raw image data from the incoming file
        image_data = image_file.read()

        # Use BytesIO to treat the raw image data as a file for Pillow
        image_stream = io.BytesIO(image_data)
        original_image = Image.open(image_stream)

        # Create another BytesIO object to store the compressed image
        compressed_image_stream = io.BytesIO()

        # Save the image to the new stream with compression.
        # We'll save it as JPEG with a significantly reduced quality.
        # You can adjust the quality value (0-100) to find a good balance
        # between file size and image quality. A lower quality value (e.g., 30-50)
        # will result in a smaller file size but might degrade image quality more.
        # Experiment with values like 50, 40, or 30 to hit your target of 1 MB.
        # If the original image is PNG, saving as JPEG will lose transparency.
        # Consider saving as PNG with optimize=True for PNGs if transparency is needed,
        # but JPEG generally offers better compression for photos.
        original_image.save(compressed_image_stream, format='JPEG', quality=40)

        # Get the bytes from the compressed image stream
        compressed_image_data = compressed_image_stream.getvalue()

        # Encode the compressed image data to base64 and decode to a UTF-8 string
        base64_encoded = base64.b64encode(compressed_image_data).decode('utf-8')

        # Define the output file name
        output_filename = 'base64_output.txt'

        # Write the base64 encoded string to a text file
        with open(output_filename, 'w') as f:
            f.write(base64_encoded)

        # Return a success message
        return jsonify({'message': f'Base64 encoded (compressed) image saved to {output_filename}'}), 200

    except Exception as e:
        # Handle any errors during the process
        # This might include errors if the file is not a valid image
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
