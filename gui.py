import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from ffmpeg import FFMpeg
import utils

class Window(QWidget):
    segmentLayout = QVBoxLayout()
    segments = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        timestamps = QLabel('Timestamps')
        name = QLabel('Name')

        self.inputEdit = QLineEdit()

        inputBtn = QPushButton('Video')
        inputBtn.setShortcut('Ctrl+O')
        inputBtn.setStatusTip('Select video to split.')
        inputBtn.clicked.connect(self.inputFileDialog)

        runBtn = QPushButton('Run')
        runBtn.clicked.connect(self.run)

        addBtn = QPushButton('Add')
        addBtn.clicked.connect(self.addSegment)

        labelLayout = QHBoxLayout()
        labelLayout.addWidget(timestamps)
        labelLayout.addWidget(name)

        runLayout = QHBoxLayout()
        runLayout.addWidget(inputBtn)
        runLayout.addWidget(self.inputEdit)
        runLayout.addWidget(addBtn)
        runLayout.addWidget(runBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(labelLayout)
        mainLayout.addLayout(self.segmentLayout)
        mainLayout.addLayout(runLayout)

        self.setLayout(mainLayout)

        self.addSegment()

        self.setWindowTitle('Video Splitter')
        self.show()

    def addSegment(self):
        hlayout = QHBoxLayout()

        timestampsEdit = QLineEdit()
        nameEdit = QLineEdit()

        hlayout.addWidget(timestampsEdit)
        hlayout.addWidget(nameEdit)

        self.segmentLayout.addLayout(hlayout)

        self.segments.append({
            'timestamps': timestampsEdit,
            'name': nameEdit,
        })


    def inputFileDialog(self):
        self.input = QFileDialog.getOpenFileName(self, 'Select video to split', '.')
        if self.input:
            self.inputEdit.setText(str(self.input[0]))

    def run(self):
        input = self.inputEdit.displayText()
        for segment in self.segments:
            name  = segment['name'].displayText()
            timestamps = utils.timestr_to_timestamps(segment['timestamps'].displayText())
            start = timestamps['start']
            end = timestamps['end']
            FFMpeg(input, name, start, end).run()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
