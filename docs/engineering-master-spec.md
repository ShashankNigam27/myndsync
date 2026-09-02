# PROJECT ENGINEERING MASTER SPECIFICATION
## Suraksha Setu — AI-Based Dynamic Mental Health Monitoring & Distress Prediction System for Victims/Witnesses under the SC/ST (Prevention of Atrocities) Act, 1989

Labels used throughout: **PS FACT** (from the SIH problem statement) · **DESIGN DECISION** (our chosen approach) · **ASSUMPTION** (not specified by PS, assumed for completeness) · **FUTURE POSSIBILITY** (later extension, not built now).

This document is the engineering source of truth for this project. It assumes the problem statement, project narrative, and PPT already established in this conversation and does not repeat them except where an engineering decision depends on them.

---

# 1. PROJECT DEFINITION

| Field | Value |
|---|---|
| Project name | **Suraksha Setu** `[DESIGN DECISION — finalized]` |
| One-line description | An AI-assisted, human-supervised platform that continuously monitors the psychological well-being of registered atrocity victims/witnesses and predicts distress escalation before crisis, routing explainable alerts to counsellors and authorities. |
| Detailed description | Suraksha Setu conducts periodic, multi-channel check-ins (chatbot, IVRS, SMS, app, web) with registered victims/witnesses, converts responses into a Dynamic Distress Score (DDS) using NLP/sentiment/emotion/voice-stress signals, tracks longitudinal trend, predicts escalation risk, and routes explainable alerts to counsellors and district/state/national authorities — who alone decide and act on interventions. |
| Vision | A justice system where no victim's psychological decline goes unnoticed between legal milestones. |
| Objectives | Continuous monitoring; early detection of escalating distress; faster, targeted intervention; longitudinal evidence for policymakers. |
| Target users | Victims/complainants, witnesses, counsellors, district/state/national officials, system administrators. |
| Beneficiaries | Victims/witnesses registered under the PoA Act receiving relief, compensation, rehabilitation, protection. `[PS FACT]` |
| Stakeholders | Ministry of Social Justice & Empowerment, State SC/ST Welfare Departments, DLSA, police, empanelled counsellors, NGOs. `[ASSUMPTION]` |
| Core use cases | Periodic distress check-in; risk escalation & alert; counsellor case review; intervention recommendation & tracking; multi-level dashboard monitoring. |
| Value proposition | Converts the silent gap between legal events into a monitored, response-ready period, without replacing human judgment. |
| Key differentiators | Proactive (not reactive) monitoring; multi-signal AI (not single metric); mandatory human-in-the-loop; explainability on every alert. |

---

# 2. COMPLETE SYSTEM SCOPE

**What the system does:**
- Enrolls consenting victims/witnesses and conducts scheduled multi-channel check-ins.
- Processes text/voice responses into distress signals (NLP, sentiment, emotion, voice-stress).
- Computes a Dynamic Distress Score with trend and anomaly detection.
- Predicts escalation risk and generates explainable, prioritized alerts.
- Provides role-based dashboards (Counsellor, District, State, National).
- Tracks human-decided interventions and follow-ups to closure.

**What the system does NOT do:**
- Does not diagnose mental illness or any clinical condition.
- Does not autonomously dispatch protection, medical, legal, or financial action.
- Does not access real government systems in the prototype (simulated only).
- Does not expose raw scores/clinical detail to the victim directly.

| Capability tier | Items |
|---|---|
| Core | Enrollment/consent, multi-channel check-ins, NLP/sentiment/emotion/voice-stress analysis, DDS + trend, escalation prediction, alerting, dashboards, explainability, RBAC/audit |
| Supporting | Adaptive scheduling, multilingual support, case-event integration (simulated), counsellor case-queue prioritization, follow-up tracking |
| Advanced | Anomaly detection, bias/fairness monitoring, SLA tracking |
| Future | Real government API integration, clinically validated instruments, expanded language/channel coverage `[FUTURE POSSIBILITY]` |

---

# 3. USER ROLES & PERMISSIONS

| Role | Can Access | Can Do | Cannot Access |
|---|---|---|---|
| Victim/Witness | Own history, status (non-clinical), resources | Respond to check-ins, request help, manage consent, choose channel/language | Other victims' data, raw DDS/risk band |
| Counsellor | Assigned case DDS trend + explanation, interaction summaries | Log intervention, escalate, close/reassess assigned cases | Unassigned cases, other counsellors' caseloads |
| District Official | District aggregate + identifiable high-risk/protection cases | Assign counsellor, trigger protection workflow | Full clinical interaction content, other districts' identifiable data |
| State Authority | De-identified state aggregate, district comparison | Resource allocation, audited drill-down request | Individual case data by default |
| National Authority | Fully de-identified national aggregate | Policy threshold configuration | Any individual-level data by default |
| Administrator | System logs, access records, config | Manage roles/permissions, monitor system health | Victim clinical content (no standing access) |

### Role-Permission Matrix (module-level)

| Module | Victim | Counsellor | District | State | National | Admin |
|---|---|---|---|---|---|---|
| Enrollment/Consent | Self only | View | View (jurisdiction) | View (aggregate) | View (aggregate) | No |
| Check-in/Interaction | Self only | Assigned cases | No (unless escalated) | No | No | No |
| DDS/Risk view | No (self-status only) | Assigned cases | Aggregate + high-risk | Aggregate | Aggregate | No |
| Alerts | No | Assigned | District-level | State-level | National-level | No |
| Intervention Mgmt | Request only | Full (assigned) | Coordinate | No | No | No |
| Dashboards | No | Own queue | District | State | National | System health only |
| User/Role Mgmt | No | No | No | No | No | Full |
| Audit Logs | No | No | No | No | No | Full |

---

# 4. END-TO-END SYSTEM WORKFLOW

| Stage | Actor | Input | Processing | Output | Next Stage |
|---|---|---|---|---|---|
| Enrollment | Victim/Witness, System | Case ID, contact, channel choice | Identity/case linkage | Monitoring profile created | Consent |
| Consent | Victim/Witness | Consent choice | Scope + timestamp recorded | Active/inactive consent record | Baseline |
| Baseline Assessment | Victim, AI Engine | First interaction | Signal extraction | Baseline DDS | Periodic Check-ins |
| Periodic Check-ins | Victim, Channel Service | Scheduled prompt response | Logging + metadata capture | Interaction record | AI Analysis |
| AI Analysis | AI/ML Engine | Text/voice/behavioural signals | NLP, sentiment, emotion, voice-stress | Structured signal set | DDS Update |
| DDS + Trend | Scoring Engine | Signal set + history | Score, trend, anomaly check | Updated DDS + trend | Risk Prediction |
| Risk Prediction | Prediction Engine | DDS history + context | Escalation modelling | Risk band + escalation probability | Explainability |
| Explainability | XAI Layer | Model internals | Factor attribution | Plain-language explanation | Alert (if threshold crossed) |
| Alert | Alert Service | Risk band + explanation | Routing rules | Alert to Counsellor/District | Human Review |
| Human Review | Counsellor | Alert + case detail | Manual assessment | Confirmed/adjusted risk | Intervention |
| Intervention | Counsellor/Official | Recommendation + decision | Human-selected action | Logged intervention | Follow-up |
| Follow-up | Counsellor | Intervention outcome | Outcome logging | Follow-up record | Reassessment |
| Reassessment | AI Engine + Counsellor | New check-ins | DDS recompute | Updated status | Check-ins (loop) or Closure |
| Case Closure | Counsellor, Victim | Resolution + consent | Status update | Closed case (reopenable) | — |

---

# 5. FUNCTIONAL REQUIREMENTS

Grouped by module. Priority: P0 = must-have core, P1 = important, P2 = advanced.

### Enrollment & Consent
- **FR-001** — Register victim/case. Actor: Victim/District Official. Precondition: valid case reference. Main flow: capture contact, language, channel, link to case ID. Output: victim profile. Dependencies: Case lookup (simulated). Priority: P0.
- **FR-002** — Capture/revoke consent. Actor: Victim. Precondition: profile exists. Main flow: present scope, record choice, allow revocation anytime. Output: consent record. Priority: P0.

### Interaction
- **FR-003** — Schedule periodic check-in. Actor: System (scheduler). Precondition: active consent. Main flow: determine cadence, dispatch via preferred channel. Output: scheduled interaction. Priority: P0.
- **FR-004** — Receive & log interaction response. Actor: Victim via Channel Service. Main flow: capture text/voice + metadata (latency, skip). Output: interaction record. Priority: P0.
- **FR-005** — Manual "talk to a human now" request. Actor: Victim. Main flow: immediate routing to counsellor queue, bypass scheduled cadence. Output: priority alert. Priority: P0.

### AI/Signal Processing
- **FR-006** — NLP/sentiment/emotion analysis of text/transcribed voice. Actor: AI Engine. Output: sentiment score, emotion label, confidence. Priority: P0.
- **FR-007** — Voice-stress feature extraction. Actor: AI Engine. Input: raw audio. Output: stress-indicator score. Priority: P1.
- **FR-008** — Safety-critical keyword/anomaly detection (bypass cadence). Actor: AI Engine. Output: immediate flag. Priority: P0.

### Distress Scoring & Prediction
- **FR-009** — Compute DDS (baseline, current, trend). Actor: Scoring Engine. Output: DDS record. Priority: P0.
- **FR-010** — Longitudinal trend/rate-of-deterioration analysis. Actor: Scoring Engine. Output: trend classification. Priority: P0.
- **FR-011** — Escalation risk prediction. Actor: Prediction Engine. Output: risk band + probability. Priority: P0.
- **FR-012** — Generate explanation (top contributing factors). Actor: XAI Layer. Output: factor list, plain-language summary. Priority: P0.

### Alerts & Case Management
- **FR-013** — Generate + route alert on threshold breach. Actor: Alert Service. Output: alert record, notification dispatched. Priority: P0.
- **FR-014** — Counsellor case queue with prioritization. Actor: Counsellor. Output: sorted worklist. Priority: P0.
- **FR-015** — Record human review decision. Actor: Counsellor. Output: reviewed/confirmed/adjusted case status. Priority: P0.

### Intervention
- **FR-016** — Recommend intervention category. Actor: Intervention Engine. Output: suggested category + rationale. Priority: P0.
- **FR-017** — Record human-selected intervention & responsible stakeholder. Actor: Counsellor/Official. Output: intervention record. Priority: P0.
- **FR-018** — Log follow-up outcome, trigger reassessment. Actor: Counsellor. Output: follow-up record. Priority: P0.

### Dashboards
- **FR-019** — District dashboard (identifiable high-risk cases, local aggregate). Actor: District Official. Priority: P0.
- **FR-020** — State dashboard (de-identified aggregate + audited drill-down). Actor: State Authority. Priority: P0.
- **FR-021** — National dashboard (fully de-identified). Actor: National Authority. Priority: P0.

### Security & Admin
- **FR-022** — Role-based access control enforcement. Actor: System. Priority: P0.
- **FR-023** — Immutable audit logging of all sensitive-data access. Actor: System. Priority: P0.
- **FR-024** — User/role management console. Actor: Admin. Priority: P1.

---

# 6. SYSTEM MODULES

| Module | Purpose | Inputs | Processing | Outputs | Dependencies | Key DB Entities |
|---|---|---|---|---|---|---|
| Auth | Identity & session management | Credentials/SSO token | OAuth2/JWT issuance, RBAC check | Session token | Identity provider | User, Authority |
| Case Management | Track victim/case lifecycle | Enrollment, case events | State transitions | Case record | Case-Event Integration (simulated) | Case, Victim |
| Consent | Manage consent lifecycle | Consent choice | Record, timestamp, scope | Consent record | Case Management | Victim |
| Interaction/Channel Service | Multi-channel check-in delivery/receipt | Schedule, victim response | Channel routing, queueing | Interaction record | SMS/IVRS/Chatbot gateways | Interaction |
| NLP Engine | Text/voice signal extraction | Text, transcript | Sentiment/emotion classification | Signal set | Interaction | Assessment |
| Voice Analysis | Acoustic stress features | Raw audio | Prosody/pitch/pause extraction | Stress score | Interaction | Assessment |
| Distress Scoring | Compute DDS | Signal set, history | Baseline/trend/anomaly calc | DDS record | NLP, Voice Analysis | DistressScore |
| Risk Prediction | Escalation forecasting | DDS history, context | Predictive model inference | Risk band, probability | Distress Scoring | RiskPrediction |
| Explainability (XAI) | Human-readable rationale | Model internals | Factor attribution (e.g., SHAP) | Explanation text | Risk Prediction | RiskEvent |
| Alerts | Notify humans on threshold breach | Risk event | Routing rules, dedup | Alert record, notification | Risk Prediction, Notification | Alert |
| Intervention | Track recommended/actual action | Alert, human decision | Workflow state | Intervention record | Alerts | Intervention |
| Notifications | Deliver messages across channels | Alert/system event | Channel dispatch, retry | Delivery status | SMS/Email/Push gateway | Notification |
| Dashboards/Analytics | Role-based visualization | Aggregated data | Aggregation, de-identification | Dashboard views | Case, DDS, RiskEvent | (read-only views) |
| Audit Logging | Accountability trail | All state-changing actions | Immutable append | Audit record | All modules | AuditLog |
| Administration | Platform management | Admin actions | Role/config management | Config/role state | Auth | User, Role |

---

# 7. UI/UX SPECIFICATION

Format per screen: ID · Name · Role · Purpose · Entry point · Components/Fields · Actions · Validation · API deps · Loading/Empty/Error/Success states.

## Victim-Facing

**SCR-V01 — Consent & Enrollment**
- Role: Victim. Purpose: capture consent + preferences. Entry: link/QR from case registration or NHAA referral.
- Components: plain-language explainer (+ audio icon), channel-selection cards, language selector, consent toggle + "Not right now" option.
- Actions: Submit consent, decline, request more info.
- Validation: at least one channel selected if consenting.
- API: `POST /api/v1/victims`, `POST /api/v1/consents`.
- States: Loading (spinner on submit) · Empty (n/a, first screen) · Error ("Couldn't save — try again," retry button) · Success (confirmation + next check-in date).

**SCR-V02 — Check-in (Chat)**
- Role: Victim. Purpose: conduct scheduled check-in.
- Components: conversational prompt, worded response options, "Skip for now," fixed "Talk to a person now" button.
- Actions: Respond, skip, escalate to human.
- Validation: none blocking (skip always allowed).
- API: `POST /api/v1/interactions`.
- States: Loading (message send) · Empty (no scheduled check-in: friendly "nothing due" message) · Error (retry, offline queue) · Success (thank-you + next steps).

**SCR-V03 — My Status**
- Role: Victim. Purpose: transparency without alarm.
- Components: plain-language status card, resource list (Counselling/Legal Aid/Financial/Medical), counsellor contact card.
- Actions: Request resource, contact counsellor.
- API: `GET /api/v1/victims/{id}/status`, `POST /api/v1/interventions/requests`.
- States: Loading (skeleton card) · Empty (not yet enrolled) · Error (fallback contact info shown) · Success (populated card).

**SCR-V04 — Home**
- Role: Victim. Purpose: landing/navigation.
- Components: greeting, next check-in reminder, resource shortcuts, privacy footer note.
- API: `GET /api/v1/victims/{id}/summary`.

## Authority/Counsellor-Facing

**SCR-C01 — Counsellor Case Queue**
- Role: Counsellor. Purpose: prioritized worklist.
- Components: sortable case list (risk band, trend arrow), filter, alert badge count.
- Actions: Open case, mark reviewed.
- API: `GET /api/v1/counsellors/{id}/cases`.
- States: Loading (list skeleton) · Empty ("No cases currently assigned") · Error (retry banner) · Success (populated list).

**SCR-C02 — Case Detail**
- Role: Counsellor. Purpose: full case review + action.
- Components: DDS trend chart, explanation panel (top factors), interaction history summary, intervention selector, notes field.
- Actions: Confirm/adjust risk, select intervention, log follow-up, close/reassess case.
- Validation: intervention selection required before closing an alert.
- API: `GET /api/v1/cases/{id}`, `POST /api/v1/interventions`, `PATCH /api/v1/cases/{id}`.
- States: Loading, Empty (n/a), Error (partial data warning if signal missing), Success.

**SCR-D01 — District Dashboard**
- Role: District Official. Purpose: local coordination.
- Components: stat cards (active cases, high/critical count, pending alerts, SLA%), case map/grid, alert feed.
- Actions: Assign counsellor, trigger protection workflow.
- API: `GET /api/v1/dashboards/district/{id}`.

**SCR-S01 — State Dashboard**
- Role: State Authority. Purpose: resource allocation oversight.
- Components: district comparison table/chart, risk-band distribution, "Request Drill-Down" (audited) button.
- API: `GET /api/v1/dashboards/state/{id}`.

**SCR-N01 — National Dashboard**
- Role: National Authority. Purpose: policy-level evidence.
- Components: state comparison, national KPI trend charts, intervention mix.
- API: `GET /api/v1/dashboards/national`.

**Cross-cutting UX requirements:** multilingual (persistent selector), accessible (WCAG-AA contrast, no color-only status indication), mobile-first for victim screens, low-literacy friendly (icon-led, short text, audio narration option), no raw score/risk-band shown to victims.

---

# 8. FRONTEND ARCHITECTURE

- **Framework:** React 18 + TypeScript (web dashboards); Flutter (victim mobile app + chatbot shell).
- **UI library:** Tailwind CSS + shadcn/ui component primitives; Chart.js for trend visualization.
- **Routing:** React Router (web); Flutter Navigator 2.0 (mobile).
- **State management:** React Query (server state/caching) + lightweight local state (Zustand) for UI state; avoid Redux boilerplate for this scope.
- **Form handling:** React Hook Form + schema validation (Zod).
- **API layer:** typed API client (generated from OpenAPI spec, Section 11) with a single Axios instance, interceptors for auth/error handling.
- **Auth handling:** JWT stored in memory + httpOnly refresh cookie; auto-refresh interceptor.
- **Error handling:** centralized error boundary per route; toast notifications for recoverable errors; fallback UI for data-fetch failures.
- **Component architecture:** atomic-ish structure — `ui/` (primitives), `components/` (composed, feature-agnostic), `features/` (feature-specific, e.g., `features/case-queue/`).

**Frontend folder structure (web dashboard):**
```
frontend/
  src/
    api/                # typed API client, endpoint hooks
    components/          # shared composed components
    ui/                   # design-system primitives
    features/
      auth/
      case-queue/
      case-detail/
      dashboards/
        district/
        state/
        national/
      victim-portal/      # if web victim access is in scope
    hooks/
    lib/                  # utilities, formatters
    routes/
    store/                # Zustand stores
    types/                # shared TS types (mirrors Section 12 models)
    App.tsx
  public/
  tests/
```

---

# 9. BACKEND ARCHITECTURE

- **Framework:** FastAPI (Python 3.11+).
- **API style:** REST, versioned (`/api/v1/`).
- **Application layers:** `routers/` (HTTP layer) → `services/` (business logic) → `repositories/` (DB access) → `models/` (ORM/schema).
- **Authentication:** OAuth2 password/bearer flow with JWT access + refresh tokens.
- **Authorization:** RBAC middleware evaluated per-route against the matrix in Section 3.
- **Business logic:** isolated in `services/`, independent of FastAPI request/response objects (testable in isolation).
- **Validation:** Pydantic models for request/response schemas.
- **Error handling:** centralized exception handlers mapping domain exceptions to consistent HTTP error responses.
- **Background processing:** Celery (or FastAPI `BackgroundTasks` for lighter jobs) for scheduled check-in dispatch, async AI inference, notification retries.
- **AI/ML integration:** AI/ML Engine exposed as an internal service (same repo, separate module, callable via internal API or direct import) — not a public-facing microservice at this scale.
- **Notifications:** dedicated `notifications/` service abstracting SMS/Email/Push/IVRS providers behind a common interface.
- **Logging:** structured JSON logging (e.g., `structlog`), correlation IDs per request.
- **Configuration:** environment-variable driven (Section 25), loaded via Pydantic Settings.

**Backend folder structure:**
```
backend/
  app/
    api/
      v1/
        routers/          # auth.py, victims.py, cases.py, interactions.py, alerts.py, interventions.py, dashboards.py
    services/              # business logic per domain
    repositories/          # DB access layer
    models/                 # SQLAlchemy ORM models
    schemas/                 # Pydantic request/response schemas
    ai/
      nlp/
      voice/
      scoring/
      prediction/
      explainability/
    notifications/
    core/                   # config, security, RBAC, exceptions
    db/                      # session, migrations (Alembic)
  tests/
  alembic/
  main.py
```

**Avoid unnecessary microservices** `[DESIGN DECISION]` — a single modular monolith with clear internal module boundaries is appropriate at this scale; the AI engine can be split into a separate service later (Section 24, ideal architecture) once load justifies it.

---

# 10. DATABASE DESIGN

Entities, purpose, and key fields (conceptual; exact SQL types are implementation detail for Antigravity to finalize against Section 25's `.env` and chosen PostgreSQL version).

| Entity | Purpose | Key Fields | PK | FK | Notes |
|---|---|---|---|---|---|
| User | Login-capable account for any human role | id, full_name, email, role, authority_id, auth_provider, last_login | id | authority_id → Authority.id | Victims are NOT Users (no login credential model needed for anonymous/low-literacy channels) |
| Authority | An official's org context | id, role, jurisdiction_level, district, state | id | — | jurisdiction_level ∈ {district, state, national} |
| Victim | Registered victim/witness | id, case_ref_id, preferred_language, preferred_channel, consent_status, enrolled_at | id | — | No direct login; identified by case linkage |
| Case | A legal case under monitoring | id, victim_id, crime_category, legal_stage, assigned_authority_id, status, created_at, closed_at | id | victim_id → Victim.id; assigned_authority_id → Authority.id | status ∈ {active, closed, reopened} |
| Interaction | One check-in event | id, case_id, channel, raw_ref_pointer, response_latency_sec, was_skipped, occurred_at | id | case_id → Case.id | raw_ref_pointer points to isolated encrypted store, not raw content inline |
| Assessment | AI-derived signals from one interaction | id, interaction_id, sentiment_score, emotion_label, voice_stress_score, confidence, processed_at | id | interaction_id → Interaction.id | |
| DistressScore | DDS snapshot | id, case_id, assessment_id, current_score, baseline_score, trend_slope, risk_band, computed_at | id | case_id, assessment_id | risk_band ∈ {low, moderate, high, critical} |
| RiskEvent | A detected threshold/anomaly trigger | id, dds_id, trigger_type, explanation_summary, detected_at | id | dds_id → DistressScore.id | trigger_type ∈ {threshold, anomaly, keyword} |
| Alert | Notification generated from a risk event | id, risk_event_id, authority_id, priority, status, sent_at, reviewed_at | id | risk_event_id, authority_id | status ∈ {pending, reviewed, dismissed} |
| Intervention | Human-decided action | id, alert_id, category, responsible_stakeholder, decision_notes, actioned_at | id | alert_id → Alert.id | category enum per Section 17 |
| FollowUp | Outcome tracking post-intervention | id, intervention_id, outcome_notes, reassessment_needed, followup_at | id | intervention_id → Intervention.id | |
| Notification | Delivery record for any dispatched message | id, alert_id (nullable), channel, recipient_ref, status, sent_at | id | alert_id → Alert.id | Distinct from Alert: one alert can have multiple delivery attempts |
| AuditLog | Immutable access/action trail | id, case_id (nullable), user_id, action_type, access_tier, logged_at | id | case_id, user_id | Append-only, no update/delete permitted at app layer |

**Relationships (summary):** Victim 1—* Case · Case 1—* Interaction · Interaction 1—1 Assessment · Assessment 1—* DistressScore (over time) · DistressScore 1—* RiskEvent · RiskEvent 1—* Alert · Alert 1—* Intervention · Intervention 1—* FollowUp · Authority 1—* User · Case/User → AuditLog (many-to-one each).

**Sensitivity tiering (carried into schema design):** raw voice/text NEVER stored inline in `Interaction` — only a pointer (`raw_ref_pointer`) into a separately encrypted, access-isolated object store. This is a hard constraint, not an optimization (see Section 19).

**Indexes (minimum):** `Case(victim_id)`, `Interaction(case_id, occurred_at)`, `DistressScore(case_id, computed_at)`, `Alert(authority_id, status)`, `AuditLog(case_id, logged_at)`.

---

# 11. API SPECIFICATION

Base path: `/api/v1`. Auth: Bearer JWT unless noted. All timestamps ISO-8601 UTC.

### Auth
**POST /api/v1/auth/login**
- Purpose: authenticate a User (staff role). Auth: none (public).
- Request: `{ "email": "string", "password": "string" }`
- Response 200: `{ "access_token": "string", "refresh_token": "string", "role": "counsellor" }`
- Errors: 401 invalid credentials.

**POST /api/v1/auth/refresh**
- Request: `{ "refresh_token": "string" }` → Response 200: `{ "access_token": "string" }`

### Victims & Consent
**POST /api/v1/victims** — Authorized: District Official, System (enrollment flow).
- Request: `{ "case_ref_id": "string", "preferred_language": "hi", "preferred_channel": "sms" }`
- Response 201: `{ "id": "uuid", "case_ref_id": "string", "enrolled_at": "iso8601" }`
- Errors: 400 invalid case_ref_id, 409 already enrolled.

**POST /api/v1/consents** — Authorized: Victim (via channel-authenticated session).
- Request: `{ "victim_id": "uuid", "consented": true, "channels": ["sms","chatbot"] }`
- Response 201: `{ "id": "uuid", "victim_id": "uuid", "status": "active" }`

**GET /api/v1/victims/{id}/status** — Authorized: Victim (self).
- Response 200: `{ "enrolled": true, "next_checkin": "iso8601", "resources": [ {"category":"counselling","available":true} ] }` — note: no score/risk-band field exists in this response by design.

### Interactions
**POST /api/v1/interactions** — Authorized: Victim (self, via channel session).
- Request: `{ "case_id": "uuid", "channel": "chatbot", "response_text": "string", "response_latency_sec": 12 }`
- Response 201: `{ "id": "uuid", "occurred_at": "iso8601" }`
- Errors: 400 missing case_id, 403 consent inactive.

### Cases & Risk
**GET /api/v1/cases/{id}** — Authorized: Counsellor (assigned), District/State/National (role-filtered).
- Response 200: `{ "id":"uuid", "victim_id":"uuid", "status":"active", "current_dds": {"score":62,"risk_band":"moderate","trend":"worsening"}, "explanation": ["Sustained negative sentiment over 3 check-ins","Reduced engagement"] }`

**GET /api/v1/counsellors/{id}/cases** — Authorized: Counsellor (self).
- Query params: `?risk_band=high&sort=priority`
- Response 200: `{ "cases": [ {"id":"uuid","risk_band":"high","trend":"worsening","last_checkin":"iso8601"} ] }`

**PATCH /api/v1/cases/{id}** — Authorized: Counsellor (assigned), District Official.
- Request: `{ "status": "closed", "closure_reason": "string" }`
- Response 200: updated case object. Errors: 409 open alert pending review.

### Alerts
**GET /api/v1/alerts** — Authorized: Counsellor, District/State/National (role-filtered).
- Response 200: `{ "alerts": [ {"id":"uuid","case_id":"uuid","priority":"high","status":"pending","sent_at":"iso8601"} ] }`

**PATCH /api/v1/alerts/{id}** — Authorized: Counsellor.
- Request: `{ "status": "reviewed" }` → Response 200: updated alert.

### Interventions
**POST /api/v1/interventions** — Authorized: Counsellor, District Official.
- Request: `{ "alert_id":"uuid", "category":"counselling", "responsible_stakeholder":"district_welfare", "decision_notes":"string" }`
- Response 201: `{ "id":"uuid", "actioned_at":"iso8601" }`
- Errors: 400 invalid category enum.

**POST /api/v1/interventions/{id}/followups** — Authorized: Counsellor.
- Request: `{ "outcome_notes":"string", "reassessment_needed": true }`
- Response 201: follow-up object.

### Dashboards
**GET /api/v1/dashboards/district/{id}** — Authorized: District Official (own district).
- Response 200: `{ "active_cases": 42, "high_critical_count": 5, "pending_alerts": 3, "sla_compliance_pct": 91.2, "cases": [ ... identifiable, role-justified ... ] }`

**GET /api/v1/dashboards/state/{id}** — Authorized: State Authority (own state).
- Response 200: `{ "districts": [ {"name":"...", "active_cases":120, "risk_distribution":{"low":80,"moderate":30,"high":8,"critical":2}} ] }` — de-identified.

**GET /api/v1/dashboards/national** — Authorized: National Authority.
- Response 200: `{ "states": [...], "national_risk_distribution": {...}, "avg_time_to_intervention_days": 4.2 }` — fully de-identified.

### Audit
**GET /api/v1/audit-logs** — Authorized: Admin only.
- Query: `?case_id=uuid&from=iso8601&to=iso8601`
- Response 200: `{ "logs": [ {"user_id":"uuid","action_type":"case_view","logged_at":"iso8601"} ] }`

**Standard error shape (all endpoints):**
```json
{ "error": { "code": "STRING_CODE", "message": "human-readable", "details": {} } }
```
Standard status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Validation Error, 500 Internal Error.

---

# 12. SHARED DATA MODELS

```typescript
type RiskBand = "low" | "moderate" | "high" | "critical";
type CaseStatus = "active" | "closed" | "reopened";
type Channel = "chatbot" | "ivrs" | "sms" | "app" | "web";
type InterventionCategory =
  "counselling" | "legal_aid" | "medical_referral" |
  "protection_relocation" | "financial_assistance" | "rehabilitation";

interface Victim {
  id: string;               // required
  case_ref_id: string;      // required
  preferred_language: string; // required
  preferred_channel: Channel; // required
  consent_status: "active" | "revoked" | "pending"; // required
  enrolled_at: string;      // required, ISO8601
}

interface Case {
  id: string;
  victim_id: string;
  crime_category: string;
  legal_stage?: string;      // optional — may be unknown early
  assigned_authority_id?: string;
  status: CaseStatus;
  created_at: string;
  closed_at?: string;        // optional
}

interface Assessment {
  id: string;
  interaction_id: string;
  sentiment_score: number;     // -1..1
  emotion_label?: string;      // optional — may be low-confidence/unavailable
  voice_stress_score?: number; // optional — only if voice channel used
  confidence: number;          // 0..1
  processed_at: string;
}

interface DistressScore {
  id: string;
  case_id: string;
  assessment_id: string;
  current_score: number;   // 0-100
  baseline_score: number;
  trend_slope: number;
  risk_band: RiskBand;
  computed_at: string;
}

interface RiskPrediction {
  id: string;
  case_id: string;
  escalation_probability: number; // 0..1
  window_days: number;            // prediction horizon
  top_factors: string[];          // explanation
  generated_at: string;
}

interface Alert {
  id: string;
  risk_event_id: string;
  authority_id: string;
  priority: "moderate" | "high" | "critical";
  status: "pending" | "reviewed" | "dismissed";
  sent_at: string;
  reviewed_at?: string;
}

interface Intervention {
  id: string;
  alert_id: string;
  category: InterventionCategory;
  responsible_stakeholder: string;
  decision_notes?: string;
  actioned_at: string;
}

interface Notification {
  id: string;
  alert_id?: string;         // optional — some notifications are non-alert (e.g., check-in reminders)
  channel: Channel;
  status: "sent" | "delivered" | "failed";
  sent_at: string;
}
```
These models are the single contract shared across frontend TS types, backend Pydantic schemas, and the API responses in Section 11 — any change must be reflected in all three (see Section 38, rule 3).

---

# 13. AUTHENTICATION & AUTHORIZATION

- **Registration:** staff Users (Counsellor/District/State/National/Admin) are provisioned by an Admin — no public self-registration for authority roles. Victims are enrolled (Section 11), not "registered" with credentials.
- **Login:** email + password for staff; OAuth2 password flow.
- **Authentication mechanism:** JWT access token (short-lived, 15 min) + refresh token (httpOnly cookie, 7 days).
- **Password handling:** bcrypt/argon2 hashing, never logged or returned in any response.
- **RBAC:** enforced via a decorator/dependency on every route, checked against the matrix in Section 3.
- **Session expiry:** access token 15 min; forced re-auth on refresh token expiry or role change.
- **Password reset:** email-based reset link, single-use token, 30-min expiry.
- **Administrative access:** Admin actions (role changes, user creation) require re-authentication (step-up auth) and are always audit-logged.

### Authorization matrix (endpoint-group level)

| Endpoint group | Victim | Counsellor | District | State | National | Admin |
|---|---|---|---|---|---|---|
| /victims, /consents | Self | Read (assigned) | Read (jurisdiction) | Read (aggregate) | Read (aggregate) | No |
| /interactions | Self (write) | Read (assigned) | No | No | No | No |
| /cases | No | Read/Write (assigned) | Read/Write (jurisdiction) | Read (aggregate) | Read (aggregate) | No |
| /alerts | No | Read/Write (assigned) | Read (jurisdiction) | Read (aggregate) | Read (aggregate) | No |
| /interventions | Request only | Read/Write | Read/Write (coordinate) | No | No | No |
| /dashboards/* | No | Own queue | District | State | National | System health |
| /audit-logs | No | No | No | No | No | Full |
| /admin/users | No | No | No | No | No | Full |

---

# 14. AI/ML ARCHITECTURE

### Input signals
Text (chatbot/SMS/app free-text) · Structured questionnaire responses · Voice (IVRS audio) · Behavioural/engagement (latency, skip rate, channel-switch) · Case events (hearing dates, threats reported — simulated feed) · Temporal (time since complaint, time since last contact).

### Processing pipeline

| Component | Input | Method | Output | Purpose |
|---|---|---|---|---|
| Preprocessing | Raw text/audio | Cleaning, language ID, transcription (voice→text) | Normalized text + audio features | Prepare for downstream models |
| NLP/Sentiment | Normalized text | Fine-tuned multilingual transformer (e.g., IndicBERT/MuRIL base) | Sentiment score, confidence | Base distress signal |
| Emotion | Normalized text | Emotion classification head | Emotion label (fear/sadness/anger/hopelessness/neutral) | Refines beyond polarity |
| Voice Analysis | Raw audio | Acoustic feature extraction (prosody/pitch/pause via OpenSMILE/Librosa) | Voice-stress score | Independent, cross-checking signal |
| Feature Extraction | All signals + metadata | Feature vectorization | Feature vector | Model-ready input |
| Distress Scoring | Feature vector + history | Rule-weighted composite (deterministic, not ML) `[DESIGN DECISION]` | DDS (0-100) | Central interpretable score |
| Longitudinal/Trend | DDS time series | Statistical trend (e.g., weighted slope) — deterministic, not ML | Trend direction, rate | Distinguish bad day vs decline |
| Escalation Prediction | Trend + context | ML classifier (e.g., gradient-boosted trees on tabular features) | Escalation probability, risk band | Proactive alerting |
| Anomaly Detection | Interaction-to-interaction deltas | Statistical/ML anomaly detection (e.g., isolation forest) | Anomaly flag | Catches sharp deviations |
| Explainability | Model internals | SHAP (tree/ensemble models), attention weights (transformer) | Top contributing factors | Human-auditable rationale |

**ML vs rule-based vs generative — explicit boundary `[DESIGN DECISION]`:**
- **ML models:** sentiment/emotion classification, escalation prediction, anomaly detection.
- **Deterministic/rule-based:** DDS composite scoring formula, trend-slope calculation, threshold-to-risk-band mapping — kept deterministic specifically so it stays auditable and explainable, not a black box.
- **Generative AI:** NOT used for scoring or decisions. May optionally be used only for drafting plain-language explanation phrasing from structured factor lists (never for generating clinical judgments).

### Output
Distress score · Risk band · Trend direction · Contributing factors (ranked) · Confidence/uncertainty per signal · Recommended intervention category (Section 17).

---

# 15. DYNAMIC DISTRESS SCORE

**Conceptual formula** `[DESIGN DECISION — initial weights are ASSUMPTIONS requiring clinical validation before deployment]`:

```
DDS_current = clamp(0, 100,
    w1 * normalized_sentiment_component
  + w2 * normalized_emotion_component
  + w3 * normalized_voice_stress_component
  + w4 * engagement_dropoff_component
  + w5 * contextual_risk_component
)

Initial illustrative weights (ASSUMPTION, not validated):
  w1 = 0.30 (sentiment)
  w2 = 0.25 (emotion)
  w3 = 0.20 (voice stress, when available; redistributed proportionally when absent)
  w4 = 0.15 (engagement dropoff)
  w5 = 0.10 (contextual risk factors: e.g., recent threat, upcoming hearing)
```

- **Baseline:** DDS from first assessment, personalizes subsequent comparisons.
- **Trend slope:** linear regression (or weighted moving average) over the last N check-ins.
- **Rate of deterioration:** trend slope magnitude compared against a personalized threshold (not a single global cutoff).
- **Contextual modifiers:** additive risk factors (active threat report: +X, upcoming hearing within 7 days: +Y) — values are `[ASSUMPTION]`, to be tuned with clinical/domain partners.

**Risk band thresholds (illustrative, ASSUMPTION):**

| Band | DDS range (illustrative) | Trigger |
|---|---|---|
| Low | 0-39 | Routine schedule continues |
| Moderate | 40-59 | Counsellor notified, no forced action |
| High | 60-79 | Alert to counsellor + district, SLA review required |
| Critical | 80-100 OR safety-keyword/anomaly flag | Immediate alert, bypasses normal cadence |

**Escalation logic:** a case escalates a band when (a) DDS crosses the next threshold, OR (b) trend slope exceeds the personalized deterioration threshold for 2+ consecutive check-ins, OR (c) an anomaly/safety-keyword flag fires independent of the numeric score.

**Explicit constraint (non-negotiable):** DDS is a decision-support indicator only. It is never presented as a diagnosis, never shown to the victim as a raw number, and always accompanied by an explanation when shown to a counsellor.

---

# 16. RISK PREDICTION & EXPLAINABILITY

- **Prediction target:** probability of entering "High" or "Critical" risk band within the prediction window.
- **Prediction window:** 5-7 days `[ASSUMPTION, matches the PS's innovation framing of early-warning]`.
- **Features:** DDS history (last 5 check-ins), trend slope, contextual risk factors, engagement pattern, time-since-last-threat-report.
- **Model options:** gradient-boosted trees (e.g., XGBoost/LightGBM) for tabular escalation prediction — chosen for interpretability compatibility with SHAP over deep sequence models, given small expected pilot dataset size.
- **Training requirements:** requires a labeled pilot dataset (does not exist yet — `[ASSUMPTION/gap]`, see Section 33 risks); model must not be deployed at "prediction-grade" confidence until validated with clinical partners.
- **Output:** escalation probability (0-1), risk band, ranked contributing factors, confidence interval.
- **Thresholds:** calibrated per Section 15's risk bands; probability > 0.7 within window triggers "High" alert regardless of current DDS band.
- **False positives:** human review absorbs these — no autonomous action ever taken on a prediction alone.
- **False negatives:** mitigated by independent anomaly detection + safety-keyword bypass (Section 14) as a second net.
- **Human review:** mandatory before any intervention is dispatched (Section 17).

**What an authority sees when a case is flagged (concrete UI contract):**
```
Case CASE-2481 — Risk: HIGH (escalation probability: 0.78)
Why flagged:
  • Sustained negative sentiment trend over last 3 check-ins (+0.41 contribution)
  • Engagement drop-off: 2 consecutive skipped check-ins (+0.22 contribution)
  • Contextual: hearing scheduled in 4 days (+0.15 contribution)
Confidence: Medium (voice signal unavailable this cycle)
[Review Case] [Log Intervention] [Dismiss with note]
```
This is the literal contract — "HIGH RISK" is never shown without the "Why flagged" block directly beneath it.

---

# 17. INTERVENTION ENGINE

**Framework:** Risk/Condition → Reason (explanation) → Recommended Intervention → Responsible Role → Human Decision → Logged Outcome.

| Category | Trigger pattern (example) | Responsible role |
|---|---|---|
| counselling | Sustained moderate distress, no acute risk | Counsellor |
| medical_referral | Distress linked to reported physical/trauma symptoms | Health department liaison |
| protection_relocation | Threat/intimidation signal (witness) | Police / District Official |
| financial_assistance | Distress linked to compensation delay/economic hardship mentions | District welfare office |
| legal_aid | Distress linked to case delay/procedural confusion | DLSA |
| rehabilitation | Post-crisis stabilization | NGO/welfare partner |

**Hard rule `[DESIGN DECISION, non-negotiable]`:** the Intervention Engine only ever produces a *recommendation* (category + rationale). The `POST /api/v1/interventions` endpoint requires an authenticated human (Counsellor/District Official) as the actor of record — there is no system-actor path that can create an Intervention record. This is enforced at the API layer, not just the UI layer.

---

# 18. NOTIFICATION & ALERT SYSTEM

| Alert type | Severity | Trigger | Recipients | Channels |
|---|---|---|---|---|
| Routine review | Moderate | DDS enters Moderate band | Assigned Counsellor | In-app |
| Priority review | High | DDS enters High band / escalation probability > 0.7 | Counsellor + District Official | In-app, SMS |
| Critical/immediate | Critical | Safety keyword, anomaly, or Critical band | Counsellor + District Official (+ State if unactioned past SLA) | In-app, SMS, Email |
| System/operational | N/A | Notification delivery failure, integration failure | Admin | In-app, Email |

- **Escalation:** if a High/Critical alert is not reviewed within its SLA (`[ASSUMPTION]` 4 hours for Critical, 24 hours for High), auto-escalate visibility to the next authority level.
- **Retry handling:** failed SMS/Email dispatch retried with exponential backoff (3 attempts); persistent failure logged and surfaced to Admin.
- **Notification status:** `sent → delivered → (failed)`, tracked per the `Notification` entity (Section 10).
- **Real vs simulated:** In-app + Email are real integrations in the prototype. SMS/IVRS use a sandbox/mock provider interface in the prototype `[DESIGN DECISION]`, swappable for a real telecom gateway in production — clearly logged as `provider: "mock"` vs `provider: "live"` in the Notification record so this is never ambiguous.

---

# 19. SECURITY, PRIVACY & ETHICS

- **Consent:** explicit, scoped, timestamped, revocable at any time via `POST /api/v1/consents`.
- **Data minimization:** only fields listed in Section 10/12 are collected — no open-ended profiling fields.
- **Encryption:** TLS 1.2+ in transit; AES-256 at rest for the isolated raw voice/text store; standard encryption-at-rest for the relational DB.
- **RBAC:** enforced per Sections 3 and 13, at the API layer (not just UI).
- **Secure APIs:** rate limiting, input validation (Pydantic), no sensitive data in URL query strings, CORS restricted to known frontend origins.
- **Sensitive data handling:** raw voice/text lives only in the isolated store, referenced by pointer (Section 10) — never joined into analytics/dashboard queries.
- **Pseudonymization:** State/National dashboard queries aggregate via case IDs, never victim name/contact.
- **Audit logs:** append-only `AuditLog` entity, every read of case-level data by a Counsellor/District Official is logged.
- **Data retention:** `[ASSUMPTION — requires legal consultation]` proposed default: active case data retained for case duration + 1 year post-closure, then archived/anonymized; raw voice/text purged on a shorter cycle (e.g., 90 days) once processed into Assessment records.
- **Access monitoring:** anomalous access patterns (e.g., bulk case reads by one user) flagged to Admin.
- **Secrets management:** all credentials via environment variables / secret manager (Section 25), never committed to source control.
- **Backup:** daily encrypted DB backups, tested restore procedure `[FUTURE POSSIBILITY for prototype phase, required for production]`.
- **Incident response:** `[ASSUMPTION]` documented escalation contact and breach-notification procedure required before any real deployment — not built in the prototype.
- **Bias/fairness:** model performance must be evaluated across language, gender, and crime-type subgroups before deployment; ongoing monitoring required — flagged as a pre-deployment gate, not yet satisfied (Section 33).
- **Human oversight:** enforced structurally per Sections 16-17 (no autonomous action path exists in the API).
- **AI limitations:** explicitly communicated in every counsellor-facing explanation ("Confidence: Medium/Low" states, per Section 16).
- **Legal compliance:** this document does NOT claim certified compliance with any specific law (e.g., DPDP Act 2023) — it states design intent compatible with consent/minimization principles, pending formal legal review. `[explicit non-claim, per Section 36 rules]`

---

# 20. ERROR HANDLING & EDGE CASES

| Scenario | System behavior |
|---|---|
| Missing data (partial signal) | Compute DDS with confidence-weighted partial data; flag as "Low/Medium confidence," never silently treated as "Low risk" |
| Invalid input | 422 validation error with field-level detail; no partial write |
| Victim stops responding | Escalating but non-intrusive re-contact attempts; sustained non-response itself becomes a lower-confidence risk signal routed for human check |
| Sudden distress escalation | Anomaly/keyword bypass routes immediately, independent of scheduled cadence |
| Conflicting responses (e.g., calm text, stressed voice) | Flagged as anomaly for human judgment, never auto-averaged away |
| Duplicate case | Case-ID matching against case_ref_id prevents duplicate Victim/Case creation (409 Conflict) |
| Duplicate assessments | Idempotency key on `POST /api/v1/interactions` per (case_id, scheduled_slot) |
| AI failure (model unavailable) | Interaction still logged; DDS marked "pending computation," retried async; counsellor notified if retry exceeds threshold |
| Voice analysis failure | Falls back to text-only signal set with explicit confidence downgrade; never blocks the interaction |
| Language ambiguity | Routes to human-language-support flag rather than guessing; interaction still logged |
| Network failure (channel gateway) | Store-and-forward retry for IVRS/SMS; fallback channel suggested to victim on next contact |
| Database failure | Read replicas / retry with backoff; write failures return 503, never silently drop data |
| Notification failure | Retry per Section 18; persistent failure surfaced to Admin, never silently swallowed |
| Unauthorized access attempt | 403 + audit log entry + Admin alert on repeated attempts |
| False prediction (confirmed post-hoc) | Logged for model recalibration; does not auto-adjust live thresholds without a review cycle |

---

# 21. DASHBOARDS & ANALYTICS

| Level | Visible information | Explicitly NOT visible |
|---|---|---|
| District | Active case count, high/critical case list (identifiable, role-justified), alert feed, SLA compliance, counsellor assignment status | Raw interaction text/voice |
| State | District-wise aggregate risk distribution, trend comparison, resource allocation view | Individual case identity (drill-down requires audited justification) |
| National | State-wise aggregate, national risk-band distribution, policy KPIs (avg. time-to-intervention, intervention mix) | Any individual-level data by default |

All dashboard queries read from aggregated/role-filtered views (Section 10), never directly from `Interaction`/raw-content tables — enforced architecturally, not just by permission check, so a bug in RBAC cannot leak raw content through a dashboard endpoint.

---

# 22. SYSTEM ARCHITECTURE

### High-Level Architecture
```mermaid
flowchart TD
    A["Victim Channels<br/>Chatbot | IVRS | SMS | App | Web"] --> B["Interaction Service"]
    B --> C["AI/ML Engine<br/>NLP · Voice · Scoring · Prediction · XAI"]
    C --> D["Case & Alert Management Service"]
    D --> E["Notification Service"]
    D --> F["Dashboards API"]
    B --> G[("PostgreSQL — Case/Relational Data")]
    C --> H[("Encrypted Object Store — Raw Voice/Text")]
    D --> G
    F --> I["Counsellor App"]
    F --> J["District Dashboard"]
    F --> K["State Dashboard"]
    F --> L["National Dashboard"]
```

### Authentication Flow
```mermaid
sequenceDiagram
    participant U as Staff User
    participant FE as Frontend
    participant API as Backend API
    participant DB as Auth Store

    U->>FE: Enter credentials
    FE->>API: POST /auth/login
    API->>DB: Verify hash
    DB-->>API: OK
    API-->>FE: access_token + refresh_token
    FE->>API: Subsequent requests with Bearer token
    API->>API: RBAC check per route
```

### Assessment Flow
```mermaid
sequenceDiagram
    participant V as Victim
    participant CH as Channel Service
    participant AI as AI Engine
    participant DB as DistressScore Store

    V->>CH: Check-in response
    CH->>AI: text/voice + metadata
    AI->>AI: NLP + Voice + Feature Extraction
    AI->>DB: Write Assessment
    AI->>DB: Compute + write DistressScore
```

### Risk/Alert Flow
```mermaid
stateDiagram-v2
    [*] --> Assessed
    Assessed --> BelowThreshold
    Assessed --> ThresholdCrossed
    BelowThreshold --> [*]
    ThresholdCrossed --> ExplanationGenerated
    ExplanationGenerated --> AlertDispatched
    AlertDispatched --> HumanReviewed
    HumanReviewed --> [*]
```

### Intervention Flow
```mermaid
flowchart LR
    A[Alert Reviewed] --> B[Intervention Recommended]
    B --> C{Human Decision}
    C -->|Approve| D[Intervention Logged]
    C -->|Modify| D
    C -->|Reject| E[Dismissed with Note]
    D --> F[Follow-up Scheduled]
    F --> G[Outcome Logged]
```

---

# 23. TECHNOLOGY STACK

| Technology | Purpose | Reason for selection |
|---|---|---|
| React + TypeScript | Web dashboard frontend | Mature ecosystem, strong typing reduces integration bugs across the shared-models contract (Section 12) |
| Flutter | Victim mobile app + chatbot shell | Single codebase for Android/iOS, good offline support for low-connectivity users |
| FastAPI (Python) | Backend API | Async-native (good for I/O-bound multi-channel dispatch), auto-generates OpenAPI spec matching Section 11, same language as the AI stack |
| PostgreSQL | Relational data store | ACID guarantees needed for case/audit integrity, mature RBAC-friendly row-level security options |
| Encrypted object storage (S3-compatible) | Raw voice/text isolated store | Separation of sensitivity tiers (Section 10/19) |
| HuggingFace Transformers (IndicBERT/MuRIL) | NLP/sentiment/emotion | Pretrained multilingual base for Indian languages, fine-tunable |
| OpenSMILE / Librosa | Voice feature extraction | Established open-source acoustic feature toolkits |
| XGBoost/LightGBM | Escalation prediction | Interpretable-enough for SHAP explainability, works well on modest tabular datasets (realistic for a pilot) |
| SHAP | Explainability | Standard, model-agnostic-enough attribution method |
| OAuth2 + JWT | Authentication | Standard, stateless, RBAC-friendly |
| Celery + Redis | Background jobs (scheduling, async AI, notification retries) | Mature, well-understood task queue pairing with FastAPI |
| Docker | Containerization | Consistent dev/prod environments |
| Government-approved cloud / on-prem data center | Hosting | `[ASSUMPTION]` required for real deployment; prototype can run on any standard cloud (e.g., AWS/GCP) or locally |

**Avoided deliberately:** microservice sprawl, NoSQL for core case data (relational integrity matters more here than horizontal write scale at pilot size), any generative-AI-as-decision-maker pattern.

---

# 24. DEPLOYMENT ARCHITECTURE

### Prototype/development architecture
- Single Docker Compose stack: `frontend`, `backend`, `postgres`, `redis`, `celery-worker`, `object-storage (minio, S3-compatible mock)`.
- AI models loaded in-process within the backend container (no separate ML-serving infra needed at prototype scale).
- Mock providers for SMS/IVRS (Section 18).

### Ideal production architecture `[DESIGN DECISION — not built now]`
- Frontend: static hosting + CDN (web), app stores (mobile).
- Backend: containerized, deployed on government-approved cloud/data center, horizontally scalable behind a load balancer.
- AI/ML: split into a separate inference service once load justifies it, with model versioning.
- Database: managed PostgreSQL with read replicas, automated backups.
- Object storage: managed encrypted bucket with strict IAM policy, separate from application DB credentials.
- Logging/Monitoring: centralized log aggregation + metrics dashboard (e.g., Prometheus/Grafana equivalent) + alerting on system health (distinct from victim risk alerts).
- CI/CD: automated build → test → staged deploy pipeline, manual approval gate for production.

---

# 25. ENVIRONMENT CONFIGURATION

`.env.example` (no real secrets — placeholders only):
```
# App
APP_ENV=development
APP_SECRET_KEY=changeme-generate-a-real-secret
API_BASE_URL=http://localhost:8000/api/v1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myndsync
DATABASE_POOL_SIZE=10

# Redis / Celery
REDIS_URL=redis://localhost:6379/0

# Auth
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
JWT_SECRET_KEY=changeme-generate-a-real-secret

# Object Storage (raw voice/text — isolated tier)
OBJECT_STORAGE_ENDPOINT=http://localhost:9000
OBJECT_STORAGE_ACCESS_KEY=changeme
OBJECT_STORAGE_SECRET_KEY=changeme
OBJECT_STORAGE_BUCKET=myndsync-sensitive-store

# AI/ML
NLP_MODEL_NAME=ai4bharat/indic-bert
VOICE_STRESS_ENABLED=true
ESCALATION_MODEL_PATH=./models/escalation_model.pkl

# Notifications (mock providers in prototype)
SMS_PROVIDER=mock
EMAIL_PROVIDER=smtp
SMTP_HOST=changeme
SMTP_PORT=587
SMTP_USER=changeme
SMTP_PASSWORD=changeme

# Feature flags
ENABLE_CASE_EVENT_INTEGRATION_SIMULATION=true
```

**Sensitive variables** (never logged, never committed): `APP_SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL` (contains credentials), `OBJECT_STORAGE_ACCESS_KEY`/`SECRET_KEY`, `SMTP_USER`/`PASSWORD`.

---

# 26. REPOSITORY STRUCTURE

```
myndsync/
  frontend/           # React + TypeScript web dashboards (Section 8)
  mobile/              # Flutter victim app (Section 8)
  backend/             # FastAPI application (Section 9)
  ml/
    training/           # model training scripts, notebooks (not run in prod app)
    evaluation/          # bias/fairness/accuracy evaluation scripts
    models/               # versioned trained model artifacts
  docs/
    engineering-master-spec.md   # this document
    api-spec.yaml                 # generated OpenAPI (from Section 11)
    adr/                           # architecture decision records
  tests/
    backend/
    frontend/
    e2e/
  scripts/
    seed_data.py         # synthetic/illustrative seed data ONLY, never real case data
    migrate.sh
  .env.example
  docker-compose.yml
  README.md
```

Each top-level directory owns its own dependency management (`package.json` for frontend/mobile, `pyproject.toml`/`requirements.txt` for backend/ml) — no shared global dependency file.

---

# 27. COLLABORATIVE DEVELOPMENT WORKFLOW

- **Main branch:** `main` — always deployable, protected (no direct pushes).
- **Feature branches:** `feature/<module>-<short-desc>` (e.g., `feature/alerts-sla-escalation`).
- **Pull requests:** required for all merges to `main`; minimum 1 reviewer approval.
- **Code review:** reviewer checks against Section 38 rules (no silent API/DB contract changes, no scope creep).
- **Commit conventions:** Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`) for auto-changelog compatibility.
- **Issue tracking:** GitHub Issues, linked to FR-IDs (Section 5) and AC-IDs (Section 31) where applicable.
- **Environment setup:** `docker-compose up` should bring up a fully working local stack from a fresh clone + `.env` copy.
- **Merge strategy:** squash-merge to keep `main` history clean, one logical change per merged PR.
- **Shared documentation:** this spec (`docs/engineering-master-spec.md`) is updated in the same PR as any approved architectural change (Section 38, rule 10) — never left to drift.

---

# 28. TESTING STRATEGY

| Type | Scope | Example scenarios |
|---|---|---|
| Unit | Individual functions/services | DDS formula computation, trend-slope calculation, RBAC permission check function |
| API | Each endpoint in isolation | `POST /interactions` with missing consent → 403; `PATCH /cases/{id}` closure with pending alert → 409 |
| Integration | Cross-module flows | Interaction → Assessment → DistressScore → RiskEvent → Alert chain end-to-end |
| Frontend | Component + interaction | Case queue sort/filter, consent screen decline flow, "Talk to a person now" always renders |
| AI/ML evaluation | Model quality, not app logic | Sentiment/emotion accuracy on held-out labeled sample; subgroup performance (language, gender) for bias check; escalation model precision/recall on illustrative synthetic data |
| Security | Access control, data isolation | Attempt cross-district data access → 403 + audit log entry; attempt to read raw voice via dashboard endpoint → structurally impossible (test asserts no such join exists) |
| End-to-end | Full user journeys | Enroll → check-in → escalate → alert → intervention → follow-up → closure, across District dashboard visibility |
| User acceptance | Role-specific usability | Counsellor can find and act on a High-risk case within N clicks; victim can decline consent without dark patterns |

**Critical test (non-negotiable, ties to Section 17):** an automated test must assert that no code path exists where an `Intervention` record can be created without an authenticated human `user_id` as actor — this is a permanent regression guard on the human-in-the-loop constraint.

---

# 29. DEVELOPMENT ROADMAP

```mermaid
flowchart LR
    A[Foundation<br/>Auth, Victim/Case, Consent] --> B[Core System<br/>Interactions, Channels]
    B --> C[AI<br/>NLP, Voice, Feature Extraction]
    C --> D[Risk<br/>DDS, Trend, Prediction, XAI]
    D --> E[Dashboard<br/>Counsellor, District, State, National]
    E --> F[Integration<br/>Notifications, Simulated Case-Events]
    F --> G[Testing<br/>Security, E2E, Bias eval]
    G --> H[Deployment<br/>Prototype demo environment]
```

**Dependencies:** AI (C) depends on Core System (B) providing real interaction data to process; Risk (D) depends on AI (C) for input signals; Dashboards (E) depend on Risk (D) existing to have anything meaningful to show; Integration (F) can proceed in parallel with D/E once Core System (B) is stable; Testing (G) is continuous but a dedicated hardening pass follows E/F; Deployment (H) is prototype-only at this stage (no production rollout implied).

---

# 30. MVP EXTRACTION PREPARATION

| Capability | Tier |
|---|---|
| Enrollment + Consent | Essential Core |
| Text-based check-in (chatbot/SMS) | Essential Core |
| Basic NLP sentiment analysis | Essential Core |
| DDS computation (deterministic formula) | Essential Core |
| Threshold-based alerting to Counsellor | Essential Core |
| Counsellor case queue + case detail view | Essential Core |
| Basic District dashboard | Essential Core |
| RBAC + audit logging | Essential Core |
| Voice/IVRS channel + voice-stress analysis | Important |
| Emotion recognition (beyond sentiment) | Important |
| Escalation prediction model (ML) | Important |
| State/National dashboards | Important |
| Explainability (SHAP-based factor attribution) | Important |
| Anomaly detection | Advanced |
| Bias/fairness monitoring pipeline | Advanced |
| SLA auto-escalation | Advanced |
| Real government API integration | Future |
| Clinically validated instrument versions | Future |
| Additional languages/channels beyond pilot set | Future |

This classification is preparation only — MVP is derived from this list in a separate step, not decided here.

---

# 31. ACCEPTANCE CRITERIA

- **AC-001** — Given a victim with active consent, when a scheduled check-in is due, the system dispatches it via their preferred channel within the scheduling window.
- **AC-002** — Given a victim submits a check-in response, when processed, an Assessment record is created within an acceptable processing time (`[ASSUMPTION]` < 30s for text).
- **AC-003** — Given 3+ consecutive check-ins with worsening sentiment, when DDS is recomputed, the trend is classified as "worsening" and reflected in the case's risk band.
- **AC-004** — Given a case crosses into High or Critical risk band, when the RiskEvent is generated, an Alert is dispatched to the assigned Counsellor within the defined SLA.
- **AC-005** — Given an Alert is displayed to a Counsellor, the "Why flagged" explanation is always rendered together with the risk band — never the risk band alone.
- **AC-006** — Given a Counsellor wants to create an Intervention, the system rejects any attempt without a valid authenticated human `user_id` as actor.
- **AC-007** — Given a District Official views the dashboard, only cases within their jurisdiction are visible.
- **AC-008** — Given a State Authority views the dashboard, no individually identifiable victim data is visible without an audited drill-down request.
- **AC-009** — Given any read of case-level sensitive data, an AuditLog entry is created recording user, action, and timestamp.
- **AC-010** — Given a victim revokes consent, no further check-ins are scheduled and existing scheduled ones are cancelled.
- **AC-011** — Given the AI engine is unavailable, an interaction is still logged and not lost, with DDS computation marked pending/retried.
- **AC-012** — Given a safety-critical keyword is detected in a response, the system routes an alert immediately, bypassing the normal check-in cadence.

---

# 32. DEFINITION OF DONE

A capability is considered technically complete when:
- **Frontend:** implemented per Section 7 screen spec (including loading/empty/error/success states), responsive, meets accessibility baseline.
- **Backend:** endpoint implemented per Section 11 contract, validated against Pydantic schemas, RBAC-enforced.
- **Database:** schema matches Section 10, migration scripts committed, indexes in place.
- **APIs:** documented in the generated OpenAPI spec, matches Section 12 shared models exactly.
- **AI/ML:** model output includes confidence/uncertainty, explainability factors present for any risk-affecting output.
- **Security:** relevant AC from Section 31 passes; no sensitive data in logs; audit logging verified.
- **Testing:** unit + API tests passing; relevant E2E scenario (Section 28) passing.
- **Documentation:** this spec updated if any contract changed (Section 38); README updated if setup steps changed.
- **Deployment:** runs cleanly via `docker-compose up` in the prototype environment.

---

# 33. TECHNICAL RISKS

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| No labeled dataset exists for escalation prediction | High — model may be unreliable pre-pilot | High | Treat prediction model as illustrative until a supervised pilot with clinical partners produces real labels; keep deterministic DDS as the primary interpretable signal |
| Voice stress analytics is a scientifically contested signal | Medium — could mislead if over-trusted | Medium | Keep as one input among several, never sole determinant; always paired with confidence indicator |
| Multilingual NLP performance varies across low-resource languages | Medium — inconsistent signal quality | High | Phased language rollout; confidence-downgrade for unsupported/low-confidence languages rather than false precision |
| Sensitive data breach (voice/text store) | Very High — severe, irreversible harm to vulnerable population | Low (if controls followed) | Isolated encrypted store, strict RBAC, audit logging, minimal retention |
| Alert fatigue from false positives | Medium — counsellor trust erosion, missed real alerts | Medium | Human review buffer, prioritized queue, ongoing threshold calibration |
| Missed crisis (false negative) | Very High | Medium | Multiple independent signals (trend + anomaly + keyword bypass), periodic random-sample review of Low-band cases |
| Government integration remains simulated indefinitely | Medium — limits real-world utility | Medium (until partnership secured) | Keep integration layer clearly abstracted/swappable (Section 15/18 "mock vs live" pattern) |
| Scope creep during development | Medium — timeline/complexity risk | Medium | Section 38 rules (no unapproved architecture/feature changes); MVP tiering (Section 30) enforced |
| Bias/differential performance across demographic subgroups | High — ethical/credibility risk | Medium | Mandatory subgroup evaluation (Section 28) as a pre-deployment gate |
| Team members working on conflicting DB/API changes | Low-Medium — integration breakage | Medium | Section 27 workflow (PR review, shared spec as source of truth) |

---

# 34. SIH PPT MASTER (Engineering-Aligned)

This is a lighter, engineering-grounded companion to the PPT content already built earlier in this conversation — use whichever is more current; do not present both. Referenced here for spec completeness only.

| # | Title | Objective | Key content | Visual | Stats/source |
|---|---|---|---|---|---|
| 1 | Title | Identify project | MyndSync, PS ID, team | SIH branding | — |
| 2 | Problem | Establish gap | Prolonged distress, no continuous monitoring | Constellation graphic (already built) | — |
| 3 | Existing Gap | Quantify the gap | 94%+ court pendency (from the earlier GoI data extract) | Donut chart | POA Act Report 2022, GoI |
| 4 | Target Users & Stakeholders | Roles | Role table (Section 3 of this doc) | Stakeholder mindmap | — |
| 5 | Proposed Solution | Introduce MyndSync | One-liner, UVP | — | — |
| 6 | System Workflow | Show lifecycle | Section 4 lifecycle table | Sequence + state diagrams (Section 22) | — |
| 7 | AI/ML Innovation | Technical depth | Section 14 table | Pipeline diagram | — |
| 8 | Dynamic Distress & Risk Prediction | Explain DDS | Section 15 formula (illustrative), risk bands | Quadrant chart (prioritization logic) | Explicitly "illustrative" |
| 9 | Intervention & Dashboard | Human-in-loop + oversight | Section 17 framework, dashboard screens | District/State/National mockups | — |
| 10 | Technical Architecture | Credibility | Section 22 high-level diagram | Architecture flowchart | — |
| 11 | Expected Impact | Outcomes | PS-stated outcomes, directional only | Journey map (before/after) | — |
| 12 | Future Scope | Roadmap | Section 2 future tier, Section 24 production architecture | Gantt roadmap | — |

---

# 35. SINGLE SOURCE OF TRUTH — CONSISTENCY AUDIT

| Chain link | Check | Status |
|---|---|---|
| Problem → Requirements | Every FR traces to a PS capability (periodic interaction, NLP/sentiment/emotion, DDS, prediction, alerts, intervention, dashboards, explainability, privacy) | Consistent |
| Requirements → Features | Section 2 scope matches Section 5 FRs, no untraceable features | Consistent |
| Features → User Flows | Section 4 lifecycle matches FR groupings | Consistent |
| User Flows → UI | Section 7 screens cover every lifecycle stage requiring human interaction | Consistent |
| UI → APIs | Every screen's "API dependencies" maps to an endpoint in Section 11 | Consistent |
| APIs → Backend | Section 11 endpoints map to Section 9 router/service structure | Consistent |
| Backend → Database | Every endpoint's data need maps to a Section 10 entity | Consistent |
| Database → AI | AI outputs (Assessment, DistressScore, RiskPrediction) match Section 14 pipeline outputs exactly | Consistent |
| AI → Risk → Alerts | Section 15/16 risk bands match Section 18 alert severity mapping | Consistent |
| Alerts → Intervention | Section 17 categories match the `InterventionCategory` enum in Section 12 | Consistent |
| Intervention → Security | Human-actor-required rule (Section 17) matches AC-006 (Section 31) and the DoD security check (Section 32) | Consistent |
| Security → Architecture | Section 19 sensitivity tiering matches Section 10's isolated-store design and Section 22's architecture diagram | Consistent |
| Architecture → Technology | Section 23 stack choices match Section 22's components exactly (no unlisted technology appears in diagrams) | Consistent |
| Technology → PPT | Section 34 PPT references only technologies/claims already established in this document | Consistent |

No contradictions identified across the chain.

---

# 36. FACT / DESIGN DECISION / ASSUMPTION — SUMMARY

Every section above is inline-labeled; key structural ones repeated here for visibility:
- **PS FACT:** multi-channel periodic interaction requirement; NLP/Sentiment/Emotion AI/Voice Stress as named innovation components; dashboards at district/state/national level; explainable AI, privacy, and legal/ethical compliance requirement; priority use cases (rape/gang rape, murder/grievous hurt/arson, intimidated witnesses, caste-violence-affected families).
- **DESIGN DECISION:** project name MyndSync; deterministic DDS formula (vs. black-box ML) for the core score; hard API-layer block on autonomous intervention creation; modular monolith over microservices; mock-vs-live provider pattern for notifications/integration.
- **ASSUMPTION:** DDS weights and risk thresholds (Section 15) are illustrative, pending clinical validation; data retention periods (Section 19); prediction window of 5-7 days; SLA timings (Section 18); stakeholder list (Section 1).
- **FUTURE POSSIBILITY:** real government API integration; clinically validated instruments; expanded language/channel coverage; production-grade deployment architecture (Section 24).

No government API, dataset, statistic, or partnership is claimed as real beyond what is explicitly sourced in this conversation's data extract (the GoI POA Act 2022 report, cited by name).

---

# 37. CRITICAL SIH REVIEW

**Weaknesses / risks:** the escalation prediction model has no real training data yet — it is a designed capability, not a proven one, and should be presented as such. Voice stress analytics is scientifically contested. Multilingual performance is unproven at this stage. Government integration is entirely simulated.

**What's genuinely innovative:** the deliberate split between a deterministic, auditable DDS core and an ML-based predictive layer — most comparable systems would black-box the whole thing; this design keeps the load-bearing score explainable by construction, not just by an XAI layer bolted on afterward.

**What could be simplified for a demo:** voice-stress analysis and full escalation ML could be deferred to "Important" tier (already reflected in Section 30) if development time is tight — the deterministic DDS + sentiment/emotion + threshold alerting alone demonstrates the core loop convincingly.

**What would make it stronger:** a real (even if small) pilot dataset; a named clinical/NGO partner for validation; a working demo of the human-review interface, not just the AI pipeline; the court-pendency statistic (94%+, from the GoI report already in this conversation) prominently justifying urgency.

### Top 10 Judge Questions

1. **"Is this AI diagnosing mental illness?"** No — DDS is a decision-support indicator; Section 15 states this explicitly and the victim never sees a raw score.
2. **"Where's your training data?"** None exists yet for this specific population; the escalation model is a designed capability pending a supervised pilot (Section 33) — the deterministic DDS core does not require training data and is usable from day one.
3. **"Can the AI ever act on its own?"** No — enforced at the API layer (Section 17), not just policy; a regression test (Section 28) guards this permanently.
4. **"How do you prevent alert fatigue?"** Threshold + anomaly + human-review buffer (Section 18/33); ongoing calibration.
5. **"Is voice stress analysis reliable?"** No, and we say so — it's one weak signal among several, never sole determinant (Section 33).
6. **"How is victim privacy protected?"** Tiered data sensitivity, isolated encrypted store, RBAC, audit logging, minimal retention (Section 19).
7. **"Do you have real government API access?"** No — clearly simulated (Section 18/36), swappable design for future real integration.
8. **"What happens if a prediction is wrong?"** Human review absorbs it before any real-world action (Section 16/17); logged for recalibration (Section 20).
9. **"How does this scale beyond a pilot district?"** Roadmap in Section 24 (ideal production architecture) and Section 29; MVP tiering (Section 30) shows deliberate phased scope.
10. **"What's the single biggest technical risk?"** Absence of labeled data for the predictive layer (Section 33) — mitigated by not over-relying on it; the deterministic, explainable DDS remains the system's backbone.

---

# 38. ANTIGRAVITY IMPLEMENTATION RULES

This document is the engineering source of truth. The coding agent must:

1. Not redesign the architecture (Sections 8, 9, 22-24) without explicit approval.
2. Not change API contracts (Section 11) silently — any change requires updating this document in the same change set.
3. Not change database entities/relationships (Section 10) silently — same rule as above.
4. Not introduce features absent from Section 2's scope or Section 5's FR list.
5. Not expose secrets — follow Section 25's environment variable pattern strictly; never hardcode credentials.
6. Follow the folder structures defined in Sections 8, 9, and 26 exactly.
7. Maintain consistency between frontend types, backend schemas, and API responses per Section 12 — a change to one requires the same change to all three in the same PR.
8. Handle errors explicitly per Section 20 — no silent failures, no swallowed exceptions.
9. Write modular, maintainable code following the layered architecture in Section 9 (routers → services → repositories).
10. Update this document when an approved architectural change occurs (same PR, per Section 27).
11. Implement incrementally, following the roadmap and dependency order in Section 29.
12. Test each module (Section 28) before integrating into the next roadmap phase.
13. When a requirement is ambiguous, explain the recommended approach and its trade-offs before making a major architectural decision — do not silently pick one.
14. Never claim functionality that has not actually been implemented — no placeholder UI that implies a working feature; use explicit "Coming soon" states instead.
15. Keep prototype simulations (mock SMS/IVRS providers, simulated case-event integration) clearly labeled and structurally separated from any real external integration, per the `provider: "mock"` vs `"live"` pattern in Section 18.
16. The hard rule in Section 17 (no autonomous Intervention creation) and the AC-006 test (Section 31) are permanent invariants — any change to this specific constraint requires explicit human approval, not inferred from a related change.

---

*End of Project Engineering Master Specification. This document, the earlier Project Master Specification (business/product framing), and the PPT content package are the three source-of-truth documents for this project — keep all three in sync when any of them changes.*
