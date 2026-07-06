// CSAT engine entry point. Same build runs in CI (via the Node test runner)
// and in the browser (design principle: "One engine, one language" —
// see CLAUDE.md, DECISIONS.md D-001). Responsibility-map building,
// disposition resolution and scoring are Phase 4/5 work; this stub exists
// so the Phase 1 test harness has a real module to import and type-check
// against.

export * from "./types.js";

import type { EngineResult, PersonaProfile } from "./types.js";

/**
 * Builds the responsibility map, resolves a disposition for every master
 * catalog control, and computes per-domain ceilings, for one persona tier.
 * Public API defined in Milestone 4a (types only); implemented in
 * Milestone 4d. See tests/assertions/layer2-spec.yaml (the owner-authored
 * Layer-2 specification this function must satisfy) and
 * tests/assertions/conversion-table.md.
 */
export function resolve(_persona: PersonaProfile, _tierId: string): EngineResult {
  throw new Error("resolve() is not implemented until Milestone 4d");
}
