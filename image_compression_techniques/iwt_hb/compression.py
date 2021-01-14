import huffman
import wavelet
import os
import numpy as np
import hilbert
import time
from PIL import Image
from bitstream import OutputBitStream, InputBitStream, from_binary_list, to_binary_list, pad_bits


def hilbert_compression(array):
    """ Takes an array, perform wavelet transform, do hilbert scan and return coefficients """
    output = np.zeros((array.shape[0]*2, array.shape[1], 3))
    print("Performing integer wavelet and hilbert scan on each channel...")

    for i in range(3):
        band = array[:, :, i]
        # Perform IWT on array
        coefficients = wavelet.iwt2(band)
        coefficients = coefficients[:band.shape[0], :band.shape[1]]
        # Perform Hilbert scan on coefficients
        hb = hilbert.decode(coefficients, 2, 5)

        hb = hb.reshape(output[:, :, i].shape)
        output[:, :, i] = hb

    return output


def hilbert_decompression(array, height, width):
    """ An array of scanned Hilbert coefficients is decoded to image array """
    output = np.zeros((height, width, 3))
    print("Performing Hilbert Scan and inversing the integer transform...")
    for i in range(3):
        band = array[:, :, i]
        band = band.reshape((height, width, 2))
        hb = hilbert.encode(band, 2, 5)
        hb = hb.reshape((height, width))

        coeffs = wavelet.iiwt2(hb)
        coeffs = coeffs[:height, :width]

        output[:, :, i] = coeffs

    output = output.astype('uint8')
    return output


def compress_image(input_file):
    before = time.time()
    path = os.path.dirname(__file__)+"/images/"+input_file
    print("Compressing %s ..." % input_file)
    image = Image.open(path)
    print("Image is %d x %d" % (image.size[0], image.size[1]))
    img_raw_size = huffman.raw_size(image.size[0], image.size[1])
    print("Image size is: %d byte." % img_raw_size)
    data = np.asarray(image)

    hilbert_array = hilbert_compression(data)

    hilbert_array = hilbert_array.astype('uint8')

    print("Counting symbols...")
    counts = huffman.count_hilbert(hilbert_array)

    print("Building tree...")
    tree = huffman.build_tree(counts)

    print("Trimming tree...")
    trimmed_tree = huffman.trim_tree(tree)

    print("Assigning codes to pixels...")
    codes = huffman.assign_codes(trimmed_tree)

    estimated_size = huffman.compressed_size(counts, codes)

    print("Estimated size: %d bytes" % estimated_size)

    output_path = os.path.dirname(__file__)+"/output/"+input_file[:-3]+"txt"

    print("Writing to %s..." % (input_file[:-3]+"txt"))
    stream = OutputBitStream(output_path)
    print("Encoding header...")
    huffman.encode_header(image, stream)
    stream.flush_buffer()
    print("Encoding tree...")
    huffman.encode_tree(trimmed_tree, stream)
    stream.flush_buffer()
    print("Encoding pixels...")
    huffman.encode_hilbert(hilbert_array, codes, stream)
    stream.close()

    after = time.time()
    real_size = stream.bytes_written
    print("Wrote %d bytes." % real_size)

    print("Estimate is %scorrect." %
          ('' if estimated_size == real_size else 'in'))
    print("Compression ratio: %0.2f" % (float(img_raw_size)/real_size))
    print("Took %0.2f seconds." % (after - before))

    return hilbert_array


def decompress_image(input_file):
    input_path = os.path.dirname(__file__)+"/output/"+input_file
    print("Decompressing '%s'..." % input_file)
    print("Reading file...")
    stream = InputBitStream(input_path)
    print("Decoding header...")
    height, width = huffman.decode_header(stream)
    stream.flush_buffer()
    print("Decoding the tree...")
    trimmed_tree = huffman.decode_tree(stream)
    stream.flush_buffer()
    print("Decoding the values...")
    array = huffman.decode_array(height, width, trimmed_tree, stream)
    stream.close()
    print("Read %d bytes." % stream.bytes_read)

    output = hilbert_decompression(array, height, width)

    image = Image.fromarray(output)

    path = os.path.dirname(__file__)+"/images/"+input_file[:-4]+"_hb.png"
    image.save(path)


compress_image("IMAGE")

decompress_image("IMAGE.txt")
