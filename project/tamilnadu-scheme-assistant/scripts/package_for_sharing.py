import os
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_ZIP = ROOT_DIR.parent / "tamilnadu-scheme-assistant.zip"

EXCLUDE_DIRS = {
    "venv",
    ".venv",
    "node_modules",
    ".git",
    "__pycache__",
    ".pytest_cache",
    "dist",
    ".vscode",
    ".idea"
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".zip"
}

def should_exclude(rel_path: Path) -> bool:
    for part in rel_path.parts:
        if part in EXCLUDE_DIRS:
            return True
    if rel_path.suffix in EXCLUDE_EXTENSIONS:
        return True
    return False

def package_project():
    print("=" * 60)
    print("  Packaging Tamil Nadu Scheme Assistant for Sharing")
    print("=" * 60)
    print(f"Source: {ROOT_DIR}")
    print(f"Target: {OUTPUT_ZIP}\n")

    count = 0
    total_bytes = 0

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(ROOT_DIR):
            # Prune excluded directories in-place so os.walk skips them
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(ROOT_DIR)

                if should_exclude(rel_path):
                    continue

                # Add to zip inside a clean folder wrapper
                archive_name = Path("tamilnadu-scheme-assistant") / rel_path
                zip_file.write(file_path, archive_name)
                count += 1
                total_bytes += file_path.stat().st_size

    zip_size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    raw_size_mb = total_bytes / (1024 * 1024)

    print(f" Packaging complete!")
    print(f" Files included:    {count}")
    print(f" Uncompressed size: {raw_size_mb:.2f} MB")
    print(f" Final Zip Size:    {zip_size_mb:.2f} MB")
    print(f" Zip Location:      {OUTPUT_ZIP}")
    print("=" * 60)
    print("You can now send this lightweight zip file directly to your colleague via:")
    print(" - Google Drive / OneDrive")
    print(" - Email (if under 25 MB)")
    print(" - WhatsApp / Telegram / Slack")
    print(" - USB Drive")
    print("=" * 60)

if __name__ == "__main__":
    package_project()
