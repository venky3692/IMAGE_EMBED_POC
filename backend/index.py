from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from comparison import comparison
from color_comparison import compare_color_similarity
from dominating_color import dominating_color
# from text_extraction import extraction_of_text
import base64
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
        comparison_obj = comparison()
        #similar_image, image_name, cosine_similarity = comparison_obj.image_comparison_and_embedder(file_path)
        similarity_score, text_similarity, text_extracted = comparison_obj.text_comparison_and_embedder(file_path)
        compare_file_path = os.path.join('../data_set/text_test', similarity_score.entity.image_name)
        matching_text_file_path = os.path.join('../data_set/text_test', text_similarity.entity.image_name)
        # color_similarity = compare_color_similarity(file_path, compare_file_path)
        dominating_color_similarity = dominating_color(file_path, compare_file_path)
        orig_text_extracted = ' '
        fake_text_extracted = ' '
        # orig_text_extracted, fake_text_extracted = extraction_of_text(file_path, compare_file_path)
        common_dom_colors = [[float(num) for num in item[0].tolist()] for item in dominating_color_similarity[1]]
        print("common_dom_colors", common_dom_colors)
        with open(compare_file_path, 'rb') as f:
            image_data = f.read()
        
        # Convert the image data to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        with open(matching_text_file_path, 'rb') as f:
            image_data2 = f.read()
        
        # Convert the image data to base64
        image_base64_2 = base64.b64encode(image_data2).decode('utf-8')
        return jsonify({'message': 'File successfully uploaded', 'matching-logo': similarity_score.entity.image_name, 
                        'similarity_score': (similarity_score.distance)*100,
                        'text_similarity_score': (text_similarity.distance)*100, 
                        'dominating_color_similarity': (dominating_color_similarity[0])*100,
                        'matching_image_text': text_similarity.entity.extracted_text,
                        'imageData2': image_base64_2,
                        'uploaded_image_text': text_extracted, 'imageData': image_base64, 'matching_colors':common_dom_colors,})

if __name__ == '__main__':
    app.run(port=5000)
