from errors import *
from utilities import *
from structs import *
from io import *
from . import env
from . import log
from . import util
from . import const
from . import types
import atexit





terminal = log.terminal()
trace = lambda *message: terminal.blue(*message)

is_win = lambda: env.os.win
is_osx = lambda: env.os.osx

empty = lambda o: True if not o else False
is_str = lambda o: isinstance(o, basestring)
is_num = lambda o: isinstance(o, (int, long))
is_int = lambda o: isinstance(o, int)
is_list = lambda o: isinstance(o, (list, tuple))
is_dict = lambda o: isinstance(o, dict)



def __destroy__():
    terminal.whitespace()

atexit.register(__destroy__)
terminal.whitespace()
terminal.green()
#atexit.register(App.destroy)


# # Python 3 compatibility hack
# if sys.version_info[:2] >= (3, 0):
#     # pylint: disable=E0611,F0401
#     import pickle
#     from urllib.request import build_opener
#     from urllib.error import HTTPError, URLError
#     py2utf8_encode = lambda x: x
#     py2utf8_decode = lambda x: x
#     compat_input = input
# else:
#     from urllib2 import build_opener, HTTPError, URLError
#     import cPickle as pickle
#     py2utf8_encode = lambda x: x.encode("utf8")
#     py2utf8_decode = lambda x: x.decode("utf8")
#     compat_input = raw_input