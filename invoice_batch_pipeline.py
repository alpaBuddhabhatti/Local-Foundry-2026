import json
from pathlib import Path
import openai
from foundry_local_sdk import Configuration, FoundryLocalManager

PROJECT_DIR = Path(__file__).parent
INVOICES_DIR = PROJECT_DIR / "invoices"
OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_ALIAS = "phi-3-mini-4k"  # Verify with: foundry model list

def main():
    config = Configuration(app_name="invoice_batch_lab")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    model = manager.catalog.get_model(MODEL_ALIAS)
    print(f"Downloading model if needed: {MODEL_ALIAS}")
    model.download()

    print("Loading model...")
    model.load()

    manager.start_web_service()
    base_url = f"{manager.urls[0]}/v1"

    client = openai.OpenAI(
        base_url=base_url,
        api_key="none"
    )

    combined_results = []

    for invoice_file in sorted(INVOICES_DIR.glob("*.txt")):
        print(f"Processing {invoice_file.name} ...")
        invoice_text = invoice_file.read_text(encoding="utf-8")

        response = client.chat.completions.create(
            model=model.id,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract invoice_number, vendor, total, currency, date as valid JSON only. "
                        "If a field is missing, return an empty string for that field."
                    )
                },
                {
                    "role": "user",
                    "content": invoice_text
                }
            ]
        )

        result_text = response.choices[0].message.content.strip()

        output_file = OUTPUT_DIR / f"{invoice_file.stem}.json"
        output_file.write_text(result_text, encoding="utf-8")

        try:
            parsed = json.loads(result_text)
            parsed["_source_file"] = invoice_file.name
            combined_results.append(parsed)
        except Exception:
            combined_results.append({
                "_source_file": invoice_file.name,
                "_raw_output": result_text
            })

    combined_file = OUTPUT_DIR / "combined_results.json"
    combined_file.write_text(json.dumps(combined_results, indent=4), encoding="utf-8")

    print(f"Saved combined results to {combined_file}")

    model.unload()
    manager.stop_web_service()
    print("Batch pipeline completed successfully.")

if __name__ == "__main__":
    main()
