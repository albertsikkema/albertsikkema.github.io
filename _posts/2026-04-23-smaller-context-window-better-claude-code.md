---
layout: post
title: "Why I Shrunk Claude Code's Context Window Back to 200k"
date: 2026-04-23
categories: ai development tools
description: "The 1M context window in Claude Code sounds like an upgrade. In practice, constraining it to 200k with early compaction produces better results and lower costs."
keywords: "Claude Code, context window, context rot, compaction, CLAUDE_CODE_DISABLE_1M_CONTEXT, CLAUDE_AUTOCOMPACT_PCT_OVERRIDE, token optimization, LLM context management"
image: /assets/images/smaller-context-window-better-claude-code-blog.png
---

<figure>
  <img src="/assets/images/context-window-rain-glass.jpg" alt="Rain-covered glass with blurred warm lights behind, signal obscured by noise" width="1920" height="1078" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>Photo by <a href="https://unsplash.com/@c_g_">c g</a> on <a href="https://unsplash.com">Unsplash</a></figcaption>
</figure>

This morning I watched a video on context window management in Claude Code as part of my daily "keep up with what is happening in the LLM space" routine. Good content, solid diagnosis of the problem. But everything in it was about manual interventions: trigger compaction at the right moment, use structured handoffs, rewind instead of correcting. All valid techniques. But there is an issue that is buried deeper and there are two settings, buried in the documentation, that may solve most of this.

## The Problem With More Room

Since Opus 4.6 it ships with a default [1M token context window](https://claude.com/blog/1m-context-ga). Five times the 200k window of their predecessors. Sounds like a pure upgrade. Great! 

It is not. The single most important thing for working with LLMs is context management: keep it as small as possible with as relevant info as possible and nothing more than that. Anthropic's [engineering team](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) says you should be "striving for the minimal set of information that fully outlines your expected behavior." Their [documentation](https://platform.claude.com/docs/en/build-with-claude/context-windows) acknowledges that "as token count grows, accuracy and recall degrade, a phenomenon known as context rot." The root cause is the n-squared attention mechanism: double the context, quadruple the number of pairwise relationships the model has to track.

I am not alone in experiencing this. Some quick research finds similar sentiment: [Paul Gauthier](https://simonwillison.net/2025/Jan/26/paul-gauthier/), the creator of Aider, found that "every model seems to get confused when you feed them more than ~25-30k tokens." He calls it the number one problem his users report. [JetBrains Research](https://blog.jetbrains.com/research/2025/12/efficient-context-management/) tested observation masking (hiding old tool outputs) and found a 52% cost reduction while *boosting* solve rates by 2.6%. Less context, better results. The [NoLiMa benchmark](https://eval.16x.engineer/blog/llm-context-management-guide) found that 11 of 12 tested models dropped below 50% of their short-context performance at just 32k tokens. Not 200k. Not 1M. 32 thousand.

In practice this means: more hallucinations, forgotten instructions, goal drift, inconsistent decisions. Not at 900k tokens. Much, much earlier.

## What I Keep Seeing

A lot of the advice I come across focuses on manual interventions. Trigger compaction yourself at the right moment. Use `/clear` when switching tasks. Save state to a JSON file before clearing. Ask Claude for periodic summaries. Use sub-agents to keep intermediate work out of your main context.

These are all valid. I use sub-agents heavily (they get their own fresh context window, which is [the single most effective architectural pattern](https://www.morphllm.com/context-rot) for avoiding context rot) and `/clear` between unrelated tasks. But manual interventions are workarounds for a window that is too large, not fixes for the underlying problem. They require you to watch your context usage while trying to get work done. That is overhead the tooling should handle.

[Amp](https://tessl.io/blog/amp-retires-compaction-for-a-cleaner-handoff-in-the-coding-agent-context-race) went further: they dropped compaction entirely and designed around short threads with clean handoffs. Their senior engineer Dan Mac put it bluntly: "You should basically never use compaction.".

## The Simpler Fix

Two [environment variables](https://code.claude.com/docs/en/env-vars) solve this without ongoing attention:

**`CLAUDE_CODE_DISABLE_1M_CONTEXT`** set to `1` caps the context window back to 200k tokens. It removes the 1M model variants from the [model picker](https://code.claude.com/docs/en/model-config#extended-context) entirely.

**`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`** set to a value between 1-100 controls when auto-compaction triggers, as a percentage of context capacity. The [default is around 95%](https://code.claude.com/docs/en/how-claude-code-works), which means on a 1M window, compaction does not kick in until you are at 950k tokens. That is way past the point where quality has degraded.

Set both in your project or user settings:

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_1M_CONTEXT": "1",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "70"
  }
}
```

200k window at 70% threshold means compaction triggers around 140k tokens. Well before quality drops off. Compaction runs more frequently but with less context to summarize, which means better summaries. [Andrej Karpathy](https://x.com/karpathy/status/1937902205765607626) described context engineering as "filling the context window with just the right information for the next step." Too much, and "performance might come down." A constrained window forces that discipline automatically.

## The Cost Angle

Every turn in Claude Code sends the full conversation context to Anthropic's servers. If your context window is sitting at 600k tokens of accumulated tool output, file reads, and old conversation, all of that gets re-sent and re-billed on the next message.

With [Opus 4.6 at $5 per million input tokens](https://platform.claude.com/docs/en/about-claude/pricing), a 600k context costs a lot per turn just for input (not exactly 3 dollar because there is also caching going on). A 140k context (right before compaction) theoretically costs $0.70. Over a long session with dozens of turns, that difference adds up. One user on [Hacker News](https://news.ycombinator.com/item?id=47580395) described burning through $100 in credit when Opus 4.6 "got stuck in a bullshit reasoning loop." So a smaller window is better for quality and is cheaper.

## Compaction Is Not a Safety Net

The standard advice is to rely on compaction to keep your context clean. And compaction works, sort of and sometimes. It summarizes the conversation to free up space. But it is lossy. The model decides what matters and what gets dropped, and its judgment is not always yours. Often I feel like I have to start over again with the nuances of the problem we were working on.

Another problem is what happens *after* compaction. Yesterday I was in a session, working on changes across a repo. Auto-compaction kicked in mid-task. First thing Claude did after compacting: committed everything. Without being asked. It lost enough context to forget that I had not asked for a commit, saw uncommitted files and went ahead.

[Thariq Shihipar](https://claude.com/blog/using-claude-code-session-management-and-1m-context) from the Claude Code team recommends compacting proactively at 50-60% capacity instead of waiting for auto-compaction. Good advice. But if you constrain your window to 200k and set the threshold to 70%, you get roughly the same effect automatically. No need to watch your token count and manually trigger `/compact` at the right moment.

There is another upside to the smaller window: compaction itself gets better. If compaction triggers at 70% and reduces back to roughly 30%, the 1M window has to summarize away 400,000 tokens of conversation. The 200k window only discards 80,000. Five times less information to lose. Smaller contexts lead to more accurate summaries. (For the information theory purists out there: I am aware that it is more complicated than this, please forgive my shortcuts)

## Fresh Sessions, Not Long Ones

The env vars help within a session. But the bigger win is avoiding compaction by not having long sessions in the first place.

My workflow separates every phase into its own session. Research runs in one session, planning in another, building in a third. Never chained together in the same conversation. I [built an orchestrator](/AI/LLM/development/productivity/2025/11/21/orchestrator-automating-claude-code-workflows.html) that does this automatically: each step launches a separate Claude Code instance. The whole rationale is context isolation. Each phase starts clean with only the information needed to start that session.

This is the same principle behind sub-agents, just at a larger scale. When Claude Code spawns a sub-agent, that agent gets its own fresh context window. All intermediate work (file reads, grep output, failed attempts) stays in the sub-agent's context. Only the final result comes back. [Morph's research](https://www.morphllm.com/context-rot) found a 90% performance gain using sub-agent architecture over single-agent. The reason is straightforward: every file read and tool call that stays out of your main context is noise that never competes for attention.

## The Counterintuitive Takeaway

The 1M context window is a capacity increase, not a quality increase. More room means more space for noise, higher bills, and worse output once you cross the degradation threshold. Steve Smith [calls it](https://blog.nimblepros.com/blogs/context-windows-wont-grow-forever/) "a huge junk drawer." Glen Rhodes [describes context](https://glenrhodes.com/context-window-management-treating-llm-context-as-working-memory-not-unlimited-storage/) as working memory, not storage, and argues you should treat it like RAM on a constrained system: deliberate about what gets loaded, suspicious of anything that lingers.

The best results I get from Claude Code come from keeping the window small, compacting early, and never letting one phase pollute the next. Two environment variables and a habit of starting fresh. That is the whole trick.

---

*Running into context issues or managing your own Claude Code setup? <a href="#" onclick="task1(); return false;">Get in touch</a> to compare notes.*

## Resources

### Claude Code documentation

- [Using Claude Code: session management and 1M context](https://claude.com/blog/using-claude-code-session-management-and-1m-context) -- Thariq Shihipar's practical guide to context management
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) -- Anthropic's engineering blog on context rot and mitigation
- [Claude Code environment variables](https://code.claude.com/docs/en/env-vars) -- Official docs including the two env vars discussed here
- [Explore the context window](https://code.claude.com/docs/en/context-window) -- Interactive simulation of how context fills during a session
- [Context windows API docs](https://platform.claude.com/docs/en/build-with-claude/context-windows) -- Model-by-model context sizes and Anthropic's acknowledgment of context rot

### Research and analysis

- [Lost in the Middle (Liu et al., 2023)](https://arxiv.org/abs/2307.03172) -- The foundational research on performance degradation in long contexts
- [Context Rot research by Chroma](https://www.trychroma.com/research/context-rot) -- Evaluation of 18 LLMs showing universal degradation with input length
- [JetBrains: Smarter Context Management for Agents](https://blog.jetbrains.com/research/2025/12/efficient-context-management/) -- Observation masking: less context, better results
- [Morph: Context Rot complete guide](https://www.morphllm.com/context-rot) -- Sub-agent architecture and agent-specific context data
- [Compaction research across coding tools](https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f) -- Claude Code, Codex CLI, OpenCode, Amp compared

### Developer perspectives

- [Paul Gauthier on practical context limits](https://simonwillison.net/2025/Jan/26/paul-gauthier/) -- Aider creator: models get confused above 25-30k tokens
- [Karpathy on context engineering](https://x.com/karpathy/status/1937902205765607626) -- "Too much or too irrelevant, and performance might come down"
- [Amp drops compaction for handoff](https://tessl.io/blog/amp-retires-compaction-for-a-cleaner-handoff-in-the-coding-agent-context-race) -- Why one coding tool designed around short threads
- [Why Context Windows Won't Keep Growing Forever](https://blog.nimblepros.com/blogs/context-windows-wont-grow-forever/) -- Steve Smith on diminishing returns and the junk drawer effect
- [Context as working memory, not storage](https://glenrhodes.com/context-window-management-treating-llm-context-as-working-memory-not-unlimited-storage/) -- Glen Rhodes on treating context like constrained RAM

### Related posts

- [The Orchestrator: Automating Full Claude Code Workflows](/AI/LLM/development/productivity/2025/11/21/orchestrator-automating-claude-code-workflows.html) -- Each phase in its own Claude Code instance
- [Fully Automated LLM Builds: Where It Actually Stops](/ai/development/automation/2026/04/17/automated-builds-cost-fatigue-ceiling.html) -- Token costs as a ceiling on automation
- [gtk: Filtering CLI Noise to Save Tokens](/ai/development/tools/2026/04/09/gtk-cutting-llm-token-costs-cli-output.html) -- Reducing what goes into context in the first place
