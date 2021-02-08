from PIL import Image
import array as arr


class ArrayListIterator:

    def __init__(self, lst):
        self._lst: ArrayList = lst
        # member variable to keep track of current index
        self._index: int = 0

    def __next__(self):
        ''''Returns the next value from the stored MyList instance.'''
        if self._index < len(self._lst):
            value = self._lst[self._index]
            self._index += 1
            return value
        # End of Iteration
        raise StopIteration


class ArrayList:
    '''A list interface.'''

    def __init__(self, size: int, value=None) -> None:
        """Creates a list of the given size, optionally intializing elements to value.

        The list is static. It only has space for size elements.

        Args:
        - size: size of the list; space is reserved for these many elements.
        - value: the optional initial value of the created elements.

        Returns:
        none
        """
        if value:
            temp = [value[0], value[1], value[2]]*size
            self.lst = arr.array('I', temp)
        else:
            self.lst = arr.array('I', [0]*3*size)

    def __len__(self) -> int:
        '''Returns the size of the list. Allows len() to be called on it.

        Ref: https://stackoverflow.com/q/7642434/1382487

        Args:

        Returns:
        the size of the list.
        '''
        return int(len(self.lst) / 3)

    def __getitem__(self, i: int):
        '''Returns the value at index, i. Allows indexing syntax.

        Ref: https://stackoverflow.com/a/33882066/1382487

        Args:
        - i: the index from which to retrieve the value.

        Returns:
        the value at index i.
        '''
        # Ensure bounds.
        assert 0 <= i < len(self),\
            f'Getting invalid list index {i} from list of size {len(self)}'

        return (self.lst[3*i], self.lst[(3*i)+1], self.lst[(3*i)+2])

    def __setitem__(self, i: int, value) -> None:
        '''Sets the element at index, i, to value. Allows indexing syntax.

        Ref: https://stackoverflow.com/a/33882066/1382487

        Args:
        - i: the index of the elemnent to be set
        - value: the value to be set

        Returns:
        none
        '''
        # Ensure bounds
        assert 0 <= i < len(self),\
            f'Setting invalid list index {i} in list of size {self.size()}'

        self.lst[3*i] = value[0]
        self.lst[(3*i)+1] = value[1]
        self.lst[(3*i)+2] = value[2]

    def __iter__(self) -> ArrayListIterator:
        '''Returns an iterator that allows iteration over this list.

        Ref: https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/

        Args:

        Returns:
        an iterator that allows iteration over this list.
        '''
        return ArrayListIterator(self)

    def get(self, i: int):
        '''Returns the value at index, i.

        Alternate to use of indexing syntax.

        Args:
        - i: the index from which to retrieve the value.

        Returns:
        the value at index i.
        '''
        return self[i]

    def set(self, i: int, value) -> None:
        '''Sets the element at index, i, to value.

        Alternate to use of indexing syntax.

        Args:
        - i: the index of the elemnent to be set
        - value: the value to be set

        Returns:
        none
        '''
        self[i] = value


class PointerListIterator:
    ''' Iterator class to make MyList iterable.
    https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
    '''

    def __init__(self, lst):
        self._lst: PointerList = lst
        self._index: int = 0

    def __next__(self):
        if self._index < len(self._lst):
            value = self._lst[self._index]
            self._index += 1
            return value
        # End of Iteration
        raise StopIteration


# node implemented to be used in linked list
class Node:

    def __init__(self, value=None):
        self.value = value
        self.next = None


class PointerList:
    '''A list interface.'''

    def __init__(self, size: int, value=None) -> None:
        """Creates a list of the given size, optionally intializing elements to value.

        The list is static. It only has space for size elements.

        Args:
        - size: size of the list; space is reserved for these many elements.
        - value: the optional initial value of the created elements.

        Returns:
        none
        """
        self.head = None
        self.size = 0

        # initialize pointer list with the value passed in the constructor
        for i in range(size):
            self.insert(i, value)

    def __len__(self):
        return self.size

    def __iter__(self) -> PointerListIterator:
        '''Returns an iterator that allows iteration over this list.

        Ref: https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/

        Args:

        Returns:
        an iterator that allows iteration over this list.
        '''
        return PointerListIterator(self)

    def __getitem__(self, i: int):
        '''Returns the value at index, i.

        Alternate to use of indexing syntax.

        Args:
        - i: the index from which to retrieve the value.

        Returns:
        the value at index i.
        '''
        u = self.head

        # traversing elements until we reach the one required
        for index in range(i):
            u = u.next
        return u.value

    def __setitem__(self, i: int, value) -> None:
        '''Sets the element at index, i, to value.

        Alternate to use of indexing syntax.

        Args:
        - i: the index of the elemnent to be set
        - value: the value to be set

        Returns:
        none
        '''
        u = self.head

        # traversing elements until we reach the one required
        for index in range(i):
            u = u.next
        u.value = value

    def insert(self, i, value):

        temp_node = Node(value)

        # inserting initial value
        if self.size == 0:
            self.head = temp_node

        # inserting at the very beginning
        elif i == 0:
            temp_node.next = self.head
            self.head = temp_node

        # inserting at end
        else:
            u = self.head
            for index in range(i-1):
                u = u.next

            temp_node.next = u.next
            u.next = temp_node
        self.size += 1

    def set(self, i: int, value) -> None:
        '''Sets the element at index, i, to value.

        Alternate to use of indexing syntax.

        Args:
        - i: the index of the elemnent to be set
        - value: the value to be set

        Returns:
        none
        '''
        self[i] = value

    def get(self, i: int):
        '''Returns the value at index, i.

        Alternate to use of indexing syntax.

        Args:
        - i: the index from which to retrieve the value.

        Returns:
        the value at index i.
        '''
        return self[i]


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
    """Returns an copy of src with the mask from maskfile applied to it.

    maskfile specifies a text file which contains an n by n mask. It has the
    following format:
    - the first line contains n
    - the next n^2 lines contain 1 element each of the flattened mask

    Args:
    - src: the image on which the mask is to be applied
    - maskfile: path to a file specifying the mask to be applied
    - average: if True, averaging should to be done when applying the mask

    Returns:
    an image which the result of applying the specified mask to src.
    """

    width, height = src.size

    img = src

    # new image instantiated that will store the resultant image
    result_img = MyImage((width, height), src.pointer)

    f = open(maskfile, "r")
    f = f.readlines()
    weights = []

    # mask length stores the size of matrix - n
    mask_length = int(f[0])

    # weights 2D list implemented below
    temp = []
    for i in range(1, len(f)):
        temp.append(int(f[i]))
        if i % mask_length == 0:
            weights.append(temp)
            temp = []

    # row (r) and column (c) used further below for accessing the position of each pixel and using the same for weights list
    r = 0
    c = 0

    for i in img.pixels:
        total_pixel_weight = 0
        weights_sum = 0

        mid = mask_length//2
        weights_mid = weights[mid][mid]
        incrementer = 1
        temp_offset = 0

        # middle pixel weight added
        mid_pixel = img.get(r, c)
        total_pixel_weight += (int((mid_pixel[0]+mid_pixel[1] +
                                    mid_pixel[2])//3)) * weights_mid

        weights_sum = weights[mid][mid]

        for j in range(mid+1, mask_length):
            # pixels on right added to weighted sum of the pixel
            try:
                avg_pixel = img.get(r, c+incrementer)
                avg_pixel = (avg_pixel[0] + avg_pixel[1] + avg_pixel[2])//3
                weight_of_avg_pixel = weights[mid][mid+incrementer]
                total_pixel_weight += (avg_pixel * weight_of_avg_pixel)
                weights_sum += weights[mid][mid+incrementer]
            except:
                pass

            # pixels on left added to weighted sum of the pixel
            try:
                avg_pixel2 = img.get(r, c-incrementer)
                avg_pixel2 = (avg_pixel2[0] + avg_pixel2[1] + avg_pixel2[2])//3
                weight_of_avg_pixel = weights[mid][mid-incrementer]
                total_pixel_weight += (avg_pixel2 * weight_of_avg_pixel)
                weights_sum += weights[mid][mid-incrementer]
            except:
                pass

            # pixels on upper side added to weighted sum of the pixel
            try:
                avg_pixel2 = img.get(r+incrementer, c)
                avg_pixel2 = (avg_pixel2[0] + avg_pixel2[1] + avg_pixel2[2])//3
                weight_of_avg_pixel = weights[mid+incrementer][mid]
                total_pixel_weight += (avg_pixel2 * weight_of_avg_pixel)
                weights_sum += weights[mid+incrementer][mid]
            except:
                pass

            # pixels on lower side added to weighted sum of the pixel
            try:
                avg_pixel2 = img.get(r-incrementer, c)
                avg_pixel2 = (avg_pixel2[0] + avg_pixel2[1] + avg_pixel2[2])//3
                weight_of_avg_pixel = weights[mid-incrementer][mid]
                total_pixel_weight += (avg_pixel2 * weight_of_avg_pixel)
                weights_sum += weights[mid-incrementer][mid]
            except:
                pass

            # pixels on upper left diagonal added to weighted sum of the pixel
            try:
                avg_pixel2 = img.get(r-incrementer, c-incrementer)
                avg_pixel2 = (avg_pixel2[0] + avg_pixel2[1] + avg_pixel2[2])//3
                weight_of_avg_pixel2 = weights[mid -
                                               incrementer][mid-incrementer]
                total_pixel_weight += (avg_pixel2 * weight_of_avg_pixel2)
                weights_sum += weights[mid-incrementer][mid-incrementer]
            except:
                pass

            # pixels on bottom right added to weighted sum of the pixel
            try:
                avg_pixel2 = img.get(r+incrementer, c+incrementer)
                avg_pixel2 = (avg_pixel2[0] + avg_pixel2[1] + avg_pixel2[2])//3
                weight_of_avg_pixel2 = weights[mid +
                                               incrementer][mid+incrementer]
                total_pixel_weight += (avg_pixel2 * weight_of_avg_pixel2)
                weights_sum += weights[mid+incrementer][mid+incrementer]
            except:
                pass

            # pixels on upper right added to weighted sum of the pixel
            try:
                avg_pixel2 = img.get(r-incrementer, c+incrementer)
                avg_pixel2 = (avg_pixel2[0] + avg_pixel2[1] + avg_pixel2[2])//3
                weight_of_avg_pixel2 = weights[mid -
                                               incrementer][mid+incrementer]
                total_pixel_weight += (avg_pixel2 * weight_of_avg_pixel2)
                weights_sum += weights[mid-incrementer][mid+incrementer]
            except:
                pass

            # pixels on bottom left added to weighted sum of the pixel
            try:
                avg_pixel3 = img.get(r+incrementer, c-incrementer)
                avg_pixel3 = (avg_pixel3[0] + avg_pixel3[1] + avg_pixel3[2])//3
                weight_of_avg_pixel3 = weights[mid +
                                               incrementer][mid-incrementer]
                total_pixel_weight += (avg_pixel3 * weight_of_avg_pixel3)
                weights_sum += weights[mid+incrementer][mid-incrementer]
            except:
                pass

            for val in range(1, temp_offset+1):
                # pixels missed on upper right added to weighted sum of the pixel
                try:
                    avg_pixel4 = img.get(r-incrementer, c+val)
                    avg_pixel4 = (avg_pixel4[0] +
                                  avg_pixel4[1] + avg_pixel4[2])//3

                    weight_of_avg_pixel4 = weights[mid-incrementer][mid+val]
                    total_pixel_weight += (avg_pixel4 * weight_of_avg_pixel4)
                    weights_sum += weights[mid-incrementer][mid+val]
                except:
                    pass

                # pixels missed on upper left added to weighted sum of the pixel
                try:
                    avg_pixel5 = img.get(r-incrementer, c-val)
                    avg_pixel5 = (avg_pixel5[0] +
                                  avg_pixel5[1] + avg_pixel5[2])//3
                    weight_of_avg_pixel5 = weights[mid-incrementer][mid-val]
                    total_pixel_weight += (avg_pixel5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid-incrementer][mid-val]
                except:
                    pass

                # pixels missed on lower right added to weighted sum of the pixel
                try:
                    avg_pixel5 = img.get(r+incrementer, c+val)
                    avg_pixel5 = (avg_pixel5[0] +
                                  avg_pixel5[1] + avg_pixel5[2])//3
                    weight_of_avg_pixel5 = weights[mid+incrementer][mid+val]
                    total_pixel_weight += (avg_pixel5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid+incrementer][mid+val]
                except:
                    pass

                # pixels missed on lower left added to weighted sum of the pixel
                try:
                    avg_pixel5 = img.get(r+incrementer, c-val)
                    avg_pixel5 = (avg_pixel5[0] +
                                  avg_pixel5[1] + avg_pixel5[2])//3
                    weight_of_avg_pixel5 = weights[mid+incrementer][mid-val]
                    total_pixel_weight += (avg_pixel5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid+incrementer][mid-val]
                except:
                    pass

                # pixels missed on right lower added to weighted sum of the pixel
                try:
                    avg_pixel5 = img.get(r+val, c+incrementer)
                    avg_pixel5 = (avg_pixel5[0] +
                                  avg_pixel5[1] + avg_pixel5[2])//3
                    weight_of_avg_pixel5 = weights[mid+val][mid+incrementer]
                    total_pixel_weight += (avg_pixel5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid+val][mid+incrementer]
                except:
                    pass

                # pixels missed on right upper added to weighted sum of the pixel
                try:
                    avg_pixel5 = img.get(r-val, c+incrementer)
                    avg_pixel5 = (avg_pixel5[0] +
                                  avg_pixel5[1] + avg_pixel5[2])//3
                    weight_of_avg_pixel5 = weights[mid-val][mid+incrementer]
                    total_pixel_weight += (avg_pixel5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid-val][mid+incrementer]
                except:
                    pass

                # pixels missed on left lower added to weighted sum of the pixel
                try:
                    avg_pixel5 = img.get(r+val, c-incrementer)
                    avg_pixel5 = (avg_pixel5[0] +
                                  avg_pixel5[1] + avg_pixel5[2])//3
                    weight_of_avg_pixel5 = weights[mid+val][mid-incrementer]
                    total_pixel_weight += (avg_pixel5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid+val][mid-incrementer]
                except:
                    pass

                # pixels missed on left upper added to weighted sum of the pixel
                try:
                    avg_pixel5 = img.get(r-val, c-incrementer)
                    avg_pixel5 = (avg_pixel5[0] +
                                  avg_pixel5[1] + avg_pixel5[2])//3
                    weight_of_avg_pixel5 = weights[mid-val][mid-incrementer]
                    total_pixel_weight += (avg_pixel5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid-val][mid-incrementer]
                except:
                    pass

            temp_offset += 1
            incrementer += 1

        if average:
            new_value = int(total_pixel_weight // weights_sum)
            new_value = (new_value, new_value, new_value)
        else:
            new_value = int(total_pixel_weight)
            new_value = min(max(0, new_value), 255)
            new_value = (new_value, new_value, new_value)

        result_img.set(r, c, new_value)

        # value of row and column incremented according to the pixels being traversed
        if c == (width-1):
            c = -1
            r += 1

        c += 1

    return result_img
