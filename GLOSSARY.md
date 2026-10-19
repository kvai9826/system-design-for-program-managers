# Distributed Systems Glossary for Program Managers

[Home](./README.md) > **Architectural Glossary**

This glossary defines foundational distributed systems, cloud infrastructure, and technical program governance terminology. Every Technical Program Manager should understand these definitions, formulas, and architectural trade-offs.

---

## A

### ACID
A set of properties guaranteeing that database transactions are processed reliably:
- **Atomicity**: All operations in a transaction succeed, or the entire transaction is rolled back.
- **Consistency**: Data written to the database satisfies all defined schema constraints, cascades, and triggers.
- **Isolation**: Concurrent transactions execute without cross-contaminating each other.
- **Durability**: Once committed, transaction data survives power loss, system crashes, and reboots via write-ahead logging (WAL).

### Active-Active vs Active-Passive
- **Active-Active**: Redundant compute and database nodes simultaneously receive and process live production traffic, maximizing infrastructure utilization.
- **Active-Passive**: Traffic routes exclusively to a primary instance; a standby replica remains idle until a failure triggers failover via heartbeat protocols (e.g. VRRP).

### Architectural Decision Record (ADR)
A lightweight document capturing a significant technical choice, including its context, alternatives considered, decision outcome, and long-term consequences.

---

## B

### Backpressure
A flow-control mechanism where a downstream consumer signals an upstream producer to slow down or pause message transmission when buffer capacity approaches saturation.

### BASE
The philosophical counterpoint to ACID in distributed NoSQL databases:
- **Basically Available**: The system guarantees availability by continuing to operate despite node partitions.
- **Soft State**: System data may drift or change over time without explicit user input due to eventual consistency.
- **Eventual Consistency**: Replicas will converge to identical values given sufficient time without new writes.

### Bloom Filter
A space-efficient, probabilistic data structure used to test set membership. A Bloom filter can return false positives (saying an item exists when it does not), but **never returns false negatives** (if it says an item does not exist, it definitely does not exist). Frequently placed in front of caches to prevent Cache Penetration.

### Bulkhead Pattern
An architectural isolation pattern named after watertight compartments in ships. By segregating thread pools, connection limits, and memory quotas across services, a failure in one non-critical component (e.g. PDF generation) cannot exhaust resources required for critical paths (e.g. user authentication).

---

## C

### Cache Avalanche
A catastrophic failure mode occurring when hundreds of thousands of cache keys expire simultaneously, causing the entire incoming traffic volume to hit downstream databases. Mitigated by adding randomized jitter to TTL expirations.

### Cache Penetration
An anti-pattern where clients repeatedly query non-existent keys (e.g. negative IDs). Cache misses force repeated database reads. Mitigated by Bloom filters or caching null results with short TTLs.

### Cache Stampede (Thundering Herd)
A sudden wave of concurrent cache misses occurring when a viral or heavily accessed key expires, causing thousands of application threads to query the primary database for the exact same record at the same millisecond. Mitigated by distributed mutex locking or probabilistic early regeneration (XFetch).

### Cache-Aside (Lazy Loading)
A caching pattern where the application code directly coordinates between cache and database: querying cache first, reading database on miss, and populating cache before returning.

### CAP Theorem
Formulated by Eric Brewer and proved by Gilbert and Lynch: a distributed data store can guarantee at most two out of Consistency, Availability, and Partition Tolerance simultaneously. In real-world physical networks, partitions ($P$) are inevitable; systems must choose between Consistency ($CP$) or Availability ($AP$).

### Change Data Capture (CDC)
A software design pattern that monitors and captures committed row-level changes from a database transaction log (e.g. Debezium reading MySQL binlog) and streams them to message brokers like Kafka.

### Circuit Breaker Pattern
A stability pattern that prevents an application from repeatedly attempting an operation that is failing. Transitions across three states: **Closed** (normal execution), **Open** (failing fast immediately without network calls), and **Half-Open** (allowing canary probe requests to verify downstream recovery).

### Consistent Hashing
A distributed hashing technique mapping nodes and keys onto a circular hash ring ($0$ to $2^{32}-1$). When servers are added or removed, only $K/N$ keys need to be rebalanced (where $K$ is total keys, $N$ is server count). Uses virtual nodes (vnodes) to achieve uniform distribution and prevent hot spots.

### CQRS (Command Query Responsibility Segregation)
An architectural pattern that separates mutation operations (Commands: `INSERT`, `UPDATE`) from read operations (Queries: `SELECT`) into independent models and databases.

---

## D

### Dead Letter Queue (DLQ)
A specialized message queue dedicated to storing malformed messages or poison pills that have exceeded retry thresholds, preventing them from blocking consumer progress.

### Distributed Tracing
A diagnostic methodology tracking the end-to-end path of an execution across multiple microservices by injecting a unique **Trace ID** and propagating it through HTTP headers (W3C `traceparent`).

---

## E

### Error Budget
The maximum permissible unreliability of a service over a rolling window (typically 30 days):
$$\text{Error Budget} = 100\% - \text{SLO}$$
When an error budget is exhausted, product feature deployments freeze until reliability engineering remediates the root cause.

### Exponential Backoff with Jitter
A retry algorithm where clients progressively double wait duration between retries, adding randomized noise (jitter) to prevent synchronized waves of traffic (retry storms).

---

## H

### H3 Spatial Index
An open-source hexagonal hierarchical spatial indexing system developed by Uber. Partitions the Earth into hexagonal cells where all 6 neighboring cells are equidistant, eliminating corner distortions found in square grids (Geohashes).

### High Availability ("The Nines")
A metric quantifying the proportion of time a system is operational. Calculated as:
$$\text{Availability} = \frac{\text{Uptime}}{\text{Uptime} + \text{Downtime}} \times 100\%$$
- **99.9% (Three Nines)**: 8.76 hours downtime/year.
- **99.99% (Four Nines)**: 52.6 minutes downtime/year.
- **99.999% (Five Nines)**: 5.26 minutes downtime/year.

---

## I

### Idempotency
A mathematical property where executing an operation multiple times produces the exact same outcome as executing it once:
$$f(f(x)) = f(x)$$
In distributed systems, mutation APIs pass an **Idempotency Key** to ensure network retries do not duplicate state changes (e.g. double-charging a credit card).

---

## L

### Layer 4 vs Layer 7 Load Balancing
- **Layer 4**: Operates at the transport layer (TCP/UDP). Routes traffic based on source/destination IP addresses and ports without inspecting application payloads. Ultra-fast, minimal CPU overhead.
- **Layer 7**: Operates at the application layer (HTTP/HTTPS). Inspects URIs, HTTP headers, cookies, and payloads. Enables path-based routing, TLS termination, and canary traffic splitting.

### LSM-Tree (Log-Structured Merge-Tree)
A write-optimized storage engine (used in Cassandra, RocksDB) that appends writes sequentially to an in-memory MemTable and write-ahead log (WAL), later flushing them sequentially to immutable SSTables on disk. Trades read latency for extreme write throughput.

---

## O

### OpenTelemetry (OTel)
A vendor-neutral, open-source observability framework under the CNCF providing standardized APIs, libraries, and agents to collect metrics, logs, and distributed traces.

---

## P

### PACELC Theorem
An extension of the CAP theorem by Daniel Abadi addressing normal operating conditions:
$$\text{If } \mathbf{P} \text{ (Partition): Choose } \mathbf{A} \text{ or } \mathbf{C}; \quad \text{EL} \text{se: Choose } \mathbf{L} \text{ (Latency) or } \mathbf{C} \text{ (Consistency)}$$

### Poison Pill
A malformed message payload (e.g. invalid syntax) that causes consumer applications to crash on every processing attempt. Handled via Dead Letter Queues (DLQ).

---

## R

### Rate Limiting
A defensive traffic-shaping technique restricting incoming request volume per client. Common algorithms include **Token Bucket** (allows controlled bursts), **Leaky Bucket** (smooths traffic to a constant rate), and **Sliding Window Counter** (approximates rolling windows).

### Recovery Point Objective (RPO)
The maximum acceptable duration of data loss measured backward in time from a disaster event (e.g. RPO of 15 minutes means at most 15 minutes of uncommitted transactional data can be lost).

### Recovery Time Objective (RTO)
The maximum acceptable duration of downtime required to restore normal system operations following an outage (e.g. RTO of 1 hour means secondary infrastructure must be fully serving traffic within 60 minutes).

---

## S

### Saga Pattern
A distributed transaction pattern coordinating multiple local transactions across microservices without distributed two-phase locking. If a downstream step fails, the Saga orchestrator executes **compensating transactions** to roll back preceding steps in reverse order.

### SLA vs SLO vs SLI
- **SLI (Service Level Indicator)**: A quantifiable metric tracking service health in real time (e.g. percentage of successful requests under 200ms).
- **SLO (Service Level Objective)**: The internal engineering target agreed upon by Product, TPM, and Engineering (e.g. 99.9% of requests meet SLI over 30 days).
- **SLA (Service Level Agreement)**: The contractual promise to customers with financial penalties (service credits) if breached.

### Strangler Fig Pattern
An incremental legacy migration strategy where an API Gateway or facade proxy intercepts incoming traffic, gradually routing specific service paths to new microservices until the legacy monolith can be safely decommissioned.

---

## W

### WebSockets vs Server-Sent Events (SSE)
- **WebSockets**: Full-duplex, bidirectional communication over a single persistent TCP socket. Ideal for chat, gaming, and collaborative editing.
- **Server-Sent Events (SSE)**: Unidirectional streaming from server to client over standard HTTP. Ideal for live dashboards, stock tickers, and LLM text generation.
