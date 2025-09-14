from uuid import UUID

from uqbar.objects import get_vars, new

from supriya.patterns.events import CompositeEvent, Event


def sanitize_id(id_: UUID, cache: dict[UUID, UUID]) -> UUID:
    if id_ not in cache:
        cache[id_] = UUID(int=len(cache))
    return cache[id_]


def sanitize_event(event: Event, cache: dict[UUID, UUID]) -> Event:
    if isinstance(event, CompositeEvent):
        return new(event, events=[sanitize_event(x, cache) for x in event.events])
    sanitize_data = {}
    args, _, kwargs = get_vars(event)
    for key, value in args.items():
        if isinstance(value, UUID):
            value = sanitize_id(value, cache)
        sanitize_data[key] = value
    for key, value in sorted(kwargs.items()):
        if isinstance(value, UUID):
            value = sanitize_id(value, cache)
        sanitize_data[key] = value
    return type(event)(**sanitize_data)


def sanitize(exprs):
    cache = {}
    sanitized = []
    for expr in exprs:
        if isinstance(expr, Event):
            sanitized.append(sanitize_event(expr, cache))
        else:
            sanitized.append(expr)
    return sanitized


def run_pattern_test(pattern, expected, is_infinite, stop_at):
    assert pattern.is_infinite == is_infinite
    iterator = iter(pattern)
    actual = []
    ceased = True
    for iteration in range(1000):
        try:
            if stop_at == iteration:
                expr = iterator.send(True)
            else:
                expr = next(iterator)
            actual.append(expr)
        except StopIteration:
            break
    else:
        ceased = False
    if is_infinite:
        assert not ceased
        sanitized_actual = sanitize(actual[: len(expected)])
    else:
        sanitized_actual = sanitize(actual)
    assert sanitized_actual == expected, sanitized_actual
