from collections import Counter
from itertools import chain
from PIL import Image
from bitstream import OutputBitStream, InputBitStream, from_binary_list, to_binary_list, pad_bits
import os
import time


def count_symbols(image):
    """ Count the intensity of pixels in an image """
    pixels = image.getdata()
    values = chain.from_iterable(pixels)
    counts = Counter(values).items()

    return sorted(counts, key=lambda x: x[::-1])


def build_tree(counts):
    """Build the huffman tree """
    nodes = [elements[::-1] for elements in counts]
    while len(nodes) > 1:
       # Get two symbols with the smallest frequency
        least_two_symbols = tuple(nodes[0:2])
        print(type(least_two_symbols))
        the_others = nodes[2:]
        print(type(the_others[:2]))
        # Add up the frequencies of the smallest two symbol, to create the branch point
        combined_freq = least_two_symbols[0][0] + least_two_symbols[1][0]
        # Add the branch point to the end
        new_node = [(combined_freq, least_two_symbols)]
        print(type(new_node))
        nodes = the_others + new_node
        nodes.sort(key=lambda t: t[0])
    return nodes[0]


def trim_tree(tree):
    """ Remove the frequencies of the symbols from the trees """
    root = tree[1]  # Get the root node of the tree
    if type(root) is tuple:
        # Trim the left branch and the right branch of the root then recombine
        return (trim_tree(root[0]), trim_tree(root[1]))
    return root  # If no children, return the root


def assign_codes_to_pixels(codes, node, pattern):
    """ Assign code to the node on the tree """
    if type(node) == tuple:
        # Do the left branch
        assign_codes_to_pixels(codes, node[0], pattern + [0])
        # Do the right branch
        assign_codes_to_pixels(codes, node[1], pattern + [1])
    else:
        codes[node] = pattern


def assign_codes(tree):
    codes = {}
    assign_codes_to_pixels(codes, tree, [])
    return codes


def raw_size(width, height):
    """ Get the raw size of the image """
    header_size = 2 * 16  # height and width as 16 bit values
    pixels_size = 3 * 8 * width * height  # 3 channels, 8 bits per channel
    return (header_size + pixels_size) / 8


""" COMPRESSION """


def compressed_size(counts, codes):
    """ Get the size of the compressed file """

    header_size = 2 * 16

    tree_size = len(counts) * (1+8)
    tree_size += len(counts) - 1
    if tree_size % 8 > 0:
        tree_size += 8 - (tree_size % 8)

    pixels_size = sum([count * len(codes[symbol]) for symbol, count in counts])
    if pixels_size % 8 > 0:
        pixels_size += 8 - (pixels_size % 8)

    return (header_size + tree_size + pixels_size) / 8


def encode_header(image, bitstream):
    """ Add the height and width information of the image to the encoded file"""
    height_bits = pad_bits(to_binary_list(image.height), 16)
    bitstream.write_bits(height_bits)
    width_bits = pad_bits(to_binary_list(image.width), 16)
    bitstream.write_bits(width_bits)


def encode_tree(tree, bitstream):
    """ Encode the huffman tree into the file """
    if type(tree) == tuple:  # If the tree has branches
        bitstream.write_bit(0)
        encode_tree(tree[0], bitstream)
        encode_tree(tree[1], bitstream)
    else:  # If there's no children
        bitstream.write_bit(1)
        symbol_bits = pad_bits(to_binary_list(tree), 8)
        bitstream.write_bits(symbol_bits)


def encode_pixels(image, codes, bitstream):
    for pixel in image.getdata():
        for value in pixel:
            bitstream.write_bits(codes[value])


def compress_image(input_file, output_file):
    before = time.time()
    input_path = os.path.dirname(__file__)+"/images/"+input_file

    print("Compressing '%s' --> '%s'...." % (input_file, output_file))
    image = Image.open(input_path)
    print("Image height: %d, width: %d" % (image.height, image.width))
    img_raw_size = raw_size(image.width, image.height)
    print("Raw image size: %d bytes" % img_raw_size)
    print("Counting symbols...")
    counts = count_symbols(image)
    print("Building tree...")
    tree = build_tree(counts)
    print("Trimming tree...")
    trimmed_tree = trim_tree(tree)
    print("Assigning codes to pixels...")
    codes = assign_codes(trimmed_tree)

    estimated_size = compressed_size(counts, codes)
    print("Estimated size: %d bytes" % estimated_size)

    print("Writing to %s..." % output_file)
    output_path = os.path.dirname(__file__)+"/output/"+output_file
    stream = OutputBitStream(output_path)
    print("Encoding header...")
    encode_header(image, stream)
    stream.flush_buffer()
    print("Encoding tree...")
    encode_tree(trimmed_tree, stream)
    stream.flush_buffer()
    print("Encoding pixels...")
    encode_pixels(image, codes, stream)
    stream.close()

    after = time.time()
    real_size = stream.bytes_written
    print("Wrote %d bytes." % real_size)

    print("Estimate is %scorrect." %
          ('' if estimated_size == real_size else 'in'))
    print("Compression ratio: %0.2f" % (float(img_raw_size)/real_size))
    print("Took %0.2f seconds." % (after - before))


""" DECOMPRESSION """


def decode_header(bitstream):
    """ Return the width and height """
    height = from_binary_list(bitstream.read_bits(16))
    width = from_binary_list(bitstream.read_bits(16))
    return (height, width)


def decode_tree(bitstream):
    """ Decoding the tree from the encoded file """
    flag = bitstream.read_bits(1)[0]
    if flag == 1:
        return from_binary_list(bitstream.read_bits(8))

    left = decode_tree(bitstream)
    right = decode_tree(bitstream)

    return (left, right)


def decode_value(tree, bitstream):
    """ Decoding the values of the image from the tree """
    bit = bitstream.read_bits(1)[0]
    node = tree[bit]
    if type(node) == tuple:  # If children exists
        return decode_value(node, bitstream)

    return node


def decode_pixels(height, width, tree, bitstream):
    pixels = bytearray()
    for i in range(height * width * 3):
        node = decode_value(tree, bitstream)
        pixels.append(node)

    return Image.frombytes('RGB', (width, height), bytes(pixels))


def decompress_image(input_file, output_file):
    input_path = os.path.dirname(__file__)+"/output/"+input_file
    print("Decompressing '%s'..." % input_file)
    print("Reading file...")
    stream = InputBitStream(input_path)
    print("Decoding header...")
    height, width = decode_header(stream)
    stream.flush_buffer()
    print("Decoding the tree...")
    trimmed_tree = decode_tree(stream)
    stream.flush_buffer()
    print("Decoding the values...")
    image = decode_pixels(height, width, trimmed_tree, stream)
    stream.close()
    print("Read %d bytes." % stream.bytes_read)
    output_path = os.path.dirname(__file__)+"/images/"+output_file
    image.save(output_path)
