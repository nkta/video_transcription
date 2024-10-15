# Audio Transcription and Translation Tool

This project is a Python-based tool that transcribes audio from various sources (including YouTube videos) and optionally translates the transcription to a specified language. It also generates SRT subtitle files.

## Features

- Audio processing from local files or YouTube URLs
- Speech-to-text transcription using Whisper AI
- Optional translation to any language using Ollama (default: French)
- SRT subtitle file generation
- CUDA support for faster processing on compatible GPUs

## Prerequisites

- Python 3.10 or higher
- CUDA-compatible GPU (optional, for faster processing)
- Ollama installed and configured (for translation)

## Installation

### 1. Clone the repository:
   ```
   git clone https://github.com/yourusername/audio-transcription-tool.git
   cd audio-transcription-tool
   ```

### 2. Install CUDA (for GPU acceleration):

CUDA installation can be complex and varies depending on your system. Here's a general guide:

a. Check if your GPU is CUDA-compatible:
   Visit the [NVIDIA CUDA GPUs list](https://developer.nvidia.com/cuda-gpus) to confirm.

b. Download and install the NVIDIA GPU drivers:
   - For Windows: Use the [NVIDIA Driver Downloads](https://www.nvidia.com/Download/index.aspx) page.
   - For Linux: Use your distribution's package manager or NVIDIA's `.run` file.

c. Install CUDA Toolkit:
   - Download the CUDA Toolkit from the [NVIDIA CUDA Downloads](https://developer.nvidia.com/cuda-downloads) page.
   - Choose the version that matches your system and follow the installation instructions.

d. Set up environment variables:
   - On Windows, the installer should set these up automatically.
   - On Linux, add the following to your `.bashrc` or `.zshrc`:
     ```
     export PATH=/usr/local/cuda/bin:$PATH
     export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
     ```

e. Verify CUDA installation:
   ```
   nvcc --version
   ```

f. Install cuDNN:
   - Download cuDNN from the [NVIDIA cuDNN page](https://developer.nvidia.com/cudnn) (requires NVIDIA account).
   - Follow the installation instructions for your platform.

### 3. Install the required Python packages:
   ```
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   pip install faster-whisper yt-dlp tqdm
   ```

### 4. Install Ollama and the required language model:
   ```
   # Install Ollama (instructions may vary based on your OS)
   curl https://ollama.ai/install.sh | sh

   # Pull the Mistral language model
   ollama pull mistral:7b-instruct
   ```

## Usage

Basic usage:

```
python main.py --input <audio_file_or_youtube_url> [options]
```

Options:
- `--input`: Path to local audio file or YouTube URL (required)
- `--output`: Output file name (default: transcription.txt)
- `--srt`: Generate SRT subtitle file
- `--translate`: Translate the transcription
- `--target-lang`: Target language for translation (default: fr for French)

Examples:

1. Transcribe a YouTube video:
   ```
   python main.py --input https://www.youtube.com/watch?v=example --srt
   ```

2. Transcribe and translate a local audio file to French:
   ```
   python main.py --input path/to/audio.mp3 --translate --srt
   ```

3. Transcribe and translate a YouTube video to Spanish:
   ```
   python main.py --input https://www.youtube.com/watch?v=example --translate --target-lang es --srt
   ```

## Output

The tool generates the following outputs:
- A text file containing the transcription (and translation if requested)
- An SRT subtitle file (if the --srt option is used)

## Troubleshooting

If you encounter issues with CUDA:
1. Ensure your NVIDIA drivers are up to date.
2. Check that CUDA is in your system PATH.
3. Verify that PyTorch is using CUDA:
   ```python
   import torch
   print(torch.cuda.is_available())
   ```

## Contributing

Contributions to this project are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Whisper AI](https://github.com/openai/whisper) for the speech recognition model
- [Ollama](https://ollama.ai/) for the translation capabilities
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube video processing