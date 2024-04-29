from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from image_comparison import image_comparison_and_embedder
app = Flask(__name__)
CORS(app)

# Define the folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Endpoint to upload image
@app.route('/upload', methods=['POST'])
def upload_image():
    print("request.files", request.files)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    # similarity_score = image_comparison_and_embedder(file)
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        similarity_score = image_comparison_and_embedder(file_path)
        return jsonify({'message': 'File successfully uploaded', 'filename': filename, 'similarity_score': similarity_score})

if __name__ == '__main__':
    app.run(port=5000)