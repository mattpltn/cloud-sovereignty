import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import type { Disposition, Layer, SovDomain } from "../../engine/types.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..", "..");
const DATA_DIR = join(ROOT, "data");

interface RawControlRecord {
  id: string;
  sov_domain?: string;
  criterion_type?: string;
  layer?: string;
  disposition_default?: string;
  localization_level?: string;
  assurance_level?: string;
  addressed_party?: string;
}

interface CatalogEntryRaw {
  id: string;
  primary_id: string;
  primary_framework: string;
  sov_domains: string[];
  member_ids: string[];
}

/** One master-catalog entry, joined with metadata from its member records. */
export interface CatalogEntry {
  id: string; // e.g. "cat-0001"
  primary_id: string; // e.g. "csat-sov4-01-c1" — the control_id the engine's EngineResult uses
  sov_domains: SovDomain[];
  member_ids: string[];
  // Metadata is drawn from the PRIMARY member's own record (the one C3A/
  // ECSF/CADA record chosen as primary_id), since that's what the engine
  // resolves a single disposition against.
  layer?: Layer;
  criterion_type?: string;
  disposition_default?: Disposition;
  localization_level?: "C1" | "C2";
  assurance_level?: "UA-1" | "UA-2" | "UA-3" | "UA-4";
  addressed_party: "provider" | "government_self";
}

function loadRawRecords(): Map<string, RawControlRecord> {
  const byId = new Map<string, RawControlRecord>();
  for (const file of ["c3a.json", "ecsf.json", "cada.json"]) {
    const records: RawControlRecord[] = JSON.parse(readFileSync(join(DATA_DIR, "extracted", file), "utf8"));
    for (const r of records) byId.set(r.id, r);
  }
  // cada-act.json's government_self-tagged records are catalog members too
  // (D-030) but don't conform to control-record.schema.json (D-017) — no
  // layer/criterion_type/localization_level/assurance_level, just an id and
  // addressed_party.
  const cadaAct: (RawControlRecord & { addressed_party?: string })[] = JSON.parse(
    readFileSync(join(DATA_DIR, "extracted", "cada-act.json"), "utf8"),
  );
  for (const r of cadaAct) {
    if (r.addressed_party === "government_self") byId.set(r.id, r);
  }
  return byId;
}

let cachedEntries: CatalogEntry[] | undefined;

/** Loads all master-catalog entries (data/catalog/catalog.json), joined with their primary member's control metadata. */
export function loadCatalog(): CatalogEntry[] {
  if (cachedEntries) return cachedEntries;
  const raw: { entries: CatalogEntryRaw[] } = JSON.parse(readFileSync(join(DATA_DIR, "catalog", "catalog.json"), "utf8"));
  const records = loadRawRecords();

  cachedEntries = raw.entries.map((e) => {
    const primary = records.get(e.primary_id);
    return {
      id: e.id,
      primary_id: e.primary_id,
      sov_domains: e.sov_domains as SovDomain[],
      member_ids: e.member_ids,
      layer: primary?.layer as Layer | undefined,
      criterion_type: primary?.criterion_type,
      disposition_default: primary?.disposition_default as Disposition | undefined,
      localization_level: primary?.localization_level as "C1" | "C2" | undefined,
      assurance_level: primary?.assurance_level as "UA-1" | "UA-2" | "UA-3" | "UA-4" | undefined,
      addressed_party: (primary?.addressed_party as "government_self" | undefined) ?? "provider",
    };
  });
  return cachedEntries;
}

/** Finds a catalog entry by its primary_id (the engine's control_id). */
export function findControl(primaryId: string): CatalogEntry {
  const entry = loadCatalog().find((e) => e.primary_id === primaryId);
  if (!entry) throw new Error(`No catalog entry with primary_id ${primaryId}`);
  return entry;
}

/** All catalog entries for a given SOV domain. */
export function controlsInDomain(domain: SovDomain): CatalogEntry[] {
  return loadCatalog().filter((e) => e.sov_domains.includes(domain));
}
