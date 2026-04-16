# Foundry Local Lab 4 – Batch Invoice Processing

## What this exercise does

This lab processes multiple invoice text files from the `invoices` folder using a local Phi model with Microsoft Foundry Local.

Flow:

invoices/*.txt
↓
Foundry Local Phi model
↓
JSON per invoice
↓
output folder
↓
combined_results.json

## Files included

. `invoice_batch_pipeline.py` – batch processing script
. `convert_results_to_csv.py` – optional converter from combined JSON to CSV
. `requirements.txt` – Python dependencies
. `invoices/` – sample invoice text files
. `output/` – output folder for generated results

## Setup

1. Open this folder in VS Code.
2. Open Terminal.
3. Activate your virtual environment if you use one.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the batch invoice pipeline

```bash
python invoice_batch_pipeline.py
```

## Optional: convert combined JSON to CSV

```bash
python convert_results_to_csv.py
```

## Output files

The script creates:

. `output/invoice_001.json`
. `output/invoice_002.json`
. `output/invoice_003.json`
. `output/combined_results.json`

Optional CSV:

. `output/combined_results.csv`

## Important note about Phi model alias

This package uses:

```python
MODEL_ALIAS = "phi-3-mini-4k"
```

Before running, verify your machine supports that exact alias:

```bash
foundry model list
```

If your machine shows a different Phi alias, update `MODEL_ALIAS` in `invoice_batch_pipeline.py`.
