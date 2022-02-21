import cv2
import numpy as np
import glob
import argparse

# Codigo para calibração
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def calibrate(dirpath, prefix, image_format, square_size, width=9, height=6):

    # preparar pontos, como (0,0,0) ou (8,6,0)
    objp = np.zeros((height * width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    objp = objp * square_size

    # Vetores para armazenar pontos de objeto e pontos de imagem para cada imagem usada na calibração
    objpoints = []  # pontos 3d no mundo real
    imgpoints = []  # pontos 2d na figura.

    if dirpath[-1:] == '/':
        dirpath = dirpath[:-1]

    images = glob.glob(dirpath + '/' + prefix + '*.' + image_format)

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Encontrando as bordas do tabuleiro de xadrez
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        # Se encontrar, adicionar pontos de objeto
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Desenhando no display
            img = cv2.drawChessboardCorners(
                img, (width, height), corners2, ret)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)

    return [ret, mtx, dist, rvecs, tvecs]
# dirpath: Diretorio das imagens para calibração
# prefix: Todas as imagens devem ter o mesmo nome e o prefixo sendo o nome sem
# numeração image1.jpg
# square_size: Tamanho da borda de um quadrado
# width: Número de pontos de intersecção de quadrados no lado comprido do quadro
# de calibração.
# heigth: Número de pontos de intersecção de quadrados no lado curto do quadro
# de calibração
# A função retorna ret, mtx, dist, rvecs, tvecs.


def save_coefficients(mtx, dist, path):
    """ Salvando a matriz da camera e os coeficientes de distorção em um arquivo """
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write("K", mtx)
    cv_file.write("D", dist)
    # é realease mesmo, não close
    cv_file.release()


def load_coefficients(path):
    """ Carregando a matriz da camera e os coeficientes de distorção """

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]
