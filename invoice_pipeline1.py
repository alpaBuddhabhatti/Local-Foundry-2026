
import openai
from pathlib import Path
from foundry_local_sdk import Configuration, FoundryLocalManager

# STEP 1 — Initialize Foundry Local SDK
config = Configuration(app_name="invoice_pipeline_lab")
FoundryLocalManager.initialize(config)

manager = FoundryLocalManager.instance

# STEP 2 — Select Phi model
model = manager.catalog.get_model("phi-3-mini-4k")

print("Downloading model if needed...")
model.download()

print("Loading model...")
model.load()

# STEP 3 — Start local inference service
manager.start_web_service()
base_url = f"{manager.urls[0]}/v1"

client = openai.OpenAI(
    base_url=base_url,
    api_key="none"
)

# STEP 4 — Read invoice file from common project locations
invoice_name = "sample_invoice.txt"
script_dir = Path(__file__).resolve().parent

candidate_paths = [
    Path.cwd() / invoice_name,
    script_dir / invoice_name,
    script_dir / "Foundry" / invoice_name,
]

invoice_path = next((p for p in candidate_paths if p.exists()), None)
if invoice_path is None:
    searched = "\n".join(str(p) for p in candidate_paths)
    raise FileNotFoundError(
        f"Could not find '{invoice_name}'. Checked:\n{searched}"
    )

with open(invoice_path, "r", encoding="utf-8") as file:
    invoice_text = file.read()

print(f"Using invoice file: {invoice_path}")

# STEP 5 — Run extraction prompt
response = client.chat.completions.create(
    model=model.id,
    messages=[
        {
            "role": "system",
            "content": "Extract invoice_number, vendor, total, currency, date. Return JSON only."
        },
        {
            "role": "user",
            "content": invoice_text
        }
    ]
)

result_text = response.choices[0].message.content

print("\nExtracted JSON:\n")
print(result_text)

# STEP 6 — Save JSON output
output_filename = "extracted_invoice.json"

with open(output_filename, "w", encoding="utf-8") as outfile:
    outfile.write(result_text)

print(f"\nSaved output to {output_filename}")

# STEP 7 — Clean up resources
model.unload()
manager.stop_web_service()

print("\nPipeline completed successfully.")
