import utils.audio_utils as audio_utils
import utils.video_utils as video_utils
import utils.image_utils as image_utils

def run_video():
    print("\n🔹 Running Video Examples...")

    # Merge two videos
    video_utils.merge_videos("example1.mp4", "example2.mp4")

    # Crop a video (top, bottom, left, right)
    video_utils.crop_video("example1.mp4", crop_top=50, crop_bottom=20, crop_left=30, crop_right=30)

    # Trim beginning and end
    video_utils.trim_video("example1.mp4", cut_duration=2)


def run_image():
    print("\n🖼️ Running Image Examples...")

    # Resize an image to 480x480
    image_utils.resize_image("example.jpg", image_size=480)

    # Create gif and video from a folder of images
    image_utils.create_gif_and_video("images")  # folder must contain img_1.jpg to img_16.jpg


def run_audio():
    print("\n🎧 Running Audio Examples...")

    # audio_utils.split_audio("full.wav", "audio_segments", segment_duration=20)
    
    audio_utils.split_by_excel("full.wav", "excl.xlsx", "person")


if __name__ == "__main__":
    # run_video()
    # run_image()
    run_audio()
