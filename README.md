# guardrail-sdk-poc


https://github.com/user-attachments/assets/c0eee824-02f2-426c-a265-f9eb310b2b85

1️⃣ pip install guardrails-ai

Approx install size (including dependencies):

Component	Approx Size
guardrails-ai core	~5–10 MB
pydantic, typer, etc	~10–15 MB
nltk (dependency)	~15–25 MB
other misc deps	~10–20 MB

Total pip footprint:
👉 ~40–70 MB installed in virtualenv

This is normal Python package weight.

2️⃣ guardrails hub install hub://guardrails/detect_pii

This installs:

DetectPII validator package

NLTK tokenizer models (punkt etc.)

Some rule-based detection components

Approx additional size:

Component	Approx Size
detect_pii validator	~1–3 MB
nltk punkt model	~10–15 MB
additional tokenizer assets	~5–10 MB

Total additional footprint:
👉 ~15–25 MB

3️⃣ Hub API key setup

This adds:

Zero MB

Just config file (~few KB)

💡 Total Realistic Disk Impact

If someone sets this up from scratch:

👉 ~55 MB – 95 MB total inside venv
