# TTS to IVR Audio - Python dependencies
# Install with: pip install -r requirements.txt


# TTS to IVR Audio

A simple desktop tool that converts text (or a CSV of prompts) into speech using Google Text-to-Speech (gTTS) and then converts the audio into a format suitable for Interactive Voice Response (IVR) systems.

**Target format:** 8 kHz, mono, 16-bit PCM WAV (common for telephony / IVR testing).

---

## Features

- Single-text conversion via a simple GUI
- Batch processing from a CSV file (`prompt_name`, `content`)
- Language selection (powered by gTTS)
- Automatic conversion to IVR-friendly audio (8 kHz mono)
- Progress window for batch jobs
- Output folder selection

---

## Requirements

- Python 3.8 or higher
- Tkinter (included with most Python installations)
- FFmpeg (recommended – required by `pydub` for some audio operations)

### Python packages

Install the dependencies with:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
gTTS>=2.5.0
librosa>=0.10.1
numpy>=1.24.0
soundfile>=0.12.1
pydub>=0.25.1
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/umashankar47/TTStoIVRAudio.git
cd TTStoIVRAudio
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional but recommended) Install FFmpeg and make sure it is available in your system PATH.

---

## Usage

Run the application:

```bash
python main.py
```

### Single prompt

1. Type the text you want to convert in the text field.
2. Choose a language from the dropdown.
3. Click **O/P Folder** to select where the audio file should be saved.
4. Click **Generate**.

### Batch processing (CSV)

1. Prepare a CSV file with two columns (no header required, but the first row is skipped as a header in the current code):

   ```csv
   prompt_name,content
   welcome,Welcome to our customer service line.
   menu,Please press 1 for sales or 2 for support.
   goodbye,Thank you for calling. Goodbye.
   ```

2. Click **Load a CSV File** and select your CSV.
3. Choose the output folder.
4. In the progress window click **Start**.

Audio files will be named after the `prompt_name` column and saved in the selected output folder.

---

## Notes & Known Limitations

- The application currently hard-codes the conversion to supported IVR audio format **8 kHz mono PCM_16  μ-law / A-law **. 
- Only the Google TTS engine is fully wired up.

---

## Project Structure

```
TTStoIVRAudio/
├── main.py              # Main application (GUI + logic)
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── .idea/               # IDE settings (should normally be git-ignored)
```

---



## License

No license file is currently present in the repository. Please add one if you plan to distribute or reuse the code.
