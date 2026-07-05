import { describe, expect, it } from "vitest";
import { filterApproved, loadAllPersonas, loadApprovedPersonas } from "./personas.js";
import type { PersonaProfile } from "../../engine/types.js";

// Minimal synthetic fixtures (CR-2, reviews/persona-approval-review.md) —
// deliberately NOT under tests/personas/, so the approval gate's negative
// case (drafts excluded) stays provable even once every real golden
// persona is approved and no draft remains among them.
const SYNTHETIC_DRAFT: PersonaProfile = {
  persona_id: "synthetic-draft-fixture",
  name: "Synthetic draft fixture",
  summary: "Test-only fixture; never a real golden persona.",
  status: "draft",
  priorities: [
    "continuity_under_disconnection",
    "protection_from_foreign_legal_access",
    "lock_in_avoidance",
    "local_capacity_building",
    "cost_efficiency",
  ],
  classification_scheme: "default_4_tier",
  tiers: [
    {
      tier_id: "public",
      axis_a: "A4",
      modifiers: { ops_outsourced: { outsourced: true }, service_model: "SaaS", key_custody: "provider_held" },
    },
  ],
};
const SYNTHETIC_APPROVED: PersonaProfile = {
  ...SYNTHETIC_DRAFT,
  persona_id: "synthetic-approved-fixture",
  status: "approved",
  approved_by: "Test Fixture",
  approved_date: "2026-07-04",
};

describe("persona fixture loader", () => {
  it("loads all 8 golden persona fixtures", () => {
    const personas = loadAllPersonas();
    expect(personas.map((p) => p.persona_id).sort()).toEqual(
      [
        "colo-oss-supported",
        "gov-dc-closed-outsourced",
        "gov-dc-oss-inhouse",
        "hyperscaler-iaas-strong-contract",
        "hyperscaler-saas-standard",
        "local-csp-iaas",
        "mixed-tier-estate",
        "sovereign-region-partner",
      ].sort(),
    );
  });

  it("loads all 8 golden personas as approved, post owner review", () => {
    // Per reviews/persona-owner-review.md (2026-07-04), the project owner
    // amended and approved all 8 golden personas. This test documents and
    // enforces that the persona ownership gate reflects that: approved
    // personas are now visible to engine tests.
    expect(loadApprovedPersonas().map((p) => p.persona_id).sort()).toEqual(
      [
        "colo-oss-supported",
        "gov-dc-closed-outsourced",
        "gov-dc-oss-inhouse",
        "hyperscaler-iaas-strong-contract",
        "hyperscaler-saas-standard",
        "local-csp-iaas",
        "mixed-tier-estate",
        "sovereign-region-partner",
      ].sort(),
    );
  });

  it("excludes a draft persona from the approval gate (CR-2 negative case)", () => {
    // With all 8 real golden personas now approved, this fixture pair is
    // what keeps the gate's exclusion behavior tested: a gate regression to
    // "return everything" would still pass the test above (all 8 loaded
    // personas happen to be approved) but would fail this one.
    const result = filterApproved([SYNTHETIC_DRAFT, SYNTHETIC_APPROVED]);
    expect(result.map((p) => p.persona_id)).toEqual(["synthetic-approved-fixture"]);
  });
});
