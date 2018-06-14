from PIL import Image
import numpy

def generate_matrix(color):
    """
    Generates a transformation matrix for the specified color.
    Inputs:
        color: string with exactly one of the following values:
               'red', 'blue', 'green', or 'none'
    Returns:
        matrix: a transformation matrix corresponding to
                deficiency in that color
    """
    # You do not need to understand this function.
    if color == 'red':
        c = [[.567, .433, 0], [.558, .442, 0], [0, .242, .758]]
    elif color == 'green':
        c = [[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.142, 0.858]]
    elif color == 'blue':
        c = [[.95, 0.05, 0], [0, 0.433, 0.567], [0, 0.475, .525]]
    elif color == 'none':
        c = [[1, 0., 0], [0, 1, 0.], [0, 0., 1]]
    return c


def matrix_multiply(m1, m2):
    """
    Multiplies the input matrices.
    Inputs:
        m1,m2: input matrices
    Returns:
        result: the matrix product of m1 and m2
        in a list of floats
    """

    product = numpy.matmul(m1, m2)
    if type(product) == numpy.int64:
        return float(product)
    else:
        result = list(product)
        return result


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
    RGB_mode = im.convert('L')
    # Getting the size of the image to iterate over it
    image_shape = im.size
    # Creating an empty array for the pixel values of the image
    RGB_image = []
    # Iterate over the image pixels and get the RGB values of them and append them to the RGB_image
    for x in range(image_shape[0]):
        for y in range(image_shape[1]):
            RGB_image.append(RGB_mode.getpixel((x, y)))
    return RGB_image


def convert_pixels_to_image(pixels, size):
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
    img = Image.new("RGB", size, "white")
    # Loading all of its pixel values in the new_pixels
    new_pixels = img.load()
    # Setting a counter to go over the pixel values in the pixels input
    counter = 0
    # Iterating over the size of the image and changing the pixel values
    for x in range(size[0]):
        for y in range(size[1]):
            new_pixels[x, y] = (pixels[counter])
            counter += 1
    return img

def apply_filter(pixels, color):
    """
    pixels: a list of pixels in RGB form, such as [(0,0,0),(255,255,255),(38,29,58)...]
    color: 'red', 'blue', 'green', or 'none', must be a string representing the color
    deficiency that is being simulated.
    returns: list of pixels in same format as earlier functions,
    transformed by matrix multiplication
    """
    # Creating the transform matrix
    transformation_matrix = generate_matrix(color)
    # Iterating over the pixels and multiplying each pixel by the transformation matrix
    for i in range(len(pixels)):
        pixels[i] = matrix_multiply(transformation_matrix, pixels[i])
        pixels[i] = [int(x) for x in pixels[i]]
        pixels[i] = tuple(pixels[i])
    return pixels

# original_im = Image.open('test2.png')
pixel_vals = convert_image_to_pixels('hidden1.bmp')
print(pixel_vals[:100])

# new_pixs = apply_filter(pixel_vals, 'red')
# print(new_pixs[0:5])
# made_image = convert_pixels_to_image(new_pixs, original_im.size)
# made_image.show()