# 🎬 Media Toolbox

A modular Python project for processing **video**, **image**, and **audio** using `FFmpeg`, `OpenCV`, and CLI interfaces.

## 🚀 Features

- 🎞️ **Video Processing**
  - Merge two videos into one
  - Crop any side of a video
  - Trim from beginning and end

- 🖼️ **Image Processing**
  - Resize images to square dimensions
  - Create GIF and video from a sequence of images

- 🔊 **Audio Processing**
  - Split an audio file into fixed-duration chunks

## 📁 Project Structure

media-toolbox/

├── main.py

├── requirements.txt

├── README.md

└── utils/

├── init.py

├── ensure_ffmpeg.py

├── video_utils.py

├── image_utils.py

└── sound_utils.py

## 🧰 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

FFmpeg will be automatically downloaded to the ffmpeg/ folder if not found.

## 🧪 Example Usage
Video
```bash
# Video
python utils/video_utils.py merge example1.mp4 example2.mp4
python utils/video_utils.py crop example1.mp4 --top 20 --bottom 20 --left 30 --right 30
python utils/video_utils.py trim example1.mp4 --seconds 2.0

# Image
python utils/image_utils.py resize example.jpg 480
python utils/image_utils.py gif images/

# Audio
python utils/audio_utils.py full.wav out_segments/ --duration 10
python utils/audio_utils.py full.wav out_segments/ --excel timings.xlsx
```

## ▶️ Run all examples from main.py:
Edit and uncomment what you need:
```bash
# main.py
run_video()
run_image()
run_audio()
```
Then run:
```bash
python main.py
```

### 💡 Notes
Place 16 image files named img_1.jpg to img_16.jpg in the images/ folder for GIF generation.

Output files are named automatically with cropped_, resized_, merged_, etc.

Compatible with Python 3.7+

