import { describe, it } from "vitest";

/**
 * I4 — Score bounds and renormalization.
 *
 * achieved <= ceiling <= 100 in every SOV domain, for every workload tier.
 * Suppressed controls contribute zero weight, and remaining weights
 * renormalize so the domain still sums to 100% ceiling potential.
 *
 * Implementation depends on: scoring (Phase 5). Runs against every
 * approved persona and every domain/tier combination it declares.
 */
describe("I4: achieved <= ceiling <= 100, weights renormalize around suppression", () => {
  it.todo(
    "for each approved persona tier and each SOV domain, 0 <= achieved <= ceiling <= 100, and suppressed-control weight is excluded with the remainder renormalized to 100%",
  );
});
