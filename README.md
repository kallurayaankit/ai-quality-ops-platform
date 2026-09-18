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
