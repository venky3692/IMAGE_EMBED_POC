from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from image_comparison import img_comparison
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
        comparison_obj = img_comparison()
        similar_image, image_name, cosine_similarity = comparison_obj.image_comparison_and_embedder(file_path)
        #similarity_score = image_comparison_and_embedder(file_path)
        return jsonify({'message': 'File successfully uploaded', 'filename': filename, 'similarity_score': cosine_similarity,
                        'similar_image_name': image_name})

if __name__ == '__main__':
    app.run(port=5000)
