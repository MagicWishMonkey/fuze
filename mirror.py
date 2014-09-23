#!/usr/bin/env python
import os
import sys
import time
import shutil
import codecs
import urllib
import urllib2
import requests
import threading
from threading import Lock
from BeautifulSoup import BeautifulSoup


class util:
    __print_lock__ = threading.Lock()

    @staticmethod
    def trace(*messages):
        util.__print_lock__.acquire()
        if len(messages) == 0:
            sys.stdout.write("\n")
            util.__print_lock__.release()
            return

        for message in messages:
            sys.stdout.write(message)
            sys.stdout.write("\n")

        util.__print_lock__.release()

    @staticmethod
    def unroll(lst):
        if lst is None:
            return []
        def list_or_tuple(x):
            return isinstance(x, (list, tuple))
        def flatten(seq, to_expand=list_or_tuple):
            for i in seq:
                if to_expand(i):
                    for sub in flatten(i, to_expand):
                        yield sub
                else:
                    yield i

        if list_or_tuple(lst) is False:
            return [lst]

        unravelled = []
        for o in flatten(lst):
            unravelled.append(o)
        return unravelled

    @staticmethod
    def ask(message, repeat=False):
        while True:
            sys.stdout.write(message)
            txt = sys.stdin.readline().strip()
            if len(txt) == 0:
                if repeat is False:
                    return None
                continue

            if txt.isdigit() is True:
                return int(txt)

            if len(txt) < 10:
                t = txt.lower()
                if t == "true" or t == "yes" or t == "y":
                    return True
                if t == "false" or t == "no" or t == "n":
                    return False
            return txt

    @staticmethod
    def digitize(txt):
        if isinstance(txt, basestring) is False:
            if isinstance(txt, (int, float)) is True:
                return txt
            return None

        buffer = []
        integer = True
        for c in txt:
            if c.isdigit() is True:
                buffer.append(c)
                continue

            if integer is False or len(buffer) == 0:
                continue

            if c == ".":
                integer = False
                buffer.append(c)

        if len(buffer) == 0:
            return None

        txt = "".join(buffer)
        if integer is False:
            return float(txt)
        return int(txt)

    @staticmethod
    def json(o, pretty=True):
        import simplejson as json

        if pretty is True:
            return json.dumps(o, indent=4)
        return json.dumps(o)

    @staticmethod
    def unjson(data):
        import simplejson as json
        return json.loads(data, strict=False)

    @staticmethod
    def base64(txt):
        import base64
        txt = base64.encodestring(txt)
        return txt

    @staticmethod
    def unbase64(txt):
        import base64
        txt = base64.decodestring(txt)
        return txt

    @staticmethod
    def compress(data):
        import zlib
        return zlib.compress(data)

    @staticmethod
    def decompress(data):
        import zlib
        return zlib.decompress(data)

    @staticmethod
    def curry(f, *a, **kw):
        def curried(*more_a, **more_kw):
            return f(*(a + more_a), **dict(kw, **more_kw))
        return curried

    @staticmethod
    def commonest(values, limit=None):
        if len(values) == 0:
            return None

        from collections import Counter
        c = Counter(values)
        common = c.most_common(5)
        common = common[0][0]
        return common

    @staticmethod
    def sleep(seconds=.01):
        time.sleep(seconds)

    @staticmethod
    def guid(*length):
        import uuid
        import hashlib
        txt = hashlib.md5(str(uuid.uuid1())).hexdigest()
        if len(length) == 0:
            return txt
        length = length[0]
        txt = txt[:length]
        return txt

    @staticmethod
    def hash(data):
        import hashlib
        txt = hashlib.md5(data).hexdigest()
        return txt


class io:
    @staticmethod
    def read_lines(path):
        data = io.read_file(path, text=True)
        lines = data.split("\n")
        lines = [l.strip() for l in lines if l != "\r"]
        lines = [l for l in lines if len(l) > 0]
        return lines

    @staticmethod
    def read_text(path):
        return io.read_file(path, text=True)

    @staticmethod
    def read_file(path, text=True):
        if text is False:
            try:
                with open(path, "rb") as f:
                    data = f.read()
                    return data
            except Exception, ex:
                message = "Error reading file [ {file} ] -> {message}".format(file=path, message=ex.message)
                print message
                raise Exception(message)

        try:
            with codecs.open(path, "r", "utf-8") as f:
                data = f.read()
                return data
        except Exception, ex:
            message = "Error reading file [ {file} ] -> {message}".format(file=path, message=ex.message)
            print message
            raise Exception(message)

    @staticmethod
    def write_text(path, data):
        return io.write_file(path, data, text=True)

    @staticmethod
    def write_file(path, data, text=False):
        if isinstance(data, list) is True:
            data = "\n".join(data)

        if io.exists(path) is True:
            os.remove(path)

        if text is False:
            try:
                with open(path, "wb") as f:
                    f.write(data)
            except Exception, ex:
                message = "Error writing file [ {file} ] -> {message}".format(file=path, message=ex.message)
                print message
                raise Exception(message)

        try:
            with codecs.open(path, "w", "utf-8") as f:
                f.write(data)
        except Exception, ex:
            message = "Error writing file [ {file} ] -> {message}".format(file=path, message=ex.message)
            print message
            raise Exception(message)

    @staticmethod
    def create(path, overwrite=False):
        if io.exists(path) is True:
            if overwrite is False:
                return
            io.delete(path)

        try:
            os.makedirs(path)
        except Exception, ex:
            if io.exists(path) is True:
                return
            raise ex

    @staticmethod
    def delete(uri):
        if io.exists(uri) is False:
            return

        if uri.endswith(os.sep) is False:
            try:
                os.remove(uri)
            except Exception, ex:
                message = "Error deleting file '{uri}' -> {message}".format(uri=uri, message=ex.message)
                print message
            return

        #this is a folder
        for current, dirs, files in os.walk(uri):
            for file in files:
                path = os.path.join(current, file)
                os.remove(path)

            for dir in dirs:
                path = "{path}{name}{sep}".format(path=current, name=dir, sep=os.sep)
                io.delete(path)

        try:
            os.rmdir(uri)
        except Exception, ex:
            message = "Error deleting folder '{uri}' -> {message}".format(uri=uri, message=ex.message)
            print message

    @staticmethod
    def file_size(uri):
        st = os.stat(uri)
        bytes = st.st_size
        kb = 1 if bytes <= 1024 else int(round((float(bytes) / float(1024)), 2))
        return kb

    @staticmethod
    def move(src, dst):
        shutil.move(src, dst)

    @staticmethod
    def exists(uri):
        """Return true if the file/folder exists."""
        return True if os.path.exists(uri) else False

    @staticmethod
    def relative(uri, path):
        new_uri = os.path.join(uri, path)
        new_uri = os.path.normpath(new_uri)
        return new_uri

    @staticmethod
    def temp_file(folder, name):
        guid = util.guid(6)
        name = "{name}_{guid}.temp".format(name=name, guid=guid)
        path = os.path.join(folder, name)
        return path

    @staticmethod
    def rename(src, dst):
        if dst.find(os.sep) == -1:
            parts = src.split(os.sep)
            parts[len(parts) - 1] = dst
            dst = os.sep.join(parts)

        #print "%s -> %s" % (src, dst)
        os.rename(src, dst)

    @staticmethod
    def name(uri):
        parts = uri.split(os.sep)
        return parts[len(parts) - 1]

    @staticmethod
    def files(uri, recursive=False):
        return io.contents(uri, recursive=recursive)[1]

    @staticmethod
    def folders(uri, recursive=False):
        return io.contents(uri, recursive=recursive)[0]

    @staticmethod
    def contents(uri, recursive=False):
        def __walk__(folder_list, file_list, recursive, uri):
            for current, folders, files in os.walk(uri):
                for file in files:
                    file = os.path.join(current, file)
                    file_list.append(file)

                for folder in folders:
                    folder = os.path.join(current, folder)
                    folder_list.append(folder)

                    if recursive is True:
                        __walk__(folder_list, file_list, recursive, folder)
        folders, files = [], []
        __walk__(folders, files, recursive, uri)
        return folders, files


class web:
    __types__ = {}

    @staticmethod
    def find_type(type):
        types = web.__types__
        if len(types) == 0:
            videos = ["mov", "mp4", "wmv", "mpg", "mpeg", "avi", "3g2", "3gp", "asf", "asx", "flv", "m4v", "swf", "vob"]
            images = ["jpg", "jpeg", "png", "gif", "bmp", "psd", "tif", "tiff", "ai", "eps", "es", "svg"]
            audio = ["mp3", "m38", "aif", "iff", "m4a", "mid", "mpa", "wav", "wma"]
            documents = ["pdf", "epub", "mobi", "opf", "prc", "tpz", "azw", "aa", "aax", "txt", "rtf", "lit", "doc", "docx"]
            types = {
                "videos": videos,
                "images": images,
                "audio": audio,
                "documents": documents
            }
            web.__types__ = types

        type = type.strip().split("?")[0]
        if type.find(".") > -1:
            parts = type.split(".")
            type = parts[len(parts) - 1]

        type = type.strip().lower()
        if type in types["videos"]:
            return "video"

        if type in types["images"]:
            return "image"

        if type in types["audio"]:
            return "audio"

        if type in types["documents"]:
            return "document"

        return None

    @staticmethod
    def fetch_file_size(uri):
        try:
            request = requests.head(uri)
            headers = request.headers
            for header in headers:
                if header.lower() == "content-length":
                    bytes = headers[header]
                    if isinstance(bytes, basestring) is True:
                        bytes = int(bytes)

                    kb = 1 if bytes < 1024 else round((float(bytes) / float(1024)), 2)
                    if kb < 1024:
                        return kb
                    mb = round((float(kb) / float(1024)), 2)
                    return mb
            return 0
        except:
            return 0

    @staticmethod
    def crawl(uri):
        def clean_name(txt):
            txt = txt.strip()
            if txt[0] == ".":
                txt = "_%s" % txt[1:]

            txt = txt.replace("&amp;", "&")
            txt = txt.replace("&gt;", ">")
            txt = txt.replace("&lt;", "<")
            txt = txt.replace("?", " ")
            txt = txt.replace("<", " ")
            txt = txt.replace(">", " ")
            txt = txt.replace("|", " ")
            txt = txt.replace("\\", " ")
            txt = txt.replace("/", " ")
            txt = txt.replace(":", " ")
            txt = txt.replace("*", " ")
            txt = txt.replace('"', " ")
            txt = txt.strip()
            while txt.find("  ") > -1:
                txt = txt.replace("  ", " ")
            return txt

        def parse_size(tag, name, href):
            size = None
            try:
                parent = tag.parent.parent
                content = parent.contents[3]
                size = content.next
                if size is not None and len(size) > 1:
                    size = size.strip().lower()
                    digits = util.digitize(size)
                    if digits is not None:
                        unit = "kb"
                        if size.find("m") > -1 or size.find("mb") > -1:
                            unit = "mb"
                        elif size.find("g") > -1 or size.find("gb") > -1:
                            unit = "gb"

                        if unit == "kb":
                            if digits > 1024:
                                digits = round((float(digits) / float(1024)), 2)
                        elif unit == "gb":
                            digits = round((float(digits) * float(1024)), 2)
                        return digits
            except:
                size = None


            parent = tag.parent
            attrs = parent.attrs
            if len([a for a in attrs if a[0] == "class" and a[1] == "wrap"]) > 0:
                try:
                    text = parent.text
                    parts = text.strip().split(" ")
                    size = parts[len(parts) - 1].lower()
                    if size.find("k") > -1:
                        parts = size.split("k")
                        size = float(parts[0].strip())
                        size = round((size / float(1024)), 2)
                    elif size.find("m") > -1:
                        parts = size.split("m")
                        size = round(float(parts[0].strip()), 2)
                    elif size.find("g") > -1:
                        parts = size.split("g")
                        size = float(parts[0].strip())
                        size = round((size * float(1024)), 2)
                    else:
                        size = None
                except:
                    size = None

            if size is not None and util.digitize(size) is None:
                size = None

            if size is None:
                try:
                    txt = tag.nextSibling
                    txt = txt.strip()
                    parts = txt.split(" ")
                    txt = parts[len(parts) - 1]
                    size = util.digitize(txt)
                    if size is not None:
                        txt = txt.lower()
                        if txt.find("k") > -1 or txt.find("kb") > -1:
                            size = round((size / float(1024)), 2)
                        elif txt.find("g") > -1 or txt.find("gb") > -1:
                            size = round((size * float(1024)), 2)
                        elif txt.find("m") > -1 or txt.find("mb") > -1:
                            size = round(float(size), 2)
                        else:
                            size = None
                except:
                    size = None


            if size is None:
                ext = name.strip().lower().split("?")[0]
                ext = ext.split("/")
                ext = ext[len(ext) - 1]
                if ext.endswith(".ico"):
                    size = 0
                else:
                    size = web.fetch_file_size(href)
            return size

        util.trace("crawling > %s" % uri)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36')]
        response = opener.open(uri)
        html = response.read()
        soup = BeautifulSoup(html)
        tags = soup.findAll("a")

        folders, files = [], []

        cnt = len(tags)
        for x in xrange(cnt):
            tag, href = tags[x], None

            try:
                href = [attr[1] for attr in tag.attrs if attr[0].lower() == "href"][0]
            except:
                pass

            if href is None or len(href.strip()) < 2 or href.lower().find("?c=") == 0:
                continue

            name = tag.text.strip()
            if len(name) == 0:
                continue

            name = clean_name(name)
            lowercase = name.lower()
            if lowercase == "parent directory" or lowercase == "favicon.ico":
                continue

            folder = True if href.strip().endswith("/") is True else False
            if href[0] == "/" and len(href) > 1:
                href = href[1:]

            #relative = href
            href = "%s%s" % (uri, href)
            name = urllib.unquote(name)
            if name.endswith("..") or name.endswith("..>"):
                parts = href.split("?")[0].split("/")
                name = parts[len(parts) - 1]
                parts = name.split(".")
                parts.pop()
                name = ".".join(parts)
                name = urllib.unquote(name)

            if folder is True:
                folders.append({"uri": href, "name": name})
                continue

            file_name = name.strip().lower()
            if file_name.split(".")[0] == "favicon":
                continue
            size = parse_size(tag, name, href)
            file_name = name
            try:
                parts = href.split("?")[0].split("/")
                sfx = parts[len(parts) - 1]
                if sfx.find(".") > -1:
                    file_name = sfx
            except:
                pass
            type = web.find_type(file_name)
            if type is None:
                if size is None or size == 0:
                    #files.append({"uri": href, "name": name, "type": "file"})
                    files.append({"uri": href, "name": name})
                else:
                    #files.append({"uri": href, "name": name, "type": "file", "size": size})
                    files.append({"uri": href, "name": name, "size": size})
            else:
                if size is None or size == 0:
                    #files.append({"uri": href, "name": name, "type": "file", "category": type})
                    files.append({"uri": href, "name": name, "type": type})
                else:
                    #files.append({"uri": href, "name": name, "type": "file", "category": type, "size": size})
                    files.append({"uri": href, "name": name, "type": type, "size": size})

        return folders, files


class Buffer(object):
    def __init__(self):
        self.__list__ = []
        self.__lock__ = Lock()
        self.__loading__ = False
        self.__closed__ = False

    @property
    def closed(self):
        return self.__closed__

    def close(self):
        self.__closed__ = True
        return self

    def extend(self, values):
        with self.__lock__:
            self.__list__.extend(values)
        return self

    def append(self, value):
        with self.__lock__:
            if isinstance(value, list) is True:
                map(self.__list__.append, value)
            else:
                self.__list__.append(value)

        return self

    def set(self, value):
        return self.append(value)

    def get(self):
        with self.__lock__:
            try:
                o = self.__list__.pop()
                return o
            except:
                return None

    def pop(self):
        return self.get()

    def __iter__(self):
        return self.next()

    def next(self):
        while True:
            # if self.empty is True:
            #     if self.__loading__ is True:
            #         time.sleep(.01)
            #         continue
            #     break

            o = self.pop()
            if o is None and self.empty is True:
                if self.__loading__ is True:
                    time.sleep(.01)
                    continue
                break

            yield o

    def __repr__(self):
        return "Buffer#{cnt}".format(cnt=self.__len__())

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.__list__)

    @property
    def empty(self):
        cnt = len(self.__list__)
        return True if cnt == 0 else False


class Worker(object):
    def __init__(self, fn):
        import uuid
        import hashlib
        self.uuid = "Worker#{uuid}".format(uuid=hashlib.md5(str(uuid.uuid4())).hexdigest()[0:10])
        self.fn = fn
        self.thread = None
        self.running = False
        self.complete = False
        self.result = None

        self.thread = threading.Thread(target=self.__run__, name=self.uuid)
        self.thread.setDaemon(True)

    def __run__(self):
        self.running = True
        fn = self.fn
        try:
            self.result = fn()
        except Exception, ex:
            message = "Error executing thread function: %s" % ex.message
            print message
            self.result = Exception(message, ex)
        finally:
            self.running = False
            self.complete = True
            self.thread = None


    def start(self):
        if self.running is True or self.thread is None:
            print "This thread has already been run!"
            return self

        self.running = True
        self.thread.start()
        return self

    def abort(self):
        if self.thread is None:
            return self

        try:
            self.thread.join()
        except:# Exception, ex:
            pass
        self.thread = None
        self.running = False
        self.complete = False
        return self

    @property
    def failed(self):
        return True if isinstance(self.result, Exception) is True else False


settings = {
    "thread_count": 8,
    "ignore": []
}


def build_spider(uri):
    name = uri.strip().split("?")[0].lower()
    if name.startswith("http://"):
        name = name[7:len(name) - 1]
    elif name.startswith("https://"):
        name = name[8:len(name) - 1]
    if name.startswith("www."):
        name = name[4:len(name) - 1]

    name = name.split("/")[0]

    def recurse(queue, *folder, **kwd):
        recursive = kwd.get("recursive", True)
        apply_filter = kwd.get("apply_filter", True)
        folder = None if len(folder) == 0 else folder[0]
        if folder is None:
            folder = queue.pop()
            while folder is None:
                if queue.empty is True:
                    return
                time.sleep(.25)

        folders, files = web.crawl(folder["uri"])
        if len(folders) > 0:
            if apply_filter is True:
                filters = settings["ignore"]
                if len(filters) > 0:
                    for x in xrange(len(folders)):
                        f = folders[x]
                        name = f["name"].strip().lower()
                        for filter in filters:
                            if name.startswith(filter) == -1:
                                continue
                            folders[x] = None
                    folders = [f for f in folders if f is not None]
            if len(folders) > 0:
                folder["folders"] = folders
                queue.extend(folders)

        if len(files) > 0:
            types = [f.get("type", None) for f in files if f.get("type", None) is not None]
            if len(types) > 0:
                type = util.commonest(types)
                folder["content"] = type

            folder["files"] = files

            sizes = []
            for f in files:
                fs = f.get("size", None)
                if fs is not None:
                    sizes.append(fs)
                    if fs > 1024:
                        fs = round((float(fs) / float(1024)), 2)
                        fs = str(fs)
                        if fs.endswith(".0"):
                            fs = fs.split(".")[0]
                        fs = "%s GB" % fs
                    elif fs < 1:
                        fs = round(fs, 2)
                        fs = str(fs)
                        if fs.endswith(".0"):
                            fs = fs.split(".")[0]
                        fs = "%s KB" % fs
                    else:
                        fs = round(fs, 2)
                        fs = str(fs)
                        if fs.endswith(".0"):
                            fs = fs.split(".")[0]
                        fs = "%s MB" % fs
                    f["size"] = fs

            if len(sizes) > 0:
                size = sum(sizes)
                if size > 1024:
                    size = round((float(size) / float(1024)), 2)
                    size = str(size)
                    if size.endswith(".0"):
                        size = size.split(".")[0]

                    size = "%s GB" % size
                elif size < 1:
                    size = round(size, 2)
                    size = str(size)
                    if size.endswith(".0"):
                        size = size.split(".")[0]
                    size = "%s KB" % size
                else:
                    size = round(size, 2)
                    size = str(size)
                    if size.endswith(".0"):
                        size = size.split(".")[0]
                    size = "%s MB" % size
                folder["size"] = size

        if recursive is False:
            return

        recurse(queue)

    queue = Buffer()
    root = {
        "uri": uri,
        "name": name
    }
    recurse(queue, root, recursive=False, apply_filter=False)

    workers = []
    for x in xrange(settings["thread_count"]):
        worker = Worker(util.curry(recurse, queue))
        workers.append(worker)

    [worker.start() for worker in workers]
    time.sleep(.25)
    recurse(queue)
    while queue.empty is False:
        time.sleep(.1)

    queue.close()

    workers = [worker for worker in workers if worker.running is True]
    while len(workers) > 0:
        time.sleep(.1)
        workers = [worker for worker in workers if worker.running is True]

    #data = util.json(root, pretty=True)
    #print data
    return root


path = os.getcwd()
path = "/Users/ron/Downloads/_NS_/demo"


#uri = "http://www.extremeteens.net/trial/content/upload/"
#uri = "http://www.extremeteens.net/trial/content/upload/ALABS1265268065/"
uri = "http://files.diydharma.org/"
#uri = "http://files.diydharma.org/Dalai_Lama/"
uri = "http://groundlingsvoice.com/pron/"

spider_json_file = io.relative(path, "__spider__.json")
spider_html_file = io.relative(path, "__spider__.html")
#io.delete(spider_json_file)
#io.delete(spider_html_file)
spider = {}
if io.exists(spider_json_file) is False:
    spider = build_spider(uri)
    spider["_"] = {
        "uri": uri
    }

    data = util.json(spider, pretty=True)
    io.write_text(spider_json_file, data)
else:
    spider = util.unjson(io.read_text(spider_json_file))



def build_spider_page(spider):
    def attach_file(indents, buffer, file):
        name, uri, size, type = file["name"], file["uri"], file.get("size", None), file.get("type", None)

        out_pad = "".join([" " for x in xrange(len(indents) - 1)])
        pad = "%s " % out_pad
        buffer.append("%s<ul class='files'>" % out_pad)
        if type is not None:
            type = "<div style='width: 25px; height: 25px;' class='{type}_icon' alt='{type}'></div>".format(type=type)
        else:
            type = "<div style='width: 25px; height: 25px;'>&nbsp;</div>"

        buffer.append("%s<li>%s</li>" % (pad, type))


        link = "<a href='{uri}'>{name}</a>".format(uri=uri, name=name)
        buffer.append("%s<li>%s</li>" % (pad, link))

        if size is not None:
            size = "<div style='width: 75px; height: 25px;' class='size_cell'>{size}</div>".format(size=size)
        else:
            size = "<div style='width: 75px; height: 25px;' class='size_cell'>&nbsp;</div>"
        buffer.append("%s<li>%s</li>" % (pad, size))
        buffer.append("%s</ul>" % out_pad)


    def attach_folder(indents, buffer, folder):
        name, uri, size, type = folder["name"], folder["uri"], folder.get("size", None), folder.get("type", None)
        if len(name) == 0:
            name = uri.split("?")[0]
            if name.endswith("/"):
                name = name[0:len(name) - 1]
            parts = name.split("/")
            name = parts[len(parts) - 1]
            name = urllib2.unquote(name)


        indents.append(None)
        out_pad = "".join([" " for x in xrange(len(indents) - 1)])
        pad = "%s " % out_pad


        buffer.append("%s<ul class='folders'>" % out_pad)
        if type is not None:
            type = "<div class='{type}_icon' alt='{type}'></div>".format(type=type)
        else:
            type = "<div class='blank_icon'>&nbsp;</div>"

        if size is not None:
            size = "<div class='size_cell'>{size}</div>".format(size=size)
        else:
            size = "<div class='size_cell'>&nbsp;</div>"

        link = "<a href='{uri}'>{name}</a>".format(uri=uri, name=name)
        buffer.append(pad)
        buffer.append("<li>")
        buffer.append(type)
        buffer.append(link)
        buffer.append(size)
        buffer.append("</li>")


        # buffer.append("%s<li>%s</li>" % (pad, type))
        #
        #
        #
        # buffer.append("%s<li>%s</li>" % (pad, link))
        #
        # if size is not None:
        #     size = "<div style='width: 75px; height: 25px;' class='size_cell'>{size}</div>".format(size=size)
        # else:
        #     size = "<div style='width: 75px; height: 25px;' class='size_cell'>&nbsp;</div>"
        # buffer.append("%s<li>%s</li>" % (pad, size))
        files = folder.get("files", [])
        if len(files) > 0:
            indents.append(None)
            indents.append(None)
            # buffer.append("%s<li>" % pad)
            # #buffer.append("%s <div style='padding-left: 20px; background: pink; height: 5px;'>" % pad)
            # for file in files:
            #     attach_file(indents, buffer, file)
            # #buffer.append("%s </div>" % pad)
            # buffer.append("%s</li>" % pad)
            indents.pop()
            indents.pop()

        folders = folder.get("folders", [])
        if len(folders) > 0:
            indents.append(None)
            indents.append(None)
            buffer.append("%s<li>" % pad)
            for folder in folders:
                attach_folder(indents, buffer, folder)
            buffer.append("%s</li>" % pad)
            indents.pop()
            indents.pop()

        indents.pop()
        buffer.append("%s</ul>" % out_pad)

    indents = [None]
    buffer = []
    folders = spider.get("folders", [])
    for folder in folders:
        attach_folder(indents, buffer, folder)

    files = spider.get("files", [])
    if len(files) > 0:
        buffer.append("<li>")
        #buffer.append("<div style='padding-left: 20px; background: pink; height: 5px;'>")
        for file in files:
            attach_file(indents, buffer, file)
        #buffer.append("</div>")
        buffer.append("</li>")

    inner = "\n".join(buffer)

    buffer = []
    buffer.append("<div>")
    buffer.append(inner)
    buffer.append("</div>")
    inner = "\n".join(buffer)
    return inner



inner = build_spider_page(spider)
html = io.read_text(io.relative(path, "__template__.html"))
html = html.replace("@inner@", inner)
#print html

io.write_text(spider_html_file, html)





#mirror("http://files.diydharma.org/")




# folders, files = crawl("http://www.miyanabooks.com/artnudeangels/")
# for folder in folders:
#     uri = folder["uri"]
#     crawl(uri)