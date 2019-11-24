import urllib.request
import urllib.parse
import json
import sys
import re
import html
import argparse


# Conversion code from
# http://code.activestate.com/recipes/577459-convert-a-youtube-transcript-in-srt-subtitle/
pat = re.compile(r'<?text start="(\d+\.\d+)" dur="(\d+\.\d+)">(.*)</text>?')


def parse_line(text):
    """Parse a subtitle."""
    m = re.match(pat, text)
    if m:
        return m.group(1), m.group(2), m.group(3)
    else:
        return None


def format_srt_time(sec_time):
    """Convert a time in seconds (google's transcript) to srt time format."""
    sec, micro = str(sec_time).split('.')
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return "{:02}:{:02}:{:02},{}".format(h,m,s,micro)


def convert_html(text):
    """A few HTML encodings replacements.
    &amp;#39; to '
    &amp;quot; to "
    """
    return text.replace('&amp;#39;', "'").replace('&amp;quot;', '"')


def print_srt_line(i, elms):
    """Print a subtitle in srt format."""
    return "{}\n{} --> {}\n{}\n\n".format(i, format_srt_time(elms[0]),
                                          format_srt_time(float(elms[0]) +
                                                          float(elms[1])),
                                          convert_html(elms[2]))


def to_srt(buf):
    out_srt = []
    buf = "".join(buf.replace('\n', '')).split('><')
    i = 0
    for text in buf:
        parsed = parse_line(text)
        if parsed:
            i += 1
            out_srt.append(print_srt_line(i, parsed))
    out_srt_string = ''.join(out_srt)
    return out_srt_string


# Scraping code inspired to
# https://github.com/syzer/youtube-captions-scraper/blob/master/src/index.js
def get_video_info(video_id):
    contents = urllib.request.urlopen(
        "https://youtube.com/get_video_info?video_id=%s&hl=en" % video_id)\
        .read()
    contents = contents.decode('utf-8')
    # contents = urllib.parse.unquote(contents)
    return urllib.parse.parse_qs(contents)


def get_sub_track_url(video_info, lang='it'):
    try:
        v = json.loads(video_info['player_response'][0])
    except KeyError:
        raise Exception("Error retrieving metadata. The video may be non-existing.")
    tracks_l = v['captions']['playerCaptionsTracklistRenderer']['captionTracks']
    for t in tracks_l:
        if lang == t['languageCode']:
            return t['baseUrl']
    return None


def get_subs_data(subs_url):
    contents = urllib.request.urlopen(subs_url).read()
    contents = contents.decode('utf-8')
    return html.unescape(contents)


def download_subs(video_identifier, target_language):
    info = get_video_info(video_identifier)
    track_url = get_sub_track_url(info, target_language)
    if track_url is None:
        print('Track not found for language %s' % target_language)
    else:
        subs_data = get_subs_data(track_url)
        print(to_srt(subs_data))


def download_subs_arguments():
    parser = argparse.ArgumentParser(description='Download subtitles from youtube.')
    parser.add_argument('video',
                        help="Video id from youtube.")
    parser.add_argument('--lang', default='en',
                        help='The subs language')
    args = parser.parse_args()
    download_subs(args.video, args.lang)


if __name__ == '__main__':
    download_subs_arguments()
