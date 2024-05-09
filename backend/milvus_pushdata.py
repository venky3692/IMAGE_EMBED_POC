from pymilvus import connections, Collection
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

class push:
    def __init__(self):
        self.image_path = "/home/ubuntu/DPIIT/logos/"
        connections.connect(host="localhost", port=19530)
        self.collection = Collection("IMAGE_EMBEDDINGS")
        self.base_options = python.BaseOptions(model_asset_path='embedder.tflite')
        self.l2_normalize = True #@param {type:"boolean"}
        self.quantize = True #@param {type:"boolean"}
        self.options = vision.ImageEmbedderOptions(
            base_options=self.base_options, l2_normalize=self.l2_normalize, quantize=self.quantize)

    def push_data_to_milvus(self):
        with vision.ImageEmbedder.create_from_options(self.options) as embedder:
            embedding_list =[]
            image_name_list = []
            for image in os.listdir(self.image_path):
                image_name = image.split('/')[-1]
                embedding = embedder.embed(image)
                embedding_list.append(embedding.embeddings[0].embedding)
                image_name_list.append(image_name)
                self.collection.insert([embedding_list, image_name_list])
                embedding_list.clear()
                image_name_list.clear()

            index_params = {
            'metric_type':'COSINE',
            'index_type':"FLAT",
            'params':{"nlist":15}
        }

            self.collection.create_index(field_name="embeddings", index_params=index_params)

    def size_of_collection(self):
        print('size of collection', self.collection.num_entities)
        print('is empty', self.collection.is_empty) 


obj = push()
obj.push_data_to_milvus()
obj.size_of_collection()