import subprocess
from tqdm import tqdm

def translate_text(transcription, target_lang="fr", start_index=0):
    """Translate each segment of a transcription.

    Parameters
    ----------
    transcription : dict
        Transcription data with a ``segments`` list.
    target_lang : str, optional
        Target language code, by default "fr".
    start_index : int, optional
        Starting index to use for the returned translation mapping. This is
        useful when translating batches of segments so that indices remain
        aligned with the global transcript.

    Returns
    -------
    dict
        Mapping of segment index to translated text.
    """

    segments = transcription['segments']
    translated_segments = {}

    for i, segment in enumerate(tqdm(segments, desc="Translating"), start=start_index):
        text = segment['text']
        prompt = f"""You are a professional translator. Your task is to translate the following text from any language to {target_lang}. I don't want commentary just translate text for response
Text to translate:
{text}
"""

        try:
            # Run the Ollama command directly
            result = subprocess.run(
                ["ollama", "run", "llama3.1:8b"],
                input=prompt.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            # Process the output
            output = result.stdout.decode('utf-8').strip()
            translated_segments[i] = output
        except subprocess.CalledProcessError as e:
            print(f"Error during Ollama command: {e.stderr.decode('utf-8')}")
            translated_segments[i] = "Translation error"
        except Exception as e:
            print(f"Unexpected error: {e}")
            translated_segments[i] = "Translation error"

    return translated_segments
