from PyQt6 import QtWidgets, QtGui

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(300, 300)
        f = open("photo.jpg", "rb")
        d = f.read()
        f.close()
        self.img = QtGui.QImage.fromData(d, "JPG")

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.img)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Класс QImage")
    window.show()
    sys.exit(app.exec())
