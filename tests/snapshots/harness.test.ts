// Layer 3 — snapshot harness smoke test (Milestone 4a). No baselines are
// committed yet (CLAUDE.md: baselines are generated in Milestone 4d and
// are themselves a reviewed artifact). This only proves the harness code
// itself is wired correctly against the Milestone 4a API — it does not,
// and cannot yet, diff against a committed baseline.

import { describe, it } from "vitest";
import { loadApprovedPersonas } from "../helpers/personas.js";
import { buildSnapshot, serializeSnapshot } from "./harness.js";

describe("Layer 3 harness (no baselines yet)", () => {
  for (const persona of loadApprovedPersonas()) {
    it.fails(`${persona.persona_id}: buildSnapshot produces a serializable snapshot`, () => {
      const snapshot = buildSnapshot(persona);
      const serialized = serializeSnapshot(snapshot);
      if (!serialized.startsWith("{")) throw new Error("serializeSnapshot did not produce JSON");
    });
  }

  it.todo(
    "commit the first Layer-3 baseline snapshots for all 8 personas under tests/snapshots/*.json once resolve() is implemented (Milestone 4d) — flag the initial baseline generation for external review in the Phase 4 report, per CLAUDE.md's Layer 3 re-baseline discipline",
  );
});
