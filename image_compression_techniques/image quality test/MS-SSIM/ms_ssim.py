import tensorflow as tf
import pathlib
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cv2
from PIL import Image

#list_ds = tf.data.Dataset.list_files()


path = os.path.dirname(__file__)

print(path)


def parse_image(filename):
    label = filename
    # CHANGE FOLDER NAME HERE
    image = tf.io.read_file(path+'/wavelets/'+filename)
    print(image.shape)
    image = tf.image.decode_png(image)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.reshape(image, image.shape)
    print(image.shape)
    return image, label


def calcMS_SSIM(image1, image2):
    score = tf.image.ssim_multiscale(image1, image2, max_val=1.0)
    return score


def calcSSIM(image1, image2):
    return tf.image.ssim(image1, image2, max_val=1.0, filter_size=11, filter_sigma=1.5, k1=0.01, k2=0.03)


def show(image, label):
    plt.figure()
    plt.imshow(image)
    plt.title(label)
    plt.axis('off')
    plt.show()


image, label = parse_image('sat_image_3.png')  # Put original image name here
#show(image, label)
img_compressed, label_compressed = parse_image(
    'sat_image_3_integer_wavelet.png')  # Put reconstructed/compressed image here
#show(img_compressed, label_compressed)

ms_ssim = calcMS_SSIM(image, img_compressed)
ssim = calcSSIM(image, img_compressed)
print("MS-SSIM: %0.3f" % ms_ssim)
print("SSIM: %0.3f" % ssim)
