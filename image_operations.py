from PIL import Image
from APL import *
from myimage import MyImage
import array as arr

def remove_channel(src: MyImage, red: bool = False, green: bool = False,
                   blue: bool = False) -> MyImage:
    """Returns a copy of src in which the indicated channels are suppressed.

    Suppresses the red channel if no channel is indicated. src is not modified.

    Args:
    - src: the image whose copy the indicated channels have to be suppressed.
    - red: suppress the red channel if this is True.
    - green: suppress the green channel if this is True.
    - blue: suppress the blue channel if this is True.

    Returns:
    a copy of src with the indicated channels suppressed.
    """

    width, height = src.size

    # img will store the resultant image in this case
    img = src

    for j in range(height):
        for i in range(width):
            temp_tuple = img.get(j, i)

            # red color suppressed if red is true
            if red:
                temp_tuple = (0,) + (temp_tuple[1],) + (temp_tuple[2],)

            # green color suppressed if green is true
            if green:
                temp_tuple = (temp_tuple[0],) + (0,) + (temp_tuple[2],)

            # blue color suppressed if blue is true
            if blue:
                temp_tuple = (temp_tuple[0],) + (temp_tuple[1],) + (0,)

            # default condition implemented (red channel suppressed)
            if red == False and blue == False and green == False:
                temp_tuple = (0,) + (temp_tuple[1],) + (temp_tuple[2],)

            img.set(j, i, temp_tuple)

    return img


def rotations(src: MyImage) -> MyImage:
    """Returns an image containing the 4 rotations of src.

    The new image has twice the dimensions of src. src is not modified.

    Args:
    - src: the image whose rotations have to be stored and returned.

    Returns:
    an image twice the size of src and containing the 4 rotations of src.
    """

    width, height = src.size

    img = src

    # two temporary images instantiated for use in between rotations
    temp_img = MyImage((width, height), src.pointer)
    temp_img2 = MyImage((width, height), src.pointer)

    # new image instantiated that will store the resultant image
    result_img = MyImage((width*2, height*2), src.pointer)

    # rotate once (top left image)
    for j in range(height):
        for i in range(width):
            temp_tuple = img.get(j, i)

            new_row = height - 1 - i
            new_column = j

            temp_img.set(new_row, new_column, temp_tuple)
            result_img.set(new_row, new_column, temp_tuple)

    # rotate twice (bottom left image)
    for j in range(height):
        for i in range(width):
            temp_tuple = temp_img.get(j, i)

            new_row = height - 1 - i
            new_column = j

            temp_img2.set(new_row, new_column, temp_tuple)
            result_img.set(new_row+height, new_column, temp_tuple)

    # rotate thrice (bottom right image)
    for j in range(height):
        for i in range(width):
            temp_tuple = temp_img2.get(j, i)

            new_row = height - 1 - i
            new_column = j

            temp_img.set(new_row, new_column, temp_tuple)
            result_img.set(new_row+height, new_column+width, temp_tuple)

    # rotate fourth time (top right image or original image)
    for j in range(height):
        for i in range(width):
            temp_tuple = temp_img.get(j, i)

            new_row = height - 1 - i
            new_column = j

            temp_img2.set(new_row, new_column, temp_tuple)
            result_img.set(new_row, new_column+width, temp_tuple)

    return result_img


def apply_mask(src: MyImage, maskfile: str, average: bool = True) -> MyImage:
    
    newImage = MyImage(src.size)
    column,row=src.size
    mask=open(maskfile,'r')

    masking_matrix=[]
    average_denominator=0
    mask_size=int(mask.readline())
    
    mask_lines=mask.readlines()
    for i in range(0,len(mask_lines)):
        masking_matrix.append(int(mask_lines[i]))
    
    for i in range(row):
        for j in range(column):
            value = 0
            mask_index = 0
            average_denominator = 0
            for x in range(-(mask_size//2), (mask_size//2)+1, 1):
                for y in range(-(mask_size//2), (mask_size//2)+1, 1):
                    try:
                        value += (sum(src.get(i+x, j+y))//3 ) * masking_matrix[mask_index]
                        average_denominator = average_denominator + masking_matrix[mask_index]
                        mask_index += 1
                    except:
                        mask_index += 1
                        continue

            if average==True:
                value=int(value//average_denominator)

            if value < 0 or value > 255:
                value=min(max(0,value), 255)
            newImage.set(i,j,(value,value,value))


    # newImage.show()
    # newImage.save('give path file here')
    return newImage


#img=MyImage((100,100))
#myimg = MyImage.open('hu-logo.png')
#rotations(myimg)
# remove_channel(myimg,True,False,False)
#apply_mask(myimg,'mask-blur-more.txt')
