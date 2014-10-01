

class Registry:
    __table__ = {}

    @staticmethod
    def register(cls):
        name, meta_type = cls.__name__, None
        try:
            meta_type = cls.__metaclass__.__name__
        except:
            pass

        tbl = Registry.__table__
        tbl[name] = cls
