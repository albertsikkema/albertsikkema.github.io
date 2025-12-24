#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["Pillow>=12.0.0"]
# ///
"""
Image optimization for Jekyll blog.
Optimizes PNG, JPG, and WebP images.

Usage:
    ./scripts/optimize-images.py                    # Optimize all images
    ./scripts/optimize-images.py path/to/image.jpg  # Optimize specific image
    ./scripts/optimize-images.py --check            # Check which images need optimization
    ./scripts/optimize-images.py --hook             # Run as git pre-commit hook

Install as pre-commit hook:
    ln -s ../../scripts/optimize-images.py .git/hooks/pre-commit
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

from PIL import Image

# Configuration
IMAGES_DIR = Path("assets/images")
MAX_SIZE_KB = 500
QUALITY_JPG = 85
QUALITY_WEBP = 85
MAX_DIMENSION = 1920


def get_file_size_kb(filepath: Path) -> float:
    """Get file size in KB."""
    return filepath.stat().st_size / 1024


def needs_optimization(filepath: Path) -> Tuple[bool, str]:
    """Check if image needs optimization."""
    size_kb = get_file_size_kb(filepath)

    if size_kb > MAX_SIZE_KB:
        return True, f"{size_kb:.1f}KB > {MAX_SIZE_KB}KB"

    try:
        with Image.open(filepath) as img:
            width, height = img.size
            if width > MAX_DIMENSION or height > MAX_DIMENSION:
                return True, f"{width}x{height} exceeds {MAX_DIMENSION}px"
    except Exception as e:
        return False, f"Error: {e}"

    return False, f"{size_kb:.1f}KB - OK"


def optimize_image(filepath: Path) -> Tuple[bool, str]:
    """Optimize an image file."""
    try:
        original_size = get_file_size_kb(filepath)

        with Image.open(filepath) as img:
            # Convert RGBA to RGB for JPG
            if filepath.suffix.lower() in [".jpg", ".jpeg"] and img.mode == "RGBA":
                rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
                img = rgb_img

            # Resize if needed
            width, height = img.size
            if width > MAX_DIMENSION or height > MAX_DIMENSION:
                ratio = min(MAX_DIMENSION / width, MAX_DIMENSION / height)
                new_size = (int(width * ratio), int(height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Save optimized image
            temp_path = filepath.with_suffix(filepath.suffix + ".tmp")

            if filepath.suffix.lower() in [".jpg", ".jpeg"]:
                img.save(temp_path, "JPEG", quality=QUALITY_JPG, progressive=True, optimize=True)
            elif filepath.suffix.lower() == ".webp":
                img.save(temp_path, "WebP", quality=QUALITY_WEBP, method=6)
            elif filepath.suffix.lower() == ".png":
                img.save(temp_path, "PNG", optimize=True)

            new_size = get_file_size_kb(temp_path)

            if new_size < original_size:
                temp_path.replace(filepath)
                reduction = ((original_size - new_size) / original_size) * 100
                return True, f"{original_size:.1f}KB → {new_size:.1f}KB ({reduction:.0f}% reduction)"
            else:
                temp_path.unlink()
                return True, f"{original_size:.1f}KB (already optimal)"

    except Exception as e:
        return False, f"Error: {e}"


def find_images(path: Path | None = None) -> List[Path]:
    """Find all image files to process."""
    if path and path.is_file():
        return [path]

    search_dir = path if path and path.is_dir() else IMAGES_DIR

    if not search_dir.exists():
        return []

    images = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.webp", "*.PNG", "*.JPG", "*.JPEG", "*.WebP"]:
        images.extend(search_dir.glob(ext))

    return [img for img in images if not img.name.endswith(".tmp")]


def get_staged_images() -> List[Path]:
    """Get list of staged image files from git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True,
        )
        files = result.stdout.strip().split("\n")
        return [
            Path(f)
            for f in files
            if f and Path(f).suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"] and Path(f).exists()
        ]
    except subprocess.CalledProcessError:
        return []


def run_as_hook() -> int:
    """Run as git pre-commit hook."""
    staged = get_staged_images()

    if not staged:
        return 0

    print(f"\n🖼️  Optimizing {len(staged)} staged image(s)...\n")

    success_count = 0
    for img_path in staged:
        needs, _ = needs_optimization(img_path)
        if not needs:
            print(f"⏭️  {img_path}: already optimized")
            continue

        success, message = optimize_image(img_path)
        if success:
            print(f"✅ {img_path}: {message}")
            # Re-add optimized image to staging
            subprocess.run(["git", "add", str(img_path)], check=True)
            success_count += 1
        else:
            print(f"❌ {img_path}: {message}")
            return 1

    if success_count > 0:
        print(f"\n✨ Optimized {success_count} image(s) and re-staged\n")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Optimize images for Jekyll blog")
    parser.add_argument("path", nargs="?", help="Specific image or directory to optimize")
    parser.add_argument("--check", action="store_true", help="Check which images need optimization")
    parser.add_argument("--hook", action="store_true", help="Run as git pre-commit hook")
    args = parser.parse_args()

    # Hook mode
    if args.hook or Path(__file__).name == "pre-commit":
        return run_as_hook()

    # Find images
    images = find_images(Path(args.path) if args.path else None)

    if not images:
        print(f"No images found in {IMAGES_DIR}")
        return 0

    print(f"Found {len(images)} image(s)\n")

    # Check mode
    if args.check:
        print(f"Checking images (max: {MAX_SIZE_KB}KB, {MAX_DIMENSION}px):\n")
        needs_opt = []
        for img in sorted(images):
            needs, reason = needs_optimization(img)
            status = "⚠️  OPTIMIZE" if needs else "✅ OK"
            print(f"{status}: {img.name} - {reason}")
            if needs:
                needs_opt.append(img)

        print(f"\nSummary: {len(needs_opt)} need optimization")
        return 1 if needs_opt else 0

    # Optimize mode
    print("Optimizing images...\n")
    success_count = 0
    for img in sorted(images):
        needs, _ = needs_optimization(img)
        if not needs:
            print(f"⏭️  {img.name}: already optimized")
            continue

        success, message = optimize_image(img)
        if success:
            print(f"✅ {img.name}: {message}")
            success_count += 1
        else:
            print(f"❌ {img.name}: {message}")
            return 1

    print(f"\n✨ Optimized {success_count} image(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
