#!/usr/bin/env python3
"""Phase 2a: BSI C3A v1.0 extraction into /data/extracted/c3a.json.

Source: sources/C3A_Cloud_Computing_Autonomy.pdf (git-ignored locally per
docs/DECISIONS.md D-002). Text below was captured verbatim from that PDF
(via pypdf) and transcribed by hand into this script, criterion by
criterion, cross-checked against the extracted text.

Methodology (see docs/METHODOLOGY.md Phase 2a section for the full writeup):
- Every criterion (C) and additional criterion (AC) is captured, one
  record per document, based on the explicit "Criterion" / "Additional
  criterion" label following each ID in the source (NOT inferred from the
  ID's own suffix letter — SOV-4-01-C3 is labelled "Additional criterion"
  despite its "C3" suffix, so it is extracted as criterion_type: AC).
- "Supplementary information" (SI) blocks are not extracted as separate
  control records (out of scope for this phase; schema has no SI
  criterion_type). Their content is not reproduced elsewhere either.
- derivation: verbatim for every record — no generalization, no
  {NATION}/{TRUSTED_REGION} substitution. That is Phase 2d.
- localization_level (C1=EU / C2=Germany) is set ONLY where the source
  presents a genuine paired EU-vs-Germany variant of the identical
  requirement (same subject/scope, differing only in jurisdiction).
  Criteria that merely mention "EU" or "Germany" without a paired
  counterpart of the same requirement are left untagged, because the
  schema's C1/C2 values model paired localization variants specifically,
  not "does the EU appear in this text."
- fr text is not machine-translated (would create a derivative under
  C3A's CC-BY-ND license — see docs/DECISIONS.md D-005); the literal
  placeholder "FR-TRANSLATION-PENDING" is used instead, in both
  source_text.fr and generalized_text.fr.
- layer is a best-effort mapping to the responsibility-map layer enum;
  needs_review is set with a note wherever the mapping isn't a clean fit,
  per CLAUDE.md working rule 2 ("never guess").
- weight is uniformly 1.0 and evidence_quality_options is the full set of
  four tiers for every record — both are Phase 5 scoring concerns, not
  decided here.
- disposition_default is uniformly "assess" — actual scenario-dependent
  dispositions are Phase 4 rule work.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "extracted" / "c3a.json"
VERBATIM_OUT = ROOT / "data" / "local" / "c3a-verbatim.json"

DOCUMENT = "BSI C3A v1.0 (27.04.2026)"
FR_PENDING = "FR-TRANSLATION-PENDING"
LOCAL_VERBATIM_PLACEHOLDER = "SEE-LOCAL-VERBATIM"
GENERALIZATION_PENDING_PLACEHOLDER = "GENERALIZATION-PENDING"
ALL_EVIDENCE = ["self_attested", "contractual_commitment", "third_party_certified", "independently_audited"]


def rec(id_suffix, sov_domain, section_id, criterion_type, layer, page, text_en,
        localization_level=None, needs_review=False, needs_review_note=None):
    r = {
        "id": f"csat-{id_suffix}",
        "sov_domain": sov_domain,
        "criterion_type": criterion_type,
        "layer": layer,
        "derivation": "verbatim",
        "source_refs": [{"framework": "C3A", "section_id": section_id}],
        "source_pointer": {"document": DOCUMENT, "section": section_id, "page": page},
        "source_text": {"en": text_en, "fr": FR_PENDING},
        "generalized_text": {"en": text_en, "fr": FR_PENDING},
        "disposition_default": "assess",
        "evidence_quality_options": ALL_EVIDENCE,
        "weight": 1.0,
        "needs_review": needs_review,
    }
    if localization_level:
        r["localization_level"] = localization_level
    if needs_review_note:
        r["needs_review_note"] = needs_review_note
    return r


SOV1 = [
    rec("sov1-01-c1", "SOV-1", "SOV-1-01-C1", "C", "legal_jurisdiction", 7,
        "The cloud service provider MUST operate under EU jurisdiction, with contract governance and dispute resolution.",
        localization_level="C1"),
    rec("sov1-01-c2", "SOV-1", "SOV-1-01-C2", "C", "legal_jurisdiction", 7,
        "The cloud service provider MUST operate under German jurisdiction, with contract governance and dispute resolution.",
        localization_level="C2"),
    rec("sov1-02-c1", "SOV-1", "SOV-1-02-C1", "C", "legal_jurisdiction", 7,
        "The cloud service provider MUST have a registered head office in the EU.",
        localization_level="C1"),
    rec("sov1-02-c2", "SOV-1", "SOV-1-02-C2", "C", "legal_jurisdiction", 7,
        "The cloud service provider MUST have a registered head office in Germany.",
        localization_level="C2"),
    rec("sov1-03-c1", "SOV-1", "SOV-1-03-C1", "C", "legal_jurisdiction", 7,
        "The cloud service provider MUST be effectively controlled by one or more EU corporations. "
        "The cloud service provider MUST ensure that effective controls are transparent to cloud service customers.",
        localization_level="C1"),
    rec("sov1-03-c2", "SOV-1", "SOV-1-03-C2", "C", "legal_jurisdiction", 7,
        "The cloud service provider MUST be under the effective control of one or more German undertakings. "
        "The cloud service provider MUST ensure that effective controls are transparent to cloud service customers.",
        localization_level="C2"),
    rec("sov1-04-c", "SOV-1", "SOV-1-04-C", "C", "legal_jurisdiction", 8,
        "The cloud service provider MUST inform cloud service customers 90 days in advance of any actual changes "
        "affecting the cloud service provider's control that could undermine or affect the C3A controls associated "
        "with the cloud service, including significant changes to ownership, shareholding, or governance "
        "relationships of the cloud service provider."),
]

SOV2 = [
    rec("sov2-01-c", "SOV-2", "SOV-2-01-C", "C", "legal_jurisdiction", 8,
        "The cloud service provider MUST identify, at least once a year, any non-EU law relating directly to the "
        "provided cloud services that have cross-border implications for the availability of cloud services and the "
        "confidentiality and integrity of customer created data. They MUST also carry out a structured risk "
        "assessment to evaluate the risks arising from these laws."),
    rec("sov2-02-c1", "SOV-2", "SOV-2-02-C1", "C", "legal_jurisdiction", 8,
        "The cloud service provider MUST document procedures that allow the relevant federal or national "
        "cybersecurity authority to verify compliance with the C3A criteria by an audit. The responsible authority is "
        "the one in the country where the data center is located.",
        localization_level="C1"),
    rec("sov2-02-c2", "SOV-2", "SOV-2-02-C2", "C", "legal_jurisdiction", 8,
        "The cloud service provider MUST document procedures that allow the German federal administration to "
        "verify compliance with the C3A criteria by an audit.",
        localization_level="C2"),
    rec("sov2-03-c1", "SOV-2", "SOV-2-03-C1", "C", "legal_jurisdiction", 8,
        "If an EU member state declares a state of defense, the cloud service provider MUST enable the EU member "
        "state to take over the capabilities required to operate the cloud, including the necessary physical assets and "
        "personnel, within the framework of legal possibilities.",
        localization_level="C1", needs_review=True,
        needs_review_note="Spans legal_jurisdiction (the right to take over), facility (physical assets), and "
                           "operations_personnel (personnel handover); tagged legal_jurisdiction as the primary "
                           "overarching obligation since the requirement is fundamentally a legal enablement duty. "
                           "Review whether Phase 4's disposition rules need a multi-layer treatment instead."),
    rec("sov2-03-c2", "SOV-2", "SOV-2-03-C2", "C", "legal_jurisdiction", 9,
        "If Germany declares a state of defense, the cloud service provider MUST enable the German federal "
        "administration to take over the capabilities required to operate the cloud, including the necessary material "
        "assets and personnel, within the framework of legal possibilities.",
        localization_level="C2", needs_review=True,
        needs_review_note="Same multi-layer concern as SOV-2-03-C1 (legal_jurisdiction / facility / "
                           "operations_personnel); tagged legal_jurisdiction as primary."),
]

SOV3 = [
    rec("sov3-01-c1", "SOV-3", "SOV-3-01-C1", "C", "data", 9,
        "A cloud service customer MUST be able to check where their cloud service derived data, cloud service "
        "customer data, and account data are stored and processed."),
    rec("sov3-01-c2", "SOV-3", "SOV-3-01-C2", "C", "data", 9,
        "The cloud service provider MUST provide a service option where cloud service derived data and account "
        "data are exclusively stored and processed in the EU."),
    rec("sov3-01-c3", "SOV-3", "SOV-3-01-C3", "C", "data", 9,
        "The cloud service provider MUST provide a service option where cloud service customer data is exclusively "
        "stored and processed in the EU.",
        localization_level="C1"),
    rec("sov3-01-c4", "SOV-3", "SOV-3-01-C4", "C", "data", 9,
        "The cloud service provider MUST provide a service option where cloud service customer data is exclusively "
        "stored and processed in Germany.",
        localization_level="C2"),
    rec("sov3-01-c5", "SOV-3", "SOV-3-01-C5", "C", "data", 9,
        "The cloud service provider MUST provide a service option where cloud service provider data is exclusively "
        "stored and processed in the EU."),
    rec("sov3-02-c", "SOV-3", "SOV-3-02-C", "C", "data", 9,
        "The cloud service provider MUST allow the integration of external encryption key management system for "
        "creating, managing, and storing encryption keys outside of the cloud service provider environment for the "
        "use of IaaS and PaaS, or provide functionally equivalent mechanisms that ensure the customer can only "
        "create, manage and store the encryption keys only outside of the cloud service provider environment."),
    rec("sov3-02-ac", "SOV-3", "SOV-3-02-AC", "AC", "data", 9,
        "The cloud service provider MUST allow the integration of external key management systems for creating, "
        "managing and storing keys outside of the cloud environment also for SaaS, or provide functionally "
        "equivalent mechanisms that ensure the customer can only create, manage and store the encryption keys "
        "outside of the cloud service provider environment."),
    rec("sov3-03-c", "SOV-3", "SOV-3-03-C", "C", "identity", 10,
        "The cloud service provider MUST support standards-based integration of external identity providers for "
        "authentication and access management for the cloud service."),
    rec("sov3-03-ac1", "SOV-3", "SOV-3-03-AC1", "AC", "identity", 10,
        "The integration of an external Identity Provider MUST be implemented via open, non-proprietary "
        "standards."),
    rec("sov3-03-ac2", "SOV-3", "SOV-3-03-AC2", "AC", "identity", 10,
        "The provider MUST support a stateless authentication model that does not mandate the creation and copies "
        "of accounts within the provider's directory."),
    rec("sov3-03-ac3", "SOV-3", "SOV-3-03-AC3", "AC", "identity", 10,
        "Authorization MUST be controllable via dynamic claims and attributes issued directly by the customer's "
        "external identity provider."),
    rec("sov3-04-c", "SOV-3", "SOV-3-04-C", "C", "data", 10,
        "The cloud service provider MUST provide customers with the capability to record, retain, and review logs of "
        "management and data access activities related to cloud service customer data. These logs MUST enable "
        "customers to identify when access occurred, the identity associated with the request, and the relevant "
        "operational context available through the service's logging capabilities.",
        needs_review=True,
        needs_review_note="Logging capability spans data (records of data-access activity) and platform/"
                           "operations_personnel (who/what performs and hosts the logging); tagged data as the "
                           "closest fit since the criterion centers on data-access accountability."),
    rec("sov3-04-ac1", "SOV-3", "SOV-3-04-AC1", "AC", "data", 10,
        "The logging service MUST ensure full data flow transparency by providing real-time access via standardized "
        "open-source APIs.",
        needs_review=True,
        needs_review_note="Same data/platform ambiguity as SOV-3-04-C."),
    rec("sov3-04-ac2", "SOV-3", "SOV-3-04-AC2", "AC", "data", 10,
        "The service MUST support granular filtering.",
        needs_review=True,
        needs_review_note="Same data/platform ambiguity as SOV-3-04-C."),
    rec("sov3-05-c", "SOV-3", "SOV-3-05-C", "C", "data", 10,
        "The cloud service provider MUST enable client-side encryption of cloud service customer data. Whenever "
        "the cloud service customer data is transmitted, processed or stored inside the cloud environment, it MUST "
        "be encrypted with a private key that is only available to the cloud service customer outside of the cloud "
        "service provider environment."),
]

SOV4 = [
    rec("sov4-01-c1", "SOV-4", "SOV-4-01-C1", "C", "operations_personnel", 11,
        "All personnel who have logical or physical access to infrastructure used to operate the cloud service, as well "
        "as those who are responsible for customer support, and all persons who have management control of the "
        "cloud service provider MUST be EU citizens with EU as main residency.",
        localization_level="C1"),
    rec("sov4-01-c2", "SOV-4", "SOV-4-01-C2", "C", "operations_personnel", 11,
        "All personnel who have logical or physical access to infrastructure used to operate the cloud service, as well "
        "as those who are responsible for customer support, and all persons who have management control of the "
        "cloud service provider MUST be EU citizens with Germany as main residency.",
        localization_level="C2"),
    rec("sov4-01-c3", "SOV-4", "SOV-4-01-C3", "AC", "operations_personnel", 11,
        "The operating personnel is part of an organization that MUST be a standalone European organization."),
    rec("sov4-02-c1", "SOV-4", "SOV-4-02-C1", "C", "operations_personnel", 11,
        "The cloud service provider MUST implement organizational and technical measures ensuring that "
        "administrative access to systems used to operate the cloud service is performed through access paths located "
        "within the EU. Administrative access originating from locations outside the EU MUST be technically "
        "restricted, except in narrowly defined and controlled exceptional scenarios that are subject to additional "
        "authorization and monitoring controls.",
        localization_level="C1"),
    rec("sov4-02-c2", "SOV-4", "SOV-4-02-C2", "C", "operations_personnel", 11,
        "The cloud service provider MUST implement organizational and technical measures ensuring that "
        "administrative access to systems used to operate the cloud service is performed through access paths located "
        "within the EU. Administrative access originating from locations outside Germany MUST be technically "
        "restricted, except in narrowly defined and controlled exceptional scenarios that are subject to additional "
        "authorization and monitoring controls.",
        localization_level="C2", needs_review=True,
        needs_review_note="Verbatim source text states access paths must be located 'within the EU' in the first "
                           "sentence but restricts non-'Germany' origins in the second — a source-document "
                           "inconsistency confirmed against the published PDF, p. 11 (D-008; the C2/Germany "
                           "variant would be expected to say 'within Germany' throughout, matching SOV-4-01-C2's "
                           "pattern). Captured verbatim as printed, not corrected. Intended meaning to be handled "
                           "via a generalization_note referencing D-008 in Phase 2d."),
    rec("sov4-03-c", "SOV-4", "SOV-4-03-C", "C", "facility", 11,
        "The cloud service provider MUST ensure redundant and independent connectivity for the delivery of the "
        "sovereign cloud service. In the event of a disruption of one connectivity provider, alternative connectivity "
        "providers MUST be able to maintain connectivity in accordance with the contractual service level "
        "agreements. At least one of the connectivity providers MUST be an EU based company.",
        needs_review=True,
        needs_review_note="Connectivity-provider redundancy sits between facility (physical network connectivity "
                           "into the datacenter) and supply_chain_services (connectivity provider as an external "
                           "supplier relationship, post-D-007 taxonomy); tagged facility as primary since the "
                           "criterion concerns operational network redundancy at the facility level."),
    rec("sov4-03-ac", "SOV-4", "SOV-4-03-AC", "AC", "facility", 11,
        "At least one of the connectivity providers is not part of the corporate structure of the cloud service "
        "provider.",
        needs_review=True,
        needs_review_note="Same facility/supply_chain_services ambiguity as SOV-4-03-C."),
    rec("sov4-04-c1", "SOV-4", "SOV-4-04-C1", "C", "operations_personnel", 12,
        "The cloud service provider MUST ensure that Security Operations Center (SOC) capabilities for the offered "
        "cloud services are established and operated within the EU. In the case of a disconnect (SOV-4-10), a stand-"
        "alone and equivalent SOC MUST be provided in the EU.",
        localization_level="C1"),
    rec("sov4-04-c2", "SOV-4", "SOV-4-04-C2", "C", "operations_personnel", 12,
        "The cloud service provider MUST ensure that Security Operations Center (SOC) capabilities for the offered "
        "cloud services are established and operated within Germany. In the case of a disconnect (SOV-4-10), a stand-"
        "alone and equivalent SOC MUST be provided in Germany.",
        localization_level="C2"),
    rec("sov4-05-c", "SOV-4", "SOV-4-05-C", "C", "platform", 12,
        "All software updates and operational data affecting the cloud service MUST be received, authorized and "
        "validated in a secured network area managed and controlled by the cloud service provider. The cloud "
        "service provider MUST verify and check updates for known vulnerabilities. Updates MUST include "
        "documentation satisfying the needs of the cloud service provider. The update process MUST be based on a "
        "controlled change management processes."),
    rec("sov4-05-ac1", "SOV-4", "SOV-4-05-AC1", "AC", "platform", 12,
        "The cloud service provider MUST implement the secure network area (e. g. DMZ) on dedicated physical "
        "devices."),
    rec("sov4-05-ac2", "SOV-4", "SOV-4-05-AC2", "AC", "platform", 12,
        "The cloud service provider MUST provide technical documentation how the criterion SOV-4-05-C is "
        "implemented to the responsible cybersecurity authority if requested, in accordance with applicable law and "
        "established supervisory, cooperation agreements or audit mechanisms. The responsible authority is the one "
        "in the country where the data center is located. Such information may be provided through appropriate "
        "confidentiality protections and secure disclosure procedures."),
    rec("sov4-06-c", "SOV-4", "SOV-4-06-C", "C", "platform", 12,
        "When using third-party software under the cloud service provider's responsibility, the cloud service "
        "provider MUST implement risk-based security analysis prior to deployment, including measures to detect "
        "and mitigate malicious code, viruses, spyware, and ransomware."),
    rec("sov4-07-c", "SOV-4", "SOV-4-07-C", "C", "data", 12,
        "Any cloud service derived data, cloud service customer data and account data exchanged between the cloud "
        "service provider and third parties MUST always be monitored, controlled and logged. In order to do so, the "
        "cloud service provider MUST establish a documented process. The documentation MUST be reviewed and "
        "updated regularly, at least once a year. The cloud service provider MUST document what kind of data is "
        "exchanged with third parties. This documentation MUST ensure that it is clear which data is flowing to "
        "which party and this can also be meaningfully aggregated. The cloud service provider MUST make this "
        "documentation available to the cloud service customer. It is acceptable that this is only made available to "
        "the customer if they have agreed to keep the information confidential and not publicly disclose it. The "
        "cloud service provider MUST clearly define the exchange format and document it as part of the data "
        "exchange documentation."),
    rec("sov4-08-c", "SOV-4", "SOV-4-08-C", "C", "data", 13,
        "The cloud service provider MUST document, define, and visualize (via a Data Flow Diagram) all data "
        "exchanges between the cloud service provider and third parties of cloud service derived data, cloud service "
        "customer data, and account data. The data exchanges MUST occur only via known gateways. The "
        "documentation MUST clearly identify data origins, destinations, transport protocols, data type and security "
        "mechanisms protecting these exchanges. The documentation MUST be reviewed and updated regularly, at "
        "least once a year. This documentation does not need to be published publicly."),
    rec("sov4-08-ac", "SOV-4", "SOV-4-08-AC", "AC", "data", 13,
        "The cloud service provider MUST provide the Data Flow Diagram to the responsible cybersecurity authority "
        "if requested, in accordance with applicable law and established supervisory, cooperation agreements or "
        "audit mechanisms. The responsible authority is the one in the country where the data center is located. "
        "Such information may be provided through appropriate confidentiality protections and secure disclosure "
        "procedures."),
    rec("sov4-09-c", "SOV-4", "SOV-4-09-C", "C", "platform", 13,
        "The cloud service provider MUST be able to disconnect all non-EU network-connections to the cloud "
        "without an impairment of the availability, integrity, authenticity and confidentiality of the cloud service. "
        "This includes all incoming updates and data exchanges with non-EU entities (including but not limited to: "
        "external heartbeat signals and global license validation servers) that are in the responsibility of the cloud "
        "service provider. The cloud service provider MUST establish and document a process, when and how a "
        "disconnect is executed. This process MUST be independent from non-EU entities. The cloud service "
        "provider MUST update this documentation regularly, at least once a year. The cloud service provider MUST "
        "conduct disconnection tests for ensuring the availability of all cloud services in case of a disconnection "
        "from the non-EU network-connections at least once a year. The cloud service provider MUST document "
        "these tests as part of the aforementioned documentations. The documentation MUST include, but is not "
        "limited to, the results of the performed test."),
    rec("sov4-09-ac", "SOV-4", "SOV-4-09-AC", "AC", "platform", 14,
        "The cloud service provider MUST provide the documentation of the disconnect process and disconnection "
        "tests to the responsible cybersecurity authority if requested, in accordance with applicable law and "
        "established supervisory, cooperation agreements or audit mechanisms. Where relevant, the cloud service "
        "provider may provide supporting documentation. The responsible authority is the one in the country where "
        "the data center is located. Such information may be provided through appropriate confidentiality "
        "protections and secure disclosure procedures."),
    rec("sov4-10-c", "SOV-4", "SOV-4-10-C", "C", "platform", 14,
        "The cloud service provider MUST be able to reestablish all non-EU-connections after a disconnect in "
        "accordance of criterion SOV-4-9-C (\"Disconnect\") has been performed and has a process to install updates if "
        "the cloud environment was disconnected for a maximum of 90 days. The process to install updates if the "
        "cloud environment was disconnected for at most 90 days MUST also be tested."),
]

SOV5 = [
    rec("sov5-01-c", "SOV-5", "SOV-5-01-C", "C", "supply_chain_software", 14,
        "The cloud service provider MUST identify, for each cloud service, the software components used and their "
        "respective countries of origin. A list of the relevant software suppliers and their country or countries for "
        "each service, MUST be compiled and available on demand to cloud service customers. The identification of "
        "the software components should be based on a Software Bill of Materials (SBOM) (e.g. TR-03183-2) or "
        "achieve a comparable level of quality."),
    rec("sov5-01-ac", "SOV-5", "SOV-5-01-AC", "AC", "supply_chain_software", 14,
        "The cloud service provider MUST maintain a risk-based process for identifying and mitigating "
        "dependencies on external software suppliers relevant to the operation of the cloud service. Where critical "
        "dependencies are identified, the cloud service provider MUST implement appropriate mitigation strategies "
        "and maintain architectural flexibility that enables substitution of software components. If it is not "
        "technically and reasonably feasible, this information MUST be adequately provided to the cloud service "
        "customer."),
    rec("sov5-02-c", "SOV-5", "SOV-5-02-C", "C", "supply_chain_hardware", 15,
        "The cloud service provider MUST maintain a documented inventory of the hardware components used to "
        "provide cloud services. A list of the relevant hardware suppliers and their country or countries MUST be "
        "compiled and available on demand to cloud service customers."),
    rec("sov5-02-ac", "SOV-5", "SOV-5-02-AC", "AC", "supply_chain_hardware", 15,
        "The cloud service provider MUST maintain a risk-based process for identifying and mitigating "
        "dependencies on hardware suppliers relevant to the operation of the cloud service. Where critical "
        "dependencies are identified, the cloud service provider MUST implement mitigation strategies and maintain "
        "architectural flexibility enabling substitution of hardware components. If it is not technically and "
        "operationally feasible, this information MUST be adequately provided to the cloud service customer."),
    rec("sov5-03-c", "SOV-5", "SOV-5-03-C", "C", "supply_chain_services", 15,
        "The cloud service provider MUST maintain a documented inventory of used external cloud services that are "
        "necessary for the delivery of the cloud service. The list of information regarding the relevant external "
        "service providers and the country or countries of service provision or development MUST be made "
        "available to cloud service customers."),
    rec("sov5-03-ac", "SOV-5", "SOV-5-03-AC", "AC", "supply_chain_services", 15,
        "The cloud service provider MUST maintain a documented process for identifying and managing external "
        "service dependencies relevant to the delivery of the cloud service. Where critical dependencies are "
        "identified, the cloud service provider MUST implement mitigation strategies and maintain architectural "
        "flexibility enabling substitution of service dependencies. If it is not technically and operationally "
        "feasible, this information MUST be adequately provided to the cloud service customer."),
    rec("sov5-04-c", "SOV-5", "SOV-5-04-C", "C", "supply_chain_hardware", 15,
        "The cloud service provider MUST maintain documented processes for identifying and mitigating risks "
        "related to export restrictions or supply chain disruptions affecting software, external services, and "
        "hardware used in the delivery of the cloud service. Where such restrictions may materially affect the "
        "operation of the cloud service, the cloud service provider MUST inform affected customers.",
        needs_review=True,
        needs_review_note="Spans all three post-D-007 supply-chain layers (software, hardware, external services) "
                           "simultaneously — export-restriction risk applies across all of them. Tagged "
                           "supply_chain_hardware as primary since export-control regimes (e.g. ITAR/EAR-style "
                           "restrictions) are most classically applied to physical hardware/technology export; "
                           "software and service dependencies are also in scope per the verbatim text above."),
    rec("sov5-05-c1", "SOV-5", "SOV-5-05-C1", "C", "platform", 16,
        "Capacity management MUST be performed in the EU in accordance with C5.",
        localization_level="C1", needs_review=True,
        needs_review_note="Filed under the SOV-5 Supply Chain Sovereignty domain in the source, but content "
                           "concerns operational capacity-management location, not a supply-chain relationship; "
                           "tagged platform as the better content-based layer fit. sov_domain (SOV-5) is preserved "
                           "as given by the source structure; layer is assessed independently per the "
                           "responsibility-map model."),
    rec("sov5-05-c2", "SOV-5", "SOV-5-05-C2", "C", "platform", 16,
        "Capacity management MUST be performed in Germany in accordance with C5.",
        localization_level="C2", needs_review=True,
        needs_review_note="Same domain/layer distinction as SOV-5-05-C1."),
]

SOV6 = [
    rec("sov6-01-c", "SOV-6", "SOV-6-01-C", "C", "platform", 16,
        "The cloud service provider MUST have a backup of the source code in the EU that is not older than 24 hours "
        "and contains at minimum 5 versions of the cloud services so that the operation of the cloud service is "
        "possible at any time without external dependencies. This includes all infrastructure-as-code build-scripts "
        "and deployment toolchains. The local source code backup MUST include a documentation that enables the "
        "cloud service provider to independently work with the source code and develop it further at any time "
        "without external dependencies."),
    rec("sov6-02-c", "SOV-6", "SOV-6-02-C", "C", "platform", 16,
        "In the event of disconnection of third parties, the cloud service provider MUST maintain documented "
        "contingency strategies ensuring continued secure delivery of the cloud services. These strategies may "
        "include alternative software suppliers, internal remediation capabilities, or compensating security "
        "controls."),
    rec("sov6-02-ac", "SOV-6", "SOV-6-02-AC", "AC", "platform", 16,
        "In the event of disruption or loss of an external software vendor, the cloud service provider MUST "
        "maintain the capability to remediate software vulnerabilities and implement necessary changes. The cloud "
        "provider MUST maintain specialized engineering talent and local build-environments necessary to compile, "
        "test, and deploy emergency security patches to the cloud services independently of third parties."),
    rec("sov6-03-c", "SOV-6", "SOV-6-03-C", "C", "platform", 16,
        "The cloud service provider MUST ensure that authorised personnel have access to the software development "
        "tools and environments necessary to maintain and update the cloud services. The cloud service provider "
        "MUST also maintain documented contingency procedures for scenarios in which access to critical software "
        "development tools or development environment dependencies is disrupted, ensuring the continued ability "
        "to maintain and update the cloud services."),
]

DOMAINS = {
    "SOV-1": SOV1,
    "SOV-2": SOV2,
    "SOV-3": SOV3,
    "SOV-4": SOV4,
    "SOV-5": SOV5,
    "SOV-6": SOV6,
}


def write_through(domain_key: str) -> None:
    """Writes /data/extracted/c3a.json (public) containing every domain up
    to and including domain_key, in DOMAINS order, plus
    data/local/c3a-verbatim.json (git-ignored, D-009) holding the real
    verbatim source_text for those same records. Used to produce one
    commit's worth of records per Phase 2a batch.

    Per D-009 (license caution, CR-2): the public file's source_text
    values are replaced with the literal placeholder
    LOCAL_VERBATIM_PLACEHOLDER; the real text is kept only in the
    git-ignored local file, keyed by record id.

    Per D-010 (CR-3): generalized_text is currently just a copy of the
    verbatim English (Phase 2d hasn't run generalization yet), so it is
    also scrubbed to GENERALIZATION_PENDING_PLACEHOLDER in the public
    file — Phase 2d owns filling this field for real.
    """
    order = list(DOMAINS.keys())
    public_records = []
    verbatim = {}
    for d in order[: order.index(domain_key) + 1]:
        for r in DOMAINS[d]:
            verbatim[r["id"]] = dict(r["source_text"])
            public = json.loads(json.dumps(r))  # deep copy
            public["source_text"] = {"en": LOCAL_VERBATIM_PLACEHOLDER, "fr": LOCAL_VERBATIM_PLACEHOLDER}
            public["generalized_text"] = {"en": GENERALIZATION_PENDING_PLACEHOLDER, "fr": GENERALIZATION_PENDING_PLACEHOLDER}
            public_records.append(public)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(public_records, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(public_records)} public records (source_text scrubbed) through {domain_key} -> {OUT}")

    VERBATIM_OUT.parent.mkdir(parents=True, exist_ok=True)
    VERBATIM_OUT.write_text(json.dumps(verbatim, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(verbatim)} verbatim entries -> {VERBATIM_OUT} (git-ignored, local only)")


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "SOV-6"
    write_through(target)
