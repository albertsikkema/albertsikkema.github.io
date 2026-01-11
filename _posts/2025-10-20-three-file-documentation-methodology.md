---
layout: post
title: "Three Files Are All You Need: Rethinking Project Documentation for AI-Assisted Development"
date: 2025-10-20
categories: ai development documentation productivity
description: "Simplify project documentation for AI-assisted development. Learn a minimal 3-file approach using MoSCoW prioritization for better productivity."
keywords: "AI documentation, project management, MoSCoW method, lean documentation, Claude Code workflow, developer productivity"
---

Last week I spent the better part of an hour documenting a user authentication feature. In the end I wrote it up in three places: the epic file, the must-haves document, and the technical todo list. Same information, slightly different formats, all needing to stay synchronized as requirements evolved. And that was my own project with simple file-based project documentation. If I have to use Jira it becomes even more fragmented and time-consuming. It is a lot of administration, and what the actual benefit is, is not always clear. Especially in small teams or as a solo developer. 

And then AI enters the equation. You'd think having lots of documents wouldn't be a problem—Claude can read everything, right? But reading isn't the issue. Getting the *right* information out is. And here's where it gets expensive: that MCP server for Atlassian that connects to Jira? It loads project metadata, issue histories, and board configurations into your context window. Context you could be using for actual code, implementation plans, or architectural decisions.

Worse, how often does Claude actually need to pull from Jira during implementation? In my experience, rarely. Maybe at the start to understand requirements, maybe at the end to update ticket status. But during the actual work? That context sits there, expensive and mostly idle, like paying for a premium subscription you use twice a month.

And what is the source of truth anyway? In the end it's the actual code, not the user documentation or project management system. The code is what runs, what gets tested, what solves the problem. Everything else is commentary.

That's when I realized I'd been doing this wrong. Not just slightly inefficient wrong, but fundamentally misaligned with how AI-assisted development actually works. I was using a documentation structure designed for 20-person enterprise teams when I was a solo developer with an AI assistant.

So I did what any frustrated engineer does: researched alternatives, tested different approaches, and rebuilt the whole thing from scratch.

## The Documentation Spiral

Here's what documenting a simple authentication feature looked like for me a few months ago (and still does at work, though we use Jira as the source of truth):

In `musthaves.md`, I'd write the full user story format: "As a user, I want to register with email and password so that I can create an account." Then list out all the requirements—email validation, password strength, secure hashing, password reset flow. Maybe 150 lines total.

Then in `epics/epic-authentication.md`, I'd repeat most of that information but with more technical detail. Epic goals, the same user stories again, technical requirements (JWT tokens, bcrypt, email service integration), acceptance criteria. Another 300 lines.

Finally, in `todo.md`, I'd extract the actual actionable tasks: implement registration, implement login, implement password reset, set up email service. Maybe 50 lines.

Total: roughly 500 lines of documentation for a feature I could describe in a single sentence.

The problems weren't immediately obvious. Documentation feels productive. You're planning, you're being thorough, you're following best practices. But after a few weeks, the cracks started showing:

When requirements changed, I had to update three places. When Claude Code asked about implementation details, I'd point it to the epic file. When I needed to see what was actually left to do, I'd check the todo list. But which one had the latest thinking? The cognitive overhead of "where does this information belong" started eating into actual development time.

More frustrating: none of this ceremony was helping Claude Code write better code. It didn't need user stories in the "As a... I want... so that..." format. It needed context—what we're building, why we're building it, what the constraints are, and what to do next.

## What AI Actually Needs

Traditional team documentation exists for a reason. You need detailed specs for handoffs between developers. You need user stories so product managers and engineers share understanding. You need comprehensive docs because people forget context between sprints.

AI assistants don't work like that.

Claude Code doesn't forget context between tasks—it never had context to begin with. Every session starts fresh. It reads whatever documentation you point it to, and it builds a mental model from that.

What it needs isn't instructions on *how* to build something. It's perfectly capable of figuring out implementation details. What it needs is *context*: What are we building? Why? What's the architecture? What decisions have we already made? What are we explicitly not doing?

And critically: what should I work on next?

That realization led me to research how other teams handle lightweight documentation. I looked at [MoSCoW prioritization](https://en.wikipedia.org/wiki/MoSCoW_method) (Must have, Should have, Could have, Won't have). I read through [Shape Up](https://basecamp.com/shapeup) from Basecamp with its 6-week cycles and appetite-based planning. I found [Getting Real](https://basecamp.com/gettingreal) from 37signals with its minimalist "build half a product, not a half-assed product" philosophy. I also read "Fast Solo Development" by T.O.M. Mannigel and "The DevOps Handbook" by Gene Kim, looking for patterns in how successful teams manage complexity.

The best approach to me seemed to be combining MoSCoW's dead-simple prioritization with lean documentation principles. MoSCoW asks one question: "Can we ship without this?" If no, it's a Must Have. If yes but it would hurt, it's a Should Have. That's it. No ceremony, no training needed, works for any project.

## Three Files

I reduced my entire documentation system to three files.

**project.md** holds the stable context. What we're building, why it matters, the technical stack, architecture overview, success metrics, and—critically—what's explicitly out of scope. Think of it as the README for your AI assistant. You write it once, update it rarely, and it provides the foundation for every interaction.

**todo.md** is the single source of truth for active work. Everything goes here: features, bugs, improvements, infrastructure work. It's organized by priority—Must Haves and Should Haves—and within each priority level, items are grouped by type. Each item is a checkbox. If it's blocked, you prefix it with `[BLOCKED]` and note why. If it depends on something else, you note that inline. Top to bottom roughly represents workflow order.

**done.md** preserves history. When work completes, you move it from todo.md to done.md with the completion date. But you don't just mark it done—you link back to the implementation plan if one existed, the Architecture Decision Record if you made significant choices, the pull request, and the impact. "Reduced registration time from 30 seconds to 3 seconds." This isn't busywork—it creates a learning resource so future AI sessions (and future humans) can see what approaches worked.

That authentication feature that took 500 lines across three files? Here's the new version:

```markdown
## Must Haves

### Features
- [ ] User authentication system
  - Registration with email/password
  - Login with session management (JWT)
  - Password reset via email
  - Password hashing with bcrypt
  - Email validation and strength requirements
```

Ten lines. One file.

## The Numbers

I tracked the difference across several features in my own projects:

Template files dropped from 7 to 3. In my experience, time to document a feature went from about 15 minutes to about 2 minutes. Lines of documentation per feature went from around 150 to around 10. Files that needed to stay synchronized dropped from 4-5 to just 2 (todo.md and done.md).

But the real improvement wasn't measurable in metrics. It was cognitive load.

Instead of five questions—Is this an epic or a feature? Do I need a user story? Where do I document this? Which file is source of truth? Should this be in the must-haves or the epic file?—there's one question: "Can we ship without this?"

That simplicity compounds. Add a checkbox, done. Move completed items to done.md with links when they're finished. No synchronization overhead, no document coordination, no ceremony.

## Why It Works

Claude Code only needs to read three files instead of five to seven. The structure is predictable—project.md for stable context, todo.md for active work, done.md for history. Dependencies are explicit where they matter, implicit (through ordering) where they don't.

More importantly, done.md becomes a learning resource. Claude Code can see what implementation approaches worked before, understand project velocity, and reference past architectural decisions because they're linked from completed work.

For humans, the benefits are equally tangible. No ceremony about user story format. No deciding "Is this an epic or a feature?" Single file (todo.md) shows all active work at once. Easy to scan, easy to reprioritize, easy to maintain.

## Edge Cases

Large projects might need split todo files if you're managing more than 50 active items. Multi-team projects might keep a single project.md for shared context but split todo.md by team. If you need epic-level grouping, just use sub-sections under Must Haves or Should Haves. Complex features can link to detailed implementation plans. Research tasks? Research is actionable work—treat it like any other checkbox.

The system flexes to accommodate different needs without requiring structural changes. Start simple, add complexity only when you actually need it.

## Integration

This three-file approach fits naturally into a complete development workflow. Research findings get saved to their own directory, referenced from relevant todo items. Complex features get implementation plans that are linked from the checkbox. Work progresses through todo.md Must Haves. When complete, items move to done.md with full traceability—links to plans, research, Architecture Decision Records, pull requests, and impact metrics.

In my [claude-config-template](https://github.com/albertsikkema/claude-config-template) project, the `/project` command generates all three files from templates based on a few targeted questions. The `/rationalize` command updates them as work completes, maintaining the links and context automatically.

## The Philosophy

This isn't about doing less documentation. It's about doing exactly enough.

MoSCoW Method provides simple prioritization that forces clarity. Getting Real's "build half a product, not a half-assed product" philosophy reminds us that less is often more. Lean documentation principles emphasize documenting with purpose—minimal viable documentation that actually gets used.

Combine those principles, and you get a system that gives AI assistants clear, simple, complete context without drowning developers in ceremony.

## Getting Started

If you're drowning in documentation overhead while working with AI assistants, try this:

Create project.md with essential context—what you're building, why, technical stack, architecture, what's out of scope. Move all active work to todo.md with Must Have and Should Have priorities. Start done.md for completed work with links back to plans and decisions.

The templates are available in [claude-config-template](https://github.com/albertsikkema/claude-config-template) if you want a starting point, but the structure is simple enough to create from scratch.

One file for context. One file for active work. One file for history. One question for prioritization: "Can we ship without this?"

## What Changed

After using this, especially working alone or in a small team, I can't imagine going back. The reduction in cognitive load alone makes it worthwhile. No more "where does this information belong" decisions. No more keeping multiple files synchronized. No more ceremony that adds documentation without adding clarity.

But the real magic? AI assistants become dramatically more effective when they have clear, simple, complete context. Claude Code doesn't waste time resolving contradictions between documents. It doesn't need to ask which file is authoritative. It knows exactly where to look for context, priorities, and history.

The three-file methodology delivers that. Nothing more complicated than it needs to be. Nothing less useful than it should be.

Exactly enough.

> Interesting how older methods are becoming relevant again. MoSCoW was developed in 1994. The [Parnas paper on faking rational design](https://users.ece.utexas.edu/~perry/education/SE-Intro/fakeit.pdf) was written in 1986. These simpler approaches from thirty to forty years ago may work better with AI assistants than the complex methodologies we built in between.

> Or as [grugbrain.dev](https://grugbrain.dev/) would put it: "complexity very, very bad."

## Food for Thought

One last observation: if you're following the [Parnas approach of faking a rational design process](/ai/development/documentation/llm/2025/10/10/faking-rational-design-ai-era.html), you might not even need done.md. The whole point of that philosophy is to present the rationalized version, not the chronological discovery process. Your code is the implementation. Your ADRs capture the rationalized decisions—what you chose and why, presented as if you knew it all along. Why maintain a historical record of completed checkboxes when the ADRs already tell the clean story?

That would simplify to just two files: project.md for context, todo.md for active work (delete items when done), plus ADRs for significant decisions. Even leaner. Something to consider.

---

*What documentation approaches have you found that work well with AI? What's helped or hurt your workflow? I'd love to hear about it—connect with me on [LinkedIn](https://www.linkedin.com/in/albert-sikkema/).*
