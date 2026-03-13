from libcpp cimport bool


cdef extern from "scope_buffer.hpp" namespace "detail_server_shm":
    cdef cppclass scope_buffer_reader:
        bool valid()
        bool pull(unsigned int& frames)
        float* data()
        unsigned int max_frames()
        unsigned int channels()


cdef extern from "server_shm.hpp" namespace "detail_server_shm":
    cdef cppclass server_shared_memory_client:
        server_shared_memory_client(unsigned int port_number) except +
        float* get_control_busses()
        void set_control_bus(int bus, float value)
        scope_buffer_reader get_scope_buffer_reader(unsigned int index)
