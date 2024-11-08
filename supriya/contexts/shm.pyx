# cython: language_level=3
# distutils: language = c++

from typing import List, Union

from .entities import Bus, BusGroup
from .shm cimport server_shared_memory_client


cdef class ServerSHM:
    """
    Server shared memory interface.

    Currently supports reading control busses only.

    .. warning::

       Not supported on Windows.

    """
    cdef server_shared_memory_client* client
    cdef unsigned int bus_count

    def __cinit__(self, unsigned int port_number, unsigned int bus_count):
        self.bus_count = bus_count
        self.client = new server_shared_memory_client(port_number)

    def __dealloc__(self) -> None:
        del self.client

    def __getitem__(self, item: Union[int, slice, Bus, BusGroup]) -> Union[float, List[float]]:
        if isinstance(item, Bus):
            item = int(item)
        elif isinstance(item, BusGroup):
            item = slice(int(item), int(item) + len(item))
        if isinstance(item, int):
            if item < 0 or item >= self.bus_count:
                raise ValueError("index out of bounds")
            return self.client.get_control_busses()[item]
        elif isinstance(item, slice):
            result = []
            for index in range(*item.indices(self.bus_count)):
                result.append(self.client.get_control_busses()[index])
            return result
        raise ValueError(item)

    def __setitem__(self, item: Union[int, slice, Bus, BusGroup], value: Union[float, List[float]]) -> None:
        if isinstance(item, Bus):
            item = int(item)
        elif isinstance(item, BusGroup):
            item = slice(int(item), int(item) + len(item))
        if isinstance(item, int):
            if item < 0 or item >= self.bus_count:
                raise ValueError("index out of bounds")
            if not isinstance(value, float): 
                raise ValueError(value) 
            self.client.set_control_bus(item, value)
        elif isinstance(item, slice):
            for i, j in enumerate(range(*item.indices(self.bus_count))):
                self.client.set_control_bus(j, value[i])
