
# Create a service key from this link and download the json - https://console.cloud.google.com/iam-admin/serviceaccounts/details/113105866777091223651/keys?project=dp-iit-422513

#set env variable with the path of json downloaded file - export GOOGLE_APPLICATION_CREDENTIALS="/home/username/dp-iit-422513-57a5bb7b90de.json"

# install this - sudo snap install google-cloud-sdk --classic

# Do authentication login - gcloud auth application-default login - It will take you to the Google login page. Enter your credentials

# Run this to set quota for your project - gcloud auth application-default set-quota-project dp-iit-422513

# Use location - us-central1 beacuse asia won't work! 

# Code from this link - https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings#img-txt-request

from google.cloud import aiplatform
import vertexai

from vertexai.vision_models import Image, MultiModalEmbeddingModel

vertexai.init(project="dp-iit-422513", location="us-central1")

model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
image = Image.load_from_file("/home/venkateshriyer/Downloads/levis_elvis-fake.jpg")

embeddings = model.get_embeddings(
    image=image, 
    contextual_text= 'Levis'
    )

print(embeddings)
