import sys
import os
import argparse
from audio_processor import process_audio, sanitize_filename, get_segment_start
from transcriber import transcribe_audio
from translator import translate_text
from utils import save_results
from subtitle_generator import generate_srt
import torch
import gc

def process_batch(batch, model_size, target_lang=None, start_index=0):
    full_transcription = {"text": "", "segments": [], "language": None}
    translation = {}
    index = start_index

    for segment_file in batch:
        transcription = transcribe_audio(segment_file, model_size=model_size)
        offset = get_segment_start(segment_file)
        for seg in transcription["segments"]:
            seg["start"] += offset
            seg["end"] += offset

        if not full_transcription["language"]:
            full_transcription["language"] = transcription["language"]

        full_transcription["text"] += transcription["text"] + " "
        full_transcription["segments"].extend(transcription["segments"])

        if target_lang:
            segment_translation = translate_text(
                transcription,
                target_lang=target_lang,
                start_index=index,
            )
            translation.update(segment_translation)
        index += len(transcription["segments"])
        
        gc.collect()
        torch.cuda.empty_cache()  # Vide le cache CUDA si un GPU est utilisé

    return full_transcription, translation, index

def main():
    parser = argparse.ArgumentParser(description="Transcribe and optionally translate audio")
    parser.add_argument("--input", help="Input audio file or URL", required=True)
    parser.add_argument("--output", help="Output file name (optional)")
    parser.add_argument("--output-dir", help="Répertoire de sortie pour les résultats (optionnel)", default="output")
    parser.add_argument("--srt", action="store_true", help="Générer un fichier de sous-titres SRT")
    parser.add_argument("--translate", action="store_true", help="Traduire la transcription")
    parser.add_argument("--target-lang", default="fr", help="Langue cible pour la traduction (par défaut : fr pour français)")
    parser.add_argument("--segment-duration", type=int, default=900, help="Durée des segments audio à traiter à la fois (en secondes)")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"], help="Taille du modèle Whisper")
    parser.add_argument("--batch-size", type=int, default=4, help="Nombre de segments à traiter en batch")
    args = parser.parse_args()

    # Traitement de l'audio
    print("Étape 1: Traitement de l'audio...")
    audio_segments, video_title = process_audio(args.input, args.segment_duration)
    
    if video_title:
        sanitized_title = sanitize_filename(video_title)
        # Créer un sous-répertoire pour la vidéo
        video_output_dir = os.path.join(args.output_dir, sanitized_title)
    else:
        video_output_dir = args.output_dir

    # Créer le répertoire de sortie (et le sous-répertoire si nécessaire)
    os.makedirs(video_output_dir, exist_ok=True)

    if video_title:
        output_base = sanitized_title if not args.output else os.path.splitext(args.output)[0]
    else:
        output_base = os.path.splitext(args.output)[0] if args.output else "transcription"

    # Définir le chemin complet pour le fichier de sortie
    output_file = os.path.join(video_output_dir, f"{output_base}.txt")

    full_transcription = {"text": "", "segments": [], "language": None}
    full_translation = {}
    segment_index = 0
    
    for i in range(0, len(audio_segments), args.batch_size):
        batch = audio_segments[i:i+args.batch_size]
        print(f"\nTraitement du lot {i//args.batch_size + 1}/{(len(audio_segments) + args.batch_size - 1)//args.batch_size}...")
        
        batch_transcription, batch_translation, segment_index = process_batch(
            batch,
            args.model,
            args.target_lang if args.translate else None,
            start_index=segment_index,
        )
        
        full_transcription["text"] += batch_transcription["text"]
        full_transcription["segments"].extend(batch_transcription["segments"])
        if not full_transcription["language"]:
            full_transcription["language"] = batch_transcription["language"]
        
        if args.translate:
            full_translation.update(batch_translation)
        
        gc.collect()
        torch.cuda.empty_cache()

    print(f"Transcription complète (premiers 100 caractères): {full_transcription['text'][:100]}...")
    
    print("\nÉtape 4: Sauvegarde des résultats...")
    save_results(output_file, full_transcription, full_translation if args.translate else None)

    if args.srt:
        print("\nÉtape 5: Génération des sous-titres SRT...")
        original_srt, translated_srt = generate_srt(full_transcription, full_translation if args.translate else None)
        
        original_srt_filename = os.path.join(video_output_dir, f"{output_base}.srt")
        with open(original_srt_filename, 'w', encoding='utf-8') as srt_file:
            srt_file.write(original_srt)
        print(f"Sous-titres SRT originaux générés et enregistrés dans '{original_srt_filename}'")
        
        if args.translate:
            translated_srt_filename = os.path.join(video_output_dir, f"{output_base}_translated.srt")
            with open(translated_srt_filename, 'w', encoding='utf-8') as srt_file:
                srt_file.write(translated_srt)
            print(f"Sous-titres SRT traduits générés et enregistrés dans '{translated_srt_filename}'")

    print(f"\nTraitement terminé. Le résultat a été enregistré dans '{output_file}'.")
    print(f"Langue d'origine détectée : {full_transcription['language']}")

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA is available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
    main()
