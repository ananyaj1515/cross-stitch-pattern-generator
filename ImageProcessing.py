from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

# my helper functions
def hex_to_tuple(hex_color):
    if not isinstance(hex_color, str):
        return None
    hex_color = hex_color.strip().lstrip('#')

    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (r, g, b)

dmc_df = pd.read_csv('dmc.csv')
dmc_df.columns = dmc_df.columns.str.strip()
dmc_df['rgb_tuple'] = dmc_df['RGB_COLOR'].apply(hex_to_tuple)


def calculateDimensions(original_width, original_height, max_dim=50):
    scale_factor = max_dim / max(original_height, original_width)
    new_width = round(original_width * scale_factor)
    new_height = round(original_height * scale_factor)
    return (new_width, new_height)

def resizeImage(img, dims):
    res = img.resize(dims, Image.Resampling.LANCZOS)
    return res

def colourQuantisation(img):
    n_colours = 15
    reshaped = img.reshape(-1, 3) 
    model = KMeans(
        n_clusters=n_colours,
        n_init=10,
        random_state=42
    )
    labels = model.fit_predict(reshaped)
    colours = model.cluster_centers_.astype("uint8")
    # output_image = colors[labels].reshape(img.shape)
    # plt.imshow(output_image)
    # plt.axis("off")
    # plt.show()
    print(colours)
    return colours, labels


def find_dmc_match(pixels):
    colors = colourQuantisation(pixels)   # (15, 3)
    dmc_rgb_array = np.array(dmc_df['rgb_tuple'].tolist())  # (456, 3)

    distances = np.linalg.norm(
        colors[:, None, :] - dmc_rgb_array[None, :, :],
        axis=2
    )

    closest_indices = np.argmin(distances, axis=1)
    matches = dmc_df.iloc[closest_indices].copy()
    matches['cluster_rgb'] = list(map(tuple, colors))
    return matches


img = Image.open("test3.jpeg")
new_image = resizeImage(img, calculateDimensions(img.size[0], img.size[1], 50))
new_image.save("new-test3.png")

pixels = np.array(new_image)
print(f"Grid Image: {pixels.shape}")
print(f"Color at (0,0) {pixels[0,0]}")
print(f"Total unique colors {len(np.unique(pixels.reshape(-1,3), axis=0))}")

find_dmc_match(pixels)
