import functools
import weakref


class Bindable:

    def __init__(self, func=None, *, rebroadcast=False):
        if func is not None:
            functools.update_wrapper(self, func)
        self.func = func
        self.rebroadcast = bool(rebroadcast)
        self.incoming_bindings = set()
        self.outgoing_bindings = set()
        self.forbid_reentrancy = False
        self.instances = weakref.WeakKeyDictionary()

    def __call__(self, *args, **kwargs):
        if self.func is None:
            return type(self)(
                func=args[0],
                rebroadcast=self.rebroadcast,
                )
        return_value = self.func(*args, **kwargs)
        if return_value is not None:
            with self:
                for binding in self.outgoing_bindings:
                    binding.perform_outgoing(return_value)
                if self.rebroadcast:
                    for binding in self.incoming_bindings:
                        binding.perform_incoming(return_value)
        return return_value

    def __get__(self, instance, class_=None):
        #print('GET', type(self).__name__, instance, class_.__name__, self.func)
        if instance is None:
            #print('    CLS')
            return self
        elif instance in self.instances:
            #print('    OLD', instance, instance.func)
            return self.instances[instance]
        instance_method = self.func.__get__(instance, class_)
        instance_decorator = self.__class__(
            instance_method,
            rebroadcast=self.rebroadcast,
            )
        self.instances[instance] = instance_decorator
        #print('    NEW', instance, instance.func)
        return instance_decorator

    def __enter__(self):
        self.forbid_reentrancy = True

    def __exit__(self, *args):
        self.forbid_reentrancy = False
