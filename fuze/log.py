from __future__ import print_function



class Logger(object):
    __instance__ = None

    def __init__(self):
        self.level = None

    def debug(self, *message):
        print("debug...")

    def trace(self, *message):
        print("trace...")

    def info(self, *message):
        print("info...")

    def warn(self, *message):
        print("warn...")

    def error(self, *message):
        print("error...")


    @staticmethod
    def get():
        return Logger.__instance__


Logger.__instance__ = Logger()


# import os
# from . import env
# from .types import Wrapper
#
#
#
# class Terminal(object):
#     __colors__ = None
#     __colorama__ = False
#
#     def __init__(self):
#         self.colors = Terminal.__colors__
#         if self.colors is None:
#             colors = Wrapper({
#                 "ul": "",
#                 "white": "",
#                 "red": "",
#                 "green": "",
#                 "yellow": "",
#                 "blue": "",
#                 "pink": "",
#             })
#
#
#             try:
#                 from colorama import init as init_colorama, Fore, Style
#                 Terminal.__colorama__ = True
#                 if env.os.win is True:
#                     colors.ul = Style.DIM + Fore.YELLOW
#                     colors.white = Style.RESET_ALL
#                     colors.red = Fore.RED
#                     colors.green = Fore.GREEN
#                     colors.yellow = Fore.YELLOW
#                     colors.blue = Fore.CYAN
#                     colors.pink = Fore.MAGENTA
#                 else:
#                     # colors.ul = Style.DIM + Fore.YELLOW
#                     # colors.white = Style.RESET_ALL
#                     # colors.red = Fore.RED
#                     # colors.green = Fore.GREEN
#                     # colors.yellow = Fore.YELLOW
#                     # colors.blue = Fore.CYAN
#                     # colors.pink = Fore.MAGENTA
#
#                     colors.ul = "\x1b[%sm" * 3 % (2, 4, 33)
#                     colors.white = "\x1b[%sm" % 0
#                     cols = ["\x1b[%sm" % n for n in range(91, 96)]
#                     colors.red = cols[0]
#                     colors.green = cols[1]
#                     colors.yellow = cols[2]
#                     colors.blue = cols[3]
#                     colors.pink = cols[4]
#             except ImportError:
#                 pass
#
#             Terminal.__colors__ = colors
#             self.colors = colors
#             self.current = colors.white
#
#     @property
#     def color_list(self):
#         return self.colors.keys()
#
#     def bind(self, color):
#         if color is None:
#             return self.write
#
#         if color == "blue":
#             self.current = self.colors.blue
#             return self.blue
#         elif color == "red":
#             self.current = self.colors.red
#             return self.red
#         elif color == "green":
#             self.current = self.colors.green
#             return self.green
#         elif color == "yellow":
#             self.current = self.colors.yellow
#             return self.yellow
#         elif color == "blue":
#             self.current = self.colors.blue
#             return self.blue
#         elif color == "pink":
#             self.current = self.colors.pink
#             return self.pink
#         return self.write
#
#     def clear(self):
#         os.system("clear")
#         return self
#
#     def ul(self, *message):
#         self.current = self.colors.ul
#         if len(message) == 0:
#             return self
#         return self.write(*message)
#
#     def yellow(self, *message):
#         self.current = self.colors.yellow
#         if len(message) == 0:
#             return self
#         return self.write(*message)
#
#     def red(self, *message):
#         self.current = self.colors.red
#         if len(message) == 0:
#             return self
#         return self.write(*message)
#
#     def green(self, *message):
#         self.current = self.colors.green
#         if len(message) == 0:
#             return self
#         return self.write(*message)
#
#     def blue(self, *message):
#         self.current = self.colors.blue
#         if len(message) == 0:
#             return self
#         return self.write(*message)
#
#     def pink(self, *message):
#         self.current = self.colors.pink
#         if len(message) == 0:
#             return self
#         return self.write(*message)
#
#     def white(self, *message):
#         self.current = self.colors.white
#         if len(message) == 0:
#             return self
#         return self.write(*message)
#
#     def whitespace(self):
#         print(self.colors.white)
#         return self
#
#     def write(self, *message, **kwd):
#         if len(kwd) > 0:
#             color = kwd.get("color", None)
#             if color is not None:
#                 print("CHANGING COLOR TO %s" % color)
#
#
#             # color = self.colors[kwd.values()[0]]
#             # if color is not None:
#             #     print("CHANGING COLOR TO %s" % str(kwd.values()[0]))
#             #     self.current = color
#
#         buffer = [self.current]
#         for msg in message:
#             if msg is None:
#                 msg = ""
#             buffer.append(msg)
#         buffer.append(self.colors.white)
#         txt = "".join(buffer)
#         print(txt)
#         return self
#
#     # def __del__(self):
#     #     print(self.colors.white)
#     #     #self.whitespace()
#
# def terminal():
#     return Terminal()
#
#
#
#
# # try:
# #     from colorama import init as init_colorama, Fore, Style
# #     has_colorama = True
# # except ImportError:
# #     has_colorama = False
#
#
#
# # # Python 3 compatibility hack
# # if sys.version_info[:2] >= (3, 0):
# #     # pylint: disable=E0611,F0401
# #     import pickle
# #     from urllib.request import build_opener
# #     from urllib.error import HTTPError, URLError
# #     py2utf8_encode = lambda x: x
# #     py2utf8_decode = lambda x: x
# #     compat_input = input
# # else:
# #     from urllib2 import build_opener, HTTPError, URLError
# #     import cPickle as pickle
# #     py2utf8_encode = lambda x: x.encode("utf8")
# #     py2utf8_decode = lambda x: x.decode("utf8")
# #     compat_input = raw_input