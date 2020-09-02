#!/usr/bin/env python3
import os
import yaml
import argparse
import datetime
import re
import subprocess

from pprint import pprint


class FFCut:
    def __init__(self, profile_path, ffmpeg_path="/usr/local/bin/ffmpeg", ffprobe_path="/usr/local/bin/ffprobe"):
        self.PROFILE = self.load_profile(profile_path)
        self.FFMPEG_PATH = ffmpeg_path
        self.FFPROBE_PATH = ffprobe_path
        self.VIDEO_DURATION_SECONDS = self.get_video_duration(self.PROFILE['input'])
        self.DATE_REGEX = re.compile(r'((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
        self.INVERT_TIMEFRAME = True if self.PROFILE['cut_method'] == 'delete' else False

    @staticmethod
    def load_profile(profile_path):
        with open(profile_path) as file:
            return yaml.full_load(file)

    @staticmethod
    def get_video_duration(video_path):

        video_call = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_path
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if video_call.returncode != 0:
            raise Exception(video_call.stderr)

        return float(video_call.stdout)

    def convert_to_seconds(self, time_string):
        if time_string == 'start':
            return 0
        elif time_string == 'end':
            return self.VIDEO_DURATION_SECONDS

        time_dict = self.DATE_REGEX.match(time_string)
        if not time_dict:
            raise Exception("can not parse {}, fix your config".format(time_string))

        # filter out results like: {'hours': None, 'minutes': '1', 'seconds': '6'} before pass it to timedelta()
        time_dict_filtered = {key: int(value) for (key, value) in time_dict.groupdict().items() if value is not None}

        return datetime.timedelta(**time_dict_filtered).seconds

    def generate_time_pairs(self):

        time_pair_list = []
        for time_pair in self.PROFILE['timeframe']:
            time_pair_list.append(
                (
                    self.convert_to_seconds(time_pair['from']),
                    self.convert_to_seconds(time_pair['to'])
                )
            )

        # pprint(time_pair_list)

        return time_pair_list

    def invert_time_pairs(self):
        time_pair_list = self.generate_time_pairs()

        inverted_time_pair = []

        if time_pair_list[0][0] != 0:
            inverted_time_pair.append(
                (0, time_pair_list[0][0])  # don't put -1 in here
            )
            if time_pair_list[0][0] == time_pair_list[0][1]:
                time_pair_list[0][1] += 1

        for i in range(0, len(time_pair_list)-1):
            # first = time_pair_list[i][1] + 1
            first = time_pair_list[i][1]
            second = time_pair_list[i+1][0]
            if first == second:
                second += 1
            inverted_time_pair.append(
                (
                    first,
                    second,
                )
            )

        if time_pair_list[-1][1] != self.VIDEO_DURATION_SECONDS:
            inverted_time_pair.append(
                (time_pair_list[-1][1], self.VIDEO_DURATION_SECONDS)
            )
        return inverted_time_pair

    def show_video_info(self):
        subprocess.run(["ffprobe", self.PROFILE['input']])

    def get_selected_timeframe(self):

        if self.INVERT_TIMEFRAME:
            return self.invert_time_pairs()
        else:
            return self.generate_time_pairs()

    def format_ffmpeg_call(self):

        selected_time_list = self.get_selected_timeframe()

        format_cut_time = []
        for cut_time in selected_time_list:
            format_cut_time.append(
                "between(t,{},{})".format(cut_time[0], cut_time[1])
            )

        between_from_template = "+".join(format_cut_time)
        return [
            "ffmpeg",
            # "-hwaccel", "videotoolbox",
            # "--hwdec=auto",
            "-i", self.PROFILE['input'],
            "-vf", "select='{}',setpts=N/FRAME_RATE/TB".format(between_from_template),
            "-af", "aselect='{}', asetpts=N/SR/TB".format(between_from_template),
            self.PROFILE['output']
        ]

    def apply_cut(self):
        subprocess.run(self.format_ffmpeg_call())


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='\033[93m[[ FFMPEG Cutter ]]\033[0m',
    )
    parser.add_argument(
        '--profile', '-p', dest='profile', help='yaml file with details', required=True,
    )
    parser.add_argument(
        '--show-command', dest='show_command', help='do not run ffmpeg, just show a command', action="store_true"
    )
    args = parser.parse_args()

    if not os.path.exists(args.profile):
        raise Exception("Profile {} not found".format(args.profile))

    ffcut_object = FFCut(profile_path=args.profile)

    if not args.show_command:
        ffcut_object.apply_cut()
    else:
        ffcut_object.show_video_info()
        pprint(ffcut_object.format_ffmpeg_call())


