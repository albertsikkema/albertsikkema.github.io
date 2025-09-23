---
layout: post
title: "Using the PDCA Cycle to guide Claude Code for Software Development"
date: 2025-09-23
categories: ai development productivity
---

You're probably familiar with the PDCA cycle: Plan, Do, Check, Act ([Wikipedia](https://en.wikipedia.org/wiki/PDCA)). It's a continuous improvement methodology that's been around since the 1950s, helping organizations optimize their processes. But here's something interesting: when working with Claude Code to write software, you can implement a remarkably similar strategy that transforms AI-assisted coding from a chaotic experiment into a structured, reliable process.

## Plan - Setting the Foundation

The magic starts with planning. Before diving into code, you need to ensure both you and Claude Code are perfectly aligned on what needs to happen. Think of it as creating a detailed blueprint that Claude Code can follow without getting lost or making assumptions.

Here's what a comprehensive planning phase looks like:
- Research the codebase extensively using the Task tool to spawn specialized agents
- Analyze existing patterns: architecture, components, database schemas, API routes, testing frameworks
- Review both local documentation and external resources for the tech stack
- Apply the "No Prior Knowledge" test: would an AI with only this plan be able to implement successfully?
- Create a comprehensive implementation blueprint with specific file paths, patterns, and validation gates
- Include all context needed for one-pass implementation success

## Do - Bringing the Plan to Life

With a solid plan in hand, it's time to execute. This is where Claude Code does its thing, systematically working through your requirements while maintaining code quality and consistency.

The execution phase follows these key steps:
- Set up Git workflow and create feature branch
- Analyze the PLAN thoroughly to understand all requirements and constraints
- Use TodoWrite tool to break down implementation into trackable tasks
- Implement systematically: database layer, API endpoints, frontend components, email integration
- Write tests alongside implementation (>90% coverage requirement)
- Run validation gates continuously: formatting, build, migrations, tests, security checks
- Verify multi-tenant isolation and customer data filtering in all operations
- Create PR with description of the issue (linked to a Github or Jira issue)

## Check - Trust, but Verify

Here's where things get interesting. Claude Code is incredibly capable, but it occasionally takes creative liberties or makes assumptions that might not align with your exact vision. The Check phase is your quality control gate.

This comprehensive review includes:
- Run code quality checks in parallel using subagents: formatting (npm run clean), linting, and code review
- Execute comprehensive test suite: unit, integration, and e2e tests with coverage validation
- Verify documentation updates: README.md, CLAUDE.md, and environment variables documentation
- Review API documentation: endpoints, request/response examples, and tests
- Consolidate all findings into a timestamped review report
- Flag any deviations from the plan, missing tests, or incomplete documentation

## Act - Sealing the Deal

The final step brings everything together. This is where you confirm that the implementation meets your standards and prepare it for integration into your codebase.
- Check git status and analyze what changed (git status, git diff --staged)
- Help decide what to stage if nothing is staged yet
- Suggest appropriate commit type (feat/fix/docs/style/refactor/perf/test/chore)
- Create conventional commit message with Jira or Github ticket linking
- For complex changes, suggest breaking into multiple commits
- Ask for approval before creating the commit
- Offer to push or create PR with comprehensive documentation of changes

## The Human Element: Why You're Essential

I've found that keeping a human in the loop at every step is absolutely crucial for success:

### During Planning
Iterating over the plan yields significantly better results. Take the time to read through the plan and really think about it. Is it complete? Does it cover edge cases? Will Claude Code have enough context to succeed? Are there decisions that deviate from your projects practices? And most importantly, does it solve the issue? This is by far the most important step in this cycle.

### During Execution
In the Do phase, Claude Code takes the wheel. You can watch it work – it's fascinating at first, though I'll admit it becomes less exciting after the hundredth file edit. But staying engaged helps you catch issues early. In that case you can choose to adjust, or just remove all the changes and start over with planning.

### During Checking
This is perhaps the most critical step. Remember: you are responsible for the code, not Claude Code. Ensure everything meets your standards. Finding lots of mistakes or deviations? It might be best to revert the changes and revisit the planning stage. Claude Code sometimes takes shortcuts, especially with testing and validation gates.

### During Action
Claude Code can handle the commit process for you – all the heavy lifting is done. However, I still prefer to push manually. It gives me one final opportunity to review my work and ensures I maintain control over what goes into the repository.

## Key Lessons Learned

**Context is everything!** The more context you provide upfront, the better the results. Claude Code can only work with what it knows.

**Git versioning is your safety net!** A solid versioning strategy means you can experiment freely, knowing you can always roll back if needed. You'll thank yourself later.

## Beyond PDCA: Additional Prompts for Your Toolkit

This PDCA approach has worked wonderfully for feature development, but I've also created specialized prompts for other common scenarios:

- **Pull Request Creation and Review**: Automated PR generation with comprehensive descriptions, linking to tickets, and review checklists
- **Security Analysis**: Deep-dive security audits that check for vulnerabilities, validate input sanitization, and ensure proper authentication/authorization
- **Code Efficiency Analysis**: Performance optimization reviews that identify bottlenecks, suggest improvements, and validate resource usage
- **Code Review**: Systematic code quality checks that ensure adherence to best practices, maintainability, and team standards

Each of these prompts follows a similar structured approach, ensuring consistency and reliability in your AI-assisted development workflow.

## Final Thoughts

The PDCA cycle isn't just a manufacturing concept – it's a powerful framework for working with AI coding assistants. By structuring your interactions with Claude Code through Plan, Do, Check, and Act phases, you transform what could be unpredictable AI assistance into a reliable, repeatable process that consistently delivers quality code.

The key is remembering that Claude Code is a powerful tool, but it's still just that – a tool. Your expertise, oversight, and strategic thinking remain irreplaceable. Use the PDCA cycle to harness Claude Code's capabilities while maintaining the control and quality standards your projects deserve.