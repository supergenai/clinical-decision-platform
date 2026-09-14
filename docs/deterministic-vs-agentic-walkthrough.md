# Deterministic vs. agentic — walkthrough

One rule governs the whole system: **an LLM may only propose a candidate value with
a citation, or abstain. It never decides a branch, never sees the tree, and its
output is never trusted until a deterministic validator accepts it.**

This file is the implementation-facing version of `system-overview.html` section 4,
walked through against `trees/tree_a.example.yaml`. Read it before writing any
code that touches evidence, the tree, or the ADK skill.

## The two categories

| | Deterministic (Python, no LLM) | Non-deterministic (ADK / LLM) |
|---|---|---|
| Same input → same output, always | Yes | No — must be bounded, cited, and validated |
| Can decide a clinical branch | Never | Never |
| Tested by | Exact unit/property tests, replay equality | Arize AX experiments against a baseline, with a hard zero-tolerance gate on false acceptance |
| Where it lives | `run/`, `validator/`, `executor/` (import-linted: no I/O, no LLM client) | `orchestrator/`, `skills/extract_*` |

## Step-by-step against `tree_a.example.yaml`

| # | Step | Component | Category | Notes for implementation |
|---|---|---|---|---|
| 1 | Read `culture_gate.requires` → need `culture_result` | Controller | Deterministic | Evidence *requirements* come from the tree YAML, never from a model |
| 2 | Query BigQuery view for `culture_result` | `bigquery_adapter_c` | Deterministic | Parameterized query, patient scope bound by controller, not by tool args |
| 3 | Read `renal_gate.requires` → need `serum_creatinine` | Controller | Deterministic | |
| 4 | Query BigQuery view for `serum_creatinine` | `bigquery_adapter_p` | Deterministic | |
| 5 | Read `allergy_gate.requires` → need `allergy_class` | Controller | Deterministic | |
| 6 | Look up `allergy_class` in `evidence_registry` → `source: unstructured` | **ADK orchestrator** | Non-deterministic, but the *lookup itself* should be config-driven (see below) | This is the only "routing decision" in the system. Implement it as a table read, not a model judgment call. |
| 7 | Extract allergy class from the scanned/free-text document, with a citation | `rlm_lightrag_extraction` skill | Non-deterministic | Must return: value, citation (span or page/region), confidence/abstain. Reuse existing RLM + LightRAG components — do not rebuild extraction from scratch. |
| 8 | Validate all three candidates (type, unit, freshness, citation, patient identity) | Validator | Deterministic | Identical code path for BigQuery-sourced and RLM-sourced candidates. No source gets a shortcut. |
| 9 | Assemble the snapshot | Validator/controller | Deterministic | Immutable once written; pinned to this run |
| 10 | Evaluate `culture_gate` → `renal_gate` → `allergy_gate` → terminal node | Tree executor | Deterministic | Pure function of `(tree, node, snapshot, evaluated_at)`. No I/O. No LLM import. Must pass an import-linter check. |
| 11 | Fill the explanation template for the reached `output_code` | Template renderer | Deterministic | Fields bind only to recorded evidence/path — never freeform generation |
| 12 | Clinician approves, rejects, or resolves evidence | Human | — | The only step where judgment about the case is applied |

### The one design decision to get right: step 6

The registry (`evidence_registry` block in `tree_a.example.yaml`) is what keeps
step 6 from becoming a real agentic decision. It must stay a **static, versioned
lookup table** — `evidence key → adapter or skill` — not something the model infers
at runtime. If a future evidence key's routing is ambiguous, that ambiguity is
resolved by an engineer editing the registry, not by giving the orchestrator
discretion. Any change to make routing "smarter" (inferred rather than
looked up) is an architecture decision that needs its own review — see
`docs/mvp-plan-70-day.html`, finding **G-18**, which is exactly this class of risk.

## Hard boundaries (do not cross without a written ADR)

1. `executor/` and `validator/` packages must not import an ADK, Vertex AI, or
   any HTTP client. Enforce with an import linter in CI (CDP-603 acceptance
   criteria).
2. No `eval()`, no executable YAML tags. Trees are data, loaded with a safe
   YAML loader only.
3. A candidate from `rlm_lightrag_extraction` and a candidate from a BigQuery
   adapter pass through the *same* validator function. Do not special-case
   either source.
4. The orchestrator's evidence-routing table is versioned and reviewed like
   code. It is never regenerated or edited by the model itself.
5. Reconciliation between conflicting candidates and free-text explanation
   generation are explicitly **out of scope for this MVP** (see HLD findings
   G-18) — route conflicts to clinician review instead of building an agent
   to resolve them.

## Where to start building

1. `executor/` — implement `evaluate_node(tree, node, snapshot, evaluated_at)`
   against `trees/tree_a.example.yaml` using recorded fixture snapshots first
   (no real sources needed yet).
2. `validator/` — implement the checks in the table above against the same
   fixtures.
3. `adapters/bigquery_*` — thin, parameterized, typed. Fixture-backed for
   local dev (see `docs/mvp-plan-70-day.html`, CDP-1208).
4. `orchestrator/` — the registry-lookup dispatcher, wired to the existing
   RLM + LightRAG components for the unstructured path.
5. Everything above is testable and demoable before any real BigQuery or
   Vertex AI credentials exist.
