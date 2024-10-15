def save_results(output_file, transcription, translation=None):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Langue d'origine détectée : {transcription['language']}\n\n")
        f.write("Transcription originale :\n")
        f.write(transcription["text"])
        if translation:
            f.write("\n\nTraduction :\n")
            if isinstance(translation, dict):
                for i, segment in enumerate(transcription['segments']):
                    f.write(f"{i+1}. Original: {segment['text']}\n")
                    f.write(f"   Traduction: {translation.get(i, 'Non traduit')}\n\n")
            elif isinstance(translation, str):
                f.write(translation)
            else:
                f.write("Format de traduction non reconnu")