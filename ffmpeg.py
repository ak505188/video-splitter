import subprocess

class FFMpeg(object):
    def __init__(self, input_file, output_file, start=0, end=None, codec='copy'):
        self.input_file = input_file
        self.output_file = output_file
        # We are assuming that start and end are floats and represent duration
        self.start = start
        self.end = end
        self.codec = codec

    def run(self):
        self._create_command()
        print(self.args)
        subprocess.call(self.args)

    def _create_command(self):
        args = ['ffmpeg']

        # Appending -i after -ss and -t makes ffmpeg start
        # splitting at the first keyframe. Otherwise it
        # will have a blank screen with audio until it
        # reaches the first keyframe
        # https://superuser.com/questions/358155/how-can-i-avoid-a-few-seconds-of-blank-video-when-using-vcodec-copy/358969

        args.append('-ss')
        # Adding an extra .5 seconds to the startime as a hack
        # to avoid blackscreen on splits at the start of the video
        args.append(str(float(self.start + .5)))

        args.append('-i')
        args.append(self.input_file)

        args.append('-t')
        args.append(str(self.end))

        args.append('-c')
        args.append(self.codec)

        args.append(self.output_file)
        self.args = args
