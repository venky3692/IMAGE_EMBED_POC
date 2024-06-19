from google.cloud import aiplatform, storage
from vertexai.vision_models import Image, MultiModalEmbeddingModel
import vertexai.vision_models
from io import BytesIO
import vertexai
import uuid
import json
import base64

embedding_json_list =[]
metadata_json_list= []
flag_embeddings = False
flag_deployment = True

# import google.auth
# credentials = google.auth.default()[0] 
# print(dir(credentials))

class vectorSearch:
    def __init__(self):
        vertexai.init(project="dp-iit-422513", location="asia-south1")
        self.client = storage.Client()
        self.bucket = self.client.get_bucket("dpiit-images-input")
        self.model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
        
    def create_embeddings(self):
        for blob in self.bucket.list_blobs():
            print(blob)
            id = str(uuid.uuid4())
            blob_url = blob.public_url
            blob_name = blob.name
            image_data = blob.download_as_string()
            # image = Image.open(BytesIO(image_data))
            base64_image = base64.b64encode(image_data).decode()
            # image = BytesIO(image_data)
            image = vertexai.vision_models.Image.load_from_file(blob_url)
            image_embeddings = self.model.get_embeddings(
                image=image
            )
            metadata_dict = {
                "id":id,
                "blob_name":blob_name,
                "blob_url":blob_url,
                "base64image": base64_image,
                "image_embedding": image_embeddings.image_embedding
            }
            embedding_dict = {
                "id": id,
                "embedding": image_embeddings.image_embedding
            }
            
            embedding_json_list.append(embedding_dict)
            metadata_json_list.append(metadata_dict)
        
        with open("dpiit_only_embeddings.json", "w") as json_file:
            for ele in embedding_json_list:
                json_file.write(json.dumps(ele)+"\n")
        
        with open("dpiit_metadata.json", "a") as json_md_file:
            json.dump(metadata_json_list,json_md_file, indent=2)

        print(len(embedding_json_list))
        print(len(metadata_json_list))
        print('Embedding files created!')

    def push_jsondata_to_storage(self,bucket_name, destination_blob_name, source_file_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        print('Json file uploaded!')

    def create_vector_index(self):
        DPIIT_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name = "DPIIT-Embedding-Search",
        contents_delta_uri = "gs://dpiit-json-dataset",
        dimensions = 1408,
        approximate_neighbors_count = 10,
        )
        
        DPIIT_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
        display_name = "DPIIT-Embedding-Search",
        public_endpoint_enabled = True
        )                      
    
        DPIIT_index_endpoint.deploy_index(
        index = DPIIT_index, deployed_index_id = "DPIITEmbeddingSearch"
        )
        
        print("Deployment done!")

if __name__ == '__main__':
    if flag_embeddings:
        embed = vectorSearch()
        embed.create_embeddings()
    if flag_deployment:
        deploy = vectorSearch()
        # json_storage = deploy.push_jsondata_to_storage(bucket_name='dpiit-json-dataset',
        #                                                source_file_name = './dpiit_only_embeddings.json', 
        #                                                destination_blob_name='dpiit_only_embeddings.json')
        deploy.create_vector_index()



