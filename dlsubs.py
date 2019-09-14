import urllib.request
import urllib.parse
import json
import sys
import re
import html

# Conversion code from http://code.activestate.com/recipes/577459-convert-a-youtube-transcript-in-srt-subtitle/
pat = re.compile(r'<?text start="(\d+\.\d+)" dur="(\d+\.\d+)">(.*)</text>?')

def parseLine(text):
    """Parse a subtitle."""
    m = re.match(pat, text)
    if m:
        return (m.group(1), m.group(2), m.group(3))
    else:
        return None

def formatSrtTime(secTime):
    """Convert a time in seconds (google's transcript) to srt time format."""
    sec, micro = str(secTime).split('.')
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return "{:02}:{:02}:{:02},{}".format(h,m,s,micro)

def convertHtml(text):
    """A few HTML encodings replacements.
    &amp;#39; to '
    &amp;quot; to "
    """
    return text.replace('&amp;#39;', "'").replace('&amp;quot;', '"')

def printSrtLine(i, elms):
    """Print a subtitle in srt format."""
    return "{}\n{} --> {}\n{}\n\n".format(i, formatSrtTime(elms[0]), formatSrtTime(float(elms[0])+float(elms[1])), convertHtml(elms[2]))

def tosrt(buf):
    outsrt=[]
    buf = "".join(buf.replace('\n','')).split('><')
    i = 0
    for text in buf:
        parsed = parseLine(text)
        if parsed:
            i += 1
            outsrt.append(printSrtLine(i, parsed))
    outsrt_string = ''.join(outsrt)
    return outsrt_string



# Scraping code inspired to https://github.com/syzer/youtube-captions-scraper/blob/master/src/index.js

def get_video_info(video_id):
    contents = urllib.request.urlopen("https://youtube.com/get_video_info?video_id=%s&hl=en" % video_id).read()
    contents = contents.decode('utf-8')
    #contents = urllib.parse.unquote(contents)
    return urllib.parse.parse_qs(contents)
def get_sub_track_url(video_info, lang='it'):
    v = json.loads(video_info['player_response'][0])
    tracks_l = v['captions']['playerCaptionsTracklistRenderer']['captionTracks']
    for t in tracks_l:
        if lang == t['languageCode']:
            return t['baseUrl']
    return None
def get_subs_data(subsurl):
    contents = urllib.request.urlopen(subsurl).read()
    contents = contents.decode('utf-8')
    return html.unescape(contents)



def main(video_id, target_lang='it'):
    info = get_video_info(video_id)
    track_url = get_sub_track_url(info, target_lang)
    if track_url is None:
        print('Track not found for language %s' % target_lang)
    else:
        subs_data = get_subs_data(track_url)
        print(tosrt(subs_data))


if __name__=='__main__':
    video_id = 'rS2KlPC-E54'
    target_lang = 'it'
    if len(sys.argv) > 1:
        video_id = sys.argv[1]
    if len(sys.argv) > 2:
        target_lang = sys.argv[2]
    main(video_id, target_lang)