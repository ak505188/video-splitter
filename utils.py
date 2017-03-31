import re

def parse_time(time):
    try:
        return float(time)
    except ValueError:
        rgx = '^(?:(?:(?P<hours>[0-9]+):)?(?:(?P<minutes>[0-5]?[0-9]):))?(?P<seconds>[0-5]?[0-9])$'
        tm_lst = re.search(rgx, time)
        hours =  int(tm_lst.group('hours')) if tm_lst.group('hours') else 0
        minutes = int(tm_lst.group('minutes')) if tm_lst.group('minutes') else 0
        seconds = int(tm_lst.group('seconds')) if tm_lst.group('seconds') else 0
        return float(hours * 3600 + minutes * 60 + seconds)

def timestr_to_timestamps(line):
    rgx = '^(?P<start>[0-9:.]+)(?P<type>\+|-)(?P<end>[0-9:.]+)$'
    m = re.match(rgx, line)
    if m:
        start = parse_time(m.group('start'))
        end = parse_time(m.group('end'))

        # + Signifies duration
        # - Signifies timestamp
        # If timestamp should be converted to duration

        if '-' in m.group('type'):
            end = end - start
        return { 'start': start, 'end': end }
    # TODO: Handle non-match
    return None

def textfile_to_output(filename):
    f = open(filename)
    lines = f.readlines()
    outputs = []
    count = 1
    for line in lines:
        output = timestr_to_timestamps(line)
        # Temporary name generation
        output['name'] = str(count) + '.flv'
        outputs.append(output)
        count = count + 1
    return outputs
