// Layer 2 — persona spot-checks, converted from tests/assertions/layer2-spec.yaml's
// P7 group. See reviews/layer2-assertions-owner-review.md and
// tests/assertions/conversion-table.md.
//
// Marked it.fails throughout (expected red) since resolve() throws until
// Milestone 4d — remove .fails there.

import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { CONTROL_REFS } from "../helpers/control-refs.js";
import { autoAnswerOf, ceiling, dispositionOf, negotiationCount, questionCount } from "../helpers/engine-assertions.js";
import { loadPersonaByShorthand } from "../helpers/personas.js";

const P4 = loadPersonaByShorthand("P4");
const P5 = loadPersonaByShorthand("P5");
const P7 = loadPersonaByShorthand("P7");
const TIER = P7.tiers[0].tier_id;

describe("Layer 2 — P7 (partner-operated sovereign region)", () => {
  it.fails("P7-1: ceiling(P7,SOV-6) <= ceiling(P4,SOV-6) and <= ceiling(P2,SOV-6) (deepest platform dependence — also covered as X2)", () => {
    const p7 = ceiling(resolve(P7, TIER), "SOV-6");
    const p4 = ceiling(resolve(P4, P4.tiers[0].tier_id), "SOV-6");
    if (!(p7 <= p4)) throw new Error(`SOV-6: P7 (${p7}) not <= P4 (${p4})`);
  });

  it.fails("P7-2: ceiling(P7,SOV-1) > ceiling(P5,SOV-1) (local partner entity vs foreign provider entity)", () => {
    const p7 = ceiling(resolve(P7, TIER), "SOV-1");
    const p5 = ceiling(resolve(P5, P5.tiers[0].tier_id), "SOV-1");
    if (!(p7 > p5)) throw new Error(`SOV-1: P7 (${p7}) not strictly > P5 (${p5})`);
  });

  it.fails("P7-3: key-management controls auto_answer met (HYOK); audit controls met via contract (contractual evidence tier)", () => {
    const result = resolve(P7, TIER);
    const keyMgmt = dispositionOf(result, CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT);
    if (keyMgmt.disposition !== "auto_answer") throw new Error(`expected disposition=auto_answer, got ${keyMgmt.disposition}`);
    const a = autoAnswerOf(result, CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT);
    if (!/met/i.test(a.rationale)) throw new Error(`expected rationale to indicate the control is met, got: ${a.rationale}`);
    const contractualAutoAnswers = result.auto_answers.filter((x) => x.evidence_tier === "contractual_commitment");
    if (contractualAutoAnswers.length === 0) throw new Error("expected at least one auto_answer with evidence_tier=contractual_commitment (audit controls)");
  });

  it.fails("P7-4: exit/reversibility controls not-met + negotiation_opportunity >= 1 (no exit path from licensed stack)", () => {
    const result = resolve(P7, TIER);
    if (negotiationCount(result) < 1) throw new Error(`expected >= 1 negotiation flag, got ${negotiationCount(result)}`);
  });

  it.fails("P7-5: asked-question count in [30,70]", () => {
    const result = resolve(P7, TIER);
    const count = questionCount(result);
    if (count < 30 || count > 70) throw new Error(`assess count ${count} outside [30,70]`);
  });

  it.fails("P7-6: effective-control controls (C3A SOV-1-03 class) assess — not auto-met: license dependence must be examined", () => {
    const result = resolve(P7, TIER);
    for (const id of CONTROL_REFS.EFFECTIVE_CONTROL) {
      const d = dispositionOf(result, id);
      if (d.disposition === "auto_answer") throw new Error(`${id}: expected NOT auto_answer (must assess license dependence), got auto_answer`);
    }
  });
});
