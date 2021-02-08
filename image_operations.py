from myimage import MyImage
from APL import *
from array import arr
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

            # RED color suppressed if RED is true
            if RED:
                temp_t_tuple = (0,) + (temp_t_tuple[1],) + (temp_t_tuple[2],)

            # GREEN color suppressed if GREEN is true
            if GREEN:
                temp_t_tuple = (temp_t_tuple[0],) + (0,) + (temp_t_tuple[2],)

            # BLUE color suppressed if BLUE is true
            if BLUE:
                temp_t_tuple = (temp_t_tuple[0],) + (temp_t_tuple[1],) + (0,)

            # default condition implemented (RED channel suppressed)
            if RED == False and BLUE == False and GREEN == False:
                temp_t_tuple = (0,) + (temp_t_tuple[1],) + (temp_t_tuple[2],)

            photo.set(j, i, temp_t_tuple)

    return photo

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


def apply_mask(src: MyImage, maskfile: str, average: bool = True) -> MyImage:
    #src.size is a tuple holding size of the picture (WT, HT)
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
    WT, HT = src.size

    photo = src

    # new image instantiated that will store the resultant image
    result_photo = MyImage((WT, HT), src.pointer)

    f = open(maskfile, "x_axis")
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

    # row (x_axis) and column (y_axis) used further below for accessing the position of each pixel and using the same for weights list
    x_axis = 0
    y_axis = 0

    for i in photo.pixels:
        total_pixel_weight = 0
        weights_sum = 0

        mid = mask_length//2
        weights_mid = weights[mid][mid]
        inc = 1
        temp_offset = 0

        # middle pixel weight added
        mid_pixel = photo.get(x_axis, y_axis)
        total_pixel_weight += (int((mid_pixel[0]+mid_pixel[1] +
                                    mid_pixel[2])//3)) * weights_mid

        weights_sum = weights[mid][mid]

        for j in range(mid+1, mask_length):
            # pixels on right added to weighted sum of the pixel
            try:
                avg_pixel = photo.get(x_axis, y_axis+inc)
                avg_pixel = (avg_pixel[0] + avg_pixel[1] + avg_pixel[2])//3
                weight_of_avg_pixel = weights[mid][mid+inc]
                total_pixel_weight += (avg_pixel * weight_of_avg_pixel)
                weights_sum += weights[mid][mid+inc]
            except:
                pass

            # pixels on left added to weighted sum of the pixel
            try:
                a2 = photo.get(x_axis, y_axis-inc)
                a2 = (a2[0] + a2[1] + a2[2])//3
                weight_of_avg_pixel = weights[mid][mid-inc]
                total_pixel_weight += (a2 * weight_of_avg_pixel)
                weights_sum += weights[mid][mid-inc]
            except:
                pass

            # pixels on upper side added to weighted sum of the pixel
            try:
                a2 = photo.get(x_axis+inc, y_axis)
                a2 = (a2[0] + a2[1] + a2[2])//3
                weight_of_avg_pixel = weights[mid+inc][mid]
                total_pixel_weight += (a2 * weight_of_avg_pixel)
                weights_sum += weights[mid+inc][mid]
            except:
                pass

            # pixels on lower side added to weighted sum of the pixel
            try:
                a2 = photo.get(x_axis-inc, y_axis)
                a2 = (a2[0] + a2[1] + a2[2])//3
                weight_of_avg_pixel = weights[mid-inc][mid]
                total_pixel_weight += (a2 * weight_of_avg_pixel)
                weights_sum += weights[mid-inc][mid]
            except:
                pass

            # pixels on upper left diagonal added to weighted sum of the pixel
            try:
                a2 = photo.get(x_axis-inc, y_axis-inc)
                a2 = (a2[0] + a2[1] + a2[2])//3
                weight_of_avg_pixel2 = weights[mid -
                                               inc][mid-inc]
                total_pixel_weight += (a2 * weight_of_avg_pixel2)
                weights_sum += weights[mid-inc][mid-inc]
            except:
                pass

            # pixels on bottom right added to weighted sum of the pixel
            try:
                a2 = photo.get(x_axis+inc, y_axis+inc)
                a2 = (a2[0] + a2[1] + a2[2])//3
                weight_of_avg_pixel2 = weights[mid +
                                               inc][mid+inc]
                total_pixel_weight += (a2 * weight_of_avg_pixel2)
                weights_sum += weights[mid+inc][mid+inc]
            except:
                pass

            # pixels on upper right added to weighted sum of the pixel
            try:
                a2 = photo.get(x_axis-inc, y_axis+inc)
                a2 = (a2[0] + a2[1] + a2[2])//3
                weight_of_avg_pixel2 = weights[mid -
                                               inc][mid+inc]
                total_pixel_weight += (a2 * weight_of_avg_pixel2)
                weights_sum += weights[mid-inc][mid+inc]
            except:
                pass

            # pixels on bottom left added to weighted sum of the pixel
            try:
                a3 = photo.get(x_axis+inc, y_axis-inc)
                a3 = (a3[0] + a3[1] + a3[2])//3
                weight_of_avg_pixel3 = weights[mid +
                                               inc][mid-inc]
                total_pixel_weight += (a3 * weight_of_avg_pixel3)
                weights_sum += weights[mid+inc][mid-inc]
            except:
                pass

            for val in range(1, temp_offset+1):
                # pixels missed on upper right added to weighted sum of the pixel
                try:
                    a4 = photo.get(x_axis-inc, y_axis+val)
                    a4 = (a4[0] +
                                  a4[1] + a4[2])//3

                    weight_of_avg_pixel4 = weights[mid-inc][mid+val]
                    total_pixel_weight += (a4 * weight_of_avg_pixel4)
                    weights_sum += weights[mid-inc][mid+val]
                except:
                    pass

                # pixels missed on upper left added to weighted sum of the pixel
                try:
                    a5 = photo.get(x_axis-inc, y_axis-val)
                    a5 = (a5[0] +
                                  a5[1] + a5[2])//3
                    weight_of_avg_pixel5 = weights[mid-inc][mid-val]
                    total_pixel_weight += (a5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid-inc][mid-val]
                except:
                    pass

                # pixels missed on lower right added to weighted sum of the pixel
                try:
                    a5 = photo.get(x_axis+inc, y_axis+val)
                    a5 = (a5[0] +
                                  a5[1] + a5[2])//3
                    weight_of_avg_pixel5 = weights[mid+inc][mid+val]
                    total_pixel_weight += (a5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid+inc][mid+val]
                except:
                    pass

                # pixels missed on lower left added to weighted sum of the pixel
                try:
                    a5 = photo.get(x_axis+inc, y_axis-val)
                    a5 = (a5[0] +
                                  a5[1] + a5[2])//3
                    weight_of_avg_pixel5 = weights[mid+inc][mid-val]
                    total_pixel_weight += (a5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid+inc][mid-val]
                except:
                    pass

                # pixels missed on right lower added to weighted sum of the pixel
                try:
                    a5 = photo.get(x_axis+val, y_axis+inc)
                    a5 = (a5[0] +
                                  a5[1] + a5[2])//3
                    weight_of_avg_pixel5 = weights[mid+val][mid+inc]
                    total_pixel_weight += (a5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid+val][mid+inc]
                except:
                    pass

                # pixels missed on right upper added to weighted sum of the pixel
                try:
                    a5 = photo.get(x_axis-val, y_axis+inc)
                    a5 = (a5[0] +
                                  a5[1] + a5[2])//3
                    weight_of_avg_pixel5 = weights[mid-val][mid+inc]
                    total_pixel_weight += (a5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid-val][mid+inc]
                except:
                    pass

                # pixels missed on left lower added to weighted sum of the pixel
                try:
                    a5 = photo.get(x_axis+val, y_axis-inc)
                    a5 = (a5[0] +
                                  a5[1] + a5[2])//3
                    weight_of_avg_pixel5 = weights[mid+val][mid-inc]
                    total_pixel_weight += (a5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid+val][mid-inc]
                except:
                    pass

                # pixels missed on left upper added to weighted sum of the pixel
                try:
                    a5 = photo.get(x_axis-val, y_axis-inc)
                    a5 = (a5[0] +
                                  a5[1] + a5[2])//3
                    weight_of_avg_pixel5 = weights[mid-val][mid-inc]
                    total_pixel_weight += (a5 * weight_of_avg_pixel5)
                    weights_sum += weights[mid-val][mid-inc]
                except:
                    pass

            temp_offset += 1
            inc += 1

        if average:
            new_value = int(total_pixel_weight // weights_sum)
            new_value = (new_value, new_value, new_value)
        else:
            new_value = int(total_pixel_weight)
            new_value = min(max(0, new_value), 255)
            new_value = (new_value, new_value, new_value)

        result_photo.set(x_axis, y_axis, new_value)

        # value of row and column incremented according to the pixels being traversed
        if y_axis == (WT-1):
            y_axis = -1
            x_axis += 1

        y_axis += 1

    return result_photo
