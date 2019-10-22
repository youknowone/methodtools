from methodtools import lru_cache, _functools_lru_cache


def test_lru_cache():

    @_functools_lru_cache(maxsize=4)
    def ff(v):
        return 0 + v

    @lru_cache(maxsize=4)
    def f(v):
        return 1000 + v

    class C(object):

        base = 3000

        def __init__(self):
            self.base = 2000

        @lru_cache(maxsize=4)
        def m(self, v):
            return self.base + v

        @lru_cache(maxsize=4)
        @classmethod
        def c(cls, v):
            return cls.base + v

        @lru_cache(maxsize=4)
        @staticmethod
        def s(v):
            return 4000 + v

    c = C()
    assert f.cache_info() == ff.cache_info()
    assert c.m.cache_info() == ff.cache_info()
    assert C.c.cache_info() == ff.cache_info()
    assert c.c.cache_info() == ff.cache_info()
    assert C.s.cache_info() == ff.cache_info()
    assert c.s.cache_info() == ff.cache_info()

    ff(1)
    assert f.cache_info() != ff.cache_info()

    assert f(1) == 1001
    assert c.m(1) == 2001
    assert C.c(1) == 3001
    assert c.c(1) == 3001
    assert C.s(1) == 4001
    assert c.s(1) == 4001

    assert f.cache_info() == ff.cache_info()
    assert c.m.cache_info() == ff.cache_info()
    assert C.c.cache_info().hits == 1
    assert c.c.cache_info().hits == 1
    assert C.s.cache_info().hits == 1
    assert c.s.cache_info().hits == 1

    ff.cache_clear()
    assert f.cache_info() != ff.cache_info()

    f.cache_clear()
    c.m.cache_clear()
    C.c.cache_clear()
    c.c.cache_clear()
    C.s.cache_clear()
    c.s.cache_clear()

    assert f.cache_info() == ff.cache_info()
    assert c.m.cache_info() == ff.cache_info()
    assert C.c.cache_info() == ff.cache_info()
    assert c.c.cache_info() == ff.cache_info()
    assert C.s.cache_info() == ff.cache_info()
    assert c.s.cache_info() == ff.cache_info()

    o1 = C()
    o2 = C()
    o1.m(1)
    assert o1.m.__call__ != o2.m.__call__
    assert o1.m.cache_info().misses == 1
    assert o2.m.cache_info().misses == 0

    o1.c(1)
    assert o1.c.__call__ == o2.c.__call__
    assert o1.c.cache_info().misses == 1
    assert o2.c.cache_info().misses == 1

    o1.s(1)
    assert o1.s.__call__ == o2.s.__call__
    assert o1.s.cache_info().misses == 1
    assert o2.s.cache_info().misses == 1

    assert f(2) == 1002
    assert c.m(2) == 2002
    assert C.c(2) == 3002
    assert c.c(2) == 3002
    assert C.s(2) == 4002
    assert c.s(2) == 4002
