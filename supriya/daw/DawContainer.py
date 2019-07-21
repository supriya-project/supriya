import contextlib

from uqbar.containers import UniqueTreeList

from .DawNode import DawNode


class DawContainer(DawNode, UniqueTreeList):
    """
    A DAW node container.
    """

    ### INITIALIZER ###

    def __init__(self):
        DawNode.__init__(self)
        UniqueTreeList.__init__(self)

    ### PRIVATE METHODS ###

    def _collect_roots(self, new_items, old_items, prototype=None):
        roots = set()
        for parent in reversed(self.parentage):
            if not prototype or isinstance(parent, prototype):
                roots.add(parent)
                break
        for new_item in new_items:
            for parent in reversed(new_item.parentage):
                if not prototype or isinstance(parent, prototype):
                    roots.add(parent)
                    break
        for old_item in old_items:
            if old_item in new_items:
                continue
            for parent in reversed(old_item.parentage):
                if not prototype or isinstance(parent, prototype):
                    roots.add(parent)
                    break
        return roots

    def _insertion_hook(self, new_items, start_index, stop_index):
        self.node[start_index:stop_index] = [
            _.node for _ in new_items if _.node is not None
        ]

    def _post_insertion_hook(self, new_items, old_items, alloc_nodes, nonalloc_nodes):
        if not self.server:
            return
        for node in alloc_nodes:
            node._post_allocate()
        for node in nonalloc_nodes:
            node._reallocate()
        for node in old_items:
            if node not in new_items:
                node._free()

    def _pre_insertion_hook(self, new_items, old_items):
        alloc_nodes, nonalloc_nodes = [], []
        if self.server:
            for node in new_items:
                if node._pre_allocate(self._server):
                    alloc_nodes.append(node)
                else:
                    nonalloc_nodes.append(node)
        else:
            for node in new_items:
                node._free()
        return alloc_nodes, nonalloc_nodes

    def _process_roots(self, roots):
        pass

    def _set_items(self, new_items, old_items, start_index, stop_index):
        self._debug_tree("Setting")
        with contextlib.ExitStack() as exit_stack:
            applications = set()
            for item in new_items + old_items + [self]:
                application = item.application
                if application is not None:
                    applications.add(application)
            for application in applications:
                self._debug_tree("Locking")
                exit_stack.enter_context(application._lock)
            roots = self._collect_roots(old_items, new_items)
            UniqueTreeList._set_items(
                self, new_items, old_items, start_index, stop_index
            )
            self._process_roots(roots)
            alloc_nodes, nonalloc_nodes = self._pre_insertion_hook(new_items, old_items)
            self._insertion_hook(new_items, start_index, stop_index)
            self._post_insertion_hook(new_items, old_items, alloc_nodes, nonalloc_nodes)
