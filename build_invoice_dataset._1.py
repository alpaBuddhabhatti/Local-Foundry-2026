import json
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
OUTPUT_DIR = PROJECT_DIR / "output"

DATASET_JSON = PROJECT_DIR / "invoice_dataset.json"
DATASET_CSV = PROJECT_DIR / "invoice_dataset.csv"

records = []

for file in OUTPUT_DIR.glob("*.json"):

    try:
        text = file.read_text(encoding="utf-8").strip()

        # Remove markdown JSON wrappers if present
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        data = json.loads(text)

        # Ensure dictionary structure
        if isinstance(data, dict):
            data["_source_file"] = file.name
            records.append(data)

        else:
            print(f"Skipping non-dictionary JSON in {file.name}")

    except Exception as e:
        print(f"Skipping invalid JSON file: {file.name}")
        print(e)


# Save combined dataset JSON
with open(DATASET_JSON, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=4)


# Save CSV dataset
import csv

fieldnames = [
    "_source_file",
    "invoice_number",
    "vendor",
    "total",
    "currency",
    "date"
]

with open(DATASET_CSV, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for record in records:
        writer.writerow(record)


print("\nDataset created successfully ✅")
print("Generated files:")
print("invoice_dataset.json")
print("invoice_dataset.csv")