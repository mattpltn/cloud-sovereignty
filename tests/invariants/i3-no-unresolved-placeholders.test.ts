import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { loadApprovedPersonas } from "../helpers/personas.js";

/**
 * I3 — No unresolved placeholders.
 *
 * No unresolved {NATION}, {TRUSTED_REGION} or {PROVIDER} placeholder in
 * any rendered text (question wording, rationale, negotiation clause).
 *
 * Milestone 4a scope: the only free-text field the Phase 4 public API
 * exposes is auto_answers[].rationale (question wording is Phase 6;
 * negotiation clause text is Phase 6's clause library, not part of
 * negotiation_flags, which is just a list of control_ids). Checks that
 * field now; extend once Phase 6 renders more text.
 *
 * Marked it.fails (expected red) since resolve() throws until Milestone 4d.
 */
describe("I3: no unresolved placeholders in rendered text", () => {
  const PLACEHOLDER_PATTERN = /\{NATION\}|\{TRUSTED_REGION\}|\{PROVIDER\}/;

  for (const persona of loadApprovedPersonas()) {
    for (const tier of persona.tiers) {
      it.fails(`${persona.persona_id}/${tier.tier_id}: no unresolved placeholder in any auto_answer rationale`, () => {
        const result = resolve(persona, tier.tier_id);
        for (const a of result.auto_answers) {
          if (PLACEHOLDER_PATTERN.test(a.rationale)) {
            throw new Error(`${a.control_id}: rationale contains an unresolved placeholder: ${a.rationale}`);
          }
        }
      });
    }
  }
});
