import fnmatch
import os


class Assets:

    ### SPECIAL METHODS ###

    def __getitem__(self, pattern):
        import supriya
        search_path, pattern = os.path.split(pattern)
        search_path = os.path.expanduser(search_path)
        if not search_path:
            search_path = os.path.join(
                supriya.__path__[0],
                'assets',
                )
        elif not os.path.isabs(search_path):
            search_path = os.path.join(
                supriya.__path__[0],
                'assets',
                search_path,
                )
        result = []
        result = os.listdir(search_path)
        result = fnmatch.filter(result, pattern)
        result = [os.path.join(search_path, _) for _ in result]
        if len(result) == 1:
            return result[0]
        return result


Assets = Assets()
