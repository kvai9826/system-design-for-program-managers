# Module 1.3: Distributed Caching Strategies

[Home](../README.md) > [Module 1: Foundations](./README.md) > **Chapter 1.3: Caching Strategies**

---

Caching is one of the most effective techniques to reduce latency, protect downstream databases from traffic spikes, and optimize cloud infrastructure costs. For technical program managers, understanding cache design patterns, invalidation strategies, and failure modes prevents costly production outages.

---

## 1. Multi-Tier Caching Architecture

Caching operates across every layer of the modern technology stack. A well-architected system leverages multiple cache boundaries to maximize hit rates and minimize database IOPS.

```mermaid
flowchart TD
    Client[Client Device / Browser] -->|1. Browser Cache: Local Storage / Service Worker| Client
    Client -->|2. Edge Cache| CDN[Content Delivery Network: Static & Geo Assets]
    CDN -->|3. Gateway Cache| GW[API Gateway / Reverse Proxy Cache: Shared HTTP Responses]
    GW -->|4. App Process Memory| App[Application Pod: In-Memory L1 Cache Caffeine/Go-Cache]
    App -->|5. Distributed Cache| DistCache[(Distributed L2 Cache: Redis / Memcached Cluster)]
    DistCache -->|6. Storage Engine Cache| DB[(Primary Database: Buffer Pool / Page Cache)]

    classDef cacheStyle fill:#fef3c7,stroke:#d97706,stroke-width:1px;
    class CDN,GW,DistCache cacheStyle;
```

---

## 2. Read and Write Caching Patterns

The choice of caching pattern defines the consistency contract between the application, the cache, and the underlying database.

```mermaid
flowchart TD
    subgraph ReadPatterns [Read Caching Strategies]
        direction LR
        CA[Cache-Aside / Lazy Loading: App coordinates cache and DB]
        RT[Read-Through: App queries Cache, Cache loads DB on miss]
    end

    subgraph WritePatterns [Write Caching Strategies]
        direction LR
        WT[Write-Through: App writes Cache, Cache writes DB synchronously]
        WB[Write-Behind / Write-Back: App writes Cache, Cache queues DB async]
        WA[Write-Around: App writes DB directly, Cache populated on read]
    end

    classDef rstyle fill:#eff6ff,stroke:#2563eb,stroke-width:1px;
    classDef wstyle fill:#ecfdf5,stroke:#059669,stroke-width:1px;
    class CA,RT rstyle;
    class WT,WB,WA wstyle;
```

### 1. Cache-Aside (Lazy Loading)

The application code directly coordinates between the cache and the database.

```mermaid
sequenceDiagram
    autonumber
    participant App as Application Service
    participant Cache as Redis Cache
    participant DB as Database

    App->>Cache: 1. GET key
    alt Cache Hit
        Cache-->>App: 2. Return cached value (Sub-millisecond)
    else Cache Miss
        Cache-->>App: 2. Return null (miss)
        App->>DB: 3. Query primary database
        DB-->>App: 4. Return row data
        App->>Cache: 5. SET key = data (with TTL)
        App-->>App: 6. Process request
    end
```

- **Pros**: Only requested data is cached (memory efficient); cache failure does not crash the system (gracefully degrades to direct database queries).
- **Cons**: High latency penalty on cache miss (3 network round-trips); potential stale data if records are updated in the database directly without cache invalidation.

### 2. Write-Through vs Write-Behind (Write-Back)

| Dimension | Write-Through | Write-Behind (Write-Back) | Write-Around |
| :--- | :--- | :--- | :--- |
| **Data Flow** | App writes to Cache; Cache writes to DB synchronously before returning success | App writes to Cache; Cache writes to DB asynchronously in batches | App writes directly to DB; Cache is bypassed and populated on next read |
| **Write Latency** | Higher (waits for both memory cache and disk DB write to commit) | Ultra-low (returns immediately after memory write confirms) | Standard database disk write latency |
| **Consistency** | High consistency between cache and primary store | Eventual consistency; data loss risk if cache crashes before flush | Cache holds stale data unless explicitly invalidated on write |
| **Ideal For** | Financial balances, user permissions, security tokens | Heavy write workloads, clickstream tracking, IoT telemetry | Infrequently read logs, large batch file uploads |

---

## 3. Cache Eviction Policies

When memory reaches capacity limits, the cache engine must evict items to make room for new entries.

- **LRU (Least Recently Used)**: Evicts items that have not been accessed for the longest time. Standard default for general-purpose workloads.
- **LFU (Least Frequently Used)**: Tracks access counts and evicts items with the lowest access frequency. Ideal for stable, predictable hot-keys.
- **FIFO (First In, First Out)**: Evicts the oldest created items regardless of recent usage.
- **TTL (Time-to-Live)**: Automatically marks keys as expired after a configured duration (e.g. 300 seconds).

---

## 4. Redis vs Memcached

Program managers frequently navigate vendor and technology selections between Redis and Memcached.

| Feature | Redis | Memcached |
| :--- | :--- | :--- |
| **Data Structures** | Strings, Hashes, Lists, Sets, Sorted Sets, Bitmaps, HyperLogLogs, Geospatial | Pure Key-Value (Strings and byte arrays only) |
| **Threading Model** | Single-threaded core engine (with multithreaded I/O since v6) | Pure Multi-threaded architecture (scales linearly across CPU cores) |
| **Persistence** | RDB snapshots, AOF (Append-Only File) logging | In-memory only (no native disk persistence) |
| **Replication & HA** | Redis Sentinel, Redis Cluster (automatic sharding and failover) | No native clustering; requires client-side consistent hashing |
| **Advanced Features** | Pub/Sub, Lua scripting, Transactions, Redis Streams | Simple, lightweight get/set memory cache |
| **Best Used For** | Rich data caching, leaderboards, rate limiters, session stores | Simple high-throughput memory caching across many CPU cores |

---

## 5. Critical Cache Failure Modes and Mitigations

These three failure modes are staple topics in architecture reviews and system design interviews.

```mermaid
flowchart LR
    subgraph Failures [Cache Anti-Patterns & Failures]
        direction TB
        F1[Cache Stampede / Thundering Herd]
        F2[Cache Avalanche]
        F3[Cache Penetration]
    end

    subgraph Mitigations [Engineering Mitigations]
        direction TB
        M1[Distributed Mutex Lock / Probabilistic Early Recomputation XFetch]
        M2[Jittered TTLs / Random Offset e.g. Base TTL + rand 0 to 60s]
        M3[Bloom Filters at Gateway + Cache Null Values with short TTL]
    end

    F1 ==> M1
    F2 ==> M2
    F3 ==> M3

    classDef fstyle fill:#fee2e2,stroke:#ef4444,stroke-width:1px;
    classDef mstyle fill:#ecfdf5,stroke:#059669,stroke-width:1px;
    class F1,F2,F3 fstyle;
    class M1,M2,M3 mstyle;
```

### 1. Cache Stampede (Thundering Herd)
- **Problem**: A high-traffic key (e.g. homepage banner) expires. Thousands of concurrent requests experience a cache miss simultaneously and hammer the database with identical queries.
- **Mitigation**:
  - *Distributed Mutex*: Only the first thread that misses the cache acquires a lock to query the DB and update the cache; other threads wait or return previous stale data.
  - *Probabilistic Early Expiration (XFetch)*: Recomputes the cache value in the background before the key actually expires based on request probability.

### 2. Cache Avalanche
- **Problem**: Hundreds of thousands of keys are configured with the exact same TTL (e.g. 1 hour) during a bulk sync. All keys expire at the same second, causing the entire traffic volume to fall back on the database.
- **Mitigation**: Add random jitter to key expirations (e.g. `TTL = 3600 + random(0, 300)` seconds).

### 3. Cache Penetration
- **Problem**: Clients query non-existent keys (e.g. malicious requests for `user_id = -9999`). The cache misses, queries the database, finds nothing, and does not store a result. Every subsequent request hits the database.
- **Mitigation**:
  - *Cache Null Objects*: Store a null value with a short TTL (e.g. 60 seconds).
  - *Bloom Filters*: Position an in-memory Bloom filter in front of the cache. If the filter indicates the item definitely does not exist, return 404 immediately without touching cache or database.

---

## 6. Back-of-the-Envelope Cache Sizing (The Correct 80/20 Working Set Formula)

In system design reviews, TPMs must estimate memory requirements using distinct items rather than raw request counts:

1. **The Pareto Principle (80/20 Rule)**: 20% of the **distinct active catalog items** generate 80% of read traffic. You only need to size the fast cache tier for that hot 20%.
2. **Formula**:
   $$\text{Working Set Memory} = (\text{Total Unique Active Items} \times 0.20) \times (\text{Average Record Size} + \text{Key Overhead})$$
3. **Accounting for Redis Memory Overhead**:
   - Each key in Redis incurs approximately 60 to 100 bytes of structural overhead (`dictEntry`, `robj` header, jemalloc allocation alignment).
   - *Example*: Sizing a cache for 10 Million unique active user profiles (average profile size = 1 KB):
     $$\text{Hot Working Set} = 10,000,000 \times 0.20 = 2,000,000\text{ profiles}$$
     $$\text{Raw Data} = 2,000,000 \times 1,000\text{ bytes} = 2\text{ GB}$$
     $$\text{Key Overhead} = 2,000,000 \times 80\text{ bytes} = 160\text{ MB}$$
     $$\text{Memory with 30% Headroom Buffer} = (2\text{ GB} + 0.16\text{ GB}) \times 1.30 \approx 2.8\text{ GB RAM}$$

---

## 7. TPM Review Checklist

When validating caching designs in your program:

- [ ] Is there an explicit invalidation strategy for mutable data (TTL vs event-driven invalidation via CDC)?
- [ ] Are all cache keys set with a Time-To-Live (TTL) to prevent unbounded memory leaks?
- [ ] Are TTLs randomized with jitter to eliminate cache avalanche risks?
- [ ] What happens to application SLAs when the cache cluster restarts or fails?
- [ ] Is cache hit ratio (CHR) tracked as a critical service-level indicator (SLI)? Target CHR: 95%+ for read-heavy tiers.
- [ ] Has memory overhead for allocator fragmentation and hash table buckets been included in cluster capacity sizing?

---

## 8. Primary Sources and Further Reading

- **Scaling Memcache at Facebook**: *Scaling Memcache at Facebook* by Rajesh Nishtala et al. (USENIX NSDI, 2013).
- **Redis In-Depth**: *Redis: The Definitive Guide* and Redis Official Memory Optimization Documentation (https://redis.io/docs/management/optimization/memory-optimization/).
- **Probabilistic Cache Regeneration**: *Optimal Probabilistic Cache Stampede Prevention* by Vattani, Chierichetti, and Lowenstein (VLDB, 2015).
- *Database Internals: A Deep Dive into How Distributed Data Systems Work* by Alex Petrov (O'Reilly Media, 2019) - Chapter 12: Distributed Caching.
