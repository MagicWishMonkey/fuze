import urllib
import requests



class Request(object):
    def __init__(self, uri, *headers):
        self.__uri = uri
        self.__headers = {}
        self.__params = None
        self.__locals = None
        self.__method = "GET"

        if len(headers) > 0:
            header_table = self.__headers
            for header in headers:
                key, val = None, None
                if isinstance(header, basestring) is True:
                    parts = header.split(":") if header.find(":") > -1 else header.split("=")
                    if len(parts) < 2:
                        raise Exception("The header format is not valid.")
                    key = parts[0].strip()
                    val = ":".join(parts[1:]).strip() if header.find(":") > -1 else "=".join(parts[1:]).strip()
                else:
                    if isinstance(header, (tuple, list)) is False:
                        raise Exception("The header format is not valid.")
                    key, val = header[0], header[1]
                header_table[key.lower()] = val

    def set_local(self, key, val):
        tbl = self.__locals
        if tbl is None:
            self.__locals = {}
            tbl = self.__locals
        tbl[key] = val

    def get_local(self, key, default=None):
        tbl = self.__locals
        if tbl is None:
            return None
        try:
            return tbl[key]
        except KeyError:
            return default


    @property
    def headers(self):
        return self.__headers

    @property
    def uri(self):
        uri = self.__uri
        querystring = self.querystring
        if not querystring:
            return uri

        uri = "%s?%s" % (uri, querystring)
        return uri

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, method):
        method = method.strip().lower()
        if method == "get":
            self.__method = "GET"
        elif method == "post":
            self.__method = "POST"
        elif method == "head":
            self.__method = "HEAD"
        elif method == "delete":
            self.__method = "DELETE"
        else:
            raise Exception("The specified method is not supported: %s" % method.upper())

    def set_header(self, key, val):
        headers = self.__headers
        if key.lower() == "content-length":
            key = key.lower()

        if isinstance(val, basestring) is False:
            val = str(val)

        headers[key] = val
        return self

    def get_header(self, key):
        headers = self.__headers
        try:
            return headers[key.strip().lower()]
        except KeyError:
            return None

    def has_header(self, key):
        return True if self.get_header(key) else False

    def as_post(self):
        self.__method = "POST"
        return self

    def as_get(self):
        self.__method = "GET"
        return self


    # def POST(self):
    #     self._method = "POST"
    #     data = self.body
    #     if data is None:
    #         if self._form:
    #             data = urllib.urlencode(self._form)
    #             #data = "&".join(self._form)
    #             if self.content_type is None:
    #                 self.content_type = "application/x-www-form-urlencoded"
    #     if self.has_header("Content-Length") is False:
    #         if data:
    #             self.header("Content-Length", len(data))#(len(data) * 8))
    #         else:
    #             self.header("Content-Length", 0)
    #             #if data and self.has_header("Content-length") is False:
    #             #    self.header("Content-length", len(data))
    #
    #     if self.content_type is not None:
    #         self.header("Content-Type", self.content_type)
    #
    #     #print data
    #     uri = self.to_uri()
    #     #print uri
    #     headers = self.headers
    #     try:
    #         if headers and data:
    #             response = requests.post(uri, data=data, headers=headers, allow_redirects=True)
    #         elif data:
    #             response = requests.post(uri, data=data)
    #         elif headers:
    #             response = requests.post(uri, headers=headers)
    #         else:
    #             response = requests.post(uri)
    #
    #         status_code = response.status_code
    #         if status_code == 404 or status_code == 500:
    #             try:
    #                 from fusion import tools
    #                 if response.content is not None:
    #                     response = response.content
    #                 else:
    #                     response = response.text
    #
    #                 return tools.unjson(response)
    #             except:
    #                 pass
    #
    #             reason = response.reason
    #             raise HttpRequestException("[%s] Http request failed: %s" % (str(status_code), reason))
    #
    #         if response.content is not None:
    #             response = response.content
    #         else:
    #             response = response.text
    #
    #         if self.callback is not None:
    #             self.callback()
    #         return response
    #     except Exception, ex:
    #         if isinstance(ex, HttpRequestException) is True:
    #             raise ex
    #
    #         raise HttpRequestException(
    #             "Error with the HTTP POST request-> %s\n%s" % (uri, ex.message), ex
    #         )
    #
    # def GET(self, *fmt):
    #     self.method = "GET"
    #     data = self.body
    #     if data and self.has_header("Content-length") is False:
    #         self.header("Content-length", len(data))
    #
    #     uri = self.to_uri()
    #     #print uri
    #     #logger.info("http.GET %s" % uri)
    #     headers = self.headers
    #     try:
    #         if headers and data:
    #             response = requests.get(uri, data=data, headers=headers)
    #         elif data:
    #             response = requests.get(uri, data=data)
    #         elif headers:
    #             response = requests.get(uri, headers=headers)
    #         else:
    #             response = requests.get(uri)
    #
    #         status_code = response.status_code
    #         if status_code == 404 or status_code == 500:
    #             try:
    #                 from fusion import tools
    #                 if response.content is not None:
    #                     response = response.content
    #                 else:
    #                     response = response.text
    #
    #                 return tools.unjson(response)
    #             except:
    #                 pass
    #             reason = response.reason
    #             raise HttpRequestException("[%s] Http request failed: %s" % (str(status_code), reason))
    #
    #         if response.content is not None:
    #             response = response.content
    #         else:
    #             response = response.text
    #         if len(fmt) > 0:
    #             fmt = fmt[0]
    #             response = fmt(response)
    #         return response
    #     except Exception, ex:
    #         if isinstance(ex, HttpRequestException) is True:
    #             raise ex
    #
    #         raise HttpRequestException(
    #             "Error with the HTTP GET request-> %s\n%s" % (uri, ex.message), ex
    #         )


    @property
    def querystring(self):
        params = self.__params
        if not params:
            return ""

        buffer = []
        for key in params:
            val = params[key]
            if val is None:
                val = ""
            else:
                val = urllib.urlencode(str(val))
            buffer.append("%s=%s" % (key, val))

        txt = "&".join(buffer)
        return txt

    @classmethod
    def plugin(cls, plugin):
        name = plugin.func_name
        setattr(cls, name, plugin)

    @property
    def size(self):
        size = self.get_local("size")
        if size is not None:
            return size

        uri = self.__uri
        try:
            request = requests.head(uri)
            headers = request.headers
            for header in headers:
                if header.lower() == "content-length":
                    bytes = headers[header]
                    if isinstance(bytes, basestring) is True:
                        bytes = int(bytes)

                    kb = 1 if bytes < 1024 else round((float(bytes) / float(1024)), 2)
                    self.set_local("size", kb)
                    return kb
            return 0
        except:
            return 0

    def __str__(self):
        return self.uri

    def __repr__(self):
        return self.__str__()

@Request.plugin
def download(self, file, async=False, callback=None, block_size=1024):
    try:
        from fuze import util
    except:
        message = "Unable to import the fuze util module."
        raise Exception(message)

    if isinstance(file, basestring) is False:
        try:
            file = file.uri
        except Exception, ex:
            message = "Invalid file parameter! %s" % ex.message
            raise Exception(message)


    def __stream__(uri, file, flush_limit=1024, callback=None):
        if flush_limit is None or flush_limit < 1:
            flush_limit = 1024

        headers = {}
        headers["User-Agent"] = "Mozilla/5.0 Chrome/34.1.2222.1111 Safari/511.56"
        headers["Accept-Encoding"] = "gzip,deflate,compress"
        headers["Accept-Language"] = "en-US,en;q=0.8"
        headers["Referer"] = "https://www.google.com/"
        headers["Accept"] = "*/*"
        request = requests.get(uri, headers=headers, timeout=120, stream=True)

        try:
            bytes_total = 0
            flush_count = 0
            with open(file, 'wb') as f:
                for chunk in request.iter_content(chunk_size=10240):
                    if chunk is not None: # filter out keep-alive new chunks
                        f.write(chunk)
                        cnt = (len(chunk) * 1024)
                        bytes_total = (bytes_total + cnt)
                        flush_count = (flush_count + cnt)
                        if flush_count > flush_limit:
                            flush_count = 0
                            f.flush()
        except Exception, ex:
            message = "Error downloading the file: %s" % ex.message
            print message
            raise Exception(message)

        if callback is not None:
            callback()

    uri = self.uri
    fn = util.curry(__stream__, uri, file, flush_limit=block_size, callback=callback)
    if async is True:
        util.dispatch(fn)
        return self

    fn()
    return self




# def download(uri, file):
#     headers = {}
#     headers["User-Agent"] = "Mozilla/5.0 Chrome/34.1.2222.1111 Safari/511.56"
#     headers["Accept-Encoding"] = "gzip,deflate,compress"
#     headers["Accept-Language"] = "en-US,en;q=0.8"
#     headers["Referer"] = "https://www.google.com/"
#     headers["Accept"] = "*/*"
#     request = requests.get(uri, headers=headers, timeout=120, stream=True)
#
#     if isinstance(file, basestring) is True:
#         file = File(file)
#
#     temp = file.parent.file("%s.temp" % file.uri)
#     try:
#         flush_bytes = 0
#         with open(temp.uri, 'wb') as f:
#             for chunk in request.iter_content(chunk_size=10240):
#                 if chunk is not None: # filter out keep-alive new chunks
#                     f.write(chunk)
#                     #         flush_bytes = (flush_bytes + (len(chunk) * 1024))
#                     #         if flush_bytes > 1024:
#                     #             f.flush()
#                     #             flush_bytes = 0
#                     # if flush_bytes > 0:
#                     #     util.trace("Flushing {count} bytes...".format(count=flush_bytes))
#                     #     f.flush()
#     except Exception, ex:
#         message = "Error downloading the file: %s" % ex.message
#         print message
#
#
#     incomplete, retries = True, 0
#     while incomplete is True and retries < 5:
#         if retries > 0:
#             io.delete(temp)
#             util.sleep(5)
#
#         r = requests.get(uri, headers=headers, timeout=120, stream=True)
#         try:
#             flush_bytes = 0
#             with open(temp, 'wb') as f:
#                 for chunk in r.iter_content(chunk_size=10240):
#                     if chunk is not None: # filter out keep-alive new chunks
#                         f.write(chunk)
#                         flush_bytes = (flush_bytes + (len(chunk) * 1024))
#                         if flush_bytes > 1024:
#                             f.flush()
#                             flush_bytes = 0
#
#                 if flush_bytes > 0:
#                     util.trace("Flushing {count} bytes...".format(count=flush_bytes))
#                     f.flush()
#
#
#             io.move(temp, path)
#             file["size"] = io.file_size(path)
#             incomplete = False
#         except Exception, ex:
#             message = "Error downloading the file '{name}' -> {message}".format(name=name, message=ex.message)
#             util.trace(message)
#             retries = (retries + 1)

