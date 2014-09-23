from fuze import util



class PivotalObject(object):
    def __init__(self, tracker, **kwd):
        self.__tracker__ = tracker
        for key in kwd:
            val = kwd[key]
            self.__dict__[key] = val

    @property
    def tracker(self):
        return self.__tracker__

    @property
    def label(self):
        return self.__dict__["name"]

    def _get_(self, uri):
        return self.__tracker__._get_(uri)

    def _post_(self, uri):
        return self.__tracker__._post_(uri)

    def stringify(self):
        tracker = self.__tracker__
        self.__tracker__ = None
        data = util.pickle(self)
        data = util.base64(data)
        self.__tracker__ = tracker
        return data

    def bind(self, tracker):
        self.__tracker__ = tracker
        return self

    def __str__(self):
        try:
            return "%s [#%s] %s" % (self.__class__.__name__, str(self.id), self.label)
        except:
            return "%s #%s" % (self.__class__.__name__, str(self.id))

    def __repr__(self):
        return self.__str__()

    @classmethod
    def spawn(cls, tracker, *objects):
        objects = util.unroll(objects)
        return [cls(tracker, **(o)) for o in objects]


class PivotalProject(PivotalObject):
    def __init__(self, tracker, **kwd):
        PivotalObject.__init__(self, tracker, **kwd)
        self.__stories__ = None

    def fetch_story(self, id):
        stories = self.stories
        for story in stories:
            if story.id == id:
                return story
        return None


    @property
    def stories(self):
        if self.__stories__ is not None:
            return self.__stories__

        filter = "current_state:started,planned,unstarted,unscheduled"
        objects = self._get_("https://www.pivotaltracker.com/services/v5/projects/{id}/stories/?limit=1000&filter={filter}".format(id=self.id, filter=filter))
        stories = PivotalStory.spawn(self.tracker, objects)
        self.__stories__ = stories
        return stories


    @property
    def accounts(self):
        objects = self._get_("https://www.pivotaltracker.com/services/v5/projects/{id}/memberships".format(id=self.id))
        objects = [object["person"] for object in objects]
        accounts = [PivotalAccount(self.tracker, **(object)) for object in objects]
        return accounts



class PivotalStory(PivotalObject):
    def __init__(self, tracker, **kwd):
        PivotalObject.__init__(self, tracker, **kwd)

    @property
    def label(self):
        return self.__dict__["name"]


class PivotalAccount(PivotalObject):
    def __init__(self, tracker, **kwd):
        PivotalObject.__init__(self, tracker, **kwd)

    @property
    def label(self):
        return self.__dict__["name"]



class Pivotal(object):
    def __init__(self, token):
        self.token = token
        self.__projects__ = None
        self.__stories__ = None

    def inflate(self, data):
        data = util.unbase64(data)
        obj = util.unpickle(data)
        obj.bind(self)
        return obj

    @property
    def projects(self):
        if self.__projects__ is None:
            self.__projects__ = PivotalProject.spawn(self, self._get_("https://www.pivotaltracker.com/services/v5/projects/"))
        return self.__projects__

    @property
    def accounts(self):
        lst = []
        projects = self.projects
        for project in projects:
            accounts = project.accounts
            if len(accounts) > 0:
                lst.extend(accounts)
        accounts = dict((account.username, account) for account in lst).values()
        return accounts


    @property
    def stories(self):
        if self.__stories__ is not None:
            return self.__stories__

        lst = []
        projects = self.projects
        for project in projects:
            stories = project.stories
            if len(stories) > 0:
                lst.extend(stories)

        self.__stories__ = lst
        return lst

    def _get_(self, uri):
        response = util.web_get(uri, ("X-TrackerToken", self.token))
        object = util.unjson(response)
        if isinstance(object, list) is True:
            objects = [ServerObject.create(**(o)) for o in object]
            return objects
        object = ServerObject.create(**(object))
        return object

    def _post_(self, uri):
        request = tools.create_http_request(uri, ("X-TrackerToken", self.token))
        response = request.POST()

        #response = tools.http_post(uri, headers={"X-TrackerToken": self.token})
        object = tools.unjson(response)
        if isinstance(object, list) is True:
            objects = [ServerObject.create(**(o)) for o in object]
            return objects
        object = ServerObject.create(**(object))
        return object


    def fetch_story(self, id):
        projects = self.projects
        for project in projects:
            story = project.fetch_story(id)
            if story is not None:
                return story
        return None

    def reset(self):
        self.__projects__ = None
        return self

    def __str__(self):
        return "Pivotal: %s" % self.token

    def __repr__(self):
        return self.__str__()

    # def stringify(self):
    #     blob = tools.pickle(self)
    #     blob = tools.deflate(blob)
    #     return blob
    #
    # @staticmethod
    # def restore(data):
    #     data = tools.inflate(data)
    #     obj = tools.unpickle(data)
    #     return obj

class ServerObject(dict):
    def __getattr__(self, key):
        try:
            o = self[key]
            if isinstance(o, dict) is True:
                if isinstance(o, ServerObject) is False:
                    o = ServerObject.create(o)
                    self[key] = o
            elif isinstance(o, list) is True:
                if len(o) > 0:
                    if isinstance(o[0], dict) is True and isinstance(o[0], ServerObject) is False:
                        o = map(ServerObject.create, o)
                        self[key] = o
            return o
        except KeyError, ex:
            return None

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            self.pop(key)
        except KeyError:
            pass

    def objectify(self):
        o = {}
        for key in self:
            val = self[key]
            if isinstance(val, list):
                if len(val) > 0 and isinstance(val[0], ServerObject) is True:
                    val = [v.objectify() for v in val]
            elif isinstance(val, ServerObject) is True:
                val = val.objectify()

            o[key] = val
        return o

    def __str__(self):
        obj = self.objectify()
        data = tools.json_encode_pretty(obj)
        return data

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def create(*args, **kwargs):
        if args and len(args) > 0:
            return ServerObject(args[0])
        return ServerObject(kwargs)

