# Guide for analyzing whiteboard selector filters in Jupyter Notebook / PyCharm
# This script illustrates how to import and run the different filters on the copied examples.

import sys
from pathlib import Path
import cv2
import matplotlib.pyplot as plt

# Add algorithms folder to path to import modules
sys.path.append(str(Path(__file__).resolve().parent / "algorithms"))

# Example importing filters
try:
    from pizarra_filter import filter_pizarra_frames
    from pizarra_occlusion_filter import run_occlusion_filter
    from pizarra_template_matching_transcript import run_template_matching_transcript_filter
    print("✓ Successfully imported all filters!")
except ImportError as e:
    print(f"✗ Failed to import filters: {e}")

def plot_image(path):
    """Utility function to display images in Jupyter notebooks"""
    if not Path(path).exists():
        print(f"File not found: {path}")
        return
    img = cv2.imread(str(path))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 6))
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.show()

# List bad whiteboard examples available
bad_examples = sorted([f.stem for f in Path(__file__).resolve().parent.glob("bad_whiteboard/*.jpg")])
print(f"\nAvailable bad whiteboard examples ({len(bad_examples)}):")
for ex in bad_examples[:10]:
    print(f" - {ex}")
if len(bad_examples) > 10:
    print(f" ... and {len(bad_examples) - 10} more.")

print("\nHow to use in a Jupyter notebook:")
print("""
# Paste this in a Jupyter cell:
import sys
from pathlib import Path
sys.path.append("./algorithms")

# Import the filter methods
import pizarra_filter
import pizarra_occlusion_filter

# Run occlusion filter on a video ID (e.g. '1SwHH7qQ6Pc')
# pizarra_occlusion_filter.run_occlusion_filter('1SwHH7qQ6Pc')
""")
