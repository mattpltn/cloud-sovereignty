import { describe, it } from "vitest";

/**
 * I1 — Single disposition.
 *
 * Every catalog control resolves to exactly one disposition, for every
 * approved persona tier; zero unresolved, zero rule conflicts. Two
 * disposition rules firing for the same control with different
 * dispositions is a BUILD FAILURE, not silent precedence.
 *
 * Implementation depends on: the master catalog (Phase 3) and the
 * responsibility-map/disposition engine (Phase 4). Runs against every
 * approved persona via tests/helpers/personas.ts#loadApprovedPersonas.
 */
describe("I1: every control resolves to exactly one disposition", () => {
  it.todo(
    "for each approved persona tier, engine.resolveDispositions returns exactly one disposition per catalog control, with no conflicting rule matches",
  );
});
