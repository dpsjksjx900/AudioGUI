import os
import shutil
import tempfile
import urllib.request
import zipfile

REPO_ZIP_URL = "https://github.com/dpsjksjx900/AudioGUI/archive/refs/heads/main.zip"


def update_from_zip(repo_dir: str) -> None:
    """Download the latest repo zip and replace files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "repo.zip")
        print("\U0001F4E6  Downloading latest version...")
        urllib.request.urlretrieve(REPO_ZIP_URL, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmpdir)
        extracted_root = os.path.join(tmpdir, "AudioGUI-main")
        for name in os.listdir(extracted_root):
            if name in {"venv", ".git"}:
                continue
            src = os.path.join(extracted_root, name)
            dst = os.path.join(repo_dir, name)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    print("\u2705  Update complete.")


if __name__ == "__main__":
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    update_from_zip(repo_dir)
