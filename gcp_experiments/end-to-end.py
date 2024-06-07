from google.cloud import aiplatform, storage
from vertexai.vision_models import Image, MultiModalEmbeddingModel
from io import BytesIO
import vertexai
from PIL import Image
import uuid
import json
import base64

import vertexai.vision_models
vertexai.init(project="dp-iit-422513", location="us-central1")

client = storage.Client(project="dp-iit-422513")
bucket = client.get_bucket("dpiit_image_dataset")
model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
json_list =[]
def is_image(blob):
    return any(blob.name.endswith(extension) for extension in ['.jpg', '.jpeg', '.png'])

def create_embeddings():
    for blob in bucket.list_blobs():
        id = str(uuid.uuid4())
        blob_url = blob.public_url
        blob_name = blob.name
        image_data = blob.download_as_string()
        # image = Image.open(BytesIO(image_data))
        base64_image = base64.b64encode(image_data).decode()
        # image = BytesIO(image_data)
        image = vertexai.vision_models.Image.load_from_file(blob_url)
        image_embeddings = model.get_embeddings(
            image=image
        )
        data_dict = {
            "id":id,
            "blob_name":blob_name,
            "blob_url":blob_url,
            "base64image": base64_image,
            "image_embedding": image_embeddings.image_embedding
        }
        json_list.append(data_dict)
    
    with open("dpiit_embeddings.json", "w") as json_file:
        json.dump(json_list,json_file, indent=2)
        # json_file.write("\n")

def create_vector_index():
    DPIIT_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name = "DPIIT-Search",
    contents_delta_uri = "gs://dpiit_embedding_dataset",
    dimensions = 1408,
    approximate_neighbors_count = 10,
    )
    
    DPIIT_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name = "DPIIT-Search",
    public_endpoint_enabled = True
    )                      
 
    DPIIT_index_endpoint.deploy_index(
    index = DPIIT_index, deployed_index_id = "DPIITSearch"
    )
    print("DONE!!")
# create_embeddings()
create_vector_index()

# from vertexai.vision_models import Image, MultiModalEmbeddingModel

# vertexai.init(project="dp-iit-422513", location="us-central1")

# model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
# image = Image.load_from_file("/home/venkateshriyer/Downloads/levis_elvis-fake.jpg")
# print(type(image))
# embeddings = model.get_embeddings(
#     image=image, 
#     contextual_text= 'Levis'
#     )

# print(embeddings)