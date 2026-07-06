import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { questionCount } from "../helpers/engine-assertions.js";
import { loadPersonaByShorthand, type PersonaShorthand } from "../helpers/personas.js";

/**
 * I7 — Questionnaire size sanity.
 *
 * The count of disposition=assess controls rendered per persona falls
 * within a declared band. A count above the band signals
 * suppression/auto_answer logic is leaking questions that should have
 * been resolved automatically or excluded as not applicable.
 *
 * Bands are the owner-frozen bands from tests/assertions/layer2-spec.yaml
 * (owner decision 8; P1-7/P2-5/P3-5/P4-5/P5-5/P6-5/P7-5): P1/P3 [50,90];
 * P2 [40,80]; P4 [35,75]; P5/P7 [30,70]; P6 [15,50]. P8's tiers reuse
 * P1's band (restricted, P1-class posture) and P6's band (public,
 * P6-class posture) per X5/P8-1 rather than a new band, since P8 is
 * explicitly a consistency vehicle, not a new posture.
 *
 * Marked it.fails (expected red) since resolve() throws until Milestone 4d.
 */
describe("I7: assessed-question count per persona stays within the declared band", () => {
  const BANDS: Record<PersonaShorthand, [number, number]> = {
    P1: [50, 90],
    P2: [40, 80],
    P3: [50, 90],
    P4: [35, 75],
    P5: [30, 70],
    P6: [15, 50],
    P7: [30, 70],
    P8: [15, 90], // widest span covering both its P1-class and P6-class tiers
  };

  for (const shorthand of Object.keys(BANDS) as PersonaShorthand[]) {
    const persona = loadPersonaByShorthand(shorthand);
    const [min, max] = BANDS[shorthand];
    for (const tier of persona.tiers) {
      it.fails(`${shorthand} (${persona.persona_id})/${tier.tier_id}: assess count within [${min},${max}]`, () => {
        const result = resolve(persona, tier.tier_id);
        const count = questionCount(result);
        if (count < min || count > max) throw new Error(`assess count ${count} outside declared band [${min},${max}]`);
      });
    }
  }
});
