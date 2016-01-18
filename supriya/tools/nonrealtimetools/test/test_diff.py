

def p2c_to_c2p(p2c):
    c2p = {}
    nodes_needing_parents = list(p2c)
    for parent, children in p2c.items():
        if not children:
            continue
        for child in children:
            c2p[child] = parent
            nodes_needing_parents.remove(child)
    assert len(nodes_needing_parents) == 1
    c2p[nodes_needing_parents[0]] = None
    return c2p


def test_diff_01():

    source_p2c = {
        'A': ('B', 'C', 'D'),
        'B': ('E', 'F'),
        'C': None,
        'D': ('G', 'H'),
        'E': ('I',),
        'F': ('J',),
        'G': None,
        'H': None,
        'I': None,
        'J': None,
        }
    source_c2p = p2c_to_c2p(source_p2c)

    target_p2c = {
        'A': ('K', 'D', 'B'),
        'B': ('M', 'N'),
        'C': None,
        'D': ('G',),
        'G': ('H',),
        'H': None,
        'J': None,
        'K': ('J', 'L'),
        'L': None,
        'M': ('C',),
        'N': None,
        }
    target_c2p = p2c_to_c2p(target_p2c)

    initial_node = 'A'

    requests = []

    def recurse(parent, children):
        if parent not in target_p2c:
            request = ('free', parent)
        
