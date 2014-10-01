

class Wrapper(dict):
    """
    A Wrapper object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.
        >>> o = Wrapper(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'
    """

    def override(self, other):
        def override(a, b):
            keys = b.keys()
            for key in keys:
                o = b[key]
                if isinstance(o, dict) is True:
                    try:
                        i = a[key]
                        for k in o.keys():
                            i[k] = o[k]
                    except KeyError:
                        a[key] = o
                else:
                    a[key] = o

        override(self, other)
        return self

    def __getattr__(self, key):
        try:
            o = self[key]
            if isinstance(o, dict) is True:
                if isinstance(o, Wrapper) is False:
                    o = Wrapper.create(o)
                    self[key] = o
            return o
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            pass

    def reduce(self, fn=None):
        obj = {}
        keys = self.keys()
        for key in keys:
            v = self[key]
            if isinstance(v, list) and len(v) > 0 and hasattr(v[0], "reduce"):
                for x in xrange(len(v)):
                    v[x] = v[x].reduce()

            obj[key] = v
        if fn:
            return fn(obj)
        return obj

    def clone(self):
        return Wrapper(self.copy())

    def __repr__(self):
        return '<Wrapper ' + dict.__repr__(self) + '>'

    @staticmethod
    def create(*args, **kwargs):
        if args and len(args) > 0:
            return Wrapper(args[0])
        return Wrapper(kwargs)