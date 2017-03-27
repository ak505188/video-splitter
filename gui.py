import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class Window(QMainWindow):
    splits = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.resize(320, 240)
        self.setWindowTitle('Video Splitter')

        self.input_le = QLineEdit(self)
        self.input_le.move(130, 22)

        # Button to select video
        self.input_btn = QPushButton('Video', self)
        self.input_btn.move(20, 20)
        self.input_btn.setShortcut('Ctrl+O')
        self.input_btn.setStatusTip('Select video to split.')
        self.input_btn.clicked.connect(self.inputFileDialog)

        self.show()

    def inputFileDialog(self):
        self.input = QFileDialog.getOpenFileName(self, 'Select video to split', '.')
        if self.input:
            print(self.input[0])
            self.input_le.setText(str(self.input[0]))

    def addSplit(self):
        time_le = QLineEdit(self)
        if len(self.splits) > 0:
            y = self.splits[-1]['y'] + 33
        else:
            y = 0
        time_le.move(0, y)
        self.splits.append({ 'le': time_le, 'x': 0, 'y': y })


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
