---
layout: post
title: "Human in the Loop: Why Your LLM-Assisted Code Still Needs Human Eyes"
date: 2025-11-14
categories: AI LLM development best-practices
description: "LLM-generated code needs human review. Real story of meta-test bugs that passed automated checks but were caught by experienced developers. Essential lessons for AI-assisted development."
keywords: "AI-assisted development, LLM code review, human in the loop, AI agent development, code quality, Claude AI development"
---

This week I was working on some code for a project that uses Python and [PydanticAI](https://ai.pydantic.dev/) to create a few agents for legal document search. But the specific domain doesn't really matter - what I want to focus on is the role of 'human in the loop' and why it's essential when working with agentic tooling to create software.

<figure>
  <img src="/assets/images/human_ai_laptop.webp" alt="Human in the Loop AI Code Review">
  <figcaption>This is what AI thinks an image for this blog should look like...</figcaption>
</figure>

## The Project: Legal Domain Search Agent

So let me explain what happened when creating the code: The idea was to create an agentic structure where the user could ask questions and the LLM would return answers solely based on the results of a search in an Azure AI Search Index and would only respond to questions in the field it was supposed to work with (in this case 'legal domain'). Seems pretty straightforward right?

There was already a chat in this project, which I built the week before, using PydanticAI. So I started to create an agentic system that took in a prompt from the user, and then it had access to a search index (I created a tool for the agent to do that) so it could do a search. But as you can probably guess: the issue here is how to get the agent to actually use the search. Because what I did not want to happen was that the agent would answer without searching, relying on its general knowledge (which is vast, but not always returns specific enough answers, let alone correct ones). And of course it did use its general knowledge more than it did the search tool.

So what to do? First I started with revising the prompt to make it more strict in using the search tool, with reasonable results. I needed more insight in what exactly happened with the prompts and LLM calls, so I added a proper monitoring tool ([Phoenix Arize](https://github.com/Arize-ai/phoenix), opensource and runs on your own hardware, ideal for privacy sensitive projects as the one I was working on. I'll write another blogpost about monitoring of LLM calls soon, it is an interesting subject with as of late great tools to help you.) That improved the situation quite well, not perfect but there was progress. And good enough for now. Let's move on.

## Adding Intent Classification

The next problem to tackle: only answer questions related to 'legal domain'. This can get quite complicated, but the first goal is to get it running. We'll deal with the complexity later. So given that this chat was supposed to only respond to questions related to legal subjects, it was not doing what it should do: You could answer questions about 'why are trees green?' and it would answer. So I added another step in the process: an agent that would try to determine the intent of the question: if it was a legal question it should continue, if it was not or unclear it should return an appropriate answer, like 'I only know stuff about laws, please ask me a better question', but then of course more user friendly. Implemented that, and it worked.

Great. So the code changes became quite complex, and to be honest a little bit too big for one PR. But I went over it again, used my agentic code review tools and saw that it was good (enough) to have it reviewed by my colleagues. You have to realize here that the tools I use ([see my repo](https://github.com/albertsikkema/claude-config-template)) with Claude Code are quite extensive: before I have the PR reviewed, it is checked several times by the LLM. And over the months that I use this system and improve it, I see better and better results. So as always I did another manual read and asked for reviews.

## The Discovery: Meta Tests Testing Tests

So some time later the reviews came in from two of my colleagues: some good things, some things that need to be improved. Most were expected, some things to consider for the future. But one reviewer was very thorough and saw some of my tests (as you may have read in my earlier blogs, I hate writing tests. So I leave that to Claude.) and concluded that two of my tests did nothing more than testing if the tests existed and worked. Which is about as meta as it gets. Something like this:

```python
def test_intent_classifier_exists():
    """Test that the intent classifier test exists."""
    assert callable(classify_intent)
    assert True  # Test passes if we got here

def test_search_tool_works():
    """Test that search tool test works."""
    mock_search = MagicMock(return_value="results")
    result = mock_search("query")
    assert result == "results"  # Just testing the mock works
```

So the agents went over it several times and did not recognize it as strange tests. And I went over it (I must have read that at least two times, but probably 3 to 4 times) and did not see it. And a tool we use for code review in the pipeline did not see it. But a human with enough knowledge did.

## Does It Really Matter?

Now does this really matter: a few tests that test whether a test works? Not really. You could argue that it pollutes the codebase (true), is unnecessary (true) and even bad for the environment (because extra CPU cycles, thus extra energy, thus not environment friendly) and more costly (same reason, more energy, more cost). But it makes clear that you can not trust the LLM at all times (and you should never), but also that you yourself can not be trusted.

Compare it to driving a Tesla: the assistant helps you, but you are expected to keep your eyes on the road. But everyone starts to be tired, bored and you start missing things. With potentially dangerous situations. [NHTSA found that Tesla Autopilot was linked to hundreds of collisions](https://www.cnbc.com/2024/04/26/tesla-autopilot-linked-to-hundreds-of-collisions-has-critical-safety-gap-nhtsa.html), identifying a "critical safety gap" where driver inattention was a major factor. In many cases, drivers had their hands off the wheel for extended periods because they trusted the system too much.

The same principle applies to AI-assisted coding: over-reliance without active supervision leads to problems slipping through. And that is the real challenge for developers: how not to get bored. This boredom comes from two sources: first, reading code you didn't fully write yourself - you miss the actual connection with code you created from scratch. Second, reviewing other people's code that wasn't completely written by them either. It's a fundamentally different relationship with the codebase, on both sides of the review process.

## Lessons from the ICU

I have worked in multiple industries and spent about 10 years working as an ICU nurse. One thing I learned there is not to trust my own knowledge and skills for the full 100%. Trust in yourself, but always verify: check yourself, let your colleagues check you and learn from mistakes. In healthcare, this is formalized through protocols and training, resulting in a culture where errors are catched early and the organisation learns from its mistakes. Even the most experienced doctors use checklists, because human memory and attention are fallible.

So what have I learned from this story? Humans in the loop are essential for this kind of development cycle: sometimes you have read the same piece of code so much, that you no longer see the discrepancies. And apparently the LLMs do not see them either (at least not this kind of meta stuff). So what helps: leave the code for 24 hours and come back to it. The structure will still be clear in your head, but there is enough time and distance between you and the code to look at it with a fresh set of eyes and ideas. And have your colleagues check.

## The Economics of Human Review

The problem with human in the loop is that it will become one of the more expensive parts of writing software: the time it takes to do a good review is substantial and eats into the profit margin of a project. So we will see more and more automated reviews, which is not necessarily a bad thing, but a fresh set of human eyes with extensive knowledge of writing and maintaining software will still be needed!

The economics are interesting:
- **LLM code generation**: Costs cents per thousand tokens, generates code in seconds
- **Automated review tools**: Run in CI/CD pipeline, costs minimal
- **Human code review**: 30-60 minutes per PR, at senior developer rates (€ or $100-150/hour)

This creates pressure to reduce human review time. But as my experience shows, there are certain classes of errors - especially logical contradictions and meta-level mistakes - that both LLMs and automated tools miss. So the question isn't whether to use human review, but **where** to apply it most effectively. And how to change the process of writing software to optimise for that.

## Finding the Balance

The combination of tools, LLMs and human review works:

1. **LLM generates code** - Fast, handles boilerplate, follows patterns
2. **Automated tools check** - Linting, type checking, security scanning
3. **LLM reviews** - Catches obvious issues, suggests improvements
4. **Human reviews** - Catches logical errors, architectural issues, meta-problems
5. **Fresh eyes after 24h** - You catch your own mistakes

The key is accepting that each layer catches different types of problems. The meta-test issue? Only caught by a human who understood the *purpose* of tests, not just their *syntax*.

## Conclusion

LLMs are powerful coding assistants, but they're assistants, not replacements. AI-assisted development requires engaged human oversight. The most effective approach combines the speed of AI with the insight of experienced developers.

And if you're using LLM-generated tests like I do: maybe give those an extra careful look. You might find they're testing that tests test tests.

## Resources

### PydanticAI & Agents
- [PydanticAI Documentation](https://ai.pydantic.dev/) - Official PydanticAI docs
- [Building AI Agents with PydanticAI](https://docs.pydantic.dev/latest/concepts/ai/) - Pydantic's AI concepts

### LLM Monitoring
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) - Open-source LLM observability

### Code Review & Quality
- [Google's Code Review Developer Guide](https://google.github.io/eng-practices/review/) - Industry best practices
- [Code Review Best Practices](https://github.com/thoughtbot/guides/tree/main/code-review) - Thoughtbot's guide

### AI Safety & Human Oversight
- [Pair Programming with AI](https://martinfowler.com/articles/exploring-gen-ai.html#memo-03) - Martin Fowler's take

---

*Have you caught similar meta-bugs in LLM-generated code? How do you balance automation with human review? I'd love to hear about your experiences—connect with me on [LinkedIn](https://www.linkedin.com/in/albert-sikkema/).*
