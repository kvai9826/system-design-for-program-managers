# Module 2.3: The CAP and PACELC Theorems

[Home](../README.md) > [Module 2: Data Architecture](./README.md) > **Chapter 2.3: The CAP and PACELC Theorems**

---

Distributed systems must navigate fundamental trade-offs imposed by the laws of physics and network unreliability. The CAP and PACELC theorems provide the theoretical foundation for explaining why no distributed database can offer both instantaneous global consistency and uninterrupted availability during network splits.

---

## 1. The CAP Theorem Explained

Formulated by Eric Brewer and later proved by Seth Gilbert and Nancy Lynch, the CAP theorem states that a distributed data store can guarantee at most two out of three properties simultaneously:

```mermaid
flowchart TD
    subgraph CAP [The CAP Theorem Core Dimensions]
        C[Consistency: Every read receives the most recent write or an error]
        A[Availability: Every non-failing node returns a non-error response]
        P[Partition Tolerance: System operates despite arbitrary packet drops]
    end

    classDef capStyle fill:#eff6ff,stroke:#2563eb,stroke-width:1px;
    class C,A,P capStyle;
```

### The Fundamental Reality: Partition Tolerance is Non-Negotiable
In physical networks, routers fail, optical fiber cables get cut, and network switches drop packets. Therefore, a distributed system **must** tolerate partitions ($P$). The real architectural choice is:

> **In the presence of a network partition ($P$), does the system choose Consistency ($CP$) or Availability ($AP$)?**

```mermaid
flowchart LR
    PartitionEvent{Network Partition Occurs!} --> PathCP[Choose CP: Reject Writes / Pause Service]
    PartitionEvent --> PathAP[Choose AP: Accept Writes on Both Sides]

    PathCP --> ResCP[Guarantees no stale or conflicting data, but clients experience errors]
    PathAP --> ResAP[Nodes continue serving requests locally, trading cross-partition consistency]

    classDef cpStyle fill:#fee2e2,stroke:#b91c1c,stroke-width:1px;
    classDef apStyle fill:#ecfdf5,stroke:#047857,stroke-width:1px;
    class PathCP,ResCP cpStyle;
    class PathAP,ResAP apStyle;
```

---

## 2. CP Systems vs AP Systems

| System Type | Core Behavior during Network Split | Representative Databases | Typical Business Domains |
| :--- | :--- | :--- | :--- |
| **CP (Consistency + Partition Tolerance)** | Unreachable nodes reject requests or time out until the partition heals to prevent data divergence | Google Cloud Spanner, CockroachDB, HBase, Redis Sentinel, ZooKeeper | Financial balances, stock inventory, flight seat booking, identity tokens |
| **AP (Availability + Partition Tolerance)** | Nodes on each side of the split accept reads and writes. Data reconciles when partition heals | Apache Cassandra, AWS DynamoDB (default), Couchbase, ScyllaDB | Social feeds, video view counts, shopping cart items, telemetry logs |

---

## 3. The PACELC Theorem: Beyond Failure States

The CAP theorem only describes what happens when the system fails (during a network partition). But distributed systems spend 99.9% of their operating time in a healthy, unpartitioned state.

Daniel Abadi developed the **PACELC theorem** to address normal state trade-offs:

$$\text{If } \mathbf{P} \text{ (Partition): Choose } \mathbf{A} \text{ or } \mathbf{C}; \quad \text{EL} \text{se: Choose } \mathbf{L} \text{ (Latency) or } \mathbf{C} \text{ (Consistency)}$$

```mermaid
graph TD
    Start[System State] --> IsPart{Is there an active network partition?}
    
    IsPart -->|Yes: Partition P| ChoiceP{Trade-off:}
    ChoiceP -->|A| AP[Availability: Cassandra, DynamoDB]
    ChoiceP -->|C| CP[Consistency: Spanner, HBase]

    IsPart -->|No: Else E| ChoiceE{Trade-off:}
    ChoiceE -->|L| EL[Low Latency: Replicate async, return immediately]
    ChoiceE -->|C| EC[High Consistency: Wait for multi-node consensus round-trips]

    classDef boxStyle fill:#f8fafc,stroke:#334155,stroke-width:1px;
    class Start,IsPart,ChoiceP,ChoiceE boxStyle;
```

### PACELC Database Classification

| Database | PACELC Classification | Architectural Mechanics |
| :--- | :--- | :--- |
| **DynamoDB** | **PA / EL** | If partitioned: Availability over Consistency. Else: Low Latency over strong consistency (asynchronous replication by default). |
| **Cassandra** | **PA / EL** | Tunable consistency, but defaults to high availability and low latency with eventual consistency. |
| **Cloud Spanner** | **PC / EC** | TrueTime atomic clocks enforce strict serializability. Consistency is prioritized during partitions and normal operations. |
| **MongoDB** | **PC / EC** | Routes primary writes with replica acknowledgement. Defaults to consistency over availability and latency. |
| **PostgreSQL (Async Replica)** | **PC / EL** | Single master enforces consistency on writes. Replicas accept lag for low-latency read queries. |

---

## 4. The Consistency Spectrum

Consistency in distributed systems is not binary (strong vs eventual). It exists on a continuum:

```mermaid
flowchart LR
    S1[Strict / Linearizable Consistency] --> S2[Sequential Consistency]
    S2 --> S3[Causal Consistency]
    S3 --> S4[Read-Your-Own-Writes]
    S4 --> S5[Eventual Consistency]

    classDef specStyle fill:#eff6ff,stroke:#1d4ed8,stroke-width:1px;
    class S1,S2,S3,S4,S5 specStyle;
```

1. **Linearizability (Strongest)**: Every read sees the latest globally committed write instantaneously, as if there were only one copy of data in the universe. Highest latency penalty.
2. **Sequential Consistency**: Operations appear in the order defined by the program, and all nodes see the same sequence of operations.
3. **Causal Consistency**: Causally related events (e.g. Question $\rightarrow$ Answer) appear in order across all nodes; unrelated operations can be observed in different orders.
4. **Eventual Consistency (Weakest)**: If no new writes occur, all replicas eventually converge to the same value. Lowest latency and highest throughput.

---

## 5. TPM Decision Framework: Aligning Business with Architecture

As a program manager, you must translate business requirements into distributed consistency parameters:

| Business Domain | Required Behavior | Recommended Choice | Rationale |
| :--- | :--- | :--- | :--- |
| **Core Banking Ledger** | Prevent negative balance and double-spending | **CP / EC** | Financial balance errors destroy trust and violate statutory regulatory compliance. |
| **E-Commerce Product Reviews** | Show newly posted reviews to shoppers | **AP / EL** | A shopper seeing a review 2 seconds late has zero business impact. Availability and low page latency drive sales. |
| **Collaborative Document Editing** | Avoid losing keystrokes during connection drops | **AP with CRDTs** | Local updates render with zero latency; Conflict-free Replicated Data Types merge edits deterministically. |
| **Inventory Reservation** | Ensure item is not sold to two buyers | **CP / EC** | Overselling generates customer support escalations, cancellation penalties, and logistical overhead. |

---

## 6. TPM Review Checklist

When evaluating distributed storage trade-offs:

- [ ] Does the product experience tolerate eventual consistency (stale reads of 50ms to 2000ms)?
- [ ] For AP systems, how are write conflicts resolved (Last-Write-Wins, vector clocks, or application-level merges)?
- [ ] What is the exact customer experience when a network partition forces a CP system to reject requests?
- [ ] Has the engineering team configured timeout thresholds and circuit breakers for quorum reads?
- [ ] Are business metrics (conversion rates, revenue) balanced against the latency penalty of strong consistency?

---

## 7. Primary Sources and Further Reading

- **CAP Proof**: *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services* by Seth Gilbert and Nancy Lynch (ACM SIGACT News, 2002).
- **CAP 12-Year Retrospective**: *CAP Twelve Years Later: How the Rules Have Changed* by Eric Brewer (IEEE Computer, 2012).
- **PACELC Formulation**: *Consistency Tradeoffs in Modern Distributed Database System Design: CAP is Only Part of the Story* by Daniel J. Abadi (IEEE Computer, 2012).
- *Principles of Eventual Consistency* by Sebastian Burckhardt (Foundations and Trends in Programming Languages, 2014).
