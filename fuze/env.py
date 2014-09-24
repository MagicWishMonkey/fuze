import os as __os__
import pwd as __pwd__
import socket as __socket__
import platform as __platform__
import datetime as __datetime__
from .types import Enum



# class __ENV__(dict):
#     __locked__ = False
#
#     def __init__(self):
#         self.uid = os.getuid()
#         self.uri = os.getcwd()
#         self.usr = pwd.getpwuid(os.getuid())[0]
#         self.date = datetime.datetime.now()
#         self.debug = __debug__
#         self.address = socket.gethostbyname(socket.gethostname())
#
#     def __getattr__(self, key):
#         try:
#             o = self[key]
#             return o
#         except KeyError:
#             return None
#
#     def __setattr__(self, key, value):
#         self[key] = value
#
#     def __str__(self):
#         return "ENV"
#
#     def __repr__(self):
#         return self.__str__()
#
# self = __ENV__()

os = Enum("OSX", osx=True, linux=False, win=False) if __os__.name == "posix" \
    else Enum("Windows", osx=False, linux=False, win=True) if __os__.name == "nt" \
    else Enum("Linux", osx=False, linux=True, win=False)


uid = __os__.getuid()
uri = __os__.getcwd()
usr = __pwd__.getpwuid(__os__.getuid())[0]
date = __datetime__.datetime.now()
debug = __debug__
machine = __platform__.node()
address = __socket__.gethostbyname(__socket__.gethostname())



# o["process"] = {
#     "uid": os.getuid(),
#     "usr": pwd.getpwuid(os.getuid())[0]
# }
# o["quarantine"] = constants.QUARANTINE
# o["address"] = socket.gethostbyname(socket.gethostname())
# o["flags"] = self.ctx.flags.reduce()
# o["machine"] = platform.node()
# o["environment"] = constants.ENVIRONMENT.__str__()
# o["quarantine"] = True if constants.QUARANTINE is True else False
# o["home_path"] = constants.HOME_PATH