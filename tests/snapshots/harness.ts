// Layer 3 — snapshot harness (Milestone 4a: harness only, no baselines
// committed yet — see CLAUDE.md's Layer 3 testing methodology section).
// Baselines are generated and committed in Milestone 4d, once resolve()
// is implemented and Layers 1/2/5 are green; each baseline generation is
// itself a reviewed artifact (flagged for external review in the Phase 4
// report), and re-baselining afterward requires human review of the
// diff + a /reviews note + a `rebaseline: <persona> — <reason>` commit
// message (CLAUDE.md, Layer 3).

import { resolve } from "../../engine/index.js";
import type { EngineResult, PersonaProfile } from "../../engine/types.js";

/** One persona's full engine output across every tier it declares — the unit CI diffs against a committed baseline. */
export interface PersonaSnapshot {
  persona_id: string;
  tiers: Record<string, EngineResult>;
}

/**
 * Builds the full, deterministic snapshot for one persona: every tier's
 * complete EngineResult (dispositions, auto_answers, ceilings,
 * negotiation_flags, question_set). Pure function of (persona) via
 * resolve() — no I/O beyond what resolve() itself does.
 */
export function buildSnapshot(persona: PersonaProfile): PersonaSnapshot {
  const tiers: Record<string, EngineResult> = {};
  for (const tier of persona.tiers) {
    tiers[tier.tier_id] = resolve(persona, tier.tier_id);
  }
  return { persona_id: persona.persona_id, tiers };
}

/** Canonical JSON serialization for baseline files — stable key order via JSON.stringify's own object-key insertion order, 2-space indent, trailing newline. */
export function serializeSnapshot(snapshot: PersonaSnapshot): string {
  return JSON.stringify(snapshot, null, 2) + "\n";
}
