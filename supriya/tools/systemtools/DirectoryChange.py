import os


class DirectoryChange:
    """
    A context manager for temporarily changing the current working directory.
    """

    ### INITIALIZER ###

    def __init__(self, directory=None, verbose=None):
        if directory is None:
            pass
        elif os.path.isdir(directory):
            pass
        elif os.path.isfile(directory):
            directory = os.path.dirname(directory)
        self._directory = directory
        self._original_directory = None
        if verbose is not None:
            verbose = bool(verbose)
        self._verbose = bool(verbose)

    ### SPECIAL METHODS ###

    def __enter__(self):
        self._original_directory = os.getcwd()
        if self._directory is not None:
            os.chdir(self.directory)
            if self.verbose:
                message = 'Changing directory to {} ...'
                message = message.format(self.directory)
                print(message)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._directory is not None:
            os.chdir(self._original_directory)
            if self.verbose:
                message = 'Returning to {} ...'
                message = message.format(self.original_directory)
                print(message)
        self._original_directory = None

    ### PUBLIC PROPERTIES ###

    @property
    def directory(self):
        return self._directory

    @property
    def original_directory(self):
        return self._original_directory

    @property
    def verbose(self):
        return self._verbose
