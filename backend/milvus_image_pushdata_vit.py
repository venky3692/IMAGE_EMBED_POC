from pymilvus import connections, Collection, utility
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import oracledb
import io
import cv2
from transformers import ViTFeatureExtractor, ViTModel
import torch
from PIL import Image
from image_similarity_measures.quality_metrics import rmse, psnr, ssim, fsim, issm, sre, sam, uiq
import os;

feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
model = ViTModel.from_pretrained('google/vit-base-patch16-224')

class push_image:
    def __init__(self):
        self.dbconnection = oracledb.connect(user='imageUser', password='imageUser123', dsn='localhost:1521/XEPDB1');
        self.cursor = self.dbconnection.cursor()
        self.image_path = "/home/sanjayvijaykumar/Documents/IMAGE_EMBED_POC/data_set/text_test/"
        connections.connect(host="localhost", port=19530)
        print(utility.list_collections(timeout=None))
        self.collection = Collection("IMAGE_EMBEDDINGS")
    
    def push_image_data_to_milvus(self):
        embedding_list =[]
        image_name_list = []
        self.cursor.execute("SELECT * FROM sys.images")
        self.dbconnection.commit()
        rows = self.cursor.fetchall()
        for row in rows:
            # image_name = image.split('/')[-1]
            # img = mp.Image.create_from_file(self.image_path+image_name)
            image_data = row[1].read()

            pre_img = io.BytesIO(image_data);
            print("image", pre_img);
            images = Image.open(pre_img).convert('RGB')
            inputs = feature_extractor(images=images, return_tensors="pt")

            # Forward pass to get the embeddings
            with torch.no_grad():
                    outputs = model(**inputs)

            # Get the embeddings
            # embeddings = outputs.last_hidden_state
            embedding = outputs.last_hidden_state.squeeze(0).mean(dim=0).numpy()
            print("embeddings", embedding)
            print("embeddings type", embedding.shape)
            # embedding_list.append(embedding.embeddings[0].embedding)
            embedding_list.append(embedding)
            image_name_list.append(row[2])
            self.collection.insert([embedding_list, image_name_list])
            embedding_list.clear()
            image_name_list.clear()
        self.cursor.close()
        self.dbconnection.close()
        index_params = {
        'metric_type':'COSINE',
        'index_type':"FLAT",
        'params':{"nlist":15}
    }

        self.collection.create_index(field_name="embeddings", index_params=index_params)

    def size_of_collection(self):
        print('size of collection', self.collection.num_entities)
        print('is empty', self.collection.is_empty) 


obj = push_image()
# obj.push_image_data_to_milvus()
obj.size_of_collection()
