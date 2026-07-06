// Layer 2 — persona spot-checks, converted from tests/assertions/layer2-spec.yaml's
// P4 group. See reviews/layer2-assertions-owner-review.md and
// tests/assertions/conversion-table.md.
//
// Marked it.fails throughout (expected red) since resolve() throws until
// Milestone 4d — remove .fails there.

import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { CONTROL_REFS } from "../helpers/control-refs.js";
import { ceiling, dispositionOf, negotiationCount, questionCount } from "../helpers/engine-assertions.js";
import { loadPersonaByShorthand } from "../helpers/personas.js";

const P1 = loadPersonaByShorthand("P1");
const P4 = loadPersonaByShorthand("P4");
const TIER = P4.tiers[0].tier_id;

describe("Layer 2 — P4 (local CSP on foreign closed stack, IaaS, standard terms)", () => {
  it.fails("P4-1: provider-jurisdiction controls (operate under {NATION} law class) auto_answer met (domestic provider entity)", () => {
    const result = resolve(P4, TIER);
    const d = dispositionOf(result, CONTROL_REFS.PROVIDER_JURISDICTION[0]);
    if (d.disposition !== "auto_answer") throw new Error(`expected disposition=auto_answer, got ${d.disposition}`);
  });

  it.fails("P4-2: SOV-6 ceiling(P4) <= ceiling(P1,SOV-6) - 1 band (foreign platform reflected in supply-chain/technology controls)", () => {
    const p4sov6 = ceiling(resolve(P4, TIER), "SOV-6");
    const p1sov6 = ceiling(resolve(P1, P1.tiers[0].tier_id), "SOV-6");
    if (!(p4sov6 <= p1sov6 - 1)) throw new Error(`SOV-6: P4 (${p4sov6}) not <= P1 (${p1sov6}) - 1 band`);
  });

  it.fails("P4-3: extraterritorial-exposure controls assess or auto_answer not-met — never suppressed, despite domestic provider (provider_stack vector)", () => {
    const result = resolve(P4, TIER);
    const d = dispositionOf(result, CONTROL_REFS.SOURCE_CODE_AVAILABILITY);
    if (d.disposition === "suppress") throw new Error("must not be suppressed — the foreign provider_stack is a real dependency for P4");
  });

  it.fails("P4-4: negotiation-flagged controls >= 3 (exit/reversibility, escrow-with-platform-vendor, key custody class)", () => {
    const result = resolve(P4, TIER);
    if (negotiationCount(result) < 3) throw new Error(`expected >= 3 negotiation flags, got ${negotiationCount(result)}`);
  });

  it.fails("P4-5: asked-question count in [35,75]", () => {
    const result = resolve(P4, TIER);
    const count = questionCount(result);
    if (count < 35 || count > 75) throw new Error(`assess count ${count} outside [35,75]`);
  });

  it.fails("P4-6: audit-rights controls auto_answer met via contract (evidence tier: contractual)", () => {
    const result = resolve(P4, TIER);
    const contractualAutoAnswers = result.auto_answers.filter((a) => a.evidence_tier === "contractual_commitment");
    if (contractualAutoAnswers.length === 0) throw new Error("expected at least one auto_answer with evidence_tier=contractual_commitment");
  });
});
