#!/usr/bin/env python3
"""
Bundle generator for LLM ingestion (llms.txt and llms-full.txt).
Consolidates the complete System Design for Program Managers curriculum into a single
prompt-optimized text file (~45k tokens) ready for ingestion into ChatGPT, Claude, Gemini,
NotebookLM, or Cursor.
"""

import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

COURSE_FILES = [
    ("Curriculum Overview & Architecture Map", "README.md"),
    ("Master Architectural Glossary", "GLOSSARY.md"),
    ("Module 1 Overview: Foundations", "01-foundations/README.md"),
    ("Module 1 Chapter 1: Client-Server Networking & Protocols", "01-foundations/01-client-server-networking.md"),
    ("Module 1 Chapter 2: Load Balancing & API Gateways", "01-foundations/02-load-balancing-gateways.md"),
    ("Module 1 Chapter 3: Caching Strategies & Memory Tiers", "01-foundations/03-caching-strategies.md"),
    ("Module 2 Overview: Data Architecture & Storage Engines", "02-data-architecture/README.md"),
    ("Module 2 Chapter 1: Databases: SQL vs NoSQL Internals", "02-data-architecture/01-databases-sql-vs-nosql.md"),
    ("Module 2 Chapter 2: Sharding, Replication & Partitioning", "02-data-architecture/02-sharding-replication.md"),
    ("Module 2 Chapter 3: CAP and PACELC Theorems in Practice", "02-data-architecture/03-cap-pacelc-theorems.md"),
    ("Module 2 Chapter 4: Message Queues & Event Streaming", "02-data-architecture/04-message-queues-streaming.md"),
    ("Module 3 Overview: Resilience & High Availability", "03-system-resilience-scale/README.md"),
    ("Module 3 Chapter 1: Scalability Patterns & Microservices", "03-system-resilience-scale/01-scalability-patterns.md"),
    ("Module 3 Chapter 2: Fault Tolerance & Self-Healing Architecture", "03-system-resilience-scale/02-fault-tolerance-patterns.md"),
    ("Module 3 Chapter 3: Non-Functional Requirements: SLAs, SLIs & SLOs", "03-system-resilience-scale/03-slas-slis-slos-nfrs.md"),
    ("Module 4 Overview: TPM Execution Framework", "04-tpm-execution-framework/README.md"),
    ("Module 4 Chapter 1: The TPM System Design Blueprint", "04-tpm-execution-framework/01-tpm-system-design-framework.md"),
    ("Module 4 Chapter 2: Back-of-the-Envelope Math & Capacity Planning", "04-tpm-execution-framework/02-back-of-the-envelope-math.md"),
    ("Module 4 Chapter 3: Migration & Zero-Downtime Deployment Strategies", "04-tpm-execution-framework/03-migration-deployment-strategies.md"),
    ("Module 4 Chapter 4: Observability, Governance & Telemetry", "04-tpm-execution-framework/04-observability-governance.md"),
    ("Module 5 Overview: Real-World Case Studies", "05-real-world-case-studies/README.md"),
    ("Case Study 1: High-Throughput URL Shortener", "05-real-world-case-studies/01-url-shortener.md"),
    ("Case Study 2: Multi-Channel Notification Engine", "05-real-world-case-studies/02-notification-engine.md"),
    ("Case Study 3: Global Video Streaming Platform", "05-real-world-case-studies/03-video-streaming-platform.md"),
    ("Case Study 4: High-Concurrency Ride-Sharing Dispatch", "05-real-world-case-studies/04-ride-sharing-dispatch.md"),
    ("Case Study 5: Distributed Flash-Sale E-Commerce Checkout", "05-real-world-case-studies/05-distributed-ecommerce-checkout.md"),
]

def build_llms_txt() -> str:
    lines = [
        "# System Design for Program Managers",
        "",
        "> A book-grade distributed systems reference handbook and curriculum built specifically for Technical Program Managers (TPMs), Product Managers, and engineering leaders.",
        "",
        "## Core Curriculum Modules",
        "- [Module 1: Foundations](01-foundations/README.md): Client-server networking, HTTP/3, QUIC, Layer 4 vs Layer 7 load balancing, and multi-tier caching.",
        "- [Module 2: Data Architecture](02-data-architecture/README.md): SQL vs NoSQL storage engines, LSM vs B-Trees, sharding, PACELC theorem, Kafka, and streaming.",
        "- [Module 3: Resilience and Scale](03-system-resilience-scale/README.md): Microservice scalability patterns, fault tolerance, circuit breakers, SLAs, SLIs, and SLOs.",
        "- [Module 4: TPM Execution Framework](04-tpm-execution-framework/README.md): ADR templates, worked design reviews, back-of-the-envelope math, and zero-downtime migrations.",
        "- [Module 5: Real-World Case Studies](05-real-world-case-studies/README.md): 5 production architectures with formal ADRs, FMEA failure matrices, API contracts, and RACI plans.",
        "- [Glossary](GLOSSARY.md): 50+ standardized distributed systems definitions, latency tiers, and reference formulas.",
        "",
        "## Full Consolidated Bundle",
        "- [Full Course Text (Prompt-Ready)](llms-full.txt): Complete consolidated handbook text (~45k tokens) optimized for direct context ingestion into Claude, ChatGPT, Gemini, or NotebookLM.",
        ""
    ]
    return "\n".join(lines)

def build_llms_full_txt() -> str:
    header = [
        "# System Design for Program Managers: The Complete Architectural Handbook",
        "Author: Karthikeya Vaibhav (https://github.com/kvai9826/system-design-for-program-managers)",
        "",
        "AI ASSISTANT INSTRUCTIONS:",
        "You are an expert Principal Systems Architect and Technical Program Management (TPM) Mentor.",
        "This document contains the complete, authoritative curriculum of the 'System Design for Program Managers' handbook.",
        "Use this knowledge base to answer architectural interview questions, review system designs, evaluate non-functional requirements (SLAs/SLIs/SLOs), formulate Architectural Decision Records (ADRs), calculate capacity and wire-protocol overhead, and design resilient distributed systems.",
        "",
        "=" * 80,
        "TABLE OF CONTENTS",
        "=" * 80,
    ]
    
    for idx, (title, rel_path) in enumerate(COURSE_FILES, 1):
        header.append(f"{idx:02d}. {title} ({rel_path})")
    
    header.append("=" * 80)
    header.append("")
    
    sections = ["\n".join(header)]
    
    for idx, (title, rel_path) in enumerate(COURSE_FILES, 1):
        file_path = REPO_ROOT / rel_path
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}", file=sys.stderr)
            continue
        
        content = file_path.read_text(encoding="utf-8").strip()
        
        section_banner = [
            "",
            "=" * 80,
            f"SECTION {idx:02d}: {title.upper()}",
            f"FILE: {rel_path}",
            "=" * 80,
            "",
            content,
            ""
        ]
        sections.append("\n".join(section_banner))
    
    return "\n".join(sections)

def main():
    print("Building llms.txt index...")
    llms_txt_content = build_llms_txt()
    (REPO_ROOT / "llms.txt").write_text(llms_txt_content, encoding="utf-8")
    print(f"  Generated llms.txt ({len(llms_txt_content)} bytes)")
    
    print("Building consolidated llms-full.txt bundle...")
    llms_full_content = build_llms_full_txt()
    full_path = REPO_ROOT / "llms-full.txt"
    full_path.write_text(llms_full_content, encoding="utf-8")
    
    word_count = len(llms_full_content.split())
    est_tokens = int(word_count * 1.33)
    print(f"  Generated llms-full.txt ({len(llms_full_content):,} bytes, ~{word_count:,} words, ~{est_tokens:,} tokens)")
    
    # Check for em dashes
    em_dashes = [c for c in llms_full_content if c in ('—', '–')]
    if em_dashes:
        print(f"Warning: Found {len(em_dashes)} em/en dashes in generated bundle!", file=sys.stderr)
    else:
        print("  Verified: Zero em/en dashes in generated bundle.")
        
    if "--copy" in sys.argv:
        try:
            if sys.platform == "darwin":
                subprocess.run(["pbcopy"], input=llms_full_content.encode("utf-8"), check=True)
                print("  Copied complete course bundle to macOS clipboard (pbcopy)!")
            elif sys.platform.startswith("linux"):
                subprocess.run(["xclip", "-selection", "clipboard"], input=llms_full_content.encode("utf-8"), check=True)
                print("  Copied complete course bundle to Linux clipboard (xclip)!")
        except Exception as e:
            print(f"  Clipboard copy failed: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
