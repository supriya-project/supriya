import collections

from supriya.system import BindableFloat


class BindableNamespace(collections.Mapping):

    # TODO: Support key-adding __setitem__, and __delitem__.
    #       Unbind bindings on __delitem__.

    class ProxyProxy:
        def __init__(self, namespace):
            self.namespace = namespace

        def __getattr__(self, key):
            return self.namespace._proxies[key]

        def __getitem__(self, key):
            return self.namespace._proxies[key]

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        namespace = dict(*args, **kwargs)
        self._proxies = {}
        for key, value in namespace.items():
            self._proxies[key] = BindableFloat(value)

    ### SPECIAL METHODS ###

    def __getitem__(self, key):
        return self._proxies[key].value

    def __len__(self):
        return len(self._proxies)

    def __iter__(self):
        return iter(self._proxies)

    def __setitem__(self, key, value):
        self._proxies[key](value)

    ### PUBLIC PROPERTIES ###

    @property
    def proxies(self):
        return self.ProxyProxy(self)
