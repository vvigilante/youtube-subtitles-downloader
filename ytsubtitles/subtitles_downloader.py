import sys,os
import urllib.request
import urllib.parse
import json
import html
import argparse
from .srt_converter import to_srt


class TrackNotFoundException(Exception):
    pass


class VideoParsingException(Exception):
    pass


def download_subs_arguments():
    parser = argparse.ArgumentParser(description=
                                     'Download subtitles from youtube.')
    parser.add_argument('video',
                        help="Video id from youtube.")
    parser.add_argument('--lang', default='en',
                        help='The subs language')
    args = parser.parse_args()
    try:
        v_id = args.video.split("watch?v=")[1]
    except IndexError:
        try:
            v_id = args.video.split("youtu.be/")[1]
        except IndexError:
            v_id = args.video
    __download_subs__(v_id, args.lang)


def __download_subs__(video_identifier, target_language):
    video_info = __get_video_info__(video_identifier)
    try:
        track_urls = __get_sub_track_urls__(video_info)
        target_track_url = __select_target_language_track_url(track_urls,
                                                              target_language)
        subs_data = __get_subs_data__(target_track_url)
        print(to_srt(subs_data))
    except VideoParsingException as e:
        print(str(e))
    except TrackNotFoundException:
        print('Track not found for language %s' % target_language)


def __get_video_info__(video_id):
    """ Get video info. Scraping code inspired to:
    https://github.com/syzer/youtube-captions-scraper/blob/master/src/index.js
    """
    contents = urllib.request.urlopen(
        "https://youtube.com/get_video_info?video_id=%s&hl=en" % video_id) \
        .read()
    contents = contents.decode('utf-8')
    return urllib.parse.parse_qs(contents)


def __get_sub_track_urls__(video_info):
    try:
        video_response = json.loads(video_info['player_response'][0])
        caption_tracks = \
            video_response['captions']['playerCaptionsTracklistRenderer'][
                'captionTracks']
        return {caption_track["languageCode"]: caption_track["baseUrl"]
                for caption_track in caption_tracks}
    except KeyError as e:
        print(video_info, file=sys.stderr)
        raise VideoParsingException("Error retrieving metadata. "
                        "The video may be non-existing or be licensed.")


def __select_target_language_track_url(track_urls, target_language):
    try:
        return track_urls[target_language]
    except KeyError:
        raise TrackNotFoundException()


def __get_subs_data__(subs_url):
    contents = urllib.request.urlopen(subs_url).read()
    contents = contents.decode('utf-8')
    return html.unescape(contents)
