from fuze import *
#from fuze.console import Console

# import os
# import atexit
#
#
# class Downloader(Console):
#     __temp__ = {}
#
#     def __init__(self, *uri):
#         Console.__init__(self)
#         uri = os.getcwd() if len(uri) == 0 else uri[0]
#         self.folder = util.folder(uri)
#         self.queue = []
#
#         files = self.folder.files(recursive=True)
#         for file in files:
#             if file.kb < 1:
#                 uri = file.read_text()
#                 if uri.find("/") > -1 and uri.startswith("http://") or uri.startswith("https://") or uri.startswith("www."):
#                     self.queue.append((uri, file))
#
#     def start(self):
#         queue = self.queue
#         def download(total, ix, uri, file, color):
#
#             trace = self.terminal.bind(color)
#
#             name = file.name
#             temp = file.parent.file("%s.tmp" % file.uri)
#             Downloader.__temp__[temp.uri] = temp.uri
#             try:
#                 def on_download(temp):
#                     uri = temp.uri
#                     uri = uri[0:len(uri) - 4]
#                     file = temp.parent.file(uri)
#                     temp.move(file, overwrite=True)
#
#                 callback = util.curry(on_download, temp)
#
#
#                 request = util.request(uri)
#                 file_size = request.size
#                 tmp_uri = temp.uri
#
#
#                 request.download(temp, async=True, callback=callback)
#                 while temp.exists is False:
#                     util.sleep(.01)
#
#                 #self.clear()
#                 counter = 0
#                 while True:
#                     if util.file(tmp_uri).exists is False:
#                         break
#
#                     kb = temp.kb
#                     pct = round((kb / file_size), 2) if kb > 0 else 0
#                     if pct > 0:
#                         pct = (pct * float(100))
#
#                     if counter == 0 or counter > 10:
#                         counter = 0
#                         buffer = ["[%s of %s]" % (str(ix + 1), str(total)), " [", str(pct), "%]", " - ", name]
#                         msg = "".join(buffer)
#                         #self.notify(msg)
#                         trace(msg)
#                     counter = (counter + 1)
#                     util.sleep(.25)
#             except Exception, ex:
#                 try:
#                     temp.delete()
#                 except:
#                     pass
#                 raise ex
#             finally:
#                 try:
#                     Downloader.__temp__.pop(temp.uri)
#                 except:
#                     pass
#
#         colors = self.terminal.color_list
#         colors = [c for c in colors if c != "ul" and c != "white"]
#         total = len(queue)
#         for ix, o in enumerate(queue):
#             uri, file, color = o[0], o[1], None
#             try:
#                 color = colors.pop()
#             except:
#                 colors = self.terminal.color_list
#                 colors = [c for c in colors if c != "ul" and c != "white"]
#                 color = colors.pop()
#
#
#             download(total, ix, uri, file, color)
#
#     @staticmethod
#     def cleanup():
#         files = Downloader.__temp__.keys()
#         [util.file(file).delete() for file in files]
#
#     @classmethod
#     def open(cls, *uri):
#         dl = Downloader(*uri)
#         return dl
#
# atexit.register(Downloader.cleanup)
#



def init():
    #Downloader(util.folder("/Users/ron/Downloads/__NS__/TEST").uri).start()
    print util.json({"label": "ron"})
    raw_input("...")
    quit()

    folder = util.folder("/Users/ron/Downloads/__NS__/TEST")
    files = folder.files(recursive=True)
    queue = []
    for file in files:
        if file.kb < 1:
            uri = file.read_text()
            if uri.find("/") > -1 and uri.startswith("http://") or uri.startswith("https://") or uri.startswith("www."):
                queue.append((uri, file))

    def download(uri, file):
        name = file.name
        temp = file.parent.file("%s.tmp" % file.uri)
        try:
            def on_download(temp):
                uri = temp.uri
                uri = uri[0:len(uri) - 4]
                file = temp.parent.file(uri)
                temp.move(file, overwrite=True)

            callback = util.curry(on_download, temp)


            request = util.request(uri)
            file_size = request.size
            tmp_uri = temp.uri


            request.download(temp, async=True, callback=callback)
            while temp.exists is False:
                util.sleep(.01)

            while True:
                if util.file(tmp_uri).exists is False:
                    break

                kb = temp.kb
                pct = round((kb / file_size), 2) if kb > 0 else 0
                if pct > 0:
                    pct = (pct * float(100))

                buffer = [name, " - ", str(pct), "%"]
                msg = "".join(buffer)
                print msg
                #print "%s - %s %" % (name, str(pct))
                util.sleep(.5)
        except Exception, ex:
            try:
                temp.delete()
            except:
                pass

            raise ex


    for uri, file in queue:
        download(uri, file)



    # file = util.file("~/iktg_august_ames_480p_1000.mp4")
    # temp = file.parent.file("%s.tmp" % file.uri)
    # temp.delete()
    #
    # def on_download(temp):
    #     uri = temp.uri
    #     uri = uri[0:len(uri) - 4]
    #     file = temp.parent.file(uri)
    #     file.parent(temp.uri).move(file, overwrite=True)
    #
    #
    #
    # uri = file.read_text()
    # request = util.request(uri)
    # file_size = request.size
    #
    # callback = util.curry(on_download, temp)
    # request.download(temp, async=True, callback=callback)
    # while temp.exists is False:
    #     util.sleep(.01)
    # while True:
    #     if temp.exists is False:
    #         break
    #
    #     kb = temp.kb
    #     pct = round((kb / file_size), 2) if kb > 0 else 0
    #     if pct > 0:
    #         pct = (pct * float(100))
    #     print "{pct}%".format(pct=pct)
    #
    #     # print "%s of %s" % (str(kb), str(file_size))
    #     util.sleep(.5)
    #
    # # kb = request.size
    # #
    # # #size = util.fetch_file_size(uri)
    # # print size
    # #util.download(uri, file)

    raw_input("...")

init()
quit()

# from fuze.db import *
# #from crawlers import *
#
# import math
#
# class CircleBuffer(object):
#     def __init__(self, list):
#         self.ix = 0
#         self.list = list
#         self.max = len(list)
#
#     def increment(self, *count):
#         count = 1 if len(count) == 0 else count[0]
#         ix = self.ix
#         ix = (ix + count)
#         while ix >= self.max:
#             diff = (ix - self.max)
#             ix = diff
#         self.ix = ix
#         return self
#
#     def decrement(self, *count):
#         count = 1 if len(count) == 0 else count[0]
#         ix = self.ix
#         ix = (ix - count)
#         while ix < 0:
#             diff = (self.max + ix)
#             ix = diff
#         self.ix = ix
#         return self
#
#     def slide(self, pct):
#         ix = math.ceil(round((float(self.max) * float(pct)), 2))
#         self.ix = int(ix)
#         return self
#
#     def transpose(self, invert=False):
#         ix = self.ix
#         if ix == 0:
#             self.list.reverse()
#             return self
#
#         pfx = self.list[0:ix]
#         sfx = self.list[ix:]
#         if invert is True:
#             pfx.reverse()
#             sfx.reverse()
#
#         self.list = sfx
#         self.list.extend(pfx)
#         return self
#
#     @property
#     def index(self):
#         return self.ix
#
#     @property
#     def value(self):
#         return self.list[self.ix]
#
#     def __repr__(self):
#         return "Buffer[{ix}] > {value}".format(ix=self.ix, value=self.value)
#
#     def __str__(self):
#         return self.__repr__()
#
# def tester(pwd):
#     models = "eJxdkk2O2zAMha+iAxC9g+2kmfzOIAZm0R1jEzERmRpIcjrK6fvkboouLFg0yff40RfOnCamo2Y2dg01UcXThk0HpsMPdwhsxrSTEO/KuJokaqNmk+J62npf6MhZhVpBL/oInundC2o++Ib3Tm1cU+gk6tn1s+aJ9k/IUaOziLsWNjpzvIcMA9uneDWhA5sINV6+NbkulpTZ0xkd7hEOfrJlrR2WiHSutnnEvV+nOXCa1agxTOW2tIs8iOvoog+mjSRUFvpkLyiC4jWkVFy7pIl6L0+t2iNGXiR6Rps+y9cEIFJNrqpXwcMIiseEJ2WcR56lMF3CrLA5TPgk9MtXJueqe2JYNUBZKoSp0DZWxC3HG0dEfovkf6TeKvaJWmVDVscxrFQaG6NUtD7MNWyjYrTTMvy/IljV1wt+UF9o/3oVtxH/NdUme7tHHcEQJ0PJS6E+eBukCkUk+JWt6ZIrTPwLQjsfgKsyBNS/u6Q3waKxbcy94UdAvAtW3R91voFeAZtnLZKAfmceQ/2XTmJL0scf6VDhpg=="
#     models = util.inflate(models)
#     models = models.split(",")
#     models = util.dedupe(models)
#     pwd = util.hash(pwd)
#     if pwd[0] == "0":
#         models.reverse()
#
#     lst = constants.LETTERS
#     letters = {}
#     for x, c in enumerate(lst):
#         letters[c.lower()] = x
#
#     print pwd
#
#     digits = []
#     for c in pwd:
#         if c.isdigit():
#             if c == "0":
#                 digits.append(int(c))
#             else:
#                 digits.append(round((float(int(c)) / float(10)), 2))
#             continue
#         digits.append(letters[c])
#
#     buffer = CircleBuffer(models)
#
#     if digits[len(digits) - 1] == 0:
#         buffer.slide(.25)
#         total = sum([int(d) for d in digits])
#         if total % 2 == 0:
#             buffer.transpose(invert=True)
#         else:
#             buffer.transpose()
#
#         digits = digits[0:len(digits) - 1]
#         total = str(total)
#         total = total.replace("0", "")
#         for c in total:
#             digits.append(int(c))
#
#     for digit in digits:
#         print buffer
#         if digit == 0:
#             buffer.transpose()
#             continue
#
#         if isinstance(digit, float):
#             buffer.slide(digit)
#         else:
#             buffer.increment(digit)
#
# #from fuze import terminal
# #from pivotal.tracker import Tracker
# from pivotal import Tracker
#
# def init():
#     tracker = Tracker({"token": "48c168c732fccd52961ddebcc7dc75fc", "database": "/Work/prototype/fuze/"})
#     story = tracker.story("Topferral V1")
#     print story.label
#
#     # stories = tracker.stories
#     # for story in stories:
#     #     print story.label
#     # #tracker.sync()
#     # #tracker.sync(accounts=False, projects=False, stories=False)
#
#
#
# init()
# quit()
#
#
# def start():
#
#     # models = "eJxdksGy2jAMRff6inxB/yEBCg8CfZNMu+hOJBqihyMztkNrvr7XaRdvuogntmXp6lzVY1CmCyeOE9NJExtXNdVBxdGWTQem45fq6NmMaS8+3JSxNYnUBE0muerpu0s6M+2cy3TipEKNICW1y5Dp3Tumb07wvgne34U6xf87X3G+URvXN9SKOq76WdNEdZycZORTo7cnJFGts0jVZTY6c7j5BJFbcY+ppNo9BZFCRzYRqp381lhtQo6JHZ2R9hYg9ytbKtH1EhDOpUcese/X1lH+NiVvSBJnlK0NLKod7QMPUm3oondGxYgUmX6wE7yGhgNrUdr5GHPVLHGi3slTi5YRvBYJjpGtT/KYQFOK+lVFJ/gYh+KAoVXGeuJZMtzws0L2MOFK6KcrJM+lfMuQbiC3FFJThsgPtAKLdqGsDYcrB1z9Ekmfah6KeRM1yoaoDQe/4qptDFKMcH4uxzYqWoVn/xsNzfp6lTGxYe1V6O31ytU/A7CzW9ARhLEyyhUkvXc2SPEwIh5FA+LcaoDpgpaOZbqkgNXEf+2ng2BOMCygsOW7x/nGW2mh9aEMEG7mh5ZBna9AmwHuqQUfDDW6iEfMmUdfhrUVW6LeqVuu+dMDxjyNKzEQ3TsPH/8AaCMGaA=="
#     # models = util.inflate(models)
#     # models = models.split("\n")
#     # models = util.dedupe(models)
#     WoW.start_fetch().destroy()
#
#     #WoW.preview(models).destroy()
#     #WoW.preview().destroy()
#
#
#     # print "DOWNLOAD NATASHA STUFF!"
#     # WoW.fetch_natasha().destroy()
#     #WoW.preview().destroy()
#
#     #WoW.start_fetch().destroy()
#     # WoW.cleanup_content().destroy()
#     # WoW.fetch_images().destroy()
#     #WoW.launch().destroy()
#
#     # WoW.start_fetch().destroy()
#
#
#
# start()
#
# quit()
