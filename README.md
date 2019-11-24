# Youtube subtitles downloader
Download closed captions from youtube videos (both manual and automatically generated), and convert them to srt format 

python implementation

## How to use
```bash
dlsubs --video=ZXD4X6INh7w --lang=it > out.srt
```
or
```bash
python3 dlsubs.py VIDEO_ID LANG > out.srt
```

## Example
```bash
python3 dlsubs.py rS2KlPC-E54 it > out.srt
```

# Acknowledgements
- Original js implementation: https://github.com/syzer/youtube-captions-scraper/blob/master/src/index.js
- SRT conversion: http://code.activestate.com/recipes/577459-convert-a-youtube-transcript-in-srt-subtitle/
