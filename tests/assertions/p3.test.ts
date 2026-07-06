// Layer 2 — persona spot-checks, converted from tests/assertions/layer2-spec.yaml's
// P3 group. See reviews/layer2-assertions-owner-review.md and
// tests/assertions/conversion-table.md.
//
// Marked it.fails throughout (expected red) since resolve() throws until
// Milestone 4d — remove .fails there.

import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { CONTROL_REFS } from "../helpers/control-refs.js";
import { autoAnswerOf, ceiling, dispositionOf, negotiationCount, questionCount } from "../helpers/engine-assertions.js";
import { loadPersonaByShorthand } from "../helpers/personas.js";

const P1 = loadPersonaByShorthand("P1");
const P3 = loadPersonaByShorthand("P3");
const TIER = P3.tiers[0].tier_id;

describe("Layer 2 — P3 (gov cloud in foreign-owned colo, OSS+support)", () => {
  it.fails("P3-1: facility-layer controls assess with colo-operator wording variant", () => {
    const result = resolve(P3, TIER);
    // Facility-layer proxy: the effective-control class controls sit at
    // legal_jurisdiction, not facility — use the catalog's own facility
    // members instead (D-032's cat-0031/external-key-mgmt is platform, not
    // facility). Spot-check via any assess control whose layer is facility.
    const facilityAssess = result.dispositions.filter((d) => d.disposition === "assess" && d.wording_variant === "colo_operator");
    if (facilityAssess.length === 0) throw new Error("expected at least one facility-layer control assessed with wording_variant=colo_operator");
  });

  it.fails("P3-2: ceiling(P3,SOV-2) < ceiling(P1,SOV-2) (foreign parent legal vector at facility layer)", () => {
    const p3sov2 = ceiling(resolve(P3, TIER), "SOV-2");
    const p1sov2 = ceiling(resolve(P1, P1.tiers[0].tier_id), "SOV-2");
    if (!(p3sov2 < p1sov2)) throw new Error(`SOV-2: P3 (${p3sov2}) not less than P1 (${p1sov2})`);
  });

  it.fails("P3-3: external-key-management control auto_answer met (government_held)", () => {
    const result = resolve(P3, TIER);
    const d = dispositionOf(result, CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT);
    if (d.disposition !== "auto_answer") throw new Error(`expected disposition=auto_answer, got ${d.disposition}`);
    const a = autoAnswerOf(result, CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT);
    if (!/met/i.test(a.rationale)) throw new Error(`expected rationale to indicate the control is met, got: ${a.rationale}`);
  });

  it.fails("P3-4: negotiation-flagged controls >= 1 targeting the support and/or colo contract", () => {
    const result = resolve(P3, TIER);
    if (negotiationCount(result) < 1) throw new Error(`expected >= 1 negotiation flag, got ${negotiationCount(result)}`);
  });

  it.fails("P3-5: asked-question count in [50,90]", () => {
    const result = resolve(P3, TIER);
    const count = questionCount(result);
    if (count < 50 || count > 90) throw new Error(`assess count ${count} outside [50,90]`);
  });

  it.fails("P3-6: platform-layer controls adapt to self-assessment wording (government-run stack), as in P1", () => {
    const result = resolve(P3, TIER);
    const d = dispositionOf(result, CONTROL_REFS.SBOM_SOFTWARE_DEPENDENCY);
    if (d.disposition === "assess" && d.wording_variant !== "self") {
      throw new Error(`expected wording_variant=self for the platform-layer SBOM control, got ${d.wording_variant}`);
    }
  });
});
