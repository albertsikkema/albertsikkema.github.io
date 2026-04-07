---
layout: post
title: "Security by Design: Using Project CodeGuard as AI Guardrails"
date: 2026-04-07
categories: ai development security
description: "How I use 109 OWASP-based security rules from Project CodeGuard to embed security by design into AI coding workflows."
keywords: "Claude Code, Project CodeGuard, OWASP, security by design, AI security, secure coding, CoSAI, security rules, code review, vulnerability prevention"
image: security-by-design-with-project-codeguard-blog.png
---

<figure>
  <img src="/assets/images/security-by-design-codeguard.jpg" alt="Hedgehog walking through green grass, nature's own security by design" width="1920" height="1440" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>Security by design, the natural way. Photo by <a href="https://unsplash.com/@smoliak">Viktor Smoliak</a> on <a href="https://unsplash.com/photos/7B9Ia1dQL_U">Unsplash</a>.</figcaption>
</figure>

In the [previous two posts](/ai/development/best-practices/2026/03/31/evidence-based-best-practices-ai-guardrails.html) I shared 18 best practice files that keep AI-generated code production-ready, covering architecture, error handling, security, privacy, accessibility, and more. Those are my own distillations, written from experience and grounded in standard and literature. This post adds another layer: security by design (or better 'early implementation')

The rules come from [Project CodeGuard](https://project-codeguard.org/), an open-source, model-agnostic security framework maintained by [CoSAI (Coalition for Secure AI)](https://github.com/cosai-oasis/project-codeguard) and originally developed by Cisco. The framework provides over a hundred security rules derived from OWASP cheat sheets and CWE guidance, formatted specifically so AI coding agents can use them during code generation and review.

I'm not going to walk through every rule, there are 109 of them and that would be a very boring read. Instead, I'll show how I've wired them into my Claude Code setup so they activate at the right moments, and how you could do something similar regardless of your tooling.

## What is Project CodeGuard?

Project CodeGuard ships two sets of rules:

**Core rules** (22 files) cover broad security domains: input validation, authentication, authorization, session management, cryptography, file handling, logging, container security, supply chain, privacy, and more. These are language-tagged, each file lists which programming languages it applies to in its YAML frontmatter.

**OWASP rules** (86 files) are more granular. They map closely to individual [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/): SQL injection prevention, CSRF, XSS, content security policy, JWT handling, OAuth2, Docker security, Kubernetes security, GraphQL, REST assessment, and dozens more.

The format is straightforward. Each rule is a markdown file with YAML frontmatter listing the applicable languages and a description. The body contains the actual guidance: principles, do/don't patterns, code examples in multiple languages, and implementation checklists. Here's a taste of the authorization rule:

```markdown
---
description: Authorization and access control (RBAC/ABAC/ReBAC, IDOR, mass assignment, transaction auth)
languages: [c, go, java, javascript, php, python, ruby, typescript, yaml]
alwaysApply: false
---

## Authorization & Access Control

### Core Principles
1. Deny by Default
2. Principle of Least Privilege
3. Validate Permissions on Every Request
4. Prefer ABAC/ReBAC over RBAC
```

The rules don't guarantee secure code. They steer the model toward safer patterns and away from common mistakes. Think of them as a knowledgeable colleague looking over the model's shoulder, one who has memorized every OWASP cheat sheet.

## How I Use Them

I've built a fairly extensive Claude Code setup with custom commands, agents, skills, and helper scripts, more than what most people will have. The examples below show how I've wired the rules into that setup. Your setup will look different, and that's fine. The underlying pattern is what matters: load the right rules at the right moment, not all of them all the time.

The rules sit in `memories/security_rules/` with two subdirectories: `core/` and `owasp/`. They're not loaded into every conversation, that would burn tokens on rules about Kubernetes security when you're writing a Python CLI tool. Instead, they're pulled in selectively by the parts of my setup that need them.

### Planning Phase Risk Analysis

Before writing a plan, my setup spawns a quality risk analyzer agent. It takes the feature description, figures out which security areas apply (does this feature handle user input? sessions? file uploads?), reads the relevant CodeGuard rules, then surfaces risks and recommendations that get baked into the plan itself.

The result is that security considerations don't popup at review. They're in the plan from the start, with specific rules referenced. The developer (or the model) knows what to watch for during implementation. (Which does fit the security-by-design paradigm nicely)

### Security-Aware PR Reviews

My PR review workflow spawns multiple agents in parallel, code quality, test coverage, best practices, and security. The security agent is where CodeGuard rules come alive.

The agent's instructions include a mapping table: if the diff touches user input, load the input validation rules, etcetera. The agent reads the relevant 3-5 rule files, then applies them against the actual changed code.

```
| If code handles...  | Read these rules                                          |
|----------------------|----------------------------------------------------------|
| User input           | input-validation-injection, injection-prevention          |
| Authentication       | authentication, password-storage, credential-stuffing     |
| Authorization        | authorization-access-control, insecure-direct-object-ref  |
| File operations      | file-handling-and-uploads, file-upload                    |
| Docker/K8s           | devops-ci-cd-containers, docker-security, kubernetes      |
```

This is the same table that appears in the agent definition, the code audit command, and the quality risk analyzer. This makes sure that there is consistency in mapping across all those steps.

### Full Security Audits

My code audit command runs a full security analysis across 18 areas, split into three phases: critical controls (data isolation, injection, authentication, XSS, file uploads, secrets), security configuration (rate limiting, CSRF, RBAC, database, logging, third-party integrations), and implementation patterns (secure coding, error handling, API security, frontend, dependencies, performance).

Phase 0 of this audit is "framework discovery", it detects the tech stack, then loads the relevant CodeGuard rules filtered by language. The audit then cross-references findings against both my own best practice files and the CodeGuard rules, giving two independent perspectives on the same code.

## How You Could Use Them

You don't need my specific setup to benefit from these rules. Here's the general pattern:

**Step 1: Get the rules.** Clone the [Project CodeGuard rules repository](https://github.com/project-codeguard/rules). The rules are in `core/` and `owasp/` directories.

**Step 2: Put them where your agent can find them.** For Claude Code, that means somewhere in your project directory or a path your configuration references. I use `memories/security_rules/` but any path works.

**Step 3: Don't load everything.** The rules total a lot of tokens. You benefit costwise from selective loading based on what the code actually does. 

**Step 4: Build a mapping.** Create a simple lookup: "if the code handles X, load rules Y and Z." This is the most important part. Without it, you either load nothing (useless) or everything (expensive and noisy).

**Step 5: Wire it into your review/audit workflow.** Whether that's a custom command, a hook, a skill, or just a prompt, the rules need to be loaded at the point where security matters. That's in planning and review.

The rules also come with a [SKILLS.md template](https://project-codeguard.org/getting-started/) that you can drop directly into coding agents that support skills (Claude Code, Cursor, Copilot). The template defines when to activate the skill and how to apply the rules based on what the code does. I do not use it as a skill. Why? Because that would imply that I need to think about it, and the whole point is that I do not need to remember using it, but that it is part of everything I do. So it should be there in the background, just out of sight but always there and steering the plans and reviews.

## Why External Rules and Not Just "Be Secure"

Simply prompting "Write secure code" is not gonna work for you. It is too simple, too broad and does not comply with the idea of security by design.

The model has extensive security knowledge in its training data. The art of getting this to work is activating the right knowledge at the right time. When you load a CodeGuard rule about SQL injection prevention, you're not teaching the model something new, it has a lot of data about injection prevention: you're simply telling it "this is relevant right now, apply it." The rule contains specific patterns (use parameterized queries, never concatenate user input into SQL, use least-privilege database users) that the model knows but might not prioritize without the prompt.

This is the same principle behind the best practice files from the previous posts: bring specific knowledge to the front of the model's attention when it matters. The good thing is that CodeGuard rules are maintained, OWASP-backed, and cover a broader surface than I could write. 

Keep in mind that this does not make your code secure: it still is up to you to decide if it is secure in your context. But in my experience this does help a lot! (My automated code reviews have never been so sharp and to the point as now I started applying these principles.)

## Try It Yourself

The CodeGuard rules are available from the [Project CodeGuard rules repository](https://github.com/project-codeguard/rules). The best practice files from the previous posts are in [my public repository](https://github.com/albertsikkema/claude-code-best-practices). Grab what's relevant to your stack and wire them into your workflow.

---

*Have questions or want to share your approach? <a href="#" onclick="task1(); return false;">Get in touch</a>.*

## References

- [Project CodeGuard (old Cisco repo)](https://project-codeguard.org/), the framework
- [CoSAI / Project CodeGuard (OASIS)](https://github.com/cosai-oasis/project-codeguard), the CoSAI-maintained repository
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/), the source material for many CodeGuard rules
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CoSAI (Coalition for Secure AI)](https://github.com/cosai-oasis), the broader initiative behind CodeGuard, with more AI security projects worth exploring
- [Announcing a New Framework for Securing AI-Generated Code (Cisco Blog)](https://blogs.cisco.com/ai/announcing-new-framework-securing-ai-generated-code)
