import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { loadCatalog } from "../helpers/catalog.js";
import { loadApprovedPersonas } from "../helpers/personas.js";

/**
 * I1 — Single disposition.
 *
 * Every catalog control resolves to exactly one disposition, for every
 * approved persona tier; zero unresolved, zero rule conflicts. Two
 * disposition rules firing for the same control with different
 * dispositions is a BUILD FAILURE, not silent precedence.
 *
 * Milestone 4a: marked it.fails (expected red) since resolve() throws
 * until Milestone 4d — remove .fails there. Runs against every approved
 * persona tier via tests/helpers/personas.ts#loadApprovedPersonas.
 */
describe("I1: every control resolves to exactly one disposition", () => {
  const allControlIds = loadCatalog().map((c) => c.primary_id);

  for (const persona of loadApprovedPersonas()) {
    for (const tier of persona.tiers) {
      it.fails(`${persona.persona_id}/${tier.tier_id}: exactly one disposition per catalog control, no conflicts`, () => {
        const result = resolve(persona, tier.tier_id);
        const seen = new Set<string>();
        for (const controlId of allControlIds) {
          const matches = result.dispositions.filter((d) => d.control_id === controlId);
          if (matches.length !== 1) {
            throw new Error(`${controlId}: expected exactly 1 disposition, got ${matches.length}`);
          }
          if (seen.has(controlId)) throw new Error(`${controlId}: duplicate control_id in dispositions`);
          seen.add(controlId);
        }
      });
    }
  }
});
