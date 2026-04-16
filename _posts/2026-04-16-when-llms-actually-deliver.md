---
layout: post
title: "When LLMs Actually Deliver"
date: 2026-04-16
categories: ai development operations
description: "LLMs can be brilliant and stupid within two turns. But give them the right tools and a playbook, and the results are something that was not possible two years ago."
keywords: "LLM productivity, MCP server, log analysis, Claude Code, AI operations, production debugging, logbench, developer tooling"
image: /assets/images/when-llms-actually-deliver-blog.png
---

<figure>
  <img src="/assets/images/when-llms-actually-deliver-blog.jpg" alt="Vintage industrial control room with rows of analog gauges, dials, and switches on a marble panel" width="1920" height="1280" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>Many signals, one panel. Photo by <a href="https://unsplash.com/@modry_dinosaurus">Frantisek Duris</a> on <a href="https://unsplash.com/photos/C3DfIgig1j8">Unsplash</a>.</figcaption>
</figure>

I have a love/hate relationship with LLMs (mostly love, but every now and then I get frustrated).

One moment they nail a complex refactor across six files. The next they confidently introduce a bug that any starting developer would (probably) catch, or hallucinate an API that has never existed. The swing between brilliant and stupid can happen within two turns of the same conversation. Every time you start to trust, even a little, that trust is crushed to bits.

But every now and then something happens that makes you stop and think: *this changes things*. (especially if you suddenly realise how complex and time-consuming some tasks were before)

## One Sentence, Thirty Seconds

This morning I opened Claude Code and typed one sentence:

> Please check the logs for production of <redacted repo name> over the last 24 hours. Then check the PRs made to see if the uploaded changes in the last 3 days have made a difference.

Thirty seconds later I had:

- A full breakdown of all log events with error rates per hour
- Error classification by type, with counts and affected tenants
- A correlation table showing how each merged PR impacted specific error categories
- A before/after comparison: 'clarifyinput' errors dropped from 29 to 2, OpenAI errors from 43 to zero
- An explanation of why icon errors *went up* (improved logging granularity, not a regression)
- Three concrete action items with root causes identified

Really helpful: the LLM didn't just count errors -- it 'understood' that PR #458 changed the logging format from a generic "fetching" message to per-icon "loading" messages, and correctly concluded that the apparent spike in icon errors was an artifact of better observability, not a regression. That kind of contextual reasoning across log data and code changes used to take me an hour of cross-referencing. On a bad day, longer. 

Before this, checking whether a deploy improved things looked something like:

1. Open the logging dashboard, set the time range, filter by severity
2. Stare at graphs, try to spot patterns
3. Open GitHub, find PRs merged in the relevant window
4. For each PR, read the diff and figure out which error messages it should have affected
5. Go back to the logging dashboard, write queries for those specific error messages
6. Compare before/after time windows
7. Write it all up in your head or in a document
8. Repeat for each PR

If you had proper dashboards and saved queries this was maybe an hour. Without them, half a day. And you had to know what to look for in advance -- if a PR had an unexpected side effect, you might miss it entirely.

Apart from the time it took, also the mental drain to check the logs: it takes time and energy but does not create a solution. It is not even about getting to know the scope or the cause of the problem, the energy is consumed by using tools itself, forcing you to spend mental energy on using the tools to actually see if there IS a problem. And now that energy can be put towards seeing the problem and moving on to what we get paid for: thinking about how to solve the problem.

All I had to do is decide if I agree with its conclusions (about 60% of the time I do), and decide how to tackle the issues.

## The Playbook Is Everything

The LLM did not do this on its own, left to its own with this instruction it would not have access to the logs and the repo so it could not do anything at all. Even when it has API access to the logs and would have connected to the repo, results would be not as good as this. The model would have fumbled with authentication, guessed at query syntax, missed fields, and produced a surface-level summary that looks impressive but tells you nothing you didn't already know. And it would not remember next time how it should query to get to a certain result.

What made this work is that I built the tools and the playbook first. (Logbench is one of several tools I built for this; another is [gtk](/ai/development/tools/2026/04/09/gtk-cutting-llm-token-costs-cli-output.html), which filters CLI output to save tokens.)

**Logbench** is a small MCP server I wrote in Go. It connects to our Axiom log platform and exposes a handful of tools: `query_apl` for running raw queries, `explore_dataset` and `error_breakdown` for guided analysis, `get_dataset_schema` so the LLM knows what fields exist. Nothing fancy. But each tool has a clear contract: here is what you pass in, here is what you get back. (why not the [official Axiom MCP server](https://github.com/axiomhq/mcp)? We are on a separate version (eu) and the official server does not work with that. I did take inspiration from their code though.) Besides I added some extra steps to find certain information that is unique to this implementation.

The key is the **prompted workflows**. Logbench doesn't just expose raw query access. It includes structured playbooks: "when investigating errors, first get the schema, then run an error breakdown, then drill into the top categories." The LLM follows the playbook instead of improvising.

So the LLM is not being creative here. It is following a recipe for how to query the logs for certain often needed results. And then the starting prompt turns into a logical order:

1. Get the dataset schema (know your fields)
2. Run aggregate queries (get the big picture)
3. Break down errors by message (find the categories)
4. Get recent PRs from GitHub (know what changed)
5. Run time-windowed queries per error category (measure impact)
6. Cross-reference and synthesize (connect the dots)

Each step is a tool call with predictable input and output. The LLM's job is to orchestrate the steps, handle errors (like when a field name is wrong -- it recovered and tried bracket notation), and synthesize the results into something a human can act on. (This is the same orchestration principle I described in [automating Claude Code workflows](/ai/llm/development/productivity/2025/11/21/orchestrator-automating-claude-code-workflows.html), but applied to log analysis instead of code.)

## The IFs

This only works:

**IF** you give them the right tools. Not raw access to everything, but curated tools with clear interfaces.

**IF** you give them a playbook. Not "figure it out" but "here are the steps, follow them."

**IF** the tools handle the hard parts. Authentication, query syntax, field validation, error formatting -- all of that lives in the MCP server, not in the prompt.

Without those guardrails the same model will confidently query a field that doesn't exist, and present wrong conclusions with the same authoritative tone. (I wrote about [building these kinds of guardrails](/ai/development/best-practices/2026/03/31/evidence-based-best-practices-ai-guardrails.html) in more detail previously.) Because that is what I observed starting out during development, before the playbooks and extensive query examples were in place.

## The Pattern

Sometimes LLMs are truly brilliant and come up with solutions that are elegant and useful. Most of the time they do not. Apart from those moments of brilliance, every time I have seen an LLM deliver useful results this was because of:

1. **Structured tools** with clear inputs and outputs
2. **Guided workflows** that tell the model what steps to follow
3. **Domain knowledge baked into the tools**
4. **The LLM as orchestrator and synthesizer**, not as domain expert

That is a fundamentally different use case than "write me a function" or "refactor this class." It is closer to having a junior analyst who can follow a checklist very fast and write a surprisingly good summary. You still need to build the checklist and the tools. 

## Love/Hate, But Mostly Love Today

I will go back to being mad and amazed at hallucinated facts and stupid ideas and authoritative tone tomorrow. The love/hate cycle continues. But moments like today are a reminder that the frustrating parts are worth pushing through, because when it clicks -- when the tools are right and the playbook is clear -- the result is something that was not possible two years ago.

Not because the AI is intelligent in itself, but because the system around it is. (which with some philosophical reflection is not far from how we humans function). Have a nice day!

---

*Logbench is not public -- it is custom built for internal use. Interested in building something similar? <a href="#" onclick="task1(); return false;">Get in touch</a>.*
