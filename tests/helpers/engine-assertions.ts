// Shared query helpers over EngineResult, used across the Layer-2/Layer-5
// executable tests (Milestone 4a). These are thin, deliberately
// non-clever wrappers — the interpretive work (which domains count
// toward "overall", how ceiling bands compare) is documented here once
// so every test applies it consistently, and so tests/assertions/conversion-table.md
// can point at a single place rather than re-explaining it per assertion.

import type { EngineResult, SovDomain } from "../../engine/types.js";

// The Layer-2 spec's meta.ceiling_scale is "ordinal maturity bands 0-4
// per SOV domain". SOV-7 is inheritance-only (no maturity progression —
// see D-031) and is excluded from every ceiling ladder Phase 3 built
// (data/catalog/ladders.json covers SOV-1..6 only), so "overall" ceiling
// comparisons are computed over SOV-1..6.
export const SCORED_DOMAINS: SovDomain[] = ["SOV-1", "SOV-2", "SOV-3", "SOV-4", "SOV-5", "SOV-6"];

/**
 * "Overall" ceiling under an equal_weights profile (per the spec's own
 * meta note): the arithmetic mean of the six SOV-1..6 domain ceilings.
 * This is the simplest structural combination consistent with
 * "equal_weights... to isolate posture effects" and does not anticipate
 * Phase 5's outcome-derived weighting — it is a Phase-4-only structural
 * comparison basis for the cross_persona (X-series) assertions.
 */
export function overallCeiling(result: EngineResult): number {
  const values = SCORED_DOMAINS.map((d) => result.ceilings[d]);
  if (values.some((v) => v === undefined)) {
    throw new Error(`overallCeiling: missing ceiling for one or more of ${SCORED_DOMAINS.join(", ")}`);
  }
  const nums = values as number[];
  return nums.reduce((a, b) => a + b, 0) / nums.length;
}

export function ceiling(result: EngineResult, domain: SovDomain): number {
  const v = result.ceilings[domain];
  if (v === undefined) throw new Error(`ceiling: no ceiling recorded for ${domain}`);
  return v;
}

export function questionCount(result: EngineResult): number {
  return result.question_set.length;
}

export function negotiationCount(result: EngineResult): number {
  return result.negotiation_flags.length;
}

export function dispositionOf(result: EngineResult, controlId: string) {
  const entry = result.dispositions.find((d) => d.control_id === controlId);
  if (!entry) throw new Error(`dispositionOf: no resolved disposition for ${controlId}`);
  return entry;
}

export function autoAnswerOf(result: EngineResult, controlId: string) {
  const entry = result.auto_answers.find((a) => a.control_id === controlId);
  if (!entry) throw new Error(`autoAnswerOf: no auto_answer for ${controlId}`);
  return entry;
}

/** True iff at least one of the given control_ids resolved to disposition=assess. */
export function anyAssessed(result: EngineResult, controlIds: string[]): boolean {
  return controlIds.some((id) => result.dispositions.some((d) => d.control_id === id && d.disposition === "assess"));
}
