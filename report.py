import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from collections import defaultdict

from lib import MedicineDatabase


database = MedicineDatabase()
boxes = database.get_available()
print("- Found", len(boxes), "total boxes of medicine.")
boxes_by_location = defaultdict(list)
for box in boxes:
    boxes_by_location[box.location].append(box)

for location in boxes_by_location:
    print(f"==={location}===")
    units = defaultdict(list)
    for box in boxes_by_location[location]:
        units[box.units].append(box)
    print("- Found", len(boxes_by_location[location]), "boxes at", location)
    
    counts = {unit:len(boxes) for unit, boxes in units.items()}
    counts = sorted(counts.items(), key=lambda x: x[0])
    labels = [x[0] for x in counts]
    freqs = [x[1] for x in counts]

    plt.figure(dpi=600)
    freq_series = pd.Series(freqs)
    ax = freq_series.plot(kind='bar')
    ax.set_title("Humate-P Boxes at " + location)
    ax.set_xlabel("Units")
    ax.set_ylabel("Count")
    ax.set_xticklabels(labels, rotation=0)

    rects = ax.patches
    bar_labels = [f"{datetime.fromordinal(units[unit][0].expiration).date()} ({len(units[unit])})" for unit in labels]
    for rect, bar_label in zip(rects, bar_labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, bar_label,
                ha='center', va='bottom')

    out_path = f"{Path(location)}_count.png"
    plt.savefig(out_path, bbox_inches="tight")
    print("- Saved", out_path)

