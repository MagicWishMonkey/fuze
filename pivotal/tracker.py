from fuze import util
from pivotal.structs import *
from fuze.db import SQLite



class Tracker(object):
    def __init__(self, settings):
        self.token = settings["token"]
        database = settings["database"]
        database = util.folder(database).file("pivotal.sqlite")
        self.db = TrackerDatabase(database.uri)
        self.pivotal = Pivotal(self.token)
        # if self.db.scalar("SELECT COUNT(id) FROM projects;") == 0:
        #     print "SYNC!"
        #     self.sync()

    @property
    def current_project(self):
        id = self.db.scalar("SELECT project_id FROM cache;")
        if id is None:
            return None
        return self.project(id)

    @property
    def current_story(self):
        id = self.db.scalar("SELECT story_id FROM cache;")
        if id is None:
            return None
        return self.story(id)

    def clear_story(self):
        self.db.update("UPDATE cache SET story_id=NULL, project_id=NULL;")
        return self

    def set_story(self, id):
        story = self.story(id)
        if story is None:
            print "The story record could not be found."
            self.db.update("UPDATE cache SET story_id=NULL, project_id=NULL;")
            return None

        self.db.update("UPDATE cache SET story_id={story_id}, project_id={project_id}, updated=CURRENT_TIMESTAMP;".format(story_id=story.id, project_id=story.project_id))
        return story

    def sync(self, accounts=True, projects=True, stories=True):
        if projects is True:
            records = self.pivotal.projects
            for project in records:
                if self.project_exists(project.id) is False:
                    self.create_project(project)
                else:
                    self.update_project(project)

                if stories is True:
                    inner = project.stories
                    for story in inner:
                        if self.story_exists(story.id) is False:
                            self.create_story(story)
                        else:
                            self.update_story(story)

        elif stories is True:
            records = self.pivotal.stories
            for story in records:
                if self.story_exists(story.id) is False:
                    self.create_story(story)
                else:
                    self.update_story(story)


        if accounts is True:
            records = self.pivotal.accounts
            for account in records:
                if self.account_exists(account.id) is False:
                    self.create_account(account)
                else:
                    self.update_account(account)

        self.db.update("UPDATE cache SET updated=CURRENT_TIMESTAMP;")

    def create_account(self, account):
        snapshot = account.stringify()
        self.db.insert(
            "INSERT INTO accounts (id, name, email, username, initials, snapshot) VALUES (@id, @name, @email, @username, @initials, @snapshot);",
            id=account.id,
            name=account.name,
            email=account.email,
            username=account.username,
            initials=account.initials,
            snapshot=snapshot
        )

    def update_account(self, account):
        snapshot = account.stringify()
        self.db.update(
            "UPDATE accounts SET name=@name, email=@email, username=@username, initials=@initials, snapshot=@snapshot WHERE id=@id;",
            id=account.id,
            name=account.name,
            email=account.email,
            username=account.username,
            initials=account.initials,
            snapshot=snapshot
        )


    def create_project(self, project):
        snapshot = project.stringify()
        self.db.insert(
            "INSERT INTO projects (id, name, account_id, current_iteration_number, average_velocity, snapshot) VALUES (@id, @name, @account_id, @current_iteration_number, @average_velocity, @snapshot);",
            id=project.id,
            name=project.name,
            account_id=project.account_id,
            current_iteration_number=project.current_iteration_number,
            average_velocity=project.velocity_averaged_over,
            snapshot=snapshot
        )

    def update_project(self, project):
        snapshot = project.stringify()
        self.db.update(
            "UPDATE projects SET name=@name, account_id=@account_id, current_iteration_number=@current_iteration_number, average_velocity=@average_velocity, snapshot=@snapshot WHERE id=@id;",
            id=project.id,
            name=project.name,
            account_id=project.account_id,
            current_iteration_number=project.current_iteration_number,
            average_velocity=project.velocity_averaged_over,
            snapshot=snapshot
        )


    def create_story(self, story):
        snapshot = story.stringify()
        owner_id, description, estimate = None, None, 0
        try:
            owner_id = story.owned_by_id
        except:
            pass

        try:
            description = story.description
        except:
            pass

        try:
            estimate = story.estimate
        except:
            pass

        self.db.insert(
            "INSERT INTO stories (id, name, project_id, type, owner_id, url, description, estimate, status, last_update, snapshot) VALUES (@id, @name, @project_id, @type, @owner_id, @url, @description, @estimate, @status, @last_update, @snapshot);",
            id=story.id,
            name=story.name,
            project_id=story.project_id,
            type=story.story_type,
            owner_id=owner_id,
            url=story.url,
            description=description,
            estimate=estimate,
            status=story.current_state,
            last_update=story.updated_at,
            snapshot=snapshot
        )

    def update_story(self, story):
        snapshot = story.stringify()
        owner_id, description, estimate = None, None, 0
        try:
            owner_id = story.owned_by_id
        except:
            pass

        try:
            description = story.description
        except:
            pass

        try:
            estimate = story.estimate
        except:
            pass

        self.db.update(
            "UPDATE stories SET name=@name, project_id=@project_id, type=@type, owner_id=@owner_id, url=@url, description=@description, estimate=@estimate, status=@status, last_update=@last_update, snapshot=@snapshot WHERE id=@id;",
            id=story.id,
            name=story.name,
            project_id=story.project_id,
            type=story.story_type,
            owner_id=owner_id,
            url=story.url,
            description=description,
            estimate=estimate,
            status=story.current_state,
            last_update=story.updated_at,
            snapshot=snapshot
        )



    @property
    def accounts(self):
        snapshots = self.db.scalars("SELECT snapshot FROM accounts;")
        return map(self.pivotal.inflate, snapshots)

    @property
    def projects(self):
        snapshots = self.db.scalars("SELECT snapshot FROM projects;")
        return map(self.pivotal.inflate, snapshots)

    @property
    def stories(self):
        snapshots = self.db.scalars("SELECT snapshot FROM stories;")
        return map(self.pivotal.inflate, snapshots)

    def account(self, key):
        id = key if isinstance(key, int) is True else None
        if id is None:
            id = self.db.scalar("SELECT id FROM accounts WHERE email=@email OR username=@username OR initials=@initials;", email=key, username=key, initials=key)
        if id is None:
            return None

        data = self.db.scalar("SELECT snapshot FROM accounts WHERE id={id};".format(id=id))
        if data is None:
            return None

        if self.db.scalar("SELECT id FROM accounts WHERE id={id};".format(id=id)) is None:
            return False
        return True


    def project(self, key):
        id = key if isinstance(key, int) is True else None
        if id is None:
            id = self.db.scalar("SELECT id FROM projects WHERE name=@name;", name=key)

        if id is None:
            self.sync(projects=True, accounts=False, stories=False)
            id = key if isinstance(key, int) is True else None
            if id is None:
                id = self.db.scalar("SELECT id FROM projects WHERE name=@name;", name=key)
            if id is None:
                return None


        data = self.db.scalar("SELECT snapshot FROM projects WHERE id={id};".format(id=id))
        if data is None:
            if data is None:
                self.sync(projects=True, accounts=False, stories=False)
            data = self.db.scalar("SELECT snapshot FROM projects WHERE id={id};".format(id=id))
            if data is None:
                return None
        return self.pivotal.inflate(data)


    def account_exists(self, key):
        id = key if isinstance(key, int) is True else None
        if id is None:
            id = self.db.scalar("SELECT id FROM accounts WHERE email=@email OR username=@username OR initials=@initials;", email=key, username=key, initials=key)

        if id is None:
            return None

        if self.db.scalar("SELECT id FROM accounts WHERE id={id};".format(id=id)) is None:
            return False
        return True


    def project_exists(self, key):
        id = key if isinstance(key, int) is True else None
        if id is None:
            id = self.db.scalar("SELECT id FROM projects WHERE name=@name;", name=key)

        if id is None:
            return False

        if self.db.scalar("SELECT id FROM projects WHERE id={id};".format(id=id)) is None:
            return False
        return True


    def story(self, key):
        id = key if isinstance(key, int) is True else None
        if id is None:
            id = self.db.scalar("SELECT id FROM stories WHERE name=@name;", name=key)

        if id is None:
            self.sync(projects=False, accounts=False, stories=True)
            id = key if isinstance(key, int) is True else None
            if id is None:
                id = self.db.scalar("SELECT id FROM stories WHERE name=@name;", name=key)
            if id is None:
                return None

        data = self.db.scalar("SELECT snapshot FROM stories WHERE id={id};".format(id=id))
        if data is None:
            self.sync(projects=False, accounts=False, stories=True)
            data = self.db.scalar("SELECT snapshot FROM stories WHERE id={id};".format(id=id))
            if data is None:
                return None
        story = self.pivotal.inflate(data)
        story.project = util.curry(self.project, story.project_id)
        return story


    def story_exists(self, id):
        if self.db.scalar("SELECT id FROM stories WHERE id={id};".format(id=id)) is None:
            return False
        return True

    def lookup_stories(self, name):
        sql = "select id from stories where name like '{name}%' or name like '%{name}' or name like '%{name}%';".format(name=name.replace("'", ""))
        keys = self.db.scalars(sql)
        if len(keys) == 0:
            return []

        stories = self.db.scalars("SELECT snapshot FROM stories WHERE id IN ({csv});".format(csv=",".join(map(str, keys))))
        stories = map(self.pivotal.inflate, stories)
        return stories



class TrackerDatabase(object):
    def __init__(self, uri):
        self.uri = uri
        self.db = SQLite.open(uri, constructor=self.init_db_schema)
        if self.db.scalar("SELECT id FROM cache;") is None:
            self.db.insert("INSERT INTO cache (id, updated) VALUES (1, CURRENT_TIMESTAMP);")


    def update(self, sql, **params):
        return self.db.update(sql, **params)

    def insert(self, sql, **params):
        return self.db.insert(sql, **params)

    def execute(self, sql, **params):
        return self.db.execute(sql, **params)

    def query_buffer(self):
        return self.db.query_buffer()

    def sequence(self, *count):
        return self.db.sequence(*count)

    def scalar(self, sql, **params):
        return self.db.scalar(sql, **params)

    def scalars(self, sql, **params):
        return self.db.scalars(sql, **params)

    def record(self, sql, *fn, **params):
        return self.db.record(sql, *fn, **params)

    def select(self, sql, *fn, **params):
        return self.db.select(sql, *fn, **params)

    def init_db_schema(self, db):
        queries = []
        queries.append("""
            CREATE TABLE "accounts" (
                 "id" INTEGER NOT NULL,
                 "name" VARCHAR(250),
                 "email" VARCHAR(250),
                 "username" VARCHAR(250),
                 "initials" VARCHAR(10),
                 "snapshot" TEXT,
                PRIMARY KEY("id")
            );""")

        queries.append("""
            CREATE TABLE "stories" (
                 "id" INTEGER NOT NULL,
                 "project_id" INTEGER NOT NULL,
                 "name" VARCHAR(500),
                 "type" VARCHAR(10),
                 "owner_id" INTEGER NOT NULL,
                 "url" VARCHAR(500),
                 "description" VARCHAR(2000),
                 "estimate" INTEGER NOT NULL,
                 "status" VARCHAR(10),
                 "last_update" DATETIME,
                 "snapshot" TEXT,
                PRIMARY KEY("id")
            );""")

        queries.append("""
            CREATE TABLE "projects" (
                 "id" INTEGER NOT NULL,
                 "name" VARCHAR(500),
                 "account_id" INTEGER NOT NULL,
                 "current_iteration_number" INTEGER NOT NULL,
                 "average_velocity" INTEGER NOT NULL,
                 "snapshot" TEXT,
                PRIMARY KEY("id")
            );""")

        queries.append("""
            CREATE TABLE "cache" (
                "id" INTEGER NOT NULL,
                "project_id" INTEGER,
                "story_id" INTEGER,
                "account_id" INTEGER,
                "updated" DATETIME,
                PRIMARY KEY("id")
            );""")
        [db.execute(query) for query in queries]


