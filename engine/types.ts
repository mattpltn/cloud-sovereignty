// Structural types mirroring /schema/*.schema.json. The schemas are the
// source of truth (validated by scripts/validate.py); these types exist so
// the engine and its tests get compile-time checking. Keep in sync by hand
// until Phase 2+ introduces schema-to-type generation, if ever needed.

export type Disposition = "assess" | "auto_answer" | "inherit" | "suppress";

export type Layer =
  | "legal_jurisdiction"
  | "facility"
  | "supply_chain_hardware"
  | "supply_chain_software"
  | "supply_chain_services"
  | "virtualization"
  | "platform"
  | "data"
  | "identity"
  | "operations_personnel";

export type AxisA = "A1" | "A2" | "A3" | "A4" | "A5";
export type AxisB = "vanilla_oss" | "oss_commercial_support" | "closed_proprietary";
export type KeyCustody = "provider_held" | "hyok" | "external_hsm" | "government_held";
export type ServiceModel = "IaaS" | "PaaS" | "SaaS";

export interface Modifiers {
  ops_outsourced: { outsourced: boolean; to_whom?: string; jurisdiction?: string };
  service_model: ServiceModel;
  provider_jurisdiction?: string;
  facility_jurisdiction?: string;
  extraterritorial_law_exposure?: boolean;
  key_custody: KeyCustody;
  // Owner-review addition (D-025/persona schema): the platform stack
  // beneath a third-party provider (e.g. Axis A3's local CSP), when it
  // differs from the provider entity/facility jurisdiction. Same value
  // set as axis_b.
  provider_stack?: AxisB;
  contract_terms?: {
    audit_rights?: boolean;
    exit_reversibility?: boolean;
    residency_commitment?: boolean;
    escrow?: boolean;
  };
}

export interface TierScenario {
  tier_id: string;
  axis_a: AxisA;
  axis_b?: AxisB;
  modifiers: Modifiers;
}

export type Priority =
  | "continuity_under_disconnection"
  | "protection_from_foreign_legal_access"
  | "lock_in_avoidance"
  | "local_capacity_building"
  | "cost_efficiency";

export interface PersonaProfile {
  persona_id: string;
  name: string;
  summary: string;
  status: "draft" | "approved";
  approved_by?: string;
  approved_date?: string;
  priorities: Priority[];
  classification_scheme: "default_4_tier" | "national";
  tiers: TierScenario[];
}

export interface ResponsibilityMapEntry {
  layer: Layer;
  owning_party: string;
  operating_party: string;
  legal_reach_jurisdiction: string;
}

// ============================================================
// Phase 4 engine public API (Milestone 4a — types only; resolve() itself
// is not implemented until Milestone 4d). See tests/assertions/layer2-spec.yaml
// and reviews/layer2-assertions-owner-review.md for the specification this
// API shape must support, and tests/assertions/conversion-table.md for how
// each owner assertion maps onto these types.
// ============================================================

// The wording-variant KEY selected by the responsibility map for a given
// control — which party the question addresses. Question prose authoring
// (the actual text per key) is Phase 6; Phase 4 only selects the key.
export type WordingVariant =
  | "self" // government runs this layer itself (e.g. A1/A2 government-run stack)
  | "provider" // a third-party cloud/CSP provider
  | "integrator" // an independent local systems integrator/ops vendor
  | "colo_operator" // a colocation facility operator
  | "saas" // SaaS-specific framing (provider owns the full stack)
  | "partner"; // a licensed/franchised local partner operating a "sovereign region"

// Evidence-quality tiers, mirroring control-record.schema.json's
// evidence_quality_options enum (weakest to strongest).
export type EvidenceQuality =
  | "self_attested"
  | "contractual_commitment"
  | "third_party_certified"
  | "independently_audited";

// SOV-8 is out of scope per CLAUDE.md; SOV-7 is inheritance-only (still
// appears here since its catalog entries still resolve a disposition,
// just always "inherit").
export type SovDomain = "SOV-1" | "SOV-2" | "SOV-3" | "SOV-4" | "SOV-5" | "SOV-6" | "SOV-7";

// control_id is a master-catalog primary_id (data/catalog/catalog.json),
// e.g. "csat-sov4-01-c1" — one catalog entry is one distinct,
// independently disposable requirement (D-032 fixed the catalog so this
// holds for C1/C2 localization pairs too).
export interface DispositionEntry {
  control_id: string;
  disposition: Disposition;
  wording_variant?: WordingVariant;
  negotiation_opportunity: boolean;
}

export interface AutoAnswer {
  control_id: string;
  rationale: string;
  rule_id: string;
  evidence_tier: EvidenceQuality;
}

// Ceilings are ordinal 0-4 maturity bands per SOV domain (SEAL-consistent
// semantics per Phase 3's ladders.json and the Layer-2 spec's meta.ceiling_scale),
// computed structurally from the responsibility map + disposition rules.
// Achieved scores, outcome weights, and evidence-quality math are Phase 5 —
// not part of this type.
export type Ceilings = Partial<Record<SovDomain, number>>;

export interface EngineResult {
  dispositions: DispositionEntry[];
  auto_answers: AutoAnswer[];
  ceilings: Ceilings;
  negotiation_flags: string[]; // control_ids with negotiation_opportunity=true
  question_set: string[]; // control_ids with disposition=assess
}
