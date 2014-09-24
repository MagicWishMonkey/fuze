class Clipboard:
    __instance__ = None

    def __init__(self):
        if Clipboard.__instance__ is None:
            Clipboard.__instance__ = self

            import platform, os
            if os.name == 'nt' or platform.system() == 'Windows':
                import ctypes
                def winGetClipboard():
                    ctypes.windll.user32.OpenClipboard(0)
                    pcontents = ctypes.windll.user32.GetClipboardData(1) # 1 is CF_TEXT
                    data = ctypes.c_char_p(pcontents).value
                    ctypes.windll.user32.CloseClipboard()
                    return data

                def winSetClipboard(text):
                    GMEM_DDESHARE = 0x2000
                    ctypes.windll.user32.OpenClipboard(0)
                    ctypes.windll.user32.EmptyClipboard()
                    try:
                        # works on Python 2 (bytes() only takes one argument)
                        hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE, len(bytes(text))+1)
                    except TypeError:
                        # works on Python 3 (bytes() requires an encoding)
                        hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE, len(bytes(text, 'ascii'))+1)
                    pchData = ctypes.windll.kernel32.GlobalLock(hCd)
                    try:
                        # works on Python 2 (bytes() only takes one argument)
                        ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text))
                    except TypeError:
                        # works on Python 3 (bytes() requires an encoding)
                        ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text, 'ascii'))
                    ctypes.windll.kernel32.GlobalUnlock(hCd)
                    ctypes.windll.user32.SetClipboardData(1,hCd)
                    ctypes.windll.user32.CloseClipboard()
                self.getter = winGetClipboard
                self.setter = winSetClipboard

            elif os.name == 'mac' or platform.system() == 'Darwin':
                def macSetClipboard(text):
                    outf = os.popen('pbcopy', 'w')
                    outf.write(text)
                    outf.close()

                def macGetClipboard():
                    outf = os.popen('pbpaste', 'r')
                    content = outf.read()
                    outf.close()
                    return content

                self.getter = macGetClipboard
                self.setter = macSetClipboard
            elif os.name == 'posix' or platform.system() == 'Linux':
                xclipExists = os.system('which xclip') == 0
                if xclipExists:
                    self.getter = xclipGetClipboard
                    self.setter = xclipSetClipboard
                else:
                    xselExists = os.system('which xsel') == 0
                    if xselExists:
                        self.getter = xselGetClipboard
                        self.setter = xselSetClipboard
                    try:
                        import gtk
                        self.getter = gtkGetClipboard
                        self.setter = gtkSetClipboard
                    except:
                        try:
                            import PyQt4.QtCore
                            import PyQt4.QtGui
                            app = QApplication([])
                            cb = PyQt4.QtGui.QApplication.clipboard()
                            self.getter = qtGetClipboard
                            self.setter = qtSetClipboard
                        except:
                            raise Exception('Pyperclip requires the gtk or PyQt4 module installed, or the xclip command.')

    @staticmethod
    def instance():
        clipboard = Clipboard.__instance__
        if clipboard is not None:
            return clipboard
        clipboard = Clipboard()
        return clipboard

    @staticmethod
    def read():
        return Clipboard.instance().getter()

    @staticmethod
    def write(o):
        Clipboard.instance().setter(o)


def read():
    return Clipboard.read()


def write(o):
    Clipboard.write(o)