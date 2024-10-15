from faster_whisper import WhisperModel
from tqdm import tqdm
import time
import torch

def transcribe_audio(audio_file, segment_duration=30, model_size="tiny"):
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA is available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Current device: {torch.cuda.current_device()}")
        print(f"Device name: {torch.cuda.get_device_name(0)}")

    try:
        print(f"Tentative de chargement du modèle {model_size} sur CUDA...")
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
        print("Modèle chargé avec succès sur CUDA")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle sur CUDA: {e}")
        print("Tentative de chargement sur CPU...")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print("Début de la transcription...")
    start_time = time.time()
    
    segments, info = model.transcribe(audio_file, word_timestamps=True, vad_filter=True)
    
    # Convertir le générateur en liste pour pouvoir l'utiliser avec tqdm
    segments = list(segments)
    
    result = {
        "text": "",
        "segments": [],
        "language": info.language
    }
    
    for segment in tqdm(segments, desc="Traitement des segments"):
        result["text"] += segment.text + " "
        result["segments"].append({
            "text": segment.text,
            "start": segment.start,
            "end": segment.end
        })
    
    end_time = time.time()
    print(f"Transcription terminée en {end_time - start_time:.2f} secondes")
    
    return result