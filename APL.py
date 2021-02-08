import array as arr
class Node:
    def __init__(self, value):
        
        self.data = value
        self.nextNode = None


class PointerListIterator:

    def __init__(self, lst):
        # PointerList object reference
        self._lst: PointerList = lst
        # member variable to keep track of current index
        self._index: int = 0

    def __next__(self):
        ''''Returns the next value from the stored PointerList instance.'''
        if self._index < len(self._lst):
            value = self._lst[self._index]
            self._index += 1
            return value
        # End of Iteration
        raise StopIteration


class PointerList:

    def __init__(self, size: int, value=None) -> None:
        self.size = size
        self.head = None

        if value:
            
            for i in range(size):
                if self.head == None:
                    self.head = Node(value)
                else:

                    cNode = self.head

                    while cNode.nextNode:
                        cNode = cNode.nextNode
                    if cNode.nextNode == None:
                        cNode.nextNode = Node(value)
    
    def __len__(self) -> int:
        return self.size

    def __getitem__(self, i: int):
        assert 0 <= i < len(self),\
            f'Getting invalid list index {i} from list of size {len(self)}'
        x = 0
        cNode = self.head
        while x < i:
            cNode = cNode.nextNode
            x += 1
        return cNode.data

    def __setitem__(self, i: int, value) -> None:
        assert 0 <= i < len(self),\
            f'Setting invalid list index {i} in list of size {self.size()}'
        x = 0
        cNode = self.head
        while x < i:
            cNode = cNode.nextNode
            x += 1
        cNode.data = value        
            

    def __iter__(self):
        return PointerListIterator(self)

    def get(self, i: int) -> tuple:
        return self[i]

    def set(self, i: int, value) -> None:
        self[i] = value
        


class ArrayListIterator:
    ''' Using this to iterate over the three RGB arrays'''

    def __init__(self, red, green, blue):
        self._red: ArrayList = red
        self._green: ArrayList = green
        self._blue: ArrayList = blue
        self._index: int = 0

    def __next__(self):
        if self._index < len(self._green):
            r, g, b = self._red[self._index], self._green[self._index], self._blue[self._index]
            self._index += 1
            return (r, g, b)
        raise StopIteration

class ArrayList(object):
    def __init__(self, size: int, value):
        self.size = 0
        if value == None:
            self.red_array = arr.array('l')
            self.green_array = arr.array('l')
            self.blue_array = arr.array('l')

        else:
            self.red_array = arr.array('l', [value[0]])
            self.green_array = arr.array('l', [value[1]])
            self.blue_array = arr.array('l', [value[2]])
            self.size += 1

    def set(self, i: int, value) -> None: 
        self.__setitem__(i, value)

    def __getitem__(self, i: int):
        return (self.red_array[i], self.green_array[i], self.blue_array[i])
        
    def get(self, i: int) -> (int, int, int): 
        self.__getitem__(i)

        assert 0 <= i < __len__(self),\
            f'Getting invalid list index {i} from list of size {len(self)}'

    def __len__(self):
        return self.size

    def __setitem__(self, i: int, value) -> None:
        if i >= self.size:
            self.red_array.append(value[0])
            self.green_array.append(value[1])
            self.blue_array.append(value[2])
            self.size += 1
        else:
            self.red_array[i] = value[0]
            self.green_array[i] = value[1]
            self.blue_array[i] = value[2]

         # Ensure bounds.
        assert 0 <= i < len(self),\
            f'Setting invalid list index {i} in list of size {self}'


    def __iter__(self) -> ArrayListIterator:
        return ArrayListIterator(self.red_array, self.green_array, self.blue_array)

