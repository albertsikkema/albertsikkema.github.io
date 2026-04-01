---
layout: post
title: "Evidence-Based Best Practices as AI Guardrails (Part 1)"
date: 2026-03-31
categories: ai development best-practices
description: "How structured, evidence-based best practice files keep Claude Code from cutting corners. Part 1 of 2: architecture, error handling, testing, API design, data integrity, and structured logging."
keywords: "Claude Code, best practices, AI guardrails, software architecture, error handling, testing strategy, API design, data integrity, structured logging, WCAG, RFC 9457, OWASP"
image: evidence-based-best-practices-ai-guardrails-blog.png
---

<figure>
  <img src="/assets/images/guardrails-desert-road-valley-of-fire.jpg" alt="Desert road with guardrails leading toward red mountains in Valley of Fire, Nevada" width="1920" height="2832" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>Guardrails keep you on the road, even when the terrain gets rough. Photo by <a href="https://unsplash.com/@bricecooper">Brice Cooper</a> on <a href="https://unsplash.com/photos/a-road-with-a-mountain-in-the-background-rZybLYQ7xTg">Unsplash</a>.</figcaption>
</figure>

Claude Code writes working code. It passes tests, it runs, it does what you asked. Then it logs passwords in plaintext, skips input validation, serves pages that screen readers can't parse, and deploys in a way that takes your site down for thirty seconds.

Tell it once, it listens. Next conversation, same mistakes.

I've spent over 2,000 hours iterating on my Claude Code setup. The single most impactful thing I did wasn't clever prompting or complex hooks, it was writing down what I know about building production software in a way the model can actually use.

Not opinions. Evidence-based practices, grounded in standards: [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) for error responses, [WCAG 2.2](https://www.w3.org/TR/WCAG22/) for accessibility, [OWASP Top 10](https://owasp.org/www-project-top-ten/) for security, [DAMA-DMBOK](https://www.dama.org/cpages/body-of-knowledge) for data quality. Each practice traces to a concrete requirement, each requirement traces to a specification, and each specification traces to a library choice. When the model writes code, it doesn't just know *what* to do, it knows *why*, and *with what*.

## The Problem with Instructions

You've probably tried the obvious approach: tell the LLM what to do.

"Always use parameterized queries." "Handle errors properly." "Make it accessible."

This works once, maybe twice but inevitably it drifts. The model is smart enough, but the instructions are vague, context-dependent, and easily outweighed by other things in the prompt. "Handle errors properly" means nothing without defining what "properly" looks like in your stack, with your patterns, for your use case. And you need to keep repeating this, every prompt. Or it will revert to its old ways.

I went through the same cycle most people go through. First, I wrote instructions in the prompt, then claude.md. Then I moved them to rules. Then I [added hooks to enforce them](/ai/security/development/tools/2026/02/01/securing-claude-code-hooks-best-practices.html). Each step helped, but the model kept finding new ways to cut corners I hadn't explicitly forbidden. Then skills came into swing.

I also tried existing frameworks (when I started they did not really exist yet). [BMAD](https://github.com/bmadcode/BMAD-METHOD), spec-driven development, [HumanLayer](https://github.com/humanlayer/humanlayer) (which I genuinely liked for its "thoughts" directory approach to project memory). But in practice, I found most of them too dogmatic. They impose a rigid process that doesn't bend to the messy reality of actual projects, where sometimes you need to spike something quickly, sometimes you need deep planning, and the model needs to know the difference. What works is pragmatism: take the good ideas from each, discard the ceremony, and [build something that adapts to how you actually work](/ai/tools/productivity/2025/10/14/supercharge-claude-code-with-custom-configuration.html).

I am not explaining my full system in this series: it would take way more to explain that, maybe I will do that later. (I am now building a semi-automated system, that takes these best practices and so far is actually able to write better code than I can, maintaining a level of quality and coherence) But it remains a work in progress.

## The System: Requirements, Specifications, Best Practices

What I ended up building is a connected system of three layers:

**Requirements** define *what* must be true. Each has an ID, a description, and a project phase (start, mvp, production). For example:

> **REQ-API-001**: Error responses must follow RFC 9457 (Problem Details for HTTP APIs) with a consistent structure: `type`, `title`, `status`, `detail`, and optional `instance` and extension fields. *(Phase: mvp)*

**Specifications** define *how* to implement each requirement. They trace back to requirement IDs:

> **Error format**: RFC 9457 Problem Details. Content-Type: `application/problem+json`. Structure: `{ "type", "title", "status", "detail", "instance" }`. Use `type` as a stable URI for each error category. Add extension fields as needed. Never expose stack traces in production. *(Traces to: REQ-API-001)*

**Best practices** provide the *deep knowledge*, the why, the trade-offs, the common mistakes, the patterns. They are what this series shares.

The traceability matters. When the model writes an error handler, it doesn't just know "use RFC 9457", it knows the requirement demands it, the specification defines the exact format, and the best practice file explains why generic errors are useless at 2 AM and how to add context that actually helps diagnose problems. And not to forget: the extensive training data knows more about this standard than I will ever do: you just have to 'trigger' it to come forward from that vast amount of data.

This is part one of a two-part series. The files discussed here (and the rest) are available in a [public repository](https://github.com/albertsikkema/claude-code-best-practices) that I'll keep updating as I add more.

## "Doesn't This Cost a Lot of Tokens?"

Yes. It does.

Loading best practice files, requirements, and specifications into context costs tokens. There's no way around that. But the cost is manageable if you're smart about *when* you load *what*.

I don't dump all 18 files into every conversation. The full files are loaded during the steps that actually use them: planning and review. When the model is designing an approach or reviewing code against standards, it needs the deep knowledge. When it's implementing a well-defined task from an approved plan, the plan itself already encodes the relevant practices, the model doesn't need to re-read the source material. And every now and then you find a little gem, where Claude Code starts correcting you based on your own best practices. One of mine says to leave no dead code in the repo. It corrected me that my commented-out code was not in accordance with the best practices.

The alternative, not spending the tokens, is worse. Without this context, the model drifts. It makes its own architectural decisions, picks its own error format, skips validation it doesn't know you care about. Then you spend tokens correcting it. And correcting the corrections. And explaining why the correction matters. And next conversation, you start over.

In the end it is simple math: pay upfront to load the model with your standards at the right moments, or you pay afterwards and repeatedly to fix the output when it inevitably diverges from what you need. The upfront cost is predictable and targeted. The correction cost is unpredictable and compounds. (both in time and in money)

So yes, be selective: nothing more and nothing less than what is needed at that point. A frontend task doesn't need the container security file. A database migration doesn't need the accessibility rules. Load what's relevant to the phase of work you're in.

## What This Post Covers

In this first post: the foundational practices every project needs regardless of what you're building.

1. [Layered Architecture](#1-layered-architecture), how to structure code so Claude doesn't write spaghetti
2. [Error Handling](#2-error-handling), turning "something went wrong" into actionable diagnostics
3. [Testing Strategy](#3-testing-strategy), tests that catch real bugs, not just verify mock wiring
4. [API Design](#4-api-design), consistent, predictable interfaces that follow standards
5. [Data Integrity](#5-data-integrity), because corrupt data is worse than downtime
6. [Structured Logging](#6-structured-logging), logs that are actually useful at 3 AM

For each practice, I'll show the problem it solves, a taste of the key rules, and how it connects back to the requirements and standards it's built on. Most of this is no rocket science, and you might not agree with some choices, which is fine. Define your own.

---

## 1. Layered Architecture

**The problem**: Without explicit guidance, Claude tends to put everything in one place. Business logic in the API handler. Database queries mixed with validation. HTTP status codes decided deep inside a service function. It works, until you need to test it, replace a dependency, or understand what the code does.

**The principle**: Separate code into distinct layers with strict downward dependency, handler, service, repository, model. Each layer has one job and never reaches past its neighbour.

```
Handler / API Layer      -- owns the transport protocol
    |
Service / Business Logic -- owns the rules
    |
Repository / Data Access -- owns the queries
    |
Domain Model             -- owns the data shape
```

**Key rules from the file**:

- The handler validates input shape and formats responses. It does not contain business rules.
- The service layer orchestrates business logic and defines transaction boundaries. It does not know about HTTP status codes or request objects.
- The repository layer executes queries and maps results. It does not decide what data to return based on business rules.
- Dependencies go down only. A service never imports from a handler. A repository never calls a service.

**Why it matters for AI-generated code**: When the model understands this separation, it stops making the most common architectural mistake: putting everything in the handler. It writes services you can test without spinning up an HTTP server. It writes repositories you can swap without rewriting business logic.

**Traces to**: REQ-QUAL-005 (testable code), REQ-QUAL-006 (maintainable tests). Built on the principle that each module should be describable in one sentence.

## 2. Error Handling

**The problem**: Claude's default error handling is either too aggressive (catch everything, return a generic message) or too lazy (let exceptions propagate without context). Both are bad. The first hides bugs. The second makes debugging impossible.

**The principle**: Errors are not exceptional, they're a normal part of program execution. Handle them explicitly at every layer, propagate them with context, translate them at boundaries, and never swallow them silently.

**Key rules from the file**:

- **Never swallow errors.** `catch (e) { log(e) }` is not handling, it's ignoring with a paper trail. The system continues in a corrupt state.
- **Add context when propagating.** Each layer adds what it was doing. The final message reads like a stack of explanations: `"create order: charge payment: POST /payments: connection refused"`.
- **Translate at boundaries.** A repository throws a database error. The service translates it to a domain error. The handler translates it to an HTTP response. Each layer speaks its own language.
- **Distinguish error types.** Retriable (5xx, timeout) vs terminal (4xx, auth) vs corruption. Different types require different responses: retry, report to user, or alert on-call.

**The standard**: Error responses follow [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) (Problem Details for HTTP APIs), a machine-parseable format with `type`, `title`, `status`, `detail`, and `instance` fields. This replaces the ad-hoc `{ "error": "something went wrong" }` that Claude defaults to.

```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 422,
  "detail": "Account abc-123 has EUR 10.00, but the transaction requires EUR 25.00.",
  "instance": "/orders/order-456"
}
```

**Traces to**: REQ-API-001 (RFC 9457 error format), REQ-API-002 (appropriate status codes), REQ-OBS-002 (errors logged with sufficient context).

## 3. Testing Strategy

**The problem**: Left to its own devices, Claude writes tests that test nothing. It mocks everything, asserts that mocked functions were called with the right arguments, and calls it a day. The tests pass. The code is broken. Nobody notices until production.

**The principle**: Test behaviour, not implementation. The test pyramid (unit -> integration -> E2E) defines how many tests of each type to write, but the core rule is simpler: if everything is mocked, the test proves nothing.

**Key rules from the file**:

- **Every feature tests five things**: happy path, validation errors, auth errors, downstream failures, and edge cases.
- **Mock at system boundaries**, not internally. Mock the payment gateway, not the service that calls it. Your test should exercise the actual code path.
- **Name tests as specifications**: `test_create_user_with_duplicate_email_returns_409` tells you exactly what broke without reading the test body.
- **Tests must be independent and parallelisable.** No shared state, no ordering dependencies, no "run test A before test B."
- **Coverage target**: 80% overall, 70% minimum per module. Not as a vanity metric, but as a signal that error paths are tested.

**Why it matters for AI-generated code**: When the model has this file, it stops writing tests that just verify mock wiring. It writes tests with real assertions against real behavior. And when you ask it to add error handling, it also adds the test that verifies the error handling works. This ties into the broader [human-in-the-loop review](/ai/llm/development/best-practices/2025/11/14/human-in-the-loop-ai-code-review.html) approach: the AI writes, you verify.

**Traces to**: REQ-QUAL-005 (test happy and error paths), REQ-QUAL-006 (useful, maintainable tests), REQ-QUAL-003 (coverage thresholds), REQ-QUAL-007 (test framework bootstrap from day one).

## 4. API Design

**The problem**: Claude builds APIs that work for the happy path but fall apart at the edges. No pagination. Inconsistent error formats. Stack traces in production error responses. Rate limiting that returns no headers so clients can't self-throttle.

**The principle**: An API is a contract. It should be consistent, predictable, and follow established standards so that clients (and future developers) can rely on its behavior without reading the implementation.

**Key rules from the file**:

- **Standard HTTP status codes.** Not just 200 and 500, use the full vocabulary: 201 (created), 204 (no content), 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 409 (conflict), 422 (unprocessable), 429 (rate limited).
- **RFC 9457 for all errors.** Same format, every time, machine-parseable. The `type` field is a stable URI that clients can switch on.
- **Cursor-based pagination** for large datasets. Offset pagination breaks under concurrent writes. Include `items`, `hasMore`, and `nextCursor` in every list response.
- **Rate limiting with standard headers.** `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` on every response. 429 with `Retry-After` when exceeded. Clients shouldn't have to guess.
- **Never expose internals.** No stack traces, no SQL errors, no file paths in production responses. Log them server-side, return a clean error to the client.

**Traces to**: REQ-API-001 through REQ-API-004, REQ-SEC-009 (rate limiting), REQ-DOC-001 (OpenAPI documentation). The specification further mandates generating OpenAPI docs from code annotations and validating them in CI.

## 5. Data Integrity

**The problem**: Claude writes code that works perfectly, until two requests arrive at the same time, or a payment fails after inventory was already deducted, or a migration drops a column while the old code is still running. Concurrency and partial failure are invisible in code reviews. They only surface in production.

**The principle**: Data corruption is worse than downtime. A crashed server restarts in minutes. Corrupt data requires investigation, manual fixes, and sometimes can't be recovered at all.

**Key rules from the file**:

- **Transactions for multi-step mutations.** Create order, deduct inventory, charge payment, all in one transaction. If payment fails, everything rolls back.
- **Database constraints as the last line of defence.** `NOT NULL`, `UNIQUE`, `FOREIGN KEY`, `CHECK` constraints. Application validation can have bugs. The database doesn't lie.
- **Idempotency by design.** Every operation that might be retried (webhooks, queue messages, API calls) must produce the same result when executed twice.
- **Race condition prevention.** Optimistic locking (version column) for low-contention reads. Pessimistic locking (`SELECT ... FOR UPDATE`) for critical sections. `INSERT ... ON CONFLICT` instead of check-then-insert.
- **Expand-contract migrations.** Never drop or rename a column in the same migration that adds its replacement. Add the new column, backfill, deploy code that uses it, then remove the old one.

**The framework**: Data quality is evaluated across eight dimensions from [DAMA-DMBOK](https://www.dama.org/cpages/body-of-knowledge): accuracy, completeness, consistency, integrity, reasonability, timeliness, uniqueness, and validity. These give you a vocabulary for discussing data issues.

**Traces to**: REQ-DATA-001 (versioned migrations), REQ-DEPLOY-002 (expand-contract pattern), REQ-DEPLOY-003 (tested rollback scripts).

## 6. Structured Logging

**The problem**: Claude's default logging is `console.log("user created")` or `logger.info(f"Processing order {order_id}")`. String interpolation, no structure, no context. Useless in production where you need to filter, aggregate, and correlate across services.

**The principle**: Logs are structured data, not formatted strings. Every log entry should be a set of key-value pairs that machines can parse and humans can read.

**Key rules from the file**:

- **Structured fields, not string interpolation.** `logger.info("order_created", user_id=user.id, order_id=order.id, total=order.total)`, not `logger.info(f"Created order {order.id} for user {user.id}")`.
- **Consistent field names across the codebase.** `user_id`, `request_id`, `session_id`, `error_type`, `duration_ms`, `operation`. Pick names once and stick with them.
- **Never log secrets.** Not passwords, not tokens, not API keys. Log their presence: `api_key_present=true`, not the value.
- **Log at system boundaries.** Request received, request completed, outbound call started, outbound call finished, job started, job completed. Not inside tight loops.
- **Severity levels mean something.** DEBUG for developer-only detail, INFO for expected events, WARN for unexpected-but-handled situations, ERROR for failures requiring investigation. Don't log everything as INFO.
- **Correlation IDs.** Generate a request ID at the entry point, propagate it through all downstream calls. Every log line includes it. When something breaks, you can trace the entire request path.

**Traces to**: REQ-OBS-001 (structured JSON logs with request context), REQ-OBS-002 (errors logged with diagnostic context), REQ-OBS-003 (correlation IDs propagated through downstream calls).

---

## The Connection Between Layers

These six practices don't exist in isolation. They reinforce each other:

- **Layered architecture** creates the boundaries where **error handling** translates errors between layers.
- **Error handling** defines the error format that **API design** exposes to clients.
- **Testing strategy** verifies all of the above, and is made possible by the clean separation that **layered architecture** provides.
- **Data integrity** protects the database layer that sits at the bottom of the architecture.
- **Structured logging** observes what happens across all layers, with the correlation IDs that **API design** generates at the entry point.

And all of them trace back to requirements with IDs, specifications with implementation details, and a tech stack where every library choice is justified. The model doesn't just follow rules, it understands a system.

## Try It Yourself

The full files for all six practices discussed here, plus twelve more covering security, resilience, accessibility, deployment, and more, are available in the [public repository](https://github.com/albertsikkema/claude-code-best-practices).

You can use them as-is by dropping them into a `best_practices/` directory that your Claude Code setup references, or adapt them to your own stack and standards. The format is simple: a principle, a "why" section, core rules with code examples, and common mistakes. The model picks them up without any special configuration, they just need to be part of the context.

**Coming up next:**

- **Part 2: Security, Privacy, Operations, Accessibility, SEO, and Integration Patterns** -- the remaining 12 files covering authorization, validation, containers, privacy, resilience, deployment, observability, background jobs, accessibility, SEO, robots/scraping, and LLM integration.

---

*Have questions or want to share how you keep AI-generated code in line? <a href="#" onclick="task1(); return false;">Get in touch</a>.*

## Standards and References

- [RFC 9457 - Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)
- [WCAG 2.2 - Web Content Accessibility Guidelines](https://www.w3.org/TR/WCAG22/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [DAMA-DMBOK - Data Management Body of Knowledge](https://www.dama.org/cpages/body-of-knowledge)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/)
- [OCI Image Specification](https://github.com/opencontainers/image-spec)
