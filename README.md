# Image Compression Techniques
All the image compression techniques used in the study. There are five techniques used:
1. Discrete Wavelet Transforms
2. Huffman Encoding
3. Integer Wavelet Transform with Hilbert and Huffman
4. K-Means Clustering
5. LZW Compression

## Discrete Wavelet Transforms
It has two subfolders: Daubechies and Integer Wavelet.

TO USE: 
1. Create a folder called 'images' and insert it into subfolder. Fill the folder with images to be tested.
2. Open the script in editor.
3. Call the function wavelet_compression() with image name (e.g: 'image_1.png') as an argument.
        
## Huffman Encoding
TO USE:
1. Open terminal at the folder.
2. Run "py main.py image_1.png image_1.txt".

## Integer Wavelet Transform with Hilbert and Huffman
TO USE:
1. Create a folder called 'images' and insert it into subfolder. Fill the folder with images to be tested.
2. Go to 'compression.py'
3. Call the function compress_image() with image name (e.g: 'image_1.png') as an argument.
4. To decompress, at the same script, call decompress_image() with image output file (image_1.txt) as an argument.

## K-Means Clustering
TO USE:
1. Make sure image is in same folder as the script.
2. Open terminal, and run "py k_means.py image_1.png no_of_clusters"

## LZW Compression
TO USE:
1. Create a folder called 'images' and insert it into subfolder. Fill the folder with images to be tested.
2. Open script. Call main() with image name (e.g: 'image_1.png') as an argument.

## Image Quality Test
There are two image quality test used. MS-SSIM and Histograms.

For MS-SSIM:
1. Put folder of test images in the same folder as 'ms_ssim.py' script.
2. Change the file path to the test folder, in the code.
3. Change the name of the images where parse_image() is being called.

For Histograms:
1. Make sure the script is in the same folder as the images.
2. Open terminal, and run "py histogram.py original_img.png compressed_img.png".
