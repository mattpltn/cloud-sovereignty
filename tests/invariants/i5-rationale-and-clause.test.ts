import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { loadApprovedPersonas } from "../helpers/personas.js";

/**
 * I5 — Rationale and clause completeness.
 *
 * Every auto_answer disposition carries a rationale and a rule citation.
 * Every control flagged negotiation_opportunity carries clause text.
 * Nothing is scored or recommended invisibly (replaces v1's silent
 * auto_fail — see CLAUDE.md, Dispositions).
 *
 * Milestone 4a scope split: the Phase 4 public API's auto_answers[]
 * carries rationale + rule_id (this milestone's naming for "rule
 * citation") — that half is fully checkable now. Clause TEXT itself is
 * Phase 6's clause library; negotiation_flags (Phase 4's API) is only a
 * list of control_ids, with no text field to check yet. That half stays
 * it.todo until Phase 6 gives the engine clause text to check — again a
 * scope split anticipated by the task, not a weakening.
 *
 * Marked it.fails (expected red) since resolve() throws until Milestone 4d.
 */
describe("I5: auto_answer has non-empty rationale + rule_id", () => {
  for (const persona of loadApprovedPersonas()) {
    for (const tier of persona.tiers) {
      it.fails(`${persona.persona_id}/${tier.tier_id}: every auto_answer has non-empty rationale and rule_id`, () => {
        const result = resolve(persona, tier.tier_id);
        for (const a of result.auto_answers) {
          if (!a.rationale?.trim()) throw new Error(`${a.control_id}: auto_answer has no (non-empty) rationale`);
          if (!a.rule_id?.trim()) throw new Error(`${a.control_id}: auto_answer has no (non-empty) rule_id`);
        }
      });
    }
  }

  it.todo("every control with negotiation_opportunity=true has non-empty clause text — deferred to Phase 6 (clause library doesn't exist yet; negotiation_flags carries only control_ids in the Phase 4 API)");
});
