import csv, html, sys, os
from collections import defaultdict

E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_HTML, OUT_CSV, TEMPLATE = sys.argv[1], sys.argv[2], sys.argv[3]

exec(open(os.path.join(HERE, "findings_block.py"), encoding="utf-8").read())  # defines FINDINGS

# ---------------------------------------------------------------- team & calendar
OWNERS = {
 "LEAD": ("Lead engineer", "Architecture and ADRs, agent-engineering coach, Devin guardrails, hazard log, threat model, access and dependency owner, Day-70 decision."),
 "E1": ("Engineer 1 · Data", "BigQuery adapters for P and C, data-team liaison, identity binding, terminology registry, eager snapshot, audit chain, UAT case pack."),
 "E2": ("Engineer 2 · Evidence & AI", "Snapshot schema, validator, ADK spike and extraction skill, Arize AX tracing, evaluators, agent-eval lane, held-out set."),
 "E3": ("Engineer 3 · Logic & review UI", "Tree compiler, operators, pure executor, bundles and kill switch, sign-in, worklist, review screen, audit timeline, explanation templates."),
 "E4": ("Engineer 4 · Platform", "Devin-ready dev environment, CI lanes, Terraform, Postgres, run state machine and job queue, review API, fault-injection suite."),
}
ITERS = ["I1","I2","I3","I4","I5","I6","I7","I8","I9"]
ORDER = ITERS + ["T","P2"]
CAP = {"E": {"I1":5,"I2":5,"I3":6.5,"I4":6.5,"I5":6.5,"I6":6.5,"I7":6.5,"I8":6.5,"I9":3},
       "LEAD": {"I1":5,"I2":5,"I3":5,"I4":2,"I5":2,"I6":2,"I7":2,"I8":2,"I9":1}}

ITER_INFO = [
 ("I1","Days 1–7","Foundations & bootcamp","Two-day agent-engineering bootcamp. Devin dev environment and guardrails live. Access pack and intended use sent. Snapshot schema; tree compiler; evidence matrix.","Devin opens a guarded PR that passes the fast lane; Tree A YAML compiles or fails with clear errors."),
 ("I2","Days 8–14","Contracts","CI lanes live. ADK spike traced in Arize AX. ADRs signed. Typed operators. Terminology registry and minimum-necessary spec.","A spike extraction trace in the AX dev space; operator boundary tests."),
 ("I3","Days 15–21","Core logic","Validator; pure executor; bundles; hazard log v1; Postgres; fixtures from the real BigQuery schemas; freshness gate measured.","The executor walks a Tree A node on a fixture snapshot; P and C load-lag numbers."),
 ("I4","Days 22–28","Walking skeleton","Every Tree A path passes on fixtures; run API and state machine in dev; P adapter on the BigQuery dev dataset; evaluators and agent-eval lane; templates.","POST a run, get a recorded path and audit; first AX scorecard baseline."),
 ("CP30","Day 30","Checkpoint 1","Product owner checkpoint: keep course, re-scope, or pull the real-data stretch forward.","See the Day 30 criteria."),
 ("I5","Days 29–35","Durable & agentic","Extraction skill v1; job queue with hash-chained audit; C adapter; sign-in and roles; kill switch.","A run survives a worker kill; the kill switch halts a run; skill v1 compared with baseline."),
 ("I6","Days 36–42","Clinician loop","Review API and screen; worker loop; eager snapshot; timezone rules; PHI-leak test; adversarial set.","A clinician approves and rejects Tree A cases in staging."),
 ("I7","Days 43–49","Safety depth","Revalidation before approval; conflict detection; document retrieval; failure-to-regression loop; fail-closed state; approval gating; screen iteration; staging deploy lane.","A pending culture gives no recommendation; an amended result forces recompute."),
 ("I8","Days 50–56","Quality push","Skill iteration to thresholds; frozen held-out set; UAT case pack; fault-injection suite.","Eval scorecard against thresholds; fault-injection run."),
 ("I9","Days 57–60","Buffer & freeze","No planned stories: spillover, documentation, test plan. Code freeze at end of day 60.","Checkpoint 2: feature-complete demo in staging."),
 ("T","Days 61–70","Test window","System verification against hazard log, fault injection, clinician UAT, held-out eval, restore test, data traceability.","Checkpoint 3: Day-70 decision."),
]

EPICS = [
 ("CDP-1","Governance, clinical safety & regulatory","LEAD","Safety and compliance evidence produced as work, not paperwork at the end."),
 ("CDP-2","Platform foundation","E4","Environments as code, CI/CD, and a deploy path to staging."),
 ("CDP-3","Source adapters & terminology","E1","Read-only, provenance-complete evidence from P and C in BigQuery."),
 ("CDP-4","Evidence snapshot & validation","E2","One consistent snapshot per run; absence is never a value."),
 ("CDP-5","AI evidence extraction","E2","One bounded, cited, abstaining ADK skill, improved by measurement."),
 ("CDP-6","Tree DSL & deterministic executor","E3","Trees as immutable data evaluated by a pure function."),
 ("CDP-7","Durable run orchestration","E4","Runs that survive restarts and duplicates and fail closed."),
 ("CDP-8","Clinician review","E3","A review loop clinicians can independently verify."),
 ("CDP-9","Security, access & audit","E3","Role-based access and tamper-evident audit."),
 ("CDP-10","Observability","E2","PHI-free telemetry and operational signals."),
 ("CDP-11","Verification, test window & release","LEAD","Prove it works, then decide; shadow mode follows in Phase 2."),
 ("CDP-12","Enterprise data access & readiness","LEAD","Approved, least-privilege access to P and C in BigQuery, started on day one."),
 ("CDP-13","Agent engineering: Devin, Arize AX & CI","LEAD","The build-measure-improve loop for agents, with guardrails for AI-written code."),
]

S = []
def st(key, epic, owner, pts, it, title, as_, want, so, ac, deps=(), gaps=()):
    S.append(dict(key=key, epic=epic, owner=owner, pts=pts, sprint=it, title=title, as_=as_, want=want, so=so, ac=ac, deps=list(deps), gaps=list(gaps)))

# ---------------- CDP-1
st("CDP-101","CDP-1","LEAD",3,"I1","Intended-use statement sent to counsel","clinical safety officer",
   "a signed intended-use statement for Tree A sent to regulatory counsel in week one","the determination is ready before any real patient data (Phase 2)",
   ["Names user, population, care setting and Tree A scope; no autonomous action or writeback","Assesses the non-device CDS criteria against the review-screen design","Counsel's determination tracked as a Phase 2 entry gate"], gaps=["G-01"])
st("CDP-103","CDP-1","LEAD",3,"I2","ADRs for MVP architecture choices","engineering team",
   "ADRs for single Postgres store, Postgres job queue, direct BigQuery reads via views, eager snapshot, and template explanations","the MVP's deviations from HLD v1.0 are explicit and reversible",
   ["Five ADRs with context, decision, consequences, and revisit trigger","Product owner and architecture sign-off recorded"], gaps=["G-13","G-17","G-06","G-18"])
st("CDP-102","CDP-1","LEAD",5,"I3","Hazard log v1 with hazard → control → test links","clinical safety officer",
   "every identified hazard linked to a control and a test ID","the Day-70 verification has a checklist that means something",
   ["Covers wrong patient, stale/superseded evidence, missing-as-negative, fabricated extraction, bypassed review, defective bundle, PHI egress, AI-written test tampering",
    "Each hazard has severity, control, verifying test, and residual risk","CI fails if a referenced test ID disappears"], deps=["CDP-101"], gaps=["G-01"])
st("CDP-104","CDP-1","LEAD",2,"I4","Threat model (lite)","security reviewer",
   "a STRIDE pass over API, worker, BigQuery access, model calls, telemetry, and the Devin supply chain","controls exist for the threats we introduce",
   ["Covers document prompt injection, cross-patient access, PHI egress via spans/errors, over-privileged agent credentials","Each threat mapped to a story or accepted risk; reviewed by security"], gaps=["G-14"])
st("CDP-107","CDP-1","LEAD",2,"I4","Pre-registered Day-70 thresholds","product owner",
   "numeric pass criteria for the extraction skill and safety suite signed before the held-out set is frozen","the Day-70 decision isn't fitted to results",
   ["Zero false acceptances; 100% citation validity; field-accuracy target stated with sample size","Signed by clinical lead and product owner before CDP-1403"], deps=["CDP-102"], gaps=["G-08"])
st("CDP-106","CDP-1","LEAD",3,"P2","Dual-annotation labeling protocol","clinical lead",
   "two independent annotators and adjudication for real-data evaluation","Phase 2 ground truth doesn't rest on one person",
   ["Guideline with worked examples; κ reported; not a gate until κ ≥ 0.8"], gaps=["G-07"])

# ---------------- CDP-2
st("CDP-202","CDP-2","E4",5,"I2","CI fast and integration lanes","engineer",
   "a fast lane (lint, strict types, unit and property tests, tree compiler, import rules, secret scan, SAST) and an integration lane (docker compose end-to-end on fixtures)","every PR, human or Devin, gets the same checks within minutes",
   ["Fast lane under 10 minutes; integration lane under 20; both required on main","Recorded model responses used; no live model calls outside eval lanes","Branch protection and merge queue enabled"], deps=["CDP-1301"], gaps=["G-14"])
st("CDP-201","CDP-2","E4",3,"I3","Dev and staging environments as code","platform engineer",
   "Terraform for dev and staging projects with VPC Service Controls and CMEK","environments are reproducible and synthetic-only in the MVP",
   ["No console-created resources","Dev project is the only one Devin credentials can reach","Prod project deferred to Phase 2 (CDP-209)"], gaps=["G-14"])
st("CDP-204","CDP-2","E4",3,"I3","Cloud SQL for PostgreSQL","platform engineer",
   "a Postgres instance with PITR and forward-only migrations","run state, job queue and audit share one transactional store",
   ["PITR enabled; migrations in CI","Audit role limited to INSERT and SELECT"], deps=["CDP-201"], gaps=["G-13","G-05"])
st("CDP-203","CDP-2","E4",3,"I5","API and worker services on Cloud Run","platform engineer",
   "separate api and worker services with distinct least-privilege identities","the API cannot call model or source tools directly",
   ["Worker has no public ingress; min instances ≥ 1 for queue polling","Structured logs with PHI redaction"], deps=["CDP-202","CDP-201"])
st("CDP-208","CDP-2","E4",3,"I7","Staging deploy lane with manual approval","product owner",
   "every merged build deployable to staging with one approval and a recorded bundle hash","the Friday demo always runs on a known build",
   ["Deploy records git SHA, image digest and bundle hashes","Rollback to previous build in one step"], deps=["CDP-202","CDP-201"])
st("CDP-209","CDP-2","E4",5,"P2","Production project and perimeter","platform engineer",
   "a prod project with VPC-SC bridged to the data team's BigQuery perimeter","real patient data stays inside an approved boundary",
   ["No Devin access; JIT human access only"], deps=["CDP-201"], gaps=["G-14"])
st("CDP-206","CDP-2","E4",2,"P2","Just-in-time production access","privacy officer",
   "no standing human access to prod data","engineer access to PHI is exceptional and logged",
   ["Approved, time-bound elevation with alert"], deps=["CDP-209"], gaps=["G-11"])
st("CDP-207","CDP-2","E4",3,"P2","Attested production deploys","security reviewer",
   "SBOM, Binary Authorization, and signed attestations for prod","only verified images reach patients' data",
   ["Unattested images blocked"], deps=["CDP-202"], gaps=["G-14"])

# ---------------- CDP-3
st("CDP-301","CDP-3","E1",5,"I1","Tree A evidence matrix","data engineer",
   "every Tree A evidence key mapped to BigQuery table/column, codes, units, time meaning, and gaps","adapters start from verified facts",
   ["Covers P and C tables; notes observed_at vs load time","Clinical lead reviewed"], gaps=["G-09"])
st("CDP-302","CDP-3","E1",3,"I2","Terminology registry for Tree A concepts","evidence engineer",
   "each Tree A key bound to LOINC/SNOMED CT/RxNorm value sets with UCUM units","local code changes can't silently alter meaning",
   ["serum_creatinine binds LOINC 2160-0 and 14682-9 with a tested conversion","Out-of-set codes become unresolved","Registry versioned and pinned per run"], deps=["CDP-301"], gaps=["G-09"])
st("CDP-303","CDP-3","E1",3,"I3","Patient and encounter identity binding","data engineer",
   "exact identifier binding between the run and returned BigQuery rows","evidence can't attach to the wrong patient",
   ["Exact match only; mismatched rows rejected and logged","Tests for merged and split synthetic patients"], gaps=["G-01"])
st("CDP-304","CDP-3","E1",8,"I4","P adapter (BigQuery)","evidence engineer",
   "a read-only typed tool that queries P with parameters and returns provenance-complete candidates","structured values reach the validator without an LLM",
   ["Parameterized queries only; partition filter required; maximum-bytes-billed cap","Provenance: source row ID, row hash, load time, BigQuery job ID, retrieved_at",
    "Quota/timeout errors become source-unavailable states","Runs against the dev dataset; real views arrive in Phase 2 (CDP-1204)"],
   deps=["CDP-302","CDP-303","CDP-1208"])
st("CDP-305","CDP-3","E1",3,"I5","C adapter (BigQuery)","evidence engineer",
   "C's clinical data through the same adapter framework, with distinct pending, negative and not-performed states","a pending culture is never read as negative",
   ["Preliminary/final/amended states handled; amendment yields a new candidate version","Each state traced to the executor by a fixture"],
   deps=["CDP-304"])
st("CDP-306","CDP-3","E1",3,"I6","Timezone normalization","evidence engineer",
   "every timestamp resolved to UTC with the source's configured zone","freshness math is right across DST",
   ["Naïve timestamps without a configured zone become unresolved","DST boundary tests at the freshness limit"], deps=["CDP-304"], gaps=["G-20"])
st("CDP-307","CDP-3","E1",3,"I7","Bounded document retrieval tool","evidence engineer",
   "documents returned with hash, span offsets and size limits","the extraction skill cites exact locations",
   ["Oversized documents return a truncation status","Header identifiers checked against the run's patient"], deps=["CDP-303","CDP-1209"])
st("CDP-308","CDP-3","E1",5,"P2","Source drift monitors","on-call engineer",
   "daily code, unit and missing-rate profiles per concept","upstream changes are caught before they affect recommendations",
   ["Alerts on unmapped codes and distribution shifts"], deps=["CDP-304","CDP-305","CDP-1204"], gaps=["G-10"])
st("CDP-309","CDP-3","E1",5,"P2","Real-data integration in the perimeter","evidence engineer",
   "adapters run against the approved real views","fixture assumptions are validated before shadow mode",
   ["Every fixture-vs-real discrepancy resolved"], deps=["CDP-1204","CDP-304","CDP-305"])

# ---------------- CDP-4
st("CDP-401","CDP-4","E2",5,"I1","Snapshot schema v1","evidence engineer",
   "a versioned schema separating candidates from accepted values, with missing, pending, negative, not performed, unresolved and conflict states","absence of evidence is never encoded as a clinical value",
   ["JSON Schema and Pydantic from one source","Includes valid_as_of and expires_at"], gaps=["G-06"])
st("CDP-402","CDP-4","E2",8,"I3","Deterministic evidence validator","evidence engineer",
   "type, unit, provenance and freshness checks against a recorded evaluated_at","only usable evidence reaches predicates",
   ["Inclusive freshness limit; future-dated evidence rejected","UCUM conversion via registry only","Every rejection has a reason code"], deps=["CDP-302","CDP-401"])
st("CDP-403","CDP-4","E1",3,"I6","Eager snapshot assembly","evidence engineer",
   "every evidence key the pinned tree references resolved once at run start","all nodes on a path see the same evidence",
   ["One snapshot per run version","A failing source yields explicit states, not an aborted run"], deps=["CDP-304","CDP-402"], gaps=["G-06"])
st("CDP-404","CDP-4","E1",3,"I7","Conflict detection routed to review","clinical reviewer",
   "conflicting candidates sent to review with no automatic resolution","the system never silently picks between clinical values",
   ["Specimen, encounter and status matched before comparison","No averaging; no global source precedence"], deps=["CDP-402"], gaps=["G-18"])
st("CDP-405","CDP-4","E2",3,"I7","Revalidation before approval","clinical reviewer",
   "path evidence re-queried and row hashes compared before an approval commits","I never approve a recommendation built on superseded evidence",
   ["Changed hash → new snapshot, recompute, approval returns 409 with refresh","Revalidation at review creation deferred to Phase 2"], deps=["CDP-403","CDP-801"], gaps=["G-06"])

# ---------------- CDP-5
st("CDP-501","CDP-5","E2",3,"I2","ADK spike with tracing","evidence engineer",
   "the pinned ADK version proven with ephemeral sessions, operation-ID idempotency, and OpenInference traces in AX","SDK assumptions are verified before we build on them",
   ["Findings written up for sessions, retries, and tracing","Spike skill (v0) produces a trace in the AX dev space"], deps=["CDP-1304"], gaps=["G-13"])
st("CDP-502","CDP-5","E2",8,"I5","Extraction skill v1","clinical reviewer",
   "a versioned skill with instructions, I/O schemas, tool policy, validators and abstention rules","unstructured evidence becomes cited candidates without model authority",
   ["Every candidate cites a span in the hashed document or fails validation","Token, runtime and retry budgets; exhaustion yields unresolved",
    "Merged only with an AX experiment against the main baseline"], deps=["CDP-501","CDP-1305","CDP-1208"])
st("CDP-503","CDP-5","E2",3,"I6","Adversarial extraction cases","security reviewer",
   "wrong-patient documents, embedded instructions, fabricated citations and malformed outputs in the eval set","attack and failure modes are regression-tested",
   ["All cases fail validation or remain unresolved","Run in the agent-eval lane"], deps=["CDP-502"])
st("CDP-505","CDP-5","E2",5,"I8","Skill iteration to Day-70 thresholds","product owner",
   "time-boxed error-analysis cycles on the extraction skill","quality improves by evidence, not by guesswork",
   ["Each change is one hypothesis, one experiment, one PR","Failure classes reported weekly on the scorecard","Stops at threshold or end of I8, whichever comes first"],
   deps=["CDP-502","CDP-307","CDP-503","CDP-1308"])
st("CDP-504","CDP-5","E2",2,"P2","Model registry and retirement alerts","evidence engineer",
   "pinned model IDs and retirement dates with 90-day alerts","forced migrations trigger re-validation",
   ["Served model ID recorded on each extraction"], deps=["CDP-502"], gaps=["G-21"])

# ---------------- CDP-6
st("CDP-601","CDP-6","E3",8,"I1","Tree schema and graph compiler","logic engineer",
   "YAML trees validated and compiled into a checked graph","invalid trees fail at publish time",
   ["Rejects unreachable nodes, unknown operators, missing targets, ambiguity, and cycles other than review resume","Safe loader only"])
st("CDP-602","CDP-6","E3",5,"I2","Typed operator library","logic engineer",
   "comparison, membership and Boolean operators with versioned boundary semantics","thresholds behave exactly as approved",
   ["Type mismatch is an error","Below/at/above boundary tests"], deps=["CDP-601"])
st("CDP-603","CDP-6","E3",5,"I3","Pure node evaluation","auditor",
   "evaluate_node as a pure function of tree, node, snapshot and evaluated_at","identical inputs always give the identical next node",
   ["Property-based determinism tests","Import linter forbids I/O and LLM packages in the executor"], deps=["CDP-602"])
st("CDP-604","CDP-6","E3",3,"I3","Immutable bundles with status","clinical lead",
   "trees published as hashed bundles with owner, approver ≠ author, guideline refs and status","every run pins exactly what it executed",
   ["Publish fails without approver or per-node guideline reference","Status ACTIVE/SUSPENDED/RETIRED is the only mutable field"], deps=["CDP-601"], gaps=["G-15"])
st("CDP-605","CDP-6","E3",5,"I4","Tree A with signed expected paths","clinical lead",
   "Tree A in YAML with clinician-approved expected paths as CI fixtures","every approved path is a regression test",
   ["Every terminal node and gate covered","Clinical lead signs the fixture set by day 28"], deps=["CDP-301","CDP-604"])
st("CDP-607","CDP-6","E3",5,"I5","Kill switch and recall query","clinical safety officer",
   "to suspend a bundle and halt in-flight runs at their next step","a defective tree stops within minutes",
   ["SUSPENDED → HALTED_SAFETY with banner","Recall query by bundle and date range","Suspend-to-halt under 5 minutes in tests"], deps=["CDP-604","CDP-701"], gaps=["G-03"])
st("CDP-606","CDP-6","E3",3,"P2","Replay tool","auditor",
   "to re-execute a run from stored snapshots and original evaluated_at","recorded paths are provably reproducible",
   ["Replay equals audit exactly"], deps=["CDP-902","CDP-603"], gaps=["G-21"])
st("CDP-608","CDP-6","E3",3,"P2","Cross-tree regression gate","lead engineer",
   "path suites for all onboarded trees gating merges","Tree B can't silently change Tree A",
   ["Any path diff blocks merge"], deps=["CDP-605"])

# ---------------- CDP-7
st("CDP-701","CDP-7","E4",5,"I4","Run state machine","platform engineer",
   "an explicit transition table including EXPIRED and HALTED_SAFETY","no run reaches an undefined state",
   ["Illegal transitions tested exhaustively","One active run per patient, encounter and tree"], deps=["CDP-204"], gaps=["G-16"])
st("CDP-702","CDP-7","E4",3,"I4","Run API with idempotency","clinical reviewer",
   "POST /v1/runs and GET /v1/runs/{id} with idempotency keys","retries never create duplicate runs",
   ["Changed payload under same key → 409; 24 h key TTL","Provisional vs reviewed output labelled"], deps=["CDP-701"], gaps=["G-16"])
st("CDP-703","CDP-7","E4",5,"I5","Postgres job queue with revision-checked commits","platform engineer",
   "steps claimed with FOR UPDATE SKIP LOCKED and committed with the transition, audit event, and next job in one transaction","work is never lost or double-committed",
   ["UPDATE … WHERE revision = expected; zero rows is a safe no-op","Abandoned claims reclaimed after timeout"], deps=["CDP-204","CDP-701","CDP-902"], gaps=["G-13","G-17"])
st("CDP-704","CDP-7","E4",3,"I6","Worker loop with bounded retries","on-call engineer",
   "one bounded step per claim with exponential backoff","failures become visible states",
   ["Exhausted retries → FAILED with reason","Killing the worker at any point leaves a consistent run"], deps=["CDP-703"])
st("CDP-705","CDP-7","E4",3,"I7","Fail-closed unavailable state","clinical reviewer",
   "a clear “No recommendation — follow standard pathway” state when anything is unavailable","a partial path is never mistaken for a recommendation",
   ["Partial paths never rendered as recommendations","Downtime procedure drafted with clinical lead"], deps=["CDP-704"], gaps=["G-05"])

# ---------------- CDP-8
st("CDP-805","CDP-8","E3",3,"I4","Deterministic explanation templates","clinical reviewer",
   "plain-language summaries from approved templates per output code","explanations can't contradict the recorded path",
   ["Fields bound only to recorded evidence and path","Template text approved by clinical lead"], deps=["CDP-605"], gaps=["G-18"])
st("CDP-801","CDP-8","E4",5,"I6","Review action API","clinical reviewer",
   "to approve, reject or cancel against an exact run revision","my action applies to what I actually saw",
   ["Expected revision required; stale → 409","Reviewer identity from token only; duplicates rejected","Evidence problems end the run as “insufficient evidence”"],
   deps=["CDP-701","CDP-901"])
st("CDP-803","CDP-8","E3",8,"I6","Review screen","clinical reviewer",
   "evidence with provenance, the path with guideline references, and review reasons on one screen","I can verify the basis of the recommendation myself",
   ["Each value links to its source row and observed time with zone label","Missing, pending and conflicting evidence visually distinct","Output labelled PROVISIONAL until approved"],
   deps=["CDP-801","CDP-605"], gaps=["G-01"])
st("CDP-806","CDP-8","E3",2,"I7","Approval gating on flagged evidence","clinical safety officer",
   "approve disabled until each flagged evidence item has been opened","review can't be clicked through blind",
   ["Gate enforced server-side too"], deps=["CDP-803"], gaps=["G-12"])
st("CDP-808","CDP-8","E3",3,"I7","Review screen iteration from demo feedback","clinical reviewer",
   "a budgeted iteration on the review screen after the first clinician demos","the UI reflects how clinicians actually review",
   ["Top feedback items from I6 demo fixed or logged"], deps=["CDP-803"], gaps=["G-12"])
st("CDP-804","CDP-8","E3",5,"P2","Evidence resolution by clinician","clinical reviewer",
   "to supply a sourced value with rationale","missing facts can be resolved without approving output",
   ["New snapshot version and recompute"], deps=["CDP-803","CDP-405"])
st("CDP-802","CDP-8","E4",2,"P2","Review expiry","clinical safety officer",
   "review tasks that expire without implied approval","stale recommendations don't linger",
   ["Expired run requires a new run"], deps=["CDP-801"], gaps=["G-16"])
st("CDP-807","CDP-8","E3",2,"P2","Automation-bias telemetry","clinical safety officer",
   "dwell-time and approval-rate monitoring with alerts","rubber-stamping is detected",
   ["Thresholds agreed with clinical lead"], deps=["CDP-806"], gaps=["G-12"])

st("CDP-809","CDP-8","E3",3,"I6","Worklist and start-run dialog (S1, S2)","clinical reviewer",
   "a worklist of my patients' Tree A runs with plain-language statuses and a one-step start","I can find cases that need me and start a run without duplicates",
   ["Lists only runs within the user's care assignment","Statuses: needs review, gathering evidence, no recommendation, approved, rejected, halted","Starting an existing active run opens it instead"],
   deps=["CDP-702","CDP-901"])
st("CDP-810","CDP-8","E3",2,"I7","Outcome and audit timeline (S5)","auditor",
   "a read-only timeline of every event on a run with chain hashes","anyone reviewing a case can see exactly what happened and verify it",
   ["Shows snapshot versions, gate results, evidence opened, revalidation and decision","Each event shows its hash and previous hash"],
   deps=["CDP-902","CDP-803"], gaps=["G-04"])
st("CDP-811","CDP-8","E4",2,"I8","Trees and skills admin screen (S6)","clinical safety officer",
   "a screen to see bundle status, suspend with a reason, and open the recall list","I can use the kill switch without asking an engineer",
   ["Only safety_officer and clinical_admin roles can suspend","Suspension requires a reason and is audited","Recall list shows affected runs and approved recommendations"],
   deps=["CDP-607","CDP-901"], gaps=["G-03"])

# ---------------- CDP-9
st("CDP-902","CDP-9","E1",5,"I5","Append-only hash-chained audit","auditor",
   "audit events that can't be updated or deleted and are hash-chained","tampering is detectable",
   ["sha256(prev_hash ∥ payload) per event","Test proves no UPDATE/DELETE grant","Written in the same transaction as the transition"], deps=["CDP-204"], gaps=["G-04"])
st("CDP-901","CDP-9","E3",3,"I5","Sign-in and roles (staging)","clinical reviewer",
   "sign-in via IAP/OIDC with roles and a patient check against a synthetic care-assignment table","access control is real from the first clinician demo",
   ["Roles: clinical_reviewer, clinical_admin, safety_officer, engineer_readonly","Unauthorized patient access denied by test","Real care-relationship source and break-glass in Phase 2"],
   deps=["CDP-203","CDP-1209"], gaps=["G-11"])
st("CDP-903","CDP-9","E1",3,"P2","WORM audit export","auditor",
   "hourly export to a Bucket Lock bucket plus chain verification","audit survives a compromised database",
   ["Verification failure pages on-call"], deps=["CDP-902"], gaps=["G-04"])
st("CDP-904","CDP-9","E3",3,"P2","PHI access log","privacy officer",
   "every view of patient data logged","we can answer who looked at which patient",
   ["Report by patient and by user"], deps=["CDP-901"], gaps=["G-04","G-11"])
st("CDP-905","CDP-9","E3",3,"P2","Care-relationship source and break-glass","clinical reviewer",
   "access checks against the real care-team source with audited break-glass","access matches real clinical responsibility",
   ["Break-glass alerts the safety officer"], deps=["CDP-901","CDP-1209"], gaps=["G-11"])

# ---------------- CDP-10
st("CDP-1001","CDP-10","E2",3,"I6","PHI-leak test on telemetry","privacy officer",
   "an attribute allowlist processor and a CI test that injects PHI-shaped values","nothing that would be PHI can reach Arize once real data arrives",
   ["Unknown attributes and exception messages dropped for staging/prod spaces","CI fails if injected values reach the exporter"], deps=["CDP-1304"], gaps=["G-02"])
st("CDP-1004","CDP-10","E4",3,"P2","Operational alerts and runbooks","on-call engineer",
   "alerts for stuck runs, retries, audit write failures, rejection spikes","failures reach a person",
   ["Each alert has a runbook"], deps=["CDP-704"])

# ---------------- CDP-11
st("CDP-1107","CDP-11","E1",3,"I8","Scripted UAT case pack","clinical lead",
   "25 scripted synthetic cases covering normal, pending, stale, conflicting and adversarial situations","UAT tests the hard cases, not just the happy path",
   ["Each case has expected path, expected screen state, and hazard link","Clinical lead approved"], deps=["CDP-605"])
st("CDP-1101","CDP-11","E4",3,"I8","Fault-injection suite","lead engineer",
   "automated crash-before/after-commit, duplicate claim, duplicate action and concurrent worker tests","durability claims are proven",
   ["Zero duplicated committed transitions over 500 randomized runs"], deps=["CDP-703","CDP-801"], gaps=["G-05","G-17"])
st("CDP-1401","CDP-11","LEAD",3,"T","System verification against the hazard log","clinical safety officer",
   "every MVP hazard control's test executed with evidence attached","the Day-70 decision rests on traceable evidence",
   ["All controls verified or residual risk recorded","Fault-injection suite green"], deps=["CDP-102","CDP-1101"], gaps=["G-01"])
st("CDP-109","CDP-11","E3",3,"T","Clinician UAT","clinical reviewer",
   "at least three clinicians to work the 25 scripted cases in staging","the primary safety control works for real users",
   ["No open critical usability issues","Findings logged as hazards or Phase 2 stories"], deps=["CDP-803","CDP-1107"], gaps=["G-12"])
st("CDP-1402","CDP-11","E2",3,"T","Held-out evaluation report","product owner",
   "the frozen held-out run compared with pre-registered thresholds","extraction quality is known, not assumed",
   ["Run by the restricted release job","Per-slice results and failure classes"], deps=["CDP-1403","CDP-505","CDP-107"], gaps=["G-08"])
st("CDP-1405","CDP-11","E1",3,"T","Data traceability check","auditor",
   "every evidence value on UAT runs traced from BigQuery row to snapshot to screen","provenance is proven end to end",
   ["Row hash, job ID and observed time match for every sampled value"], deps=["CDP-1107","CDP-403"])
st("CDP-1103","CDP-11","E4",2,"T","Restore test","on-call engineer",
   "a timed PITR restore of staging","recovery works before real data exists",
   ["Restore time recorded; runbook updated"], deps=["CDP-204"], gaps=["G-05"])
st("CDP-1106","CDP-11","LEAD",2,"T","Day-70 decision","product owner",
   "a documented decision: start Phase 2, fix-and-retest, or stop","the next commitment is based on evidence",
   ["Exit criteria scored with evidence links","Phase 2 re-estimated with access status"], deps=["CDP-1401","CDP-109","CDP-1402","CDP-1103","CDP-1405"])
st("CDP-1102","CDP-11","LEAD",3,"P2","Security review and pen test","security reviewer",
   "an independent review before real data","vulnerabilities are closed before shadow mode",
   ["No open critical/high findings"], deps=["CDP-901","CDP-1001","CDP-104"], gaps=["G-14"])
st("CDP-1105","CDP-11","LEAD",3,"P2","Shadow evaluation protocol","clinical lead",
   "sampling, concordance measure and discordance review defined","pilot entry is measured",
   ["Signed before shadow starts"], gaps=["G-23"])
st("CDP-1104","CDP-11","E4",3,"P2","Shadow mode in production","clinical safety officer",
   "real-patient runs with outputs hidden from clinicians","we measure without influencing care",
   ["Feature flag guarantees no clinician-facing output"], deps=["CDP-1102","CDP-1105","CDP-309","CDP-1210","CDP-209"], gaps=["G-23"])
st("CDP-1109","CDP-11","LEAD",2,"P2","Go/no-go for supervised pilot","product owner",
   "a decision against shadow results and dual-annotated evals","pilot entry is defensible",
   ["Clinical, safety and security sign-offs"], deps=["CDP-1104","CDP-1003"])
st("CDP-1003","CDP-11","E2",5,"P2","Dual-annotated real-data eval set","clinical safety officer",
   "a de-identified eval set labeled by two clinicians","real-world extraction quality is measured",
   ["κ reported; stays inside the perimeter"], deps=["CDP-106","CDP-107","CDP-1305"], gaps=["G-07","G-08"])

# ---------------- CDP-12
st("CDP-1201","CDP-12","LEAD",3,"I1","Access request pack for BigQuery P and C","lead engineer",
   "one pack naming data owner, cloud platform, privacy and InfoSec approvers with exact grants","approvals run in parallel from day one",
   ["Purpose, tables/columns, row scope, grants, data flow, retention","Submitted in week 1; status reviewed every Tuesday"])
st("CDP-1202","CDP-12","E1",3,"I2","Minimum-necessary data specification","privacy officer",
   "exact tables, columns and row filters Tree A needs, each tied to an evidence key","requests are approvable and least-privilege",
   ["No column without an evidence key","Metadata-only access requested first"], deps=["CDP-301"], gaps=["G-11"])
st("CDP-1209","CDP-12","LEAD",2,"I2","Identify document and care-team sources","lead engineer",
   "the systems holding documents and care-team assignments identified with owners","hidden integrations are scoped early",
   ["If no document source exists, re-scope CDP-5 at Day 30"])
st("CDP-1208","CDP-12","E1",3,"I3","Dev dataset and fixtures on real schemas","engineer",
   "a BigQuery dev dataset mirroring P and C schemas with synthetic rows, including amended, preliminary, missing-unit and local-code cases","humans and Devin build against realistic shapes without PHI",
   ["Schemas from INFORMATION_SCHEMA; rows synthetic","Refreshed when source schemas change"], deps=["CDP-1202"])
st("CDP-1203","CDP-12","E1",3,"I3","Freshness and history gate for P and C","clinical lead",
   "measured load lag from specimen time to BigQuery, culture pending→final update lag, and whether corrections overwrite rows","we know by Day 30 whether BigQuery can meet Tree A's freshness rules",
   ["p50/p95 lag from load-job history and sampled metadata","If p95 lag exceeds a freshness limit, decision at Day 30"], deps=["CDP-1202"], gaps=["G-06"])
st("CDP-1204","CDP-12","E4",5,"P2","Authorized views on real P and C","platform engineer",
   "authorized views over real tables readable only by the worker identity","real data is reachable with least privilege",
   ["Base-table query denied by test","Stretch: pulled into I6 if approved by Day 30"], deps=["CDP-1201","CDP-1202","CDP-201"], gaps=["G-11","G-14"])
st("CDP-1210","CDP-12","E1",3,"P2","Production data validation","clinical safety officer",
   "prod query results reconciled with source application screens for a sample","shadow mode runs on verified data",
   ["Discrepancies logged as hazards"], deps=["CDP-309"], gaps=["G-10"])

# ---------------- CDP-13
st("CDP-1301","CDP-13","E4",5,"I1","Devin-ready development environment","engineer",
   "make dev, make test and make eval-smoke working from a clean machine, with docker compose Postgres, fixture adapters, and recorded model responses","Devin and humans run the same checks locally",
   ["Fresh clone to green tests under 15 minutes","Devin Knowledge/Playbooks: implement story, add eval case, fix failing eval","Architecture rules in the repo instructions: no LLM in executor, no eval(), never edit expected paths"],
   gaps=["G-22"])
st("CDP-1302","CDP-13","LEAD",3,"I1","Guardrails for AI-written code","lead engineer",
   "enforced rules for Devin: dev-only credentials, no merge rights, protected test oracles, PR size limit, labels and Jira links","speed from Devin doesn't erode safety",
   ["CODEOWNERS: clinical lead on trees/expected paths/golden sets; two humans on executor/, validator/, authz/",
    "Devin credentials reach only the dev project; no access to holdout, staging or prod","PRs over 400 changed lines (excluding generated) fail a check; ai-authored label and Devin session link required",
    "Definition of Done in PR template: tests, hazard ID, AX link if skill changed"], gaps=["G-22"])
st("CDP-1304","CDP-13","E2",3,"I2","Arize AX spaces and ADK tracing","evidence engineer",
   "AX spaces for dev, staging and a restricted holdout, with OpenInference ADK tracing and custom spans","every agent run is inspectable from day 8",
   ["Spans carry git_sha, bundle_hash, skill_version, model_id, run hash","Devin API key scoped to cdp-dev only","Prod space created in Phase 2 with structural spans only"])
st("CDP-1305","CDP-13","E2",6,"I4","Code evaluators and agent-eval PR lane","product owner",
   "field, unit, timestamp, citation-validity, abstention and false-acceptance evaluators running as an AX experiment on every skill/prompt/model PR","agent changes are measured against main before merging",
   ["Golden set v1 (≥ 40 clinician-reviewed synthetic cases) in AX","Gate: zero false acceptances, 100% citation validity, accuracy ≥ baseline − 2 points","Experiment link and delta table posted to the PR"],
   deps=["CDP-1304","CDP-401","CDP-202"], gaps=["G-08"])
st("CDP-1308","CDP-13","E2",2,"I7","Failure-to-regression loop","clinical lead",
   "a one-command path from a failing trace to a reviewed regression case","every failure makes the eval set stronger",
   ["Case added by PR with clinical lead approval","Failure class tagged: source, extraction, policy, tree, workflow"], deps=["CDP-1305","CDP-502"])
st("CDP-1403","CDP-13","E2",3,"I8","Frozen held-out set and release eval job","clinical safety officer",
   "a frozen, hashed held-out set only the human-triggered release job can read","the Day-70 eval can't have been tuned against",
   ["Patient-disjoint from golden set; hash recorded","Devin and PR lanes have no read access"], deps=["CDP-1305"], gaps=["G-08"])

# ---------------------------------------------------------------- validate
by_key = {s["key"]: s for s in S}
assert len(by_key) == len(S)
errs = []
for s in S:
    for d in s["deps"]:
        if d not in by_key: errs.append(f"{s['key']} unknown dep {d}")
        elif ORDER.index(by_key[d]["sprint"]) > ORDER.index(s["sprint"]):
            errs.append(f"{s['key']} ({s['sprint']}) depends on later {d} ({by_key[d]['sprint']})")
fids = {f[0] for f in FINDINGS}
for s in S:
    for g in s["gaps"]:
        if g not in fids: errs.append(f"{s['key']} unknown gap {g}")
uncovered = sorted(fids - {g for s in S for g in s["gaps"]} - {"G-19"})
matrix = defaultdict(lambda: defaultdict(int))
for s in S: matrix[s["owner"]][s["sprint"]] += s["pts"]
print("errors:", errs); print("uncovered:", uncovered)
for o in OWNERS: print(o, [matrix[o][i] for i in ORDER], "build", sum(matrix[o][i] for i in ITERS))
build_pts = sum(s["pts"] for s in S if s["sprint"] in ITERS)
t_pts = sum(s["pts"] for s in S if s["sprint"] == "T")
p2 = [s for s in S if s["sprint"] == "P2"]; p2_pts = sum(s["pts"] for s in p2)
mvp_n = sum(1 for s in S if s["sprint"] in ITERS or s["sprint"] == "T")
cap_total = sum(CAP["E"][i] for i in ITERS) * 4 + sum(CAP["LEAD"][i] for i in ITERS)
print("build", build_pts, "T", t_pts, "P2", len(p2), p2_pts, "cap", cap_total)
if errs or uncovered: sys.exit(1)

# ---------------------------------------------------------------- CSV
sprint_name = {i: f"CDP {i} ({d})" for i, d, *_ in ITER_INFO if i in ITERS}
sprint_name["T"] = "CDP Test window (Days 61–70)"; sprint_name["P2"] = ""
with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Issue ID","Parent ID","Issue Type","Summary","Description","Labels","Story Points","Sprint","Assignee Role"])
    for k, name, owner, goal in EPICS:
        w.writerow([k, "", "Epic", f"{k} {name}", goal, "cdp", "", "", OWNERS[owner][0]])
    for s in S:
        phase = "phase-2" if s["sprint"] == "P2" else ("test-window" if s["sprint"] == "T" else "mvp-70")
        desc = (f"As a {s['as_']}, I want {s['want']}, so that {s['so']}.\n\nAcceptance criteria:\n" + "\n".join(f"- {a}" for a in s["ac"]) +
                (f"\n\nDepends on: {', '.join(s['deps'])}" if s["deps"] else "") + (f"\nAddresses review findings: {', '.join(s['gaps'])}" if s["gaps"] else ""))
        labels = " ".join(["cdp", phase, s["owner"].lower()] + [g.lower() for g in s["gaps"]])
        w.writerow([s["key"], s["epic"], "Story", f"{s['key']} {s['title']}", desc, labels, s["pts"], sprint_name[s["sprint"]], OWNERS[s["owner"]][0]])

# ---------------------------------------------------------------- HTML pieces
sev_label = {"critical":"Critical","high":"High","medium":"Medium"}
counts = {k: sum(1 for f in FINDINGS if f[1]==k) for k in sev_label}

def sprint_badge(sp):
    if sp == "P2": return '<span class="phase ph-p2">Phase 2</span>'
    if sp == "T": return '<span class="phase ph-t">Test</span>'
    return f'<span class="phase ph-mvp">{sp}</span>'

def findings_html():
    out = []
    for sev in ["critical","high","medium"]:
        items = [f for f in FINDINGS if f[1]==sev]
        out.append(f'<h3 class="sevhead"><span class="sev sev-{sev}">{sev_label[sev]}</span> {len(items)} findings</h3><div class="findings">')
        for fid,_,area,title,gap,std,fix in items:
            ks = [s for s in S if fid in s["gaps"]]
            line = " ".join(f'<a class="skey" href="#{s["key"]}">{s["key"]}</a>' + ('<sup class="p2">P2</sup>' if s["sprint"]=="P2" else "") for s in ks) or '<span class="muted">Fixed in this document (architecture diagram)</span>'
            out.append(f'''<article class="finding" id="{fid}"><div class="fmeta"><span class="fid">{fid}</span><span class="sev sev-{sev}">{sev_label[sev]}</span><span class="area">{E(area)}</span></div>
<div class="fbody"><h4>{E(title)}</h4><p><span class="lbl">Gap</span>{gap}</p><p class="std"><span class="lbl">Standard</span>{E(std)}</p><p class="fix"><span class="lbl">Fix</span>{fix}</p><p class="tracked"><span class="lbl">Tracked in</span>{line}</p></div></article>''')
        out.append('</div>')
    return "\n".join(out)

def capacity_html():
    cols = ITERS + ["T","P2"]
    head = "".join(f'<th scope="col" class="num">{c}</th>' for c in cols)
    rows = []
    for o,(name,_) in OWNERS.items():
        capk = "LEAD" if o=="LEAD" else "E"
        cells = []
        for c in cols:
            v = matrix[o][c]
            cls = ""
            if c in ITERS and v > CAP[capk][c] * 1.25: cls = "caphi"
            if v == 0: cls = "cap0"
            if c == "P2": cls += " p2col"
            cells.append(f'<td class="num {cls}">{v or "–"}</td>')
        b = sum(matrix[o][c] for c in ITERS)
        capo = sum(CAP[capk][c] for c in ITERS)
        rows.append(f'<tr><th scope="row">{E(name)}</th>{"".join(cells)}<td class="num tot">{b}<small> / {capo:g}</small></td></tr>')
    tot = "".join(f'<td class="num{" p2col" if c=="P2" else ""}">{sum(matrix[o][c] for o in OWNERS)}</td>' for c in cols)
    return f'''<div class="scroll"><table class="cap"><thead><tr><th scope="col">Owner</th>{head}<th scope="col" class="num">Build / capacity</th></tr></thead>
<tbody>{"".join(rows)}</tbody><tfoot><tr><th scope="row">Total</th>{tot}<td class="num tot">{build_pts}<small> / {cap_total:g}</small></td></tr></tfoot></table></div>'''

def epics_html():
    out = []
    for k,name,owner,goal in EPICS:
        items = sorted([s for s in S if s["epic"]==k], key=lambda s: ORDER.index(s["sprint"]))
        mvp_pts = sum(s["pts"] for s in items if s["sprint"] != "P2")
        rows = []
        for s in items:
            ph = "p2" if s["sprint"]=="P2" else ("t" if s["sprint"]=="T" else "mvp")
            ac = "".join(f"<li>{E(a)}</li>" for a in s["ac"])
            deps = " ".join(f'<a class="skey" href="#{d}">{d}</a>' for d in s["deps"]) or '<span class="muted">—</span>'
            gaps = " ".join(f'<a class="gid" href="#{g}">{g}</a>' for g in s["gaps"])
            rows.append(f'''<tr id="{s["key"]}" data-owner="{s["owner"]}" data-phase="{ph}"{' class="rowp2"' if ph=="p2" else ''}>
<td class="k"><span class="skey">{s["key"]}</span></td>
<td class="story"><strong>{E(s["title"])}</strong><p class="as">As a {E(s["as_"])}, I want {E(s["want"])}, so that {E(s["so"])}.</p><ul class="ac">{ac}</ul>
<p class="links"><span class="lbl">Depends</span>{deps}{('<span class="lbl gl">Fixes</span>'+gaps) if gaps else ''}</p></td>
<td><span class="owner o-{s["owner"].lower()}">{s["owner"]}</span></td><td class="num">{s["pts"]}</td><td class="num">{sprint_badge(s["sprint"])}</td></tr>''')
        out.append(f'''<section class="epic" data-epic="{k}"><header class="epichead"><div><span class="ekey">{k}</span><h3>{E(name)}</h3><p>{E(goal)}</p></div>
<dl class="estats"><div><dt>Epic owner</dt><dd>{E(OWNERS[owner][0])}</dd></div><div><dt>Stories</dt><dd>{len(items)}</dd></div><div><dt>70-day pts</dt><dd>{mvp_pts}</dd></div></dl></header>
<div class="scroll"><table class="stories"><thead><tr><th scope="col">Key</th><th scope="col">Story and acceptance criteria</th><th scope="col">Owner</th><th scope="col" class="num">Pts</th><th scope="col" class="num">When</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div></section>''')
    return "\n".join(out)

team_rows = "".join(f'<tr><td><span class="owner o-{o.lower()}">{o}</span> {E(n)}</td><td>{E(d)}</td><td class="num">{sum(matrix[o][c] for c in ITERS)}</td><td class="num">{matrix[o]["T"] or "–"}</td><td class="num">{matrix[o]["P2"] or "–"}</td></tr>' for o,(n,d) in OWNERS.items())

def iter_rows():
    out = []
    for i, days, name, work, demo in ITER_INFO:
        if i == "CP30":
            out.append(f'<tr class="cprow"><td class="num"><span class="phase ph-cp">◆</span></td><td class="nowrap">{days}</td><td><strong>{E(name)}</strong></td><td>{E(work)}</td><td><a href="#cp30">Day 30 criteria</a></td></tr>')
            continue
        badge = sprint_badge(i)
        out.append(f'<tr><td class="num">{badge}</td><td class="nowrap">{days}</td><td><strong>{E(name)}</strong></td><td>{E(work)}</td><td>{E(demo)}</td></tr>')
    return "".join(out)

tmpl = open(TEMPLATE, encoding="utf-8").read()
subs = {"FINDINGS": findings_html(), "CAPACITY": capacity_html(), "EPICS": epics_html(), "TEAM_ROWS": team_rows, "ITER_ROWS": iter_rows(),
        "N_FIND": str(len(FINDINGS)), "N_CRIT": str(counts["critical"]), "N_HIGH": str(counts["high"]), "N_MED": str(counts["medium"]),
        "N_MVP_STORIES": str(mvp_n), "N_BUILD_POINTS": str(build_pts), "N_T_POINTS": str(t_pts), "N_P2_STORIES": str(len(p2)), "N_P2_POINTS": str(p2_pts),
        "CAP_TOTAL": f"{cap_total:g}", "BUFFER": f"{round((cap_total-build_pts)/cap_total*100)}"}
for k, v in subs.items(): tmpl = tmpl.replace("{{"+k+"}}", v)
assert "{{" not in tmpl, tmpl[tmpl.index("{{"):tmpl.index("{{")+40]
open(OUT_HTML, "w", encoding="utf-8").write(tmpl)
print("wrote", OUT_HTML, OUT_CSV)
