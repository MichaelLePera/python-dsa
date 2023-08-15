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
from typing import Iterator, TypeVar
from typing import Type
from typing import Callable
from typing import Generic
from typing import Optional
from typing import overload
from typing import final
from typing import cast

import array


# TODO: change to 3.12 implementation
_T = TypeVar('_T')



class Vertex(Generic[_T]):
    
    def __init__(self, data: _T | None = None) -> None:
        super().__init__()
        self._data = data
        
    def __hash__(self) -> int:
        return hash((self._data ))
    
    @property
    def data(self) -> _T:
        return self._data
    


class Graph(Collection[_T]):
    
    def __init__(self) -> None:
        super().__init__()
        self._root: Vertex[_T] | None = None
        
        # maybe should be ll/dll/skiplist? either way this memory gon be crazy
        self._vertices: list[Vertex[_T]] = list() 
        
        self._incidence_matrix: list[list[int]] = []
    
    
    @overload
    def adjacent(self, __x: Vertex[_T], __y: Vertex[_T]) -> bool:
        ...
        
    @overload
    def adjacent(self, __x: _T, __y: _T) -> bool:
        ...
    
    def adjacent(self, __x: Vertex[_T] | _T, __y: Vertex[_T] | _T) -> bool:
        
        index_x = self.index(__x)
        index_y = self.index(__y)
        
        if index_x == -1 or index_y == -1:
            raise ValueError()
        
        return index_y in self._incidence_matrix[index_x]
                
    def neighbor(self, __x:  Vertex[_T] | _T) -> int:
        return self._incidence_matrix[self.index(__x)]
    
    def add_vertex(self, __x:  Vertex[_T] | _T) -> None:
        if self.index(__x) != -1:
            raise ValueError('Vertex already added.')
        
        cardinality = len(self._vertices)
        
    
    def remove_vertex(self, x:  Vertex[_T]): ...
    
    def add_edge(self, x:  Vertex[_T], y:  Vertex[_T], z): ...
    
    def remove_edge(self, x:  Vertex[_T], y:  Vertex[_T]): ...
    
    def get_vertex_value(self, x:  Vertex[_T], y:  Vertex[_T]): ...
    
    def set_vertex_value(self, x:  Vertex[_T], y:  Vertex[_T], v): ...
    
    
    def index(self, __x: _T | Vertex[_T]) -> int: # return: {-1 <= i < inf}
        target = __x.data if isinstance(__x, Vertex) else __x
        for i, n in self._vertices:
            if n == target:
                return i
        return -1
    
    def has(self, __x: Vertex[_T] | _T) -> bool:
        return self.index(__x) != -1
        
    
    def __contains__(self, __x: Vertex[_T] | _T) -> bool:
        return self.has(__x)
    
    def __iter__(self) -> Iterator[_T]:
        return super().__iter__()
    
    def __len__(self) -> int:
        return super().__len__()
    
    


g = Graph()
g.adjacent(1, 2)