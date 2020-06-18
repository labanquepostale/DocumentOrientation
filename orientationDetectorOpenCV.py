from os import listdir
import numpy as np
import argparse
import cv2
import time

# fonction de rotation de l'image qui ne coupe pas les bords
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


start = time.clock() # début de mesure du temps d'execution du programme

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
    #print(image_name)

    (height, width) = img.shape[:2]

    # formattage de l'image
    image = img
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # accentue l'epaisseur du texte pour que les rectangles à détecter correspondent principalement à un mot
    # la taille du kernel pour la dilatation dépend du type de document.
    k_size = 5 # document dactylographié
    #k_size = 20 # document manuscrit

    kernel = np.ones((k_size, k_size), np.uint8)
    dila = cv2.dilate(thresh, kernel)

    # fonction de détection de contours d'OpenCV
    contours, hierarchy = cv2.findContours(dila, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # dans la langue française, il y a plus de lettres (et elles sont plus fréquentes) qui se prolongent vers le haut que vers le bas.
    # vers le haut : b d f h i k l t é è à ù
    # vers le bas : g j p q z(manuscrit)
    # en partant de ce constat, on cherche des rectangles contenant plusieurs lettres
    # on découpe chaque rectangle en deux dans le sens de la longueur
    # et on compare la valeur moyenne des pixels des deux côtés du rectangle.
    # cela permet d'incrémenter les valeurs count0 count90 count180 count270
    # La variable la plus élevée donne l'angle de l'image.
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

    # sauvegarde de l'image
    print("[INFO] angle: {:.3f}".format(angle))
    cv2.imwrite(output_path + "/rotated_" + image_name, rotated)

# fin de mesure du temps d'execution du programme
elapsed = time.clock()
elapsed = elapsed - start
print("Time spent : ", elapsed)
