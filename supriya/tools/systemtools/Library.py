# -*- encoding: utf-8 -*-
import fnmatch
import os


class Library(object):

    ### SPECIAL METHODS ###

    def __getitem__(self, pattern):
        import supriya
        search_path, pattern = os.path.split(pattern)
        search_path = os.path.expanduser(search_path)
        if not search_path:
            search_path = os.path.join(
                supriya.__path__[0],
                'library',
                )
        elif not os.path.isabs(search_path):
            search_path = os.path.join(
                supriya.__path__[0],
                'library',
                search_path,
                )
        result = []
        result = os.listdir(search_path)
        result = fnmatch.filter(result, pattern)
        result = [os.path.join(search_path, _) for _ in result]
        if len(result) == 1:
            return result[0]
        return result


Library = Library()