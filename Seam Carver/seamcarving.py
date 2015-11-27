# -*- coding: utf-8 -*-

"""
Created on Tue Oct 27 18:31:27 2015
@author: Richa
"""

from matplotlib.pyplot import figure, \
    gray, subplot, title, show, imread, imshow
from skimage import filters, img_as_float
import skimage
from numpy import *
import numpy as numpy


def dual_gradient_energy(img):  # a W x H array of floats, the energy at each pixel in image.
        R = img[:, :, 0]        # Stores the red component of the image
        G = img[:, :, 1]
        B = img[:, :, 2]

        horRed = skimage.filters.sobel_h(R)         #computes a horizontal approximation of the gradient of red band
        verRed = skimage.filters.sobel_v(R)         #computes a vertical approximation of the gradient of red band
        horGr = skimage.filters.sobel_h(G)          #computes a horizontal approximation of the gradient of green band
        verGr = skimage.filters.sobel_v(G)          #computes a vertical approximation of the gradient of green band
        horBl = skimage.filters.sobel_h(B)          #computes a horizontal approximation of the gradient of blue band
        verBl = skimage.filters.sobel_v(B)          #computes a vertical approximation of the gradient of blue band
        energy_x = numpy.add(numpy.square(horRed), numpy.square(horGr))
        x_energy = numpy.add(energy_x, numpy.square(horBl))    # net horizontal energy computed
        energy_y = numpy.add(numpy.square(verGr), numpy.square(verRed))
        y_energy = numpy.add(energy_y, numpy.square(verBl))     # net vertical energy computed
        energy_total = x_energy + y_energy              # Applying the gradient formula to calculate net energy
        return energy_total


def find_seam(img, energy_total):  # an array of H integers, for each row return the column of the seam.
    h = energy_total.shape[0]           # Height of energy matrix
    w = energy_total.shape[1]           # Width of energy matrix
    seam = numpy.zeros(shape=(h, w), dtype=float)
    numpy.copyto(seam, energy_total)
    for i in range(1, h):
        for j in range(1, w-1):
            if j == 1:
                seam[i, j] = seam[i, j] + min(seam[i - 1, j], seam[i - 1, j + 1])
            if j == w - 2:
                seam[i, j] = seam[i, j] + min(seam[i - 1, j - 1], seam[i - 1, j])
            else:
                seam[i, j] = seam[i, j] + min(seam[i - 1, j - 1], seam[i - 1, j], seam[i - 1, j + 1])

    val = inf
    index = -1
    for i in range(1, w - 1):
        if seam[h - 1, i] < val:
            val = seam[h - 1, i]
            index = i
    return val, index, seam


def plot_seam(img, index, seam):  # your own visualization of the seam, img, and energy func.
    h = img.shape[0]  # backtracking the matrix
    w = img.shape[1]
    path = numpy.zeros(shape=h, dtype=int)
    for i in range(h - 1, -1, -1):  # The h is the value of image, not energy
        img[i, index][0] = 255
        img[i, index][1] = 0
        img[i, index][2] = 0
        path[i] = index
        if i != 0:
            if index == 1:  # Excluding the result for first column, as it will cause everything to be 0
                if seam[i - 1, index + 1] < seam[i - 1, index]:
                    index += 1
            elif index == w - 2:  # Considering second last column, not comparing with last col since everything will be 0
                if seam[i - 1, index - 1] < seam[i - 1, index]:
                    index -= 1
            else:
                if seam[i - 1, index - 1] < seam[i - 1, index] and seam[i - 1, index - 1] < seam[i - 1, index + 1]:
                    index -= 1
                elif seam[i - 1, index + 1] < seam[i - 1, index] and seam[i - 1, index + 1] < seam[i - 1, index + 1]:
                    index += 1
    return img, path


def remove_seam(img, path):  # modify img in-place and returns a W-1 x H x 3 slice.
    h = img.shape[0]
    w = img.shape[1]
    resize_img = numpy.zeros(shape=(h, w - 1, 3))  # w-1 to remove one seam only, 3 refers to RGB
    for i in range(h - 1, -1, -1):
        b = img[i, :, :]            # Traversing and deleting row wise
        resize_img[i, :, :] = numpy.delete(b, path[i], axis=0)
    return resize_img


def main():
    """
    >>> img = imread('C:\Users\DELL\PycharmProjects\cc3\image.png')
    >>> img = img_as_float(img)
    >>> energy = dual_gradient_energy(img)
    >>> minVal,minIndex,sOfTJ=find_seam(img,energy)
    >>> img_modified, path = plot_seam(img, minIndex, sOfTJ)
    >>> print minVal
    0.488050766739
    """
    img = imread("C:\Users\DELL\PycharmProjects\cc3\image.png")
    img = img_as_float(img)
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]
    figure(1)
    gray()
    subplot(1, 4, 1)
    imshow(img)
    title("RGB")
    subplot(1, 4, 2)
    imshow(R)
    title("Red")
    subplot(1, 4, 3)
    imshow(G)
    title("Green")
    subplot(1, 4, 4)
    imshow(B)
    title("Blue")
    show()
    energy = dual_gradient_energy(img)
    figure(2)
    subplot(2, 1, 1)
    imshow(energy)
    title("Dual Energy Gradient")
    show()

    for i in range(50):
        energy = dual_gradient_energy(img)
        val, index, seam = find_seam(img, energy)
        img1, path = plot_seam(img, index, seam)
    figure(3)
    subplot(3, 2, 1)
    imshow(img1)
    title("Seams Plotted")
    img = imread('C:\Users\DELL\PycharmProjects\cc3\image.png')
    img = img_as_float(img)
    for i in range(50):
        energy = dual_gradient_energy(img)
        val, index, seam = find_seam(img, energy)
        img1, path = plot_seam(img, index, seam)
        img = remove_seam(img1, path)
    subplot(3, 2, 2)
    imshow(img)
    title("Seams Removed")
    show()


if __name__ == '__main__':
    main()
    import doctest
    doctest.testmod()
