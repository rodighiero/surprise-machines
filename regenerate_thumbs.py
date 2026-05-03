#!/usr/bin/env python3
"""
Regenerate Surprise Machines thumbnails as 256 px WebP at quality 80.

What it does:
  1. Reads every JPEG in data/originals/.
  2. Writes a 256 px (longest side) WebP version to data/thumbs/ next to the
     existing .jpg files.
  3. Updates data/imagelists/imagelist-*.json.gz so the `images` array
     references *.webp filenames.
  4. Updates data/hotspots/hotspot-*.json.gz so cover and member images
     reference *.webp filenames.
  5. Optionally deletes the old *.jpg files in data/thumbs/.

Run from the repo root:
    python3 regenerate_thumbs.py

Add --delete-jpg at the end to remove the old JPEG thumbs once WebP is done.

Requires: pip3 install Pillow
"""

import os
import sys
import gzip
import json
import argparse
import multiprocessing as mp
from pathlib import Path
from PIL import Image, ImageFile

# Allow Pillow to encode JPEGs that were truncated during download
# (a few of the Harvard IIIF originals end without proper EOI markers).
ImageFile.LOAD_TRUNCATED_IMAGES = True

REPO = Path(__file__).resolve().parent
ORIGINALS = REPO / "data" / "originals"
THUMBS = REPO / "data" / "thumbs"
IMAGELISTS = REPO / "data" / "imagelists"
HOTSPOTS = REPO / "data" / "hotspots"

SIZE = 256
QUALITY = 80


def make_thumb(filename):
    src = ORIGINALS / filename
    stem = Path(filename).stem
    dst = THUMBS / f"{stem}.webp"
    if dst.exists():
        return None
    try:
        img = Image.open(src).convert("RGB")
        img.thumbnail((SIZE, SIZE), Image.LANCZOS)
        img.save(dst, format="WEBP", quality=QUALITY, method=4)
        return dst.stat().st_size
    except Exception as e:
        return f"ERROR {filename}: {e}"


def regenerate_thumbs():
    print(f"Source: {ORIGINALS}")
    print(f"Destination: {THUMBS}")
    print(f"Size: {SIZE}px WebP q{QUALITY}\n")
    THUMBS.mkdir(parents=True, exist_ok=True)
    files = sorted(os.listdir(ORIGINALS))
    print(f"Found {len(files)} originals.")

    n_workers = max(1, mp.cpu_count() - 1)
    total_bytes = 0
    n_skipped = 0
    n_errors = 0
    print(f"Using {n_workers} workers...\n")

    with mp.Pool(n_workers) as pool:
        for i, result in enumerate(pool.imap_unordered(make_thumb, files, chunksize=20), 1):
            if result is None:
                n_skipped += 1
            elif isinstance(result, str):
                n_errors += 1
                if n_errors < 10:
                    print(result)
            else:
                total_bytes += result
            if i % 5000 == 0:
                pct = i * 100 // len(files)
                print(f"  {i:>7}/{len(files)} ({pct}%)  total so far: {total_bytes/1e6:.0f} MB")

    print(f"\nDone. Wrote {len(files) - n_skipped - n_errors} new files. "
          f"Skipped {n_skipped} (already existed). Errors: {n_errors}.")
    print(f"Total new size on disk: {total_bytes/1e9:.2f} GB")


def update_imagelists():
    print("\nUpdating imagelist JSONs...")
    for f in IMAGELISTS.glob("*.json.gz"):
        with gzip.open(f, "rt") as fh:
            d = json.load(fh)
        if "images" in d:
            d["images"] = [Path(name).stem + ".webp" for name in d["images"]]
            with gzip.open(f, "wt") as fh:
                json.dump(d, fh)
            print(f"  rewrote {f.name}")


def update_hotspots():
    print("\nUpdating hotspot JSONs...")
    for f in HOTSPOTS.glob("*.json.gz"):
        with gzip.open(f, "rt") as fh:
            spots = json.load(fh)
        for s in spots:
            # Only the `img` field is a filename. `images` is a list of cell
            # indices (integers), not filenames — leave it alone.
            if "img" in s:
                s["img"] = Path(s["img"]).stem + ".webp"
        with gzip.open(f, "wt") as fh:
            json.dump(spots, fh)
        print(f"  rewrote {f.name}")


def delete_old_jpgs():
    print("\nRemoving old *.jpg thumbnails from data/thumbs/...")
    n = 0
    for f in THUMBS.glob("*.jpg"):
        f.unlink()
        n += 1
        if n % 10000 == 0:
            print(f"  deleted {n}")
    print(f"  deleted {n} JPEGs total")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delete-jpg", action="store_true",
                        help="Delete old .jpg files from data/thumbs/ after regeneration.")
    parser.add_argument("--skip-thumbs", action="store_true",
                        help="Skip thumbnail regeneration, only update JSON files.")
    args = parser.parse_args()

    if not args.skip_thumbs:
        regenerate_thumbs()
    update_imagelists()
    update_hotspots()
    if args.delete_jpg:
        delete_old_jpgs()


if __name__ == "__main__":
    main()
