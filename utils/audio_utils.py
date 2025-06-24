import subprocess
import argparse
import sys
import os
import pandas as pd
import re
from pydub import AudioSegment
from pydub import utils

# FFmpeg yolunu ayarla
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import ensure_ffmpeg as ef
ffmpeg_path = ef.ensure_ffmpeg()

utils.get_encoder_name = lambda: ffmpeg_path
AudioSegment.converter = ffmpeg_path
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = ffmpeg_path.replace("ffmpeg.exe", "ffprobe.exe")

# HHMMSS stringini milisaniyeye çeviren fonksiyon
def hhmmss_to_ms(hhmmss):
    val = int(hhmmss)
    h = val // 10000
    m = (val % 10000) // 100
    s = val % 100
    return (h * 3600 + m * 60 + s) * 1000

# Segmentleyici fonksiyon
def split_by_excel(input_wav, excel_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Excel verisini oku
    df = pd.read_excel(excel_path)
    df.columns = df.columns.str.strip()
    df = df[pd.notna(df['timing'])]

    # Sabit offset: 01:11:35 → ? ms
    OFFSET_MS = hhmmss_to_ms(11135)

    # Başlangıç zamanlarını hesapla
    df['start_ms'] = df['timing'].apply(hhmmss_to_ms) - OFFSET_MS
    df['start_ms'] = df['start_ms'].clip(lower=0).astype(int)

    audio = AudioSegment.from_wav(input_wav)

    for i in range(len(df)):
        start_ms = df.loc[i, 'start_ms']
        if i < len(df) - 1:
            end_ms = df.loc[i + 1, 'start_ms']
            duration = end_ms - start_ms
            if duration <= 1000:
                start_ms = max(start_ms - 100, 0)  # 100 ms ekle ama audio başlangıç sınırını aşma
                end_ms = min(end_ms + 350, len(audio))  # 350 ms ekle ama audio sınırını aşma
        else:
            end_ms = len(audio)

        if end_ms <= start_ms:
            print(f"⚠️ Atlandı: {i:03d} ({start_ms} → {end_ms})")
            continue

        segment = audio[start_ms:end_ms]
        speaker = str(df.loc[i, 'character']).strip().replace(" ", "_")
        filename = f"{i:03d}_{speaker}.wav"

        segment.export(os.path.join(output_dir, filename), format="wav")

    print(f"✅ {len(df)} segment '{output_dir}' klasörüne kaydedildi.")


# Ses dosyasını sabit süreli parçalara böler
def split_audio(input_path, output_dir, segment_duration=10):
    ffmpeg_exe = ef.ensure_ffmpeg()
    os.makedirs(output_dir, exist_ok=True)

    subprocess.run([
        ffmpeg_exe,
        "-i", input_path,
        "-f", "segment",
        "-segment_time", str(segment_duration),
        "-c", "copy",
        os.path.join(output_dir, "segment_%03d.wav")
    ], check=True)

    print(f"{input_path} dosyası {segment_duration} saniyelik parçalara bölündü → {output_dir}")

# Komut satırı arayüzü
def main():
    parser = argparse.ArgumentParser(description="Audio processing utility: split audio")
    parser.add_argument("input", type=str, help="Input audio file path")
    parser.add_argument("output_dir", type=str, help="Directory to save audio segments")
    parser.add_argument("--duration", type=int, default=None, help="Segment duration in seconds (for fixed splitting)")
    parser.add_argument("--excel", type=str, default=None, help="Excel file with timing information")

    args = parser.parse_args()

    if args.excel:
        split_by_excel(args.input, args.excel, args.output_dir)
    else:
        duration = args.duration if args.duration else 10
        split_audio(args.input, args.output_dir, segment_duration=duration)

if __name__ == "__main__":
    main()
