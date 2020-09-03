# ffmpeg_video_cutter
Python CLI front-end for FFmpeg that helps to split/cut out multiple fragments from any video

Let's say you need to review important info in the recorded video from your work meeting, without being distracted by
jokes from colleagues and the boss's stories about his beloved dog. Then FFmpeg Video Cutter will help you to make
things right. The tool has the ability to cut as many unnecessary video fragments as you want so you can concentrate
on important information.

### Dependencies
- ffmpeg

### CLI setup
```shell script
git clone https://github.com/rooty0/ffmpeg_video_cutter.git
cd ffmpeg_video_cutter
mkdir profiles && cp profile_example.yaml profiles/anyname.yaml
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

## How to start

While watching a video using your favorite multimedia player just make notes what you want to cut out, something like:
```shell script
vi profiles/anyname.yaml
```
``` yaml
---
input: "zoom_call_0.mp4"
output: "zoom_call_0_cut.mp4"
cut_method: delete  # we're going to delete following video fragments from a video call
timeframe:
  - from: start   # waiting for people to join the conference
    to: 4m
  - from: 10m11s  # awkward silence
    to: 15m50s
  - from: 30m5s   # Off-Topic Discussion
    to: end
```

Now just run the tool to cut out the video fragments, and you'll get clean conference video call that you can watch
again and again in future without spending extra time skipping the off-topic discussion

```shell script
venv/bin/python cut.py -p profiles/anyname.yaml
```
