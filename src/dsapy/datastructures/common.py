from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from collections.abc import Sized
from collections.abc import Container
from collections.abc import Collection
from collections.abc import Iterator
from collections.abc import Sequence
from collections.abc import Hashable
from typing import TypeVar
from typing import Type
from typing import Callable
from typing import Generic
from typing import Optional
from typing import overload
from typing import final
from typing import cast
from typing_extensions import Self

_T = TypeVar('_T')


class _Node(Hashable, Generic[_T], ABC):

    def __init__(self, data: _T) -> None:
        self._data = data

    @property
    def data(self) -> _T:
        return self._data

    @data.setter
    def data(self, value: _T):
        self._data = value


class _LinkedNode(_Node[_T]):

    def __init__(self, data: _T) -> None:
        super().__init__(data)
        self._next: _LinkedNode[_T] | None = None

    def __hash__(self) -> int:
        return hash((self._data, self._next))

    @property
    def next(self) -> _LinkedNode[_T] | None:
        return self._next

    @next.setter
    def next(self, other: _LinkedNode[_T] | None) -> None:
        self._next = other


class _DoublyLinkedNode(_LinkedNode[_T]):

    def __init__(self, data: _T) -> None:
        super().__init__(data)
        self._prev: _DoublyLinkedNode[_T] | None = None

    def __hash__(self) -> int:
        return hash((self._data, self._next, self._prev))

    @property
    def prev(self) -> _DoublyLinkedNode[_T] | None:
        return self._prev

    @prev.setter
    def prev(self, other: _DoublyLinkedNode[_T] | None) -> None:
        self._prev = other


class _LinkedListNodeIterator(Iterator[_LinkedNode[_T]]):

    def __init__(self, root: _LinkedNode[_T] | None):
        self._curr = root

    def __iter__(self) -> Iterator[_LinkedNode[_T]]:
        return self

    def __next__(self) -> _LinkedNode[_T]:
        if self._curr is None or not isinstance(self._curr, _LinkedNode):
            raise StopIteration()
        temp = self._curr
        self._curr = self._curr.next
        return temp


class _LinkedListIterator(Iterator[_T]):
    def __init__(self, root: _LinkedNode[_T] | None):
        self._iter = iter(_LinkedListNodeIterator(root))

    def __iter__(self) -> _LinkedListIterator[_T]:
        return self

    def __next__(self) -> _T:
        return next(self._iter).data


class LinkedList(Sequence[_T]):

    @overload
    def __getitem__(self, index: int) -> _T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[_T]:
        ...

    def __getitem__(self, index: int | slice) -> _T | Sequence[_T]:
        match index:
            case int():
                if index == -1:
                    index = self._length - 1

                if 0 > index > self._length - 1:
                    raise IndexError(f'{index} not in [0<=i<length]')
                for idx, data in enumerate(_LinkedListIterator(self._head)):
                    if idx == index:
                        return data

                raise ValueError('Index not valid.')

            case slice():
                start = index.start
                stop = index.stop if index.stop is not None else self._length
                step = index.step if index.step is not None else 1

                if (0 > start > self._length - 1) or (0 > stop > self._length):
                    raise IndexError(f'{start, stop} not in [0<=i<=length]')

                if stop - start < step:
                    raise IndexError(f'Step not valid')

                new = LinkedList(x for i, x in enumerate(_LinkedListIterator(self._head))
                                 if start <= i < stop
                                 and (i - start) % step == 0)

                return new

            case _:
                raise TypeError(f'Can only access by int or slice not {type(index)}')

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator[_T]:
        return _LinkedListIterator(self._head)

    def __contains__(self, item: object):
        ...

    def __init__(self, iterable: Iterable[_T] | None = None):
        self._head: _LinkedNode | None = None
        self._length: int = 0
        if iterable is not None:
            for d in iterable:
                self.insert(d)

    def insert(self, data: _T, index: int = -1) -> None:
        if index == -1:
            index = self._length
        elif self._length < index < 0:
            raise IndexError(f'\'{index}\' out of bounds.')

        node = _LinkedNode(data)
        if self._head is None:
            self._head = node
        else:
            match index:
                case 0:
                    node.next = self._head
                    self._head = node
                case self._length:
                    *_, last = (x for x in _LinkedListNodeIterator(self._head))
                    last.next = node
                case _:
                    prev: _LinkedNode | None = None
                    for i, n in enumerate(_LinkedListNodeIterator(self._head)):
                        if i == index - 1:
                            prev = n
                            break
                    assert prev is not None, 'something went wrong'

                    prev.next = node
        self._length += 1

    def pop(self, index: int = -1) -> _T | None:
        if index == -1:
            index = self._length
        elif self._length - 1 < index < 0:
            raise IndexError(f'\'{index}\' out of bounds.')

        if self._head is None:
            return None

        match index:
            case 0:
                val = self._head.data
                self._head = self._head.next

            case _:
                prev: _LinkedNode | None = None
                for i, n in enumerate(_LinkedListNodeIterator(self._head)):
                    if i == index - 1:
                        prev = n
                        break
                assert prev is not None, 'something went wrong'
                if prev.next is not None:
                    val = prev.next.data
                    prev.next = prev.next.next
                else:
                    val = None
                    prev.next = None
        self._length -= 1
        return val


if __name__ == '__main__':
    l1 = LinkedList('abcde')
    print(l1[1:3][-1])
