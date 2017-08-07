import sys


class RedirectedStreams:
    """
    A context manager for capturing stdout and stderr output.

    ..  container:: example

        ::

            >>> from io import StringIO
            >>> string_io = StringIO()
            >>> with supriya.RedirectedStreams(stdout=string_io):
            ...     print("hello, world!")
            ...

        ::

            >>> result = string_io.getvalue()
            >>> string_io.close()
            >>> print(result)
            hello, world!

    """

    ### INITIALIZER ###

    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    ### SPECIAL METHODS ###

    def __enter__(self):
        self._old_stdout, self._old_stderr = sys.stdout, sys.stderr
        self._old_stdout.flush()
        self._old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self._stdout.flush()
            self._stderr.flush()
        finally:
            sys.stdout = self._old_stdout
            sys.stderr = self._old_stderr

    ### PUBLIC PROPERTIES ###

    @property
    def stderr(self):
        return self._stderr

    @property
    def stdout(self):
        return self._stdout
