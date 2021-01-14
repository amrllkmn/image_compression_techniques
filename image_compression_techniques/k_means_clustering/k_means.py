from sklearn.cluster import MiniBatchKMeans
import numpy as np
import cv2
import sys

# IMAGES THAT ARE USED IN THE SCRIPT MUST BE IN THE SAME FOLDER AS THE SCRIPT
# TO RUN, OPEN COMMAND TERMINAL AT THE LOCATION OF THE SCRIPT AND IMAGES AND TYPE: py k_means.py img_name.png no_of_clusters
# Takes image name and number of clusters required and saves the compressed image in the folder where the script is saved."


def compress(image, k_clusters):
    img = cv2.imread(image)
    shape = img.shape
    img = img.reshape(shape[0]*shape[1], 3)

    kmeans = MiniBatchKMeans(k_clusters).fit(img)

    compressed_img = kmeans.cluster_centers_[kmeans.labels_]
    compressed_img = np.clip(compressed_img.astype('uint8'), 0, 255)

    compressed_img = compressed_img.reshape(shape)

    # The filename of the image will be: filename_compressed_k_clusters.png
    cv2.imwrite(image[:-4]+"_compressed_" +
                str(k_clusters)+".png", compressed_img)


def main():
    image = str(sys.argv[1])
    no_clusters = int(sys.argv[2])
    print("Compressing "+image+"...")
    compress(image, no_clusters)
    print("Compression complete.")


if __name__ == "__main__":
    main()
