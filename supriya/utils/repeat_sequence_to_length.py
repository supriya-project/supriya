import itertools


def repeat_sequence_to_length(sequence, length):
    for i, x in enumerate(itertools.cycle(sequence)):
        if i >= length:
            break
        yield x
