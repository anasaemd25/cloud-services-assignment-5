# Weekly Assignment 5 - Cloud Services

## Live Application & Repository Links
- **Live Redis Cache Endpoint (Week 5 Extension):** https://frontend-cloud-services-assignment-2.2.rahtiapp.fi/api/cache
- **Main Application (Week 4 Baseline):** https://frontend-cloud-services-assignment-2.2.rahtiapp.fi/
- **GitHub Repository:** https://github.com/anasaemd25/cloud-services-assignment-5

---

## Part A - Questions

### 1. What is YAML and why has it become the default configuration format for Kubernetes/Rahti manifests? Compare it briefly to JSON.
YAML (YAML Ain't Markup Language) is a human readable data serialization standard commonly used for configuration files. It became the default option for Kubernetes and Rahti because its clean structure relies on line indentation instead than brackets or commas, making the complex cluster definitions easier to read and maintain. Unlike JSON, YAML supports comments and has a minimal syntax. Behind the scenes, Kubernetes converts YAML manifests into JSON before applying them.

### 2. What is a Web Application Firewall (WAF) and what kinds of attacks does it defend against? Where would you place one in the three-container architecture built in Week 4?
A Web Application Firewall inspects and filters incoming HTTP/HTTPS traffic to block malicious exploits before they reach the web application. It defends against OWASP top threats like SQL Injection, Cross-Site Scripting (XSS), and automated bot attacks. In the Week 4 architecture (`Route → Frontend → Backend → Database`), a WAF would be placed at the edge of the network,right before or integrated into the public Route/Frontend, protecting Nginx and Flask from direct application layer attacks.

### 3. Explain the difference between SAML and OAuth. When would a company choose one over the other?
Security Assertion Markup Language is an XML based framework focused on **Authentication** (verifying identity) for Enterprise Single Sign-On (SSO). OAuth is an open standard focused on **Authorization** (for granting access permissions without sharing user credentials). A company chooses SAML for internal corporate login systems across employee software, but OAuth is chosen when building web applications that allow users to sign in via 3rd party providers (like MIcrosoft or Google) or when managing API access tokens

### 4. What are open data portals and why does choosing the right open-data format matter for reuse?
Open data portals are public platforms that store freely accessible datasets provided by governments and public figures. Choosing standard, machine readable formats like JSON, CSV, or GeoJSON is important for reuse, because software applications can parse and process data automatically. Unstructured formats like PDFs or images block automation and require manual extraction.

---

## Part B - Extension Implementation (Redis Cache)

### Architecture Overview
Extended the Week 4 application by deploying a **Redis Cache** instance as an independent container service within CSC Rahti.

### Verification & Testing
- **Base App:** The primary route (`/`) continues to query MySQL for database time and visitor counts.
- **Cache Endpoint:** The `/api/cache` route connects to `redis-service:6379` using the Python `redis` library to increment in-memory page visit counts without hitting the MySQL database.

### Production Readiness Reflection
In a live production deployment, relying on an in-memory cache requires implementing explicit key expiration policies (TTL) and eviction limits to avoid memory exhaustion. Strategies for cache invalidation must be integrated into database write operations to prevent delivering stale data to end users.

### Problems Encountered & Solved
1. **YAML Syntax Errors:** Corrected indentation for environment variables in `backend-deployment.yaml`.
2. **Rahti Authentication:** Resolved CLI authentication errors by fetching a fresh session token via the Rahti Web Console ("Copy login command").