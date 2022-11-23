from typing import Optional

import hypothesis
import hypothesis.strategies as st

hp_global_settings = hypothesis.settings()


def get_control_test_groups(min_size: int = 1, max_size: Optional[int] = None):
    def _wrapper(func):
        def _st_func(*args, **kwargs):
            strategy = func(*args, **kwargs)
            return st.tuples(
                st.lists(strategy, min_size=min_size, max_size=max_size),
                st.lists(strategy, min_size=min_size, max_size=max_size),
            )

        return _st_func

    return _wrapper
