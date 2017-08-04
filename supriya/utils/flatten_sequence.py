import collections


def flatten_sequence(sequence):
    for x in sequence:
        if isinstance(sequence, collections.Iterable):
            yield from flatten_sequence(x)
        else:
            yield x
