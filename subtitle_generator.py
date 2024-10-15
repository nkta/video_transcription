import re
from datetime import timedelta

def clean_translation(text):
    # Supprime tout ce qui est entre parenthèses
    cleaned_text = re.sub(r'\([^)]*\)', '', text)
    # Supprime les espaces supplémentaires
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def generate_srt(transcription, translation=None):
    segments = transcription['segments']
    original_srt = ""
    translated_srt = ""
    
    for i, segment in enumerate(segments, start=1):
        start_time = format_time(segment['start'])
        end_time = format_time(segment['end'])
        text = segment['text'].strip()
        
        original_srt += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
        
        if translation:
            translated_text = translation.get(i-1, "").strip()
            cleaned_translated_text = clean_translation(translated_text)
            translated_srt += f"{i}\n{start_time} --> {end_time}\n{cleaned_translated_text}\n\n"
    
    return original_srt, translated_srt

def format_time(seconds):
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(td.microseconds / 1000)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"