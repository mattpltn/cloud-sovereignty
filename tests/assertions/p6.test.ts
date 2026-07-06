// Layer 2 — persona spot-checks, converted from tests/assertions/layer2-spec.yaml's
// P6 group (the floor). See reviews/layer2-assertions-owner-review.md and
// tests/assertions/conversion-table.md.
//
// Marked it.fails throughout (expected red) since resolve() throws until
// Milestone 4d — remove .fails there.

import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { CONTROL_REFS } from "../helpers/control-refs.js";
import { autoAnswerOf, dispositionOf, negotiationCount, questionCount } from "../helpers/engine-assertions.js";
import { loadPersonaByShorthand } from "../helpers/personas.js";

const P6 = loadPersonaByShorthand("P6");
const TIER = P6.tiers[0].tier_id;

describe("Layer 2 — P6 (foreign hyperscaler SaaS, standard terms — the floor)", () => {
  it.fails("P6-1: jurisdiction-class controls auto_answer not-met, each with rationale + negotiation_opportunity", () => {
    const result = resolve(P6, TIER);
    for (const id of CONTROL_REFS.PROVIDER_JURISDICTION) {
      const d = dispositionOf(result, id);
      if (d.disposition !== "auto_answer") throw new Error(`${id}: expected disposition=auto_answer, got ${d.disposition}`);
      if (!d.negotiation_opportunity) throw new Error(`${id}: expected negotiation_opportunity=true`);
      const a = autoAnswerOf(result, id);
      if (!/not.?met/i.test(a.rationale)) throw new Error(`${id}: expected rationale to indicate NOT MET, got: ${a.rationale}`);
    }
  });

  it.fails("P6-2: SaaS external-key-management (AC class) auto_answer not-met (provider_held) + negotiation flag", () => {
    const result = resolve(P6, TIER);
    const d = dispositionOf(result, CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT);
    if (d.disposition !== "auto_answer") throw new Error(`expected disposition=auto_answer, got ${d.disposition}`);
    if (!d.negotiation_opportunity) throw new Error("expected negotiation_opportunity=true");
    const a = autoAnswerOf(result, CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT);
    if (!/not.?met/i.test(a.rationale)) throw new Error(`expected rationale to indicate NOT MET, got: ${a.rationale}`);
  });

  it.fails("P6-3: negotiation-flagged controls >= 3 (residency, audit rights, exit class)", () => {
    const result = resolve(P6, TIER);
    if (negotiationCount(result) < 3) throw new Error(`expected >= 3 negotiation flags, got ${negotiationCount(result)}`);
  });

  it.fails("P6-4: SaaS-specific wording/criteria variants active (service_model drives AC applicability)", () => {
    const result = resolve(P6, TIER);
    const saasVariantUsed = result.dispositions.some((d) => d.wording_variant === "saas");
    if (!saasVariantUsed) throw new Error("expected at least one control resolved with wording_variant=saas");
  });

  it.fails("P6-5: asked-question count in [15,50]", () => {
    const result = resolve(P6, TIER);
    const count = questionCount(result);
    if (count < 15 || count > 50) throw new Error(`assess count ${count} outside [15,50]`);
  });
});
