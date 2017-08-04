import itertools


def iterate_nwise(iterable, n=2):
    iterables = itertools.tee(iterable, n)
    temp = []
    for idx, it in enumerate(iterables):
        it = itertools.islice(it, idx, None)
        temp.append(it)
    return zip(*temp)
