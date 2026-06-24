---
layout: post
title: "Why LLMs Will Not Have Your Next Big Idea"
date: 2026-06-24
categories: ai opinion research
description: "After years of daily LLM use, I think we can draw a line: extraordinary tools for working within known territory, structurally unable to cross beyond it."
keywords: "LLM limitations, AI creativity, convex hull, next-token prediction, LLM novelty, Karpathy LLM wiki, semi-intelligence, AI original ideas"
image: /assets/images/why-llms-will-not-have-your-next-big-idea-blog.png
---

<figure>
  <img src="/assets/images/llm-limitations-boundary.jpg" alt="Moody coastline with cliff edge disappearing into mist, boundary between land and sea" width="1920" height="1280" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>Photo by <a href="https://unsplash.com/@phillbrown">Phill Brown</a> on <a href="https://unsplash.com">Unsplash</a></figcaption>
</figure>

I have been using LLMs daily for years now, mostly to code, but also for research, writing, and analysis. They are genuinely useful, sometimes spectacularly so. I have built tools, workflows, and entire coding pipelines around them. So this is not a "LLMs are bad" post. This is about something I have been thinking about for a while, and an enthusiastic youtube video about the [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) got me thinking again about the drawbacks (besides the obvious benefits) and why I think that way of gathering and using data is not good enough for me.

In this post I will take you through two ideas: the first one is 'LLMs can not create truly new ideas' and the second is that 'the simplification of information in an early stage leads to suboptimal results'. And the end conclusion is that, although we can do magnificent things with LLMs, this technique is not able to solve any real problems and will always result in mediocrity.

## The Argument From Mechanism

Next-token prediction works by sampling from a distribution fitted over the training corpus. There is no reasoning faculty that could exceed what the text encodes. The model stores a very high-dimensional interpolation function over token sequences. It produces outputs for inputs not exactly in the training set (that is what makes it useful), but it interpolates within the [convex hull](https://arxiv.org/abs/2110.09485) of expressed human thought. It does not extrapolate beyond the manifold it was fitted to, and the model does not learn.

What I here define as a good idea is a genuine breakthrough that is good *because* it violates the regularities the corpus taught. That is structurally outside the region the model can reach. To the model, the revolutionary idea and the incoherent error look the same: both are low-probability under the learned distribution. There is no mechanism to favour "low-probability because true-and-new" over "low-probability because wrong."

The model's only notion of "good" is "high-probability under the learned distribution," which means "resembles what was already thought." That is anti-correlated with genuine novelty almost by definition. The quality filter is filtering for conventionality, which explains why every LLM output feels competent but unsurprising. Ask any LLM to build you a web app and you will get React, Tailwind, and shadcn/ui. And only if you are an expert (or have a good general knowledge) you will spot the things it misses or simply fails on (your knowledge on that domain is then above medium).

## The Argument From Scale

Now you could argue that there are a lot of good solutions in a LLM (including the novel ones we need to solve important issues like climate, energy and water management). And that they are simply buried in the vast knowledge of the LLM and need to be combined over different domains and then extracted. But if recombinational novelty could produce breakthroughs, the current reality would have surfaced them. We have the largest idea-discrimination experiment ever running right now, with millions of LLM instances running daily, with humans reading and judging. If LLMs would live up to their promise (the big breakthrough for humanity speech we have been hearing for a few years now): why do we not see those novel ideas showing up?

The result of those LLMs has a different character: a flood of interpolative novelty (restatements, syntheses, transfers of known methods to adjacent problems) and nothing on extrapolative novelty (fundamental breaks, genuinely new ideas). That bimodal signature is exactly what the mechanism predicts. Abundant where the manifold is dense (between known points), absent where it is not (beyond them).

If the good recombinations were reachable but merely unrecognised, millions of human discriminators sifting the output over years would have found them. They have not. The breakthroughs are not hidden in the output. They are simply not there.

Recent research backs this up. [Chakrabarty et al. (2025)](https://arxiv.org/pdf/2504.12320) found that LLM-generated ideas lead to homogenous outcomes across domains, and [Tian et al. (2025)](https://arxiv.org/pdf/2504.15266) showed that aligned LLMs remain trapped in a "safe attractor basin" created during RLHF, limiting exploratory novelty even with strong creativity prompts. There is a [counterpoint from Jiang et al. (2024)](https://arxiv.org/pdf/2412.14141) showing LLMs can combine existing concepts in ways rated more novel than ideas from NLP researchers, but that is combinatorial novelty (recombining known things), not extrapolative novelty (ideas that break the frame). 

## The Pipeline Problem

This connects to something I ran into while looking at Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [rohitg00's v2 extension](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2). A wiki is basically a collection of datapoints (documents, website, databases etc) that can be connected based on theme or subject. This leads to a great overview of data on a subject with beautiful graphs that can help you understand interconnectedness of the data points. However most wikis fail here: they compile raw sources into a structured, interlinked knowledge graph at ingestion time, resulting in a more or less fixed but definitely 1 to low-dimensional description of connections. Before any question has been asked, before anything is known about what can safely be dropped, irreversible choices are made at the point of minimum information about what those choices should preserve. And the problem here is that an LLM makes those choices, easy but at the cost of massive information loss.

This is not just a gut feeling. Information theory has a name for it: the [Data Processing Inequality](https://en.wikipedia.org/wiki/Data_processing_inequality). It says that processing data can only destroy information, never create it. If X goes through transformation T to produce Y, then Y cannot contain more information about the original source than X did. Every step in a pipeline can only lose or preserve, never gain. It is the same discipline as keeping the RAW file instead of the JPEG, or lazy evaluation in programming: defer the irreversible reduction until the moment you know what you actually need.

The wiki does the opposite. It flattens at ingestion, the earliest possible moment, when it has the least information about what any future question will require. When the target artifact is a node-edge graph, only graph-shaped information survives extraction. Argument structure, evidential weight, mechanism, scope conditions, the reasoning connecting premise to conclusion: gone. Not because the model failed, but because it succeeded at building exactly the thing it was aimed at, and that thing has no room for any of it. A wiki link (even a typed one like "refutes") collapses a multi-dimensional relationship into a single undifferentiated connection. The real relationship between two claims has independent components: logical relation, evidential strength, domain, temporal validity. The graph has one slot.

For planning a holiday this does not matter, losing some nuance about hotel reviews may not be so important (and you can deliberately choose that this is not important). But for anything where the quality of reasoning matters (medical research, legal analysis, policy decisions, engineering trade-offs), early information loss is crippling. For example three pro-articles enter a pipeline; the compiled page reflects the pro-standpoint and see it as the base stance. Then a fourth article is added with a very strong point contra, that should weigh much heavier than the three pro documents with light evidence. The model has no faculty for evaluating that the fourth article's methodology is stronger. Evidential weight and citation count are different quantities, and the system only has access to the latter. Worse, the three pro-articles arrived first, so they created the concept pages, set the framing, and named things. The dissenting source arrives into a wiki already shaped to express the opposite position. It gets architecturally demoted to a status of a light contra, basically a footnote, where it should dismiss the entire pro standpoint.

And then it starts adding up: in a serial pipeline (entity extraction, graph building, contradiction resolution, consolidation), each step consumes the previous step's output as ground truth. Chain a 95%-reliable step ten times and you end up with a reliability of 60% (0.95^10 --> 0.60). And on top of that these errors are correlated toward plausibility and majority framing, so the real number is worse. This is well-documented in cascading ML systems: [Sculley et al. (2015)](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) at Google showed that ML pipelines accumulate "technical debt" where each model's errors become the next model's training signal, creating feedback loops that are extremely hard to detect or debug. LLMs are slightly different but it is reasonable to state that they are not better at this.

Making it extra complicated if you are not a domain expert is that perceived reliability and actual reliability diverge in opposite directions as the pipeline grows. Each added step makes the surface richer, more complete-looking, more authoritative (more scores, typed edges, structure) while simultaneously multiplying against the reliability floor. The more elaborate the system, the more trustworthy it looks and the less trustworthy it (most likely) is. 

The correct approach to choosing where to cut information density is as late and as informed as possible. The cut should be applied at the query, shaped by the query, discarding only what that specific question does not need. 

And this connects directly to the novelty problem. Every mechanism in these systems (confidence scoring, contradiction resolution, consolidation, forgetting curves) is tuned to suppress exactly the signature of genuine novelty: low support, high conflict, poor fit with existing structure. A good new idea is an anti-consensus object. The pipeline converts whatever novelty does appear into "noise to be cleaned up," because it has no faculty to see it as anything else.

## Semi-Intelligence

So we can define what we are actually dealing with: full competence within the convex hull of expressed human thought, zero reach outside it.

This has quite some implication: most practical work lives inside that hull: writing code, synthesising research, drafting documents, debugging, refactoring, transferring methods from one domain to an adjacent one. LLMs are quite good at all of this. I use them for it every day and they make me measurably more productive.

But "inside the hull" has a boundary, and everything interesting about the future of ideas happens at or beyond that boundary.

## The Great Equaliser

There is a way to frame this that makes the stakes clearer: the LLM is a nivellator. It pulls everyone toward the median of existing thought.

If you were below that median, you get lifted up. That is genuine value. I [wrote about this before](/ai/development/opinion/2026/06/15/why-diy-software-is-great-until-it-is-not.html): the democratisation of capability is real and good. Someone who could not write code can now build a working application. Someone who could not write a decent email can now produce clear, professional communication.

But if you were above that median, or thinking orthogonally to it, the LLM pulls you *down* toward consensus. Your unusual angle gets smoothed into the conventional take. Your weird framing gets normalised. Your instinct that the consensus is wrong gets buried under a fluent, well-structured argument for why the consensus is right. The tool does not argue with you. It just quietly steers everything toward what the training data says is most likely.

The net effect is convergence toward the mean. The better the model gets, the stronger the pull. More people producing more competent work, all of it sounding increasingly alike. Ask five people to use an LLM to write a strategy document and you get five documents that could have been written by the same person.

If you are building systems on top of LLMs (and I am), be honest about what they can and cannot do. They are navigation tools for existing knowledge, not idea generators. Do not expect an LLM pipeline to surface the insight that changes your approach. It will give you a very competent synthesis of what is already known, and that is genuinely valuable, but it is a different thing.

The people who matter most here are the ones the LLM is worst at emulating: the imaginary thinkers, the artists, the scientists, the outliers, the stubborn contrarians who look at the consensus and say "but what if that is wrong." People whose judgment is not a statistical shadow of what has already been thought, but a faculty that can value the unfamiliar as such. They were always important, and in a world where the median is increasingly automated, they are irreplaceable.

So hurray to the unconventional thinkers: the world needs you, so keep thinking those original thoughts.

*Thinking about what LLMs can and cannot do for your team? <a href="#" onclick="task1(); return false;">Get in touch</a> to compare notes.*

## Sources

### On LLM creativity and limitations

- [Has the Creativity of Large-Language Models Peaked?](https://arxiv.org/pdf/2504.12320) (Chakrabarty et al., 2025) -- LLM-generated ideas lead to homogenous outcomes across domains
- [Roll the Dice & Look Before You Leap](https://arxiv.org/pdf/2504.15266) (Tian et al., 2025) -- Aligned LLMs stay trapped in RLHF's "safe attractor basin"
- [Neither Stochastic Parroting nor AGI](https://arxiv.org/abs/2505.23323) (May 2025) -- LLMs extrapolate from training priors but only within domain boundaries
- [LLMs Can Realize Combinatorial Creativity](https://arxiv.org/pdf/2412.14141) (Jiang et al., 2024) -- Counterpoint: combinatorial novelty is real, but distinct from extrapolative novelty
- [Learning in High Dimension Always Amounts to Extrapolation](https://arxiv.org/abs/2110.09485) (Balestriero et al., 2021) -- The convex hull problem in high-dimensional learning

### On information loss and LLM pipelines

- [Data Processing Inequality](https://en.wikipedia.org/wiki/Data_processing_inequality) -- Information theory: processing can only destroy information, never create it
- [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) (Sculley et al., 2015) -- Google's analysis of cascading errors in ML pipelines
- [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (Karpathy, 2026) -- Compiled knowledge as alternative to RAG
- [LLM Wiki v2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2) (rohitg00, 2026) -- Extension with confidence scoring, temporal decay, and knowledge governance

### Related posts

- [When LLMs Actually Deliver](/ai/development/tools/2026/04/16/when-llms-actually-deliver.html) -- Where LLMs shine: the interior of the hull
- [Why DIY Software Is Great Until It Is Not](/ai/development/opinion/2026/06/15/why-diy-software-is-great-until-it-is-not.html) -- Similar theme: tools change what is possible, but not what requires expertise
- [Let the AI Pick: React](/ai/development/opinion/2026/02/13/let-the-ai-pick-react.html) -- The conventionality filter in action: every LLM picks the same stack
