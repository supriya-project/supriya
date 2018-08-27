import abc
import collections
import supriya
import uqbar.strings


class UGenMeta(abc.ABCMeta):

    def __new__(metaclass, class_name, bases, namespace):
        ordered_input_names = namespace.get('_ordered_input_names')
        unexpanded_input_names = namespace.get('_unexpanded_input_names', ())
        valid_calculation_rates = namespace.get('_valid_calculation_rates', ())
        (
            has_channel_count,
            has_settable_channel_count,
        ) = UGenMeta.get_channel_count(namespace, bases)
        if isinstance(ordered_input_names, collections.OrderedDict):
            for name in ordered_input_names:
                if name in namespace:
                    continue
                namespace[name] = UGenMeta.make_property(
                    ugen_name=class_name,
                    input_name=name,
                    unexpanded=name in unexpanded_input_names,
                )
            if '__init__' not in namespace:
                function, string = UGenMeta.make_initializer(
                    bases=bases,
                    parameters=ordered_input_names.copy(),
                    has_calculation_rate=bool(valid_calculation_rates),
                    has_channel_count=has_channel_count,
                    has_settable_channel_count=has_settable_channel_count,
                )
                namespace['__init__'] = function
                namespace['_init_source'] = string
            constructor_rates = {}
            if valid_calculation_rates:
                for rate in valid_calculation_rates:
                    if rate.token in namespace:
                        continue
                    constructor_rates[rate.token] = rate
            elif 'new' not in namespace:
                constructor_rates['new'] = None
            for name, rate in constructor_rates.items():
                function, string = UGenMeta.make_constructor(
                    ugen_name=class_name,
                    rate=rate,
                    parameters=ordered_input_names.copy(),
                    has_channel_count=has_channel_count,
                    has_settable_channel_count=has_settable_channel_count,
                )
                namespace[name] = function
                namespace['_{}_source'.format(name)] = string
        return super().__new__(metaclass, class_name, bases, namespace)

    initializer_template = uqbar.strings.normalize('''
    def __init__(
        self,
        {parameters_indent_one}
    ):
        {base_class_name}.__init__(
            self,
            {parameters_indent_two}
            )
    ''')

    constructor_template = uqbar.strings.normalize('''
    @classmethod
    def {rate_token}(
        cls,
        {parameters_indent_one}
    ):
        """
        Constructs a {rate_name_lower}-rate ``{ugen_name}`` unit generator graph.

        Returns unit generator graph.
        """
        calculation_rate = supriya.CalculationRate.{rate_name_upper}
        return cls._new_expanded(
            calculation_rate=calculation_rate,
            {parameters_indent_two}
        )
    ''')

    rateless_constructor_template = uqbar.strings.normalize('''
    @classmethod
    def new(
        cls,
        {parameters_indent_one}
    ):
        """
        Constructs a ``{ugen_name}`` unit generator graph.

        Returns unit generator graph.
        """
        return cls._new_expanded(
            {parameters_indent_two}
        )
    ''')

    @staticmethod
    def get_channel_count(namespace, bases):
        has_channel_count = namespace.get('_has_channel_count')
        if has_channel_count is None:
            for base in bases:
                has_channel_count = getattr(base, '_has_channel_count')
                if has_channel_count is not None:
                    break
        has_settable_channel_count = namespace.get('_has_settable_channel_count')
        if has_settable_channel_count is None:
            for base in bases:
                has_settable_channel_count = getattr(base, '_has_settable_channel_count')
                if has_settable_channel_count is not None:
                    break
        return has_channel_count, has_settable_channel_count

    @staticmethod
    def make_initializer(
        bases,
        parameters,
        has_calculation_rate=True,
        has_channel_count=False,
        has_settable_channel_count=False,
    ):
        if has_calculation_rate:
            new_parameters = collections.OrderedDict([
                ('calculation_rate', None),
            ])
            new_parameters.update(parameters)
            parameters = new_parameters
        if has_channel_count and has_settable_channel_count:
            parameters['channel_count'] = int(has_channel_count)
        parameters_indent_one = '\n    '.join([
            '{}={},'.format(key, value)
            for key, value in parameters.items()
        ]).replace(
            '=inf,', "=float('inf'),"
        ).replace(
            '=-inf,', "=float('-inf'),"
        )
        if has_channel_count:
            if not has_settable_channel_count:
                parameters['channel_count'] = int(has_channel_count)
            else:
                parameters['channel_count'] = 'channel_count'
        parameters_indent_two = '\n        '.join([
            '{}={},'.format(key, value if key == 'channel_count' else key)
            for key, value in parameters.items()
        ])
        string = UGenMeta.initializer_template.format(
            base_class_name=bases[0].__name__,
            parameters_indent_one=parameters_indent_one,
            parameters_indent_two=parameters_indent_two,
        )
        namespace = {}
        namespace[bases[0].__name__] = bases[0]
        try:
            exec(string, namespace, namespace)
        except Exception:
            print(string)
            raise
        function = namespace['__init__']
        return function, string

    @staticmethod
    def make_constructor(
        ugen_name,
        rate,
        parameters,
        has_channel_count=False,
        has_settable_channel_count=False,
    ):
        if has_channel_count and has_settable_channel_count:
            parameters['channel_count'] = int(has_channel_count)
        parameters_indent_one = '\n    '.join([
            '{}={},'.format(key, value)
            for key, value in parameters.items()
        ]).replace(
            '=inf,', "=float('inf'),"
        ).replace(
            '=-inf,', "=float('-inf'),"
        )
        parameters_indent_two = '\n        '.join([
            '{}={},'.format(key, key)
            for key, value in parameters.items()
        ])
        kwargs = dict(
            parameters_indent_one=parameters_indent_one,
            parameters_indent_two=parameters_indent_two,
            ugen_name=ugen_name,
        )
        if rate is None:
            string = UGenMeta.rateless_constructor_template.format(**kwargs)
        else:
            kwargs.update(
                rate_name_lower=rate.name.lower(),
                rate_name_upper=rate.name,
                rate_token=rate.token,
            )
            string = UGenMeta.constructor_template.format(**kwargs)
        namespace = {'supriya': supriya}
        try:
            exec(string, namespace, namespace)
        except Exception:
            print(string)
            raise
        if rate is None:
            return namespace['new'], string
        function = namespace[rate.token]
        return function, string

    @staticmethod
    def make_property(ugen_name, input_name, unexpanded=False):
        doc = uqbar.strings.normalize('''
        Gets ``{input_name}`` of ``{ugen_name}``.

        Returns input.
        ''').format(ugen_name=ugen_name, input_name=input_name)
        if unexpanded:
            def getter(object_):
                index = tuple(object_._ordered_input_names).index(input_name)
                return tuple(object_._inputs[index:])
        else:
            def getter(object_):
                index = tuple(object_._ordered_input_names).index(input_name)
                return object_._inputs[index]
        return property(fget=getter, doc=doc)
