// Layer 2 — persona spot-checks, converted from tests/assertions/layer2-spec.yaml's
// P5 group. See reviews/layer2-assertions-owner-review.md and
// tests/assertions/conversion-table.md.
//
// Marked it.fails throughout (expected red) since resolve() throws until
// Milestone 4d — remove .fails there.

import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { CONTROL_REFS } from "../helpers/control-refs.js";
import { autoAnswerOf, dispositionOf, negotiationCount, questionCount } from "../helpers/engine-assertions.js";
import { loadPersonaByShorthand } from "../helpers/personas.js";

const P5 = loadPersonaByShorthand("P5");
const TIER = P5.tiers[0].tier_id;

describe("Layer 2 — P5 (foreign hyperscaler IaaS, strongest realistic contract)", () => {
  it.fails("P5-1: external-key-management control auto_answer met (HYOK)", () => {
    const result = resolve(P5, TIER);
    const d = dispositionOf(result, CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT);
    if (d.disposition !== "auto_answer") throw new Error(`expected disposition=auto_answer, got ${d.disposition}`);
    const a = autoAnswerOf(result, CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT);
    if (!/met/i.test(a.rationale)) throw new Error(`expected rationale to indicate the control is met, got: ${a.rationale}`);
  });

  it.fails("P5-2: data-residency controls: met at {TRUSTED_REGION} localization level, not-met at {NATION} level (D-032's separated C1/C2 entries)", () => {
    const result = resolve(P5, TIER);
    const trustedRegion = dispositionOf(result, CONTROL_REFS.DATA_RESIDENCY_TRUSTED_REGION);
    const nation = dispositionOf(result, CONTROL_REFS.DATA_RESIDENCY_NATION);
    if (trustedRegion.disposition !== "auto_answer") throw new Error(`{TRUSTED_REGION} residency: expected disposition=auto_answer, got ${trustedRegion.disposition}`);
    const trustedRegionAnswer = autoAnswerOf(result, CONTROL_REFS.DATA_RESIDENCY_TRUSTED_REGION);
    if (!/met/i.test(trustedRegionAnswer.rationale) || /not.?met/i.test(trustedRegionAnswer.rationale)) {
      throw new Error(`{TRUSTED_REGION} residency: expected rationale to indicate MET, got: ${trustedRegionAnswer.rationale}`);
    }
    if (nation.disposition !== "auto_answer") throw new Error(`{NATION} residency: expected disposition=auto_answer, got ${nation.disposition}`);
    const nationAnswer = autoAnswerOf(result, CONTROL_REFS.DATA_RESIDENCY_NATION);
    if (!/not.?met/i.test(nationAnswer.rationale)) {
      throw new Error(`{NATION} residency: expected rationale to indicate NOT MET, got: ${nationAnswer.rationale}`);
    }
  });

  it.fails("P5-3: provider-jurisdiction controls auto_answer not-met with rationale; negotiation-flagged controls >= 1", () => {
    const result = resolve(P5, TIER);
    const d = dispositionOf(result, CONTROL_REFS.PROVIDER_JURISDICTION[0]);
    if (d.disposition !== "auto_answer") throw new Error(`expected disposition=auto_answer, got ${d.disposition}`);
    const a = autoAnswerOf(result, CONTROL_REFS.PROVIDER_JURISDICTION[0]);
    if (!/not.?met/i.test(a.rationale)) throw new Error(`expected rationale to indicate NOT MET, got: ${a.rationale}`);
    if (negotiationCount(result) < 1) throw new Error(`expected >= 1 negotiation flag, got ${negotiationCount(result)}`);
  });

  it.fails("P5-4: exit/reversibility controls auto_answer met via contract (evidence tier: contractual)", () => {
    const result = resolve(P5, TIER);
    const contractualAutoAnswers = result.auto_answers.filter((a) => a.evidence_tier === "contractual_commitment");
    if (contractualAutoAnswers.length === 0) throw new Error("expected at least one auto_answer with evidence_tier=contractual_commitment");
  });

  it.fails("P5-5: asked-question count in [30,70]", () => {
    const result = resolve(P5, TIER);
    const count = questionCount(result);
    if (count < 30 || count > 70) throw new Error(`assess count ${count} outside [30,70]`);
  });
});
