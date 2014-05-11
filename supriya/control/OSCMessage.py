import math
import struct


class OSCMessage(object):
    '''An OSC message:

    ::

        >>> import supriya

    ::

        >>> message = supriya.osc.OSCMessage()
        >>> message.address = '/foo/bar/baz'
        >>> message.append(42)
        >>> message.append('quux')
        >>> message.extend(('i would die 4 u', 3.14159))

    ::

        >>> encoded_message = message.encode()

    ::

        >>> decoded_message = message.decode(encoded_message)
        >>> for x in decoded_message: 
        ...     x # doctest: +ELLIPSIS
        ...
        '/foo/bar/baz'
        42
        'quux'
        'i would die 4 u'
        3.14159...

    Also supports OSC blobs:

    ::

        >>> message = supriya.osc.OSCMessage(address='/nothing')                                  
        >>> message.append('', type_hint='b')                                                  
        >>> message.append('x', type_hint='b')                                                 
        >>> message.append('xx', type_hint='b')                                                
        >>> message.append('xxy', type_hint='b')                                               
        >>> message.append('xxyy', type_hint='b')                                              
        >>> message.append('xxyyx', type_hint='b')                                             
        >>> message.append('xxyyxx', type_hint='b')                                             
        >>> message.append(42)

    ::

        >>> encoded_message = message.encode()

    ::

        >>> decoded_message = message.decode(encoded_message)
        >>> for x in decoded_message:
        ...     x
        ...
        '/nothing'
        ''
        'x'
        'xx'
        'xxy'
        'xxyy'
        'xxyyx'
        'xxyyxx'
        42

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_address',
        '_message',
        '_type_tags',
        )

    _valid_type_tags = (
        ',',
        'b',
        'd',
        'f',
        'i',
        's',
        )

    ### INITIALIZER ###

    def __init__(self, address='', message=None):
        self._address = address or ''
        self._message = ''
        self._type_tags = ','
        if message is not None:
            self.extend(message)

    ### PRIVATE METHODS ###

    @staticmethod
    def _encode_osc_argument(data):
        type_tag, binary_data = '', ''
        if isinstance(data, (str, unicode)):
            type_tag = 's'
            data = str(data)
            actual_length = len(data)
            padded_length = int(math.ceil((actual_length + 1) / 4.0) * 4)
            binary_format = '>{}s'.format(
                padded_length,
                )
        elif isinstance(data, float):
            type_tag = 'f'
            binary_format = '>f'
        elif isinstance(data, int):
            type_tag = 'i'
            binary_format = '>i'
        else:
            raise Exception('Cannot convert {}'.format(data))
        binary_data = struct.pack(
            binary_format,
            data,
            )
        return type_tag, binary_data

    @staticmethod
    def _encode_osc_blob(data):
        type_tag, binary_data = '', ''
        if isinstance(data, str):
            actual_length = len(data)
            padded_length = int(math.ceil(actual_length / 4.0) * 4)
            binary_format = '>i{}s'.format(padded_length)
            binary_data = struct.pack(
                binary_format,
                actual_length,
                data,
                )
            type_tag = 'b'
        return type_tag, binary_data

    @staticmethod
    def _read_blob(data):
        length = struct.unpack('>i', data[:4])[0]
        next_data = int(math.ceil(length / 4.0) * 4) + 4
        result = data[4:length + 4]
        remainder = data[next_data:]
        return result, remainder
    
    @staticmethod
    def _read_double(data):
        result = float(struct.unpack('>d', data[:8])[0])
        remainder = data[8:]
        return result, remainder

    @staticmethod
    def _read_float(data):
        if len(data) < 4:
            result = 0.
            remainder = data
        else:
            result = struct.unpack('>f', data[:4])[0]
            remainder = data[4:]
        return result, remainder

    @staticmethod
    def _read_int(data):
        if len(data) < 4:
            result = 0
            remainder = data
        else:
            result = int(struct.unpack('>i', data[:4])[0])
            remainder = data[4:]
        return result, remainder

    @staticmethod
    def _read_long(data):
        high, low = struct.unpack('>ll', data[:8])
        result = (long(high) << 32) + low
        remainder = data[8:]
        return result, remainder

    @staticmethod
    def _read_string(data):
        length = data.find('\0')
        next_data = int(math.ceil((length + 1) / 4.0) * 4)
        result = data[:length]
        remainder = data[next_data:]
        return result, remainder

    ### PUBLIC PROPERTIES ###

    @apply
    def address():
        def fget(self):
            return self._address
        def fset(self, expr):
            self._address = str(expr)
        return property(**locals())

    @apply
    def message():
        def fget(self):
            return self._message
        def fset(self, expr):
            self._message = str(expr)
        return property(**locals())

    @apply
    def type_tags():
        def fget(self):
            return self._type_tags
        def fset(self, expr):
            assert all(x in self._valid_type_tags for x in expr), expr
            self._type_tags = str(expr)
        return property(**locals())

    ### PUBLIC METHODS ###

    def append(self, expr, type_hint=None):
        if type_hint == 'b':
            type_tag, binary_data = self._encode_osc_blob(expr)
        else:
            type_tag, binary_data = self._encode_osc_argument(expr)
        self.type_tags += type_tag
        self.message += binary_data

    def clear(self):
        self.address = ''
        self.message = ''
        self.type_tags = ','

    @staticmethod
    def decode(data):
        type_tag_converters = {
            'b': OSCMessage._read_blob,
            'd': OSCMessage._read_double,
            'f': OSCMessage._read_float,
            'i': OSCMessage._read_int,
            's': OSCMessage._read_string,
            }
        arguments, type_tags = [], ''
        address, remainder = OSCMessage._read_string(data)
        if address == '#bundle':
            time, remainder = OSCMessage._read_long(rest)
            while 0 < len(remainder):
                length, remainder = OSCMessage._read_int(remainder)
                arguments.append(
                    OSCMessage.decode(remainder[:length]),
                    )
                remainder = remainder[length:]
        elif 0 < len(remainder):
            type_tags, remainder = OSCMessage._read_string(remainder)
            if type_tags[0] == ',':
                for tag in type_tags[1:]:
                    value, remainder = type_tag_converters[tag](remainder)
                    arguments.append(value)
        return [address] + arguments
 
    def encode(self):
        encoded_address = self._encode_osc_argument(self.address)[1]
        encoded_type_tags = self._encode_osc_argument(self.type_tags)[1]
        return '{}{}{}'.format(
            encoded_address,
            encoded_type_tags,
            self.message,
            )
                       
    def extend(self, expr):
        for x in expr:
            self.append(x)
