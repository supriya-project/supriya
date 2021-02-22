cdef extern from "server_shm.hpp" namespace "detail_server_shm":
    cdef cppclass server_shared_memory_client:
        server_shared_memory_client(unsigned int port_number) except +
        float* get_control_busses()
