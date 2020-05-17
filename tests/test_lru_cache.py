from methodtools import lru_cache, _functools_lru_cache


def test_lru_cache():

    @_functools_lru_cache(maxsize=4)
    def ff(v):
        """ff is a functools lru function"""
        return 0 + v

    assert ff.__doc__ == """ff is a functools lru function"""

    @lru_cache(maxsize=4)
    def f(v):
        """f is a methodtools lru function"""
        return 1000 + v

    assert f.__doc__ == """f is a methodtools lru function"""

    class C(object):

        base = 3000
        count = 300

        def __init__(self):
            self.base = 2000
            self.count = 200

        @lru_cache(maxsize=4)
        def m(self, v):
            """m"""
            self.count += 1
            return self.base + v
        assert m.__doc__ == 'm'

        @lru_cache(maxsize=4)
        @classmethod
        def c(cls, v):
            """c"""
            cls.count += 1
            return cls.base + v
        assert c.__doc__ == 'c'

        @lru_cache(maxsize=4)
        @staticmethod
        def s(v):
            """s"""
            C.count += 1
            return 4000 + v
        assert s.__doc__ == 's'

        @lru_cache(maxsize=1)
        @property
        def p(self):
            """p"""
            self.count += 1
            return self.base
        assert p.__doc__ == 'p'

    assert C.m.__doc__ == 'm'
    assert C.c.__doc__ == 'c'
    assert C.s.__doc__ == 's'

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
    assert c.p == 2000

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
    assert o1.count == o2.count
    o1.m(1)
    assert o1.m.__call__ != o2.m.__call__
    assert o1.m.cache_info().misses == 1
    assert o2.m.cache_info().misses == 0
    assert o1.count != o2.count
    o2.m(1)
    assert o1.count == o2.count
    o2.m(1)
    assert o1.count == o2.count

    base_count = C.count
    o1.c(1)
    assert C.count == base_count + 1
    assert o1.c.__call__ == o2.c.__call__
    assert o1.c.cache_info().misses == 1
    assert o2.c.cache_info().misses == 1
    o2.c(1)
    C.c(1)
    assert C.count == base_count + 1

    base_count = C.count
    o1.s(1)
    assert C.count == base_count + 1
    assert o1.s.__call__ == o2.s.__call__
    assert o1.s.cache_info().misses == 1
    assert o2.s.cache_info().misses == 1
    o2.s(1)
    C.s(1)
    assert C.count == base_count + 1

    assert o1.count == o2.count
    o1.p
    assert o1.count != o2.count
    o2.p
    assert o1.count == o2.count
    o2.p
    assert o1.count == o2.count

    assert f(2) == 1002
    assert c.m(2) == 2002
    assert C.c(2) == 3002
    assert c.c(2) == 3002
    assert C.s(2) == 4002
    assert c.s(2) == 4002
