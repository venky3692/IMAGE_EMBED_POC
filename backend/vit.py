from transformers import ViTFeatureExtractor, ViTModel
import torch
from PIL import Image
from image_similarity_measures.quality_metrics import rmse, psnr, ssim, fsim, issm, sre, sam, uiq

# Load the feature extractor and the model
feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
model = ViTModel.from_pretrained('google/vit-base-patch16-224')


def get_embeddings(image_paths):

	# Assuming you have a list of images
	images = [Image.open(image_path) for image_path in image_paths]

	# Preprocess all images
	inputs = feature_extractor(images=images, return_tensors="pt")

	# Forward pass to get the embeddings
	with torch.no_grad():
    		outputs = model(**inputs)

	# Get the embeddings
	embeddings = outputs.last_hidden_state
	print(f"Embedding shape in the current batch size: {embeddings.shape}")  # (batch_size, seq_len, hidden_size)
	
	return embeddings
	
def compute_similarity(embedding1, embedding2, metric="rmse"):

	if metric == "rmse":
		return	rmse(org_img=embedding1.numpy(), pred_img=embedding2.numpy())
	if metric == "psnr":
		return	psnr(org_img=embedding1.numpy(), pred_img=embedding2.numpy())
	#if metric == "ssim":
	#	return	ssim(org_img=embedding1.numpy(), pred_img=embedding2.numpy())
	#if metric == "fsim":
	#	return	fsim(org_img=embedding1.numpy(), pred_img=embedding2.numpy())
	if metric == "issm":
		return	issm(org_img=embedding1.numpy(), pred_img=embedding2.numpy())
	if metric == "sre":
		return	sre(org_img=embedding1.numpy(), pred_img=embedding2.numpy())
	if metric == "sam":
		return	sam(org_img=embedding1.numpy(), pred_img=embedding2.numpy())
	if metric == "uiq":
		return	uiq(org_img=embedding1.numpy(), pred_img=embedding2.numpy())


