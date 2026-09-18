# AI Quality Ops Platform

**End-to-end AI Quality Operations** — continuously validates, monitors, and guards every aspect of an AI product, from training data to production inference.

Five automated quality pillars, orchestrated by a single JSON test plan, producing HTML reports with policy-gated pass/fail decisions.

## Architecture

```mermaid
flowchart TB
    TP[Test Plan JSON] --> ORCH[Orchestrator]
    POL[Policies YAML] -.-> ORCH
    ORCH --> P1[Pillar 1: Data Integrity]
    ORCH --> P2[Pillar 2: Accuracy and RAG]
    ORCH --> P3[Pillar 3: Security and Bias]
    ORCH --> P4[Pillar 4: Performance and Cost]
    ORCH --> P5[Pillar 5: Observability and Drift]
    P1 --> AI[AI Under Test]
    P2 --> AI
    P3 --> AI
    P4 --> AI
    P5 --> AI
    P1 --> REP[HTML Reports]
    P2 --> REP
    P3 --> REP
    P4 --> REP
    P5 --> REP
```

## Runtime flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Orch as Orchestrator
    participant Pillar as Pillar Tests
    participant AI as AI Service
    participant Report as Report Generator
    Dev->>Orch: python demo/run.py
    Orch->>Orch: load plan and policies
    loop For each pillar
        Orch->>Pillar: pytest tests/pillarN
        Pillar->>AI: HTTP request
        AI-->>Pillar: JSON response
        Pillar->>Pillar: assert against thresholds
        Pillar-->>Orch: pass or fail
    end
    Orch->>Report: generate summary.html
    Report-->>Dev: open in browser
    Orch-->>Dev: exit 0 or 1
```

## What it does

Runs five automated quality pillars:

| # | Pillar | What it checks |
|---|---|---|
| 1 | **Data Integrity** | Missing values, duplicates, schema compliance |
| 2 | **Accuracy & RAG** | Correct facts, right documents, faithfulness |
| 3 | **Security & Bias** | Prompt injection, toxicity, fairness, PII |
| 4 | **Performance & Cost** | p95 latency, token cost, SLA thresholds |
| 5 | **Observability & Drift** | Metric logging, baselines, drift alerts |

Each pillar reads its thresholds from `policies/`. If a blocking pillar fails, the run aborts with a non-zero exit code — ready for CI.

## Quickstart — one command

```bash
git clone https://github.com/kallurayaankit/ai-quality-ops-platform.git
cd ai-quality-ops-platform
python demo/run.py
```

The demo:

- Builds a bundled mock AI service (no external dependencies, no submodules)
- Starts it in Docker
- Runs the accuracy pillar against it
- Writes `reports/summary.html`
- Exits 0 if the blocking pillar passes, 1 otherwise

The bundled mock answers a few fixed questions (capital of France, largest planet, etc.) so the accuracy test has a deterministic target.

**Verified output:**

```
===== Running suite: accuracy =====
..                                                              [100%]
Master report saved: reports/summary.html

Suite         Status   Detailed Report
accuracy      PASS     Open Report
Overall Verdict: PASS
```

Open `reports/summary.html` in your browser. A committed copy lives at [`docs/sample-report/summary.html`](docs/sample-report/summary.html).

## Policies

Quality gates live in `policies/` as YAML. Each file defines thresholds for one pillar:

```yaml
# policies/accuracy.yaml
pillar: accuracy
blocking: true
metrics:
  correctness:
    threshold: 0.80
    comparison: ">="
  faithfulness:
    threshold: 0.85
    comparison: ">="
  hallucination_rate:
    threshold: 0.10
    comparison: "<="
```

The orchestrator loads every `policies/*.yaml` and passes the thresholds to the pillar tests via environment variables. Change a threshold, re-run, get a different verdict — no code changes.

See [`policies/README.md`](policies/README.md) for the full format.

## Repository layout

```
ai-quality-ops-platform/
├── orchestrator/          # Master runner
├── tests/
│   ├── pillar1/           # Data integrity
│   ├── pillar2/           # Accuracy & RAG
│   ├── pillar3/           # Security & bias
│   ├── pillar4/           # Performance & cost
│   └── pillar5/           # Observability & drift
├── policies/              # YAML quality gates
├── test_plans/            # JSON test plans
├── demo/                  # Self-contained mock AI service
├── reports/               # Generated HTML
├── qa_service/            # QA REST API + web UI
├── mock_ai_service/       # Example AI endpoint
├── docs/                  # Diagrams, sample reports
├── Dockerfile
├── docker-compose.yml
├── docker-compose.demo.yml
└── .github/workflows/     # CI/CD
```

## Tech stack

Python · pytest · FastAPI · uvicorn · Docker & Docker Compose · GitHub Actions · pytest-html

## License

MIT — see [LICENSE](LICENSE).

## Author

Ankit Kalluraya — AI Quality Architect | Staff QA Engineer
