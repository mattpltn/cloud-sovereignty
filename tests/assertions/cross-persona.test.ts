// Layer 5 — differential tests, converted from tests/assertions/layer2-spec.yaml's
// cross_persona group (X1a-X6). See reviews/layer2-assertions-owner-review.md
// and tests/assertions/conversion-table.md.
//
// Marked it.fails throughout (expected red) since resolve() throws until
// Milestone 4d — remove .fails there.

import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { ceiling, overallCeiling, SCORED_DOMAINS } from "../helpers/engine-assertions.js";
import { loadPersonaByShorthand } from "../helpers/personas.js";

const P1 = loadPersonaByShorthand("P1");
const P2 = loadPersonaByShorthand("P2");
const P3 = loadPersonaByShorthand("P3");
const P4 = loadPersonaByShorthand("P4");
const P5 = loadPersonaByShorthand("P5");
const P6 = loadPersonaByShorthand("P6");
const P7 = loadPersonaByShorthand("P7");
const P8 = loadPersonaByShorthand("P8");
const ALL = { P1, P2, P3, P4, P5, P6, P7, P8 };

// Every golden persona's "primary" tier for cross-persona ceiling
// comparisons — the tier named in each persona's own tiers list that
// isn't a second/mixed tier (P1 has two identical tiers; any resolves
// the same ceiling per D-... P1's own design intent. P8 has two
// different tiers and is compared via its own X5/P8-1 assertions, not here).
function primaryTier(persona: ReturnType<typeof loadPersonaByShorthand>) {
  return persona.tiers[0].tier_id;
}

describe("Layer 5 — cross-persona differentials (X-series)", () => {
  it.fails("X1a: overall_ceiling(P1) is the maximum among all personas", () => {
    const p1Ceiling = overallCeiling(resolve(P1, primaryTier(P1)));
    for (const [name, persona] of Object.entries(ALL)) {
      if (name === "P1") continue;
      const other = overallCeiling(resolve(persona, primaryTier(persona)));
      if (other > p1Ceiling) throw new Error(`${name}'s overall ceiling (${other}) exceeds P1's (${p1Ceiling})`);
    }
  });

  it.fails("X1b: overall_ceiling(P6) < overall_ceiling(p) for every other persona p", () => {
    const p6Ceiling = overallCeiling(resolve(P6, primaryTier(P6)));
    for (const [name, persona] of Object.entries(ALL)) {
      if (name === "P6") continue;
      const other = overallCeiling(resolve(persona, primaryTier(persona)));
      if (!(p6Ceiling < other)) throw new Error(`P6's overall ceiling (${p6Ceiling}) is not strictly less than ${name}'s (${other})`);
    }
  });

  it.fails("X1c: overall_ceiling(P4) > overall_ceiling(P5) (locality beats contracts)", () => {
    const p4 = overallCeiling(resolve(P4, primaryTier(P4)));
    const p5 = overallCeiling(resolve(P5, primaryTier(P5)));
    if (!(p4 > p5)) throw new Error(`P4's overall ceiling (${p4}) is not greater than P5's (${p5})`);
  });

  it.fails("X1d: overall_ceiling(P2) < overall_ceiling(P1) and overall_ceiling(P2) < overall_ceiling(P3)", () => {
    const p1 = overallCeiling(resolve(P1, primaryTier(P1)));
    const p2 = overallCeiling(resolve(P2, primaryTier(P2)));
    const p3 = overallCeiling(resolve(P3, primaryTier(P3)));
    if (!(p2 < p1)) throw new Error(`P2's overall ceiling (${p2}) is not less than P1's (${p1})`);
    if (!(p2 < p3)) throw new Error(`P2's overall ceiling (${p2}) is not less than P3's (${p3})`);
  });

  it.fails("X2: ceiling(P7,SOV-6) <= ceiling(P4,SOV-6) and <= ceiling(P2,SOV-6); all three < ceiling(P1,SOV-6)", () => {
    const p7 = ceiling(resolve(P7, primaryTier(P7)), "SOV-6");
    const p4 = ceiling(resolve(P4, primaryTier(P4)), "SOV-6");
    const p2 = ceiling(resolve(P2, primaryTier(P2)), "SOV-6");
    const p1 = ceiling(resolve(P1, primaryTier(P1)), "SOV-6");
    if (!(p7 <= p4)) throw new Error(`SOV-6: P7 (${p7}) not <= P4 (${p4})`);
    if (!(p7 <= p2)) throw new Error(`SOV-6: P7 (${p7}) not <= P2 (${p2})`);
    if (!(p7 < p1 && p4 < p1 && p2 < p1)) throw new Error(`SOV-6: P7/P4/P2 (${p7}/${p4}/${p2}) not all < P1 (${p1})`);
  });

  it.fails("X3: ceiling(P2,SOV-6) <= ceiling(P1,SOV-6) - 1 band; ceiling(P2,SOV-4) <= ceiling(P1,SOV-4) - 1 band", () => {
    const p1sov6 = ceiling(resolve(P1, primaryTier(P1)), "SOV-6");
    const p2sov6 = ceiling(resolve(P2, primaryTier(P2)), "SOV-6");
    const p1sov4 = ceiling(resolve(P1, primaryTier(P1)), "SOV-4");
    const p2sov4 = ceiling(resolve(P2, primaryTier(P2)), "SOV-4");
    if (!(p2sov6 <= p1sov6 - 1)) throw new Error(`SOV-6: P2 (${p2sov6}) not <= P1 (${p1sov6}) - 1 band`);
    if (!(p2sov4 <= p1sov4 - 1)) throw new Error(`SOV-4: P2 (${p2sov4}) not <= P1 (${p1sov4}) - 1 band`);
  });

  it.fails("X4: for every domain d, ceiling(P5,d) >= ceiling(P6,d); ceiling(P5,SOV-3) > ceiling(P6,SOV-3)", () => {
    const p5result = resolve(P5, primaryTier(P5));
    const p6result = resolve(P6, primaryTier(P6));
    for (const domain of SCORED_DOMAINS) {
      const p5c = ceiling(p5result, domain);
      const p6c = ceiling(p6result, domain);
      if (!(p5c >= p6c)) throw new Error(`${domain}: P5 (${p5c}) not >= P6 (${p6c})`);
    }
    const p5sov3 = ceiling(p5result, "SOV-3");
    const p6sov3 = ceiling(p6result, "SOV-3");
    if (!(p5sov3 > p6sov3)) throw new Error(`SOV-3: P5 (${p5sov3}) not strictly > P6 (${p6sov3})`);
  });

  it.fails("X5: P8.restricted engine output is identical to a standalone P1-class posture; P8.public identical to a standalone P6-class posture", () => {
    const p8Restricted = P8.tiers.find((t) => t.tier_id === "restricted");
    const p8Public = P8.tiers.find((t) => t.tier_id === "public");
    if (!p8Restricted || !p8Public) throw new Error("P8 must declare both a 'restricted' and a 'public' tier");

    const p8RestrictedResult = resolve(P8, "restricted");
    const p1Result = resolve(P1, primaryTier(P1));
    if (JSON.stringify(p8RestrictedResult) !== JSON.stringify(p1Result)) {
      throw new Error("P8.restricted output differs from the standalone P1-class posture output");
    }

    const p8PublicResult = resolve(P8, "public");
    const p6Result = resolve(P6, primaryTier(P6));
    if (JSON.stringify(p8PublicResult) !== JSON.stringify(p6Result)) {
      throw new Error("P8.public output differs from the standalone P6-class posture output");
    }
  });

  it.fails("X6: the applicable-criteria set at P1.secret is a strict superset-or-stricter of P1.internal", () => {
    const secretTier = P1.tiers.find((t) => t.tier_id === "secret");
    const internalTier = P1.tiers.find((t) => t.tier_id === "internal");
    if (!secretTier || !internalTier) throw new Error("P1 must declare both a 'secret' and an 'internal' tier");

    const secretResult = resolve(P1, "secret");
    const internalResult = resolve(P1, "internal");
    const secretIds = new Set(secretResult.dispositions.map((d) => d.control_id));
    const internalIds = new Set(internalResult.dispositions.map((d) => d.control_id));
    for (const id of internalIds) {
      if (!secretIds.has(id)) throw new Error(`${id}: applicable at P1.internal but not at P1.secret (should be a superset)`);
    }
    if (secretIds.size <= internalIds.size) {
      throw new Error(`P1.secret's applicable-criteria set (${secretIds.size}) is not strictly larger than P1.internal's (${internalIds.size})`);
    }
  });
});
