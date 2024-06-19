from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.language_models import TextEmbeddingModel
from vertexai.vision_models import Image, MultiModalEmbeddingModel
import vertexai.vision_models
from google.cloud import aiplatform
import json
import time




# vertexai.init(project="dp-iit-422513", location="asia-south1")
# aiplatform.init(project="dp-iit-422513", location="asia-south1")
get_deployed_index = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name="projects/373208582789/locations/asia-south1/indexEndpoints/1083819397824380928")


def generate_embeddings(img):
    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    image = Image.load_from_file(img)
    embeddings = model.get_embeddings(
        image=image
        )
    return embeddings.image_embedding


start_time = time.time()
query_embeddings = generate_embeddings("/home/venkateshriyer/image.png")

response = get_deployed_index.find_neighbors(
    deployed_index_id = "DPIITEmbeddingSearch",
    queries = [query_embeddings],
    num_neighbors = 10
)
print(response)
end_time = time.time()
total_time = end_time - start_time
print("--->", total_time)


# def get_response():
#     f = open('/home/venkateshriyer/IMAGE_EMBED_POC/dpiit_metadata.json')
#     data = json.load(f)
#     for neighbour in response:
#         for i in neighbour:
#             get_id = i.id
#             for element in data:
#                 if element['id'] == get_id:
#                     get_image = element['base64image']
#                     # print("get image-->", get_image)

# get_response()


