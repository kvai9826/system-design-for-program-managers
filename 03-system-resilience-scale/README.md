# Module 3: System Resilience, Scale, and Non-Functional Requirements

[Home](../README.md) > **Module 3: Resilience & Scale**

---

## Overview

A system that functions perfectly in a development environment can quickly fail in production when subjected to unpredictable real-world traffic spikes, hardware crashes, and network latency anomalies. This module equips Technical Program Managers with the frameworks and patterns needed to design resilient, fault-tolerant, horizontally scalable architectures that meet strict contractual Service Level Agreements (SLAs).

---

## Module Learning Objectives

1. **Stateless Scalability**: Architect stateless application tiers by externalizing session state, decoupling reads and writes via CQRS, and implementing graceful auto-scaling policies.
2. **Failure Isolation**: Protect platforms from cascading failures using Circuit Breakers, Exponential Backoff with randomized full jitter, Bulkheads, and distributed Idempotency Keys.
3. **Rate Limiting**: Evaluate rate-limiting algorithms (Token Bucket, Leaky Bucket, Sliding Window Counter) to protect downstream services from abusive traffic and API scraping.
4. **Reliability Governance**: Master the SLI/SLO/SLA hierarchy, calculate high availability ("The Nines") mathematics, enforce Error Budget policies, and establish Disaster Recovery (RPO/RTO) baselines.

---

## Chapter Directory

| Chapter | Title | Focus Areas | Key Trade-offs |
| :--- | :--- | :--- | :--- |
| **[3.1](./01-scalability-patterns.md)** | Architectural Scalability Patterns | Scale-Up vs Scale-Out, stateless application tier, CQRS, background workers | Infrastructure cost vs elasticity, eventual read consistency |
| **[3.2](./02-fault-tolerance-patterns.md)** | Fault Tolerance, Resilience & Rate Limiting | Circuit breakers, exponential backoff + jitter, rate limiting, bulkheads | Failure isolation vs fallback complexity, client retry storms |
| **[3.3](./03-slas-slis-slos-nfrs.md)** | High Availability, NFRs & Disaster Recovery | SLI/SLO/SLA, "The Nines" math, error budgets, RPO/RTO, DR topologies | Availability vs infrastructure cost, feature velocity vs reliability |

---

## Suggested Prerequisites

- Completion of [Module 1: Foundations](../01-foundations/README.md) and [Module 2: Data Architecture](../02-data-architecture/README.md).
- Understanding of basic probability and statistical distributions (p50, p95, p99 latency percentiles).
