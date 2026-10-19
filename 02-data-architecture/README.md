# Module 2: Data Architecture and Storage

[Home](../README.md) > **Module 2: Data Architecture**

---

## Overview

Data architecture dictates the durability, scalability, and transactional integrity of any distributed platform. As a Technical Program Manager, understanding database engines, sharding mechanisms, consistency models, and event streaming enables you to guide technical discussions, prevent data corruption, and manage schema migrations effectively.

---

## Module Learning Objectives

1. **Storage Engine Trade-offs**: Contrast B-Tree (read-optimized) vs LSM-Tree (write-optimized) architectures and understand the performance impact of secondary indexes.
2. **Database Categorization**: Select between Relational, Document, Key-Value, Wide-Column, Graph, and NewSQL engines using clear architectural criteria.
3. **Partitioning and Scaling**: Master horizontal sharding, consistent hashing rings with virtual nodes, and strategies to handle the "celebrity problem" (hot partitions).
4. **Consistency Theorems**: Apply the CAP and PACELC theorems to align business domain requirements with distributed consistency choices.
5. **Asynchronous Messaging**: Differentiate traditional message queues from distributed event streaming logs (Kafka) and enforce at-least-once processing with consumer idempotency.

---

## Chapter Directory

| Chapter | Title | Focus Areas | Key Trade-offs |
| :--- | :--- | :--- | :--- |
| **[2.1](./01-databases-sql-vs-nosql.md)** | Databases: Relational vs NoSQL vs NewSQL | ACID vs BASE, B-Trees vs LSM-Trees, indexing overhead, polyglot persistence | Strict transactional consistency vs horizontal elasticity |
| **[2.2](./02-sharding-replication.md)** | Replication, Sharding & Consistent Hashing | Primary-Replica, replication lag, consistent hashing rings, virtual nodes | Read scale vs replication staleness, re-sharding complexity |
| **[2.3](./03-cap-pacelc-theorems.md)** | The CAP and PACELC Theorems | Network partitions, CP vs AP models, PACELC latency dimension | Consistency vs Availability during network splits |
| **[2.4](./04-message-queues-streaming.md)** | Asynchronous Messaging & Event Streams | Queues vs Streams, Kafka commit log, delivery guarantees, DLQs | Temporal decoupling, ordering guarantees, consumer lag |

---

## Suggested Prerequisites

- Completion of [Module 1: Distributed Systems Foundations](../01-foundations/README.md).
- Understanding of basic relational database schemas (tables, primary keys, foreign keys).
- Familiarity with JSON payload structures.
