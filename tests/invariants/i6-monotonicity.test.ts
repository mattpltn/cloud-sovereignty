import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { SCORED_DOMAINS } from "../helpers/engine-assertions.js";
import { loadApprovedPersonas } from "../helpers/personas.js";
import type { PersonaProfile, TierScenario } from "../../engine/types.js";

/**
 * I6 — Monotonicity.
 *
 * Adding a strengthening modifier (e.g. HYOK, an audit-rights clause)
 * never lowers any score or ceiling for an approved persona tier; removing
 * one never raises them. Checked by programmatically toggling one modifier
 * at a time on an approved persona's tier and comparing resulting scores.
 *
 * Milestone 4a scope split: checked on CEILING only (0-4 ordinal bands),
 * since achieved scores don't exist until Phase 5 — same split as I4/I5.
 *
 * Marked it.fails (expected red) since resolve() throws until Milestone 4d.
 */
describe("I6: strengthening a modifier never lowers ceiling, weakening never raises it", () => {
  function withTier(persona: PersonaProfile, tierId: string, tier: TierScenario): PersonaProfile {
    return {
      ...persona,
      tiers: persona.tiers.map((t) => (t.tier_id === tierId ? tier : t)),
    };
  }

  for (const persona of loadApprovedPersonas()) {
    for (const tier of persona.tiers) {
      if (tier.modifiers.key_custody === "provider_held") {
        it.fails(`${persona.persona_id}/${tier.tier_id}: key_custody provider_held->hyok never lowers any domain's ceiling`, () => {
          const strengthened: TierScenario = { ...tier, modifiers: { ...tier.modifiers, key_custody: "hyok" } };
          const before = resolve(persona, tier.tier_id);
          const after = resolve(withTier(persona, tier.tier_id, strengthened), tier.tier_id);
          for (const domain of SCORED_DOMAINS) {
            const b = before.ceilings[domain];
            const a = after.ceilings[domain];
            if (b === undefined || a === undefined) throw new Error(`${domain}: missing ceiling`);
            if (a < b) throw new Error(`${domain}: ceiling decreased from ${b} to ${a} after strengthening key_custody`);
          }
        });
      }

      for (const flag of ["audit_rights", "exit_reversibility", "residency_commitment", "escrow"] as const) {
        if (tier.modifiers.contract_terms?.[flag] === false) {
          it.fails(`${persona.persona_id}/${tier.tier_id}: contract_terms.${flag} false->true never lowers any domain's ceiling`, () => {
            const strengthened: TierScenario = {
              ...tier,
              modifiers: { ...tier.modifiers, contract_terms: { ...tier.modifiers.contract_terms, [flag]: true } },
            };
            const before = resolve(persona, tier.tier_id);
            const after = resolve(withTier(persona, tier.tier_id, strengthened), tier.tier_id);
            for (const domain of SCORED_DOMAINS) {
              const b = before.ceilings[domain];
              const a = after.ceilings[domain];
              if (b === undefined || a === undefined) throw new Error(`${domain}: missing ceiling`);
              if (a < b) throw new Error(`${domain}: ceiling decreased from ${b} to ${a} after strengthening contract_terms.${flag}`);
            }
          });
        }
      }
    }
  }
});
