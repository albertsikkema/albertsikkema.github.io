---
layout: post
title: "Fully Automated LLM Builds: Where It Actually Stops"
date: 2026-04-17
categories: ai development automation
description: "Automated LLM-driven builds mostly work. What stops you at scale: costs, reviewer/developer fatigue, and models that are not intelligent enough."
keywords: "automated builds, LLM code review, Claude Opus 4.6, local LLM, Qwen3 Coder, Gemma, developer fatigue, token cost, AI code automation"
image: /assets/images/automated-builds-cost-fatigue-ceiling-blog.png
---

<figure>
  <img src="/assets/images/automated-builds-machinery.jpg" alt="Close-up of industrial machinery with interlocking gears, chains, belts, and pulleys" width="1920" height="1280" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>A lot of moving parts that have to mesh. Photo by <a href="https://unsplash.com/@kiwihug">Kiwihug</a> on <a href="https://unsplash.com/photos/Hld-BtdRdPU">Unsplash</a>.</figcaption>
</figure>

For the last year or so I have been automating my software build workflow, handing more and more of the actual development work over to LLMs and watching where it breaks. The builds mostly run themselves now with good quality code, good enough that I can hand off that work and check back an hour later on the progress (or react to the Telegram message telling me a PR is waiting). 

This is the point I was aiming for when I started iterating on automated LLM-driven development a year ago. There were quite a few steps in between with different levels of automation, tools, start all over again, improve etcetera.

## What I Found to Be Bottlenecks

Three things I suspected but could only experience and prove by running the loop:

**You cannot skip the human review.** Left alone long enough the agent will drift. Possibly not in the first couple of PRs. But somewhere between 5 and 10 it will make a decision that looks locally correct and is globally wrong, and every PR after that builds on the drift. No amount of prompt engineering fixes this (and I tried a lot of methods). I wrote about the [same pattern with meta-tests](/ai/llm/development/best-practices/2025/11/14/human-in-the-loop-ai-code-review.html) last November and it is still true, just with a bigger blast radius now that the loop is tighter.

**Work item size matters.** Too small and you burn tokens spinning up six agents to change a button color. Too large and the model cannot hold the whole thing in its usable context and produces something that seems plausible or it does not get anywhere at all (one word of advice: set up a max number of turns, some processes can go on for hours not actually doing anything apart from a logical loop). The trap is assuming "size" maps to the human version of the word. It does not. Eight hours of copy-paste work is boring, not complex, and the LLM will do it in seconds. A 15-minute architectural decision can be too much for the model because it needs judgment the model does not have. The right granularity for an agent queue is not a human time estimate, it is "how much context and judgment does this require," and you have to learn that shape by running the loop and watching where it breaks. Getting the backlog granularity right is now a separate skill. And automating that part is the challenge: I start to reach the conclusion that with the current models this is not possible. And perhaps we can even say that with LLMs as we know it, this will highly likely never be possible (not until we get different kinds of intelligence). So there is the human role again.

**Reviewing LLM code all day is boring.** This one is mostly about me, but I do not think I am alone. When you do not write the code yourself, the mental connection is gone. I have to search for everything. When I wrote (parts of) the codebase myself, I knew my way (that data model contains this, we have a helper function for that, etc). You are reading prose somebody else wrote in a codebase you do not actually know by heart, with the added complication that the entity (in the broadest sense) that wrote the code does not actually learn from your feedback across sessions (you can use memories to persist, but that is not learning). After a few hours your attention drops and you start approving things you would not have approved in the morning. And the idea that the future holds endless PR reviews every day for the rest of my life is not really motivating, especially since code will be produced so fast that the pipeline will always be full and waiting for you. 

## The Review-Triage-Fix Loop

The first two problems I can partly engineer around. The third one I can only manage.

What I experimented with, and works better than anything else I tried, is a review loop with three stages before a human sees it:

1. A **very critical review**, with explicit checklists, run by a strong model. Not "looks fine" but "hunt for everything." Complete, pedantic, slightly paranoid. Use multiple agents all focused on certain angles to look at the codebase.
2. A **triage** pass over the findings. What actually needs to be fixed now? What goes on the backlog? What is wrong but not wrong enough to matter? 
3. A **fix** pass on the must-fix items and fix them automatically.

<figure>
  <img src="/assets/images/automated-builds-dashboard.jpg" alt="Project Server jobs dashboard showing a succeeded build with Setup, Build, Review, Triage and Fix stages ticked off">
  <figcaption>One run of the loop: plan, build, review, triage, fix, all green. 51 minutes, 407 turns, 111k tokens, one PR out the other end.</figcaption>
</figure>

Then and only then the human looks. By this point the easy stuff is handled, the backlog has captured the medium stuff, and the human is actually adding judgment.

This works. The reviews get caught early, the agent stays on track, and I can intervene at the point where my time is worth the most. But two things crack under load.

## Cost

Each loop eats a lot of tokens. A critical review is not a two-line "LGTM" prompt, it is pages of context, guidelines, and targeted checks. The triage step needs the full review output. The fix step needs the triage output plus the original code plus the repo context. Do this on every PR and the bill adds up.

And having the human only intervene at the PR stage means a lot of work has been done before. If the PR is turned down or changes (possibly big ones) need to be made, this adds to the costs. 

Opus 4.6 runs [$5 per million input tokens and $25 per million output tokens](https://platform.claude.com/docs/en/about-claude/pricing). That is one of the most expensive models that are currently available. It is even more expensive at scale with this approach: every feature goes through several expensive passes before a human is even involved. [Caching helps](https://www.finout.io/blog/anthropic-api-pricing), batching helps, but the floor is still non-trivial. And it is of course the most fun to have several processes run at once (let's say I can burn through my Claude Code token limits in no time). And then the extra usage starts, most of the time I am at 1 euro per hour. Not sustainable for the long run unless you are deeply funded and have money to burn (literally almost). So needless to say that I turned that off for most projects I work on.

The obvious question is whether you can drop to a cheaper model for some of the stages. I have tried, and the answer is no for most work. What works for me is Opus on planning and review, Sonnet on building. Results are better with Sonnet on everything, but token usage is a factor. I have never found a use for Haiku in this loop, and anything smaller than Sonnet on the build stage just breaks. The reviews from a weaker model miss the subtle stuff or flag perfectly fine code as breaking issues. A mediocre review is worse than no review because it gives you false confidence, the human at that point has to be able to trust the review done automatically. That is not the place to save tokens. Every time I have tried to save tokens by running a cheaper model somewhere in the chain, the quality drop caused rework, and the rework cost more tokens than I saved. The cheap option is, in the end, the expensive option. Given the hourly rate of the developer and the costs of tokens you can do a nice calculation of what it actually costs: in the end the human is more expensive. So making it easy for the human is key: less time spent per feature is cheaper. But rework costs extra time.

## Fatigue

The other problem is me (or developers in general). I can absorb code and automated reviews in a PR for a while, but only a while. Staring at well-structured PR summaries and deciding "yes, agree, ship it" over and over is draining in a way that writing code is not. You are in evaluation mode all day and never in creation mode, and evaluation mode runs on a smaller battery.

The obvious fix is to take the human out of every review, but that runs straight back into lesson one. Automated reviews alone miss things an experienced developer would catch in thirty seconds. A well-rested, motivated, experienced developer is still a better reviewer than any model I have tried, even with careful prompts and all the checklists in the world.

An interesting sub-observation: the automated review is probably better than a significant fraction of what developers actually do in practice. I would guesstimate 40%, with no hard numbers to back that up, based on the PR reviews I have seen from myself and colleagues over the years. Tired reviewer on a Friday afternoon versus an LLM run on a critical-review prompt? LLM wins, most of the time.

## The Ceiling

So what is blocking the next step, where I can actually trust the loop without babysitting it every (few) PRs?

Two things, and they are linked.

**Tokens.** Cost and availability. I need to run more review passes, with more context, on more PRs, and I cannot unless the per-token cost drops or the rate limits go up. Right now a busy day maxes out my limits before I am done, which is its own kind of bottleneck. Combine that with recent changes in Anthropic weighing tokens used between 14 and 22h (that is in my timezone) and it means having this run after 2 in the afternoon makes it even more expensive. And a few times per week connections fail, so lots of problems there.

**Smarter models.** Specifically, smarter models that I can run locally. Not because I want to self-host for the sake of it, but because local inference is how the per-token cost actually will drop. The current local options are getting genuinely good. [Qwen3 Coder Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) scores 44.3 on SWE-Bench Pro, above DeepSeek-V3.2 and GLM-4.7. [Qwen 3.5 hits 76.4 on SWE-bench Verified](https://techie007.substack.com/p/qwen-35-the-complete-guide-benchmarks), level with Gemini 3 Pro. [Gemma 4](https://ollama.com/library/gemma4) is a real step up from Gemma 3. 

But Opus 4.6 still [wins on the hard stuff](https://akitaonrails.com/en/2026/04/05/testing-llms-open-source-and-commercial-can-anyone-beat-claude-opus/): multi-file reasoning, long-horizon planning, the kind of review where you need to hold a whole architecture in your head. And the critical review stage is exactly that kind of work. For me to move the review loop onto local hardware, the local models need to actually match what Opus 4.6 does today, not approximately match it. We need something closer to Opus 4.6+++, running on a box in my office, before this flips.

That will happen. Local models are improving fast. But it is not this year.

## And Then There Is Electricity

[AI data center demand is pushing electricity prices up across Europe](https://www.cnbc.com/2026/02/12/electricity-price-data-center-ai-inflation-goldman.html). Goldman expects a 10 to 15% boost to European power demand over the coming 10 to 15 years, mostly from data centers. The [IEA puts global data center consumption on track to approach 1,050 TWh by 2026](https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai), which would rank data centers between Japan and Russia if they were a country.

On top of that, the situation in the Middle East has pushed [physical crude oil prices near $150 a barrel](https://www.iea.org/reports/oil-market-report-april-2026), with [shipping through the Strait of Hormuz still severely restricted](https://www.aljazeera.com/news/2026/4/14/global-oil-demand-to-plunge-amid-middle-east-war-disruptions). Energy, in other words, is getting more expensive while AI is driving demand higher, and both lines are bending up. Thankfully we have wind and sun.

So even the local-hardware dream has a cost floor (not forgetting the rising costs of RAM and GPUs). Running Opus-class models on your own machine still takes a lot of watts and decent hardware.

## Where This Leaves Me

The review-triage-fix catches more than manual review alone. It produces better PRs than pure automation. It lets me spend my attention on the decisions that need attention.

But it is not the end state. The end state, where I can genuinely let the builds run themselves, is gated by two things I cannot fix on my laptop: cheaper strong-model inference, and a local model that reaches Opus 4.6 plus. Until those arrive I am more or less at a standstill when it comes to further improvement.

Which is fine if you look back at what is now possible that was not possible only three years ago when all this started for me. I have run worse loops. And in the meantime I have learned a lot about where the human actually adds value in this stack, which is probably the most useful thing you can learn right now. 

If you are running a similar loop and have found something that works better, I would really like to hear about it.

---

*Automating builds, tuning review loops, or stuck on the same ceiling? <a href="#" onclick="task1(); return false;">Get in touch</a> to compare notes.*

## Resources

### Models and pricing

- [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) - Official Anthropic pricing for Opus 4.6 and other models
- [Anthropic API pricing deep dive](https://www.finout.io/blog/anthropic-api-pricing) - Caching and batching cost breakdown
- [Qwen3-Coder-Next on Hugging Face](https://huggingface.co/Qwen/Qwen3-Coder-Next) - Open-weight coding model
- [Qwen 3.5 benchmarks](https://techie007.substack.com/p/qwen-35-the-complete-guide-benchmarks) - SWE-bench and real-world results
- [Gemma 4 on Ollama](https://ollama.com/library/gemma4) - Local deployment
- [Can anyone beat Claude Opus?](https://akitaonrails.com/en/2026/04/05/testing-llms-open-source-and-commercial-can-anyone-beat-claude-opus/) - Open vs commercial comparison

### Energy and infrastructure

- [IEA: Energy demand from AI](https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai) - Global data center projections
- [Goldman Sachs on AI electricity demand](https://www.cnbc.com/2026/02/12/electricity-price-data-center-ai-inflation-goldman.html) - European power demand forecast
- [IEA Oil Market Report April 2026](https://www.iea.org/reports/oil-market-report-april-2026) - Current supply disruptions
- [Middle East crisis and global oil demand](https://www.aljazeera.com/news/2026/4/14/global-oil-demand-to-plunge-amid-middle-east-war-disruptions)

### Related posts

- [Human in the Loop](/ai/llm/development/best-practices/2025/11/14/human-in-the-loop-ai-code-review.html) - Why human review still matters
- [When LLMs Actually Deliver](/ai/development/operations/2026/04/16/when-llms-actually-deliver.html) - The tooling that makes LLMs useful
- [gtk: Filtering CLI Noise to Save Tokens](/ai/development/tools/2026/04/09/gtk-cutting-llm-token-costs-cli-output.html) - Related token-cost work
