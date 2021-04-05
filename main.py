import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Tuple, Optional, Dict
import isodate

MAPPING = {
    'C': 'channel',
    'T': 'title',
    'S': 'subtitle',
    'D': 'description',
    'E': 'time',
    'F': 'framerate',
    'L': 'lifetime',
    'P': 'priority',
    'X': 'technical_details',
    'R': 'age_restriction'
}

# See http://www.vdr-wiki.de/wiki/index.php/Info
FORMATS = {
    '1': {'type': 'video', 'format': 'MPEG2'},
    '2': {'type': 'video', 'format': 'MPEG2'},
    '3': {'type': 'subtitles'},
    '4': {'type': 'video', 'format': 'AC3'},
    '5': {'type': 'video', 'format': 'H.264'},
    '6': {'type': 'video', 'format': 'HEAAC'}
}

VIDEO_FORMATS = {
    '01': {'aspect_ratio': '4:3', 'quality': 'sd'},
    '05': {'aspect_ratio': '4:3', 'quality': 'sd'},
    '02': {'aspect_ratio': '16:9', 'quality': 'sd'},
    '04': {'aspect_ratio': '16:9', 'quality': 'sd'},
    '03': {'aspect_ratio': '16:9', 'quality': 'sd'},
    '06': {'aspect_ratio': '16:9', 'quality': 'sd'},
    '07': {'aspect_ratio': '16:9', 'quality': 'sd'},
    '08': {'aspect_ratio': '16:9', 'quality': 'sd'},
    '09': {'aspect_ratio': '4:3', 'quality': 'hd'},
    '0D': {'aspect_ratio': '4:3', 'quality': 'hd'},
}


def parse_line(line: str, info: dict):
    key, value = line.split(' ', 1)
    if key not in MAPPING:
        return
    value = value.strip()
    key = MAPPING[key]
    if key == 'channel':
        # Remove astra settings
        channel = value.split(' ', 1)[1]
        info[key] = channel
    elif key == 'time':
        value = value.split(' ')
        date = datetime.fromtimestamp(int(value[1]), tz=timezone.utc)
        duration = timedelta(seconds=int(value[2]))
        info['date'] = date.isoformat()
        info['duration'] = isodate.duration_isoformat(duration)
    elif key == 'technical_details':
        value = value.split()
        technical_details = info[key] if key in info else list()
        technical_details.append(FORMATS[value[0]])
        info[key] = technical_details
    elif key == 'framerate':
        info[key] = int(value)
    elif key == 'lifetime':
        info[key] = int(value)
    elif key == 'priority':
        info[key] = int(value)
    else:
        # Adopt information unprocessed
        info[key] = value


def parse_file(path: Path) -> dict:
    with open(path, encoding='utf8') as file:
        info = dict()
        for line in file:
            parse_line(line, info)
    return info


def write_json_file(info_path: Path, content: Dict[str, str]):
    json_path = info_path.with_suffix('.json')
    with open(json_path, 'w') as file:
        json.dump(content, file, indent=' ', ensure_ascii=False)


def main():
    filename = Path('test.rec.info')
    info = parse_file(filename)
    print(info)
    write_json_file(filename, info)


main()
