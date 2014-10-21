# -*- encoding: utf-8 -*-
import os


class Media(object):

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        import supriya
        return os.path.abspath(
            os.path.join(
                supriya.__path__[0],
                'media',
                str(item),
                )
            )


Media = Media()