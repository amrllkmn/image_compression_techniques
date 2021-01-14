from PIL import Image
import os
import io
import numpy
import cv2
import sys
import time


def get_image_values(path):

    from PIL import Image
    i = Image.open(path)

    pixels = i.load()  # this is not a list, nor is it list()'able
    width, height = i.size

    all_pixels = []
    for x in range(width):
        for y in range(height):

            cpixel = pixels[x, y]
            bw_value = int(round(sum(cpixel) / float(len(cpixel))))
            # the above could probably be bw_value = sum(cpixel)/len(cpixel)
            all_pixels.append(bw_value)

    return all_pixels, i.size


def compress(uncompressed):
    """Compress a string to a list of output symbols."""
    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size

            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result


def decompress(compressed):
    """Decompress a list of output ks to a string."""

    # Build the dictionary.
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop

    result = io.StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry

    return result.getvalue()


def regenerate_the_image(code, size, in_file):
    print("Regenerating the compresed image:\n")
    pixelList = []
    for c in code:
        pixelList.append(ord(c))
    # print("Key Values: ", pixelList)

    pixels_out = []
    for row in pixelList:
        pixels_out.append((row, row, row))

    # print("Image Pixels: ", pixels_out)

    # Convert the pixels into an array using numpy
    array = numpy.flip(numpy.array(
        pixels_out, dtype=numpy.uint8).reshape((size[0], size[1], 3)), 1)

    file_path = os.path.abspath(os.path.dirname(__file__))

    reconstructed = os.path.join(
        file_path, "images/"+in_file[:-4]+"_reconstructed.png")
    #ret = cv2.imwrite(reconstructed, array)

    # print(ret)

    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array)
    new_image.save(reconstructed)


def main(in_file):

    path = os.path.dirname(__file__)+"/images/"

    before = time.time()

    all_pixels, size = get_image_values(path+in_file)

    values = []

    for v in all_pixels:
        values.append(v)

    converted = []

    for f in values:
        converted.append(chr(f))

    string = ""

    for s in converted:
        string += str(s)

    print("Before compression: ", len(string) * 3)

    compressed_img = compress(string)

    with open(in_file[:-3]+"txt", "w") as f:
        f.write(str(compressed_img))

    after = time.time()
    print("After compression: ", len(compressed_img) * 3)
    print("Took %0.2f seconds." % (after-before))

    decompressed = decompress(compressed_img)

    print("After DE-compression: ", len(decompressed))

    regenerate_the_image(decompressed, size, in_file)


main("sat_image_3.png")
