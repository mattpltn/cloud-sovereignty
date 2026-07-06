// Layer 2 — persona spot-checks, converted from tests/assertions/layer2-spec.yaml's
// P2 group (the trap case). See reviews/layer2-assertions-owner-review.md
// and tests/assertions/conversion-table.md.
//
// Marked it.fails throughout (expected red) since resolve() throws until
// Milestone 4d — remove .fails there.

import { describe, it } from "vitest";
import { resolve } from "../../engine/index.js";
import { CONTROL_REFS } from "../helpers/control-refs.js";
import { dispositionOf, negotiationCount, questionCount } from "../helpers/engine-assertions.js";
import { loadPersonaByShorthand } from "../helpers/personas.js";

const P2 = loadPersonaByShorthand("P2");
const TIER = P2.tiers[0].tier_id;

describe("Layer 2 — P2 (gov DC, closed stack, local-integrator ops — the trap case)", () => {
  it.fails("P2-1: SOV-6 source-code-availability class (C3A SOV-6-01) auto_answer not-met + negotiation_opportunity", () => {
    const result = resolve(P2, TIER);
    const d = dispositionOf(result, CONTROL_REFS.SOURCE_CODE_AVAILABILITY);
    if (d.disposition !== "auto_answer") throw new Error(`expected disposition=auto_answer, got ${d.disposition}`);
    if (!d.negotiation_opportunity) throw new Error("expected negotiation_opportunity=true");
  });

  it.fails("P2-2: operations wording variant = integrator phrasing; facility wording = self", () => {
    const result = resolve(P2, TIER);
    // Spot-checked via the update/patch-channel controls (operations layer)
    // and the change-of-control-class control (facility/legal layer proxy
    // for "the facility itself is self-run").
    const opsControls = CONTROL_REFS.UPDATE_PATCH_CHANNEL;
    for (const id of opsControls) {
      const d = dispositionOf(result, id);
      if (d.disposition === "assess" && d.wording_variant !== "integrator") {
        throw new Error(`${id}: expected wording_variant=integrator for an assessed ops-layer control, got ${d.wording_variant}`);
      }
    }
  });

  it.fails("P2-3: extraterritorial/legal controls assess or auto_answer not-met — never suppressed", () => {
    const result = resolve(P2, TIER);
    const d = dispositionOf(result, CONTROL_REFS.PROVIDER_JURISDICTION[0]);
    if (d.disposition === "suppress") throw new Error("extraterritorial/legal control must not be suppressed for P2 (vendor tech-channel exposure exists)");
  });

  it.fails("P2-4: negotiation-flagged controls >= 3 (audit rights, exit/reversibility, escrow class)", () => {
    const result = resolve(P2, TIER);
    if (negotiationCount(result) < 3) throw new Error(`expected >= 3 negotiation flags, got ${negotiationCount(result)}`);
  });

  it.fails("P2-5: asked-question count in [40,80]", () => {
    const result = resolve(P2, TIER);
    const count = questionCount(result);
    if (count < 40 || count > 80) throw new Error(`assess count ${count} outside [40,80]`);
  });

  it.fails("P2-6: update/patch-channel controls (C3A SOV-4-05/SOV-4-09 class) assess with vendor-dependency wording, not suppressed", () => {
    const result = resolve(P2, TIER);
    for (const id of CONTROL_REFS.UPDATE_PATCH_CHANNEL) {
      const d = dispositionOf(result, id);
      if (d.disposition === "suppress") throw new Error(`${id}: must not be suppressed (vendor update/patch channel is a real dependency for P2)`);
    }
  });
});
