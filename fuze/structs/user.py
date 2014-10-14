

class Person(object):
    __slots__ = [
        "id",
        "name",
        "username",
        "email"
    ]

    def __init__(self, **kwd):
        self.id = None
        self.name = None
        self.username = None
        self.email = None
        try:
            self.id = kwd["id"]
        except KeyError:
            pass

        try:
            self.name = kwd["name"]
        except KeyError:
            pass

        try:
            self.username = kwd["username"]
        except KeyError:
            pass

        try:
            self.email = kwd["email"]
        except KeyError:
            if self.username is not None:
                if self.username.find("@") > -1:
                    self.email = self.username

        if self.email is None and self.username is not None:
            if self.username is not None:
                if self.username.find("@") > -1:
                    self.email = self.username
        elif self.username is None and self.email is not None:
            if self.email is not None:
                if self.email.find("@") > -1:
                    self.username = self.email
    @staticmethod
    def create(id=None, name=None, username=None, email=None):
        return Person(
            id=id,
            name=name,
            username=username,
            email=email
        )

    def __repr__(self):
        id = self.id
        name = self.name
        username = self.username
        if id is not None:
            if username is not None:
                name = username
            if name is not None:
                return "User#%s [%s]" % (str(id), name)
            return "User#%s" % str(id)

        if username is not None:
            name = username
        if name is not None:
            return "User# [%s]" % name
        return "User"

    def __str__(self):
        return self.__repr__()
