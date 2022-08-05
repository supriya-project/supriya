# distutils: language = c++

from .shm cimport server_shared_memory_client


cdef class ServerSHM:
    cdef server_shared_memory_client* client
    cdef unsigned int bus_count

    def __cinit__(self, unsigned int port_number, unsigned int bus_count):
        self.client = new server_shared_memory_client(port_number)
        self.bus_count = bus_count

    def __dealloc__(self):
        del self.client

    def __getitem__(self, item):
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
