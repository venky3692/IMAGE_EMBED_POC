import cv2

def calculate_color_histogram(image):
    """
    Calculate color histogram for an image.
    """
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate histogram for each channel (Hue, Saturation, Value)
    hist_hue = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    hist_saturation = cv2.calcHist([hsv], [1], None, [256], [0, 256])
    hist_value = cv2.calcHist([hsv], [2], None, [256], [0, 256])
    
    # Normalize histograms
    hist_hue /= hist_hue.sum()
    hist_saturation /= hist_saturation.sum()
    hist_value /= hist_value.sum()
    
    return hist_hue, hist_saturation, hist_value

def compare_color_histograms(hist1, hist2):
    """
    Compare color histograms using Bhattacharyya distance.
    """
    # Calculate Bhattacharyya distance for each channel
    distance_hue = cv2.compareHist(hist1[0], hist2[0], cv2.HISTCMP_BHATTACHARYYA)
    distance_saturation = cv2.compareHist(hist1[1], hist2[1], cv2.HISTCMP_BHATTACHARYYA)
    distance_value = cv2.compareHist(hist1[2], hist2[2], cv2.HISTCMP_BHATTACHARYYA)
    
    # Calculate overall similarity score
    similarity_score = 1 - (distance_hue + distance_saturation + distance_value) / 3
    
    return similarity_score

def compare_color_similarity(image_path1, image_path2):
    """
    Compare color similarity between two images.
    """
    # Read images
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)
    
    # Calculate color histograms for each image
    hist1 = calculate_color_histogram(image1)
    hist2 = calculate_color_histogram(image2)
    
    # Compare color histograms
    similarity_score = compare_color_histograms(hist1, hist2)
    
    return similarity_score

# # Example usage
# image1_path = "starbucks-original.PNG"
# image2_path = "starbucks-fake.PNG"
# similarity_score = compare_color_similarity(image1_path, image2_path)
# print("Color similarity score between the images:", similarity_score)