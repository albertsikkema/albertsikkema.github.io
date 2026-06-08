---
layout: post
title: "Your AI Tests Are Probably Lying to You"
date: 2026-06-08
categories: ai development testing
description: "LLM-generated tests pass without proving anything. I built a review skill backed by test smell research to catch what green CI dashboards hide."
keywords: "test smells, rotten green tests, LLM testing, AI code generation, test quality, Claude Code, mock abuse, test review"
image: /assets/images/your-ai-tests-are-probably-lying-to-you-blog.png
---

<figure>
  <img src="/assets/images/ai-tests-lying.jpg" alt="Sunlight breaking through a dense forest, bright at the center but dark at the edges" width="1920" height="1280" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>Photo by <a href="https://unsplash.com/@ingmarr">Ingmar</a> on <a href="https://unsplash.com">Unsplash</a></figcaption>
</figure>

As you may have read in an [earlier post](/ai/llm/development/best-practices/2025/11/14/human-in-the-loop-ai-code-review.html), I do not like writing tests. So when an LLM is able to write it for me: great, I let Claude do it. In a review a colleague pointed out that two of my tests did nothing more than verify that mocks return what mocks are told to return. The tests passed, the ci passed but it mainly tested a very obvious thing. And also useless.  I read them myself three or four times and did not see it either.

That was seven months ago and it has been nagging me: how to improve tests while not spending too much time on it. After all I do rely on tests, so they have to have a certain quality. But I do not want to have to write them myself.

## Some more observations

After that happened I started looking more carefully at AI-generated tests in general. Not just mine, also in code I reviewed for colleagues, and I saw some patterns: Tests that assert a mock returns what you told it to return. Tests that wrap the assertion in a try/except so they pass even when the check fails. Tests with `if status == 200: assert ...` that silently skip when the status is something else. Etcetera.

So I went looking at what the academic world has to say about this. Of course this has been researched: ["rotten green tests"](https://dl.acm.org/doi/10.1109/ICSE.2019.00062), coined by Delplanque et al. in 2019. What it means is tests whose assertions never actually execute. The concept of "test smells" goes back even further, to [van Deursen et al. in 2001](https://www.researchgate.net/publication/2534882_Refactoring_Test_Code) and [Meszaros in 2007](http://xunitpatterns.com/). So this has been a known problem for 25 years. What is new is that LLMs produce these smells at industrial scale. (Then again the LLM's training data probably contains at least some of these badly formulated and constructed tests)

## LLM is not so good at generating tests

I spent some time going through recent studies on LLM-generated tests and the results are not encouraging.

[One study](https://arxiv.org/abs/2406.18181) tested LLMs on unit test generation across 17 Java projects. Between 34% and 62% of generated tests did not even compile. Of the ones that did compile and run, 75% of the bugs they missed were missed because the tests used boring, normal input values. The LLM picks safe values that exercise the happy path even when the code is broken. If you need to set a value to NaN or pass an empty string or hit an exact boundary to trigger the bug, the LLM will not do that. It generates the test equivalent of "hello world."

Another [survey of 115 publications](https://arxiv.org/abs/2511.21382) on LLM test generation found that the best model they evaluated detected 8 out of 163 real bugs (0.74%).

And [CodeRabbit's analysis](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) of 470 open-source PRs found that AI-co-authored code has 1.7x more issues overall and up to 2.74x more security vulnerabilities than human-written code.

Those numbers are quite high (higher than I recognise from my daily practice, but that has partly to do with the guardrails I use on every LLM interaction).

The real problem is that you can not trust your tests: LLMs often filter out failing tests before showing you results. They throw away the tests that fail (which might be the ones that actually found something) and present you tests that pass. And then teams look at "400 tests, all passing" and feel confident, which is not a confidence that is justified.

One option is to build the tests first (TDD), which works quite well and I do implement that (partly) by defining tests before the actual code is written. However I also found that the building process can only be planned to a certain extent: chaos is always looming (a package that does not work as expected, incomplete view of how the database works etc.) So while I do believe that TDD is a nice idea, I do see more productive progress in a slightly less defined and rigid way of TDD. But however you want to do this: back to the main question: how to make sure that tests are of a proper quality and test things that matter and do not test things that do not matter?

## So I Built a Thing

The idea is simple: instead of a generic "review this code" prompt (which misses test smells because it focuses on code quality, not test purpose), give the LLM a specific taxonomy of test defects to hunt for. And crucially, make it read both the test file AND the production code the test covers. You cannot judge whether a test proves anything without seeing what it is supposed to be testing. So after some research I defined several categories that are recognisable to an LLM. See the resources section below if you want to know more.

The [skill](https://github.com/albertsikkema/codebench/tree/main/.claude/skills/review-tests) checks for nine categories:

- **Rotten green tests** -- tests that pass without verifying what they claim. Tautologies, conditional assertions, swallowed errors
- **Classic test smells** -- Assertion Roulette (multiple asserts, no messages), Eager Test (one test doing too much), Mystery Guest (depends on invisible external state)
- **Mock abuse** -- so many mocks that the test is not testing real behavior anymore. If your test has more mocks than assertions, something is off
- **Contract drift** -- tests that verify internal method call order instead of observable output. These break on every refactor even when behavior stays the same
- **Missing negative paths** -- no 401 test, no 403 test, no input validation test. Every auth-protected endpoint needs these
- **LLM-generated defects** -- hallucinated APIs that do not exist in the codebase, generic-only inputs, type-not-value assertions like `isinstance(result, dict)`
- **Fixture fragility** -- tests that depend on execution order, shared mutable state, or fixtures that do too much
- **Assertion quality** -- loose assertions (`len(x) >= 1` when exact count is known), missing assertions, or ten checks on the happy path and one on the error path
- **Missing edge cases** -- empty collections, boundary values, concurrent access, cleanup after mutation

You run it like this:

```bash
/review-tests                          # review changed test files on current branch
/review-tests backend/tests/unit/      # review a specific path
```

Output is as small as possible, with one line per finding:

```
tests/test_auth.py:L42: bug: assert mock.return_value == mock.return_value. Tautology. Assert against expected value from spec.
tests/test_api.py:L18: risk: try/except catches AssertionError. Test passes on failure. Remove bare except.
tests/test_search.py:L91: gap: No 401 test for /api/search endpoint. Add unauthenticated request test.
```

## The Contradiction: LLMs can create bad tests and find them quite well

[Santana Jr et al.](https://arxiv.org/abs/2506.07594) evaluated LLMs on detecting test smells in Java projects and found detection rates up to 96% for classic smells. LLMs are better at finding test smells than rule-based tools, especially for things like Assertion Roulette and Eager Test that require understanding what the test is trying to do.

The same technology that mass-produces rotten green tests is also the best tool we have for finding them. I noticed this in practice too. Claude is most of the time pretty good at writing tests, but "pretty good" is not good enough when you need tests that catch real bugs. Left to its own devices it gravitates toward happy paths and shallow assertions. But when you give it a specific list of things to look for and force it to read the production code alongside the test, it catches things I miss. Not always, not perfectly, but consistently better than my own manual review.

## Where I Use It

I run it when i decide it is useful (large amount of tests) and as part of my automated PR review. The skill is part of [codebench](https://github.com/albertsikkema/codebench), where I collect Claude Code skills, hooks, and configuration. If you use Claude Code for test generation (and you probably do, because writing tests is boring), give it a try.

*Letting AI write your tests and wondering what slips through? <a href="#" onclick="task1(); return false;">Get in touch</a> to compare notes.*

## Resources

### Research

- [Refactoring Test Code](https://www.researchgate.net/publication/2534882_Refactoring_Test_Code) (van Deursen et al., 2001) -- The original test smells paper
- [xUnit Test Patterns](http://xunitpatterns.com/) (Meszaros, 2007) -- 68 patterns for maintainable tests
- [Rotten Green Tests](https://dl.acm.org/doi/10.1109/ICSE.2019.00062) (Delplanque et al., ICSE 2019) -- Tests that pass because their assertions never execute
- [Growing Object-Oriented Software, Guided by Tests](https://growing-object-oriented-software.com/) (Freeman & Pryce, 2009) -- Test behavior, not implementation
- [Investigating Severity Thresholds for Test Smells](https://dl.acm.org/doi/10.1145/3379597.3387453) (Spadini et al., MSR 2020) -- Not all test smell instances are equally harmful

### LLM Test Generation

- [On the Evaluation of Large Language Models in Unit Test Generation](https://arxiv.org/abs/2406.18181) (Yang et al., 2024) -- 34-62% of LLM-generated tests fail to compile; 75% of undetected defects due to missing triggering inputs
- [Large Language Models for Unit Test Generation](https://arxiv.org/abs/2511.21382) (Alshahwan et al., 2025) -- Survey of 115 publications; best model found 8 of 163 bugs
- [Evaluating LLMs Effectiveness in Detecting and Correcting Test Smells](https://arxiv.org/abs/2506.07594) (Santana Jr et al., 2025) -- LLMs detect test smells at up to 96% accuracy
- [State of AI vs Human Code Generation Report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) (CodeRabbit, 2025) -- AI-co-authored code has 1.7x more issues and 2.74x more security vulnerabilities

### Tools

- [review-tests skill](https://github.com/albertsikkema/codebench/tree/main/.claude/skills/review-tests) -- The Claude Code skill discussed in this post
- [codebench](https://github.com/albertsikkema/codebench) -- Skills, hooks, and configuration for Claude Code
- [AI Regression Testing skill](https://github.com/affaan-m/everything-claude-code/blob/main/skills/ai-regression-testing/SKILL.md) -- Community skill for AI blind spots in test generation

### Related posts

- [Human in the Loop: Why Your LLM-Assisted Code Still Needs Human Eyes](/ai/llm/development/best-practices/2025/11/14/human-in-the-loop-ai-code-review.html) -- The meta-test story that started this
- [From Prototype to Production: Automated Builds](/ai/development/automation/2026/05/23/from-prototype-to-production-automated-builds-with-codebuilder.html) -- Where automated test review fits in the build pipeline
- [Benchmarking Open-Source PII Detection](/python/security/privacy/2026/06/01/benchmarking-open-source-pii-detection.html) -- Similar approach: benchmark tools, pick the practical winner
