---
layout: post
title: "Evidence-Based Best Practices as AI Guardrails (Part 2)"
date: 2026-04-01
categories: ai development best-practices security
description: "The remaining 12 best practice files that keep AI-generated code production-ready. Part 2 of 2: security, privacy, operations, accessibility, SEO, and integration patterns."
keywords: "Claude Code, best practices, AI guardrails, authorization, container security, privacy, GDPR, resilience patterns, zero-downtime deployment, observability, accessibility, WCAG, SEO, LLM integration, OWASP"
image: security-privacy-production-hardening-ai-guardrails-blog.png
---

<figure>
  <img src="/assets/images/security-privacy-hardening-antelope-canyon.jpg" alt="Sunlight beam piercing through layered sandstone walls of Antelope Canyon, Arizona" width="5472" height="3648" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>Layers of protection, carved deep. Photo by <a href="https://www.pexels.com/@madhu-shesharam-108388377">Madhu Shesharam</a> on <a href="https://www.pexels.com/photo/a-cave-of-red-rock-formation-with-sunlight-reflection-9579434/">Pexels</a>.</figcaption>
</figure>

This is part two of an originally three part now turned into two-part series on using evidence-based best practice files to keep AI-generated code production-ready and improve the general quality. [Part 1](/ai/development/best-practices/2026/03/31/evidence-based-best-practices-ai-guardrails.html) covered the foundations: architecture, error handling, testing, API design, data integrity, and structured logging -- with detailed examples of how each file works. I originally planned 3 parts, but I do not like dragging it out, and I get bored easily, so better to get it done: here is the rest!

This post covers the remaining twelve files. Rather than repeating the deep-dive format, I'll give you the core idea behind each: the problem it solves, the principle it encodes, and why Claude gets it wrong without it. The files themselves contain the full rules, code examples, and trade-offs -- grab them from the [public repository](https://github.com/albertsikkema/claude-code-best-practices) and read what's relevant to your stack.

## What This Post Covers

**Security and Privacy**

1. [Authorization](#1-authorization) -- the difference between "logged in" and "allowed"
2. [Defense-in-Depth Validation](#2-defense-in-depth-validation) -- why one validation layer is never enough
3. [Container Security](#3-container-security) -- a secret "deleted" in layer 5 still exists in layer 3
4. [Privacy by Design](#4-privacy-by-design) -- the safest data is data you never collected

**Operations and Reliability**

5. [Resilience Patterns](#5-resilience-patterns) -- designing for the certainty that dependencies will fail
6. [Zero-Downtime Deployment](#6-zero-downtime-deployment) -- old and new code run simultaneously, plan for it
7. [Observability](#7-observability) -- turning 2-hour investigations into 5-minute ones
8. [Background Job Patterns](#8-background-job-patterns) -- not all work belongs in the request cycle

**User-Facing Quality**

9. [Accessibility](#9-accessibility) -- build interfaces that work for everyone
10. [SEO](#10-seo) -- make your structure machine-readable

**External Boundaries**

11. [Robots and Scraping Protection](#11-robots-and-scraping-protection) -- control what automated agents can access
12. [LLM Integration Patterns](#12-llm-integration-patterns) -- route cheap before expensive

---

## Security and Privacy

### 1. Authorization

Authentication and authorization are two different things. Claude is quite loose in using the terminology: It builds login flows, JWT validation, and session management, then considers security "done." But knowing *who* a user is tells you nothing about *what they're allowed to do*. (BTW important to realise: this is not necessarily Claude's 'fault', probably has more to do with the training data and the ambiguity in there.)

The file encodes default-deny authorization: every request is unauthorized unless explicitly permitted. Object-level checks (not just "can users access orders" but "can *this* user access *this specific* order"), centralized RBAC, and re-authentication for destructive operations. Without it, Claude writes `GET /api/orders/:id` that returns any order to any authenticated user. IDOR (Insecure Direct Object Reference -- where a user accesses resources by manipulating an identifier like an ID in the URL, without the server checking whether they're allowed to) sits at #1 in the [OWASP Top 10](https://owasp.org/www-project-top-ten/) as a part of A01:2021 Broken Access Control. And Claude in my experience is notoriously bad and inconsistent when it comes to IDOR.

### 2. Defense-in-Depth Validation

Most of the time Claude adds one layer of input validation (if at all) -- usually a schema check at the handler -- and moves on. That catches missing fields and wrong types. It does nothing against path traversal, injection patterns, or context-specific attacks. Not a problem, I do not expect to create perfect software all in one go. But I am supposed to spot that and deliver a secure product. Defense in depth is a step in getting there.

The file defines four independent validation layers: structural constraints, format and character restrictions, explicit security pattern checks (path traversal, null bytes, injection), and downstream sanitization (parameterized queries, shell escaping, HTML encoding). The key principle: each layer assumes the others might fail. Remove any single layer and the system is still protected (perhaps not as good as with the layer you removed, but you get the point: adding multiple layers protects you from yours or Claude's stupidity).

### 3. Container Security

Claude is actually quite good at writing docker container definitions. It does not use full Ubuntu base images, running as root, secrets passed as build arguments visible in `docker history` forever. It does not build a functional container with the attack surface of a full server. But it is smart to keep it aligned with your (or in this case my) vision on security and building layers.

The file mandates minimal base images (distroless or slim), multi-stage builds, non-root execution, read-only filesystems, dropped capabilities, and never baking secrets into layers. A Go app in distroless is small with no shell to exploit. The same app in Ubuntu is 500MB with everything that gives a bad actor points to interact with.

### 4. Privacy by Design

Sometimes I think Claude has no concept or was never trained on the basic concepts of privacy. Ask it to build a user profile page and it'll collect date of birth, phone number, and address "in case we need them later." That "in case" creates legal liability under [GDPR](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679) that compounds over time. Plenty of examples (also here in the Netherlands) with very private data that becomes available on the dark web or is ransomed. Not something you want to run into. So the starting point: do not collect it unless absolutely necessary (and most of it is absolutely NOT necessary).

The file encodes data minimization (collect only what's functionally necessary), consent management (explicit, informed, granular, revocable), right to erasure (covering all copies: database, backups, caches, third-party systems), data portability, and cookie compliance under the [ePrivacy Directive](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02009L0136-20201221). Privacy becomes a first-class architectural concern, not a compliance checkbox. You want to start with privacy awareness in the start phase of your product, but keep the right to erasure and data portability for a later stage.

---

## Operations and Reliability

### 5. Resilience Patterns

Sometimes you get lucky and Claude remembers to build in some resilience. Most of the time you will find out when testing, or even better in production. And with luck the first time a dependency slows down in production, the entire system cascades into failure. Better to build this in from the start and explicitly design for it.

The file defines timeouts on every outbound call (with specific defaults per type), deadline propagation, retries with exponential backoff and jitter (only for idempotent operations, only for transient errors), circuit breakers (closed/open/half-open), graceful degradation (hard vs soft dependencies), and backpressure. The composition order matters: backpressure -> circuit breaker -> timeout -> retry -> degradation. As I said in the previous post: Claude knows much more about this than I will ever do, but you need to call it to the center of attention (not unlike how you focus a human's attention I find).

### 6. Zero-Downtime Deployment

Deployments and data migrations with Claude can often go awesome, and sometimes you are in deep trouble. So it is good, for your own sanity and job security, to protect the data at all costs. How far you will take this is up to you. You decide what is acceptable (no data loss is priority one and zero downtime (or near zero) is a good second one.) If need be, make sure to run both versions of your database at once. Or just go for it. It is a thrill (if you like that kind of thrill). Rule number one: make sure you always can go back! Rule number two: backup. Rule number three: make sure you can roll back. Rule number four: backup. (And rule 5 and following: make sure your backups can be deployed. Best to do that before deploying.)

The file mandates expand-contract migrations in four phases (expand, backfill, deploy new code, contract), health-check-gated rollouts with separate `/health` and `/ready` endpoints, graceful shutdown on SIGTERM, and tested rollback scripts. Every change must be safe for both old and new versions to read and write at the same time. Make this as complex as you want or the situation warrants.

### 7. Observability

Simply following a data flow through your code using correlation IDs is really handy. It really helps with debugging, monitoring and logging. Claude sometimes adds `logger.info("request processed")` and considers observability done and is very sure of that. No correlation IDs, no metrics, no structured context. When something breaks, you're searching unstructured logs with no way to connect a failed request to its downstream calls. And the good thing about doing this properly (or at least add some improvements that help observability): Claude will help you debug better because it can easily work with this.

The file covers the three pillars: structured logs (what happened), metrics (how much), and distributed traces (the journey of a request). Every request gets a correlation ID propagated through all downstream calls. The Four Golden Signals (latency, traffic, errors, saturation), RED method for services, USE method for resources. Alerts with severity-appropriate thresholds and enough context to start investigating immediately.

### 8. Background Job Patterns

I suspect that it has to do with the training data, but Claude will almost never propose to put a process in a background process, unless you explicitly ask it to. Mentioning it in these files does increase the likelihood that it will be used in the places that matter (it is funny when you worked with claude for a while and start adding these files, it seems to become a lot better at making code that makes sense.)

The file defines three patterns with clear selection criteria: fire-and-forget (return 202, spawn background work, no status tracking), tracked jobs (return a job ID, persist status to a database, client polls for completion), and queue-based processing (decouple producer and consumer with a message queue, bounded retries, dead letter queues). Cross-cutting concerns are covered: isolation between request and worker threads, correlation IDs for background logging, timeouts on every job, and graceful shutdown behavior. Start simple, scale up when you need it. Background processes are not the answer to all problems, but they have their uses.

---

## User-Facing Quality

### 9. Accessibility

Claude generates `<div onClick={...}>` instead of `<button>`, skips `alt` attributes, ignores keyboard navigation, and uses color alone to convey meaning. The result looks fine. A screen reader can't parse it, a keyboard user can't navigate it, and you're non-compliant with the [European Accessibility Act](https://ec.europa.eu/social/main.jsp?catId=1202). This is one thing Claude is actually really bad at, it has never given me ideas or steps to improve accessibility. Again the training data I think. Anyway, it is vital to include this. It used to be quite a hassle, but nowadays you cannot build a webpage with no attention for WCAG. Implementing the basics is easy with Claude, you just have to tell what you want. This file helps with that. But just this file is in this case not enough. In a later post I will share how I (attempt to) solve this.

The file targets [WCAG 2.2](https://www.w3.org/TR/WCAG22/) Level AA: semantic HTML elements for their intended purpose, keyboard accessibility for all interactive elements, text alternatives for all non-text content, color contrast ratios (4.5:1 for normal text, 3:1 for large text and UI components), labeled form inputs, respect for `prefers-reduced-motion`, proper ARIA live regions for dynamic content, text resizing support, and automated axe-core checks in CI. Automated tools catch 30-40% of issues -- the file also specifies what requires manual testing. Important here is to watch the structure of a page.

### 10. SEO

SEO is not automatically added to your page if you let Claude build it. For most projects I work on that is not an issue: internal tools and applications do not need that. But for a lot of pages visibility for search engines is crucial. BTW good performance is useful for every tool, so parts of this are useful for those internal tools as well.

The file covers crawlability (SSR for public pages, no orphan pages), canonical URLs (one URL per piece of content), meaningful title and meta tags, structured data via JSON-LD (Organization, Product, Article, FAQ, Breadcrumb), auto-generated sitemaps, hreflang for multi-language sites, Core Web Vitals optimization (LCP < 2.5s, CLS < 0.1, INP < 200ms), proper redirect handling, and useful 404 pages. For multi-region sites: URL strategies (ccTLD vs subdomain vs subdirectory) with trade-offs for each.

---

## External Boundaries

### 11. Robots and Scraping Protection

Even though I love using LLM's, the amount of bot traffic has risen tremendously as a consequence. The problem is that Claude doesn't think about bot traffic (a cynic could argue that this is in its own (or its owners) interest). It builds a public API without rate limiting, exposes admin paths in `robots.txt` (telling attackers exactly where to look), and ignores the fact that AI training crawlers will scrape everything they can reach.

The file separates search engine crawlers (usually welcome) from AI training crawlers (block by default: GPTBot, CCBot, Google-Extended, Bytespider, ClaudeBot, and others). Per-page control via meta tags for indexing decisions. Server-side rate limiting on all public endpoints -- `robots.txt` is advisory only, not enforcement. API scraping protection through authentication, pagination limits, and monitoring. And a `security.txt` so researchers know where to report vulnerabilities. But keep in mind: a lot of bots ignore robots.txt. So do not be surprised if your cloud bills are through the roof because of a sudden spike in bot interest. (this is actually a really good reason to run your applications on your own (rented) hardware)

### 12. LLM Integration Patterns

This is a work in progress and far from complete. The basic idea is that you use logic for the deterministic parts of your workflow and LLM for the non- or semi-deterministic parts. You do not want to use LLMs for every step, most of the time it is far better to use a bit of code: it is predictable, reliable and testable. All things that an LLM are not. I am still improving this part, but found that this already helps in getting Claude to 'think' in the direction I want it to.

The file encodes a principle: route cheap before expensive. Keep deterministic work (filtering, sorting, validation) outside the LLM. Use a cheap classifier to route off-topic requests before hitting the expensive agent. Format context deliberately with truncation limits -- a pure function that takes structured data and returns a token-efficient string. Manage prompts as versioned files, not hardcoded strings. Cache responses for repeated queries. Handle non-determinism explicitly: validate structured output against schemas, track fallback rates, retry once on malformed responses. Never expose raw LLM errors to users. And observe everything: prompt length, response length, token usage, latency, cost per request, tool call sequences. Your wallet will thank you (or your boss).

---

## The Full Picture

Across both posts, these 18 files form a connected system. Part 1 laid the structural foundations: how code is organized, how errors flow, how tests verify, how APIs behave, how data stays consistent, and how logs tell you what happened. This post covered what makes that foundation trustworthy in production: who can do what, how input is validated at multiple layers, how containers are hardened, how privacy is protected, how the system survives failure, how deploys avoid downtime, how you observe it all, how background work is managed, how interfaces work for everyone, how search engines find you, how bots are controlled, and how LLM integrations stay efficient.

No single file solves the problem. Authorization without observability means you won't know when it fails. Resilience without observability means watching failures you can't diagnose. Container security without privacy means a hardened runtime leaking PII through the application. The value is in the combination -- and in the traceability back to requirements, specifications, and standards.

And as mentioned before and here again: the clue is not to try to tell Claude what it needs to do. It is to get Claude to 'remember' what it already knows. Bring to the front of its attention those things you think are necessary for that step in the development process in your product. It has way more data than you ever will comprehend, but it needs a hooman to keep it focused.

## Try It Yourself

All 18 best practice files are in the [public repository](https://github.com/albertsikkema/claude-code-best-practices). Drop them into your setup, adapt them to your stack, or use them as a starting point for your own.

**In this series:**

- [Part 1: Architecture, Error Handling, Testing, API Design, Data Integrity, Structured Logging](/ai/development/best-practices/2026/03/31/evidence-based-best-practices-ai-guardrails.html)
- **Part 2: Security, Privacy, Operations, Accessibility, SEO, and Integration Patterns** (this post)

---

*Have questions or want to share your approach to keeping AI-generated code in line? <a href="#" onclick="task1(); return false;">Get in touch</a>.*

## Standards and References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GDPR (Regulation 2016/679)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679)
- [ePrivacy Directive (2009/136/EC)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02009L0136-20201221)
- [WCAG 2.2 - Web Content Accessibility Guidelines](https://www.w3.org/TR/WCAG22/)
- [European Accessibility Act](https://ec.europa.eu/social/main.jsp?catId=1202)
- [OCI Image Specification](https://github.com/opencontainers/image-spec)
- [RFC 9457 - Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)
