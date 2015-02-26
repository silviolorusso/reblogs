#!/usr/bin/python

'''
take a screenshot of a webpage
'''

# MODULES

import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

# VARIABLES

my_url = 'http://nasahistory.tumblr.com/post/111883935036/this-is-a-great-view-of-the-space-shuttle-rearing'
my_title = 'missile.png'

# FUNCTIONS

class Screenshot(QWebView):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)

    def capture(self, url, filename, width, height):
        self.load(QUrl(url))
        self.wait_load()
        # set to webpage size
        frame = self.page().mainFrame()
        size = frame.contentsSize()
        size.setWidth(width)
        size.setHeight(height)
        # disable scrollbars    
        frame.setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        frame.setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff) 
        self.page().setViewportSize(size)
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        print '\nSaving', filename, 'from', url
        image.save(filename)

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True

# WORK

if __name__ == '__main__':
	s = Screenshot()
	s.capture(my_url, my_filename, 1000, 2000)