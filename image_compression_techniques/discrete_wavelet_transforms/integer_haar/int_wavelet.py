import wavelet
from PIL import Image
import numpy as np
import os
import time


def three_channel_compression(array):

    output = np.zeros(array.shape, dtype='uint8')

    red = array[:, :, 0]
    green = array[:, :, 1]
    blue = array[:, :, 2]

    i = 0
    for band in (red, green, blue):
        # Decompose image
        coeffs = wavelet.iwt2(band)

    # Do the thresholding
        Csort = np.sort(np.abs(coeffs.reshape(-1)))

        thresh = Csort[int(np.floor((1-0.3)*len(Csort)))]

        ind = np.abs(coeffs) >= thresh

        Cfilt = coeffs * ind

        arecon = wavelet.iiwt2(Cfilt)
        arecon = arecon.astype('uint8')

        print(output.shape, arecon.shape)
        output[:, :, i] = arecon[:output.shape[0], :output.shape[1]]
        i += 1  # Decomp

    return output


def single_channel_compression(array):
    output = np.zeros(array.shape, dtype='uint8')

    coeffs = wavelet.iwt2(array)

    # Do the thresholding
    Csort = np.sort(np.abs(coeffs.reshape(-1)))

    thresh = Csort[int(np.floor((1-0.3)*len(Csort)))]

    ind = np.abs(coeffs) > thresh

    Cfilt = coeffs * ind

    Cfilt = Cfilt.reshape(array.shape)

    arecon = wavelet.iiwt2(Cfilt)
    arecon = arecon.astype('uint8')

    if arecon.shape[0] % 2 != 0:
        output[:, :] = arecon[:arecon.shape[0], :]
    elif arecon.shape[1] % 2 != 0:
        output[:, :] = arecon[:, :arecon.shape[1]]
    else:
        output[:, :] = arecon[:, :]

    return output


def wavelet_compression(input_file):
    before = time.time()
    path = os.path.dirname(__file__)+"/images/"+input_file

    # Open image
    image = Image.open(path)

    data = np.asarray(image)

    channel = len(data.shape)

    if channel == 3:
        print("Performing three channel integer wavelet compression")
    else:
        print("Performing single channel integer wavelet compression")

    output = three_channel_compression(
        data) if channel == 3 else single_channel_compression(data)

    a_img = Image.fromarray(output)

    a_img.save(path[:-4]+"_integer_wavelet.png")
    after = time.time()

    print("Compression took %0.2f seconds." % (after - before))


inpt = "IMAGE NAME HERE"
wavelet_compression(inpt)
