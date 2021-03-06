import sys
import textwrap
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

from ffmpeg import FFMpeg
import utils
import getffmpeg

class Window(QWidget):
    segmentLayout = QVBoxLayout()
    segments = []
    ffmpeg_path = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        start = QLabel('Start')
        end   = QLabel('End')
        name  = QLabel('Name')

        self.inputEdit = QLineEdit()

        inputBtn = QPushButton('Video')
        inputBtn.setShortcut('Ctrl+O')
        inputBtn.setToolTip('Select video to split.')
        inputBtn.clicked.connect(self.inputFileDialog)

        runBtn = QPushButton('Run')
        runBtn.setToolTip('Split Video.')
        runBtn.clicked.connect(self.run)

        addBtn = QPushButton('Add')
        addBtn.setToolTip('Add another split.')
        addBtn.clicked.connect(self.addSegment)

        labelLayout = QHBoxLayout()
        labelLayout.addWidget(start)
        labelLayout.addWidget(end)
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

        # Check if FFmpeg is installed
        ffmpeg_path = getffmpeg.checkFFmpeg()
        if isinstance(ffmpeg_path, str):
            self.ffmpeg_path = ffmpeg_path + '.exe'
        elif ffmpeg_path is False:
            ffmpegMsg = QMessageBox()
            if sys.platform == 'win32':
                ffmpegMsg.setText('Downloading FFmpeg locally.')
                getffmpeg.getFFmpeg()
            else:
                ffmpegMsg.setText(textwrap.dedent('''
                    It appears you do not have FFmpeg installed.
                    To run this program you need to have FFmpeg
                    installed and in your path.

                    To install: https://ffmpeg.org/
                '''))
            ffmpegMsg.exec()

    def addSegment(self):
        hlayout = QHBoxLayout()

        startEdit = QLineEdit()
        endEdit   = QLineEdit()
        nameEdit  = QLineEdit()

        # timestampsEdit.setToolTip(textwrap.dedent('''
        #     The times to cut to make the output video.
        #     ex:
        #     3:00-480 Will cut the video from 3 minutes to 8 minutes
        #     240+4:30 Will cut the video 4 minutes to 8:30 minutes
        #     Plus means the second number will be the length of the vid
        #     Minus means the second number will be the timestamp of where
        #     the cut stops.
        # '''))

        # '''
        # nameEdit.setToolTip(textwrap.dedent('''
        #     Name of the outputed video file. Make sure
        #     to end with the same extention.
        #         ex: Input file:  in.mp4
        #         All outputs should end with .mp4
        # '''))

        hlayout.addWidget(startEdit)
        hlayout.addWidget(endEdit)
        hlayout.addWidget(nameEdit)

        self.segmentLayout.addLayout(hlayout)

        self.segments.append({
            'start' : startEdit,
            'end'   : endEdit,
            'name'  : nameEdit,
        })


    def inputFileDialog(self):
        self.input = QFileDialog.getOpenFileName(self, 'Select video to split', '.')
        if self.input:
            self.inputEdit.setText(str(self.input[0]))

    def run(self):
        inputfile = self.inputEdit.displayText()
        for index, segment in enumerate(self.segments):
            timestamps = {}
            filenames  = {}

            filenames['input']  = inputfile
            filenames['output'] = segment['name'].displayText()

            try:
                timestamps['start'] = utils.parse_time(segment['start'].displayText())
                timestamps['end']   = utils.parse_time(segment['end'].displayText())
            except ValueError:
                QMessageBox.about(self, 'Error', 'Segment %d is invalid.' % (index + 1))
                return

            FFMpeg(filenames, timestamps, path=self.ffmpeg_path).run()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
