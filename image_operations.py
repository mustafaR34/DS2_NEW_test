from PIL import Image
from APL import *
import array as arr

class MyImage:
    """ Holds a flattened RGB image and its dimensions.
    """
    def __init__(self, size: (int, int), pointer=False) -> None:
        """Initializes a black image of the given size.
        Args:
        - size: (width, height) specifies the dimensions to create.
        Returns:
        none
        """
        self.pointer = pointer
        width, height = self.size = size
        if pointer:
            self.pixels: PointerList = PointerList(
                width * height, value=(0, 0, 0))
        else:
            self.pixels: ArrayList = ArrayList(width * height, value=(0, 0, 0))
    def _get_index(self, r: int, c: int) -> int:
        """Returns the list index for the given row, column coordinates.
        This is an internal function for use in class methods only. It should
        not be used or called from outside the class.
        Args:
        - r: the row coordinate
        - c: the column coordinate
        Returns:
        the list index corresponding to the given row and column coordinates
        """
        # Confirm bounds, compute and return list index.
        width, height = self.size
        assert 0 <= r < height and 0 <= c < width, "Bad image coordinates: "\
            f"(r, c): ({r}, {c}) for image of size: {self.size}"
        return r*width + c
    def open(path, pointer=False):
        """Creates and returns an image containing from the information at file path.
        The image format is inferred from the file name. The read image is
        converted to RGB as our type only stores RGB.
        Args:
        - path: path to the file containing image information
        Returns:
        the image created using the information from file path.
        """
        # Use PIL to read the image information and store it in our instance.
        img: PIL.Image = Image.open(path)
        myimg: MyImage = MyImage(img.size, pointer)
        width, height = img.size
        # Covert image to RGB. https://stackoverflow.com/a/11064935/1382487
        img: PIL.Image = img.convert('RGB')
        # Get list of pixel values (https://stackoverflow.com/a/1109747/1382487),
        # copy to our instance and return it.
        for i, rgb in enumerate(list(img.getdata())):
            myimg.pixels.set(i, rgb)
        return myimg
    def save(self, path: str) -> None:
        """Saves the image to the given file path.
        The image format is inferred from the file name.
        Args:
        - path: the image has to be saved here.
        Returns:
        none
        """
        # Use PIL to write the image.
        img: PIL.Image = Image.new("RGB", self.size)
        img.putdata([rgb for rgb in self.pixels])
        img.save(path)
    def get(self, r: int, c: int) -> (int, int, int):
        """Returns the value of the pixel at the given row and column coordinates.
        Args:
        - r: the row coordinate
        - c: the column coordinate
        Returns:
        the stored RGB value of the pixel at the given row and column coordinates.
        """
        return self.pixels[self._get_index(r, c)]
    def set(self, r: int, c: int, rgb: (int, int, int)) -> None:
        """Write the rgb value at the pixel at the given row and column coordinates.
        Args:
        - r: the row coordinate
        - c: the column coordinate
        - rgb: the rgb value to write
        Returns:
        none
        """
        self.pixels[self._get_index(r, c)] = rgb
    def show(self) -> None:
        """Display the image in a GUI window.
        Args:
        Returns:
        none
        """
        # Use PIL to display the image.
        img: PIL.Image = Image.new("RGB", self.size)
        img.putdata([rgb for rgb in self.pixels])
        img.show()

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
    WT, HT = src.size

    # photo will store the resultant image in this case
    photo = src

    for j in range(HT):
        for i in range(WT):
            temp_t_tuple = photo.get(j, i)

            # red color suppressed if red is true
            if red:
                temp_t_tuple = (0,) + (temp_t_tuple[1],) + (temp_t_tuple[2],)

            # green color suppressed if green is true
            if green:
                temp_t_tuple = (temp_t_tuple[0],) + (0,) + (temp_t_tuple[2],)

            # blue color suppressed if blue is true
            if blue:
                temp_t_tuple = (temp_t_tuple[0],) + (temp_t_tuple[1],) + (0,)

            # default condition implemented (red channel suppressed)
            if red == False and blue == False and green == False:
                temp_t_tuple = (0,) + (temp_t_tuple[1],) + (temp_t_tuple[2],)

            photo.set(j, i, temp_t_tuple)

    return photo     


# def remove_channel(src: MyImage, red: bool = False, green: bool = False,
#                    blue: bool = False) -> MyImage:
#     """Returns a copy of src in which the indicated channels are suppressed.
#     Suppresses the red channel if no channel is indicated. src is not modified.
#     Args:
#     - src: the image whose copy the indicated channels have to be suppressed.
#     - red: suppress the red channel if this is True.
#     - green: suppress the green channel if this is True.
#     - blue: suppress the blue channel if this is True.
#     Returns:
#     a copy of src with the indicated channels suppressed.
#     """
#     width, height = src.size
#     # img will store the resultant image in this case
#     img = src
#     for j in range(height):
#         for i in range(width):
#             temp_tuple = img.get(j, i)
#             # red color suppressed if red is true
#             if red:
#                 temp_tuple = (0,) + (temp_tuple[1],) + (temp_tuple[2],)
#             # green color suppressed if green is true
#             if green:
#                 temp_tuple = (temp_tuple[0],) + (0,) + (temp_tuple[2],)
#             # blue color suppressed if blue is true
#             if blue:
#                 temp_tuple = (temp_tuple[0],) + (temp_tuple[1],) + (0,)
#             # default condition implemented (red channel suppressed)
#             if red == False and blue == False and green == False:
#                 temp_tuple = (0,) + (temp_tuple[1],) + (temp_tuple[2],)
#             img.set(j, i, temp_tuple)
#     return img

def rotations(src: MyImage) -> MyImage:
    """Returns an image containing the 4 rotations of src.

    The new image has twice the dimensions of src. src is not modified.

    Args:
    - src: the image whose rotations have to be stored and returned.

    Returns:
    an image twice the size of src and containing the 4 rotations of src.
    """
    WT, HT = src.size

    photo = src

    # two temporary images instantiated for use in between rotations
    temp_img = MyImage((WT, HT), src.pointer)
    temp_img2 = MyImage((WT, HT), src.pointer)

    # new image instantiated that will store the resultant image
    result_photo = MyImage((WT*2, HT*2), src.pointer)

    # rotate once (top left image)
    for j in range(HT):
        for i in range(WT):
            temp_t_tuple = photo.get(j, i)

            x_axis = HT - 1 - i
            y_axis = j

            temp_img.set(x_axis, y_axis, temp_t_tuple)
            result_photo.set(x_axis, y_axis, temp_t_tuple)

    # rotate twice (bottom left image)
    for j in range(HT):
        for i in range(WT):
            temp_t_tuple = temp_img.get(j, i)

            x_axis = HT - 1 - i
            y_axis = j

            temp_img2.set(x_axis, y_axis, temp_t_tuple)
            result_photo.set(x_axis+HT, y_axis, temp_t_tuple)

    # rotate thrice (bottom right image)
    for j in range(HT):
        for i in range(WT):
            temp_t_tuple = temp_img2.get(j, i)

            x_axis = HT - 1 - i
            y_axis = j

            temp_img.set(x_axis, y_axis, temp_t_tuple)
            result_photo.set(x_axis+HT, y_axis+WT, temp_t_tuple)

    # rotate fourth time (top right image or original image)
    for j in range(HT):
        for i in range(WT):
            temp_t_tuple = temp_img.get(j, i)

            x_axis = HT - 1 - i
            y_axis = j

            temp_img2.set(x_axis, y_axis, temp_t_tuple)
            result_photo.set(x_axis, y_axis+WT, temp_t_tuple)

    return result_photo

# def rotations(src: MyImage) -> MyImage:
#     """Returns an image containing the 4 rotations of src.
#     The new image has twice the dimensions of src. src is not modified.
#     Args:
#     - src: the image whose rotations have to be stored and returned.
#     Returns:
#     an image twice the size of src and containing the 4 rotations of src.
#     """
#     width, height = src.size
#     img = src
#     # two temporary images instantiated for use in between rotations
#     temp_img = MyImage((width, height), src.pointer)
#     temp_img2 = MyImage((width, height), src.pointer)
#     # new image instantiated that will store the resultant image
#     result_img = MyImage((width*2, height*2), src.pointer)
#     # rotate once (top left image)
#     for j in range(height):
#         for i in range(width):
#             temp_tuple = img.get(j, i)
#             new_row = height - 1 - i
#             new_column = j
#             temp_img.set(new_row, new_column, temp_tuple)
#             result_img.set(new_row, new_column, temp_tuple)
#     # rotate twice (bottom left image)
#     for j in range(height):
#         for i in range(width):
#             temp_tuple = temp_img.get(j, i)
#             new_row = height - 1 - i
#             new_column = j
#             temp_img2.set(new_row, new_column, temp_tuple)
#             result_img.set(new_row+height, new_column, temp_tuple)
#     # rotate thrice (bottom right image)
#     for j in range(height):
#         for i in range(width):
#             temp_tuple = temp_img2.get(j, i)
#             new_row = height - 1 - i
#             new_column = j
#             temp_img.set(new_row, new_column, temp_tuple)
#             result_img.set(new_row+height, new_column+width, temp_tuple)
#     # rotate fourth time (top right image or original image)
#     for j in range(height):
#         for i in range(width):
#             temp_tuple = temp_img.get(j, i)
#             new_row = height - 1 - i
#             new_column = j
#             temp_img2.set(new_row, new_column, temp_tuple)
#             result_img.set(new_row, new_column+width, temp_tuple)
#     return result_img

def apply_mask(src: MyImage, maskfile: str, average: bool = True) -> MyImage:
    
    newImage = MyImage(src.size)
    x_axis,y_axis=src.size
    mask=open(maskfile,'r')
    matrix=[]
    denominator=0
    mask_size=int(mask.readline())
    
    mask_lines=mask.readlines()
    for i in range(0,len(mask_lines)):
        matrix.append(int(mask_lines[i]))
    
    for i in range(y_axis):
        for j in range(x_axis):
            number = 0
            index_mask = 0
            denominator = 0
            for x in range(-(mask_size//2), (mask_size//2)+1, 1):
                for y in range(-(mask_size//2), (mask_size//2)+1, 1):
                    try:
                        number += (sum(src.get(i+x, j+y))//3 ) * matrix[index_mask]
                        denominator = denominator + matrix[index_mask]
                        index_mask += 1
                    except:
                        index_mask += 1
                        continue
            if average==True:
                number=int(number//denominator)
            if number < 0 or number > 255:
                number=min(max(0,number), 255)
            newImage.set(i,j,(number,number,number))

    return newImage

# def apply_mask(src: MyImage, maskfile: str, average: bool = True) -> MyImage:
    
#     newImage = MyImage(src.size)
#     column,row=src.size
#     mask=open(maskfile,'r')
#     masking_matrix=[]
#     average_denominator=0
#     mask_size=int(mask.readline())
    
#     mask_lines=mask.readlines()
#     for i in range(0,len(mask_lines)):
#         masking_matrix.append(int(mask_lines[i]))
    
#     for i in range(row):
#         for j in range(column):
#             value = 0
#             mask_index = 0
#             average_denominator = 0
#             for x in range(-(mask_size//2), (mask_size//2)+1, 1):
#                 for y in range(-(mask_size//2), (mask_size//2)+1, 1):
#                     try:
#                         value += (sum(src.get(i+x, j+y))//3 ) * masking_matrix[mask_index]
#                         average_denominator = average_denominator + masking_matrix[mask_index]
#                         mask_index += 1
#                     except:
#                         mask_index += 1
#                         continue
#             if average==True:
#                 value=int(value//average_denominator)
#             if value < 0 or value > 255:
#                 value=min(max(0,value), 255)
#             newImage.set(i,j,(value,value,value))
#     # newImage.show()
#     # newImage.save('give path file here')
#     return newImage
# #img=MyImage((100,100))
# #myimg = MyImage.open('hu-logo.png')
# #rotations(myimg)
# # remove_channel(myimg,True,False,False)
# #apply_mask(myimg,'mask-blur-more.txt')
