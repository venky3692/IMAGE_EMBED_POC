from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.language_models import TextEmbeddingModel
from vertexai.vision_models import Image, MultiModalEmbeddingModel
import vertexai.vision_models
from google.cloud import aiplatform

vertexai.init(project="dp-iit-422513", location="us-central1")
aiplatform.init(project="dp-iit-422513", location="us-central1")
# model = GenerativeModel("gemini-pro")
get_deployed_index = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name="projects/373208582789/locations/us-central1/indexEndpoints/8191964159303221248")


# def generate_embeddings(img):
#     model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
#     image = Image.load_from_file(img)

#     embeddings = model.get_embeddings(
#         image=image
#         )

#     return embeddings.image_embedding


# print(query_embeddings)

def generate_text_embeddings(sentences):    
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings(sentences)
    vectors = [embedding.values for embedding in embeddings]
    return vectors

query_embeddings = generate_text_embeddings(["Hello, I am Venkatesh"])

response = get_deployed_index.find_neighbors(
    deployed_index_id = "DPIITSearch",
    queries = [query_embeddings[0]],
    num_neighbors = 10
)

print(response)