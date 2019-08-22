from PIL import Image
import numpy as np
import os
import sys


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


def adaptive_median_filter(image, size, window):

    xlength, ylength = size

    print('Image length in X direction: ', xlength)
    print('Image length in Y direction: ', ylength)

    """create 2-D image array and initialize window"""
    image_array = np.reshape(np.array(image), (ylength, xlength))

    pixel_count = 0

    # loop over image with specified window W
    for y in range(0, ylength):
        for x in range(0, xlength):
            window = min_window
            while (window <= max_window):
                """Creating and populating window"""
                filter_window, target_vector, vlength = create_populate_window(
                    x, y, window, image_array)

                """calculating the median for the window"""
                Zmin, Zmed, Zmax = calc_median(target_vector, vlength)
                A1 = int(Zmed) - int(Zmin)
                A2 = int(Zmed) - int(Zmax)
                if (A1 > 0 and A2 < 0):
                    B1 = int(image_array[y, x]) - int(Zmin)
                    B2 = int(image_array[y, x]) - int(Zmax)
                    if not(B1 > 0 and B2 < 0):
                        image_array[y, x] = Zmed
                        pixel_count += 1
                        break
                    else:
                        break
                else:
                    window += 1

    print("exit")
    return np.reshape(image_array, (xlength*ylength,)).tolist()


def main(argv):

    global max_window, min_window

    min_window = 1
    max_window = 4
    window = 1

    filenames = ['gray_images.png']
    for filename in filenames:
        infile = open(filename, "rb")
        inp_image = Image.open(infile)
        inp_image.show()
        print("Original image mode: ", inp_image.mode)
        # change image mode to "L" changes to a black and while image
        inp_image = inp_image.convert("L")
        inp_image.show()
        # print to console the format, size and mode of the opened image respectively
        print("Input image format: ", inp_image.format)
        print("Input image size: ", inp_image.size)
        print("Working image mode: ", inp_image.mode)

        # Convert the PIL image object to a python sequence (list)
        input_sequence = list(inp_image.getdata())

        # edge detection processing part
        output_sequence = adaptive_median_filter(
            input_sequence, inp_image.size, window)

        if (input_sequence == output_sequence):
            print("same")
        else:
            print("different")

        # spiltting filename and file extension
        # we need filename not the opened file/image so used filename
        file, ext = os.path.splitext(filename)

        outfile = "new_adap_gray_" + file + ext
        print(outfile)

        try:
            output_image = Image.new(inp_image.mode, inp_image.size, None)
            output_image.putdata(output_sequence)
            output_image.save(outfile, inp_image.format)
        except(IOError):
            print("Output file error:")

        infile.close()


if __name__ == "__main__":
    main(sys.argv)
