# -*- encoding: utf-8 -*-
import threading
import time
try:
    import queue
except ImportError:
    import Queue as queue


class NonBlockingStreamReader(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_queue',
        '_reading',
        '_stream',
        '_thread',
        )

    ### INITIALIZER ###

    def __init__(self, stream):
        self._reading = False
        self._stream = stream
        self._queue = queue.Queue()
        self._thread = None

    ### SPECIAL METHODS ###

    def __enter__(self):
        self._thread = threading.Thread(
            target=self._populate_queue,
            args=(self._stream, self._queue),
            )
        self._reading = True
        #self._thread.daemon = True
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._reading = False
        self._thread.join()

    ### PRIVATE METHODS ###

    def _populate_queue(self, stream, queue):
        while self._reading:
            line = stream.readline()
            if line:
                queue.put(line)
            else:
                raise UnexpectedEndOfStream
            time.sleep(0.01)

    ### PUBLIC METHODS ###

    def readline(self, timeout=None):
        result = None
        try:
            should_block = timeout is not None
            result = self._queue.get(
                block=should_block,
                timeout=timeout,
                )
        except queue.Empty:
            pass
        return result


class UnexpectedEndOfStream(Exception):
    pass