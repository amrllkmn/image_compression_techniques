import pywt
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
        coeffs = pywt.wavedec2(band, wavelet="db1", level=2)

    # coeff_to_array
        coeff_arr, coeff_slices = pywt.coeffs_to_array(coeffs)

    # Do the thresholding
        Csort = np.sort(np.abs(coeff_arr.reshape(-1)))

        thresh = Csort[int(np.floor((1-0.3)*len(Csort)))]

        ind = np.abs(coeff_arr) > thresh

        Cfilt = coeff_arr * ind

        coeffs_filt = pywt.array_to_coeffs(
            Cfilt, coeff_slices, output_format='wavedec2')

        arecon = pywt.waverec2(coeffs_filt, wavelet="db1")
        arecon = arecon.astype('uint8')

        width, height = arecon.shape[1], arecon.shape[0]
        if output.shape[0] != height and output.shape[1] != width:
            output[:, :, i] = arecon[:arecon.shape[0]-1, :arecon.shape[1]-1]
        elif output.shape[0] != height:
            output[:, :, i] = arecon[:arecon.shape[0]-1, :]
        elif output.shape[1] != width:
            output[:, :, i] = arecon[:, :arecon.shape[1]-1]
        else:
            output[:, :, i] = arecon[:, :, ]
        i += 1  # Decomp

    return output


def single_channel_compression(array):
    output = np.zeros(array.shape, dtype='uint8')

    coeffs = pywt.wavedec2(array, wavelet="db1", level=2)

    # coeff_to_array
    coeff_arr, coeff_slices = pywt.coeffs_to_array(coeffs)

    # Do the thresholding
    Csort = np.sort(np.abs(coeff_arr.reshape(-1)))

    thresh = Csort[int(np.floor((1-0.3)*len(Csort)))]

    ind = np.abs(coeff_arr) > thresh

    Cfilt = coeff_arr * ind

    coeffs_filt = pywt.array_to_coeffs(
        Cfilt, coeff_slices, output_format='wavedec2')

    arecon = pywt.waverec2(coeffs_filt, wavelet="db1")
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
        print("Performing three channel compression")
    else:
        print("Performing single channel compression")

    output = three_channel_compression(
        data) if channel == 3 else single_channel_compression(data)

    a_img = Image.fromarray(output)

    a_img.save(path[:-4]+"_pywavelet.png")
    after = time.time()

    print("Compression took %0.2f seconds." % (after - before))


inpt = "IMAGE NAME HERE"
wavelet_compression(inpt)
