import subprocess
import argparse
import json
import re
from ffmpeg import FFMpeg
import utils

parser = argparse.ArgumentParser(
    description='Split one video file into many',
    usage='python splitter.py')

parser.add_argument('-i', '--input', help='Path to input video', required=True)
parser.add_argument('-o', '--output', help='Name of output file')
parser.add_argument('-ss', '--start', help='Start of input to cut from', default=0)
parser.add_argument('-t', '--duration', help='Output duration')
parser.add_argument('-to', '--end', help='Output time end')

with open('timestamps.json') as output_json:
    outputs = json.load(output_json)

args = parser.parse_args()

for output in outputs:
    start = utils.time_to_duration(output['start'])
    if output['end']:
        end = utils.times_to_duration(output['start'], output['end'])
    else:
        end = output['duration']
    f = FFMpeg(args.input, output['name'], start, end).run()
