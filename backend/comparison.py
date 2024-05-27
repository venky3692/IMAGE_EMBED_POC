import mediapipe as mp
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from text_extraction import extraction_of_text
from pymilvus import connections, Collection
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import vit as v
# Create options for Image Embedder

class comparison:
    def __init__(self):
        connections.connect(host="localhost", port=19530)
        self.img_collection = Collection("IMAGE_EMBEDDINGS")
        self.text_collection = Collection("TEXT_EMBEDDINGS")

    def image_comparison_and_embedder_vit(self,user_image_path):
        self.img_collection.load();
        get_final_embedding = v.get_embeddings([user_image_path])
        similarity_search = self.img_collection.search(data= [get_final_embedding], anns_field="embeddings", param={"metric":"COSINE","offset":0},
                                          output_fields=["embeddings", "image_name"],limit=1, consistency_level="Strong" )
        similarity_score = None
        for hits in similarity_search:
            similarity_score = hits[0]

        return similarity_score
    
    def image_comparison_and_embedder(self,user_image_path):
        #connections.connect(host="localhost", port=19530)
        #self.collection = Collection("IMAGE_EMBEDDINGS")
        self.img_collection.load()
        #print("collection loaded!")
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
            similarity_search = self.img_collection.search(data= [get_final_embedding], anns_field="embeddings", param={"metric":"COSINE","offset":0},
                                          output_fields=["embeddings", "image_name"],limit=1, consistency_level="Strong" )
            similarity_score = None
            for hits in similarity_search:
                similarity_score = hits[0]
            #get_cosine_similarity = cosine_similarity([similar_image], [user_image_path])
            #similarity = vision.ImageEmbedder.cosine_similarity(
            #    first_embedding_result.embeddings[0],
            #    second_embedding_result.embeddings[0])

        return similarity_score
        #return similar_image, image_name, get_cosine_similarity

    def text_comparison_and_embedder(self,user_image_path):
        self.text_collection.load()
        BaseOptions = mp.tasks.BaseOptions
        TextEmbedder = mp.tasks.text.TextEmbedder
        TextEmbedderOptions = mp.tasks.text.TextEmbedderOptions

        # For creating a text embedder instance:
        options = TextEmbedderOptions(
            base_options=BaseOptions(model_asset_path='universal_sentence_encoder.tflite'),
            quantize=True)
        self.text_embedder = TextEmbedder.create_from_options(options)

        get_text = extraction_of_text(user_image_path)
        extracted_text = self.text_embedder.embed(get_text)
        get_finaltext_embedding = extracted_text.embeddings[0].embedding
        get_finaltext_embedding = get_finaltext_embedding.astype(np.float32)
        num_to_pad = 1024 - len(get_finaltext_embedding) % 1024

        # Pad the original data with zeros
        padded_data = np.concatenate((get_finaltext_embedding, np.zeros(num_to_pad)))

        text_similarity_search = self.text_collection.search(data= [padded_data], anns_field="embeddings", param={"metric":"COSINE","offset":0},
                                          output_fields=["embeddings", "extracted_text", "image_name"],limit=1, consistency_level="Strong" )

        print("text_similarity_search", text_similarity_search)
        get_image = self.image_comparison_and_embedder_vit(user_image_path)
        get_text_image = None
        for hits in text_similarity_search:
            get_text_image = hits[0]


        return get_image, get_text_image, get_text;

