import yt_dlp
import os
from pydub import AudioSegment

def process_audio(input_source, segment_duration=3600):
    if input_source.startswith(('http://', 'https://')):
        return download_and_segment_audio(input_source, segment_duration)
    return segment_local_audio(input_source, segment_duration)

def download_and_segment_audio(url, segment_duration):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'temp_audio.%(ext)s'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info['title']
        filename = ydl.prepare_filename(info)
        filename = os.path.splitext(filename)[0] + '.mp3'
    
    return segment_local_audio(filename, segment_duration), title

def segment_local_audio(file_path, segment_duration):
    audio = AudioSegment.from_mp3(file_path)
    duration = len(audio)
    segments = []

    for start in range(0, duration, segment_duration * 1000):
        end = start + segment_duration * 1000
        segment = audio[start:end]
        segment_file = f"{os.path.splitext(file_path)[0]}_{start // 1000}_{end // 1000}.mp3"
        segment.export(segment_file, format="mp3")
        segments.append(segment_file)

    return segments

def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in ' _-']).rstrip()