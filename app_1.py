import openai
from foundry_local_sdk import Configuration, FoundryLocalManager

# 1) Purpose: initialize Foundry Local once so the app can find models and manage runtime.
# Why: without this, model catalog and local inference APIs are unavailable.
config = Configuration(app_name="invoice_lab")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# 2) Purpose: select which local model should perform extraction.
# Why: model alias maps your task to a specific model/variant available in Foundry Local.
model = manager.catalog.get_model("phi-3-mini-4k")

# 3) Purpose: make sure model files exist and are loaded for inference.
# Why: download is needed on first use; load prepares model in memory for faster requests.
model.download()
model.load()

# 4) Purpose: expose a local OpenAI-compatible endpoint.
# Why: OpenAI SDK expects a base URL; Foundry service provides that local API surface.
manager.start_web_service()
base_url = f"{manager.urls[0]}/v1"

# 5) Purpose: create a client to send standard chat-completions requests.
# Why: this keeps usage familiar while routing calls to your local model instead of cloud.
client = openai.OpenAI(
    base_url=base_url,
    api_key="none"
)

# 6) Purpose: provide raw invoice content as model input.
# Why: the model needs source text to extract structured fields.
invoice_text = """
Invoice Number: INV-2025-001
Vendor: ABC Supplies Ltd
Total: £1,240.00
Date: 10 Feb 2025
"""

# 7) Purpose: instruct model to return only required fields in JSON format.
# Why: structured JSON is easier to validate, parse, and store in downstream systems.
response = client.chat.completions.create(
    model=model.id,
    messages=[
        {
            "role": "system",
            "content": "Extract invoice_number, vendor, total, currency, and date. Return valid JSON only."
        },
        {
            "role": "user",
            "content": invoice_text
        }
    ],
    stream=False
)



print(response.choices[0].message.content)

# 9) Purpose: release resources after inference completes.
# Why: unloading model and stopping service helps avoid memory leaks and port conflicts.
model.unload()
manager.stop_web_service()