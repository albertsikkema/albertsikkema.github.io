---
layout: post
title: "The Orchestrator: Automating Full Claude Code Workflows"
date: 2025-11-21
categories: AI LLM development productivity
description: "Automate complete AI-assisted development workflows with an orchestrator that chains Claude Code commands. Learn how to build production-ready AI agent orchestration systems."
keywords: "AI agent orchestration, Claude Code automation, AI workflow automation, AI-assisted development, Claude AI integration, production-ready AI"
---

I've been using my [claude-config-template](https://github.com/albertsikkema/claude-config-template) for several months now, and one friction point kept bothering me: manually running slash commands in sequence. Research, plan, implement, review - it's the right workflow, but it's tedious when you know exactly what needs to happen. So I built an orchestrator.

## Why Now?

I knew this kind of automation was possible from the start, but I deliberately waited. The underlying tools - the slash commands, the agents, the workflows - needed to prove themselves first. After give or take six months of daily use, testing edge cases, fixing bugs, and refining prompts, I trust them enough to let them run without supervision.

Are they perfect? Far from it. But they're reliable enough for routine tasks. And that's the threshold for automation: not perfection, but predictable behavior. When I know what the tools will do in common scenarios, I can confidently chain them together.

<figure>
  <img src="/assets/images/orchestrator1.webp" alt="Orchestrator automating Claude Code workflow">
  <figcaption>This is what AI thinks an image for this blog should look like...</figcaption>
</figure>

## The Problem with Manual Orchestration

If you've read my [previous post about the config template](/ai/tools/productivity/2025/10/14/supercharge-claude-code-with-custom-configuration.html), you know I use a structured workflow: research the codebase, create a plan, implement it, then review. This pattern works well, but it requires babysitting. Each slash command might ask questions. You need to wait for completion. Copy file paths between steps.

For routine tasks - adding a feature you've spec'd out, fixing a well-understood bug - this manual coordination adds unnecessary overhead. What I wanted was to say "do this task" and come back to reviewed code.

## The Nesting Problem

Here's the challenge: Claude Code already has subagents. So why not just create an orchestrator agent that spawns other agents? Because of a fundamental limitation in Claude's architecture: **subagents cannot spawn other subagents**.

This is probably by design, to limit resource usage. But it means you can't build a meta-agent in Claude that coordinates other agents which might themselves need to spawn agents. The codebase-researcher agent, for instance, uses multiple specialized subagents internally. An orchestrator built as a Claude agent couldn't call it without breaking the nesting rule.

The solution? Use an external LLM as the orchestrator. It doesn't live inside Claude's context, so it can spawn Claude Code instances without violating any nesting constraints.

## How It Works

The orchestrator (`claude-helpers/orchestrator.py`) is a Python script that chains Claude Code slash commands together:

```bash
uv run claude-helpers/orchestrator.py "Add user authentication with JWT tokens"
```

This kicks off five sequential operations:

1. **`/index_codebase`** - Map out the project structure
2. **`/research_codebase`** - Investigate existing patterns and relevant code
3. **`/create_plan`** - Generate an implementation plan
4. **`/implement_plan`** - Execute the plan
5. **`/code_reviewer`** - Review the changes

Each step feeds into the next. The orchestrator extracts file paths from Claude's output and passes them as context to subsequent commands. When Claude asks questions (which it does, especially during planning), the orchestrator uses OpenAI's API to generate appropriate responses.

## Why OpenAI?

You might wonder why not use Claude for the orchestration decisions too. Two reasons:

1. **No nesting constraint** - OpenAI doesn't have the same architectural limitation, so it can coordinate without restrictions
2. **Different strengths** - The orchestrator needs to parse Claude's output and make quick decisions about how to respond. It doesn't need Claude's deep reasoning or large context window

The orchestrator supports both OpenAI and Azure OpenAI. It reads configuration from `.env.claude` and auto-detects which service to use based on which environment variables are set.

## Practical Usage

For a straightforward feature:

```bash
uv run claude-helpers/orchestrator.py "Add rate limiting to the API endpoints"
```

For exploratory work where you want to review the plan before committing:

```bash
uv run claude-helpers/orchestrator.py --no-implement "Redesign the caching layer"
```

For CI/CD integration:

```bash
uv run claude-helpers/orchestrator.py --json "Fix the failing payment tests" > result.json
```

The `--json` flag structures the output for parsing. The `--no-implement` flag stops after the planning phase - useful when you want human review before the LLM touches code.

## Implementation Details

The script is built with `uv` for dependency management. First run automatically installs dependencies - no setup required. It uses subprocess to spawn Claude Code instances and streams output in real-time to stderr, so you see progress as it happens.

One design choice: the orchestrator is intentionally simple. It doesn't try to be clever about which steps to skip or how to parallelize. It runs the full workflow every time. Why? Because the overhead of making smart decisions often exceeds the cost of just doing the work. And consistency matters - I always want research before planning, always want review after implementation.

## When Not to Use It

The orchestrator is for routine tasks where the workflow is predictable. For exploratory work, complex debugging, or tasks requiring back-and-forth discussion, you still want to run commands manually. The human in the loop isn't just about reviewing output - it's about steering the process when things get complicated.

Also, be aware of cost. Running five Claude Code commands per task adds up. For small fixes, it's probably overkill. For substantial features where you'd run those commands anyway, it saves time without changing cost much.

## What's Next

The main question now is reliability. How often does the orchestrator produce usable results without intervention? I need to track this systematically - not just "it works" but failure modes, edge cases, and where human review catches issues the automation missed.

The code review step is particularly interesting. As I wrote in my [previous post about human-in-the-loop review](/ai/llm/development/best-practices/2025/11/14/human-in-the-loop-ai-code-review.html), LLM-generated reviews miss certain classes of problems - especially meta-level issues like tests that test whether tests exist. A colleague spotted that instantly; multiple LLM passes missed it entirely. So how do I make the automated review more effective? Different prompting? Multiple review passes with different perspectives?

I'm hesitant to add complexity before understanding the baseline. The value is in automation, not optimization. A simple tool that runs reliably beats a complex one that sometimes does the wrong thing.

## Try It Out

The orchestrator is included in the latest version of [claude-config-template](https://github.com/albertsikkema/claude-config-template). After installation:

```bash
# Make sure you have uv installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up your OpenAI (or Azure OpenAI) credentials in .env.claude
echo "OPENAI_API_KEY=your-key" >> .env.claude

# Run it
uv run claude-helpers/orchestrator.py "Your task description"
```

The pattern of research→plan→implement→review has served me well. Now it runs without me having to shepherd each step. That's the kind of automation that actually helps.

## Resources

- [Claude Code Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents) - Official docs on subagent capabilities and limitations
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Anthropic's engineering guide
- [claude-config-template](https://github.com/albertsikkema/claude-config-template) - The full configuration system
- [OpenAI Cookbook](https://cookbook.openai.com/) - Examples and guides for building with OpenAI
- [PydanticAI](https://ai.pydantic.dev/) - Agent framework for building production-ready AI applications

---

*Are you automating your AI-assisted workflows? What patterns have you found useful? I'd love to hear about your experiences—<a href="#" onclick="task1(); return false;">get in touch</a>.*
