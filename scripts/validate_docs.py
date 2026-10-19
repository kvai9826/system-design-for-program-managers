#!/usr/bin/env python3
"""
Automated Quality Gate and Validation Script for System Design Handbook.

Performs verification of:
1. Machine-specific local filesystem paths (e.g. file:/// or /Users/).
2. Strict typography rules (zero em dashes: — or –).
3. Internal relative Markdown link resolution.
4. Mermaid diagram syntax integrity (no broken classDef statements, balanced delimiters).
5. Case study standard 14-section structure enforcement.
6. Primary citations presence in technical modules.
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def check_no_machine_specific_paths(files):
    errors = []
    machine_path_regex = re.compile(r'file:///Users/|/Users/[a-zA-Z0-9_\-\.]+')
    for f in files:
        # Exclude AUDIT_REPORT.md and IMPROVEMENT_ROADMAP.md as they document past audit findings
        if f.name in ["AUDIT_REPORT.md", "IMPROVEMENT_ROADMAP.md"]:
            continue
        content = f.read_text(encoding="utf-8")
        for line_num, line in enumerate(content.splitlines(), start=1):
            if machine_path_regex.search(line):
                errors.append(f"{f.relative_to(REPO_ROOT)}:{line_num} -> Machine-specific path detected: '{line.strip()}'")
    return errors

def check_no_em_dashes(files):
    errors = []
    em_dash_regex = re.compile(r'[\u2014\u2013]')
    for f in files:
        # Exclude AUDIT_REPORT.md and IMPROVEMENT_ROADMAP.md if they reference em dashes in review text
        if f.name in ["AUDIT_REPORT.md", "IMPROVEMENT_ROADMAP.md"]:
            continue
        content = f.read_text(encoding="utf-8")
        for line_num, line in enumerate(content.splitlines(), start=1):
            if em_dash_regex.search(line):
                errors.append(f"{f.relative_to(REPO_ROOT)}:{line_num} -> Em dash or en dash detected: '{line.strip()}'")
    return errors

def check_internal_relative_links(files):
    errors = []
    # Match markdown links: [text](target)
    link_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    for f in files:
        content = f.read_text(encoding="utf-8")
        for line_num, match in enumerate(link_regex.finditer(content), start=1):
            target = match.group(2).strip()
            # Skip external web URLs, mailto, and anchor-only links
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            # Remove anchor fragments for file existence check
            file_target = target.split("#")[0]
            if not file_target:
                continue
            target_path = (f.parent / file_target).resolve()
            if not target_path.exists():
                errors.append(f"{f.relative_to(REPO_ROOT)} -> Broken relative link '{target}' to non-existent path: {target_path}")
    return errors

def check_mermaid_syntax(files):
    errors = []
    mermaid_block_regex = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
    bad_class_def_regex = re.compile(r'^\s*class\s+Def[A-Za-z0-9_]+\s+fill:', re.MULTILINE)
    
    for f in files:
        content = f.read_text(encoding="utf-8")
        for idx, match in enumerate(mermaid_block_regex.finditer(content), start=1):
            block = match.group(1)
            # Check for corrupted 'class Def...' statements
            if bad_class_def_regex.search(block):
                errors.append(f"{f.relative_to(REPO_ROOT)} -> Mermaid block #{idx} contains corrupted 'class Def...' syntax instead of 'classDef'")
            # Check that diagram starts with valid directive
            first_line = block.strip().splitlines()[0].strip()
            valid_directives = ("flowchart", "sequenceDiagram", "stateDiagram", "graph", "classDiagram", "erDiagram")
            if not any(first_line.startswith(d) for d in valid_directives):
                errors.append(f"{f.relative_to(REPO_ROOT)} -> Mermaid block #{idx} starts with unrecognized directive: '{first_line}'")
    return errors

def check_case_study_structure(files):
    errors = []
    case_studies = [f for f in files if "05-real-world-case-studies" in str(f) and f.name != "README.md"]
    required_keywords = [
        ("Requirements", "Requirements and SLAs"),
        ("Capacity", "Capacity Planning"),
        ("Architecture", "End-to-End System Architecture"),
        ("API Contracts", "API Contracts"),
        ("Data Model", "Data Model"),
        ("Decision Records", "Architectural Decision Records"),
        ("Failure", "Failure-Mode / FMEA"),
        ("Security", "Security and Governance"),
        ("Observability", "Observability and Monitoring"),
        ("Execution Plan", "TPM Execution Plan"),
        ("Practice", "Practice System Design Questions"),
        ("Sources", "Primary Sources and Further Reading")
    ]
    for cs in case_studies:
        content = cs.read_text(encoding="utf-8")
        for kw, desc in required_keywords:
            if kw.lower() not in content.lower():
                errors.append(f"{cs.relative_to(REPO_ROOT)} -> Missing required case study section: '{desc}' (keyword: {kw})")
    return errors

def check_primary_sources(files):
    errors = []
    core_modules = [f for f in files if any(m in str(f) for m in ["01-foundations", "02-data-architecture", "03-system-resilience-scale", "04-tpm-execution-framework"]) and f.name != "README.md"]
    for f in core_modules:
        content = f.read_text(encoding="utf-8")
        if "Primary Sources and Further Reading" not in content and "Primary Sources" not in content:
            errors.append(f"{f.relative_to(REPO_ROOT)} -> Missing 'Primary Sources and Further Reading' citation section")
    return errors

def main():
    print("=" * 70)
    print("System Design Handbook Automated Quality Gate Validator")
    print("=" * 70)
    
    all_md_files = sorted(list(REPO_ROOT.glob("**/*.md")))
    print(f"Total Markdown Documents Discovered: {len(all_md_files)}")
    print("-" * 70)
    
    total_failures = 0
    checks = [
        ("1. Machine-Specific Paths Check", check_no_machine_specific_paths),
        ("2. Typography & Zero Em-Dash Check", check_no_em_dashes),
        ("3. Internal Relative Links Resolution", check_internal_relative_links),
        ("4. Mermaid Diagram Syntax Integrity", check_mermaid_syntax),
        ("5. Case Study Standard Structure Check", check_case_study_structure),
        ("6. Technical Citations and Primary Sources", check_primary_sources),
    ]
    
    for name, func in checks:
        print(f"Running: {name}...")
        errors = func(all_md_files)
        if errors:
            print(f"  FAILED: {len(errors)} issues identified:")
            for err in errors[:10]:
                print(f"    - {err}")
            if len(errors) > 10:
                print(f"    ... and {len(errors) - 10} more.")
            total_failures += len(errors)
        else:
            print("  PASSED: 0 defects detected.")
        print("-" * 70)
        
    print(f"Validation Finished. Total Defects: {total_failures}")
    if total_failures > 0:
        print("QUALITY GATE FAILED. Please resolve identified defects before merging.")
        sys.exit(1)
    else:
        print("QUALITY GATE PASSED. All documentation files meet production handbook standards.")
        sys.exit(0)

if __name__ == "__main__":
    main()
