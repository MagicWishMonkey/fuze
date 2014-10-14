from fuze import *
from fuze.threads import current_thread




class Context(object):
    #__app_obj__ = None
    __slots__ = [
        "uuid",
        "__app__",
        "__bag__",
        "__user__",
        "__session__"
    ]

    def __init__(self, app):
        self.uuid = util.guid()
        self.__app__ = app
        self.__bag__ = None
        self.__user__ = None
        self.__session__ = None
        current_thread.set("context", self)

    @property
    def bag(self):
        bag = self.__bag__
        if bag is None:
            bag = {}
            self.__bag__ = bag
        return bag

    @property
    def app(self):
        return self.__app__

    @property
    def db(self):
        bag = self.bag
        try:
            return bag["db"]
        except:
            db = self.app.db()
            bag["db"] = db
            return db

    @property
    def redis(self):
        bag = self.bag
        try:
            return bag["redis"]
        except:
            redis = self.app.db("redis")
            bag["redis"] = redis
            return redis

    def query(self, sql, *args, **params):
        if len(args) > 0 and isinstance(args[0], dict) is True:
            kwd = args[0]
            for key in kwd.keys():
                params[key] = kwd[key]
        return self.db.query(
            sql,
            **params
        )

    def query_buffer(self):
        return self.db.query_buffer()

    def get_extension(self, name, cls):
        bag = self.bag
        try:
            return bag[name]
        except:
            ext = cls(self)
            bag[name] = ext
            return ext

    @staticmethod
    def current():
        ctx = current_thread.get("context")
        if ctx is not None:
            return ctx

        from fuze.app import App
        ctx = App.create_context()
        return ctx


class Extension(object):
    def __init__(self, *args):
        self.ctx = args[0] if len(args) > 0 else util.context()

    def __getattr__(self, method):
        fn = getattr(self.ctx, method)
        return fn

    def scalars(self, sql, *args, **params):
        return self.ctx.query(sql, *args, **params).scalars()

    def scalar(self, sql, *args, **params):
        return self.ctx.query(sql, *args, **params).scalar()

    def fetch(self, sql, *args, **params):
        return self.ctx.query(sql, *args, **params).select()

    def query(self, sql, *args, **params):
        return self.ctx.query(sql, *args, **params)

    @classmethod
    def plugin(cls, plugin):
        setattr(cls, plugin.func_name, plugin)