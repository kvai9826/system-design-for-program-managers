# Module 1.2: Load Balancing and API Gateways

Load balancers and API gateways form the front door of modern distributed architectures. They ensure high availability, prevent server saturation, enforce security policies, and route requests efficiently across fleet instances. For technical program managers, these components represent critical single points of failure (SPOFs) and cost drivers.

---

## 1. Layer 4 vs Layer 7 Load Balancing

Load balancers operate at different layers of the OSI model, trading inspection depth for raw packet throughput.

```mermaid
flowchart TD
    Client[Incoming Client Traffic] --> L4[Layer 4 Load Balancer: IP + Port Routing]
    
    L4 -->|TCP Stream Passthrough| L7A[Layer 7 Load Balancer / API Gateway]
    L4 -->|TCP Stream Passthrough| L7B[Layer 7 Load Balancer / API Gateway]
    
    L7A -->|Inspect Path /orders| SvcA[Orders Microservice]
    L7A -->|Inspect Path /users| SvcB[Users Microservice]
    L7B -->|Inspect Path /payments| SvcC[Payments Microservice]

    classDef lb fill:#eff6ff,stroke:#2563eb,stroke-width:1px;
    classDef svc fill:#f0fdf4,stroke:#16a34a,stroke-width:1px;
    class L4,L7A,L7B lb;
    class SvcA,SvcB,SvcC svc;
```

### Deep-Dive Comparison

| Dimension | Layer 4 (Transport Layer) | Layer 7 (Application Layer) |
| :--- | :--- | :--- |
| **Routing Criteria** | Source IP, Source Port, Dest IP, Dest Port, TCP/UDP protocol | HTTP URI, HTTP Headers, Cookies, Request Body, Content-Type |
| **Payload Inspection** | No inspection; forwards raw packets directly | Full inspection; terminates TCP and parses HTTP payload |
| **Performance** | Extremely high throughput, ultra-low latency, low CPU overhead | Higher CPU and memory consumption per request |
| **SSL/TLS Termination** | Passes encrypted packets or decrypts without HTTP inspection | Full SSL/TLS termination and re-encryption to backends |
| **Smart Routing** | Cannot route based on URL path or session cookies | Supports canary traffic splitting, path routing, header filtering |
| **Technologies** | AWS NLB (Network Load Balancer), HAProxy (TCP mode), IPVS, F5 | AWS ALB, NGINX, Envoy, Traefik, Kong, HAProxy (HTTP mode) |

---

## 2. Load Balancing Algorithms

Choosing the right distribution algorithm directly impacts p99 tail latency and resource utilization.

```mermaid
graph LR
    subgraph Algorithms [Load Balancing Algorithms]
        RR[Round Robin / Weighted Round Robin]
        LC[Least Connections / Weighted Least Connections]
        IPH[IP Hash / Source Hash]
        CH[Consistent Hashing]
    end

    RR -->|Best For| U1[Stateless identical backend instances]
    LC -->|Best For| U2[Long-lived connections e.g. WebSockets, heavy compute]
    IPH -->|Best For| U3[Sticky sessions without shared session storage]
    CH -->|Best For| U4[Distributed caching tiers with dynamic nodes]

    classDef algo fill:#fef3c7,stroke:#d97706,stroke-width:1px;
    class RR,LC,IPH,CH algo;
```

1. **Round Robin**:
   - Cycles through servers sequentially.
   - *Limitation*: Assumes all servers have identical capacity and all requests require equal processing time.
2. **Weighted Round Robin**:
   - Assigns a numeric weight reflecting hardware capacity (e.g. 8 cores gets 2x requests of 4 cores).
3. **Least Connections**:
   - Routes to the server with fewest active concurrent connections. Essential for variable-duration transactions like report generation or video encoding.
4. **Consistent Hashing**:
   - Maps requests and servers to a virtual ring. Minimizes cache misses when backends scale up or down.

---

## 3. High Availability Topologies: Active-Passive vs Active-Active

High availability eliminates single points of failure at the network ingress layer.

```mermaid
flowchart TD
    subgraph TopologyAP [Active-Passive Topology]
        direction TB
        ClientAP[DNS / Virtual IP VIP] --> LB_Active[Primary Active LB]
        LB_Active -.->|Heartbeat / Keepalived VRRP| LB_Passive[Standby Passive LB]
        LB_Active --> BackendsAP[Backend Application Pool]
    end

    subgraph TopologyAA [Active-Active Topology with Anycast BGP]
        direction TB
        ClientAA[Global Anycast IP] --> Router[BGP Border Router]
        Router --> LB1[Active LB Node 1]
        Router --> LB2[Active LB Node 2]
        LB1 --> BackendsAA[Backend Application Pool]
        LB2 --> BackendsAA
    end

    classDef topo fill:#f8fafc,stroke:#64748b,stroke-width:1px;
    class TopologyAP,TopologyAA topo;
```

### Architectural Trade-offs

- **Active-Passive (Failover via VRRP / Keepalived)**:
  - Simple to implement; standby node consumes idle compute cost.
  - Failover takes 1 to 5 seconds while virtual IP address migrates.
- **Active-Active (BGP Anycast / DNS Multi-A Records)**:
  - Full resource utilization; traffic is load-balanced across all gateways simultaneously.
  - Requires automated health-checking to withdraw BGP routes instantly if a node crashes.

---

## 4. The API Gateway Pattern

In a microservice architecture, client applications should never interact directly with hundreds of internal microservices. The API Gateway acts as a unified reverse proxy and policy enforcement point.

```mermaid
flowchart LR
    Clients[Web / Mobile Clients] -->|HTTPS Requests| GW[API Gateway / Ingress]
    
    subgraph GatewayResponsibilities [Gateway Cross-Cutting Concerns]
        direction TB
        R1[Authentication & Authorization - JWT Verification]
        R2[Rate Limiting & Throttling - Token Bucket]
        R3[SSL / TLS Termination]
        R4[Path Routing & Canary Traffic Splitting]
        R5[Telemetry, Logging & Distributed Tracing]
    end

    GW --- GatewayResponsibilities

    GW -->|gRPC / Internal HTTP| Svc1[Catalog Service]
    GW -->|gRPC / Internal HTTP| Svc2[Payment Service]
    GW -->|gRPC / Internal HTTP| Svc3[Notification Service]

    classDef gw fill:#eff6ff,stroke:#1d4ed8,stroke-width:2px;
    class GW gw;
```

### Core API Gateway Responsibilities

1. **Request Routing & Path Translation**:
   - Routes `/api/v1/checkout` to the Checkout cluster and `/api/v1/search` to the Search cluster.
2. **Security & Authentication Offload**:
   - Validates OAuth2 / OpenID Connect tokens, decodes JWT signatures, and passes verified user claims as internal HTTP headers (`X-User-ID`, `X-User-Role`) to backends.
3. **Rate Limiting & Abuse Prevention**:
   - Enforces tier-based quotas (e.g. 100 requests per minute for free tier, 5000 for enterprise) using Redis-backed token buckets.
4. **SSL/TLS Termination**:
   - Manages certificates centrally, decrypts incoming traffic, and communicates with internal services over high-speed private virtual private clouds (VPCs).
5. **Observability Injection**:
   - Injects correlation IDs (`X-Correlation-ID` or W3C `traceparent`) to enable end-to-end distributed tracing across microservices.

---

## 5. Reverse Proxy vs API Gateway vs Ingress Controller

Technical program managers often hear these terms used interchangeably. Here is the distinction:

| Component | Primary Scope | Typical Technology |
| :--- | :--- | :--- |
| **Reverse Proxy** | Handles single-site traffic, static asset serving, compression, basic load balancing | NGINX, Apache, HAProxy |
| **API Gateway** | Rich business-aware API management: rate limiting, auth, mocking, developer portals, monetization | Kong, Apigee, AWS API Gateway, Envoy |
| **Ingress Controller** | Bridges external traffic into Kubernetes cluster pods based on Ingress resource definitions | NGINX Ingress, Traefik, Istio Gateway |

---

## 6. Health Checks and Failover Mechanics

Load balancers rely on active and passive health checks to detect failing servers and avoid routing user requests to dead nodes.

```mermaid
sequenceDiagram
    autonumber
    participant LB as Load Balancer
    participant S1 as Server 1 (Healthy)
    participant S2 as Server 2 (Failing)

    LB->>S1: GET /healthz
    S1-->>LB: 200 OK (Response time: 15ms)
    LB->>S2: GET /healthz
    Note over S2: Process hanging / Database dead
    S2-->>LB: 503 Service Unavailable (or Timeout after 2000ms)
    Note over LB: Mark Server 2 Unhealthy after 3 consecutive failures
    LB->>LB: Remove Server 2 from active routing pool
```

### Health Check Strategy Best Practices

- **Shallow Health Check (`/ping`)**: Confirms the web process is running. Fast and lightweight, but does not verify downstream database connectivity.
- **Deep Health Check (`/healthz`)**: Verifies database connection, cache connectivity, and disk space.
- *Caution for TPMs*: Deep health checks can cause cascading failures. If a shared database slows down, all app servers fail health checks simultaneously, causing the load balancer to pull the entire fleet out of service. Use shallow health checks for load balancing routing and deep checks for synthetic monitoring alerts.

---

## 7. TPM Review Checklist

When scoping and reviewing ingress architecture programs:

- [ ] Is Layer 4 or Layer 7 load balancing selected based on throughput vs routing needs?
- [ ] Are active and passive health checks configured with sensible timeouts and failure thresholds?
- [ ] Is the API Gateway protected against distributed denial of service (DDoS) via rate limiting?
- [ ] Is SSL termination centralized to save backend compute cycles?
- [ ] Are correlation IDs generated at the gateway and forwarded through all downstream hops?
- [ ] Does the gateway support zero-downtime canary deployments (traffic splitting by percentage or header)?
