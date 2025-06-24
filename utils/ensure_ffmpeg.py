import os
import zipfile
import urllib.request

def ensure_ffmpeg():
    ffmpeg_dir = "ffmpeg"
    ffmpeg_path = os.path.join(ffmpeg_dir, "bin", "ffmpeg.exe")

    if os.path.exists(ffmpeg_path):
        return ffmpeg_path

    print("FFmpeg bulunamadı. İndiriliyor...")

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = "ffmpeg.zip"
    urllib.request.urlretrieve(url, zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("temp_ffmpeg")
    
    # klasör adı örnek: ffmpeg-release-essentials-6.0
    extracted_dir = os.path.join("temp_ffmpeg", os.listdir("temp_ffmpeg")[0])
    os.rename(extracted_dir, ffmpeg_dir)
    os.remove(zip_path)
    os.rmdir("temp_ffmpeg")

    print("✅ FFmpeg indirildi ve kuruldu!")
    return ffmpeg_path
