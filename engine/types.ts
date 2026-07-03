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
export type KeyCustody = "provider_held" | "hyok" | "external_hsm";
export type ServiceModel = "IaaS" | "PaaS" | "SaaS";

export interface Modifiers {
  ops_outsourced: { outsourced: boolean; to_whom?: string; jurisdiction?: string };
  service_model: ServiceModel;
  provider_jurisdiction?: string;
  facility_jurisdiction?: string;
  extraterritorial_law_exposure?: boolean;
  key_custody: KeyCustody;
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

// A resolved disposition for one control under one persona tier. Populated
// by the Phase 4 engine; the shape is fixed now so invariant tests can be
// written against it ahead of the implementation.
export interface ResolvedControl {
  control_id: string;
  disposition: Disposition;
  wording_variant?: string;
  rationale?: Record<string, string>;
  rule_citation?: string;
  negotiation_opportunity: boolean;
}
