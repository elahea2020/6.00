from PIL import Image


def convert_pixels_to_image(pixels,size):
    """
    Creates an Image object from a given set of RGB tuples.

    Inputs:
        pixels: a list of pixels such as the output of
                convert_image_to_pixels.
        size: a tuple of (width,height) representing
              the dimensions of the desired image. Assume
              that size is a valid input such that
              size[0] * size[1] == len(pixels).
    returns:
        img: Image object made from list of pixels
    """
    # Creating a new image
    img = Image.new('RGB', size, "white")
    # Loading all of its pixel values in the new_pixels
    new_pixels = img.load()
    # Setting a counter to go over the pixel values in the pixels input
    counter = 0
    # Iterating over the size of the image and changing the pixel values
    for x in range(size[0]):
        for y in range(size[1]):
            new_pixels[x, y] = pixels[counter]
            counter += 1
    return img

def convert_image_to_pixels(image):
    """
    Takes an image (must be inputted as a string
    with proper file attachment ex: .jpg, .png)
    and converts to a list of tuples representing pixels.
    Each pixel is a tuple containing (R,G,B) values.

    Returns the list of tuples.

    Inputs:
        image: string representing an image file, such as 'lenna.jpg'
        returns: list of pixel values in form (R,G,B) such as
                 [(0,0,0),(255,255,255),(38,29,58)...]
    """
    # Opening the image
    im = Image.open(image)
    # Converting the image to the RGB mode
    RGB_mode = im.convert('RGB')
    # Getting the size of the image to iterate over it
    image_shape = im.size
    # Creating an empty array for the pixel values of the image
    RGB_image = []
    # Iterate over the image pixels and get the RGB values of them and append them to the RGB_image
    for x in range(image_shape[0]):
        for y in range(image_shape[1]):
            RGB_image.append(RGB_mode.getpixel((x, y)))
    return RGB_image


def reveal_RGB_image(filename):
    """
    Extracts the hidden image in the 2 least significant bits
    of each pixel in the specified color image.
    Inputs:
        filename: string, input RGB file to be processed
    Returns:
        result: an Image object containing the hidden image
    """
    temp = [0, 0, 0]
    new_pixels = []
    img = Image.open(filename)
    size = img.size
    pixels = convert_image_to_pixels(filename)
    for i in range(0, len(pixels)):
        for j in range(0, 3):
            tuple_i = pixels[i]  # gets every tuple of 3 elements
            el = tuple_i[j] % 4
            if el == 1:
                el = 85
            elif el == 2:
                el = 170
            elif el == 3:
                el = 255
            temp[j] = el
        yo = tuple(temp)

        new_pixels.append(yo)  # converts list into tuple

    im = Image.new("L", size)  # creates new image
    # im.putdata(new_pixels)  # adds right color for pixels
    new_image = convert_pixels_to_image(new_pixels,size)
    new_image.show()
    # im.save("C:/Users/Julia/Downloads/PS5","bmp")

reveal_RGB_image("hidden2.bmp")