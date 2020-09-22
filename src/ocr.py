import re
import numpy as np
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt
from sys import argv
from cv2 import cv2 

IMG_DIR = '/Users/jlyi/Desktop/Meme Image Captioning/img_dir'

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 15, 255, cv2.THRESH_BINARY)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

def retrieve_text(argv):
    image = cv2.imread(IMG_DIR + argv[1])

    # Image correction to improve accuracy of OCR
    '''b,g,r = cv2.split(image)
    rgb_img = cv2.merge([r,g,b])
    plt.imshow(rgb_img)
    plt.title('Original Image')'''
    gray = get_grayscale(image)
    thresh = thresholding(gray)
    openi = opening(thresh)
    can = canny(openi)
    images = {'gray': gray, 'thresh': thresh, 'opening': openi, 'canny': can}

    # Shows the different phases of the image through correction
    # Uncomment code block below to plot them in four quadrant graph
    '''
    fig = plt.figure(figsize=(13,13))
    ax = []
    rows = 2
    columns = 2
    keys = list(images.keys())
    for i in range(rows*columns):
        ax.append( fig.add_subplot(rows, columns, i+1) )
        ax[-1].set_title('AUREBESH - ' + keys[i])
        plt.imshow(images[keys[i]], cmap='gray')
    plt.show()
    '''

    #custom_config = r'--oem 3 --psm 6'
    #, config=custom_config
    return pytesseract.image_to_string(image)

if __name__ == "__main__":
    retrieve_text(argv)