# Problem Set 5
# Name: Elaheh Ahmadi
# Collaborators: N/A
# Time: 10h

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
        c = [[.567, .433, 0],[.558, .442, 0],[0, .242, .758]]
    elif color == 'green':
        c = [[0.625,0.375, 0],[ 0.7,0.3, 0],[0, 0.142,0.858]]
    elif color == 'blue':
        c = [[.95, 0.05, 0],[0, 0.433, 0.567],[0, 0.475, .525]]
    elif color == 'none':
        c = [[1, 0., 0],[0, 1, 0.],[0, 0., 1]]
    return c

def matrix_multiply(m1,m2):
    """
    Multiplies the input matrices.  
    Inputs:
        m1,m2: input matrices
    Returns: 
        result: the matrix product of m1 and m2
        in a list of floats 
    """ 
    
    product = numpy.matmul(m1,m2)
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
        # Casting the values to int
        pixels[i] = [int(x) for x in pixels[i]]
        # Casting the RGB values from a list to tuple
        pixels[i] = tuple(pixels[i])
    return pixels


def reveal_binary_image(filename):
    """
    Extracts the hidden image in the least significant bit
    of each pixel in the specified image.
    Inputs:
       filename: string, input file to be processed
    returns:
       result: an Image object containing the hidden image
    """
    # Opening the image
    img = Image.open(filename)
    # Getting the size of the image
    size = img.size
    # Converting image to gray scale
    gray_scale_im = img.convert('L')
    # Loading the pixels
    pixels = gray_scale_im.load()
    # Creating a new plane image that will be the secret image
    secret_im = Image.new('1',size,'white')
    # Loading the secret image pixels
    secret_pixels = secret_im.load()
    # Iterating over the pixels and taking the lsb and putting it for the pixel value of the secret image
    for x in range(size[0]):
        for y in range(size[1]):
            secret_pixels[x, y] = pixels[x, y] % 2
    return secret_im


def reveal_RGB_image(filename):
    """
    Extracts the hidden image in the 2 least significant bits
    of each pixel in the specified color image.
    Inputs:
        filename: string, input RGB file to be processed
    Returns:
        result: an Image object containing the hidden image
    """
    # Opening the image
    img = Image.open(filename)
    # Getting the size of the image
    size = img.size
    # Converting image to gray scale
    img = img.convert('RGB')
    # Loading the pixels
    pixels = img.load()
    # Creating a new plane image that will be the secret image
    secret_im = Image.new('RGB', size, 'white')
    # Loading the secret image pixels
    secret_pixels = secret_im.load()
    # Iterate over the the pixels of the real image and then get the two LSB of each color of the photo and then
    # rescale them to RGB
    for x in range(size[0]):
        for y in range(size[1]):
            red_val = pixels[x, y][0] % 2 + ((pixels[x, y][0]//2) % 2)*2
            green_val = pixels[x, y][1] % 2 + ((pixels[x, y][1]//2) % 2) * 2
            blue_val = pixels[x, y][2] % 2 + ((pixels[x, y][2]//2) % 2) * 2
            secret_pixels[x,y] = (red_val*85, green_val*85, blue_val*85)
    return secret_im



def main():
    # pass

    # UNCOMMENT the following 7 lines to test part 1
    
    pixels = convert_image_to_pixels('test2.png')
    image = apply_filter(pixels,'none')
    im = convert_pixels_to_image(image, (225,224))
    im.show()
    new_image = apply_filter(pixels,'red')
    im2 = convert_pixels_to_image(new_image,(225,224))
    im2.show()
    img3 = reveal_binary_image('hidden1.bmp')
    img3.show()
    img1 = reveal_RGB_image('hidden2.bmp')
    img1.show()
    
    # No tests for part 2. Try to find the secret images! 

if __name__ == '__main__':
    main()


