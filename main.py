import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import isodate

# See http://www.vdr-wiki.de/wiki/index.php/Info
# See page 40 at https://www.etsi.org/deliver/etsi_en/300400_300499/300468/01.12.01_40/en_300468v011201o.pdf
FORMATS = {
    '1': {'type': 'video', 'format': 'MPEG2'},
    '2': {'type': 'audio', 'format': 'MPEG1'},
    '3': {'type': 'subtitles'},
    '4': {'type': 'audio', 'format': 'AC3'},
    '5': {'type': 'video', 'format': 'H.264'},
    '6': {'type': 'video', 'format': 'HEAAC'},
    '7': {'type': 'audio', 'format': 'DTS'},
    '8': {'type': 'data', 'format': 'SRM/CPCM'},
    '9': {'type': 'video', 'format': 'HEVC'}
}

# See http://www.vdr-wiki.de/wiki/index.php/Info
# See page 40 at https://www.etsi.org/deliver/etsi_en/300400_300499/300468/01.12.01_40/en_300468v011201o.pdf
VIDEO_FORMATS = {
    '01': {'aspect_ratio': '4:3', 'quality': 'SD'},
    '05': {'aspect_ratio': '4:3', 'quality': 'SD'},
    '02': {'aspect_ratio': '16:9', 'quality': 'SD'},
    '04': {'aspect_ratio': '16:9', 'quality': 'SD'},
    '03': {'aspect_ratio': '16:9', 'quality': 'SD'},
    '06': {'aspect_ratio': '16:9', 'quality': 'SD'},
    '07': {'aspect_ratio': '16:9', 'quality': 'SD'},
    '08': {'aspect_ratio': '16:9', 'quality': 'SD'},
    '09': {'aspect_ratio': '4:3', 'quality': 'HD'},
    '0D': {'aspect_ratio': '4:3', 'quality': 'HD'},
}

# See http://www.vdr-wiki.de/wiki/index.php/Info
# See page 40 at https://www.etsi.org/deliver/etsi_en/300400_300499/300468/01.12.01_40/en_300468v011201o.pdf
AUDIO_FORMATS = {
    '01': {'format': 'mono'},
    '03': {'format': 'stereo'},
    '05': {'format': 'Dolby Digital'}
}


def parse_channel(info: dict, value: str):
    channel_info = value.split(' ', 1)
    info['channel'] = {
        'id': channel_info[0],
        'name': channel_info[1]
    }


def parse_time(info: dict, value: str):
    value = value.split(' ')
    date = datetime.fromtimestamp(int(value[1]), tz=timezone.utc)
    duration = timedelta(seconds=int(value[2]))
    info['date'] = date.isoformat()
    info['duration'] = isodate.duration_isoformat(duration)


def parse_framerate(info: dict, value: str):
    info['framerate'] = int(value)


def parse_lifetime(info: dict, value: str):
    info['lifetime'] = int(value)


def parse_priority(info: dict, value: str):
    info['framerate'] = int(value)


def parse_age_restriction(info: dict, value: str):
    info['framerate'] = int(value)


def parse_title(info: dict, value: str):
    info['title'] = value


def parse_subtitle(info: dict, value: str):
    info['subtitle'] = value


def parse_description(info: dict, value: str):
    info['description'] = value


def parse_technical_details(info: dict, value: str):
    value = value.split(' ', 3)
    details = dict()
    stream = FORMATS[value[0]]
    details.update(stream)
    if stream['type'] == 'video':
        video_format = VIDEO_FORMATS[value[1]]
        details.update(video_format)
    elif stream['type'] == 'audio':
        audio_format = AUDIO_FORMATS[value[1]]
        details.update(audio_format)

    if len(value) > 2:
        details['language'] = value[2]
    if len(value) > 3:
        details['description'] = value[3]

    if 'technical_details' in info:
        info['technical_details'].append(details)
    else:
        info['technical_details'] = [details]


def parse_genre(info: dict, value: str):
    genres = value.split()
    if 'genres' in info:
        info['genres'].extend(genres)
    else:
        info['genres'] = genres


PARSING_FUNCTIONS = {
    'C': parse_channel,
    'T': parse_title,
    'S': parse_subtitle,
    'D': parse_description,
    'E': parse_time,
    'F': parse_framerate,
    'L': parse_lifetime,
    'P': parse_priority,
    'X': parse_technical_details,
    'R': parse_age_restriction,
    'G': parse_genre
}


def parse_line(line: str, info: dict):
    key, value = line.split(' ', 1)
    if key not in PARSING_FUNCTIONS:
        return
    value = value.strip()
    if key in PARSING_FUNCTIONS:
        function = PARSING_FUNCTIONS[key]
        function(info, value)


def parse_file(path: Path) -> dict:
    with open(path) as file:
        info = dict()
        for line in file:
            parse_line(line, info)
    return info


def write_json_file(info_path: Path, content: dict):
    json_path = info_path.with_suffix('.json')
    with open(json_path, 'w') as file:
        json.dump(content, file, indent=' ', ensure_ascii=False)


def main():
    filename = Path('test.rec.info')
    info = parse_file(filename)
    write_json_file(filename, info)


main()
