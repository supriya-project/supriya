# -*- encoding: utf-8 -*-
from supriya.library.systemlib.Enumeration import Enumeration


class ServerCommandType(Enumeration):
    r'''An enumeration of scsynth message types.
    '''

    ### CLASS VARIABLES ###

    NOTHING = 0
    NOTIFY = 1
    STATUS = 2
    QUIT = 3
    CMD = 4
    D_RECV = 5
    D_LOAD = 6
    D_LOAD_DIR = 7
    D_FREE_ALL = 8
    S_NEW = 9
    N_TRACE = 10
    N_FREE = 11
    N_RUN = 12
    N_CMD = 13
    N_MAP = 14
    N_SET = 15
    N_SETN = 16
    N_FILL = 17
    N_BEFORE = 18
    N_AFTER = 19
    U_CMD = 20
    G_NEW = 21
    G_HEAD = 22
    G_TAIL = 23
    G_FREE_aLL = 24
    C_SET = 25
    C_SETN = 26
    C_FILL = 27
    B_ALLOC = 28
    B_ALLOC_READ = 29
    B_READ = 30
    B_WRITE = 31
    B_FREE = 32
    B_CLOSE = 33
    B_ZERO = 34
    B_SET = 35
    B_SETN = 36
    B_FILL = 37
    B_GEN = 38
    DUMP_OSC = 39
    C_GET = 40
    C_GETN = 41
    B_GET = 42
    B_GETN = 43
    S_GET = 44
    S_GETN = 45
    N_QUERY = 46
    B_QUERY = 47
    N_MAPN = 48
    S_NOID = 49
    G_DEEP_FREE = 50
    CLEAR_SCHED = 51
    SYNC = 52
    D_FREE = 53
    B_ALLOC_READ_CHANNEL = 54
    B_READ_CHANNEL = 55
    G_DUMP_TREE = 56
    G_QUERY_TREE = 57
    ERROR = 58
    S_NEWARGS = 59
    N_MAPA = 60
    N_MAPAN = 61
    N_ORDER = 62
    P_NEW = 63

