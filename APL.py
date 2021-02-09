from mylist import *
import array as arr

class PointerListIterator:
    ''' Iterator class to make MyList iterable.
    https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
    '''

    def __init__(self, lst):
        self._lst: PointerList = lst
        self._index: int = 0

    def __next__(self):
        if len(self._lst) > self._index:
            value = self._lst[self._index]
            self._index += 1
            return value
        # End of Iteration
        else:
            raise StopIteration


class Node:

    def __init__(self, value=None):
        self.value = value
        self.next = None


class PointerList:
    '''list interface.'''

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

        for i in range(size):
            self.insert(i, value)

    def __len__(self):
        length_p = self.size
        return length_p

    def __iter__(self) -> PointerListIterator:
        '''Returns an iterator that allows iteration over this list.
        Ref: https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
        Args:
        Returns:
        an iterator that allows iteration over this list.
        '''
        p_iterator = PointerListIterator(self)
        return p_iterator

    def __getitem__(self, i: int):
        '''Returns the value at index, i.
        Alternate to use of indexing syntax.
        Args:
        - i: the index from which to retrieve the value.
        Returns:
        the value at index i.
        '''
        universal = self.head
        for index in range(i):
            universal = universal.next
        else:
            return universal.value

    def __setitem__(self, i: int, value) -> None:
        '''Sets the element at index, i, to value.
        Alternate to use of indexing syntax.
        Args:
        - i: the index of the elemnent to be set
        - value: the value to be set
        Returns:
        none
        '''
        universal = self.head
        for index in range(i):
            universal = universal.next
        else:
            universal.value = value


    def insert(self, i, value):

        temporary_t_node = Node(value)
        if self.size == 0:
            self.head = temporary_t_node
        elif i == 0:
            temporary_t_node.next = self.head
            self.head = temporary_t_node

        else:
            universal = self.head
            for index in range(i-1):
                universal = universal.next

            temporary_t_node.next = universal.next
            universal.next = temporary_t_node
        self.size = self.size + 1

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


class ArrayListIterator:
    ''' Iterator class to make MyList iterable.
    https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
    '''

    def __init__(self, lst):
        # MyList object reference
        self._lst: ArrayList = lst
        # member variable to keep track of current index
        self._index: int = 0

    def __next__(self):
        ''''Returns the next value from the stored MyList instance.'''
        if len(self._lst) > self._index:
            value = self._lst[self._index]
            self._index
            self._index = self._index + 1
            return value
        # End of Iteration
        else:
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

    def __iter__(self) -> MyListIterator:
        '''Returns an iterator that allows iteration over this list.
        Ref: https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
        Args:
        Returns:
        an iterator that allows iteration over this list.
        '''
        a_iterator = ArrayListIterator(self)
        return a_iterator

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
