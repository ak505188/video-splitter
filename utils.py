import re

def times_to_duration(start, end):
    return(time_to_duration(end) - time_to_duration(start))

def time_to_duration(time):
    try:
        return float(time)
    except ValueError:
        rgx = '^(?:(?:(?P<hours>[0-9]+):)?(?:(?P<minutes>[0-5]?[0-9]):))?(?P<seconds>[0-5]?[0-9])$'
        tm_lst = re.search(rgx, time)
        hours =  int(tm_lst.group('hours')) if tm_lst.group('hours') else 0
        minutes = int(tm_lst.group('minutes')) if tm_lst.group('minutes') else 0
        seconds = int(tm_lst.group('seconds')) if tm_lst.group('seconds') else 0
        return float(hours * 3600 + minutes * 60 + seconds)
