import { describe, it } from "vitest";

/**
 * I2 — No absent-party questions.
 *
 * No rendered question references a party or layer absent from the
 * persona's responsibility map. This is the primary defense against
 * irrelevant questions — the failure mode that sank the previous project
 * (see CLAUDE.md, Testing methodology).
 *
 * Implementation depends on: the master catalog with layer tagging
 * (Phase 3), the responsibility-map builder (Phase 4), and question
 * rendering (Phase 6). Runs against every approved persona.
 */
describe("I2: no rendered question references an absent party/layer", () => {
  it.todo(
    "for each approved persona tier, every disposition=assess control's layer exists in that tier's responsibility map",
  );
});
