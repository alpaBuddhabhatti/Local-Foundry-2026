import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime

PROJECT_DIR = Path(__file__).parent
DATASET_CSV = PROJECT_DIR / "invoice_dataset.csv"
SUMMARY_TXT = PROJECT_DIR / "invoice_summary.txt"


def parse_date(value):

    formats = [
        "%Y-%m-%d",
        "%d %b %Y",
        "%d %B %Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass

    raise ValueError(f"Unsupported date format: {value}")

def parse_amount(value: str) -> float:
    cleaned = value.replace("£", "").replace("$", "").replace(",", "").strip()
    return float(cleaned)

records = []
with open(DATASET_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["total_numeric"] = parse_amount(row["total"])
        row["date_parsed"] = parse_date(row["date"])
        records.append(row)

invoice_count = len(records)
total_amount = sum(r["total_numeric"] for r in records)
latest_invoice_date = max(r["date_parsed"] for r in records).strftime("%Y-%m-%d")

by_vendor = defaultdict(lambda: {"count": 0, "total": 0.0})
for r in records:
    vendor = r["vendor"]
    by_vendor[vendor]["count"] += 1
    by_vendor[vendor]["total"] += r["total_numeric"]

lines = []
lines.append("Invoice Dataset Analysis")
lines.append("=" * 30)
lines.append(f"Total number of invoices: {invoice_count}")
lines.append(f"Total invoice amount: £{total_amount:,.2f}")
lines.append(f"Latest invoice date: {latest_invoice_date}")
lines.append("")
lines.append("Invoices by vendor:")
for vendor, stats in sorted(by_vendor.items()):
    lines.append(f"- {vendor}: {stats['count']} invoices, £{stats['total']:,.2f}")

summary = "\n".join(lines)
print(summary)

with open(SUMMARY_TXT, "w", encoding="utf-8") as f:
    f.write(summary)

print(f"\nSaved summary to {SUMMARY_TXT.name}")
