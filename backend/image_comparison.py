import mediapipe as mp
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pymilvus import connections, Collection
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
# Create options for Image Embedder

class img_comparison:
    def __init__(self):
        connections.connect(host="localhost", port=19530)
        self.collection = Collection("IMAGE_EMBEDDINGS")

    def image_comparison_and_embedder(self,user_image_path):
        connections.connect(host="localhost", port=19530)
        self.collection = Collection("IMAGE_EMBEDDINGS")
        base_options = python.BaseOptions(model_asset_path='embedder.tflite')
        l2_normalize = True #@param {type:"boolean"}
        quantize = True #@param {type:"boolean"}
        options = vision.ImageEmbedderOptions(
            base_options=base_options, l2_normalize=l2_normalize, quantize=quantize)

        # Create Image Embedder
        with vision.ImageEmbedder.create_from_options(options) as embedder:

        # Format images for MediaPipe
            #first_image = mp.Image.create_from_file('/home/venkatesh/Desktop/hwd.png')
            user_image = mp.Image.create_from_file(user_image_path)
            
            #first_embedding_result = embedder.embed(first_image)
            embedding_result = embedder.embed(user_image)
            get_final_embedding = embedding_result.embeddings[0].embedding
            get_final_embedding = get_final_embedding.astype(np.float32)


            # Calculate and print similarity
            similar_image, image_name = self.collection.search(data= [get_final_embedding], anns_field="embeddings", param={"metric":"COSINE","offset":0},
                                          output_fields=["embeddings", "image_name"],limit=1, consistency_level="Strong" )
            
            get_cosine_similarity = cosine_similarity([similar_image], [user_image_path])
            #similarity = vision.ImageEmbedder.cosine_similarity(
            #    first_embedding_result.embeddings[0],
            #    second_embedding_result.embeddings[0])

        return similar_image, image_name, get_cosine_similarity

