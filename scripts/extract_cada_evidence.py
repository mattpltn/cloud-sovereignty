#!/usr/bin/env python3
"""Phase 2c: extracts CADA proposal Annex III (audit evidence for the
audit procedure) into data/extracted/cada-evidence.json, conforming to
a new schema, schema/cada-evidence.schema.json (the ONE new schema
authorized for this part of the phase).

Extraction only, no interpretation, per this phase's explicit
instruction. Each of the eleven audit criteria (A-K) assesses one
lettered Annex II paragraph (a)-(k) under Union assurance levels 2, 3
and 4 (Annex III's own constant framing for every criterion). Numbered
evidence items that themselves contain lettered/roman sub-bullets in
the source (e.g. criterion A's item (5)(a)-(d), criterion G's 7.1/7.2
subsections) are kept as a single evidence_items string per top-level
number, preserving the sub-structure inline as printed, rather than
introducing further nested schema structure — a schema-fit choice
documented in METHODOLOGY.md, consistent with how Annex II's own
numbered sub-criteria were handled in cada.json.

Verbatim-isolation regime (D-009/D-010) from the start:
data/local/cada-evidence-verbatim.json (git-ignored).

Run: .venv/bin/python3 scripts/extract_cada_evidence.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_PUBLIC = ROOT / "data" / "extracted" / "cada-evidence.json"
OUT_LOCAL = ROOT / "data" / "local" / "cada-evidence-verbatim.json"

DOCUMENT = "COM(2026) 502 final, 3.6.2026 — Annexes 1 to 3 (Cloud and AI Development Act proposal)"
FR_PENDING = "FR-TRANSLATION-PENDING"
PLACEHOLDER = "SEE-LOCAL-VERBATIM"


def ls(en: str) -> dict:
    return {"en": en, "fr": FR_PENDING}


def pub() -> dict:
    return {"en": PLACEHOLDER, "fr": FR_PENDING}


CRITERIA = [
    {
        "id": "A",
        "title": "Union establishment",
        "assesses_annex_ii_paragraph": "paragraph (a)",
        "page": 12,
        "evidence_items": [
            "Any evidence demonstrating that the audited provider is incorporated under the law of a Member State in the Union or otherwise constituted in line with company law of a Member State in the Union.",
            "Any evidence that the registered office, central administration, and main establishment of the audited provider is established within the Union.",
            "The auditing organisation should verify the applicable Union legal framework of the audited provider and verify whether their establishment is genuine and stable or whether the audited provider instead qualifies only as a non-EU provider offering services in the Union.",
            "The auditing organisation should verify whether the provider is legally incorporated in a Member State of the Union. Evidence of this could include, but is not limited to, the national company extracts, tax residency documentation, business licences, VAT registration, verification of whether the provider is registered in the Business Registers Interconnected System (BRIS) and the VAT information Exchange System (VIES).",
            "The auditing organisation should verify the stable and effective presence in the Union of the audited provider. The auditing organisation should therefore verify that: (a) EU physical offices or operational premises exist (for example, through lease contracts, utility bills or property documents); (b) permanent staff is located in the Union and that customer support operations are carried out in the Union (for example, through employment contracts, payroll records, personnel timesheets); (c) contractual operations are handled in the Union (for example, through activity management records, incident reporting records); (d) banking and accounting functions are exclusively in the Union (for example, through financial statements and statutory audit reports).",
            "The auditing organisation should verify the presence of EU Member State establishment units or branches (for example, through lease contracts, utility bills, property documents, employment contracts, timesheets, payroll records or purchase orders).",
        ],
    },
    {
        "id": "B",
        "title": "Location of infrastructure, assets, and personnel",
        "assesses_annex_ii_paragraph": "paragraph (b)",
        "page": 13,
        "evidence_items": [
            "Location of infrastructure: (a) A list with relevant details of the location of the infrastructure and data storage locations used in the provision of the audited service. This list should include the precise location (number, street, city, postal code and country) of the infrastructure demonstrating that all elements remain within the Union for the provision of the audited service. This includes the location for the primary, backup, disaster recovery and log storage. (b) Any other evidence that the IT infrastructure is located in the Union such as lease agreements, property deeds, maintenance contracts, service contracts, facility access logs. (c) Network diagrams and architecture documents illustrating the exclusive use of Union-based infrastructure for data storage and processing, including backup and replicated data.",
            "Location of assets: (a) A list and relevant details of the assets used in the provision of the audited service, such as an asset register. (b) Evidence that servers, equipment, and operational assets are located in the Union, such as records identifying the server and its location, purchase invoices, delivery notes, licence agreements, subscription contracts, or invoices for software purchases or subscriptions, invoices with delivery proofs for hardware. (c) Evidence that service delivery capabilities are based in the Union, such as deployment records, installation records, service status reports, configuration reports, monitoring outputs, admin logs showing usage of the service.",
            "Location of personnel: (a) A list and relevant details of the personnel involved in the provision of the audited service. (b) Evidence that the personnel involved in the provision of the audited service are located in the Union, including employment contracts, payroll records, timesheets, activity records, and organisational charts showing Union-based staff with operational responsibilities.",
            "Considerations regarding the infrastructure, assets and personnel: (a) The auditing organisation should also assess where such infrastructure, assets, or personnel: i. store, transmit, access, process or otherwise handle customer data; ii. provide, enable, or could enable administrative access to, control over, configuration of, or visibility into customer data; iii. if compromised, misconfigured, made unavailable or disrupted could reasonably result in the disruption or unavailability of the audited service.",
        ],
        "notes": (
            "'Infrastructure' means physical infrastructure, including but not "
            "limited to, data centre infrastructure or colocation "
            "infrastructure, network, cooling, and IT systems that allow for "
            "the management of the datacentre. 'Assets' means hardware and "
            "software, including, but not limited to, libraries, the internal "
            "network needed for software components to communicate, "
            "cryptographic materials that enables the provision of the cloud "
            "computing service. 'Personnel', including personnel managed by "
            "subcontractors, means individuals who support the delivery, "
            "administration, security, availability, or operation of the "
            "audited service."
        ),
    },
    {
        "id": "C",
        "title": "Data localisation in the Union",
        "assesses_annex_ii_paragraph": "paragraph (c)",
        "page": 14,
        "evidence_items": [
            "Evidence demonstrating that customer data are stored and processed exclusively in the Union and that third-parties or subcontractors that do not meet the conditions under this Annex are in no circumstances technically or operationally able to access, obtain, make unavailable, destroy or more generally process customer data without prior authorisation. Examples include access logs, support access policies, privileged access records, backup retention policy, data flows diagram demonstrating where the customer data are stored, processed, replicated and backed up. When processing personal data, contracts with the subcontractors that demonstrate compliance with Regulation (EU) 2016/679.",
            "Evidence of logs and monitoring records demonstrating that all data are stored and processed exclusively within the Union. Examples include master service agreements, data processing agreements, data residency contractual agreements or any EU data boundary.",
            "Evidence (such as contractual agreements, logs, and procedures offered to public sector bodies) demonstrating that the audited provider and the subcontractors which are involved in the provision of the audited service have put in place the necessary measures to ensure that: (a) no customer data, including encrypted data, are transferred outside of the Union without public sector body approval; (b) no data are transferred to any third-party other than subcontractors which are involved in the provision of the service or recipients expressly authorised by the public sector body.",
            "A data flow diagram showing the flows of data between the cloud computing service provider and customer data, as well as with third-party services and subcontractors. The diagram must clearly identify the source and destination of data and demonstrate that the data does not leave the Union.",
        ],
        "notes": (
            "For the purpose of this Annex, a customer means a public sector "
            "body who has entered into a contractual or other legally binding "
            "arrangement with the cloud computing service provider for the "
            "purpose of accessing or using the cloud computing service. "
            "'Customer data' could mean any data under the control of the "
            "cloud computing service customer, whether by legal, contractual, "
            "or other means, that are: (a) input into the cloud computing "
            "service by or on behalf of the customer, including "
            "authentication credentials; (b) produced through the customer's "
            "use of the cloud computing service. Customer data may also "
            "include data under the audited providers control that are "
            "derived as a result of interaction with the audited service by "
            "the cloud service customer. This includes customer data and any "
            "data resulting from the usage of the cloud computing services "
            "(i.e. telemetry, metadata). 'Cloud computing service derived "
            "data' includes the portion of log data containing records of "
            "who used the service, at what times, which functions, types of "
            "data involved and so on. It can also include information about "
            "the numbers of authorised users and their identities. It can "
            "also include any configuration or customisation data, where the "
            "cloud computing service has such configuration and "
            "customisation functionalities."
        ),
    },
    {
        "id": "D",
        "title": "Union citizenship",
        "assesses_annex_ii_paragraph": "paragraph (d)",
        "page": 15,
        "evidence_items": [
            "The audited provider should provide the auditing organisation with proof that it has implemented the measures to ensure that, if a public sector body were to request Union citizenship, the personnel involved in the provision of the audited service are Union citizens. This can be demonstrated through valid official government issued documents (e.g. valid passport and national identity card).",
            "The audited provider should provide organisational charts and job descriptions confirming that it can ensure, where requested, that only personnel with Union citizenship have access to the audited service's operation, management, maintenance, and support.",
            "The audited provider should provide documents demonstrating access control policies and audit trails showing that only authorised personnel who are Union citizens can access the service's systems and data.",
            "The audited provider should demonstrate that it has put in place procedures describing how citizenship is verified before assignment and how compliance with this audit criterion is maintained throughout employment.",
        ],
        "notes": (
            "Personnel involved in the provision of the audited service could "
            "include personnel who have logical or physical access to "
            "infrastructure and assets used to operate the cloud computing "
            "service, as well as those who are responsible for customer "
            "support, and all personnel who have management control of the "
            "cloud computing service provider."
        ),
    },
    {
        "id": "E",
        "title": "European cybersecurity certification scheme adopted under Regulation 2019/881",
        "assesses_annex_ii_paragraph": "paragraph (e)",
        "page": 15,
        "evidence_items": [
            "A valid European cybersecurity certificate issued by a competent conformity assessment body demonstrating that the audited service has been assessed and found compliant with the requirements corresponding to the 'basic', 'substantial' or 'high' assurance levels under a European cybersecurity certification scheme adopted under Regulation (EU) 2019/881, provided that such has been established.",
            "A certification report including a description of the main components used for the development and operation of the cloud computing service that is covered by the audit certificate.",
            "Until the European cybersecurity certification scheme covering cloud computing services has been established, the audited provider can demonstrate compliance through valid cybersecurity certifications. This can include, but is not limited to, the following: (a) a valid certificate issued by a competent conformity assessment body (in line with CEN/CLC/TS 18072:2025) demonstrating that the cloud computing service has been assessed and found compliant with the requirements corresponding to the 'basic' or 'substantial' or 'high' assurance levels defined under CEN/TS 18026:2024; (b) A valid certificate issued by the relevant national competent authority demonstrating that the cloud computing service has been assessed and found compliant with the requirements under the national cybersecurity scheme currently in place in the Member State; (c) in the absence of a national scheme, evidence demonstrating adherence to the highest level of cybersecurity standards available on the market.",
        ],
    },
    {
        "id": "F",
        "title": "AI systems operated by a third country or third country legal entity",
        "assesses_annex_ii_paragraph": "paragraph (f)",
        "page": 15,
        "evidence_items": [
            "Contractual clauses stating that data processed or generated by using the audited service, including customer-derived data, logs and telemetry, will not be used to train or fine-tune any AI model or system operated by a third country or a third-country legal entity, and are not transferred outside the Union in any case.",
            "Contractual clauses specifying that data are processed solely for the delivery of the audited service and not for service improvements or model or system enhancements or any other secondary purpose.",
            "Data flow diagrams documenting the end-to-end flow of data, covering data ingestion, storage, processing and deletion. The diagrams should also show where the AI pipelines or machine learning operations (MLOps) connect with customer data.",
            "MLOps or deployment records demonstrating that the build, test and release locations are in the EU.",
            "Model or system cards covering the model or system name, version, training and validation sources, including statements that the data generated by using the audited service does not leave the Union.",
            "Data lineage policies and related implementation documentation that shows that the provider operates data lineage and provenance tools and that can demonstrate (per record) what the data has been used for.",
            "A list of the subcontractors (indicating their country of establishment) that access the data generated by using the audited service.",
        ],
    },
    {
        "id": "G",
        "title": "Absence of third-country control or third-country entity control",
        "assesses_annex_ii_paragraph": "paragraph (g)",
        "page": 16,
        "evidence_items": [
            "The auditing organisation should identify and analyse: (a) all direct and indirect shareholders, up to the ultimate owners; (b) the cap table documenting the company's ownership structure; (c) the body or bodies empowered to take strategic decisions (general assembly of shareholders, supervisory board, board of directors, etc.); (d) the rules for the appointment/election/removal of governing bodies and the actual composition of the governing bodies (e.g. to identify if any shareholder is entitled to nominate a board representative or has majority seats in the board); (e) the quorums and majority required for adopting strategic decisions, in order to determine if any shareholder can take a strategic decision (either because they have the required majority to approve such a decision or because they can block such a decision through a veto or other specific rights even if they cannot impose such a decision on their own, etc.); (f) the possible influence on strategic decisions through commercial links, financial links or other means, etc.",
            "The audited provider should request all the above information from its subcontractors and make it available to the auditing organisation.",
            "7.1 Assessment of ownership and control (1): The audited provider should provide the auditing organisation with the following evidence related to the headquarters: (a) the location and full address of the global headquarters and/or head office; (b) the locations of the executive management structures.",
            "7.1 (2): The audited provider should provide the auditing organisation with the following evidence related to the ownership structure and specific rights: (a) A detailed list describing any owners that: i. hold, directly or indirectly, at least 5% of the capital or at least 5% of the voting rights, including through any content, understanding, relationship or intermediary. This includes voting agreements between shareholders that would together have more than 5% of the voting rights or 5% of the capital; ii. have one or more of the following specific rights in relation to their ownership: (a) right to veto a transfer of shares; (b) pre-emption rights; (c) right to purchase additional shares or investment subject to conditions. (b) The auditing organisation should request the following supporting documents to assess the elements in paragraph 2(a): i. commercial registry extracts and shareholders' books of the organisation and any other relevant document that clearly indicate the shareholders and their voting rights or percentage of interest; ii. shareholders' agreement, memorandum of understanding among shareholders, statutes, articles of association or other relevant documents regarding the decision-making procedures within the legal entity, investment agreements between the shareholders, etc.; iii. for any shareholders that are legal persons that hold at least 5% in the capital or at least 5% of the voting rights: (1) a graph describing the different ownership layers/chain of control until the ultimate owners; (2) the articles of association, bylaws or equivalent constitutional documents; (3) a register of directors, officers and signatories.",
            "7.1 (3): The audited provider should provide the auditing organisation with the following evidence related to the corporate governance: (a) a description of: i. the decision-making bodies, their composition as well as their nationality or place of establishment (where applicable); ii. the rules regarding election, appointment, nomination or tenure of members of the decision-making bodies or other management positions; iii. the decision-making procedures, including information on the required majority and/or quorum needed for decisions; iv. internal governance policies describing how ownership and control decisions are recorded and approved; board and management decisions reflecting the stated control structure; board minutes and resolutions for control changes. (b) supporting documents setting out or describing: the decision-making bodies and the rules on their election, appointment, nomination or tenure, decision-making procedures, voting rights, veto rights, appointment rights, approval rights within the legal entity (e.g. articles of association bylaws, reports on corporate governance, etc.). The supporting documents and information should be provided for each intermediate legal entity that directly or indirectly holds 5% or more of the capital or voting rights, up to the ultimate owners of all the layers involved.",
            "7.1 (4): The audited provider should provide the following control-related evidence to the auditing organisation: (a) evidence of the commercial links conferring control. This includes, but is not limited to, a list of individuals or legal entities with whom the audited providers (or the owners of the audited provider, including intermediate layers until the ultimate owners) have a commercial relationship that (a) leads to a similar level of control on management and resources as the ownership of shares or assets; and (b) is of very long duration (e.g. very important long-term supply agreements or credits provided by software manufacturers/customers, coupled with structural links). (b) supporting documents should include cooperation agreements with the public sector body or software manufacturers, etc.",
            "7.1 (5): The audited provider should provide the auditing organisation with the following evidence related to the financial links conferring control: (a) The audited provider should list the individuals or legal entities (including controlling shareholders or owners) on whom the audited provider (or the owners) are financially dependent in a way that could allow them to obtain concessions in strategic business areas. (b) The supporting documents should include loan documents, by-laws, documents showing the financial link; etc.",
            "7.1 (6): The audited provider should provide the auditing organisation with the following evidence related to other sources of control: (a) The audited providers should indicate to the audited organisation if there is any other means, process or link ultimately conferring control to another third country or a legal entity established in a third country (similar level of control on management and resources as the ownership of shares or assets and of long duration). (b) Supporting documents should provide evidence of any such control or a declaration that there is no such control (this declaration may come from the management board of the service provider). NB: The elements that should be taken into account when assessing control are the ownership structures and specific rights, corporate governance, commercial links conferring control, financial links conferring control and any other sources of control.",
            "7.2 Additional steps based on the conclusion of the ownership and control test: If the auditing organisation determines that the audited provider is subject to the control of a third country or a third-country legal entity, it should request the following additional evidence: (c) Demonstrating that the Commission has adopted a decision pursuant to Article 19 regarding the third country for which the cloud computing service provider is subject to the control of; (d) All evidence demonstrating that the audited provider and any subcontractor involved in the provision of the audited service has implemented the necessary measures to enforce the effective legal, technical and organisational separation between the cloud computing service provider and any third country or legal entity established in a third country, ensuring that the cloud computing service provider is unable to comply, legally, technically and operationally, with any request to access customer data, including encrypted data, or to disrupt service continuity or to degrade service quality; (e) All evidence demonstrating that the public sector body will be informed of any such request and a confirmation that the request has been refused; (f) All evidence demonstrating the maintenance of an up-to-date record of any request to access customer data, to disrupt service continuity or to degrade service quality from a third country or a legal entity established in a third country, containing at least the request and the response to the request.",
        ],
        "notes": (
            "Sub-clause numbering (7.1/7.2, and the lettering restarting at "
            "(c) in 7.2) is captured exactly as printed in the source; the "
            "7.2 lettering does not restart at (a) in the source text. "
            "7.2's reference to 'Article 19' is the same cross-reference "
            "point noted against Annex II 3.1(g) in cada.json — see "
            "csat-sov1-cada-ua3-g's needs_review_note."
        ),
    },
    {
        "id": "H",
        "title": "No technical and operational support outside of the Union",
        "assesses_annex_ii_paragraph": "paragraph (h)",
        "page": 18,
        "evidence_items": [
            "Evidence that the audited provider has implemented binding contractual clauses stating that all support, administration, maintenance, monitoring, incident response, and operational activities must be initiated and performed exclusively in the Union. This could include contractual clauses requiring advanced disclosure of all subcontractors and support locations, prior written approval before engaging any new subcontractors, and a right to reject any subcontractors located outside of the Union.",
            "Evidence that the audited provider maintains an up-to-date subcontractor register.",
            "Evidence that the audited provider does not subcontract or transfer such activities outside of the Union.",
            "Evidence that the audited provider has implemented the necessary legal, technical and organisational measures to ensure that there can be no remote access for technical and operational support from outside the Union for the audited service.",
            "Evidence that the audited provider's help desk/support services, infrastructure administration, operations of its security operations centre (SOC) or network operations centre (NOC), privileged access, backup handling, and disaster recovery operations of the audited service are exclusively provided from the Union, including the access path to operate the service.",
            "Evidence that the audited provider ensures that the personnel upon the departure from the company have no further access to the audited service and revokes all access policies.",
            "Evidence that the audited provider has implemented the necessary technical and organisational measures to ensure that administrative access to systems used to operate the audited service is provided through access paths located within the Union. This can be demonstrated through the implementation of geographically restricted network controls, Union-based administrative infrastructure, privileged access management controls, and monitoring mechanisms.",
            "Evidence that the audited provider has procedures in place that there is no effective control of a third country or a legal entity established in a third country, including for subsequent sub-outsourcing.",
        ],
    },
    {
        "id": "I",
        "title": "Ensuring the transparency of the software supply chain",
        "assesses_annex_ii_paragraph": "paragraph (i)",
        "page": 19,
        "evidence_items": [
            "The audited provider should make available to the auditing organisation a complete and up-to-date software bill of materials (SBOM) for all software components, including open-source software (OSS).",
            "The audited provider should make available to the auditing organisation a list of dependencies. This should include: (a) all software modules, libraries or application programming interfaces (APIs) used, as well as development tools; (b) origin of software: where (country of origin) and by whom the software is designed, developed and maintained, the location and jurisdiction governing the software distribution, and updates; (c) degree of reliance on non-EU vendors, facilities, or proprietary technologies; for level 3, evidence that in case the software stack is provided by a third country entity, no unduly unjustified licensing restrictions are in place; (d) degree of reliance on open-source software; (e) visibility into the entire software manufacturer and sub-manufacturer chain, including audit rights. N.B. The requirements above imply that joint ventures made, e.g., of a Union entity with a legal entity established in a third country can qualify for this level.",
            "The audited provider should provide: (a) evidence of a risk-based process for identifying and mitigating dependencies on external software manufacturers relevant to the operation of the cloud computing service; (b) evidence that it has identified one or more alternative software solutions, including open-source software. If equivalent software cannot be identified, a solution ensuring minimal viable functionality must be identified. Tests must be implemented and a switchover plan enabling migration to such alternative solutions; (c) evidence that it can migrate to an alternative solution in the event of any defect or failure of the vendor or restrictions from a third country or a legal entity established in a third country; (d) provide a list of open standards that are followed as part of the audited providers policies regarding the audited service.",
            "The audited provider should ensure transparency through remote access and source code auditability by: (a) making available to the auditing organisation a list of evidence to prove that there is no use of any remote features or mechanisms that could be used to materially tamper with or disrupt a device, system, or software. This should include: i. evidence related to the testing of the software component to prevent the use of any remote features or mechanisms that could be used to materially tamper with or disrupt a device, system, or software (test procedure, test reports, test plan, etc.); ii. evidence that the organisation's change management procedures cover any change in firmware, bios and software updates as well as integration of a new components to prevent the use of any remote feature or mechanism; iii. evidence that the maintenance procedure is updated to include preventing any remote feature or mechanism that could be used to materially tamper with or disrupt a device, system or software. (b) The audited provider must ensure that the third-party independent auditor is granted the right to access and audit the source code of such software. The audited provider must also ensure that all documentation, technical material, information necessary to evaluate and audit the source code are made available to the auditing organisation in a complete, accurate, and accessible format.",
        ],
    },
    {
        "id": "J",
        "title": "Open-source software",
        "assesses_annex_ii_paragraph": "paragraph (j)",
        "page": 20,
        "evidence_items": [
            "The audited provider should ensure transparency through remote access and source code auditability by: (a) making available to the auditing organisation a list of evidence to prove that there is no use of any remote features or mechanisms that could be used to materially tamper with or disrupt a device, system, or software. This should include: i. evidence related to the testing of the software component to prevent the use of any remote features or mechanisms that could be used to materially tamper with or disrupt a device, system, or software (test procedure, test reports, test plan, etc.); ii. evidence that the organisation's change management procedures include any change in firmware, bios and software updates as well as integration of new components to prevent the use of any remote feature or mechanism; iii. evidence that the maintenance procedure is updated to include preventing any remote feature or mechanism that could be used to materially tamper with or disrupt a device, system or software.",
            "The audited provider should provide: (a) evidence of a risk-based process to identify and mitigate: (i) a weak ecosystem and community support of the OSS; (ii) a failure to continuously monitor the updates released; (iii) cases where the OSS is deprecated or is no longer maintained. (b) evidence that the audited provider has applied the up-to-date OSS without undue delay. (c) evidence that the audited provider has identified one or several alternative open-source solutions. If the audited provider cannot identify an equivalent software, it must identify a solution ensuring minimal viable functionality. The audited provider must implement tests and a switchover plan enabling migration to the alternative solutions.",
            "Where the audited provider uses software released under an open-source licence, the audited provider should implement mechanisms to detect and provide timely notice to the public sector body if the software is acquired by or comes under control of a third country or a legal entity or foundation established in a third country.",
        ],
    },
    {
        "id": "K",
        "title": "Global services and subsidiaries in third-countries",
        "assesses_annex_ii_paragraph": "paragraph (k)",
        "page": 22,
        "evidence_items": [
            "The auditing organisation should verify that the subsidiary is legally and operationally independent from the audited provider.",
            "The audited provider must demonstrate that the subsidiary has no access to systems processing or storing the customer data.",
            "The audited provider must demonstrate that the subsidiary has no privileged accounts within the Union production environments, including cloud administration, Identity and Access Management (IAM), Privileged Access Management (PAM), monitoring or database administration privileges.",
            "The auditing organisation should verify that the personnel of the subsidiary cannot obtain access to Union customer data.",
            "The auditing organisation should verify that the subsidiary has no authority to instruct Union operational staff to disclose customer data or bypass security procedures.",
            "The auditing organisation should verify that all foreign government requests received by the subsidiary are formally redirected to the competent Union entity for legal assessment under Union and Member State law.",
        ],
    },
]


def main() -> None:
    public_criteria = []
    local_verbatim = {}

    for c in CRITERIA:
        key_prefix = f"cada-evidence-{c['id']}"
        local_verbatim[f"{key_prefix}-title"] = ls(c["title"])
        for i, item in enumerate(c["evidence_items"], start=1):
            local_verbatim[f"{key_prefix}-item{i}"] = ls(item)
        if "notes" in c:
            local_verbatim[f"{key_prefix}-notes"] = ls(c["notes"])

        record = {
            "id": c["id"],
            "title": pub(),
            "assesses_annex_ii_paragraph": c["assesses_annex_ii_paragraph"],
            "evidence_items": [pub() for _ in c["evidence_items"]],
            "source_pointer": {
                "document": DOCUMENT,
                "section": f"Annex III, audit criterion {c['id']} — {c['title']}",
                "page": c["page"],
            },
        }
        if "notes" in c:
            record["notes"] = pub()
        public_criteria.append(record)

    public_doc = {
        "document": DOCUMENT,
        "version": "COM(2026) 502 final, 3.6.2026",
        "criteria": public_criteria,
    }

    OUT_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    OUT_PUBLIC.write_text(json.dumps(public_doc, indent=2, ensure_ascii=False) + "\n")
    OUT_LOCAL.write_text(json.dumps(local_verbatim, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(public_criteria)} audit criteria -> {OUT_PUBLIC}")
    print(f"Wrote {len(local_verbatim)} verbatim entries -> {OUT_LOCAL}")


if __name__ == "__main__":
    main()
