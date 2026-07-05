## 1. Owner-review decision record (commit as reviews/persona-owner-review.md)

Conducted as a structured interview between the project owner and the external reviewer, 2026-07-04. Decisions:

1. **Key custody convention (P1, P3, P8-restricted):** new modifier value `government_held` replaces the `external_hsm` interpretation for government-operated clouds — keys held in government-operated hardware, no third party. Requires persona-schema enum addition.
2. **P1:** assess two tiers (secret + internal, same posture) to exercise tier-sensitivity of scoring; priorities reordered — protection_from_foreign_legal_access now ranks first, continuity second.
3. **P2:** contract terms confirmed realistic as drafted (no audit, no escrow, no exit, residency committed). Ops model corrected per field experience: day-to-day operations run by an **independent local systems integrator** on the closed vendor stack ({NATION} jurisdiction) — the extraterritorial vector is the vendor technology/support/licensing channel, not foreign personnel. This sharpens the trap case: domestic facility AND domestic staff, still must not score sovereign.
4. **P3:** foreign-owned in-country colo confirmed (sharper test of the parent-company legal vector); key custody → government_held per convention.
5. **P4:** re-modeled per field reality — local CSPs typically run Huawei Cloud, Mirantis, Virtuozzo, or sometimes OpenStack. Fixture models the closed foreign platform (Huawei Cloud) as the modal case; `extraterritorial_law_exposure` flips to true (vector: the foreign platform); a hypothetical clean-domestic variant may be added later as a differential fixture. New `provider_stack` modifier required in the persona schema.
6. **P5:** facility placement kept at {TRUSTED_REGION} (country-dependent in reality; in-country local zones are a runtime variant, noted in comment). **Escrow set to false** based on market research: source-code escrow is not realistically obtainable for hyperscaler platforms; a genuine escrow market exists for ISV/SaaS applications and closed-vendor stacks (DORA/NIS2-driven) — routed to the Phase 6 clause library instead (escrow = negotiable for P2-type vendor deals and SaaS vendors, not hyperscaler platform contracts).
7. **P6, P7:** confirmed as drafted (P7's local telco/SI partner model matches observed deals).
8. **P8:** confirmed as drafted; P1 conventions flow into its restricted tier.

Approval: upon application of these amendments, the owner authorizes status → approved on all 8 files.
