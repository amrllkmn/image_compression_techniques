import huffman_new
import os
import sys


def main():
    inputfile = str(sys.argv[1])
    outputfile = str(sys.argv[2])

    #huffman_new.compress_image(inputfile, outputfile)
    #print("-" * 40)
    output_img = inputfile[:-4]+"_reconstructed.png"
    huffman_new.decompress_image(outputfile, output_img)


if __name__ == "__main__":
    main()
