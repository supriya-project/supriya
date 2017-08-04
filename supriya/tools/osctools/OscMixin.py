import abc
from supriya import utils
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class OscMixin(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __str__(self):
        """
        Gets string representation of OSC object.

        ::

            size 164
               0   2f 64 5f 72  65 63 76 00  2c 62 62 00  00 00 00 6b   |/d_recv.,bb....k|
              16   53 43 67 66  00 00 00 02  00 01 04 74  65 73 74 00   |SCgf.......test.|
              32   00 00 02 43  dc 00 00 00  00 00 00 00  00 00 00 00   |...C............|
              48   00 00 00 00  00 00 02 06  53 69 6e 4f  73 63 02 00   |........SinOsc..|
              64   00 00 02 00  00 00 01 00  00 ff ff ff  ff 00 00 00   |................|
              80   00 ff ff ff  ff 00 00 00  01 02 03 4f  75 74 02 00   |...........Out..|
              96   00 00 02 00  00 00 00 00  00 ff ff ff  ff 00 00 00   |................|
             112   01 00 00 00  00 00 00 00  00 00 00 00  00 00 00 24   |...............$|
             128   2f 73 5f 6e  65 77 00 00  2c 73 69 69  69 00 00 00   |/s_new..,siii...|
             144   74 65 73 74  00 00 00 00  00 00 03 e9  00 00 00 00   |test............|
             160   00 00 00 01                                          |....|

        """
        datagram = bytearray(self.to_datagram())
        return self.format_datagram(datagram)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def to_datagram(self):
        raise NotImplementedError

    @classmethod
    def format_datagram(cls, datagram):
        result = []
        result.append('size {}'.format(len(datagram)))
        index = 0
        while index < len(datagram):
            chunk = datagram[index:index + 16]
            line = '{: >4}   '.format(index)
            hex_blocks = []
            ascii_block = ''
            for chunk in utils.group_iterable_by_count(chunk, 4):
                hex_block = []
                for byte in chunk:
                    char = int(byte)
                    if 31 < char < 127:
                        char = chr(char)
                    else:
                        char = '.'
                    ascii_block += char
                    hexed = hex(byte)[2:].zfill(2)
                    hex_block.append(hexed)
                hex_block = ' '.join(hex_block)
                hex_blocks.append(hex_block)
            hex_blocks = '  '.join(hex_blocks)
            ascii_block = '|{}|'.format(ascii_block)
            hex_blocks = '{: <53}'.format(hex_blocks)
            line += hex_blocks
            line += ascii_block
            result.append(line)
            index += 16
        result = '\n'.join(result)
        return result
