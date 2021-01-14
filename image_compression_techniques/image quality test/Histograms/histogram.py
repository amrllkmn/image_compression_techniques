import cv2 as cv
import numpy as np
import sys

# IMAGES THAT ARE USED IN THE SCRIPT MUST BE IN THE SAME FOLDER AS THE SCRIPT
# TO RUN, OPEN COMMAND TERMINAL AT THE LOCATION OF THE SCRIPT AND IMAGES AND TYPE: py histogram.py original_img.png compressed_img.png
# Takes an image filename and creates a RGB histogram


def createHistogram(image):

    src = cv.imread(image)

    rgb_split = cv.split(src)

    hist_size = 256

    histRange = (0, hist_size)

    r_hist = cv.calcHist(rgb_split, [2], None, [
                         hist_size], histRange, accumulate=False)

    g_hist = cv.calcHist(rgb_split, [1], None, [
                         hist_size], histRange, accumulate=False)

    b_hist = cv.calcHist(rgb_split, [0], None, [
                         hist_size], histRange, accumulate=False)

    hist_width = 512

    hist_height = 400

    bin_w = int(round(hist_height/hist_size))

    hist_img = np.zeros((hist_height, hist_width, 3), dtype=np.uint8)

    cv.normalize(r_hist, r_hist, alpha=0, beta=hist_height,
                 norm_type=cv.NORM_MINMAX)
    cv.normalize(g_hist, g_hist, alpha=0, beta=hist_height,
                 norm_type=cv.NORM_MINMAX)
    cv.normalize(b_hist, b_hist, alpha=0, beta=hist_height,
                 norm_type=cv.NORM_MINMAX)

    for i in range(1, hist_size):
        cv.line(hist_img, (bin_w*(i-1), hist_height - int(r_hist[i-1].round())), (bin_w*(
            i), hist_height - int(r_hist[i].round())), (0, 0, 255), thickness=2)
        cv.line(hist_img, (bin_w*(i-1), hist_height - int(g_hist[i-1].round())), (bin_w*(
            i), hist_height - int(g_hist[i].round())), (0, 255, 0), thickness=2)
        cv.line(hist_img, (bin_w*(i-1), hist_height - int(b_hist[i-1].round())), (bin_w*(
            i), hist_height - int(b_hist[i].round())), (255, 0, 0), thickness=2)

    return hist_img


def main():
    # Shows the histogram generated and saves the histogram as an image (after closing the image window) in the same folder this script is in.
    source_img = str(sys.argv[1])
    compressed_img = str(sys.argv[2])

    source_hist = createHistogram(source_img)
    compressed_hist = createHistogram(compressed_img)
    cv.imshow(source_img+" Histogram", source_hist)
    cv.imshow(compressed_img+" Histogram", compressed_hist)
    cv.waitKey()
    cv.imwrite(source_img[:-4]+"_histogram.png", source_hist)
    cv.imwrite(compressed_img[:-4]+"_histogram.png", compressed_hist)


if __name__ == "__main__":
    main()
