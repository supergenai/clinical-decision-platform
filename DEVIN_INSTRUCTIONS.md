# Instructions for the build agent

Read in this order before writing any code:

1. **`docs/deterministic-vs-agentic-walkthrough.md`** — start here. It's the
   short version of the one rule that governs every design decision in this
   repo: deterministic Python decides everything clinical; the LLM (via ADK,
   RLM, LightRAG) only proposes a cited value or abstains, and is never
   trusted until a deterministic validator accepts it.
2. **`docs/system-overview.html`** — open in a browser. Two pages: the
   architecture split (deterministic vs. non-deterministic components) and a
   worked example showing one synthetic case traverse `trees/tree_a.example.yaml`
   step by step, with the responsible component named at each step.
3. **`docs/mvp-plan-70-day.html`** — the full plan. Sections in order:
   MVP scope → architecture → business process & screens → system integration
   (interface catalogue, IF-01 through IF-15) → team → **watch-outs for a
   first-time agentic team** (read this one carefully — it names the specific
   traps: logic creeping into prompts, tuning by eye instead of by
   experiment, averages hiding a dangerous single error) → cadence →
   timeline → epics & stories.
4. **`docs/hld-v1.0.html`** — the original high-level design, for the parts
   the plan doesn't restate (snapshot schema, review semantics, GCP service
   ownership).

## Starting point for code

- `trees/tree_a.example.yaml` — a concrete, non-clinically-approved tree
  matching the worked example in the overview doc. Build the compiler,
  validator and executor against this file and its fixture data before any
  real source or model credentials exist.
- `jira/mvp-backlog.csv` — 232 stories across 13 epics, each with acceptance
  criteria, dependencies, and the story that comes before it. Import to Jira,
  or work directly off it. Story keys referenced in the walkthrough and plan
  (e.g. `CDP-601`, `CDP-503`) are rows in this file.
- `tools/generate-plan/` — the Python script that generated the plan and
  backlog. If scope changes, edit `build70.py` (the story/epic data) and
  `body70.html` (the page prose), then run
  `python3 build70.py <out.html> <out.csv> template70.html` to regenerate
  both consistently rather than hand-editing the CSV or HTML separately.

## Guardrails — non-negotiable for this repo

- **Credentials:** your sessions get access to a dev-only environment with
  synthetic data. No staging, prod, or real-source credentials, ever.
- **Protected test oracles:** never edit an expected tree path, a golden
  eval case, or a safety test's assertion to make it pass. If a test is
  wrong, open a PR that says so and let a human (clinical lead for
  clinical fixtures, two engineers for `executor/`/`validator/`) decide.
- **No LLM in `executor/` or `validator/`:** these packages must not import
  an ADK, Vertex AI, or HTTP client. This is enforced by an import linter in
  CI (CDP-603) — don't work around it.
- **No `eval()`, no executable YAML tags.** Trees load through a safe YAML
  loader only.
- **PR size:** keep PRs small (~400 changed lines, excluding generated
  files) and scoped to one story. Link the Jira/backlog key in the PR.
- **Any new agent, tool, or routing capability beyond the static
  `evidence_registry` lookup needs a written ADR before it's built** — see
  the walkthrough's "hard boundaries" section. This includes anything that
  would let the orchestrator choose between tools by judgment rather than
  by table lookup, and anything resembling reconciliation across conflicting
  evidence or freeform explanation generation (both explicitly out of scope
  — HLD finding G-18).

## First tasks, in order

1. `executor/evaluate_node()` — pure function, property-tested for
   determinism, against `trees/tree_a.example.yaml` fixtures.
2. `validator/` — type, unit, freshness, citation, identity checks, run
   against both a fixture BigQuery-shaped candidate and a fixture
   RLM-extracted candidate to prove the code path is identical.
3. `adapters/bigquery_p`, `adapters/bigquery_c` — typed, parameterized,
   fixture-backed for local dev.
4. `orchestrator/` — the registry-driven dispatcher wired to the existing
   RLM + LightRAG components for `allergy_class`.
5. Wire steps 1-4 together behind the run API's job queue once each is
   independently tested.

Open questions that need a human, not an agent, to resolve are listed at the
end of `docs/mvp-plan-70-day.html` ("Decisions needed this week") and in the
plan's Day 30 checkpoint card. Don't guess at clinical thresholds, regulatory
scope, or the single-Postgres/job-queue architecture decisions — they're
pending sign-off, not implementation details.
