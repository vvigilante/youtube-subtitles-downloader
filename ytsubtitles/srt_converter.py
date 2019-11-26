import re


# Conversion code from
# http://code.activestate.com/recipes/577459-convert-a-youtube-transcript-in-srt-subtitle/
pat = re.compile(r'<?text start="(\d+\.\d+)" dur="(\d+\.\d+)">(.*)</text>?')


def format_srt_time(sec_time):
    """Convert a time in seconds (google's transcript) to srt time format."""
    sec, micro = str(sec_time).split('.')
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return "{:02}:{:02}:{:02},{}".format(h, m, s, micro)


def print_srt_line(i, elms):
    """Print a subtitle in srt format."""
    return "{}\n{} --> {}\n{}\n\n".format(i, format_srt_time(elms[0]),
                                          format_srt_time(float(elms[0]) +
                                                          float(elms[1])),
                                          convert_html(elms[2]))


def convert_html(text):
    """A few HTML encodings replacements.
    &amp;#39; to '
    &amp;quot; to "
    """
    return text.replace('&amp;#39;', "'").replace('&amp;quot;', '"')

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


def parse_line(text):
    """Parse a subtitle."""
    m = re.match(pat, text)
    if m:
        return m.group(1), m.group(2), m.group(3)
    else:
        return None
