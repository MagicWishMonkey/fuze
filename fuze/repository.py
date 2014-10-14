from fuze import *
from fuze.context import Extension
from fuze.types import IRepository
from fuze.types import MetaRepository





class Repository(IRepository, Extension):
    __metaclass__ = MetaRepository
    __select_query__ = None
    __insert_query__ = None
    __update_query__ = None
    __delete_query__ = None
    __lookup_query__ = None
    __table_name__ = None

    def __init__(self, *ctx):
        Extension.__init__(self, *ctx)

    def select_query(self, *keys):
        sql = self.__class__.__select_query__
        assert sql is not None, "The select query is not specified for %s" % self.label

        model_class = self.model_class
        query = self.query(sql)
        if model_class is not None:
            query.adapter = model_class.create

        if len(keys) == 0:
            return query

        query.where("id=@id", keys)
        return query

    def lookup_query(self, *keys):
        sql = self.__class__.__lookup_query__
        if sql is None:
            table_name = self.table_name
            sql = "SELECT ID as id FROM %s WHERE Label=@label;" % table_name
            self.__class__.__lookup_query__ = sql

        query = self.query(sql)
        if len(keys) == 0:
            return query

        query.where("label=@label", keys)
        return query

    @property
    def table_name(self):
        table_name = self.__class__.__table_name__
        if table_name is None:
            table_name = self.label.lower()
            table_name = table_name[0:len(table_name) - 1]
            self.__class__.__table_name__ = table_name
        return table_name


    @property
    def label(self):
        return self.__class__.__name__


    def lookup(self, *keys):
        single = True if len(keys) == 0 \
                         or len(keys) == 1 \
                            and isinstance(keys[0], list) is False else []


        keys = util.unroll(keys)
        if len(keys) == 0:
            return None if single is True else []

        query = self.lookup_query(keys)
        keys = query.scalars()
        if single is True:
            return keys[0] if len(keys) > 0 else None
        return keys

    def get(self, *keys):
        if len(keys) == 0:
            return None

        single = False
        if len(keys) == 1:
            if isinstance(keys[0], list) is False:
                single = True


        keys = util.unroll(keys)
        if len(keys) == 0:
            return []

        if isinstance(keys[0], basestring) is True:
            if keys[0].isdigit() is True:
                keys = map(int, keys)
            else:
                keys = self.lookup(keys)

        #for x, key in enumerate(keys):

        query = self.select_query(keys)
        models = query.select()
        if single is True:
            return models[0] if len(models) > 0 else None
        return models


    def __str__(self):
       return "%s" % self.label

    def __repr__(self):
        return self.__str__()

