# Module 5: Real-World Architecture Case Studies

[Home](../README.md) > **Module 5: Real-World Case Studies**

---

## Overview

Theoretical knowledge becomes actionable only when applied to complex, high-scale, end-to-end architectures. This module presents five comprehensive production case studies designed to reflect the real-world interview scenarios and engineering challenges encountered at leading technology companies (Google, Meta, Amazon, Apple, Uber, Netflix).

Each case study follows a rigorous, uniform 14-section architectural framework: from initial functional scoping and mathematical capacity planning to concrete API contracts, data models, alternative trade-off tables, failure-mode matrices, and worked TPM delivery plans.

---

## Case Study Directory

| Case Study | Title | Real-World Analog | Core Architectural Challenges |
| :--- | :--- | :--- | :--- |
| **[5.1](./01-url-shortener.md)** | Global URL Shortener | TinyURL / Bitly | Key Generation Service (KGS), Base62 hashing, 301 vs 302 redirects, Zipfian cache sizing, abuse detection |
| **[5.2](./02-notification-engine.md)** | Multi-Channel Notification Platform | Twilio / OneSignal | Priority queue isolation, user preferences & quiet hours, vendor circuit breakers, SMS-to-push cost cascades |
| **[5.3](./03-video-streaming-platform.md)** | Global Video Streaming Platform | YouTube / Netflix | Chunked DAG GPU transcoding, Adaptive Bitrate Streaming (HLS/DASH), multi-terabit CDN egress, ISP edge caching |
| **[5.4](./04-ride-sharing-dispatch.md)** | Real-Time Ride-Sharing Dispatch | Uber / Lyft | 1.25M location pings/sec, Uber H3 hexagonal spatial indexing, distributed driver locking, WebSocket lifecycles |
| **[5.5](./05-distributed-ecommerce-checkout.md)** | Flash Sale & Distributed Checkout | Amazon / Shopify | Atomic in-memory inventory reservation (Redis Lua), Saga pattern rollback, payment idempotency, virtual waiting room |

---

## Recommended Study Approach

1. **Step 1: Attempt the Scoping First**: Before reading the solution, spend 5 minutes jotting down your own functional requirements, out-of-scope boundaries, and capacity math.
2. **Step 2: Compare Architectural Trade-offs**: Pay close attention to the Architectural Decision Records (ADRs) and why common alternative approaches were rejected.
3. **Step 3: Study the Failure Matrices**: Understand how each system behaves during partial network outages, broker crashes, or downstream vendor failures.
4. **Step 4: Practice the Interview Questions**: Attempt the practice questions at the end of each chapter under timed 10-minute conditions before reviewing the model rubric answers.
