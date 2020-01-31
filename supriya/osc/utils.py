import contextlib
import socket

from supriya import utils


def find_free_port():
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def format_datagram(datagram):
    result = []
    result.append("size {}".format(len(datagram)))
    index = 0
    while index < len(datagram):
        chunk = datagram[index : index + 16]
        line = "{: >4}   ".format(index)
        hex_blocks = []
        ascii_block = ""
        for chunk in utils.group_iterable_by_count(chunk, 4):
            hex_block = []
            for byte in chunk:
                char = int(byte)
                if 31 < char < 127:
                    char = chr(char)
                else:
                    char = "."
                ascii_block += char
                hexed = hex(byte)[2:].zfill(2)
                hex_block.append(hexed)
            hex_block = " ".join(hex_block)
            hex_blocks.append(hex_block)
        hex_blocks = "  ".join(hex_blocks)
        ascii_block = "|{}|".format(ascii_block)
        hex_blocks = "{: <53}".format(hex_blocks)
        line += hex_blocks
        line += ascii_block
        result.append(line)
        index += 16
    result = "\n".join(result)
    return result
