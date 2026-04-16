import json
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
combined_file = PROJECT_DIR / "output" / "combined_results.json"
csv_file = PROJECT_DIR / "output" / "combined_results.csv"

data = json.loads(combined_file.read_text(encoding="utf-8"))

fieldnames = ["_source_file", "invoice_number", "vendor", "total", "currency", "date"]

with csv_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow({k: row.get(k, "") for k in fieldnames})

print(f"Saved CSV to {csv_file}")
