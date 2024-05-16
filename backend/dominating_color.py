import numpy as np
import cv2
from sklearn.cluster import KMeans
import math

def preprocess_image(image):
    resized_image = cv2.resize(image, (100, 100))
    image_cvt = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    pixels = image_cvt.reshape((-1, 3))
    pixels = np.float32(pixels)
    return pixels


def get_dominant_colors(pixels, k=3):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)
    # Get the cluster centers and their labels
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_
    # Count the frequency of each cluster label
    unique_labels, label_counts = np.unique(labels, return_counts=True)
    # Sort labels by frequency in descending order
    sorted_indices = np.argsort(label_counts)[::-1]
    # Get dominant colors and their frequencies
    dominant_colors = colors[unique_labels[sorted_indices]]
    dominant_frequencies = label_counts[sorted_indices]
    return dominant_colors

def color_distance(color1, color2):
    """
    Calculate the Euclidean distance between two RGB colors.
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)

def compare_colors(colors1, colors2, threshold):
    """
    Compare colors between two lists of colors.
    """
    similar_colors = []
    
    for color1 in colors1:
        for color2 in colors2:
            distance = color_distance(color1, color2)
            print('distance', distance, color1, color2)
            if abs(distance) < threshold:
                similar_colors.append((color1, color2, distance))
                break  # Only consider the closest match
            
    return similar_colors

def display_dominant_colors(dominant_colors, idx):
    bar = np.zeros((50, 300, 3), dtype=np.uint8)
    startX = 0
    for color in dominant_colors:
        endX = startX + (300 // len(dominant_colors))
        cv2.rectangle(
            bar, (int(startX), 0), (int(endX), 50), color[0].astype(int).tolist(), -1
        )
        startX = endX

    cv2.imwrite("Dominant Colors"+idx+".png", bar)

def dominating_color(image_path, image_path1):
    num_colors = 3

    image = cv2.imread(image_path)

    preprocessed_image = preprocess_image(image)

    image1 = cv2.imread(image_path1)

    preprocessed_image1 = preprocess_image(image1)
    dominant_colors = get_dominant_colors(preprocessed_image, k=num_colors)
    dominant_colors1 = get_dominant_colors(preprocessed_image1, k=num_colors)
    print("dominating color1", dominant_colors)
    print("dominating color2", dominant_colors1)
    
    colors_same = compare_colors(dominant_colors, dominant_colors1, 50);
    print("colors_same", colors_same)
    dominating_color_percent = ((len(colors_same)/(len(dominant_colors))+(len(colors_same)/len(dominant_colors1))))/2
    print("percentage of domianting color", dominating_color_percent)
    # display_dominant_colors(dominant_colors, "1")
    # display_dominant_colors(dominant_colors1, "2")
    # for color in colors_same:
    #     closest_name = ''
    #     try:
    #         closest_name = webcolors.rgb_to_name(color)
    #     except ValueError:
    #         closest_name = None
    #     print("colorname", closest_name)
    return dominating_color_percent, colors_same
