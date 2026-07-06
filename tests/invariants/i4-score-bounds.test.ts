import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { SCORED_DOMAINS } from "../helpers/engine-assertions.js";
import { loadApprovedPersonas } from "../helpers/personas.js";

/**
 * I4 — Score bounds and renormalization.
 *
 * Original (Phase 1) form: achieved <= ceiling <= 100 in every SOV
 * domain, with suppressed-control weight renormalization to 100%.
 *
 * Milestone 4a scope split: Phase 4 introduces ceilings ONLY, as
 * ordinal 0-4 maturity bands (meta.ceiling_scale in
 * tests/assertions/layer2-spec.yaml) — achieved scores, outcome
 * weights, and evidence-quality math are explicitly Phase 5 (per this
 * milestone's own instructions). The checkable half now is: every
 * domain's ceiling is a valid band, 0 <= ceiling <= 4. The
 * achieved/renormalization half remains it.todo until Phase 5 gives the
 * engine an achieved score to check — this is a scope split already
 * anticipated by the task, not a weakening of the invariant.
 *
 * Marked it.fails (expected red) since resolve() throws until Milestone 4d.
 */
describe("I4: 0 <= ceiling <= 4 in every SOV domain (ordinal band bounds)", () => {
  for (const persona of loadApprovedPersonas()) {
    for (const tier of persona.tiers) {
      it.fails(`${persona.persona_id}/${tier.tier_id}: every domain's ceiling is a valid 0-4 band`, () => {
        const result = resolve(persona, tier.tier_id);
        for (const domain of SCORED_DOMAINS) {
          const c = result.ceilings[domain];
          if (c === undefined) throw new Error(`${domain}: no ceiling recorded`);
          if (c < 0 || c > 4) throw new Error(`${domain}: ceiling ${c} out of the 0-4 band range`);
        }
      });
    }
  }

  it.todo("achieved <= ceiling <= 100 with suppressed-control weight renormalization — deferred to Phase 5 (achieved scores don't exist in the Phase 4 API)");
});
