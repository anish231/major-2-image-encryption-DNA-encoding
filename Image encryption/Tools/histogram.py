
from PIL import Image
from pylab import *
import matplotlib.pylab as plt2
import numpy as np
import matplotlib.pyplot as plt


def redhistogram(loc, output, name):
    im = array(Image.open(loc).convert('RGB'))
    # print(im)
    red = im[:, :, 2]
    print(red)
    im = (100.0 / 255) * im + 100
    # Fecthing red pixels

    plt2.axis('equal')
    plt2.axis('off')
    plt2.figure()
    # plt.hist(data, color="skyblue")
    plt2.hist(red.flatten(), 256, color="red")  # Designing the histogram
    # x, y = np.unique(im.flatten(), return_counts=True)
    # print(im.flatten())
    # plt2.plot(x, y)
    plt2.xlabel("Pixel Intensity")
    plt2.ylabel("No. of Pixels")
    plt2.title("Histogram")
    plt2.legend()
    plt2.savefig(output+name)
    # show()


def greenhistogram(loc, output, name):
    im = array(Image.open(loc).convert('RGB'))
    green = im[:, :, 1]
    im = 255 - im
    plt2.axis('equal')
    plt2.axis('off')
    plt2.figure()
    plt2.hist(green.flatten(), 256, color="green")
    plt2.xlabel("Pixel Intensity")
    plt2.ylabel("No. of Pixels")
    plt2.title("Histogram")
    plt2.legend()
    # plt2.show()
    plt2.savefig(output+name)


def bluehistogram(loc, output, name):
    im = array(Image.open(loc).convert('RGB'))
    blue = im[:, :, 0]
    im = 255.0 * (im / 255.0) ** 2
    plt2.axis('equal')
    plt2.axis('off')
    plt2.figure()
    plt2.hist(blue.flatten(), 256)
    plt2.xlabel("Pixel Intensity")
    plt2.ylabel("No. of Pixels")
    plt2.title("Histogram")
    plt2.legend()
    # plt2.show()
    plt2.savefig(output+name)


def rgbhistogram(loc, output):

    im = array(Image.open(loc).convert('RGB'))

    im2 = 255 - im  # invert image green
    im3 = (100.0 / 255) * im + 100
    im4 = 255.0 * (im / 255.0) ** 2
    plt2.axis('equal')
    plt2.axis('off')
    plt2.figure()
    plt2.hist(im2.flatten(), 128)
    plt2.hist(im3.flatten(), 128)
    plt2.hist(im4.flatten(), 128)
    plt2.savefig(output+"/rgbhisto.png")


def rgbhistogram2(loc, output):
    im = array(Image.open(loc).convert('RGB'))

    im2 = 255 - im  # invert image green
    im3 = (100.0 / 255) * im + 100
    im4 = 255.0 * (im / 255.0) ** 2
    plt2.axis('equal')
    plt2.axis('off')
    plt2.figure()
    plt2.hist(im2.flatten(), 128)
    plt2.hist(im3.flatten(), 128)
    plt2.hist(im4.flatten(), 128)
    plt2.savefig(output+"/rgbhisto2.png")


# im = array(Image.open('abc.png').convert('RGB'))
#
# im2 = 255 - im # invert image green
#
# im3 = (100.0/255) * im + 100
#
# im4 = 255.0 * (im/255.0)**2
# # create a new figure
# figure()
# # don't use colors
# #gray()
# # show contours with origin upper left corner
# #contour(im2, origin='image')
#
# axis('equal')
# axis('off')
# figure()
# hist(im2.flatten(),128)
# # hist(im3.flatten(),128)
# # hist(im.flatten(),128)
# # hist(im4.flatten(),128)
# # #
# show()
