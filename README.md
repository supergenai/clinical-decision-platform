# Clinical Decision Platform — Tree A

A reusable clinical decision-tree platform: deterministic Python traversal
over a versioned evidence snapshot, with one bounded LLM step (Google ADK +
RLM/LightRAG) used only to extract cited candidate values from documents and
images. The LLM never sees the tree and never chooses a branch.

**Start here if you're implementing:** [`DEVIN_INSTRUCTIONS.md`](DEVIN_INSTRUCTIONS.md)

## Contents

| Path | What it is |
|---|---|
| [`docs/hld-v1.0.html`](docs/hld-v1.0.html) | Original high-level design |
| [`docs/mvp-plan-70-day.html`](docs/mvp-plan-70-day.html) | Full MVP plan: scope, architecture, business process & screens, system integration, team, watch-outs, cadence, timeline, epics & stories |
| [`docs/system-overview.html`](docs/system-overview.html) | Two-page architecture summary: deterministic vs. agentic split, outcome measurement, and a worked example of one synthetic case traversing the tree |
| [`docs/deterministic-vs-agentic-walkthrough.md`](docs/deterministic-vs-agentic-walkthrough.md) | Implementation-facing version of the above — read before writing code |
| [`trees/tree_a.example.yaml`](trees/tree_a.example.yaml) | Starter tree scaffold matching the worked example. Not clinically approved — a build target, not a clinical artifact. |
| [`jira/mvp-backlog.csv`](jira/mvp-backlog.csv) | 232 stories across 13 epics, ready to import into Jira |
| [`tools/generate-plan/`](tools/generate-plan/) | The generator that produces the plan page and backlog CSV together, so both stay consistent when scope changes |

## The one rule

Deterministic Python decides everything clinical — evidence requirements,
validation, branch selection, review state, audit. The LLM (ADK
orchestrator, RLM + LightRAG) only proposes a cited candidate value or
abstains, and nothing it returns is trusted until a deterministic validator
accepts it. See the walkthrough doc for exactly where that line sits in
`trees/tree_a.example.yaml`.

## Status

Design and planning stage. No application code yet — this repo is the
handoff package for the next engineer or agent to start implementation
against. Regulatory scope, clinical thresholds, and a few architecture ADRs
are pending sign-off (see "Decisions needed this week" in the plan).
