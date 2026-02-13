---
layout: post
title: "Let the AI Pick React"
date: 2026-02-13
categories: ai development
description: "The AI-React reinforcement loop is creating a monoculture. That might be exactly what frontend development needs."
keywords: "react, AI development, vibe coding, frontend frameworks, monoculture, svelte, standardisation, LLM coding"
image: /assets/images/ai-react-convergence.jpg
---

<figure>
  <img src="/assets/images/ai-react-convergence.jpg" alt="Aerial view of highway lanes converging into a single interchange, representing framework standardisation">
  <figcaption>Photo by <a href="https://unsplash.com/@dnevozhai">Denys Nevozhai</a> on <a href="https://unsplash.com">Unsplash</a></figcaption>
</figure>

There is a self-reinforcing cycle forming in frontend development, and it is making people nervous.

React has the most code in LLM training data. LLMs therefore [generate better React code](https://www.200oksolutions.com/blog/github-copilot-vs-chatgpt-vs-claude-frontend/) than anything else. More React code gets written — by both humans and AI — feeding future training data. Repeat. The flywheel spins, and React's dominance compounds with every prompt.

The evidence is hard to miss: give an LLM a vague prompt like "build me a web app" and you will almost invariably get React + Tailwind + shadcn/ui. Tools like [v0](https://v0.dev), [Lovable](https://lovable.dev), and [Bolt.new](https://bolt.new) all default to this stack. v0 technically supports Vue and Svelte, but by Vercel's own admission it "really works best using React, Tailwind and shadcn/ui."

The usual reaction to this is concern. It is called [the problem with the default AI stack](https://maximilian-schwarzmueller.com/articles/the-problem-with-the-default-ai-stack/). Others [warn about](https://logicloop.dev/frontend-frameworks/ai-creating-developer-monoculture-frontend-framework-diversity/) stifled innovation, outdated patterns being perpetuated at scale, and a knowledge barrier for newcomers who never discover alternatives because the AI never suggests them.

I see it differently.

## The Fragmentation Problem Nobody Talks About

Frontend development has been drowning in choice for a long time. React, Next, Vue, Svelte, Solid, Angular, Qwik, Astro, Lit, Preact, Marko, Alpine, Htmx — and many more, and that is just frameworks. Each comes with its own ecosystem of state management libraries, routing solutions, meta-frameworks, and component libraries. Every combination produces a slightly different mental model, a different set of conventions, a different way to do the same thing.

This fragmentation has real costs. Teams spend weeks evaluating frameworks. Developers switching jobs need ramp-up time to learn the local flavour. Hiring becomes framework-specific. Knowledge sharing across projects is harder than it should be. The industry has been paying a quiet tax on all this optionality, and for what? For 95% of use cases, any of these frameworks would do the job just fine.

What AI is doing — accidentally, through the cold logic of training data statistics — is pushing the community toward standardisation. And standardisation, when the standard is good enough, is not a loss. It is a relief.

## Good Enough Wins

React is not the best framework. I will say that plainly. If I had to write code by hand — really sit down and build components line by line — I would pick Svelte. It is cleaner, less verbose, and gives me a better overview of what is happening. The developer experience is genuinely superior when you are the one typing.

But I am not the one typing.

I wrote about this shift in my post on [vibe coding, product quality and democratisation](/2026/02/05/vibe-coding-quality-democratisation.html): the value equation has changed. When AI generates 80-90% of the code, my personal preference for a framework's syntax becomes almost irrelevant. What matters is whether the AI can produce correct, functional code — and right now, it produces better React code than anything else. That is not ideology. It is a measurable quality gap rooted in training data volume.

React is not the best. But it is good enough for the vast majority of what gets built. And "good enough + excellent AI support" beats "technically superior + mediocre AI support" in every practical scenario I can think of.

I learned this first-hand when I was using a new Svelte version with GitHub Copilot — a long time ago it seems — when the training data had not included that version yet. Not a fun experience, having to reinstruct the LLM every time.

## The Time Argument

Every hour I do not spend fighting an AI tool's weaker output in a less-supported framework is an hour I can spend on what actually matters: the product, the user experience, the business logic, the security model.

The cost savings are real. When Lovable or Claude Code can scaffold a working application in half an hour using React, the overhead of choosing a different framework — debugging AI-generated code that is slightly off, filling in gaps where training data is thin, manually correcting patterns the model has not seen enough of — becomes a luxury most projects cannot justify.

This is the argument that makes the monoculture concerns less relevant for most teams: time saved is money saved. And time is the [final currency](https://www.youtube.com/watch?v=AR9hMvlOZCo).

## When I Would Not Do This

I am not saying React is the answer to everything. There are clear cases where another approach is justified:

**Security-critical applications.** When a project demands the highest level of security assurance, I want to understand every line of code. AI-generated code — in any framework — adds a layer of uncertainty that might be unacceptable. In those cases, the framework choice should serve the security model, not the AI tooling.

**Performance as a hard requirement.** If a client needs the absolute smallest bundle size or the fastest possible rendering, Svelte or Solid or plain Javascript will outperform React. When performance is a specification, not a nice-to-have, the technical choice should win over the AI convenience.

**Simplicity as a constraint.** Some projects need to be small, understandable, and maintainable by non-specialists. A simple static site does not need React's complexity. The right tool here might be vanilla Javascript, Alpine, or something deliberately minimal.

These are the 5% cases. They exist, they matter, and they require deliberate technical choices. But they are the exception, not the rule.

## What About Innovation?

The strongest counterargument is that a React monoculture stifles innovation. If future LLMs are trained mostly on React, the reasoning goes, new frameworks will never gain enough traction to compete.

Here is how I see it: we have not actually seen real innovation in frontend frameworks for a long time. Frontend is complicated — genuinely, deeply complicated. And so far, none of the alternatives have found a definitive answer. They are variations. [Svelte's](https://svelte.dev/) compile step, [Solid's](https://www.solidjs.com/) fine-grained reactivity, [Astro's](https://astro.build/) island architecture — these are smart ideas, well-built tools, and genuine improvements in specific areas. But they are also steps back in others. They are not the next paradigm shift. They are refinements.

Meanwhile, the industry runs on a multi-year cycle that keeps repackaging older ideas under new names. Server-side rendering [is back](https://daily.dev/blog/server-side-rendering-renaissance). Signals — [called observables in Knockout.js back in 2010](https://www.builder.io/blog/history-of-reactivity) — are back. The pendulum swings, and we call it progress.

A lot of developers see their framework of choice as real innovation. I understand that attachment — I feel it with Svelte. But in the grander scheme, these are variations on the same fundamental approach to building UIs. If something truly new comes along — something that genuinely changes how we think about frontend development — it will break through regardless of what LLMs default to. That kind of innovation does not need training data momentum. It needs to be undeniably better.

Until that happens, we are better off accepting what we have and building with it.

## The Accidental Standard

React did not plan this advantage. No committee decided it should be the AI default. It happened because React was the most popular framework when the training data was collected — a decade of documentation, tutorials, Stack Overflow answers, and open-source projects.

But planned or not, it gives developers a common language. It gives teams a safe default. It gives non-developers building their first app through vibe coding a foundation that actually works. And it gives the rest of us more time to spend on what we are actually building instead of debating what to build it with.

React apparently is not that bad.

## Resources

- [The Problem with the Default AI Stack](https://maximilian-schwarzmueller.com/articles/the-problem-with-the-default-ai-stack/) — Maximilian Schwarzmüller
- [Is AI Creating a Developer Monoculture in Frontend Framework Diversity?](https://logicloop.dev/frontend-frameworks/ai-creating-developer-monoculture-frontend-framework-diversity/) — LogicLoop
- [GitHub Copilot vs ChatGPT vs Claude for Frontend Development](https://www.200oksolutions.com/blog/github-copilot-vs-chatgpt-vs-claude-frontend/) — 200ok Solutions
- [Best Vibe Coding Tools](https://www.techradar.com/pro/best-vibe-coding-tools) — TechRadar
- [Is React Still the Best Choice in 2025?](https://thealphaspot.com/articles/is-react-still-the-best-choice-in-2025/) — The Alpha Spot
- [Svelte 5 and the Future of Frameworks: A Chat with Rich Harris](https://www.smashingmagazine.com/2025/01/svelte-5-future-frameworks-chat-rich-harris/) — Smashing Magazine
- [DHH on AI, Vibe Coding, and the Future of Programming](https://thenewstack.io/dhh-on-ai-vibe-coding-and-the-future-of-programming/) — The New Stack

## Further Reading

- [Vibe Coding: Product Quality and Democratisation](/2026/02/05/vibe-coding-quality-democratisation.html) — my earlier post on vibe coding and when personal tools become products
- [Securing YOLO Mode: How I Stop Claude Code from Nuking My System](/2026/02/01/securing-claude-code-hooks.html) — on guardrails for AI-assisted development
