# AudioGUI

This project provides a simple PyQt5 GUI for running syllable segmentation. The GUI can operate in two modes: a dummy forced-alignment mode and a dummy unsupervised mode. Results are written to the selected output directory.

## Setup

1. Install Python 3.8+.
2. Run `python install.py` to create a virtual environment and install dependencies.

## Usage

After installing, launch the GUI with:

```bash
python run_gui.bat
```

On non-Windows systems, use:

```bash
python syllable_segmenter_gui.py
```

Drag and drop your audio file (and optionally transcript and lexicon files) then click **Start Segmentation**. Results are written in the specified output directory.

## Updating

To get the latest version of AudioGUI, run:

```bash
update.bat
```

