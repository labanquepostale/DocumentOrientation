from os import listdir
import numpy as np
import argparse
import cv2
import time

# Image rotation without cropping
def rotate_bound(image, angle, borderValue):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    return cv2.warpAffine(image, M, (nW, nH), borderValue=borderValue)


start = time.clock() # Start timer for measuring execution delay

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image directory")
ap.add_argument("-o", "--output", required=True,
                help="path to output image directory")
args = vars(ap.parse_args())

input_path = args['image']
output_path = args['output']

list_images = listdir(input_path)

for image_name in list_images:
    img = cv2.imread(input_path + "/" + image_name)

    (height, width) = img.shape[:2]

    # Image formatting 
    image = img
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Increase text thickness for a better word detection
    # Kernel size for dilatation (depending of document size)
    k_size = 5 # Non hand-written document
    #k_size = 20 # Hand-written document

    kernel = np.ones((k_size, k_size), np.uint8)
    dila = cv2.dilate(thresh, kernel)

    # Contours Detection
    contours, hierarchy = cv2.findContours(dila, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    # Detects the orientation of the text by measuring in the rectangle contouring the word how much ink is in the upper part
    # and how much is in the lower part. If the word is in the right orientation, more ink will be displayed in the upper part
    # as more letter in french have an upper part (eg. b d f h i k l t é è à ù )
    count0 = 0
    count90 = 0
    count180 = 0
    count270 = 0
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        if width * height // 10 > w * h > 500 and (h // w < 10 and w // h < 10):# rectangle suffisamment grand mais pas trop non plus pour correspondre à du texte (valeurs experimentales)
            cv2.rectangle(dila, (x, y), (x + w, y + h), (255, 0, 0), 2)
            if w < h:
                side1 = cv2.mean(img[y:y+h, x:x + w // 2])
                side2 = cv2.mean(img[y:y+h, x + w // 2:x+w])
                if side1[0] > side2[0]:
                    #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    count90 += 1
                else:
                    #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    count270 += 1
            else:
                side1 = cv2.mean(img[y:y + h // 2, x:x+w])
                side2 = cv2.mean(img[y + h // 2:y+h, x:x+w])
                if side1[0] > side2[0]:
                    #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    count0 += 1
                else:
                    #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
                    count180 += 1

    max_deg = max(count0, count90, count180, count270)
    angle = 0
    if count90 == max_deg:
        angle = 90
    elif count180 == max_deg:
        angle = 180
    elif count270 == max_deg:
        angle = 270

    rotated = rotate_bound(img, angle, borderValue=(255, 255, 255))

    # Save image
    print("[INFO] angle: {:.3f}".format(angle))
    cv2.imwrite(output_path + "/rotated_" + image_name, rotated)

# Stop measuring time
elapsed = time.clock()
elapsed = elapsed - start
print("Time spent : ", elapsed)
