import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { loadApprovedPersonas } from "../helpers/personas.js";
import type { AxisA, WordingVariant } from "../../engine/types.js";

/**
 * I2 — No absent-party questions.
 *
 * No rendered question references a party or layer absent from the
 * persona's responsibility map. This is the primary defense against
 * irrelevant questions — the failure mode that sank the previous project
 * (see CLAUDE.md, Testing methodology).
 *
 * Milestone 4a refinement (API shape): the public API (Milestone 4a)
 * exposes a wording_variant KEY per disposition, not the full
 * responsibility map (that's Milestone 4b's internal structure). So this
 * test checks the structurally-derivable half of I2 directly from
 * axis_a/service_model: a wording_variant can only be selected if the
 * party it names actually exists for this persona's deployment axis —
 * "colo_operator" requires Axis A2, "saas" requires service_model=SaaS,
 * "partner" requires Axis A5. This does not require the responsibility-
 * map builder to exist yet, and is not weakened relative to I2's intent:
 * it is a necessary (if not sufficient) condition of "the party exists".
 * Milestone 4b/4d should extend this once the full map is available.
 *
 * Marked it.fails (expected red) since resolve() throws until Milestone 4d.
 */
describe("I2: no rendered question references an absent party/layer", () => {
  function impossibleVariantsFor(axisA: AxisA, serviceModel: string): WordingVariant[] {
    const impossible: WordingVariant[] = [];
    if (axisA !== "A2") impossible.push("colo_operator");
    if (axisA !== "A5") impossible.push("partner");
    if (serviceModel !== "SaaS") impossible.push("saas");
    return impossible;
  }

  for (const persona of loadApprovedPersonas()) {
    for (const tier of persona.tiers) {
      it.fails(`${persona.persona_id}/${tier.tier_id}: no assess/auto_answer control uses a structurally-impossible wording_variant`, () => {
        const result = resolve(persona, tier.tier_id);
        const impossible = impossibleVariantsFor(tier.axis_a, tier.modifiers.service_model);
        for (const d of result.dispositions) {
          if ((d.disposition === "assess" || d.disposition === "auto_answer") && d.wording_variant && impossible.includes(d.wording_variant)) {
            throw new Error(`${d.control_id}: wording_variant ${d.wording_variant} is impossible for axis_a=${tier.axis_a}/service_model=${tier.modifiers.service_model}`);
          }
        }
      });
    }
  }
});
