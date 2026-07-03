import { describe, expect, it } from "vitest";
import { loadAllPersonas, loadApprovedPersonas } from "./personas.js";

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

  it("refuses to treat unapproved personas as approved (persona ownership gate)", () => {
    // All 8 golden personas are currently status: draft, awaiting project-owner
    // review. This test documents and enforces that engine tests must see
    // zero approved personas until the owner amends and approves them.
    expect(loadApprovedPersonas()).toEqual([]);
  });
});
