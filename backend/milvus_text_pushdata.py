from pymilvus import connections, Collection, utility
from text_extraction import extraction_of_text
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import numpy as np

class push:
    def __init__(self):
        self.image_path = "/home/sanjayvijaykumar/Documents/IMAGE_EMBED_POC/data_set/text_test/"
        connections.connect(host="localhost", port=19530)
        print(utility.list_collections(timeout=None))
        self.collection = Collection("TEXT_EMBEDDINGS")
        self.base_options = python.BaseOptions(model_asset_path='embedder.tflite')
        self.l2_normalize = True #@param {type:"boolean"}
        self.quantize = True #@param {type:"boolean"}
        self.options = vision.ImageEmbedderOptions(
            base_options=self.base_options, l2_normalize=self.l2_normalize, quantize=self.quantize)
        self.BaseOptions = mp.tasks.BaseOptions
        self.TextEmbedder = mp.tasks.text.TextEmbedder
        self.TextEmbedderOptions = mp.tasks.text.TextEmbedderOptions

        # For creating a text embedder instance:
        self.text_options = self.TextEmbedderOptions(
            base_options=self.BaseOptions(model_asset_path='universal_sentence_encoder.tflite'),
            quantize=True)
        self.text_embedder = self.TextEmbedder.create_from_options(self.text_options)
    
    def push_data_to_milvus(self):
        with vision.ImageEmbedder.create_from_options(self.options) as embedder:
            embedding_list =[]
            image_name_list = []
            text_embedding_list = []
            text_extracted_list = []
            for image in os.listdir(self.image_path):
                image_name = image.split('/')[-1]
                img = mp.Image.create_from_file(self.image_path+image_name)
                get_text = extraction_of_text(self.image_path + image_name)
                extracted_text = self.text_embedder.embed(get_text)
                # print("extracted_text", extracted_text)
                #text_list.append()
                print("image", img)
                embedding = embedder.embed(img)
                print("embedding", embedding)
                float_embedding = embedding.embeddings[0].embedding.astype(np.float32)
                float_text_embedding = extracted_text.embeddings[0].embedding.astype(np.float32)
                num_to_pad = 1024 - len(float_text_embedding) % 1024

                # Pad the original data with zeros
                padded_data = np.concatenate((float_text_embedding, np.zeros(num_to_pad)))
                print("float_text_embedding", padded_data.shape)
                text_embedding_list.append(padded_data)
                text_extracted_list.append(get_text)
                # embedding_list.append(embedding.embeddings[0].embedding)
                embedding_list.append(float_embedding)
                image_name_list.append(image_name)
                print("list", text_embedding_list)
                print("list2", len(text_extracted_list))
                print('list3', image_name_list)
                self.collection.insert([text_embedding_list, text_extracted_list, image_name_list])
                text_extracted_list.clear()
                text_embedding_list.clear()
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
# obj.push_data_to_milvus()
obj.size_of_collection()
