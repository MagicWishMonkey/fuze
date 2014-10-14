from email import utils as __utils__
from fuze.utilities.emails import EmailAddress as __EmailAddress__


class Person(object):
    __slots__ = [
        "id",
        "label",
        "username"
    ]

    def __init__(self, *address, **kwd):
        id, label, username = None, None, None
        if len(kwd) > 0:
            try:
                id = kwd["id"]
            except KeyError:
                pass

            try:
                label = kwd["label"]
            except KeyError:
                pass

            try:
                username = kwd["username"]
            except KeyError:
                pass

        if len(address) > 0:
            address = address[0]
            if isinstance(address, basestring) is True:
                addr = __utils__.parseaddr(address)
                name, email = addr[0], addr[1]
                if email:
                    email_address = __EmailAddress__.format(email)
                    if email_address is not None:
                        username = email_address
                    elif len(email) > 0:
                        if name is None:
                            name = email
                        if label is None:
                            label = name
        if username is None:
            if label is not None:
                if label.find("@") > -1:
                    email_address = __EmailAddress__.format(label)
                    if email_address is not None:
                        username = email_address
                        label = None

        self.id = id
        self.label = label
        self.username = username

    @property
    def email(self):
        username = self.username
        email = __EmailAddress__.parse(username)
        return email

    @property
    def domain(self):
        username = self.username
        email = __EmailAddress__.parse(username)
        if email is None or email.valid is False:
            return None
        return email.domain

    @property
    def formatted(self):
        label, username = self.label, self.username
        if not username:
            return label
        if not label:
            return username
        if label and username:
            return __utils__.formataddr((label, username))
        return ""

    @staticmethod
    def parse(address):
        label, username = None, None

        addr = __utils__.parseaddr(address)
        name, email = addr[0], addr[1]
        if email:
            email_address = __EmailAddress__.format(email)
            if email_address is not None:
                username = email_address
            elif len(email) > 0:
                if name is None:
                    name = email
        if name is not None:
            label = name
        return Person(label=label, username=username)

    @staticmethod
    def create(*address, **kwd):
        return Person(*address, **kwd)

    def __repr__(self):
        id = self.id
        name = self.formatted
        if id is not None:
            if name:
                return "%s [#%s]" % (name, str(id))
            return "Person#%s" % str(id)

        if name:
            return name
        return "Person"


    def __str__(self):
        return self.__repr__()
