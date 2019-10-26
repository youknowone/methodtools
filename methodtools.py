import functools
from wirerope import Wire, WireRope

__version__ = '0.1.2'
__all__ = 'lru_cache',


if hasattr(functools, 'lru_cache'):
    _functools_lru_cache = functools.lru_cache
else:
    try:
        import functools32
    except ImportError:
        # raise AttributeError about fallback failure
        functools.lru_cache  # install `functools32` to run on py2
    else:
        _functools_lru_cache = functools32.lru_cache


class _LruCacheWire(Wire):

    def __init__(self, rope, *args, **kwargs):
        super(_LruCacheWire, self).__init__(rope, *args, **kwargs)
        lru_args, lru_kwargs = rope._args
        wrapper = _functools_lru_cache(
            *lru_args, **lru_kwargs)(self.__func__)
        self.__call__ = wrapper
        self.cache_clear = wrapper.cache_clear
        self.cache_info = wrapper.cache_info

    def __call__(self, *args, **kwargs):
        # descriptor detection support - never called
        return self.__call__(*args, **kwargs)


@functools.wraps(_functools_lru_cache)
def lru_cache(*args, **kwargs):
    return WireRope(_LruCacheWire, wraps=True, rope_args=(args, kwargs))
