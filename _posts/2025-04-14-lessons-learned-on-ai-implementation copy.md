---
layout: post
title: "Lessons Learned from Implementing AI (Part 1)"
date: 2025-04-14 15:53:00 +0200
categories: blog
description: "Real-world lessons from enterprise AI implementation projects. Learn ethical, organizational, and technical best practices for production-ready AI systems."
keywords: "AI implementation, enterprise AI, LLM integration, production-ready AI, AI best practices, prompt engineering"
---

# Lessons Learned from Implementing AI

Over the past few years, I’ve worked on multiple projects involving large language models (LLMs). Some of these were research-based, focused on identifying practical use cases within complex environments such as national governments and large enterprises. Others were very practical. The challenges we encountered spanned ethical, organizational, and technical dimensions.

In this (likely to be a series) I’ll dive into key lessons learned from real-world projects. The examples are anonymized to ensure privacy, but the insights are as authentic as they come. 

---

## Navigating Ethical Considerations

Ethical challenges were always at the forefront. These included:

- How do we ensure privacy and compliance with data protection laws?
- What are the implications of copyright in an AI-generated world?
- Can we use LLM's since they are trained on copyrighted materials and the law (EU/NL) prohibits us from using those?
- Can we trust an LLM to give consistent answers?
- What’s the environmental impact of deploying and using large models?

Many of these questions don’t have clear answers, but they require continuous evaluation and transparency to responsibly deploy AI technologies.

---

## Organizational Barriers to Adoption

Implementing LLMs in large organizations revealed typical barriers that accompany any innovation:

- Bureaucracy and slow decision-making.
- Diverse stakeholder concerns (legal, security, IT, management).
- Fear of the unknown: “Will AI make my job obsolete?” or “What if it fails?”

Understanding these dynamics is crucial. Building empathy helps: resistance often comes from very valid concerns that need to be adressed and solved.

---

## Technical Implementation Challenges

On the technical side, things get complex very fast. Some of the most pressing challenges were:

- Scaling LLM systems throughout an organization.
- Running LLMs on-premises or in a private cloud environment.
- Keeping the data sources up to date.
- Enforcing proper data access controls.
- Integrating new AI workflows into existing IT infrastructure.

The tech stack must evolve alongside strong governance practices to maintain control and ensure performance.

---

## Practical Lessons Learned

Here’s a collection of lessons learned from day-to-day practice. These are in no particular order of priority, but they each made a substantial difference.

### 1. Clarify Internal Processes First

Before diving into AI, make sure organizational procedures and standard operating procedures (SOPs) are clearly defined. This helps you understand the business context, and speak the same language as stakeholders.



### 2. Start Small and Scale Gradually

Don’t try to tackle everything at once. You will fail. Focus on solving one problem at a time. For example: 

> Instead of indexing all documents in an enterprise, start with a well-defined, small subset.

Once you prove value and involve stakeholders early, enthusiasm and momentum will follow. Plan ahead for scaling, but don’t let that delay your initial deployment.



### 3. Stay Goal-Oriented

It’s easy to lose track of the original objective in the complexity of AI systems. Stay focused on what you're trying to achieve and align every iteration toward that goal.



### 4. Manage Stakeholder Expectations

Getting stakeholders excited is crucial — but be aware that enthusiasm can lead to unrealistic expectations and tight deadlines. Balancing excitement with realistic roadmaps is a critical skill.



### 5. LLMs Are Not Trustworthy by Default

LLMs generate fluent and convincing text, texts never express doubts, concerns or 'grayness', everything is black and white— but that doesn’t make their output reliable and certainly does not mean the output is the truth. Here’s how to reduce the risk of misinformation:

- Train users not to assume the LLM is always right.
- Design UI to reflect uncertainty or lack of truth.
- Always show the source of information, especially in Retrieval-Augmented Generation (RAG) systems.



### 6. Avoid Anthropomorphizing the AI

Remember: an LLM is not a person. It does not think, feel, or understand. Use “it” — not “he,” “she,” or “they” — when referring to an LLM. Avoid giving it a personality or implying agency. This helps users maintain a realistic view.

> Anthropomorphism is the attribution of human characteristics to non-human entities. Don’t fall into this common trap.



### 7. Latency: A Hidden UX Challenge

Waiting 10 seconds (or more) for a model to respond is not uncommon. If you're deploying agents (As you understand, I have some reservations with the word 'agent', given the previous point) that delay might increase. From a UX perspective, this is significant.

- Consider how to make the wait time feel acceptable.
- Use progress indicators or transparency to show what's happening.
- Always ask yourself: could traditional business logic solve this faster?

It’s worth asking multiple times whether AI is the right tool for this job.

> It is interesting to realise that over the last decades loads of code was written and rewritten to shave off every (sub)millisecond to optimise user experience. Now we work with latencies that are measured in multiple seconds. It does make you wonder why we accept this. And for you as a developer or product owner this should make you think about whether an LLM interaction or an 'Agent' is really a better solution than some old fashioned logic which probably is much faster.



### 8. Be Mindful of Environmental Impact

LLMs consume massive computational resources. Just running a single query engages high-performance hardware — multiplying the energy cost far beyond traditional database searches.

Always ask: is an LLM necessary here, or is there a greener route?



### 9. Understand the Limits of “Agents”

AI agents (BTW 'AI agents' is a terrible choice of words, but we'll go with it, given that this term is used a lot nowadays) can be helpful, but they are far from a human replacement:

- Agents are good at performing narrowly defined tasks — but don’t expect improvisation or contextual understanding.
- Agent output is probabilistic and can vary, unlike deterministic code.
- Complexity increases with each agent added.

Keep things simple. Begin with one agent and understand the maintenance and value before scaling up.



### 10. Prompt Engineering Is an Art (more or less)

Crafting good prompts takes continuous iteration and experimentation. Tips:

- Provide plenty of examples.
- Be mindful of the structure — key info often performs best near the end.
- Test relentlessly and adjust.



### 11. Test Early, Test Often

Like any software feature, LLM integrations need thorough testing. The sooner you build in test cases, the easier your life will be when your go-to model gets deprecated or replaced.



### 12. Educate Your Clients

Make sure clients know:

- How LLMs work.
- What they’re good at.
- Where they fall short.

This empowers clients to ideate and collaborate effectively.



### 13. Don't Fear the Model Cost

Yes, tokens cost money — but if your AI solution saves a person 15 minutes of work, the ROI is easy to justify. Keep cost in perspective relative to time and value saved.

---

## Wrapping Up

That’s enough for today — and we’ve only scratched the surface. If there’s one takeaway, it’s this: AI implementation isn’t about technology alone. It’s a delicate balance of people, process, ethics, and architecture.

I’ll share more soon in the next part of this series. Stay tuned!

---