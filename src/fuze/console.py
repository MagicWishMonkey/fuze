import sys
from .log import Terminal


class Console(object):
    def __init__(self):
        self.terminal = Terminal()
        self.debug_mode = False

    def clear(self):
        self.terminal.clear()
        return self

    def write(self, msg):
        self.terminal.white(msg)
        return self

    def trace(self, msg):
        self.terminal.blue(msg)
        return self

    def info(self, msg):
        self.terminal.green(msg)
        return self

    def notify(self, msg):
        self.terminal.yellow(msg)
        return self

    def alert(self, msg):
        self.terminal.red(msg)
        return self

    def ask(self, message):
        if message.endswith(" ") is False:
            message = "%s " % message

        sys.stdout.write(message)
        txt = sys.stdin.readline().replace("\n", "")
        if len(txt) == 0:
            return None
        if txt.lower() == "y" or txt.lower() == "yes" or txt == "1":
            return True
        if txt.lower() == "n" or txt.lower() == "no" or txt == "0":
            return False
        return txt

    def __getitem__(self, command):
        try:
            return getattr(self, command.strip().lower())
        except:
            msg = "The command '%s' is not supported." % command
            raise Exception(msg)

    @classmethod
    def invoke(cls):
        fn, cmd = cls.prepare()

        if fn is not None:
            if cmd.debug_mode is True:
                cmd.terminal.pink("----------------------------------------------")
                cmd.terminal.pink("DEBUG MODE ENABLED")
                cmd.terminal.pink("----------------------------------------------")
            try:
                fn()
                #print("...")
            except Exception, ex:
                message = "Error invoking command: %s" % ex.message
                cmd.alert(message)

    @classmethod
    def parse(cls):
        fn, cmd = cls.prepare()
        return fn

    @classmethod
    def prepare(cls):
        def curry(f, *a, **kw):
            def curried(*more_a, **more_kw):
                return f(*(a + more_a), **dict(kw, **more_kw))
            return curried

        console = None
        try:
            console = cls()
        except Exception, ex:
            message = ex.message
            Terminal().red(message)
            return None, None


        try:
            console = cls()
            txt = " ".join(sys.argv[1:])
            #print(txt)
            if txt.strip().endswith("-d"):
                txt = txt[0:len(txt) - 3]
                console.debug_mode = True
                #print(txt)

            if txt.find(" -d ") > -1:
                txt = txt.replace(" -d ", " ").strip()
                console.debug_mode = True
                #print(txt)
                #if txt.find("tag=") > -1:
                #    txt = txt.replace(" -d ", " ")

            parts = txt.split(" ")
            command = parts[0]
            args = " ".join(parts[1:])
            if len(args) == 0 and command.find(":") > -1:
                parts = command.split(":")
                command = parts[0]
                args = " ".join(parts[1:])

            function = None
            try:
                function = console[command]
            except:
                console.alert("The command could not be found: %s" % command)
                return None, None

            #print(args)
            if args is not None and len(args) > 0:
                # print("bind args...")
                function = curry(function, args)
            return function, console
        except Exception, ex:
            msg = "The command could not be parsed! %s" % ex.message
            console.alert(msg)
            return None, None

    @classmethod
    def plugin(cls, plugin):
        setattr(cls, plugin.func_name, plugin)