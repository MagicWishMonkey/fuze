import os as __os__
try:
    import pwd as __pwd__
except:
    pass

import socket as __socket__
import platform as __platform__
import datetime as __datetime__
from fuze.structs.enums import Enum as __Enum__
from fuze.io.file import File as __File__
from fuze.structs.containers import Wrapper as __Wrapper__


os = __Enum__("OSX", osx=True, linux=False, win=False) if __os__.name == "posix" \
    else __Enum__("Windows", osx=False, linux=False, win=True) if __os__.name == "nt" \
    else __Enum__("Linux", osx=False, linux=True, win=False)

uid, uri, usr = None, None, None
try:
    uid = __os__.getuid()
    uri = __os__.getcwd()
except:
    pass
try:
    usr = __pwd__.getpwuid(__os__.getuid())[0]
except:
    pass

date = __datetime__.datetime.now()
debug = __debug__
machine = __platform__.node()
address = __socket__.gethostbyname(__socket__.gethostname())
folder = __File__(__file__).parent.parent.uri
