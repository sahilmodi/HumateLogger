import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from collections import defaultdict

from lib import MedicineDatabase

def save_availablity(output_path="availability.png"):
    database = MedicineDatabase()
    boxes = database.get_available()
    print("- Found", len(boxes), "total boxes of medicine.\n")
    boxes_by_location = defaultdict(list)
    for box in boxes:
        boxes_by_location[box.location].append(box)

    n = len(boxes_by_location.keys())
    fig, axes = plt.subplots(1, 2, dpi=600, figsize=(12, 6))

    for i, location in enumerate(boxes_by_location.keys()):
        print(f"=== {location} ===")
        units = defaultdict(list)
        for box in boxes_by_location[location]:
            units[box.units].append(box)
        print("- Found", len(boxes_by_location[location]), "boxes at", location)
        
        counts = {unit:len(boxes) for unit, boxes in units.items()}
        counts = sorted(counts.items(), key=lambda x: x[0])
        labels = [x[0] for x in counts]
        str_labels = [str(l) for l in labels]
        freqs = [x[1] for x in counts]

        axes[i].bar(str_labels, freqs)
        axes[i].set_title("Humate-P Boxes at " + location)
        axes[i].set_xlabel("Units")
        axes[i].set_ylabel("Count")
        axes[i].set_yticks(range(min(freqs), max(freqs) + 1, 2))

        rects = axes[i].patches
        bar_labels = [f"{datetime.fromordinal(units[unit][0].expiration).date()} ({len(units[unit])})" for unit in labels]
        for rect, bar_label in zip(rects, bar_labels):
            height = rect.get_height()
            axes[i].text(rect.get_x() + rect.get_width() / 2, height, bar_label,
                    ha='center', va='bottom')

    fig.savefig(output_path, bbox_inches="tight")
    print("- Saved to", output_path, "\n")

