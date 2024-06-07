from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.language_models import TextEmbeddingModel
from vertexai.vision_models import Image, MultiModalEmbeddingModel
import vertexai.vision_models
from google.cloud import aiplatform
import json

vertexai.init(project="dp-iit-422513", location="us-central1")
aiplatform.init(project="dp-iit-422513", location="us-central1")
# model = GenerativeModel("gemini-pro")
get_deployed_index = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name="projects/373208582789/locations/us-central1/indexEndpoints/4237803686471925760")


def generate_embeddings(img):
    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    image = Image.load_from_file(img)
    embeddings = model.get_embeddings(
        image=image
        )
    return embeddings.image_embedding


query_embeddings = generate_embeddings("/home/venkateshriyer/IMAGE_EMBED_POC/data_set/samsung-fake.PNG")

response = get_deployed_index.find_neighbors(
    deployed_index_id = "DPIITEmbeddingSearch",
    queries = [query_embeddings],
    num_neighbors = 2
)

print(response)
print(response[0][0].id)


# def get_response():
#     f = open('/home/venkateshriyer/IMAGE_EMBED_POC/dpiit_metadata.json')
#     data = json.load(f)
#     for i in data:
#         print(i['id'])

# get_response()