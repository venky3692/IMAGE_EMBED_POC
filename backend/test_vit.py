import numpy as np
from PIL import Image
from transformers import ViTFeatureExtractor, ViTModel
import torch

# Load ViT feature extractor
feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')

# Load ViT model
model = ViTModel.from_pretrained('google/vit-base-patch16-224')

# Load and preprocess images
image_paths = ["/home/sanjayvijaykumar/Documents/IMAGE_EMBED_POC/data_set/text_test/samsung-original.PNG", "/home/sanjayvijaykumar/Documents/IMAGE_EMBED_POC/data_set/samsung-fake.PNG"]  # List of image file paths
images = []
for image_path in image_paths:
    img = Image.open(image_path).convert('RGB')
    # img = img.resize((224, 224))  # Resize to 224x224 for ViT model
    images.append(img)

# Extract embeddings for each image
embeddings = []
for image in images:
    inputs = feature_extractor(images=image, return_tensors="pt")  # Convert to PyTorch tensor
    
    # Extract features
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.squeeze(0).mean(dim=0).numpy()  # Mean pooling of embeddings
        print("shape", embedding.shape)
    
    embeddings.append(embedding)

# Calculate cosine similarity
embedding1, embedding2 = embeddings
cosine_similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

print("Cosine Similarity:", cosine_similarity)
