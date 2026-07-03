// CSAT engine entry point. Same build runs in CI (via the Node test runner)
// and in the browser (design principle: "One engine, one language" —
// see CLAUDE.md, DECISIONS.md D-001). Responsibility-map building,
// disposition resolution and scoring are Phase 4/5 work; this stub exists
// so the Phase 1 test harness has a real module to import and type-check
// against.

export * from "./types.js";

import type { PersonaProfile, ResolvedControl } from "./types.js";

/**
 * Builds the responsibility map and resolves a disposition for every
 * catalog control, for one persona tier. Not implemented until Phase 4.
 */
export function resolveDispositions(
  _persona: PersonaProfile,
  _tierId: string,
): ResolvedControl[] {
  throw new Error("resolveDispositions is not implemented until Phase 4");
}
