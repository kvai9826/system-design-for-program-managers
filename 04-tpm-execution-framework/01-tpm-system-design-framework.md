# Module 4.1: The TPM System Design Framework

[Home](../README.md) > [Module 4: TPM Execution Framework](./README.md) > **Chapter 4.1: The TPM System Design Framework**

---

System design interviews and architecture design reviews evaluate Technical Program Managers differently than Software Engineers. While software engineers are assessed on code constructs, concurrency primitives, and algorithmic efficiency, TPMs are evaluated on **architectural breadth, trade-off evaluation, cross-functional risk mitigation, capacity planning, and project delivery roadmaps**.

---

## 1. SWE vs TPM System Design Lens

Understanding the evaluation criteria is critical for succeeding in TPM interviews at top technology firms (Google, Meta, Amazon, Microsoft, Uber).

```mermaid
flowchart LR
    subgraph SWELens [Software Engineer Lens]
        direction TB
        S1[Low-level data structures]
        S2[Thread locking & memory pointers]
        S3[Algorithm time/space complexity]
        S4[Component-level implementation details]
    end

    subgraph TPMLens [Technical Program Manager Lens]
        direction TB
        T1[Cross-system architecture & boundaries]
        T2[Capacity planning & infrastructure cost]
        T3[Single points of failure & disaster recovery]
        T4[Cross-team dependencies & migration milestones]
    end

    classDef sweStyle fill:#eff6ff,stroke:#2563eb,stroke-width:1px;
    classDef tpmStyle fill:#ecfdf5,stroke:#047857,stroke-width:1px;
    class SWELens sweStyle;
    class TPMLens tpmStyle;
```

---

## 2. The 5-Stage TPM System Design Blueprint

Use this structured five-stage framework to drive any 45-minute architectural interview or cross-functional architecture review.

```mermaid
flowchart TD
    S1[Stage 1: Clarify Scope & Non-Functional Requirements<br/>5 to 7 Minutes] --> S2[Stage 2: High-Level Architecture & API Boundaries<br/>10 Minutes]
    S2 --> S3[Stage 3: Deep-Dive on Core Components & Data Model<br/>12 to 15 Minutes]
    S3 --> S4[Stage 4: Scaling, Bottlenecks & Failure Modes<br/>8 to 10 Minutes]
    S4 --> S5[Stage 5: TPM Execution Lens: Dependencies, Phasing & Cost<br/>5 Minutes]

    classDef sStyle fill:#f8fafc,stroke:#334155,stroke-width:1px;
    class S1,S2,S3,S4,S5 sStyle;
```

---

## 3. Step-by-Step Blueprint Breakdown

### Stage 1: Clarify Scope and Requirements (5 to 7 Minutes)
Never jump straight into drawing boxes. Clarify functional and non-functional requirements to set clear boundaries.

- **Functional Requirements (What the system does)**:
  - Identify 2 or 3 core use cases (e.g. "Users can upload video segments; users can stream video adaptively").
  - Explicitly state out-of-scope features (e.g. "Video comments and recommendations are out of scope for today").
- **Non-Functional Requirements (How well it performs)**:
  - Scale: Monthly active users (MAU), daily active users (DAU), read/write ratio.
  - Latency: Target p95 / p99 response times (e.g. p99 < 200ms).
  - Availability: Target "nines" (e.g. 99.99% availability).
  - Data Retention & Compliance: Data durability, GDPR, data residency constraints.

### Stage 2: High-Level Architecture (10 Minutes)
Establish the end-to-end data flow before zooming into details.

- Draw the client ingress path: Client $\rightarrow$ DNS $\rightarrow$ CDN $\rightarrow$ Load Balancer $\rightarrow$ API Gateway.
- Partition the backend into logical domain services (e.g. Ingestion Service, Processing Service, Query Service).
- Define primary data storage tiers (Transactional DB, Cache, Object Storage).
- Define core API contracts (e.g. `POST /api/v1/trips`, `GET /api/v1/drivers/nearby`).

### Stage 3: Deep-Dive and Data Modeling (12 to 15 Minutes)
Zoom in on the 1 or 2 most complex components in the design.

- **Data Model**:
  - Relational vs NoSQL selection with rationale.
  - Primary keys, foreign keys, partition keys, and secondary indexing.
- **Data Flow Mechanics**:
  - Walk through an end-to-end read and write sequence step-by-step.
  - Explain cache population, invalidation triggers, and asynchronous messaging queues.

### Stage 4: Scaling, Bottlenecks, and Failure Modes (8 to 10 Minutes)
Proactively attack your own architecture before the interviewer or team points out flaws.

- **Single Points of Failure (SPOFs)**: What happens if the load balancer, primary database, or Redis master dies?
- **Hot Partitions**: How do we handle sudden traffic surges from viral events or celebrity accounts?
- **Resilience Controls**: Where are circuit breakers, rate limiters, DLQs, and fallback mechanisms placed?

### Stage 5: The TPM Execution Lens (5 Minutes)
This stage distinguishes strong TPM candidates from engineers:

- **Cross-Team Dependencies**: Identify teams involved (e.g. Infrastructure, Security, Mobile Client, Data Platform).
- **Migration & Phasing**: How do we transition from legacy systems without downtime (Strangler Fig pattern, dark launching)?
- **Infrastructure Cost Sizing**: Rough cloud budget estimation (compute, network egress, storage tiering).
- **Launch Risks & Rollback Criteria**: Specific telemetry metrics that trigger an automated abort of the rollout.

---

## 4. Time Allocation Breakdown (45-Minute Interview)

| Stage | Activity | Time Target | Goal |
| :--- | :--- | :--- | :--- |
| **Stage 1** | Scope, NFRs & Calculations | 5 to 7 mins | Eliminate ambiguity; establish agreed scale parameters |
| **Stage 2** | High-Level Architecture Diagram | 10 mins | Establish full end-to-end flow without getting bogged down |
| **Stage 3** | Component Deep-Dive & Data Model | 12 to 15 mins | Demonstrate technical depth on primary system challenges |
| **Stage 4** | Bottlenecks, Scale & Resilience | 8 to 10 mins | Prove operational durability and failure handling |
| **Stage 5** | Execution, Phasing & Trade-offs | 5 mins | Demonstrate program delivery, risk mitigation, and leadership |

---

## 5. Architectural Decision Records (ADRs)

In enterprise programs, architectural choices must be documented to prevent endless re-litigation of technical debates. A Technical Program Manager owns the ADR process:

### Standard ADR Template (Michael Nygard Format)

```markdown
# ADR-004: Adoption of Apache Kafka for Asynchronous Order Event Streaming

## Status
Accepted (Date: 2026-03-15)

## Context
Our monolithic ordering service handles 15,000 orders/minute. Post-order workflows (inventory decrement, fraud analysis, invoice PDF generation, customer email notification) are currently executed via synchronous HTTP RPC. Downstream latency spikes in the invoice generation service are causing timeout cascades and order dropouts.

## Decision
We will decouple post-order fulfillment workflows using Apache Kafka. The checkout API will commit the order record to the primary database, publish an `OrderPlaced` event to Kafka topic `orders.v1`, and return HTTP 201 immediately to the client.

## Consequences
- **Positive**: Web request latency drops from 850ms to 65ms. Downstream outages no longer block checkout.
- **Negative**: Downstream consumers require idempotency keys to handle duplicate events. Introduces operational overhead of managing Kafka broker clusters and ZooKeeper/KRaft.

## Compliance & Monitoring
Order event lag must be monitored in Datadog with an alert threshold of lag > 5,000 messages.
```

---

## 6. Worked Design Review Examples: How a Strong TPM Challenges Proposals

During architectural review boards, a TPM must evaluate proposals critically. Below are three real-world examples:

### Example 1: E-Commerce Inventory Reservation Proposal
- **Proposed Architecture**: Checkout service makes synchronous HTTP REST calls to the Inventory Service, which runs `SELECT stock FROM inventory WHERE item_id = ? FOR UPDATE` on a single PostgreSQL database.
- **Questions a Strong TPM Must Ask**:
  1. *Throughput Ceiling*: A relational row-level lock on PostgreSQL maxes out at ~2,000 writes/sec. During a flash sale of 50,000 QPS, how will this avoid connection pool exhaustion?
  2. *Blast Radius*: If the inventory service experiences a latency spike, how do we prevent checkout threads from getting exhausted and dropping cart views?
  3. *Idempotency*: If the client times out after 1,000ms while the database write actually succeeded, what prevents duplicate stock reservation on retry?

### Example 2: IoT Fleet Telemetry Ingestion Proposal
- **Proposed Architecture**: 250,000 connected vehicles ping telemetry every 5 seconds directly to an API Gateway, which inserts rows into a standard relational database with multiple secondary indexes on timestamp and vehicle ID.
- **Questions a Strong TPM Must Ask**:
  1. *Storage Engine Suitability*: Ingestion rate is 50,000 writes/sec. A B-Tree storage engine requires random disk page writes for secondary indexes. Why are we not using an LSM-Tree write-optimized engine (Cassandra or ScyllaDB) or time-series database?
  2. *Buffer Layer*: If the database undergoes a failover maintenance window for 30 seconds, where do the 1.5 million in-flight vehicle pings get buffered to prevent permanent data loss?
  3. *Retention and Cold Storage*: At 50,000 writes/sec, the database accumulates 4.3 Billion rows per day. What is the automated partitioning and cold storage tiering policy to prevent disk saturation?

### Example 3: Global User Feed Comments Proposal
- **Proposed Architecture**: Multi-region active-active relational database deployment where users in London and Tokyo write comments to local read-write database instances, replicating synchronously across the globe.
- **Questions a Strong TPM Must Ask**:
  1. *Physical Latency Bounds*: Synchronous consensus across Tokyo and London takes at least 150ms per write due to speed-of-light networking limits. Are users willing to wait 250ms+ just to post a casual comment?
  2. *CAP Theorem Alignment*: User comments are inherently tolerant of eventual consistency. Why are we paying 5x cloud infrastructure costs for synchronous cross-region consensus instead of an AP asynchronous replication model?

---

## 7. Common Anti-Patterns to Avoid

| Anti-Pattern | Description | Correction |
| :--- | :--- | :--- |
| **The Immediate Box Drawer** | Drawing diagrams before asking clarifying scale or business questions | Spend the first 5 minutes agreeing on requirements, QPS, and scope |
| **The Pure SWE Trap** | Diving deep into single-machine thread concurrency or Python code | Elevate discussion to distributed architecture, data contracts, and scaling |
| **Buzzword Stacking** | Throwing "Kafka, Redis, and Kubernetes" at every problem without justification | Explain *why* a technology fits the specific read/write access pattern |
| **Silent Architect** | Designing in complete silence without narrating thought processes | Think out loud; present trade-offs transparently: "Option A gives X but costs Y" |
| **Ignoring Operational Cost** | Proposing infinite multi-region replication for non-critical features | Highlight cost vs reliability trade-offs: "99.9% is sufficient and saves 60% cloud spend" |

---

## 8. TPM Review Checklist

Before presenting an architecture to leadership or interview panels:

- [ ] Did I clarify both functional goals and non-functional targets (SLAs, scale, latency)?
- [ ] Is my data store selection justified by specific read/write access patterns?
- [ ] Have I proactively identified the top single points of failure (SPOFs)?
- [ ] Did I outline the rollout phases, cross-team dependencies, and rollback triggers?
- [ ] Am I prepared to defend the cost implications of high availability choices?

---

## 9. Primary Sources and Further Reading

- *Software Architecture: The Hard Parts: Modern Input for Objectives, Granularity, and Coupling* by Neal Ford, Mark Richards, Pramod Sadalage, and Zhamak Dehghani (O'Reilly Media, 2021).
- **Architecture Decision Records**: *Documenting Architecture Decisions* by Michael Nygard (cognitect.com, 2011).
- *Staff Engineer: Leadership Beyond the Management Track* by Will Larson (Stripe Press, 2021) - Chapters on Technical Strategy and Architecture Reviews.
