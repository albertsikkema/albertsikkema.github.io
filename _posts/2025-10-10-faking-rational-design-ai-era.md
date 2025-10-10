---
layout: post
title: "Faking a Rational Design Process in the AI Era: Why Documentation Matters More Than Ever"
date: 2025-10-10
categories: ai development documentation llm
---

In 1986, David Parnas and Paul Clements published a paper with a provocative title: ["A Rational Design Process: How and Why to Fake It"](https://users.ece.utexas.edu/~perry/education/SE-Intro/fakeit.pdf). Their central thesis was radical yet practical: while a perfectly rational software design process is impossible to achieve, we should document our work *as if* we had followed one. Nearly four decades later, working with AI programming assistants like Claude Code, this insight has become more relevant than ever.

## The Impossible Ideal

Parnas and Clements identified why truly rational software design is unattainable:

- **Requirements are always incomplete**: Clients rarely know exactly what they want upfront
- **Facts emerge during implementation**: Critical details only become clear as you build
- **Humans can't manage all the complexity**: We need to separate concerns, but that process itself introduces errors
- **External changes invalidate decisions**: Requirements, constraints, and technologies shift mid-project
- **Preconceived ideas influence design**: We bring baggage from previous projects and favorite solutions
- **Economic pressures force compromises**: Reusing existing code or sharing with other projects creates non-ideal solutions

Sound familiar? These challenges haven't disappeared in 2025. If anything, the pace of change has accelerated.

## Why Fake It Anyway?

Despite the impossibility of perfect rationality, Parnas and Clements argued for documenting the design *as if* we had been perfectly rational. The benefits:

1. **Guidance for designers**: A clear process helps navigate overwhelming complexity
2. **Better outcomes**: Trying to follow an ideal process yields better results than ad-hoc approaches
3. **Standardization**: Organizations benefit from consistent procedures across projects
4. **Progress measurement**: You can track where you are relative to the ideal
5. **Easier reviews**: Outsiders can meaningfully review work that follows a known process

The key insight: documentation should show the *cleaned-up, rationalized version* of what happened, not the messy discovery process. Just like mathematicians publish elegant proofs rather than their tortured paths to discovery.

## Enter the AI Era: Documentation as the Single Source of Truth

Here's where things get interesting for those of us working with AI assistants like Claude Code. The traditional challenge was maintaining documentation that reflected our current understanding. We'd make decisions, implement them, discover issues, backtrack, and adjust—but documentation often lagged behind or never got updated at all.

With AI-assisted development, particularly using approaches borrowed from [HumanLayer](https://humanlayer.dev/), documentation becomes the **control mechanism** for maintaining coherent design across AI interactions.

### The Modern "Fake It" Process

When working with Claude Code, I've found that the Parnas approach maps beautifully to a continuous cycle:

**1. Research Phase**
- Use Claude Code to analyze the codebase, existing patterns, and constraints
- Document findings in structured form (requirements, constraints, architecture)
- Identify gaps in understanding and fill them

**2. Plan Phase**
- Create comprehensive implementation plans that assume perfect knowledge
- Document design decisions, alternatives considered, and rationale for choices
- Structure plans as if we knew everything from the start (even though we don't)

**3. Execute Phase**
- Claude Code implements following the documented plan
- When discoveries happen (they always do), deal with them in the moment
- Think through and investigate possible solutions
- For minor discoveries: adjust and continue execution
- For major disruptions: stop and return to planning phase with new insights
- Let the messy reality unfold—documentation comes later

**4. Review & Rationalization Phase**
- Validate implementation against original documented requirements
- Update the plan to reflect what actually happened—presented *as if* it was always intended
- Update project documentation (CLAUDE.md, ADRs) with the rationalized narrative
- Document design decisions made, alternatives considered and rejected
- Clean up the story: show the elegant solution, not the tortured path to discovery

The crucial difference: **documentation isn't created after the fact—it's the living artifact that guides each AI interaction**.

## Why This Matters More with AI

Traditional development had one developer (or team) maintaining context in their heads. Documentation helped with handoffs and long-term maintenance, but daily work relied heavily on human memory.

AI assistants have no memory between sessions. Every conversation starts fresh. Without authoritative documentation:

- Your AI assistant (Claude Code in my case) makes assumptions based on visible code patterns
- Design decisions get lost between sessions
- Inconsistent approaches emerge across features
- The codebase becomes a patchwork of different "styles" from different AI interactions

**Documentation becomes the anchor** that ensures continuity of vision across all AI-assisted development work—whether you're using Claude Code, GitHub Copilot, Cursor, or any other AI programming assistant.

## Practical Implementation

In my work using Claude Code, I maintain several documentation artifacts that serve as the "rational design" foundation:

**CLAUDE.md**: The project's source of truth
- Architecture overview and key design decisions
- Coding standards and patterns
- Testing requirements and coverage expectations
- Multi-tenant isolation rules
- Common pitfalls and how to avoid them

**README.md**: Implementation guide
- Setup instructions
- Development workflows
- Deployment process
- Environment configuration

**ADRs (Architecture Decision Records)**: Historical context
- Major decisions with rationale
- Alternatives considered and why they were rejected
- Consequences of each decision

Every time Claude Code works on a feature, it references these documents first. When we discover something new or change direction during execution, we deal with it pragmatically. Then, at the end of the cycle, we update the documentation to reflect the final solution—presented as if that was always the plan.

## The Rationalization Loop

Here's where it gets powerful. The messiness happens during execution—you discover edge cases, find better approaches, hit unexpected constraints. But after each development cycle, you perform the "faking" that Parnas advocated:

1. **Reflect on discoveries**: What assumptions were wrong? What worked well? What alternatives did you try?
2. **Update the plan**: Revise the implementation plan to show the final approach as if it was the original design
3. **Rationalize the narrative**: Update project documentation (CLAUDE.md, ADRs) to present a coherent story
4. **Document rejected alternatives**: Capture what you tried and why it didn't work—this prevents future revisiting of dead ends
5. **Feed forward**: Next Claude Code session starts with improved, rationalized context

This creates a virtuous cycle where documentation quality continuously improves, and each AI interaction becomes more effective because it inherits the accumulated wisdom of past cycles—cleaned up and rationalized.

## The Human Element

Parnas and Clements emphasized that faking rationality doesn't mean lying—it means presenting the *refined, polished version* of our work. The human's role is crucial:

- **Curate the narrative**: Decide what belongs in documentation
- **Maintain coherence**: Ensure updates don't contradict earlier decisions (or explicitly supersede them)
- **Judge quality**: Verify that AI implementations match documented intent
- **Evolve the vision**: Update the "rational design" as understanding deepens

As I discussed in my [PDCA cycle post](/ai/development/productivity/2025/09/23/pdca-cycle-master-claude-code.html), the human must remain in the loop at every step. You're not just supervising the AI—you're maintaining the rational design narrative that guides it.

## Documentation as Design Constraint

One final insight: good documentation constrains the solution space in helpful ways. By documenting requirements, architecture, and design decisions clearly, you:

- **Reduce decision paralysis**: Claude Code doesn't waste time exploring already-rejected approaches
- **Ensure consistency**: New features align with established patterns
- **Enable validation**: You can check if implementations match documented intent
- **Facilitate onboarding**: New team members (human or AI) get up to speed quickly

The documentation becomes the "rails" that keep development on track, even as the messy reality of discovery unfolds beneath the surface.

## Conclusion: Embracing the Paradox

Software development has always been messier than we'd like to admit. Parnas and Clements recognized this in 1986, and it remains true today. The difference is that now we have AI assistants that can handle much of the implementation work—but only if we give them proper guidance.

By maintaining documentation that presents a rational design process—even when the actual process was anything but—we create:

- **Better software**: Coherent architecture emerges from coherent documentation
- **More effective AI collaboration**: Every interaction builds on a solid foundation
- **Easier maintenance**: Future developers (and future AI sessions) understand the *why* behind decisions
- **Reduced technical debt**: Decisions are documented and can be revisited systematically

The key lesson from Parnas and Clements endures: it's not about achieving perfect rationality (impossible), but about **documenting as if you had**. In the AI era, this practice transforms from a nice-to-have into an essential discipline.

Your documentation is no longer just a record of what you built—it's the instruction manual that guides every AI interaction toward your vision. Keep it current, keep it rational, and keep faking it. The results will speak for themselves.

---

*Want to see this approach in action? Check out my post on [using the PDCA cycle with Claude Code](/ai/development/productivity/2025/09/23/pdca-cycle-master-claude-code.html) for a structured workflow that embodies these principles.*
