# AudioGUI

This project provides a simple PyQt5 GUI for running syllable segmentation. The GUI can operate in two modes: a dummy forced-alignment mode and an unsupervised mode that uses `librosa` to detect syllable onsets and split the audio into multiple `.wav` files. Segments are stored in an `export` subfolder under the chosen output directory and named according to the detected pronunciation.

## Setup

1. Install Python 3.8+.
2. On Windows simply run `run_gui.bat`. The first run creates a virtual environment and installs the required packages automatically.
   On other platforms, run `python install.py` once before launching the GUI.

## Usage

After installing, launch the GUI with:

```bash
python run_gui.bat
```

On non-Windows systems, use:

```bash
python syllable_segmenter_gui.py
```

Drag and drop your audio file (and optionally transcript and lexicon files) then click **Start Segmentation**. Results are stored in an `export` subfolder inside the chosen output directory.

## Updating

To get the latest version of AudioGUI, run:

```bash
update.bat
```

