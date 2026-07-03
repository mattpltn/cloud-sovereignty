import { describe, it } from "vitest";

/**
 * I6 — Monotonicity.
 *
 * Adding a strengthening modifier (e.g. HYOK, an audit-rights clause)
 * never lowers any score or ceiling for an approved persona tier; removing
 * one never raises them. Checked by programmatically toggling one modifier
 * at a time on an approved persona's tier and comparing resulting scores.
 *
 * Implementation depends on: scoring (Phase 5). Relates to, but is
 * distinct from, the hand-picked Layer 5 differential pairs (Phase 4+),
 * which assert specific deltas rather than general monotonicity.
 */
describe("I6: strengthening a modifier never lowers score/ceiling, and vice versa", () => {
  it.todo(
    "for each approved persona tier, toggling key_custody provider_held->hyok, or any contract_terms flag false->true, never decreases any domain's achieved score or ceiling; toggling the reverse never increases them",
  );
});
