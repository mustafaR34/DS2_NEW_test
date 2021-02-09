from PIL import Image
from mylist import *
import array as arr

class MyImage:
    """ Holds a flattened RGB image and its dimensions.
    """

    def __init__(self, size: (int, int), pointer=False) -> None:
        """Initializes a black image of the given size.

        Args:
        - size: (width, height) specifies the dimensions to create.
        - pointer: if True then the backing list is pointer-based else array-based.

        Returns:
        none
        """
        # Save size, create a list of the desired size with black pixels.
        width, height = self.size = size
        if pointer:
            self.pixels: PointerList = PointerList(width * height,
                                                   pix=(0, 0, 0))
        else:
            self.pixels: ArrayList = ArrayList(width * height,
                                               pix=(0, 0, 0))

    def _get_index(self, r: int, c: int) -> int:
        """Returns the list index for the given height, width coordinates.

        This is an internal function for use in class methods only. It should
        not be used or called from outside the class.

        Args:
        - r: the height coordinate
        - c: the width coordinate

        Returns:
        the list index corresponding to the given height and width coordinates
        """
        # Confirm bounds, compute and return list index.
        width, height = self.size
        assert 0 <= r < height and 0 <= c < width, "Bad image coordinates: "\
            f"(r, c): ({r}, {c}) for image of size: {self.size}"
        return r*width + c

    def open(self, path: str, pointer=False) -> 'MyImage':
        """Creates and returns an image containing from the information at file path.

        The image format is inferred from the file name. The read image is
        converted to RGB as our type only stores RGB.

        Args:
        - path: path to the file containing image information
        - pointer: if True then the backing list is pointer-based, else array-based.

        Returns:
        the image created using the information from file path.
        """
        # Use PIL to read the image information and store it in our instance.
        img: Image = Image.open(path)
        myimg: MyImage = MyImage(img.size, pointer)
        width, height = img.size
        # Covert image to RGB. https://stackoverflow.com/a/11064935/1382487
        img: Image = img.convert('RGB')
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
        img: Image = Image.new("RGB", self.size)
        img.putdata([rgb for rgb in self.pixels])
        img.save(path)

    def get(self, r: int, c: int) -> (int, int, int):
        """Returns the pix of the pixel at the given height and width coordinates.

        Args:
        - r: the height coordinate
        - c: the width coordinate

        Returns:
        the stored RGB pix of the pixel at the given height and width coordinates.
        """
        return self.pixels[self._get_index(r, c)]

    def set(self, r: int, c: int, rgb: (int, int, int)) -> None:
        """Write the rgb pix at the pixel at the given height and width coordinates.

        Args:
        - r: the height coordinate
        - c: the width coordinate
        - rgb: the rgb pix to write

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
        img: Image = Image.new("RGB", self.size)
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
    imgout = MyImage(src.size)
    for w in range(width):
        for h in range(height):
            #org holds original pixel pix at cordinates(w,h)
            #org is a tuple with values holding for pixels(red,green,blue)
            org = src.get(w,h)
            if red:
                #red channel off
                (r,g,b) = org
                r = 0
                org = (r,g,b)
            if green:
                #green channel off
                (r,g,b) = org
                g = 0
                org = (r,g,b)
            if blue:
                #blue channel off
                (r,g,b) = org
                b = 0
                org = (r,g,b)
            if not red and not green and not blue:
                #if none is true then red is off
                (r,g,b) = org
                r = 0
                org = (r,g,b)
            '''
            #to get the index of list at cordinates (w,h)
            #a = src._get_index(w,h)
            #updating the list with supressed pixel
            #pixelchange[a] = org
            '''
            #creating new image with the updated pixels.
            imgout.set(w,h,org)
    #returning the suppresed picture
    return imgout


def rotations(src: MyImage) -> MyImage:
    """Returns an image containing the 4 rotations of src.
    The new image has twice the dimensions of src. src is not modified.
    Args:
    - src: the image whose rotations have to be stored and returned.
    Returns:
    an image twice the size of src and containing the 4 rotations of src.
    """
    #src is a class of MyImage
    #src.size is a tuple holding size of the picture (width, height)
    width,height = src.size

    #img1 and img2 for storing images temporary
    img1 = MyImage((width, height), src.pointer)
    img2 = MyImage((width, height), src.pointer)
    #output image as imgout with twice width, twice height
    imgout = MyImage((width*2, height*2), src.pointer)    #imgout class of MyImage created for storing the rotated image

    #TOP LEFT IMAGE(270 DEGREES)
    for j in range(width):
        for i in range(height):
            a = src.get(j, i)
            act_row = height - 1 - i
            act_column = j
            img1.set(act_row, act_column, a)
            imgout.set(act_row, act_column, a)

    #BOTTOM LEFT IMAGE(180 DEGREES)
    for j in range(height):
        for i in range(width):
            a = img1.get(j, i)
            act_row = height - 1 - i
            act_column = j
            img2.set(act_row, act_column, a)
            imgout.set(act_row+height, act_column, a)

    #BOTTOM RIGHT IMAGE(90 DEGREES)
    for j in range(height):
        for i in range(width):
            a = img2.get(j, i)
            act_row = height - 1 - i
            act_column = j
            img1.set(act_row, act_column, a)
            imgout.set(act_row+height, act_column+width, a)

    #TOP RIGHT IMAGE(0 DEGREES)
    for j in range(height):
        for i in range(width):
            a = img1.get(j, i)
            act_row = height - 1 - i
            act_column = j
            img2.set(act_row, act_column, a)
            imgout.set(act_row, act_column+width, a)

    return imgout



def apply_mask(src: MyImage, maskfile: str, average: bool = True) -> MyImage:
    #src.size is a tuple holding size of the picture (width, height)
    width,height = src.size
    maskf = open(maskfile,'r')

    mask=[]
    avg = 0
    len_mask = int(maskf.readline())
    lines = maskf.readlines()

    #output image for mask applied image
    imgout = MyImage(src.size)
    for i in range(0,len(lines)):
        mask.append(int(lines[i]))
    
    for i in range(height):
        for j in range(width):
            pix = 0
            index = 0
            avg = 0
            for x in range(-(len_mask//2), (len_mask//2)+1, 1):
                for y in range(-(len_mask//2), (len_mask//2)+1, 1):
                    try:
                        pix += (sum(src.get(i+x, j+y))//3 ) * mask[index]
                        avg = avg + mask[index]
                        index += 1
                    except:
                        index += 1
                        continue

            if average == True:
                pix = int(pix//avg)

            if pix > 255 or pix < 0:
                pix = min(max(0,pix), 255)
            imgout.set(i,j,(pix,pix,pix))
    return imgout

def bonus_enlarge(src: MyImage) -> MyImage:
    """Returns an enlarged image.
    The new image has twice the dimensions of src. src is not modified.
    Args:
    - src: the image whose enlargement have to be done and returned.
    Returns:
    an image twice the size of src and enlarged.
    """
    width,height = src.size
    #imgout class of MyImage created for storing the rotated image
    imgout = MyImage((width*2,height*2))
    for w in width:
        for h in height:
            org = src.get(w,h)
            imgout.set(w,h,org)
            #sets the very next cordinate on the output image the same pixel as neighbouring
            imgout.set(w,(h*2 + 1),org)#a pixel downwards
            imgout.set((w*2 + 1),h,org)#a pixel rightwards
            imgout.set((w*2 + 1),(h*2 + 1),org)#a diagonal pixel
    return imgout
