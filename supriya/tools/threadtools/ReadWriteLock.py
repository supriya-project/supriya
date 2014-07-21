import threading


class ReadWriteLock(object):
    r'''Non-reentrant write-preferring read/write lock.'''

    ### CLASS VARIABLES ###

    DEBUG = False

    __slots__ = ()

    class _ReadAccess:

        def __init__(self, rwlock):
            self.rwlock = rwlock

        def __enter__(self):
            self.rwlock.acquire_read()
            return self.rwlock

        def __exit__(self, type, value, tb):
            self.rwlock.release_read()

    class _WriteAccess:

        def __init__(self, rwlock):
            self.rwlock = rwlock

        def __enter__(self):
            self.rwlock.acquire_write()
            return self.rwlock

        def __exit__(self, type, value, tb):
            self.rwlock.release_write()

    ### INITIALIZER ###

    def __init__(self):
        self.lock = threading.Lock()
        self.active_writer_lock = threading.Lock()
        self.writer_count = 0
        self.waiting_reader_count = 0
        self.active_reader_count = 0
        self.readers_finished_condition = threading.Condition(self.lock)
        self.writers_finished_condition = threading.Condition(self.lock)
        self.read_access = self._ReadAccess(self)
        self.write_access = self._WriteAccess(self)
        if self.DEBUG:
            self.active_readers = set()
            self.active_writer = None

    def acquire_read(self):
        with self.lock:
            if self.DEBUG:
                current_thread = threading.current_thread()
                assert current_thread not in self.active_readers
                assert current_thread != self.active_writer
                self.active_readers.add(current_thread)
            if self.writer_count:
                self.waiting_reader_count += 1
                self.writers_finished_condition.wait()
                while self.writer_count:
                    self.writers_finished_condition.wait()
                self.waiting_reader_count -= 1
            self.active_reader_count += 1

    def release_read(self):
        with self.lock:
            if self.DEBUG:
                current_thread = threading.current_thread()
                assert current_thread in self.active_readers
                self.active_readers.remove(current_thread)
            assert self.active_reader_count > 0
            self.active_reader_count -= 1
            if not self.active_reader_count and self.writer_count:
                self.readers_finished_condition.notify_all()

    def acquire_write(self):
        with self.lock:
            if self.DEBUG:
                current_thread = threading.current_thread()
                assert current_thread not in self.active_readers
                assert current_thread != self.active_writer
            self.writer_count += 1
            if self.active_reader_count:
                self.readers_finished_condition.wait()
                while self.active_reader_count:
                    self.readers_finished_condition.wait()

        self.active_writer_lock.acquire()
        if self.DEBUG:
            self.active_writer = current_thread

    def release_write(self):
        if not self.DEBUG:
            self.active_writer_lock.release()
        with self.lock:
            if self.DEBUG:
                current_thread = threading.current_thread()
                assert current_thread == self.active_writer
                self.active_writer = None
                self.active_writer_lock.release()
            assert self.writer_count > 0
            self.writer_count -= 1
            if not self.writer_count and self.waiting_reader_count:
                self.writers_finished_condition.notify_all()

    def get_state(self):
        with self.lock:
            return (
                self.writer_count,
                self.waiting_reader_count,
                self.active_reader_count,
                )