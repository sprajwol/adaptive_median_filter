from PIL import Image
from PIL.Image import core as _imaging
import os
import sys
import time
import numpy as np


def create_populate_window(x, y, window, image_array):
    ax = x
    ay = y

    W = 2 * window + 1
    vlength = W * W

    """Creating the window"""
    filter_window = np.array(np.zeros((W, W)))
    target_vector = np.array(np.zeros(vlength))

    image_array = np.pad(image_array, window, mode='constant')

    """populate window, sort, find median"""
    filter_window = image_array[ay:ay+(window*2)+1, ax:ax+(window*2)+1]
    target_vector = np.reshape(filter_window, ((vlength),))

    return filter_window, target_vector, vlength


def calc_median(target_array, array_length):
    sorted_array = np.sort(target_array)
    Zmed = sorted_array[int(array_length/2)]
    Zmin = sorted_array[0]
    Zmax = sorted_array[int(array_length-1)]
    return Zmin, Zmed, Zmax


def adaptive_median_filter(image_array, size, window):
    xlength, ylength = size
    print(xlength, ylength)
    print("1")

    # loop over image with specified window W for TODO:red stream
    for y in range(0, ylength):
        for x in range(0, xlength):
            window = min_window

            while (window <= max_window):
                """Creating and populating window"""
                filter_window, target_vector, vlength = create_populate_window(
                    x, y, window, image_array)

                """calculating the median for the window"""
                Zmin, Zmed, Zmax = calc_median(target_vector, vlength)
                # print("Zmin, Zmed, Zmax:", Zmin, Zmed, Zmax)
                A1 = int(Zmed) - int(Zmin)
                # print("A1", A1)
                A2 = int(Zmed) - int(Zmax)
                # print("A2", A2)
                if (A1 > 0 and A2 < 0):
                    B1 = int(image_array[y, x]) - int(Zmin)
                    B2 = int(image_array[y, x]) - int(Zmax)
                    if not(B1 > 0 and B2 < 0):
                        image_array[y, x] = Zmed
                        break
                    else:
                        break
                else:
                    # print("Window increased")
                    window += 1

    return np.reshape(image_array, (xlength*ylength,)).tolist()


def main(argv):

    global max_window, min_window
    min_window = 1
    max_window = 4
    window = 1

    filenames = ['rgb_images.jpg']
    for filename in filenames:
        infile = open(filename, "rb")
        inp_image = Image.open(infile)

        print("Original image mode: ", inp_image.mode)
        print("Original image size: ", inp_image.size)
        inp_image.show()
        x, y = inp_image.size

        # Convert the PIL image object to a python sequence (list)
        input_sequence = inp_image.getdata()
        R, G, B = np.array(input_sequence.split())
        R = np.reshape(np.array(R), (y, x))
        G = np.reshape(np.array(G), (y, x))
        B = np.reshape(np.array(B), (y, x))

        OR = adaptive_median_filter(
            R, inp_image.size, window)
        OG = adaptive_median_filter(
            G, inp_image.size, window)
        OB = adaptive_median_filter(
            B, inp_image.size, window)

        try:
            OP_R = Image.new('L', inp_image.size, None)
            OP_R.putdata(OR)
            OP_R.show()
            print(OP_R)

            OP_G = Image.new('L', inp_image.size, None)
            OP_G.putdata(OG)
            OP_G.show()

            OP_B = Image.new('L', inp_image.size, None)
            OP_B.putdata(OB)
            OP_B.show()

            file, ext = os.path.splitext(filename)
            outfile = "new_adap_rgb_" + file + ext
            print(outfile)
            # quit()
            output_image = Image.merge('RGB', (OP_R, OP_G, OP_B))
            output_image.save(outfile, inp_image.format)
            print(output_image)
        except(IOError):
            print("Output file error:")

        quit()
        # img = Image.merge("RGB", rgb).tobytes()

        file, ext = os.path.splitext(filename)

        outfile = "new_adap_" + file + ext
        print(outfile)

        try:
            output_image = Image.new(inp_image.mode, inp_image.size, None)
            output_image.putdata()
            output_image.save(outfile, inp_image.format)
        except(IOError):
            print("Output file error:")

        infile.close()


if __name__ == "__main__":
    main(sys.argv)
