---
layout: post
title: "The Third Option for Enterprise AI"
date: 2026-06-28
categories: ai opinion cloud
description: "Enterprise AI does not have to be US hyperscalers or on-prem. European providers running open-source models offer a third path worth considering."
keywords: "sovereign AI, European cloud, data sovereignty, GDPR, open source LLM, Mistral, enterprise AI, on-premises AI, cloud AI"
image: /assets/images/the-third-option-for-enterprise-ai-blog.png
---

<figure>
  <img src="/assets/images/third-option-enterprise-ai.jpg" alt="European countryside with dramatic clouds over rolling hills" width="1920" height="1280" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>Photo by <a href="https://unsplash.com/@adlan">Adlan</a> on <a href="https://unsplash.com">Unsplash</a></figcaption>
</figure>

Almost all AI services I use with the different companies and governments I worked with are American based, mostly Azure and Anthropic. As we are all aware this is not a situation that is acceptable: especially not with 'the orange child in the white house' spewing nonsense every day and keeping us on our toes, American companies are no longer a trustworthy partner. They obviously chose sides during the orange child's election, marking a departure from the heralded status American tech companies had over the last decades. 

So all kinds of solutions are proposed to solve this. And basically there are two main trains of thought (or perhaps three). Option one: keep using the big American cloud providers (OpenAI, Anthropic, Google) and accept that your data crosses the Atlantic. As you can derive from the previous paragraph this is technically an option, but in practice definitely not: trust has been broken and will take many years to rebuild (if at all, given the current direction of American foreign politics). The alternative that I get to see pitched a lot: go fully local, run your own hardware, keep the data in the building. (Could be an option, I was in that camp for a long time, but what I do not understand about this proposition is that those who propagate it, do not mention that this would only be logical if we would move back from the cloud to full on-prem hosting of all data. For various reasons I do not see this happening anytime soon)

So that leaves a third option that makes more practical sense to me and to most European companies and is a big business opportunity within Europe: hosting opensource LLMs on European servers by European companies, that make sure privacy and data governance are guaranteed.

## Option 1: Stay on US Hyperscalers

The current situation is using US companies for LLM: it works, it is what we are used to. However this is not sustainable, both in costs and in privacy and risking being cutoff of the service on a whim of the orange child. 

Given that it is hard to filter PII or medical or legal data from a prompt, it is a minefield of GDPR and privacy issues that you need to navigate. And that is assuming you are able to make sure your employees only use your approved methods (do not forget your employees are infinitely creative to work around them, so you better make the approved methods really easy to use and perform really well, otherwise you could as well not have bothered at all)

## Option 2: Go Fully On-Prem

The counterargument is to bring everything in-house. Buy GPUs, rack them in your server room, run open-source models, keep all data on your own hardware. Full control, full sovereignty, zero legal risk.

The edge AI market is real and growing, and there are genuine use cases for local inference: air-gapped environments, defence, certain healthcare scenarios.

But here is where it gets illogical for most companies. These same organisations run their email on Microsoft 365, their CRM on Salesforce, their databases on Azure or AWS, their file storage on SharePoint. They trust cloud providers with all of that. And then the argument is that specifically the LLM part, the thing that processes text and returns text, needs to be on physical hardware in the basement?

If your data governance concern is serious enough to run AI on-prem, it is serious enough to move everything back on-prem. And that is probably not going to happen. 

There is also the cost problem. Running inference locally requires expensive GPUs, it is really complicated, so you need people who know how to operate them, and continuous investment to keep up with model improvements. For companies that are not in the AI infrastructure business, this is a distraction. (even though personally I believe every company should be in full control of its own data and software and I know this belief is shared by many IT and data professionals, this is unfortunately not a shared vision across most boards)

## Option 3: European Providers, Open-Source Models

The option I find most interesting is getting discussed more and more, but not yet seriously enough: European cloud providers running open-source models under European jurisdiction.

The landscape here has changed dramatically in the last two years. [Mistral AI](https://mistral.ai/) now offers models under Apache 2.0 with inference running entirely in EU data centres. [Scaleway](https://www.scaleway.com/) offers managed GPU instances with model-as-a-service APIs under French legal jurisdiction. [Deutsche Telekom invested over a billion euros](https://www.t-systems.com/de/en/insights/newsroom/news/ai-sovereignty-for-germany-and-europe-1124980) in an Industrial AI Cloud with 10,000 GPUs in Munich. [IONOS](https://www.ionos.com/) offers dedicated GPU servers. Even smaller players like [Regolo.ai](https://regolo.ai/) provide GDPR-compliant inference with zero data retention policies.

And the models are good enough. [Mistral Large 3](https://mistral.ai/) and [Qwen 3](https://github.com/QwenLM/Qwen3) compete with proprietary models on most practical tasks. For the "boring" enterprise use cases that make up 90% of actual AI adoption (document processing, summarisation, classification, translation, code assistance), open-source models hosted in Europe do the job.

And costs of inference are dropping rapidly: [Epoch AI's research](https://epoch.ai/data-insights/llm-inference-price-trends) shows inference costs dropped 1,000x between 2021 and 2026 for GPT-3 level performance. The median decline is 50x per year, accelerating to 200x per year post-2024. GPU compute cost follows [Wright's Law](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6198738) with an 89% learning rate per doubling of cumulative production. That is faster than solar panels ever dropped (around 20% learning rate). 

## Why This Makes Sense

The logic is simple. If you already trust cloud providers to run your email, your databases, your file storage, and your business applications, then the question is not "cloud versus on-prem." The question is "which cloud provider, under which legal jurisdiction."

A European provider running Mistral or Llama under EU law gives you:

- No Chapter V transfer headaches
- No CLOUD Act exposure
- Full [EU AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) compliance (full enforcement starts August 2026)
- The same operational model your IT team already knows (APIs, managed services, SLAs)

The market agrees. [Gartner reports](https://www.intelligentcio.com/eu/2026/02/04/europe-accelerates-shift-to-region-specific-ai-platforms-amid-sovereignty-push/) that 61% of Western European CIOs plan to increase reliance on local cloud providers, and European sovereign cloud spending is projected to grow 83% year-over-year to $12.6 billion in 2026. The [Cohere acquisition of Aleph Alpha](https://www.cnbc.com/2026/04/24/cohere-aleph-alpha-germany-ai-europe-expansion.html), backed by $600 million from Schwarz Group, signals that serious money is flowing into this space.

## When This Does Not Work

Frontier reasoning tasks. If you need the absolute best model for complex multi-step reasoning, agentic coding, or cutting-edge multimodal work, US providers still lead. The gap is closing, but it exists. An interesting complication is the [recent US government blocking](https://www.washingtonpost.com/business/2026/06/26/trump-ai-openai-gpt56-sol-cybersecurity-mythos/cdd6f804-7181-11f1-8730-e7fd0e2a6404_story.html) of Fable 5 and GPT-5.6. If the American government keeps pulling its own models from the market, the "first mover" advantage disappears, and investment in open-source alternatives accelerates. But that is a topic for another post.

For most enterprise workloads though, "the best model" is not the relevant criterion. "Good enough, legally clean, and operationally simple" is. And that is where European providers are becoming competitive.

The future I see is not a binary choice between American clouds and on-prem hardware. It is trustworthy European partners that run the LLM part, just as well as the other cloud services a company needs. And as a benefit to keep going that path: the European rules are among the toughest in the world, if a company can meet them here, it is quite possible to offer these services in other parts of the world, like South America and Africa.

*Thinking about where to run your enterprise AI? <a href="#" onclick="task1(); return false;">Get in touch</a> to talk through the options.*

## Sources

- [Epoch AI: LLM inference price trends](https://epoch.ai/data-insights/llm-inference-price-trends) -- 1,000x cost reduction data
- [Wright's Law extended to GPU compute](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6198738) -- 89% learning rate vs solar's 20%
- [EU-US Data Privacy Framework](https://www.dataprivacyframework.gov/Program-Overview) -- Current legal basis for transatlantic transfers
- [GDPR and EU-US data transfers guide 2026](https://www.aigovhub.io/guides/gdpr-eu-us-data-transfers-post-schrems-ii-guide-2026) -- Post-Schrems II compliance landscape
- [EU AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) -- Full enforcement August 2026
- [Gartner: Europe accelerates sovereign AI shift](https://www.intelligentcio.com/eu/2026/02/04/europe-accelerates-shift-to-region-specific-ai-platforms-amid-sovereignty-push/) -- 61% of CIOs increasing local provider use
- [Edge AI market projections](https://www.precedenceresearch.com/edge-ai-market) -- $25B (2025) to $143B (2034)
- [Cohere acquires Aleph Alpha](https://www.cnbc.com/2026/04/24/cohere-aleph-alpha-germany-ai-europe-expansion.html) -- $20B combined valuation, sovereign AI focus
- [Deutsche Telekom Industrial AI Cloud](https://www.t-systems.com/de/en/insights/newsroom/news/ai-sovereignty-for-germany-and-europe-1124980) -- EUR1B+, 10,000 GPUs
- [OpenAI and Anthropic limit new AI models to Trump-approved customers](https://www.washingtonpost.com/business/2026/06/26/trump-ai-openai-gpt56-sol-cybersecurity-mythos/cdd6f804-7181-11f1-8730-e7fd0e2a6404_story.html) -- Washington Post on US export controls
- [VS blokkeert Anthropic Claude Fable 5 en Mythos 5](https://tweakers.net/nieuws/249082/vs-blokkeert-anthropic-claude-fable-5-en-mythos-5-vanwege-zorgen-jailbreak.html) -- Tweakers (Dutch) on the same topic
