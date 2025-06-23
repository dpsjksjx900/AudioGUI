#!/usr/bin/env python3
import sys
import os
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QButtonGroup,
    QFileDialog, QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt
from logging import Handler, Formatter

# --- Segmentation stubs ---
def run_forced_align(audio: str, transcript: str, lexicon: str, outdir: str, logger: logging.Logger) -> str:
    """Dummy forced-alignment implementation."""
    logger.debug("Simulating forced alignment")
    result = os.path.join(outdir, "forced_align.txt")
    with open(result, "w", encoding="utf-8") as fh:
        fh.write(f"Forced alignment result for {audio}\n")
    return result


def run_unsupervised(audio: str, outdir: str, logger: logging.Logger) -> str:
    """Split audio into segments based on onset detection."""
    import librosa
    import numpy as np
    import soundfile as sf

    logger.debug("Loading audio file")
    y, sr = librosa.load(audio, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)

    logger.debug("Detecting onsets")
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time")

    # Ensure boundaries include start and end
    boundaries = np.concatenate([[0.0], onsets, [duration]])
    logger.debug(f"Detected {len(onsets)} onsets; creating {len(boundaries)-1} segments")

    for i in range(len(boundaries) - 1):
        start = boundaries[i]
        end = boundaries[i + 1]
        segment = y[int(start * sr) : int(end * sr)]
        out_path = os.path.join(outdir, f"segment_{i+1:03d}.wav")
        sf.write(out_path, segment, sr)
        logger.info(f"Wrote segment {i+1} [{start:.2f}s - {end:.2f}s]: {out_path}")

    logger.debug("Segmentation complete")
    return outdir

# --- Custom logging handler to write into QTextEdit ---
class QTextEditLogger(Handler):
    def __init__(self, widget: QTextEdit):
        super().__init__()
        self.widget = widget
        fmt = Formatter('%(asctime)s — %(levelname)s — %(message)s', '%H:%M:%S')
        self.setFormatter(fmt)

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)

# --- QLineEdit that accepts file/folder drops ---
class DropLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setPlaceholderText(placeholder)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return
        path = urls[0].toLocalFile()
        self.setText(path)
        event.acceptProposedAction()

# --- Main Application Window ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Syllable Segmenter")

        # Central widget + layout
        w = QWidget()
        layout = QVBoxLayout()
        w.setLayout(layout)
        self.setCentralWidget(w)

        # Mode selection
        mode_layout = QHBoxLayout()
        self.forced_rb = QRadioButton("Forced-Align")
        self.unsup_rb  = QRadioButton("Unsupervised")
        self.unsup_rb.setChecked(True)
        grp = QButtonGroup(self)
        grp.addButton(self.forced_rb)
        grp.addButton(self.unsup_rb)
        mode_layout.addWidget(self.forced_rb)
        mode_layout.addWidget(self.unsup_rb)
        layout.addLayout(mode_layout)

        # Helper to build file/folder rows
        def make_row(label, placeholder, browse_filter=None, is_dir=False):
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            le = DropLineEdit(placeholder)
            row.addWidget(le)
            btn = QPushButton("Browse")
            if is_dir:
                btn.clicked.connect(lambda: self._browse_dir(le))
            else:
                btn.clicked.connect(lambda: self._browse_file(le, browse_filter))
            row.addWidget(btn)
            layout.addLayout(row)
            return le

        # File inputs
        self.audio_edit = make_row("Audio:", "Drag & drop audio (.wav/.mp3)", "Audio Files (*.wav *.mp3)")
        self.tran_edit  = make_row("Transcript:", "Drag & drop transcript (.txt)", "Text Files (*.txt)")
        self.lex_edit   = make_row("Lexicon:", "Drag & drop lexicon (.dict)", "Dict Files (*.dict)")
        self.out_edit   = make_row("Output Dir:", "Drag & drop or auto-set", None, is_dir=True)

        # Start button
        self.start_btn = QPushButton("Start Segmentation")
        layout.addWidget(self.start_btn)

        # Log widget
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        layout.addWidget(self.log_widget)

        # Signals
        self.forced_rb.toggled.connect(self._update_mode)
        self.start_btn.clicked.connect(self.start_segmentation)
        self.audio_edit.textChanged.connect(self._sync_output_dir)

        # Set up logger
        self.logger = logging.getLogger("Segmenter")
        self.logger.setLevel(logging.DEBUG)
        gui_handler = QTextEditLogger(self.log_widget)
        self.logger.addHandler(gui_handler)

        # Apply initial UI state now that logger exists
        self._update_mode()

    def _update_mode(self):
        forced = self.forced_rb.isChecked()
        self.tran_edit.setEnabled(forced)
        self.lex_edit.setEnabled(forced)
        self.logger.info(f"Mode set to: {'Forced-Align' if forced else 'Unsupervised'}")

    def _browse_file(self, widget: QLineEdit, filter_str: str):
        path, _ = QFileDialog.getOpenFileName(self, "Select File", "", filter_str)
        if path:
            widget.setText(path)
            self.logger.info(f"Selected file for '{widget.placeholderText()}': {path}")

    def _browse_dir(self, widget: QLineEdit):
        path = QFileDialog.getExistingDirectory(self, "Select Directory", "")
        if path:
            widget.setText(path)
            self.logger.info(f"Selected directory: {path}")

    def _sync_output_dir(self, text: str):
        # Whenever the audio path becomes a valid file, auto-set output dir to its folder
        if os.path.isfile(text):
            parent = os.path.dirname(text)
            if self.out_edit.text().strip() != parent:
                self.out_edit.setText(parent)
                self.logger.info(f"Auto-set output directory to: {parent}")

    def start_segmentation(self):
        audio = self.audio_edit.text().strip()
        outdir= self.out_edit.text().strip()
        self.logger.info("Starting segmentation process...")

        # Validate inputs
        if not os.path.isfile(audio):
            self.logger.error(f"Invalid audio file: {audio}")
            return
        if not os.path.isdir(outdir):
            self.logger.error(f"Invalid output directory: {outdir}")
            return

        # File logging setup
        log_path = os.path.join(outdir, "syllable_segmenter.log")
        # remove old file handlers to prevent duplicates
        for h in list(self.logger.handlers):
            if isinstance(h, logging.FileHandler):
                self.logger.removeHandler(h)
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setFormatter(Formatter('%(asctime)s — %(levelname)s — %(message)s', '%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(fh)
        self.logger.info(f"Logging to file: {log_path}")

        # Choose mode
        if self.forced_rb.isChecked():
            transcript = self.tran_edit.text().strip()
            lexicon    = self.lex_edit.text().strip()
            if not os.path.isfile(transcript) or not os.path.isfile(lexicon):
                self.logger.error("Transcript or lexicon missing/invalid.")
                return
            self.logger.info(
                f"Running forced-align on '{audio}' with '{transcript}' & '{lexicon}'"
            )
            result = run_forced_align(audio, transcript, lexicon, outdir, self.logger)
        else:
            self.logger.info(f"Running unsupervised segmentation on '{audio}'")
            result = run_unsupervised(audio, outdir, self.logger)

        try:
            self.logger.info(f"Segmentation output written to: {result}")
            self.logger.info("Segmentation completed successfully.")
        except Exception as e:
            self.logger.exception(f"Segmentation failed: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw  = MainWindow()
    mw.resize(600, 500)
    mw.show()
    sys.exit(app.exec_())
