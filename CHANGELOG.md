# Changelog

All notable changes to the System Design for Program Managers handbook are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-10-19

### Added
- **Formal Audit and Roadmap**: Added `AUDIT_REPORT.md` (identifying 70 technical defects with severity rankings and verification methods) and `IMPROVEMENT_ROADMAP.md` (defining multi-phase workstreams, dependencies, and acceptance criteria).
- **Master Architecture Glossary**: Added `GLOSSARY.md` containing definitions for 50+ distributed systems terms, consensus algorithms, latency hierarchies, and reliability metrics.
- **Automated Quality Gate Validator**: Added `scripts/validate_docs.py` to enforce zero machine-specific paths, zero em dashes, valid relative links, compliant Mermaid syntax, and mandatory case study sections.
- **Continuous Integration Workflow**: Added `.github/workflows/docs-quality.yml` to automatically execute quality checks on pull requests and commits to `main`.
- **Architectural Decision Records (ADRs)**: Integrated Michael Nygard ADR format into case studies and core modules, detailing context, alternatives, trade-offs, and failure consequences.
- **Failure Mode and Effects Analysis (FMEA)**: Added comprehensive edge-case failure matrices covering partial partitions, retry storms, duplicate events, and reconciliation policies across all case studies.
- **Module Learning Roadmaps**: Created structured entry-point `README.md` files for all five curriculum modules with role-based fast tracks and deep mastery paths.
- **LLM Ingestion Standards and Tooling**: Implemented `llms.txt` and consolidated prompt-ready bundle `llms-full.txt` (~45k tokens) with `scripts/build_llm_bundle.py` for one-command ingestion into ChatGPT, Claude, Gemini, and NotebookLM.

### Changed
- **Capacity Planning Recalculations**:
  - Segregated CDN blob storage from Redis RAM metadata in photo and video storage calculations.
  - Applied Zipfian power laws ($s = 1.0$) for realistic 80/20 cache hit distribution modeling.
  - Modeled layer 4 and layer 7 network overhead (TLS 1.3 + TCP + IP + WebSocket headers), expanding GPS payloads from 36B to 150B wire footprint.
  - Recalculated notification cost models, demonstrating carrier cascades saving over $2.5B annually at global scale.
- **Technical Rigor and Qualified Claims**:
  - Removed unsupported assertions such as "100% availability" and "zero downtime".
  - Qualified high-availability designs with documented failover windows, partition semantics, and recovery time bounds.
  - Added primary citations (RFCs, academic papers, and official engineering publications) across all core chapters.
- **Mermaid Visual Architecture**:
  - Standardized flowchart, sequence, and state diagrams across all modules.
  - Corrected syntax directives to use compliant `classDef` definitions and consistent color palettes.
- **Documentation Navigation**:
  - Replaced all local filesystem links with relative repository links.
  - Added breadcrumb navigation and cross-chapter prerequisite links throughout the curriculum.

### Fixed
- Fixed broken internal relative links across Module 1 through Module 5.
- Fixed corrupted Mermaid class styling directives in URL Shortener, Notification Engine, and Observability chapters.
- Fixed missing structural sections across case study documentation.
- Eliminated all em dashes and en dashes across all files in favor of consistent typographical standards.

---

## [1.0.0] - Initial Release

- Initial curriculum covering 5 core modules and 5 real-world case studies for Technical Program Managers.
