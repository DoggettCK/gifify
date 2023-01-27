#! /usr/bin/env python3
import argparse
import os
import os.path
import re
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a movie to GIF with optional subtitles')

    parser.set_defaults(dry_run=False)
    parser.set_defaults(duration=5)
    parser.set_defaults(timestamp='00:00:00')
    parser.add_argument('-i, --input', dest='input', action='store', required=True, help='input video file')
    parser.add_argument('-o, --output', dest='output', action='store', required=True, help='output GIF file')
    parser.add_argument('-s, --subtitles', dest='subtitles', action='store', help='file containing subtitles')
    parser.add_argument('-t, --timestamp', dest='timestamp', action='store', help='timestamp to start GIF from in HH:MM:SS format')
    parser.add_argument('-d, --duration', dest='duration', action='store', help='length of GIF in seconds')
    parser.add_argument('-n, --dry_run', dest='dry_run', action='store_true')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: Input file ({args.input}) not found")
        exit(1)

    if args.subtitles != None and not os.path.exists(args.subtitles):
        print(f"ERROR: Subtitles file ({args.subtitles}) specified, but not found")
        exit(1)

    try:
        args.duration = float(args.duration)
    except ValueError:
        print(f"ERROR: Duration must be a number")
        exit(1)

    process_args = [
            "ffmpeg",
            "-i",
            f"\"{args.input}\"",
            "-vf",
            f"\"subtitles=\\'{args.subtitles}\\'\"",
            "-ss",
            f"{args.timestamp}",
            "-t",
            f"{args.duration}",
            "-y",
            f"\"{args.output}\""
            ]

    if args.subtitles == None:
        del(process_args[3:5])

    if args.dry_run:
        print(" ".join(process_args))
    else:
        try:
            subprocess.run(process_args, cwd=os.getcwd())
        except FileNotFoundError:
            print("ERROR: ffmpeg not installed")

