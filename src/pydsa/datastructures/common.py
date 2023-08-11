from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from collections.abc import Sized
from collections.abc import Container
from collections.abc import Collection
from collections.abc import Iterator
from collections.abc import Sequence
from typing import TypeVar
from typing import Callable
from typing import Generic
from typing import Optional
from typing import Self

_T = TypeVar('_T')


class LinkedList(Collection[_T]):
    class Node(Generic[_T]):
        def __init__(self, _data: Optional[_T] = None, _next: Optional[Node[_T]] = None) -> None:
            self._data = _data
            self._next = _next

        @property
        def data(self) -> _T:
            return self._data

        @data.setter
        def data(self, _data: Optional[_T]) -> None:
            self._data = _data

        @property
        def next(self) -> Optional[Node[_T]]:
            return self._next

        @next.setter
        def next(self, _next: Optional[Node[_T]]) -> None:
            self._next = _next

    class Iterator(Iterator[_T]):
        def __init__(self, head: LinkedList.Node[_T], give_node: bool = False):
            self._curr = head
            self._give_node = give_node

        def __iter__(self) -> Self[_T]:
            return self

        def __next__(self) -> _T | Node[_T]:
            if self._curr is None:
                raise StopIteration()
            temp = self._curr
            self._curr = self._curr.next
            return temp if self._give_node else temp.data

    class Result(Generic[_T]):
        def __init__(self,
                     success: bool,
                     prev: None | LinkedList.Node[_T],
                     curr: None | LinkedList.Node[_T],
                     index: None | int
                     ):
            self._success = success
            self._prev = prev
            self._curr = curr
            self._index = index

        def __repr__(self):
            return f'Result(success={self._success}, prev=Node({self._prev.data if self._prev is not None else None})' \
                   f', curr=Node({self._curr.data if self._curr is not None else None}), index={self._index})'

        @property
        def success(self) -> bool:
            return self._success

        @property
        def prev(self) -> None | LinkedList.Node[_T]:
            return self._prev

        @property
        def curr(self) -> None | LinkedList.Node[_T]:
            return self._curr

        @property
        def index(self) -> None | int:
            return self._index

    def __init__(self, iterable: Optional[Iterable[_T]] = None):
        self._head: Optional[LinkedList.Node[_T]] = None
        self._length: int = 0
        if iterable:
            for x in iterable:
                self.insert(x)

    def insert(self, data: _T, index: int = -1) -> None:
        if index == -1:
            index = self.length

        index = self._verify_index(index)

        new_node = LinkedList.Node(data)

        match index:
            case 0:
                self._insert_at_start(new_node)
            case self._length:
                self._insert_at_end(new_node)
            case _:
                self._insert_within(new_node)

        self._length += 1

    def _insert_within(self, new_node: LinkedList.Node):
        result = self._get_node(lambda i, _: i == index)
        prev, curr = result.prev, result.curr
        if prev is not None:
            prev.next = new_node
        new_node.next = curr

    def _insert_at_end(self, new_node: LinkedList.Node):
        *_, tail = LinkedList.Iterator(self._head, True)
        tail.next = new_node

    def _insert_at_start(self, new_node: LinkedList.Node[_T]):
        new_node.next = self._head
        self._head = new_node

    def _get_node(self, predicate: Callable[[int, Node[_T]], bool]) -> LinkedList.Result[_T]:
        prev = None
        for i, n in enumerate(LinkedList.Iterator(self._head, True)):
            if predicate(i, n):
                return LinkedList.Result(True, prev, n, i)
            prev = n
        return LinkedList.Result(False, None, None, -1)

    def pop(self, index: int = -1) -> _T:
        if index == -1:
            index = self._length - 1

        index = self._verify_index(index)

        result = self._get_node(lambda i, _: i == index)
        if result.prev is None:
            self._head = result.curr.next
        else:
            result.prev.next = result.curr.next
        self._length -= 1
        return result.curr.data if result.curr is not None else None

    def _verify_index(self, index: int) -> int:
        if not isinstance(index, int):
            raise TypeError(f'Index must be of type \'int\' not \'{type(index)}\'')

        if index > self._length:
            raise ValueError(f'\'{index}\' exceeds length of \'{self.length}\'.')

        if index < 0:
            raise ValueError()

        return index

    def __repr__(self):
        return '[' + ', '.join([x for x in self]) + ']'

    def __contains__(self, item: _T) -> bool:
        return self._get_node(lambda _, x: x.data == item).success

    def __iter__(self) -> LinkedList.Iterator[_T]:
        return LinkedList.Iterator(self._head)

    def __len__(self) -> int:
        return self._length

    @property
    def length(self) -> int:
        return self._length

    @property
    def is_empty(self) -> bool:
        return not bool(self._length)


class DoublyLinkedList(LinkedList[_T]):
    class Node(LinkedList.Node[_T]):
        def __init__(self,
                     _data: Optional[_T] = None,
                     _prev: Optional[Node[_T]] = None,
                     _next: Optional[Node[_T]] = None
                     ) -> None:
            super().__init__(_data, _next)
            self._prev = _prev

        @property
        def prev(self):
            return self._prev

        @prev.setter
        def prev(self, prev: DoublyLinkedList.Node[_T]):
            if not isinstance(prev, DoublyLinkedList.Node):
                raise TypeError()
            self._prev = prev

    def __init__(self, iterable: Optional[Iterable[_T]]):
        self._tail = None
        super().__init__(iterable)
    # def __init__(self, iterable: Optional[Iterable[_T]] = None):
    #     self._head: Optional[LinkedList.Node[_T]] = None
    #     self._length: int = 0
    #     if iterable:
    #         for x in iterable:
    #             self.insert(x)
