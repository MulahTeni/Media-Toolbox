import os
import subprocess
import shutil
import argparse
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
import ensure_ffmpeg as ef


def create_temp_frames(images_folder_path):
    os.makedirs("temp_frames", exist_ok=True)
    for i in range(1, 17):
        src = os.path.join(images_folder_path, f"img_{i}.jpg")
        dst = os.path.join("temp_frames", f"frame_{i:03d}.jpg")
        shutil.copyfile(src, dst)

    for j in range(4):
        repeat_index = 16 + j
        dst = os.path.join("temp_frames", f"frame_{repeat_index:03d}.jpg")
        shutil.copyfile(os.path.join(images_folder_path, "img_16.jpg"), dst)

def cleanup():
    shutil.rmtree("temp_frames", ignore_errors=True)

def create_gif_and_video(images_folder_path):
    ffmpeg_exe = ef.ensure_ffmpeg()
    create_temp_frames(images_folder_path)

    subprocess.run([
        ffmpeg_exe,
        "-y",
        "-framerate", "6",
        "-i", "temp_frames/frame_%03d.jpg",
        "-vf", "scale=640:-1",
        "output.gif"
    ], check=True)

    output_path = f"{os.path.basename(images_folder_path.strip('/'))}_output.mp4"

    subprocess.run([
        ffmpeg_exe,
        "-y",
        "-framerate", "6",
        "-i", "temp_frames/frame_%03d.jpg",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_path
    ], check=True)

    cleanup()
    print("GIF ve video başarıyla oluşturuldu:", output_path)

def resize_image(input_path, image_size):
    ffmpeg_exe = ef.ensure_ffmpeg()
    output_image_path = f"resized_image_{os.path.basename(input_path)}"
    subprocess.run([
        ffmpeg_exe,
        "-loop", "1",
        "-i", input_path,
        "-vf", f"scale={image_size}:{image_size}",
        "-frames:v", "1",
        output_image_path
    ], check=True)

    print(f"{input_path} → {output_image_path} (boyut: {image_size}x{image_size})")

def main():
    parser = argparse.ArgumentParser(description="Image processing utility: create GIF/video, resize image")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create_gif_and_video command
    gif_parser = subparsers.add_parser("gif", help="Create GIF and video from images")
    gif_parser.add_argument("folder", type=str, help="Path to folder containing images named img_1.jpg to img_16.jpg")

    # resize_image command
    resize_parser = subparsers.add_parser("resize", help="Resize a single image to square dimensions")
    resize_parser.add_argument("image", type=str, help="Path to input image")
    resize_parser.add_argument("size", type=int, help="Target width and height in pixels")

    args = parser.parse_args()

    if args.command == "gif":
        create_gif_and_video(args.folder)
    elif args.command == "resize":
        resize_image(args.image, args.size)

if __name__ == "__main__":
    main()
