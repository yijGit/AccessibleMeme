from skimage.metrics import structural_similarity
import argparse
from sys import argv
import imutils
from cv2 import cv2

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Computes the structural similarity index
# Used to see how similar/dissimilar the two given images are
def img_cmp(image1, image2):
    image_orig = cv2.imread(argv[1])
    image_mod = cv2.imread(argv[2])

    resized_orig = cv2.resize(image_orig, (300, 200))   
    resized_mod = cv2.resize(image_mod, (300, 200))

    gray_orig = cv2.cvtColor(resized_orig, cv2.COLOR_BGR2GRAY)
    gray_mod = cv2.cvtColor(resized_mod, cv2.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(gray_orig, gray_mod, full=True)
    results = [score, diff]
    return results

# Plots the two given images side-by-side and draws red rectangles 
# over regions w/ major differences in structural similarity index
def main(argv):
    results = img_cmp(argv[1], argv[2])
    score = results[0]
    diff = results[1]
    diff = (diff * 255).astype("uint8")
    print("Structural Similarity Index: {}".format(score))

    thresh = cv2.threshold(diff, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    image_orig = cv2.imread(argv[1])
    image_mod = cv2.imread(argv[2])
    resized_orig = cv2.resize(image_orig, (300, 200))   
    resized_mod = cv2.resize(image_mod, (300, 200))

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(resized_orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(resized_mod, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow("Original", resized_orig)
    cv2.imshow("Modified", resized_mod)
    cv2.imshow("Diff", diff)
    #cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)

    plt.show()

if __name__ == "__main__":
    main(argv)
