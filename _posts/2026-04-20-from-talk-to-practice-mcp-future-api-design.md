---
layout: post
title: "What MCP's Future Means for API Design"
date: 2026-04-20
categories: ai development mcp
description: "Watching a talk on MCP's future, I realized I already built the pattern they are formalizing. And it raises a bigger question about how we design APIs."
keywords: "MCP, Model Context Protocol, API design, REST API, skills over MCP, progressive discovery, agent connectivity, David Soria Parra, logbench"
image: /assets/images/from-talk-to-practice-mcp-future-api-design-blog.png
---

<figure>
  <img src="/assets/images/mcp-future-api-design.jpg" alt="Misty Scottish highland landscape with winding path through moorland">
  <figcaption>Photo by <a href="https://unsplash.com/@martinbennie">Martin Bennie</a> on <a href="https://unsplash.com">Unsplash</a></figcaption>
</figure>

This weekend I built a small CLI tool that pulls transcripts, comments, and metadata from YouTube videos. The first thing I fed it was David Soria Parra's keynote ["The Future of MCP"](https://www.youtube.com/watch?v=v3Fr2JR47KA) at the AI Engineer conference. David wrote the original Python MCP SDK at Anthropic, so he knows where the protocol is heading. I dove into MCP about 9 months ago as part of the exploratory phase of a government job, a lot has happened since, and there is a lot on the roadmap. I discussed it with an LLM, asking about REST's role, about playbooks that instruct models how to compose tools, and about the similarities with what I have been building.

## What David Laid Out

The short version: 2025 was about coding agents (local, sandboxed, verifiable). 2026 is about general knowledge workers who need connectivity to five SaaS apps and a shared drive, not a local compiler. He sees three layers for this: skills (domain knowledge in files), [MCP](https://modelcontextprotocol.io/) (rich semantics, auth, governance, long-running tasks), and CLI/computer use (great when the tool is already in pre-training data like git or gh). The best agents will use all three.

Three things he wants the ecosystem to fix: **progressive discovery** (stop dumping all tools into context, load them on demand), **programmatic tool calling** (give the model an execution environment to compose multiple calls in one script instead of round-tripping one by one, like [Cloudflare's Code Mode](https://blog.cloudflare.com/code-mode-mcp/) does), and **designing for agents, not REST** (stop mapping REST endpoints 1:1 into MCP servers, he called conversion tools "cringe").

The upcoming features add a lot, but the new feature I care about most is skills over MCP: servers shipping domain knowledge alongside their tools. More on that below. The protocol is barely 18 months old, with 110 million monthly downloads (roughly 2x faster than React hit that number), so that is proving how popular it is.

## I Already Built This

The part that clicked with me was "skills over MCP." David described it as an upcoming protocol primitive: servers should ship playbooks alongside their tools, instructing the model how to combine them for specific tasks. The server author maintains the playbooks, not the user. When workflows change, the server updates its skills and every connected agent gets the new instructions automatically.

I have been doing exactly this in [logbench](/ai/development/operations/2026/04/16/when-llms-actually-deliver.html), the MCP server I built for querying our Axiom logs. Tools like `explore_dataset` don't return raw data. They return step-by-step instructions: "first get the schema, then run an error breakdown, then drill into the top categories." The model picks the right workflow tool, gets the recipe, follows it. (Not entirely my idea, did something similar a long time ago, but this step was inspired by Axiom's official mcp code)

It works well. No context bloat because the playbook only loads when the model calls that specific tool. Progressive discovery is built in for free. And the instructions are scoped to the task at hand, not a generic "here are all the things you could do."

## Skills Over MCP: The Distribution Angle

Before I get to why formalization worries me, there is one part of skills over MCP that is genuinely exciting: distribution.

Right now, if I want my colleagues to use the logbench playbooks, they need my exact MCP server setup. If I want to share a highly specialized tool behind an auth wall or a paywall, there is no standard way to do that. Skills over MCP solves this. Your team connects to the same MCP server and everyone gets the same playbooks, updated by the server author, no local configuration needed. A specialized log analysis skill, a compliance checking workflow, a financial reporting recipe: all distributed through the same protocol, access controlled at the server level.

That is a real improvement over "copy this markdown file into your project." It means you can build tools that are genuinely sharable across teams, organizations, even commercially. The distribution story is strong.

## The Boring Toolset Problem

But here is where I am less enthusiastic. What I see happening with MCP is the same thing that happens to every successful protocol: it moves from "wow, that is cool" to the inevitable boring enterprise toolset, the same kind of [standardization convergence](/ai/development/2026/02/13/let-the-ai-pick-react.html) I wrote about with React. Mediocre-good-for-all, mostly optimized for large organizations with compliance requirements, not for developers who want to push boundaries.

My concern is not that the formalization itself will limit what I can do. It probably will not. My concern is what happens to developers along the way. When I built the playbook pattern in logbench, I understood exactly what was happening: a tool returns instructions, the model follows them. I learned how to engage with the model, how to structure instructions it would follow reliably, what worked and what did not. That understanding came from building it myself, from prodding and experimenting. Once that becomes a protocol primitive you just consume, the experimentation stops. You get a standard way to do it, and most developers will never look underneath.

That is how we lose the skill of working with LLMs directly. Not because the abstractions are bad, but because they are comfortable. People stop experimenting with how to instruct models, how to structure tool interactions, how to design playbooks that actually work. They use the MCP skills primitive because it is there, and they never discover new patterns that only emerge when you build from scratch.

MCP itself is open source now (Anthropic [donated it to the Linux Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) as part of the Agentic AI Foundation), which is good. But the ecosystem it lives inside is moving in a direction I like less. Claude Code started as a developer-focused tool, the kind of thing where you could [wire up your own workflows](/AI/development/productivity/python/2026/01/13/rethinking-claude-flow-from-per-repo-chaos-to-global-app.html) and push the boundaries. Increasingly it is becoming a fits-all product, and the pricing reflects that. The whole Claude Code environment is powerful, but it is also an ecosystem that wants you to stay inside it.

Which is why I think it is worth looking at what exists outside. [Pi](https://www.pi.dev/) is one framework worth trying for agentic use, approaching connectivity differently from MCP. There are more options than the one path Anthropic is paving, and the best time to explore them is now, while the patterns are still forming and nothing is locked in.

## What Happens to REST?

This is the question I kept coming back to. As more and more interaction moves through agents, and agents interact through MCP, what happens to the classic API?

REST is not going anywhere as plumbing. You cannot have MCP without REST (or something like it) underneath. The comments on the talk pushed back hard on this point, and they are right: MCP is essentially "discoverable REST," and the move toward stateless transport is literally re-converging toward REST patterns.

But I wonder about the trajectory: right now we have API-centered systems and we are moving toward API + MCP. Will that become MCP-centered? Eventually MCP-only for some use cases? And if so, what happens to the APIs that remain?

I think they change character, the classic REST API is a developer's tool: full CRUD, every resource exposed, every operation available, everything must be in there. The MCP model is different: only those operations that add value, combined into higher-level actions when that makes sense. Less "here are all the building blocks" and more "here is what you can actually do."

That is not a developer-centered design: it is a human-centered design, or an LLM-centered design, which turn out to be surprisingly similar. And if agents become the primary consumers of APIs, the APIs that stick around will probably start looking more like MCP tools than like the CRUD interfaces we build today. Fewer granular endpoints, more intent-oriented operations. Domain knowledge shipped alongside the API, not buried in documentation.

Or put differently: if your API is so granular that you need a playbook to use it, perhaps the API itself should be the playbook.

## What I Took Away

Watch the [full talk](https://www.youtube.com/watch?v=v3Fr2JR47KA) if you work with MCP or build agent tooling. It is 18 minutes and dense with where the protocol is heading.

My takeaways, for what they are worth:

- The playbook-as-a-tool pattern works today, no protocol extension needed. If you are building MCP servers, try it before waiting for the formalized version.
- Progressive discovery is not optional at scale. If you dump 50 tools into the context window, you are doing it wrong.
- MCP is a good protocol, but keep building things yourself too. The understanding you get from direct experimentation with LLMs is worth more than any abstraction.
- Look beyond Anthropic's ecosystem. Try [Pi](https://www.pi.dev/), try building without MCP, see what works. The best patterns come from exploration, not from consuming frameworks.
- As agents become primary data consumers, the APIs themselves will loose importance and start looking more like MCP tools: fewer CRUD endpoints, more intent-oriented operations.

---

*Building MCP servers or thinking about API design for agents? <a href="#" onclick="task1(); return false;">Get in touch</a> to compare notes.*

## Resources

- [The Future of MCP -- David Soria Parra keynote](https://www.youtube.com/watch?v=v3Fr2JR47KA) at AI Engineer conference
- [Model Context Protocol specification](https://modelcontextprotocol.io/) -- the official MCP spec and documentation
- [FastMCP](https://github.com/jlowin/fastmcp) -- the Python SDK David called "way better" than the official one
- [Cloudflare MCP server](https://github.com/cloudflare/mcp) and their [Code Mode blog post](https://blog.cloudflare.com/code-mode-mcp/) -- example of exposing an execution environment instead of individual tools
- [Agentic AI Foundation announcement](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) -- Anthropic donating MCP to the Linux Foundation
- [David Soria Parra on GitHub](https://github.com/dsp)
- [When LLMs Actually Deliver](/ai/development/operations/2026/04/16/when-llms-actually-deliver.html) -- my earlier post on logbench and the playbook pattern
