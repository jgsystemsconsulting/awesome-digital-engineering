# Awesome Digital Engineering [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[<img src="media/logo.svg" align="right" width="100" alt="Digital Engineering">](https://jgsystemsconsulting.github.io/awesome-digital-engineering/)

> Curated resources for **digital engineering** transformation: digital thread, model-based
> definition (MBD), and the policy and standards that bind them.

![Last full sweep: 2026-09](https://img.shields.io/badge/last%20full%20sweep-2026--09-brightgreen)

Part of the awesome-mbse list family (hub repository currently private).
Maintained by [JG Systems Consulting Ltd.](https://github.com/jgsystemsconsulting). See
[Editorial neutrality](CONTRIBUTING.md#7-editorial-neutrality).

initial seed; growth in progress. Every entry below passed a live link check on launch day.
**Install:** none required; clone with
`git clone https://github.com/jgsystemsconsulting/awesome-digital-engineering.git` or browse
on GitHub. **Usage:** open a Contents section, prefer primary sources, and follow
CONTRIBUTING for new entries. **Support:** Suggest a resource, Bug report, and Improvement
forms; security via private advisory (`SECURITY.md`). List text is CC0-1.0 (`LICENSE`).
Linked works keep their own terms. For JG Systems product licensing enquiries (not this list),
see https://labs.jgsystemsconsulting.com/licensing.html.

## Contents

- [Policy and strategy](#policy-and-strategy)
- [Standards](#standards)
- [Digital thread and interoperability](#digital-thread-and-interoperability)
- [Model-based definition and PMI](#model-based-definition-and-pmi)
- [Government and consortia programs](#government-and-consortia-programs)
- [Open tools and reference implementations](#open-tools-and-reference-implementations)
- [Learning and reports](#learning-and-reports)
- [Commercial platforms](#commercial-platforms)

## Policy and strategy

- [OMG Digital Engineering hot topic](https://www.omg.org/hot-topics/digital-engineering.htm) - Object Management Group overview of digital engineering standards work and related specs `DE-general` `report` (2024).
- [OMG Digital Twins hot topic](https://www.omg.org/hot-topics/digital-twins.htm) - OMG digital twin standards and community entry points `digital-thread` `report` (2024).
- [US DoD Chief Technology Officer](https://www.cto.mil/) - Office of the Under Secretary of Defense for Research and Engineering / CTO public site `DE-general` `report` (2024).
- [OUSD(R&E) Acquisition and Sustainment CTO](https://ac.cto.mil/) - Acquisition CTO portal (digital engineering initiatives live under this org tree) `DE-general` `report` (2024).

## Standards

- [ASME Y14.41](https://www.asme.org/codes-standards/find-codes-standards/y14-41-digital-product-definition-data-practices) - Digital product definition data practices for annotated model-based 3D datasets `MBD` `report` `standard` `paid` (2026).
- [ASME Y14.5](https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing) - Dimensioning and tolerancing storefront (GD&T baseline paired with MBD practice) `MBD` `GD&T` `report` `standard` `paid` (2024).
- [ISO 10303 (STEP) overview](https://en.wikipedia.org/wiki/ISO_10303) - Product data representation and exchange family for CAD/PMI interoperability `digital-thread` `report` (2024).
- [ISO/TC 184/SC 4](https://committee.iso.org/home/tc184sc4) - ISO subcommittee for industrial data (STEP and related product data standards) `digital-thread` `report` `standard` (2024).
- [LOTAR standard](https://lotar-international.org/lotar-standard/) - LOTAR EN/NAS 9300 long-term archiving standard family overview `digital-thread` `report` `standard` (2024).

## Digital thread and interoperability

- [prostep ivip](https://www.prostep-ivip.org/) - Association for digital process chains and STEP-related interoperability in industry `digital-thread` `report` (2024).
- [PDES, Inc.](https://pdesinc.org/) - US industry consortium advancing STEP and product data exchange standards `digital-thread` `report` (2024).
- [Open Applications Group (OAGi)](https://www.oagi.org/) - Open standards for business and supply-chain data exchange adjacent to digital thread `digital-thread` `report` (2024).

## Model-based definition and PMI

- [NIST STEP File Analyzer](https://www.nist.gov/services-resources/software/step-file-analyzer) - NIST software to inspect STEP files and report PMI and geometry coverage `MBD` `tool` `other-tool` (2024).
- [usnistgov/SFA](https://github.com/usnistgov/SFA) - Source for NIST STEP File Analyzer / Viewer related tooling `MBD` `tool` `other-tool` (2024).

## Government and consortia programs

- [DMSC / QIF](https://qifstandards.org/about-dmsc/) - Digital Metrology Standards Consortium; QIF (ISO 23952) and DMIS overview `DE-general` `report` (2020).
- [QIF Standards](https://qifstandards.org/) - Quality Information Framework home and digital metrology resources `DE-general` `report` (2024).
- [LOTAR International](https://lotar-international.org/) - Long-term archiving EN/NAS 9300 family based on OAIS `DE-general` `report` (2024).
- [NIST Systems Integration Division](https://www.nist.gov/el/systems-integration-division) - NIST EL division covering systems integration and MBE-related work `DE-general` `report` (2024).
- [NIST MSID](https://www.nist.gov/el/msid) - Manufacturing Systems Integration Division pages for manufacturing digital engineering `DE-general` `report` (2024).
- [ASD-STAN](https://www.asd-stan.org/) - Aerospace and defence standards body (LOTAR and related EN paths) `DE-general` `report` (2024).
- [ASD Europe](https://www.asd-europe.org/) - AeroSpace and Defence Industries Association of Europe `DE-general` `report` (2024).
- [VDA](https://www.vda.de/en) - German Association of the Automotive Industry (digital process and data exchange context) `DE-general` `report` (2024).

## Open tools and reference implementations

- [AlexFemec/STEP-file-parser](https://github.com/AlexFemec/STEP-file-parser) - Basic parser for ISO 10303-21 STEP files `digital-thread` `tool` `other-tool` (2024).
- [IfcOpenShell/step-file-parser](https://github.com/IfcOpenShell/step-file-parser) - Pure Python ISO 10303-21 STEP physical file parser `digital-thread` `tool` `other-tool` (2024).
- [stepcode/stepcode](https://github.com/stepcode/stepcode) - Open-source EXPRESS and STEP toolkit (STEPcode) `digital-thread` `tool` `other-tool` (2024).
- [tpaviot/pythonocc-core](https://github.com/tpaviot/pythonocc-core) - Python bindings to Open CASCADE for CAD geometry and STEP workflows `digital-thread` `tool` `other-tool` (2024).
- [CadQuery/cadquery](https://github.com/CadQuery/cadquery) - Parametric CAD scripting library with STEP import/export paths `MBD` `tool` `other-tool` (2024).
- [usnistgov on GitHub](https://github.com/usnistgov) - NIST public software org (search for STEP, QIF, MBE tools) `DE-general` `tool` `other-tool` (2024).

## Learning and reports

- [NIST publications search: model-based enterprise](https://www.nist.gov/publications/search?k=model-based%20enterprise) - NIST publication index filtered to model-based enterprise topics `DE-general` `report` (2024).
- [NIST Engineering Laboratory software](https://www.nist.gov/services-resources/software) - Directory of NIST EL software including MBE and STEP tools `DE-general` `report` (2024).
- [OMG specifications catalogue](https://www.omg.org/spec/) - Formal OMG specs index (Systems Modeling, digital twin-related work) `DE-general` `report` `standard` (2024).

## Commercial platforms

_No verified entries yet._

## Contributing

Contributions welcome: see [CONTRIBUTING.md](CONTRIBUTING.md) for the inclusion bar,
entry format, and tag vocabulary.

## Install

Nothing to install. This list is a curated index: browse it here on GitHub,
or clone it:

```bash
git clone https://github.com/jgsystemsconsulting/awesome-digital-engineering.git
```

## Usage

1. Open the Contents at the top and jump to a section, or search the page with
   your browser's find function.
2. Open any entry's link to reach the upstream resource; the list never
   re-hosts content.
3. To suggest a resource or report a defect, use the Support channels below
   (or open a pull request that follows CONTRIBUTING.md).

## Support

- Bug or dead link: [bug report form](https://github.com/jgsystemsconsulting/awesome-digital-engineering/issues/new?template=bug_report.yml)
- Suggest a resource (the list's improvement channel):
  [suggestion form](https://github.com/jgsystemsconsulting/awesome-digital-engineering/issues/new?template=suggest-resource.yml)
- Security issues: [private security advisory](https://github.com/jgsystemsconsulting/awesome-digital-engineering/security/advisories/new)
  (see [SECURITY.md](SECURITY.md))

## Version

Current release: **0.1.1** (2026-09-17). See [CHANGELOG.md](CHANGELOG.md) and
[RELEASE-INFO.txt](RELEASE-INFO.txt).
