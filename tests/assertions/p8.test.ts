// Layer 2 — persona spot-checks, converted from tests/assertions/layer2-spec.yaml's
// P8 group (mixed estate — consistency vehicle). See
// reviews/layer2-assertions-owner-review.md and
// tests/assertions/conversion-table.md. P8-1 duplicates X5 exactly (the
// spec itself cross-references X5) — kept as its own test per the "every
// executable test cites its spec id" rule rather than only asserting it
// once under X5.
//
// Marked it.fails throughout (expected red) since resolve() throws until
// Milestone 4d — remove .fails there.

import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { questionCount } from "../helpers/engine-assertions.js";
import { loadPersonaByShorthand } from "../helpers/personas.js";

const P1 = loadPersonaByShorthand("P1");
const P6 = loadPersonaByShorthand("P6");
const P8 = loadPersonaByShorthand("P8");

describe("Layer 2 — P8 (mixed estate — consistency vehicle)", () => {
  it.fails("P8-1: restricted-tier output identical to the P1-class posture output (X5); public-tier identical to P6-class posture output", () => {
    const restricted = resolve(P8, "restricted");
    const p1 = resolve(P1, P1.tiers[0].tier_id);
    if (JSON.stringify(restricted) !== JSON.stringify(p1)) throw new Error("P8.restricted output differs from the standalone P1-class posture output");

    const publicTier = resolve(P8, "public");
    const p6 = resolve(P6, P6.tiers[0].tier_id);
    if (JSON.stringify(publicTier) !== JSON.stringify(p6)) throw new Error("P8.public output differs from the standalone P6-class posture output");
  });

  it.fails("P8-2: combined report presents both tiers separately with per-tier ceilings; no cross-tier averaging in the posture profile", () => {
    // The Phase 4 API returns one EngineResult per (persona, tierId) call —
    // there is no combined/averaged multi-tier result type at all, which is
    // itself the structural guarantee against cross-tier averaging. This
    // assertion checks that the two tiers' ceilings are NOT required to
    // match (i.e. resolve() is genuinely called per-tier, not once for a
    // blended estate).
    const restricted = resolve(P8, "restricted");
    const publicTier = resolve(P8, "public");
    if (JSON.stringify(restricted.ceilings) === JSON.stringify(publicTier.ceilings) && P8.tiers.length > 1) {
      throw new Error("restricted and public tier ceilings are identical — suspicious for two genuinely different postures (A1 vs A4 SaaS)");
    }
  });

  it.fails("P8-3: asked-question count = sum of the applicable per-tier bands", () => {
    const restricted = resolve(P8, "restricted");
    const publicTier = resolve(P8, "public");
    const total = questionCount(restricted) + questionCount(publicTier);
    // P1-class band [50,90] + P6-class band [15,50] per I7's bands.
    if (total < 50 + 15 || total > 90 + 50) {
      throw new Error(`combined assess count ${total} outside the sum of P1-class [50,90] and P6-class [15,50] bands`);
    }
  });
});
