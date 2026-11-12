# TechBid AI

**AI-powered RFQ analysis & technical sales automation**

A working prototype that turns customer requests into structured technical-commercial reviews. It extracts requirements using **Gemini or a Python baseline**, checks them against a fictional catalog, flags missing specifications, and routes requests through a real **n8n + FastAPI** workflow.

**Python · FastAPI · Gemini · Pydantic · n8n · Prompt Evaluation · Pytest**

## From request to action

1. **Receive an RFQ:** a customer asks for industrial equipment, quantities, budget and delivery date.
2. **Extract requirements:** Gemini returns structured fields validated by Pydantic (or use Python rules without an LLM).
3. **Evaluate:** deterministic Python rules check specified attributes, price and lead time; incomplete cases are flagged for human review.
4. **Route the case:** a published n8n webhook sends it to `sales_review` or `technical_review`, and records the outcome back in FastAPI.

```text
Customer RFQ
    |
    v
Gemini / Python baseline --> Structured requirements
    |
    v
Python catalog checks --> Proposal draft or missing information
    |
    v
FastAPI webhook --> n8n --> Review queue --> FastAPI inbox
```

## Application demonstration

**RFQs routed to the right review queue** — a complete request is sent to commercial review, while an incomplete application requires technical clarification.

![TechBid AI interface showing sales and technical review queues](docs/screenshots/techbid-review-queues.png)

**Verified end-to-end n8n workflow** — webhook receipt, queue selection, API inbox registration and confirmation. The screenshot shows a successful execution of all four steps.

![Successful n8n execution with four connected green steps](docs/screenshots/n8n-successful-execution.png)

## Measured results

A small, labeled test set of **five synthetic RFQs** was used to compare the two extraction approaches:

| Metric | Python rules | Gemini, Prompt B |
|---|---:|---:|
| Correct present fields | 22 / 27 (81.5%) | **27 / 27 (100%)** |
| Correct product category | 4 / 5 | **5 / 5** |
| Fully correct extraction records | 3 / 5 | **5 / 5** |

The figures come from the reproducible Python baseline and a **real Gemini test executed locally**, with the reported model output saved in `evidence/`. These are five **synthetic demonstration cases**, not an estimate of accuracy in production. Prompt A produced at least one invalid structured value (`trilho DIN` instead of `DIN`), illustrating why output validation matters.

**Workflow verification:** three successful n8n runs were observed locally, including successful routing to both review queues. **34 automated Python tests passed** in the packaged build.

## Architecture & technical choices

| Component | Responsibility |
|---|---|
| **FastAPI** | Application API, Swagger documentation and workflow endpoints |
| **Gemini** | Extract RFQ requirements into structured fields |
| **Pydantic** | Reject invalid AI outputs rather than silently accepting them |
| **Python baseline** | Low-cost reference extractor for objective comparison |
| **Rules + fictional catalog** | Check known parameters, calculate prices and identify missing inputs |
| **n8n** | Route RFQs through an actual external workflow |
| **Pytest** | Test extraction, validation, API and evaluation behavior |

**Engineering safeguard:** a shortlisted product is *not* an approved technical selection. All catalog items, prices, deadlines and sample requests are fictitious; a commercial/engineering reviewer must confirm the final proposal.

## Run locally

**Windows — recommended**

1. Install Python 3.11+.
2. Double-click `INICIAR_WINDOWS.bat` in the project folder. It installs dependencies and guides the optional local Gemini key configuration.
3. Open **http://127.0.0.1:8000**. The Python **Baseline** works without any Google API calls.

For Gemini analysis, use your own key in the local `.env` (never upload it), with a model accessible to your project. `GEMINI_MODEL=gemini-3.5-flash-lite` is the example configuration that worked during local testing. The model's availability and quota are controlled by Google.

**Run the tests** (no Gemini calls):

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

**n8n demo:** import `n8n/techbid_workflow.json`, publish it and set the actual local production webhook URL in `.env`. When n8n runs in Docker, the workflow uses `host.docker.internal` to reach the locally running FastAPI app. Full instructions: [Guia rápido em português](docs/GUIA_RAPIDO_PT.md).

## Repository layout

```text
techbid-ai/
├── README.md
├── INICIAR_WINDOWS.bat
├── .env.example
├── requirements.txt
├── techbid/              # Python API, extraction and business rules
├── static/               # Web interface
├── data/                 # Fictional catalog and labeled RFQs
├── n8n/                  # Importable workflow
├── docs/                 # Real screenshots and setup guide
├── evidence/             # Baseline and Gemini test summaries
└── tests/                # Automated tests
```

---

**Author:** Ioglas Alves da Fonseca · Electrical Engineering · Technical Sales · Applied AI
