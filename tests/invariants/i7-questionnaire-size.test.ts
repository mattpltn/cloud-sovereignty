import { describe, it } from "vitest";

/**
 * I7 — Questionnaire size sanity.
 *
 * The count of disposition=assess controls rendered per persona falls
 * within a declared band (e.g. 25-90). A count above the band signals
 * suppression/auto_answer logic is leaking questions that should have
 * been resolved automatically or excluded as not applicable.
 *
 * The exact band is a project-owner judgment set alongside Layer 2
 * spot-check assertions (Phase 4) — not hardcoded here. Implementation
 * depends on: the master catalog (Phase 3) and the disposition engine
 * (Phase 4).
 */
describe("I7: assessed-question count per persona stays within the declared band", () => {
  it.todo(
    "for each approved persona tier, the number of disposition=assess controls falls within that persona's declared [min, max] band",
  );
});
