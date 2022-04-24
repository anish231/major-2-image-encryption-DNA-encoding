
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
    #im = (100.0 / 255) * im + 100
    # Fecthing red pixels

    plt2.axis('equal')       # square graph
    plt2.axis('off')         # makes axis invisible
    plt2.figure()
    # plt.hist(data, color="skyblue")
    plt2.hist(red.flatten(), 256, color="red")  # Designing the histogram
    # x, y = np.unique(im.flatten(), return_counts=True)
    # print(im.flatten())
    # plt2.plot(x, y)
    plt2.xlabel("Pixel Intensity")
    plt2.ylabel("No. of Pixels")
    plt2.title("Histogram")
    #plt2.legend()
    plt2.savefig(output+name)
    # show()


def greenhistogram(loc, output, name):
    im = array(Image.open(loc).convert('RGB'))
    green = im[:, :, 1]
    #im = 255 - im
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
    #im = 255.0 * (im / 255.0) ** 2
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


