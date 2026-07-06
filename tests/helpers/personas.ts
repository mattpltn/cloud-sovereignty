import { readFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import yaml from "js-yaml";
import type { PersonaProfile } from "../../engine/types.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const PERSONAS_DIR = join(__dirname, "..", "personas");

export type PersonaShorthand = "P1" | "P2" | "P3" | "P4" | "P5" | "P6" | "P7" | "P8";

/**
 * Loads a golden persona by its P1-P8 shorthand (tests/assertions/layer2-spec.yaml's
 * group keys), via the tests/personas/p<N>-<slug>.yaml filename convention —
 * the same convention scripts/validate.py's check_layer2_spec() uses, so the
 * two never drift independently.
 */
export function loadPersonaByShorthand(shorthand: PersonaShorthand): PersonaProfile {
  const n = shorthand.slice(1);
  const files = readdirSync(PERSONAS_DIR).filter((f) => f.startsWith(`p${n}-`));
  if (files.length !== 1) {
    throw new Error(`Expected exactly one persona fixture matching p${n}-*, found ${files.length}`);
  }
  return yaml.load(readFileSync(join(PERSONAS_DIR, files[0]), "utf8")) as PersonaProfile;
}

/** Loads every persona fixture, draft or approved. */
export function loadAllPersonas(): PersonaProfile[] {
  return readdirSync(PERSONAS_DIR)
    .filter((f) => f.endsWith(".yaml"))
    .map((f) => yaml.load(readFileSync(join(PERSONAS_DIR, f), "utf8")) as PersonaProfile);
}

/**
 * The approval-gate predicate itself, exported separately from
 * loadApprovedPersonas so tests can exercise it against synthetic
 * fixtures (e.g. a draft persona not present under tests/personas/)
 * without depending on the real golden-persona set ever containing a
 * draft to prove exclusion against.
 */
export function filterApproved(personas: PersonaProfile[]): PersonaProfile[] {
  return personas.filter((p) => p.status === "approved");
}

/**
 * Loads only personas with status: approved. Per the persona ownership
 * workflow (CLAUDE.md), the test runner MUST refuse to execute engine
 * tests against any persona not marked approved — this is that gate.
 */
export function loadApprovedPersonas(): PersonaProfile[] {
  return filterApproved(loadAllPersonas());
}
