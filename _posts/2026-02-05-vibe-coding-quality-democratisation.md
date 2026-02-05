---
layout: post
title: "Vibe Coding: Product Quality and Democratisation"
date: 2026-02-05
categories: ai development
description: "Vibe coding changes who can build software and what happens when they do. On product quality, democratisation, and when personal tools become products."
keywords: "vibe coding, AI development, software democratisation, product quality, LLM coding tools, build vs buy, equality"
---

I read a few articles the last few weeks about the state of SaaS products and the changes in making and selling software because of the emergence of LLM use among a greater customer base. Some are calling it the SaaSpocalypse: customers can now build their own tools, so why would they keep paying for yours? ([SaaS](https://en.wikipedia.org/wiki/Software_as_a_service): Software as a Service)

And combine that with increases in searches for "vibe coding": a jump of 6,700% in 2025. By late 2025, 84% of developers were using or planning to use AI coding tools.

So that seems to be quite a threat for a lot of software businesses. Bad times are coming. Or are they? There are multiple facets to the story, let's look at two of them: product quality and social implications.

## Product Quality

Most of the vibe-coded applications I have seen are quite bad. A few weeks ago I tried to contribute to an open-source project that was clearly vibe-coded. It was a great idea, I started with enthusiasm, but ran away within an hour.

The code looked fine at first glance: clean-ish syntax, impressive number of files. But the moment I tried to understand what it actually did, I hit a wall. Fragile abstractions, bad architecture and bugs, so many small bugs.

Now I believe that bad code is not a problem per se, just as 'good' code is not a goal in and of itself, just for the sake of writing good code (however you want to define that). (The lack of a proper definition is what keeps me from pursuing good code among other things.) I am much more pragmatic: does the code solve a problem? Yes? Then it is good code; it fulfills its purpose. However, take into account that the purpose is not just to solve the problem then and there, but also in the future. And the cost it takes to maintain the solution for the problem has by definition to be lower than the (perceived) costs the problem causes. Costs can be money, time, assets, reputation, failing to comply etc. If the costs are low enough (and good software drives down the total cost, by reducing maintenance time etc) it is a good solution. 

So the main reason to write good code is to drive down the cost of the solution to below the cost of the problem. That also means that good code is not a fixed outcome or definition, it depends on the situation. That also means that for personal use a badly coded vibed app can be perfect: who cares that it is bad? It solves my problem! (Good for you, power to the people etc.)

And that touches on what for me is one enormously important aspect: democratisation of software. No-code and low-code platforms took the first steps here, making it possible to build without writing code at all. Now AI-assisted coding takes it further: you can create actual software, not just what fits within a platform's constraints. Suddenly you do not need a masters degree to do complicated things with your computer: you can do all sorts of stuff!

I really am wondering what this will mean in terms of social improvement, equality and human rights. The keys to writing software were always in the hands of white, middle-aged, rich men with a predisposition for details and light autism, who kept their trades securely guarded and often were and are not able to properly communicate with their customers. If that is no longer the case, what will happen?

<figure>
  <img src="/assets/images/vibe-coding-democratisation.jpg" alt="Group of people with different skin tones collaborating around a laptop">
  <figcaption>The best "diverse" stock photo I could find. Note how everyone is still conventionally attractive. We have a way to go. Photo by <a href="https://unsplash.com/@silverkblack">Vitaly Gariev</a> on <a href="https://unsplash.com/photos/8gAbl776pc0">Unsplash</a>.</figcaption>
</figure>

Of course there is still a barrier: LLM costs. Right now, using these tools at scale costs real money, and that creates its own form of gatekeeping. But I expect this to come down significantly in the coming years through economies of scale, efficiency gains in model architectures, reduced energy consumption, and the rise of smaller models that perform nearly as well as the large ones.

But getting back to product quality: if writing the software is no longer the hard part (no more writing 'print' in javascript after working with python for weeks and making some changes in a javascript project), what will change?

## The Bottleneck Shift

Something strange happens when you can generate code instantly: you lose the thinking time that was hidden in the coding process.

Before AI tools, writing code forced a pace. You'd sit with a problem for days, turning it over in your mind while your fingers typed. The friction of implementation gave you space to contemplate, to look at the problem from different angles, to notice that your initial understanding was wrong.

Now? You describe what you want and get code in seconds.

The bottleneck shifts: building becomes trivial, but *understanding the problem correctly* becomes the new hard part, and you have less time to figure it out.

[Research on vibe coding](https://arxiv.org/abs/2512.11922) calls this the "flow-debt tradeoff": the speed you gain now, you pay back later in technical debt. The AI doesn't maintain a unified architectural vision across prompts, nobody documents why the code is the way it is, and the problems only surface during maintenance and scaling. The productivity gains are real, but they're borrowed time.

This is where personal use and business use diverge, because for your own tools "it works" is enough (who cares if it's messy, it solves your problem), but the moment software becomes a product, something others depend on and that needs to work next year, the equation changes completely. Building was always only about 10% of the work anyway, while the other 90% (compliance, security, support, maintenance, edge cases) doesn't go away just because building got easier.

So yes, the SaaS products that were basically CRUD apps with a subscription are in trouble, but that's not an AI problem, that's a product problem. You were always one motivated developer away from obsolescence; AI just made that developer faster.

That said, vibe coding does have a legitimate place in professional software development. In our workflow we now use it as a scratch pad: instead of going through an entire UI design process, business research, endless meetings and iteration cycles, we vibe-code the idea first and test it with the customer. Does it answer the problem? Great, now we know what to build properly. This saves so much time that would otherwise go into design documents and alignment meetings.

The challenge is managing expectations. You have to make clear to the customer that this is just a draft to explore the idea, and the real thing will cost time and money to build. That can be difficult to grasp: "But you already built it? Why does it take so much time and cost so much?" The answer is everything we discussed above: the 90% that isn't building.

## Democratisation

Back to the social angle: what happens when software creation is widely accessible? Will we see tools built by and for communities that Silicon Valley never understood? Will existing power dynamics be rearranged? Hopefully yes to both.

The complaint that vibe-coded apps are "bad" misses the point entirely: if someone who couldn't build software before can now solve their own problem, messy code and all, that's a win. The quality bar for personal tools is "does it work for me?" and nothing more. The trouble comes when personal tools try to become products, when someone thinks "this works for me, I should sell it." That's when understanding your own problem (relatively easy) becomes understanding someone else's problem (hard), and maybe it's even harder now because building no longer forces you to slow down and think.

So is the time of building and selling SaaS products over? Some think so, but the narrative that "customers will just build their own" underestimates what it takes to maintain and be accountable for software others depend on. Meanwhile, go vibe-code something for yourself, seriously. That's the democratisation promise and it's real, just have fun building!

---

*Thinking about vibe coding, democratisation, or the future of software products? I'd love to hear your perspective. <a href="#" onclick="task1(); return false;">Get in touch</a> to share your thoughts.*

## Resources

- [AI is Killing B2B SaaS](https://nmn.gl/blog/ai-killing-b2b-saas)
- [Vibe Coding in Practice: Flow, Technical Debt, and Guidelines](https://arxiv.org/abs/2512.11922)

## Further Reading

On democratisation and its implications:

- [Democratizing AI (IBM)](https://www.ibm.com/think/insights/democratizing-ai)
- [Democratization in the age of artificial intelligence (Taylor & Francis)](https://www.tandfonline.com/doi/full/10.1080/13510347.2024.2338852)
- [The Democratization of AI: A Pivotal Moment (Justia)](https://verdict.justia.com/2025/02/24/the-democratization-of-ai-a-pivotal-moment-for-innovation-and-regulation)
- [How No-code Platforms are Democratizing Software Development](https://dorik.com/blog/how-no-code-platforms-are-democratizing-software-development)

On gatekeeping in tech:

- [Gatekeeping in the software industry](https://bernardoamc.com/gatekeeping-software-development/)
- [No Gates, No Keepers](https://soatok.blog/2021/03/04/no-gates-no-keepers/)
