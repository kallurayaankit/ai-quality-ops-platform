# 🧠 AI Quality Ops Platform

**End‑to‑end AI Quality Operations ecosystem** – continuously validates, monitors, and guards every aspect of an AI product, from training data to production inference.

[![CI/CD Pipeline](https://github.com/kallurayaankit/ai-quality-ops-platform/actions/workflows/ai-quality.yml/badge.svg)](https://github.com/kallurayaankit/ai-quality-ops-platform/actions)

---

## 💡 What it does

Not just a test suite – a platform that emulates what a **Staff AI QA Engineer** would build at a top‑tier AI company.  
It runs five automated quality pillars:

1. **Data Integrity** – checks training/input data for missing values, duplicates, and schema compliance.  
2. **Accuracy & RAG Evaluation** – verifies that AI answers contain correct facts and, for RAG systems, use the right documents.  
3. **Security & Bias Red‑Teaming** – probes for prompt injection, toxicity, and fairness using adversarial agents.  
4. **Performance & Cost SLA** – measures p95 latency and estimates token cost, failing if thresholds are exceeded.  
5. **Observability & Drift Detection** – logs metrics and alerts if model behavior drifts from a healthy baseline.

All orchestrated by a single **master test plan** (JSON), with **HTML reports** generated after every run.

---

## 🏗️ Architecture
ai-quality-ops-platform/
├── orchestrator/ # Master runner – reads test plan, dispatches pillars
├── tests/
│ ├── pillar1/ # Data integrity
│ ├── pillar2/ # Accuracy & RAG evaluation
│ ├── pillar3/ # Security & bias
│ ├── pillar4/ # Performance & cost
│ └── pillar5/ # Observability & drift
├── qa_service/ # QA‑as‑a‑Service REST API + web UI
├── mock_ai_service/ # Example AI endpoint for testing
├── test_plans/ # JSON test plans & baselines
├── reports/ # Generated HTML reports
├── Dockerfile # Main project container
├── docker-compose.yml # Full stack (mock, test‑runner, QA service)
└── .github/workflows/ # CI/CD pipeline (GitHub Actions)


---

## 🚀 Quick Start (local)

**Prerequisites:** Docker Desktop & Git.

```bash
git clone https://github.com/kallurayaankit/ai-quality-ops-platform.git
cd ai-quality-ops-platform
docker compose up test-runner
