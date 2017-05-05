'''
Class responsible for interacting with ffmpeg
'''

import subprocess

class FFMpeg(object):
    def __init__(self, filenames, timestamps, codec='copy', path=None):
        self.input_file = filenames['input']
        self.output_file = filenames['output']
        # We are assuming that start and end are floats and represent duration
        self.start = timestamps['start']
        self.end = timestamps['end']
        self.codec = codec
        self.args = ['ffmpeg']
        if path:
            self.args = [path]

    def run(self):
        self._create_command()
        subprocess.call(self.args)

    def _create_command(self):
        # Appending -i after -ss and -t makes ffmpeg start
        # splitting at the first keyframe. Otherwise it
        # will have a blank screen with audio until it
        # reaches the first keyframe
        # https://superuser.com/questions/358155/how-can-i-avoid-a-few-seconds-of-blank-video-when-using-vcodec-copy/358969

        self.args.append('-ss')
        # Adding an extra .5 seconds to the startime as a hack
        # to avoid blackscreen on splits at the start of the video
        self.args.append(str(float(self.start + .5)))

        self.args.append('-i')
        self.args.append(self.input_file)

        self.args.append('-t')
        self.args.append(str(self.end))

        self.args.append('-c')
        self.args.append(self.codec)

        self.args.append(self.output_file)
