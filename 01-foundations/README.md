# Module 1: Distributed Systems Foundations

[Home](../README.md) > **Module 1: Foundations**

---

## Overview

Modern distributed systems power internet-scale applications by coordinating hundreds of independent services across global networks. This module provides the foundational building blocks required for Technical Program Managers: network transport protocols, application layer APIs, ingress routing, and multi-tier caching architectures.

---

## Module Learning Objectives

1. **Protocol Selection**: Learn how to evaluate trade-offs between TCP, UDP, HTTP/1.1, HTTP/2, and HTTP/3 (QUIC) based on latency SLAs and network conditions.
2. **API Styles**: Master the criteria for selecting REST, gRPC, GraphQL, WebSockets, or Server-Sent Events for internal and external interfaces.
3. **Ingress Architecture**: Understand how DNS, CDNs, Layer 4/Layer 7 load balancers, and API Gateways collaborate to route client requests securely and reliably.
4. **Caching Strategies**: Evaluate multi-tier caching patterns (Cache-Aside, Write-Through, Write-Behind) and prevent production incidents like Cache Stampedes and Avalanches.

---

## Chapter Directory

| Chapter | Title | Focus Areas | Key Trade-offs |
| :--- | :--- | :--- | :--- |
| **[1.1](./01-client-server-networking.md)** | Client-Server Networking & Protocols | TCP/UDP, HTTP evolution, REST, gRPC, WebSockets, DNS, CDNs | Head-of-line blocking, binary multiplexing, connection migration |
| **[1.2](./02-load-balancing-gateways.md)** | Load Balancing & API Gateways | L4 vs L7 routing, Active-Active, reverse proxies, API Gateway offload | Throughput vs deep packet inspection, SPOF mitigation |
| **[1.3](./03-caching-strategies.md)** | Distributed Caching Strategies | Multi-tier cache, read/write patterns, eviction (LRU/LFU), Redis | Consistency vs latency, stampede mitigation, working set sizing |

---

## Suggested Prerequisites

- Understanding of client-server request/response cycles.
- Basic familiarity with IP addressing and ports.
- Foundational knowledge of web browsers and mobile application clients.
