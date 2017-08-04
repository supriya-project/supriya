import itertools


def group_iterable_by_count(iterable, count):
    iterator = iter(iterable)
    while True:
        group = list(itertools.islice(iterator, count))
        if not group:
            return
        yield group
