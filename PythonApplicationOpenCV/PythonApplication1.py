import cv2
import numpy as np
import glob
import argparse


def function(x): #Função necessaria por conta do metodo implementado no openCV
    pass


def load_coefficients(path):
    """ Carregando a matriz da camera e os coeficientes de distorção """

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]


# Tratando a imagem apartir de erosão e dilatação
cv2.namedWindow('dilated image mask')
cv2.createTrackbar('erosion', 'dilated image mask', 2, 5, function)
cv2.createTrackbar('dilation', 'dilated image mask', 2, 5, function)
cv2.createTrackbar('erosion2', 'dilated image mask', 2, 5, function)
cv2.createTrackbar('dilation2', 'dilated image mask', 0, 5, function)


# Webcamera no 0 é usada para captura de frames
cap = cv2.VideoCapture(0)

# Loop
while(1):
    # => Para utilizar uma figura
    frame = cv2.imread(r'E:\\PythonApplication1\\laser.jpg')
    # _, frame = cap.read() #=>Para capturar video
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([160, 50, 50])
    upper_red = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Filtros de erosão e dilatação
    value_eroded = cv2.getTrackbarPos('erosion', 'dilated image mask')
    value_dilated = cv2.getTrackbarPos('dilation', 'dilated image mask')
    value_eroded2 = cv2.getTrackbarPos('erosion2', 'dilated image mask')
    value_dilated2 = cv2.getTrackbarPos('dilation2', 'dilated image mask')

    kernel = np.ones((4, 4), np.uint8)
    eroded_image = cv2.erode(mask, kernel, iterations=value_eroded)
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=value_dilated)
    eroded_image = cv2.erode(dilated_image, kernel, iterations=value_eroded2)
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=value_dilated2)

    # ----------------------Visualização das etapas de processamento de imagem até a imagem final
    ##res = cv2.bitwise_and(frame,frame, mask= mask)
    # cv2.imshow('frame',frame)
    # cv2.imshow('mask',mask)
    # cv2.imshow('res',res)
    #cv2.imshow('erode image mask',eroded_image)
    #cv2.imshow('dilated image mask',dilated_image)

    color_find = 255
    indexes = np.argwhere(dilated_image == color_find)
    for j in range(700):
        for i in range(700):
            if dilated_image[i][j] > 0:
                circle_image = cv2.circle(
                    frame, (j, i), radius=0, color=(120, 255, 255), thickness=-1)
                break
    cv2.imshow('dilated image mask', circle_image)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# Fecha todos os HighGUI windows.
cv2.destroyAllWindows()

# Libera a captura
cap.release()
