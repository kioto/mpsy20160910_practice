#!/usr/bin/env python

import time
import threading
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QImage, QPainter, QPen, qRgb
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

# setting
WINDOW_WIDTH  = 200
WINDOW_HEIGHT = 200
PEN_WIDTH = 10
REC_TIME = 1.0                  # sec

# constant
STATUS_READY   = 0
STATUS_RECODE  = 1
STATUS_ANALYZE = 2
STATUS_RESULT  = 3

class ScribbleWidget(QWidget):
    def __init__(self, parent=None, status_bar=None):
        super(ScribbleWidget, self).__init__(parent)

        self.setAttribute(Qt.WA_StaticContents)
        self._active_flag = False
        self._pen_color = Qt.black
        self._image = None
        self._last_point = QPoint()
        self._status = -1
        self._status_bar = status_bar
        self._set_status(STATUS_READY)
        self.value = -1
        self._timer = None

    def _set_status(self, status):
        if status == STATUS_READY:
            self._print_msg('Click view and start')
        elif status == STATUS_RECODE:
            self._image.fill(qRgb(255, 255, 255))
            self.update()
            self._print_msg('Rrecoding...')
        elif status == STATUS_ANALYZE:
            self._print_msg('Analyzing...')
        elif status == STATUS_RESULT:
            self._print_msg('Result: {}' % (self.value))
            
        self._status = status
        
    def _print_msg(self, msg):
        if self._status_bar:
            self._status_bar.showMessage(msg)

    def _wait_analyze(self):
        time.sleep(REC_TIME)
        self._set_status(STATUS_ANALYZE)
        
    def _save_image(self, fileName, fileFormat):
        visibleImage = self._image
        self._resize_image(visibleImage, self.size())

        if visibleImage.save(fileName, fileFormat):
            return True
        else:
            return False

    def _clear_image(self):
        self._image.fill(qRgb(255, 255, 255))
        self.update()

    def mousePressEvent(self, event):
        # reset timer
        if self._timer:
            self._timer.cancel()
            self._timer.join()
            del self._timer
            self._timer = None

        if self._status != STATUS_RECODE:
            return
        if event.button() == Qt.LeftButton:
            self._last_point = event.pos()
            self._active_flag = True

    def mouseMoveEvent(self, event):
        if self._status != STATUS_RECODE:
            return
        if (event.buttons() & Qt.LeftButton) and self._active_flag:
            self._draw_line(event.pos())

    def mouseReleaseEvent(self, event):
        if self._status == STATUS_READY:
            self._set_status(STATUS_RECODE)
            return
        elif self._status == STATUS_RESULT:
            self._set_status(STATUS_READY)
            return
        elif self._status == STATUS_ANALYZE:
            return
        
        if event.button() == Qt.LeftButton and self._active_flag:
            self._draw_line(event.pos())
            self._active_flag = False

        # set timer
        self._timer = threading.Timer(REC_TIME, self._wait_analyze)
        self._timer.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        dirtyRect = event.rect()
        painter.drawImage(dirtyRect, self._image, dirtyRect)

    def resizeEvent(self, event):
        self._image = QImage(QSize(self.width() + 128, self.height() + 128),
                             QImage.Format_RGB32)
        if self._status == STATUS_READY:
            self._image.fill(qRgb(128, 128, 128))
        else:
            self._image.fill(qRgb(255, 255, 255))
            
        painter = QPainter(self._image)
        painter.drawImage(QPoint(0, 0), self._image)
        self.update()
        super(ScribbleWidget, self).resizeEvent(event)
        return

    def _draw_line(self, point):
        painter = QPainter(self._image)
        painter.setPen(QPen(self._pen_color,
                            PEN_WIDTH,
                            Qt.SolidLine,
                            Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self._last_point, point)

        rad = PEN_WIDTH / 2 + 2
        rect = QRect(self._last_point, point).normalized()
        rect = rect.adjusted(-rad, -rad, +rad, +rad)
        self.update(rect)
        self._last_point = QPoint(point)

    def _resize_image(self, image, new_size):
        new_image = QImage(new_size, QImage.Format_RGB32)
        new_image.fill(qRgb(255, 255, 255))
        painter = QPainter(new_image)
        painter.drawImage(QPoint(0, 0), image)
        self._image = new_image

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.widget = ScribbleWidget(status_bar=self.statusBar())
        self.setCentralWidget(self.widget)

        self.setWindowTitle("MNIST")
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))

        #self.statusBar().showMessage('Ready')
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# end of file
