// Named lookup table mapping the Layer-2 spec's prose control-class
// references (e.g. "C3A SOV-6-01 class", "external-key-management
// control") to concrete master-catalog primary_ids. This IS the
// "interpretation made" record required alongside
// tests/assertions/conversion-table.md — every non-obvious binding here
// is also noted in that table against the assertion(s) that use it.
//
// Refined for API shape (control_id binding), never weakened: each
// mapping targets the catalog entry that most literally matches the
// spec's own wording, verified against data/catalog/catalog.json and the
// underlying c3a.json/ecsf.json/cada.json text (see conversion-table.md
// for the verification note per id).

export const CONTROL_REFS = {
  // P1-4: "C3A SOV-1-04-class (change-of-control notification) suppressed: no self-analog"
  CHANGE_OF_CONTROL_NOTIFICATION: "csat-sov1-04-c",

  // P1-5, P3-3, P5-1, P6-2, P7-3: "external-key-management control"
  // csat-sov3-02-c and -ac (SaaS-scope extension) are one catalog entry
  // (cat-0031), primary_id csat-sov3-02-ac.
  EXTERNAL_KEY_MANAGEMENT: "csat-sov3-02-ac",

  // P2-1: "SOV-6 source-code-availability class (C3A SOV-6-01)"
  SOURCE_CODE_AVAILABILITY: "csat-sov6-01-c",

  // P2-6: "update/patch-channel controls (C3A SOV-4-05/SOV-4-09 class)"
  UPDATE_PATCH_CHANNEL: ["csat-sov4-05-c", "csat-sov4-05-ac1", "csat-sov4-05-ac2", "csat-sov4-09-c", "csat-sov4-09-ac"],

  // P4-1, P5-3, P6-1: "provider-jurisdiction controls" / "jurisdiction-class controls"
  PROVIDER_JURISDICTION: ["csat-sov1-01-c1", "csat-sov1-01-c2"],

  // P5-2: "data-residency controls" — the C1/C2 pair (D-032 fixed the
  // catalog so these are two separately-disposable entries).
  DATA_RESIDENCY_TRUSTED_REGION: "csat-sov3-01-c3", // C1
  DATA_RESIDENCY_NATION: "csat-sov3-01-c4", // C2

  // P1-2: "SBOM/software-dependency control"
  SBOM_SOFTWARE_DEPENDENCY: "csat-sov5-01-c",

  // P7-6: "effective-control controls (C3A SOV-1-03 class)"
  EFFECTIVE_CONTROL: ["csat-sov1-03-c1", "csat-sov1-03-c2"],
} as const;
