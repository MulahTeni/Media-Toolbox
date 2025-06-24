import cv2
import subprocess
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
import ensure_ffmpeg as ef
import argparse

def merge_videos(video1, video2):
    ffmpeg_exe = ef.ensure_ffmpeg()
    base1 = re.sub(r"\..+$", "", os.path.basename(video1))
    base2 = re.sub(r"\..+$", "", os.path.basename(video2))
    output_path = f"{base1}_{base2}_merged.mp4"

    subprocess.run([
        ffmpeg_exe,
        "-i", video1,
        "-i", video2,
        "-filter_complex", "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa]",
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264",
        "-c:a", "aac",
        output_path
    ], check=True)

    print("Videos merged successfully:", output_path)

def crop_video(input_path, crop_top=0, crop_bottom=0, crop_left=0, crop_right=0):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {input_path}")

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    new_width = width - crop_left - crop_right
    new_height = height - crop_top - crop_bottom

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = f"cropped_{os.path.basename(input_path)}"
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cropped_frame = frame[crop_top:height - crop_bottom, crop_left:width - crop_right]
        out.write(cropped_frame)

    cap.release()
    out.release()
    print(f"Cropped video saved: {output_path}")

def trim_video(input_path, cut_duration=1.5):
    ffmpeg_exe = ef.ensure_ffmpeg()

    result = subprocess.run(
        [ffmpeg_exe, "-i", input_path],
        stderr=subprocess.PIPE,
        text=True
    )

    match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', result.stderr)
    if not match:
        raise RuntimeError("Video duration could not be read.")

    h, m, s = map(float, match.groups())
    total_seconds = h * 3600 + m * 60 + s

    start = cut_duration
    duration = total_seconds - cut_duration * 2

    if duration <= 0:
        raise ValueError("Video is too short to trim this much.")

    output_path = f"trimmed_{os.path.basename(input_path)}"
    subprocess.run([
        ffmpeg_exe,
        "-ss", str(start),
        "-i", input_path,
        "-t", str(duration),
        "-c", "copy",
        output_path
    ], check=True)

    print(f"Trimmed {cut_duration}s from start and end → {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Video processing utility: merge, crop, trim")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Merge
    merge_parser = subparsers.add_parser("merge", help="Merge two videos")
    merge_parser.add_argument("video1", help="First video file")
    merge_parser.add_argument("video2", help="Second video file")

    # Crop
    crop_parser = subparsers.add_parser("crop", help="Crop a video from all four sides")
    crop_parser.add_argument("input", help="Input video file")
    crop_parser.add_argument("--top", type=int, default=0, help="Pixels to crop from top")
    crop_parser.add_argument("--bottom", type=int, default=0, help="Pixels to crop from bottom")
    crop_parser.add_argument("--left", type=int, default=0, help="Pixels to crop from left")
    crop_parser.add_argument("--right", type=int, default=0, help="Pixels to crop from right")

    # Trim
    trim_parser = subparsers.add_parser("trim", help="Trim start and end from a video")
    trim_parser.add_argument("input", help="Input video file")
    trim_parser.add_argument("--seconds", type=float, default=1.5, help="Seconds to trim from both ends")

    args = parser.parse_args()

    if args.command == "merge":
        merge_videos(args.video1, args.video2)
    elif args.command == "crop":
        crop_video(args.input, crop_top=args.top, crop_bottom=args.bottom, crop_left=args.left, crop_right=args.right)
    elif args.command == "trim":
        trim_video(args.input, cut_duration=args.seconds)

if __name__ == "__main__":
    main()
