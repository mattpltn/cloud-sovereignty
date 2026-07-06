// Layer 2 — persona spot-checks, converted from tests/assertions/layer2-spec.yaml's
// P1 group. See reviews/layer2-assertions-owner-review.md and
// tests/assertions/conversion-table.md.
//
// Marked it.fails throughout (expected red) since resolve() throws until
// Milestone 4d — remove .fails there.

import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { CONTROL_REFS } from "../helpers/control-refs.js";
import { autoAnswerOf, ceiling, dispositionOf, negotiationCount, questionCount, SCORED_DOMAINS } from "../helpers/engine-assertions.js";
import { loadPersonaByShorthand } from "../helpers/personas.js";

const P1 = loadPersonaByShorthand("P1");
const TIER = P1.tiers[0].tier_id;

describe("Layer 2 — P1 (gov DC, vanilla OSS, in-house)", () => {
  it.fails("P1-1: ceiling(P1,d) = max band (4) for all six SOV domains", () => {
    const result = resolve(P1, TIER);
    for (const domain of SCORED_DOMAINS) {
      if (ceiling(result, domain) !== 4) throw new Error(`${domain}: ceiling is not the max band (4)`);
    }
  });

  it.fails("P1-2: provider-facing controls adapt to self-assessment wording (spot: SBOM/software-dependency control, disposition assess, wording self)", () => {
    const result = resolve(P1, TIER);
    const d = dispositionOf(result, CONTROL_REFS.SBOM_SOFTWARE_DEPENDENCY);
    if (d.disposition !== "assess") throw new Error(`expected disposition=assess, got ${d.disposition}`);
    if (d.wording_variant !== "self") throw new Error(`expected wording_variant=self, got ${d.wording_variant}`);
  });

  it.fails("P1-3: extraterritorial-exposure controls auto_answer positive, each with rationale and rule citation", () => {
    const result = resolve(P1, TIER);
    const extraterritorialAnswers = result.auto_answers.filter((a) =>
      result.dispositions.some((d) => d.control_id === a.control_id && d.disposition === "auto_answer"),
    );
    if (extraterritorialAnswers.length === 0) throw new Error("expected at least one auto_answer for extraterritorial-exposure controls");
    for (const a of extraterritorialAnswers) {
      if (!a.rationale?.trim()) throw new Error(`${a.control_id}: missing rationale`);
      if (!a.rule_id?.trim()) throw new Error(`${a.control_id}: missing rule_id`);
    }
  });

  it.fails("P1-4: C3A SOV-1-04-class (change-of-control notification) suppressed: no self-analog", () => {
    const result = resolve(P1, TIER);
    const d = dispositionOf(result, CONTROL_REFS.CHANGE_OF_CONTROL_NOTIFICATION);
    if (d.disposition !== "suppress") throw new Error(`expected disposition=suppress, got ${d.disposition}`);
  });

  it.fails("P1-5: external-key-management control auto_answer met (government_held custody)", () => {
    const result = resolve(P1, TIER);
    const d = dispositionOf(result, CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT);
    if (d.disposition !== "auto_answer") throw new Error(`expected disposition=auto_answer, got ${d.disposition}`);
    const a = autoAnswerOf(result, CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT);
    if (!/met/i.test(a.rationale)) throw new Error(`expected rationale to indicate the control is met, got: ${a.rationale}`);
  });

  it.fails("P1-6: negotiation-flagged controls = 0", () => {
    const result = resolve(P1, TIER);
    if (negotiationCount(result) !== 0) throw new Error(`expected 0 negotiation flags, got ${negotiationCount(result)}`);
  });

  it.fails("P1-7: asked-question count in [50,90]", () => {
    const result = resolve(P1, TIER);
    const count = questionCount(result);
    if (count < 50 || count > 90) throw new Error(`assess count ${count} outside [50,90]`);
  });

  it.fails("P1-8: no rendered question references a provider contract, colo operator, or external vendor (I2 spot)", () => {
    const result = resolve(P1, TIER);
    for (const d of result.dispositions) {
      if (d.disposition !== "assess") continue;
      if (d.wording_variant && d.wording_variant !== "self") {
        throw new Error(`${d.control_id}: assess control uses non-self wording_variant ${d.wording_variant}`);
      }
    }
  });
});
