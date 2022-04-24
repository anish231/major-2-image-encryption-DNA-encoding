import matplotlib.pyplot as plt2

from PIL import Image


def coplot_horizontal(loc, output, name):
    image = Image.open(loc)

    plt2.clf()

    pixels = image.load()
    list_of_pixels_of_x = []
    list_of_pixels_of_y = []

    width, height = image.size

    for pixel_coordinate_of_y in range(0, 50):
        for pixel_coordinate_of_x in range(0, 50):

            list_of_pixels_of_x.append(
                pixels[pixel_coordinate_of_x, pixel_coordinate_of_y][0])
            if pixel_coordinate_of_x+1 == width:
                list_of_pixels_of_x.pop()
                break
            else:
                list_of_pixels_of_y.append(
                    pixels[pixel_coordinate_of_x+1, pixel_coordinate_of_y][0])

    # plotting of values to a graph
    plt2.scatter(list_of_pixels_of_x, list_of_pixels_of_y,
                 label='Pixel', color='k', s=2, edgecolors='r')
    plt2.xlabel('Pixel value on location(x,y)')
    plt2.ylabel('Pixel value on location(x+1,y)')
    plt2.title("correlation coefficient graph")
    plt2.legend()
    plt2.savefig(output+name)


def coplot_vertical(loc):
    image = Image.open(loc)
    pixels = image.load()
    list_of_pixels_of_x = []
    list_of_pixels_of_y = []

    width, height = image.size

    for pixel_coordinate_of_y in range(0, 50):
        for pixel_coordinate_of_x in range(0, 50):

            list_of_pixels_of_x.append(
                pixels[pixel_coordinate_of_y, pixel_coordinate_of_x][0])
            if pixel_coordinate_of_y + 1 == height:
                list_of_pixels_of_y.pop()
                break
            else:

                list_of_pixels_of_y.append(
                    pixels[pixel_coordinate_of_y, pixel_coordinate_of_x+1][0])

    plt2.scatter(list_of_pixels_of_x, list_of_pixels_of_y,
                 label='Pixel', color='k', s=2, edgecolors='r')
    plt2.xlabel('Pixel value on location(x,y)')
    plt2.ylabel('Pixel value on location(x+1,y)')
    plt2.title("correlation coefficient graph")
    plt2.legend()
    plt2.show()
