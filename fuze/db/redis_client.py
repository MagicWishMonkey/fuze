from fuze import *
from fuze.db.config import Config
from redis import Redis



class RedisClient(object):
    __slots__ = [
        "config",
        "__server__"
    ]

    def __init__(self, config, server=None):
        self.config = config
        if server is None:
            cfg = {
                "host": config.uri,
                "port": config.port
            }
            if config.username is not None:
                cfg["username"] = config.username
            if config.password is not None:
                cfg["password"] = config.password

            server = Redis(**(cfg))
        self.__server__ = server

    @property
    def server(self):
        return self.__server__

    @property
    def label(self):
        return self.config.label

    def clone(self):
        return RedisClient(self.config, server=self.__server__)

    @classmethod
    def plugin(cls, plugin):
        setattr(cls, plugin.func_name, plugin)



    def rpush(self, name, *values):
        server = self.server
        with server.pipeline() as pipeline:
            for value in values:
                pipeline.rpush(name, value)

            pipeline.execute()

    def lpop(self, name):
        server = self.server
        o = server.lpop(name)
        return o

    def blpop(self, name, *timeout):
        timeout = 0 if len(timeout) == 0 else timeout[0]
        server = self.server
        o = server.blpop(name, timeout)
        return o

    @classmethod
    def open(cls, **kwd):
        driver = kwd.get("driver", None)
        if driver is None:
            raise Exception("The database driver is not specified.")

        params = kwd.get("params", {})
        config = Config(
            driver=driver,
            label=kwd.get("label", None),
            uri=kwd.get("uri", None),
            database=kwd.get("database", None),
            username=kwd.get("username", None),
            password=kwd.get("password", None),
            port=kwd.get("port", None),
            params=params
        )
        return cls(config)

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.__repr__()


# from fuze import util
# #from fuze import stats
# from fuze import log
# from fuze.errors import *
# from fuze.db.database import Database
# from redis import Redis
#
#
# class RedisServer(Database):
#     __slots__ = [
#         "config",
#         "server",
#         "buckets",
#         "queues",
#         "offline"
#     ]
#
#     def __init__(self, **config):
#         host = config.get("host", config.get("server", config.get("uri", None)))
#         port = config.get("port", 6379)
#         if isinstance(port, basestring) is True:
#             port = int(port)
#
#         username, password = config.get("username", None), config.get("password", None)
#
#         config = {
#             "host": host,
#             "port": port
#         }
#         if username is not None:
#             config["username"] = username
#         if password is not None:
#             config["password"] = password
#         self.config = config
#         self.server = Redis(**(config))
#         self.buckets = {}
#         self.queues = {}
#         self.offline = False
#         self.ping()
#
#     def ping(self):
#         def toggle(self, flag):
#             self.offline = flag
#             buckets = self.buckets.values()
#             for bucket in buckets:
#                 bucket.offline = flag
#
#         offline = self.offline
#         try:
#             self.engine.ping()
#             if offline == True:
#                 toggle(self, False)
#             return True
#         except Exception, ex:
#             log.error(FuzeError("Error pinging the database: %s" % ex.message, ex))
#             if offline == False:
#                 toggle(self, True)
#             return False
#
#     def bucket(self, name, encoder=None, decoder=None, ttl=None):
#         id = name.strip().lower()
#         try:
#             return self.buckets[id]
#         except KeyError:
#             bucket = Bucket(self, name, encoder=encoder, decoder=decoder, ttl=ttl)
#             self.buckets[id] = bucket
#             return bucket
#
#
# class Shard(object):
#     def __init__(self, server, name, **kwd):
#         self.server = server
#         self.name = name
#         self.namespace = name.strip().lower()
#         self.db = Redis(**(server.config))
#         self.ttl = kwd.get("ttl", None)
#         self.encoder = kwd.get("encoder", None)
#         self.decoder = kwd.get("decoder", None)
#         self.offline = False
#
#
#     def keygen(self, id):
#         return "%s:%s" % (self.namespace, id)
#
#
# class MixinClear:
#     def clear(self, *keys):
#         if self.offline is True:
#             return
#
#         if len(keys) == 0:
#             return
#
#         keys = util.unroll(keys) if len(keys) > 1 else [keys[0]]
#         if isinstance(keys[0], basestring) is False:
#             keys = map(str, keys)
#
#         keys = map(self.keygen, keys)
#         db = self.db
#         try:
#             if len(keys) == 1:
#                 db.delete(keys[0])
#             else:
#                 with db.pipeline() as pipeline:
#                     map(pipeline.delete, keys)
#                     pipeline.execute()
#         except Exception, ex:
#             log.error(FuzeError("Error deleting record from the database: %s" % ex.message, ex))
#             self.server.ping()
#
#
# class MixinExpire:
#     def expire(self, ttl, *keys):
#         db = self.db
#         try:
#             cnt = len(keys)
#             if cnt == 0:
#                 return
#
#             key = keys[0]
#             if isinstance(key, basestring) is False or key.find(":") == -1:
#                 if isinstance(key, basestring) is False:
#                     keys = map(str, keys)
#                 keys = map(self.keygen, keys)
#
#             for x in xrange(cnt):
#                 key = keys[x]
#                 db.expire(key, time=ttl)
#         except Exception, ex:
#             log.error(FuzeError("Error marking the ttl for the database record: %s" % ex.message, ex))
#             self.server.ping()
#
#
# class Bucket(Shard, MixinClear, MixinExpire):
#     def save(self, *objects):
#         if self.offline is True:
#             return False
#         if len(objects) == 0:
#             return True
#
#         objects = util.unroll(objects)
#         if len(objects) == 0:
#             return True
#
#
#         if util.is_model(objects[0]) is True:
#             objects = [(o.id, o) for o in objects]
#         elif isinstance(objects[0], tuple) is False:
#             raise FuzeError("The object list must either be a list of models or a list of key/val tuples!")
#
#         keys, vals = [o[0] for o in objects], [o[1] for o in objects]
#         if isinstance(keys[0], basestring) is False:
#             keys = map(str, keys)
#
#         keys = map(self.keygen, keys)
#
#         db, encoder = self.db, self.encoder
#         if encoder is not None:
#             vals = map(encoder, vals)
#
#         try:
#             cnt = len(keys)
#             for x in xrange(cnt):
#                 db.set(keys[x], vals[x])
#         except Exception, ex:
#             log.error(FuzeError("Error saving the database record: %s" % ex.message, ex))
#             self.server.ping()
#
#         ttl = self.ttl
#         if ttl is not None:
#             self.expire(ttl, keys)
#
#
#     def set(self, key, val):
#         self[key] = val
#
#     def get(self, key):
#         return self[key]
#
#     def __setitem__(self, key, value):
#         if self.offline is True:
#             return
#
#         if value is None:
#             self.clear(key)
#             return
#
#         db, encoder, ttl = self.db, self.encoder, self.ttl
#         key = self.keygen(key)
#         value = encoder(value) if encoder is not None else value
#
#         try:
#             db.set(key, value)
#         except Exception, ex:
#             log.error(FuzeError("Error saving the database record: %s" % ex.message, ex))
#             self.server.ping()
#             return
#
#         if ttl is not None:
#             self.expire(ttl, key)
#
#     def __getitem__(self, key):
#         if self.offline is True:
#             return None
#
#         db, decoder, ttl = self.db, self.decoder, self.ttl
#         if isinstance(key, basestring) is False:
#             key = str(key)
#         key = self.keygen(key)
#
#         object = None
#         try:
#             object = db.get(key)
#         except Exception, ex:
#             log.error(FuzeError("Error saving the database record: %s" % ex.message, ex))
#             self.server.ping()
#             return None
#
#         if object is not None:
#             if decoder is not None:
#                 object = decoder(object)
#
#             if ttl is not None:
#                 self.expire(ttl, key)
#
#         return object
#
#
