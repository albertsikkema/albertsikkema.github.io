---
layout: post
title: "Code Quality Tools: What the Research Supports"
date: 2026-06-13
categories: development quality research
description: "I reviewed research on 13 code quality methods. The ones with strongest evidence are not the ones most tools focus on."
keywords: "code quality, SonarQube, CodeScene, code metrics, cyclomatic complexity, cognitive complexity, software engineering research, defect prediction, technical debt"
image: /assets/images/code-quality-research-blog.png
---

Over the past year I have been working on tooling to improve code quality. That starts with one question first: what constitutes good code? I am a pragmatist, not a purist. Good code in my book is code that the user is happy with (it does what is expected both in use and in function), that is secure and that is easy to maintain. 

So how do we measure this? User happiness: just ask for it, and measure some statistics. Security: be diligent and complete (and a bit obsessive), if needed do an audit. But what about maintainability? The goal is to make sure code is maintainable by adhering to a certain minimal standard, enabling developers and LLM's to work faster, create better code and features more easily and create a better guardrail for code quality assurance. 

In order to do that you need to know what works and what does not. What is a marketing hype? What is actually proven to work? Which methods of analysis can be trusted to use as a gate and which are at best an indicator? So I started by implementing what I already knew and some preliminary research which resulted in about 10 methods that I integrated into an mcp server: works fine, and it helps me tremendously to get a quick overview over a codebase, pointing out weaknesses. But at a certain point you keep adding tools and start wondering: do they actually add value to this analysis? The internet is full of tools (like CodeScene and SonarQube) that claim to help, but they all have a slightly different approach.

Given the increased complexity of my tool (and thus the analysis results) and that I plan to also implement the tool I build in CI/CD pipelines, I need to make sure that what I create makes some sense. So before writing any more code for that, I wanted to know: which code quality methods are backed by real evidence? Which ones sound scientific but are not? I get a lot of flagged problems, how to prioritise them? If some of those methods do not have enough grounding, I can delete them. And perhaps it will also tell something about paid options and their credibility and usefulness given costs.

I spent some time over the last months researching this, thinking this would be a solid field where methods would have proper evidence. What I found surprised me: the methods most tools focus on (complexity metrics, code smells, coupling scores) have weaker evidence than you would think.

This post is about the research, not the tools or the implementation. I want to lay out what I found so you can decide for yourself what is worth paying attention to.

Caveat: I am not an expert at code review methods (after all that is why I started this research). Please take it as such: I did my best to not miss any important papers, but if I have, please let me know.

## What Is "Quality Code" Anyway?

Before diving into which measurement methods work, it helps to define what we are trying to measure, which is quite hard. Fortunately (or not entirely coincidental) my simple definition of what quality code is, resonates in the more official definitions.

[Garvin (1984)](https://en.wikipedia.org/wiki/Software_quality), adapted to software by Kitchenham and Pfleeger, identified five competing views of quality:

1. **Transcendental**: "I know it when I see it." Recognizable but indefinable.
2. **User-focused**: fitness for purpose. Does it solve the problem? ([Juran](https://en.wikipedia.org/wiki/Joseph_M._Juran)'s "fitness for use")
3. **Manufacturing**: conformance to requirements and specifications.
4. **Product-based**: measurable through inherent properties (complexity, coupling, duplication).
5. **Value-based**: quality relative to cost. Different stakeholders weight it differently.

Most arguments about code quality are people talking past each other across these views. A [SonarQube](https://www.sonarsource.com/products/sonarqube/) dashboard is view #4. A user who says "it works fine" is view #2. A manager asking "is it worth fixing?" is view #5.

The current international standard, [ISO/IEC 25010 (2023)](https://quality.arc42.org/standards/iso-25010), defines nine product quality characteristics: functional suitability, performance efficiency, compatibility, interaction capability, reliability, security, maintainability, flexibility, and safety. That is a useful checklist, but we can not use it to measure the code directly. What matters for this post is the causal chain it formalizes, originally from [McCall (1977)](https://www.geeksforgeeks.org/software-engineering/mccalls-quality-model/) and codified in [ISO 9126 (2001)](https://en.wikipedia.org/wiki/ISO/IEC_9126): internal quality (static code properties like complexity and coupling) *influences* external quality (runtime behavior like reliability and performance), which influences quality in use (actual user outcomes). Internal quality is necessary but not sufficient. Perfectly structured code that solves the wrong problem is still low quality. But you have to start somewhere, so let's assume the external quality and usage quality are covered.

<figure>
  <img src="/assets/images/code-quality-research-causal-chain.svg" alt="Causal chain: Internal Quality influences External Quality influences Quality in Use" width="1180" height="380" loading="lazy" style="width:100%;height:auto">
  <figcaption>The ISO 9126 / McCall causal chain. Code quality tools measure the left box only.</figcaption>
</figure>

The measurement methods I evaluate try to measure internal quality through code properties (a.o. complexity, coupling, duplication, churn patterns) and use those as proxies for maintainability. They do not measure whether users are happy or whether the software solves the right problem. That is an important limitation to keep in mind: even if every metric below worked perfectly, it would only cover one dimension of quality.

## The Setup

I looked at 13 different analysis methods that I either already built or considered building: hotspot analysis, code ownership, code smells, cognitive complexity, deep nesting, temporal coupling, duplicate code, coupling metrics, composite health scores, static analysis gates, function length, error handling analysis, and circular dependencies. For each one I collected supporting evidence and counterarguments from peer-reviewed papers.

These methods serve two different purposes. Some try to find specific bugs (static analysis catching a null dereference). Others assess code properties that make maintenance harder or easier (complexity, coupling, smells). Both matter for maintainability and code quality.

So for each method below I look at both: does it help find or predict bugs, and does it give useful insight about maintainability? Then I weigh whether it is worth keeping in a tool.

## The Methods

### Hotspot Analysis (Change Frequency x Complexity)

The idea: files that change often AND are complex are where your problems live. [Nagappan and Ball (2005)](https://dl.acm.org/doi/10.1145/1062455.1062514) showed that relative churn (normalized by component size) discriminated fault-prone binaries at 89% accuracy on Windows Server 2003 (I had that version running once, that is rather long ago). Raw commit counts are useless; you have to normalize.

[Tornhill and Borg (2022)](https://dl.acm.org/doi/10.1145/3524843.3528091) found that low-quality code (identified via hotspot analysis) contains 15x more defects and takes 124% longer to work on. This was across 39 proprietary codebases, peer-reviewed at IEEE/ACM TechDebt 2022. Tornhill is the founder of [CodeScene](https://codescene.com/), the tool that implements this approach. The research was done on CodeScene customers.

There is a deeper question though. The "complexity" half of hotspot analysis might just be measuring lines of code. Cyclomatic complexity, introduced by [McCabe in 1976](https://en.wikipedia.org/wiki/Cyclomatic_complexity), counts the number of independent paths through a function: every `if`, `for`, `while`, or `case` adds one. The idea is that more paths means harder to test and more likely to contain bugs. It is probably the most widely used complexity metric in the industry. But [Jay et al. (2009)](https://www.researchgate.net/publication/220204439) showed that cyclomatic complexity has "absolutely no explanatory power of its own" beyond LOC. The correlation between code complexity and lines of code is so stable across languages and paradigms that they are effectively measuring the same thing.

**Verdict: positive.** Be aware the complexity half may just be measuring size, but enough evidence to actually use it.

### Code Ownership and Knowledge Distribution

[Bird et al. (2011)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/bird2011dtm.pdf) studied Windows Vista and Windows 7 and found that components with many low-expertise contributors had significantly more defects. Removing ownership features from their prediction model dramatically decreased performance, confirming that ownership is a genuine signal, not a proxy for something else.

This has been replicated across multiple Microsoft products and open-source projects. [Thongtanunam et al. (2016)](https://dl.acm.org/doi/abs/10.1145/2884781.2884852) found that code review partially mitigates the ownership effect but does not eliminate it.

The counterargument: shared files may be inherently harder (more complex, more integration-heavy), and that is why many developers touch them. Correlation, not causation. And [bus factor](https://en.wikipedia.org/wiki/Bus_factor) (the number of people who would need to disappear before nobody understands a piece of code) is a lagging indicator. By the time you measure that only one person knows how the billing module works, you are already in trouble if that person leaves.

**Verdict: positive.** Strongest evidence alongside hotspot analysis. Also a direct maintainability signal: knowing where knowledge is concentrated tells you where onboarding is most critical and where your team is most vulnerable.

### Cognitive Complexity

[SonarSource's cognitive complexity](https://www.sonarsource.com/resources/cognitive-complexity/) (the metric behind SonarQube rule S3776) is probably the most widely deployed complexity metric today. And it does correlate with perceived understandability. [Munoz Baron et al. (2020)](https://arxiv.org/pdf/2007.12520) confirmed this, and [Lenarduzzi et al. (2023)](https://arxiv.org/abs/2303.07722) found it slightly outperforms cyclomatic complexity for readability.

However it has not been validated as a defect predictor. "Harder to understand = more bugs" sounds logical, but nobody has proven this for cognitive complexity specifically. And it inherits the same fundamental critique as cyclomatic complexity: [Shepperd (1988)](https://www.semanticscholar.org/paper/A-critique-of-cyclomatic-complexity-as-a-software-Shepperd/a4b522d7d55c0ed38c825c4fb9fe28c14d659c0a) showed that CC is "based upon poor theoretical foundations" and is "no more than a proxy for, and in many cases is outperformed by, lines of code."

So cognitive complexity tells you something about readability as a formula approximates it, not necessarily how a human developer perceives the code. And it is worth noting the difference: when [Buse and Weimer (2010)](https://www.semanticscholar.org/paper/Learning-a-Metric-for-Code-Readability-Buse-Weimer/1a2b8aa0ed7f24ca001508654f506ea010b18a5e) had 120 human annotators rate code readability, that *did* correlate with fewer defects. But that is human perception, not a formula counting nesting levels and branch points. Cognitive complexity claims to approximate what humans perceive, but the evidence that it actually does so well enough to predict outcomes is surprisingly thin for something so widely adopted.

**Verdict: positive.** Weak as a defect predictor, but the maintainability value is clear. A function with a score of 47 is harder for a new team member to understand than one scoring 8.

### Deep Nesting

Nesting depth (how many levels of `if`/`for`/`while` are stacked inside each other) consistently correlates with fault rates. [Hatton (1997)](https://en.wikipedia.org/wiki/Les_Hatton) identified it as one of the most important dimensions that account for defect variability. It is more reliable than function length as a standalone metric.

But it is confounded with function length: deeply nested code is usually in long functions. [El Emam et al. (2001)](https://ieeexplore.ieee.org/document/935855) showed that after controlling for size, many metrics lose significance, and nesting may be one of them. There is also no evidence that *reducing* nesting (via early-return refactoring, for example) improves outcomes. You can scatter logic across more exit points and reduce the measured nesting without making the code any clearer.

**Verdict: positive.** The bug-prediction evidence is weakened by El Emam's finding that nesting may just be a size proxy. It does not predict bugs better than LOC does. But deeply nested code is usually in long functions, and long functions do have more bugs, so the correlation comes along indirectly through size. As a maintainability signal it is more defensible: deeply nested code is genuinely hard to follow regardless of whether it independently predicts defects. Threshold-based (flag anything beyond 3-4 levels) is more useful than continuous measurement. Good supporting signal, not a primary one.

### Code Smells

"God class" and "long method" have consistent defect correlation across studies. [Palomba et al. (2018)](https://link.springer.com/article/10.1007/s10664-017-9535-z) found that "the great majority of analysed research papers found a positive correlation between code smells and software bugs."

[El Emam et al. (2001)](https://ieeexplore.ieee.org/document/935855) placed that into perspective 17 years earlier: out of 24 OO metrics examined, only 4 retained any relationship to faults after controlling for class size. Large classes have more bugs because they have more code. The smell may just be a proxy for size. (more code, more bugs --> makes sense)

[Sharma and Spinellis (2018)](https://www.semanticscholar.org/paper/A-survey-on-software-smells-Sharma-Spinellis/6fa6e56c6d57efd5e0fbbe61093c0a0bd32f73cc) surveyed the full landscape of smell research, and the evidence per smell type varies a lot. Feature envy (a method that uses another class's data more than its own) shows weaker and less consistent results. Long parameter list has almost no empirical support. Duplicated code gets the most research attention but its link to defects is debated (see duplicate code below). [Fowler's original catalog](https://refactoring.guru/refactoring/smells) includes more exotic smells (message chains, middle man, speculative generality), but [Khomh et al. (2012)](https://link.springer.com/article/10.1007/s10664-011-9171-y) only found that smell-affected classes are more change-prone as a group. That broad finding does not tell you which specific smells drive the effect, and the exotic smells have neither defect evidence nor clear maintainability benefits.

As maintainability indicators, the well-evidenced smells have direct value. A god class is hard to modify regardless of whether it contains bugs. The change-proneness finding from Khomh supports this: smell-affected classes get modified more often, which means developers spend more time on them. That is a maintenance cost even if it never produces a bug.

Smell detectors tend to produce a lot of noise. [Bessey et al. (2010)](https://dl.acm.org/doi/10.1145/1646353.1646374), writing from Coverity's experience analyzing billions of lines of production code, found that false positives kill adoption. Users prefer fewer true findings over wading through noise.

**Verdict: positive for god class and long method,** which have both defect correlation and clear maintainability value. **Negative for exotic smells** (message chains, middle man, speculative generality), which have neither proven defect prediction nor demonstrable maintainability benefits.

### Temporal Coupling (Co-Change Analysis)

Files that consistently change together may have hidden dependencies that structural analysis misses. [D'Ambros et al. (2009)](https://dl.acm.org/doi/10.1109/WCRE.2009.5070547) found that change coupling correlates with defects across three large open-source systems. [Canfora et al. (2014)](https://www.sciencedirect.com/science/article/abs/pii/S0164121214000351) found 64-93% of defects in classes with Granger-positive results.

But temporal coupling is noisy. Bulk refactoring, API changes, and rename commits produce false positives. Results are system-dependent: what works for one project may not work for another. It needs aggressive filtering (minimum commit threshold, maximum files per changeset) to be useful.

**Verdict: positive.** Unique signal that no other method provides (hidden dependencies), but noisy as a standalone predictor. For maintainability, knowing which files are secretly coupled is valuable for planning refactors. Filter aggressively, present as "hidden dependency finder."

### Duplicate Code

[Juergens et al. (2009)](https://dl.acm.org/doi/10.1109/ICSE.2009.5070547) found that 52% of clones were inconsistently changed and 15% of those inconsistencies caused faults. [Bettenburg et al. (2012)](https://www.sciencedirect.com/science/article/pii/S0167642310002091) found only 1-3% of inconsistent changes introduce defects. And [Rahman et al. (2012)](https://link.springer.com/article/10.1007/s10664-011-9195-3) found that clones may actually be *less* defect-prone than non-cloned code, possibly because cloned code tends to be simpler boilerplate.

**Verdict: positive.** Not a defect predictor, but genuinely useful for maintainability: when you fix a bug in one copy and forget the other three, that is a real maintenance problem. The value is in reducing the surface area of future changes, not in predicting where bugs are today.

### Coupling Metrics

Coupling measures how much one piece of code depends on other pieces. [Robert C. Martin](https://condor.depaul.edu/dmumaugh/OOT/Design-Principles/oodmetrc.pdf) proposed a framework that counts incoming dependencies (how many other modules use this one) and outgoing dependencies (how many other modules this one uses) to calculate an "instability" score. Theoretically clean. But [Al Dallal (2013)](https://www.researchgate.net/publication/31598248_A_Validation_of_Martin's_Metric) found "a lack of theoretical and empirical evaluation." The older [Chidamber-Kemerer metrics](https://en.wikipedia.org/wiki/Programming_complexity#Chidamber_and_Kemerer) from 1994, particularly their "coupling between objects" metric (simply counting how many other classes a class is connected to), have much better empirical validation. Martin's metrics add little over that simpler measure. And as we found before, coupling metrics might just be proxies for LOC.

**Verdict: positive.** Weak for defect prediction, but hard to dismiss as a maintainability indicator. A module with 30 incoming dependencies is risky to change because any modification can break 30 other places. That is not about bugs, it is about change impact. Simple coupling counts (CBO) are sufficient; the fancier frameworks add little.

### Composite Health Scores

[CodeScene](https://codescene.com/) assigns a 1-10 "code health" score. The general principle (combining multiple metrics beats a single metric) is well supported. And Tornhill and Borg's 15x defect rate difference is real.

But what does "7.2 health" mean? [Fenton and Pfleeger (1997)](https://dl.acm.org/doi/10.5555/580949) point out that combining things measured on different scales (readability, coupling, churn) into one number violates measurement theory. It is like averaging temperature, wind speed, and humidity into a single "weather score." You get a number, and it looks scientific, but what does it actually tell you? It seems like simplification taken too far.

**Verdict: negative.** Neither a reliable defect predictor nor a useful maintainability signal on its own, because it hides which dimensions are actually suffering. The principle of combining signals is sound, but a single number is not actionable. Better to show the individual signals and let the reviewer decide.

### Static Analysis Quality Gates

Static analyzers scan source code without running it, looking for patterns that are known to cause problems. Like using a variable before it is initialized, a null pointer dereference, a SQL query built from unsanitized user input, a resource opened but never closed. Tools like [SonarQube](https://www.sonarsource.com/products/sonarqube/), [ESLint](https://eslint.org/) (JavaScript), [Pylint](https://pylint.readthedocs.io/) (Python), [SpotBugs](https://spotbugs.github.io/) (Java), and [CodeQL](https://codeql.github.com/) (GitHub's query-based static analyzer) all fall in this category. Most work by matching code against a database of known-bad patterns, though some (like CodeQL) do more sophisticated data flow analysis.

77% of projects use at least one according to [Beller et al. (2016)](https://azaidman.github.io/publications/bellerSANER2016.pdf). The economic argument is that it is cheaper to fix early, even with low recall. Many teams use them as quality gates in CI/CD: the build fails if the analyzer finds issues in new code.

But how low is that recall? [Habib and Pradel (2018)](https://www.semanticscholar.org/paper/How-Many-of-All-Bugs-Do-We-Find-A-Study-of-Static-Habib-Pradel/72e779539de6a5f9c4d30e512ea9ca4688e02c6a) found that static bug detectors miss the large majority of bugs. Different tools are mostly complementary, each finding different things. A clean report means nothing was found within that tool's capabilities, not that the code is correct. [Dijkstra (1969)](https://en.wikipedia.org/wiki/Edsger_W._Dijkstra) said it decades ago: testing (and analysis) can show the presence of bugs, never their absence.

**Verdict: positive.** This is the one method that actually finds specific bugs rather than measuring code properties. Low recall, but what it catches is real. The economic argument holds: even catching 10% of bugs early is cheaper than finding them in production. Just do not pretend a clean report means the code is correct.

### Function Length

Size correlates with total defect count. But it does NOT reliably predict defect density (bugs per line). And since LOC and cyclomatic complexity are linearly related, measuring both is measuring the same thing twice.

**Verdict: negative.** Does not predict defects beyond what LOC already tells you, and does not add maintainability insight beyond what complexity and nesting already capture.

### Error Handling Analysis

Checking for bare except blocks, swallowed errors, ignored error returns (Go's unchecked `err`), `.unwrap()` in non-test Rust code, `await` without try/catch. These are widely accepted as defects or at minimum bad practice.

There is no large-scale empirical study quantifying defect rates from specific error handling patterns. But the face validity is high: an ignored error return in Go is a bug waiting to happen, and the false positive rate is low when patterns are well-defined. The limitation is that these checks only catch *absent* error handling, not *incorrect* handling (wrong recovery action).

**Verdict: positive.** Limited academic validation, high practical value. Low false positive rate makes it safe to flag. Both a bug finder (swallowed errors are real bugs) and a maintainability signal (code that ignores errors is fragile).

### Circular Dependencies

Circular imports make refactoring, testing, and deployment harder. Detection via DFS on the import graph is deterministic with zero false positives.

But there is limited empirical evidence directly linking cycles to defects. Small cycles may be benign. And this only addresses accidental complexity: fixing a circular dependency does not fix the underlying design problem that caused it.

**Verdict: positive.** Zero false positives makes it safe to always flag. Not a defect predictor, but a clear architectural health signal. A codebase with circular dependencies between major modules is harder to maintain and harder to test in isolation.

## The Elephant in the Room: Everything Might Just Be LOC

This is the single most damaging critique in the field, and it applies to almost everything above.

[El Emam et al. (2001)](https://ieeexplore.ieee.org/document/935855) tested 24 object-oriented metrics and found that most lost their relationship to faults after controlling for class size. [Jay et al. (2009)](https://www.researchgate.net/publication/220204439) showed that cyclomatic complexity has "absolutely no explanatory power of its own" beyond lines of code. [Graves et al. (2000)](https://ieeexplore.ieee.org/document/885631) found that when LOC is included, complexity metrics add nothing to fault prediction.

The implication is if LOC predicts defects as well as your 47-metric dashboard, your dashboard is an expensive LOC counter with a nicer UI. Any metric that claims to be useful must demonstrate predictive power *after controlling for size*.

## The Counterarguments That Apply to Everything

Beyond the LOC problem, there are critiques that cut across all methods. I collected them separately because they are worth reading as a group.

**Goodhart's Law.** "When a measure becomes a target, it ceases to be a good measure" ([Strathern, 1997](https://jellyfish.co/blog/goodharts-law-in-software-engineering-and-how-to-avoid-gaming-your-metrics/)). Developers split functions to hit a complexity threshold without improving readability. Code coverage targets lead to trivial tests. Any metric feeding into performance reviews will be optimized for the metric, not quality. (this I recognise from daily practice: a gate states that a function is too complex, so I rewrite it to pass the gate, but often that is a tradeoff on other areas)

**The Halstead cautionary tale.** [Halstead (1977)](https://en.wikipedia.org/wiki/Halstead_complexity_measures) proposed metrics based on operator/operand counts that were widely adopted in tools and standards. Then [Shen et al. (1983)](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1302&context=cstech) debunked them: conclusions based on sample sizes less than 10, core assumptions violated, conceptual errors. Metrics can be widely adopted and still be scientifically invalid. Adoption is not validation.

**Models do not transfer.** [Briand et al. (2002)](https://www.sciencedirect.com/science/article/abs/pii/S0164121200000868) showed that fault-proneness models built on one project often do not transfer to other projects. Default thresholds in any tool are starting points, not universal truths.

**False positives kill adoption.** [Bessey et al. (2010)](https://dl.acm.org/doi/10.1145/1646353.1646374) again: users prefer fewer true findings over completeness. Their finding was that developers do not care about missed bugs nearly as much as they hate false positives. A false positive wastes your time right now, a false negative is invisible: you cannot be annoyed by a bug the tool never reported. After enough false alarms, developers stop checking findings entirely, and then even the true positives get ignored. Higher precision means some real issues slip through, but a tool nobody trusts has no use at all.

**Only accidental complexity is addressable.** [Brooks (1986)](https://worrydream.com/refs/Brooks-NoSilverBullet.pdf) distinguished essential complexity (inherent in the problem) from accidental complexity (artifacts of tools and languages). Code quality tools can only address the accidental kind. Design and requirements are where most difficulty lives. No tool changes that.

**DeMarco's nuance.** Tom DeMarco claimed "you cannot control what you cannot measure" in 1982. In [2009](https://ieeexplore.ieee.org/document/5076468/) he revisited that position, writing that his earlier work "made the suggestion that metrics are good and therefore more metrics would be better." He did not reject metrics entirely, but argued that the most important software projects are transformational, and transformation cannot be measured or controlled in advance.

## So What Do I Do With All This?

Looking at all 13 methods through both lenses (bug finding and maintainability), a pattern emerges. Hotspot analysis and code ownership have the strongest evidence for predicting defects, and they are also directly useful for maintainability. Static analysis actually finds bugs, even if it misses most of them. Everything else (complexity, smells, coupling, duplicates, nesting) is weak as a defect predictor but has varying degrees of value as a maintainability signal.

This is not a complete overview, not by far. There are methods I did not cover (architecture-level metrics, test quality indicators, dependency freshness, among others) and areas where the research is evolving faster than I can read it. I may revisit this in follow-up posts.

Coming back to paying for services that do this for you and whether or not they are adding value: the strongest signals come from git history, which is free in itself. The metrics most paid tools emphasize are the ones with weaker defect-prediction evidence. You are often paying for convenience, visualization, and CI integration rather than for better science. That can be worth it, but go in knowing what the science actually supports. From maintainability standpoint there is a good case to use them, and also it saves you from having to build this yourself (even though that equation dramatically changed with LLMs at your disposal). But it is much more fun to understand what happens and build it yourself (even if you do not use it for you production code, you'll learn a lot).

I liked this quote from DeMarco in his article [from 2009](https://www.cs.uni.edu/~wallingf/teaching/172/resources/demarco-on-se.pdf) so let's end with that: "Software development is and always will be somewhat experimental. The actual software construction isn't necessarily experimental, but its conception is. And this is where our focus ought to be. It's where our focus always ought to have been."

*Looking into code quality improvement for your team? <a href="#" onclick="task1(); return false;">Get in touch</a> to compare notes on what works and what does not.*

## Sources Mentioned

- [No Silver Bullet](https://worrydream.com/refs/Brooks-NoSilverBullet.pdf) (Brooks, 1986) -- Essential vs accidental complexity
- [A Critique of Cyclomatic Complexity](https://www.semanticscholar.org/paper/A-critique-of-cyclomatic-complexity-as-a-software-Shepperd/a4b522d7d55c0ed38c825c4fb9fe28c14d659c0a) (Shepperd, 1988) -- CC is a LOC proxy with poor foundations
- [Software Measurement: A Necessary Scientific Basis](https://dl.acm.org/doi/10.5555/580949) (Fenton & Pfleeger, 1997) -- Textbook on measurement theory in software
- [Predicting Fault Incidence](https://ieeexplore.ieee.org/document/885631) (Graves et al., 2000) -- LOC makes complexity metrics redundant
- [The Confounding Effect of Class Size](https://ieeexplore.ieee.org/document/935855) (El Emam et al., 2001) -- Most metrics are LOC proxies
- [OO Metrics Don't Transfer](https://www.sciencedirect.com/science/article/abs/pii/S0164121200000868) (Briand et al., 2002) -- Models built on one project fail on others
- [Software Science Revisited](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1302&context=cstech) (Shen et al., 1983) -- Debunking Halstead metrics
- [Use of Relative Code Churn Measures](https://dl.acm.org/doi/10.1145/1062455.1062514) (Nagappan & Ball, 2005) -- Churn predicts defects at 89% accuracy
- [Software Engineering: An Idea Whose Time Has Come and Gone?](https://ieeexplore.ieee.org/document/5076468/) (DeMarco, 2009) -- "More metrics is better" recanted
- [Change Coupling and Defects](https://dl.acm.org/doi/10.1109/WCRE.2009.5070547) (D'Ambros et al., 2009) -- Change coupling correlates with defects
- [Cyclomatic Complexity and Lines of Code](https://www.researchgate.net/publication/220204439) (Jay, Hale et al., 2009) -- CC has no explanatory power beyond LOC
- [Code Clones in the Large](https://dl.acm.org/doi/10.1109/ICSE.2009.5070547) (Juergens et al., 2009) -- Inconsistent clone changes cause faults
- [A Few Billion Lines of Code Later](https://dl.acm.org/doi/10.1145/1646353.1646374) (Bessey et al., 2010) -- Coverity's lessons on static analysis adoption
- [Learning a Metric for Code Readability](https://www.semanticscholar.org/paper/Learning-a-Metric-for-Code-Readability-Buse-Weimer/1a2b8aa0ed7f24ca001508654f506ea010b18a5e) (Buse & Weimer, 2010) -- Human readability ratings correlate with defects
- [Don't Touch My Code!](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/bird2011dtm.pdf) (Bird et al., 2011) -- Code ownership predicts defects
- [An Empirical Study on Clones](https://www.sciencedirect.com/science/article/pii/S0167642310002091) (Bettenburg et al., 2012) -- Only 1-3% of clone inconsistencies cause defects
- [Do Code Smells Hinder Code Changes?](https://link.springer.com/article/10.1007/s10664-011-9171-y) (Khomh et al., 2012) -- Smell-affected classes are more change-prone
- [Cloned Code: Stable Code](https://link.springer.com/article/10.1007/s10664-011-9195-3) (Rahman et al., 2012) -- Clones may be less defect-prone
- [A Validation of Martin's Metric](https://www.researchgate.net/publication/31598248_A_Validation_of_Martin's_Metric) (Al Dallal, 2013) -- Martin's coupling metrics lack validation
- [Defect Prediction with Change Coupling](https://www.sciencedirect.com/science/article/abs/pii/S0164121214000351) (Canfora et al., 2014) -- Granger-based temporal coupling predicts defects
- [Analyzing the State of Static Analysis](https://azaidman.github.io/publications/bellerSANER2016.pdf) (Beller et al., 2016) -- 77% of projects use static analysis
- [Code Review and Ownership](https://dl.acm.org/doi/abs/10.1145/2884781.2884852) (Thongtanunam et al., 2016) -- Code review partially mitigates ownership effect
- [A Survey on Software Smells](https://www.semanticscholar.org/paper/A-survey-on-software-smells-Sharma-Spinellis/6fa6e56c6d57efd5e0fbbe61093c0a0bd32f73cc) (Sharma & Spinellis, 2018) -- Evidence per smell type varies widely
- [On the Diffuseness and Impact of Code Smells](https://link.springer.com/article/10.1007/s10664-017-9535-z) (Palomba et al., 2018) -- Smells correlate with bugs (with size caveats)
- [How Many of All Bugs Do We Find?](https://www.semanticscholar.org/paper/How-Many-of-All-Bugs-Do-We-Find-A-Study-of-Static-Habib-Pradel/72e779539de6a5f9c4d30e512ea9ca4688e02c6a) (Habib & Pradel, 2018) -- Static analyzers miss the large majority of bugs
- [Cognitive Complexity Validation](https://arxiv.org/pdf/2007.12520) (Munoz Baron et al., 2020) -- Validated for readability, not defects
- [Code Red: The Business Impact of Code Quality](https://dl.acm.org/doi/10.1145/3524843.3528091) (Tornhill & Borg, 2022) -- 15x more defects in low-quality code
- [Cognitive Complexity vs Cyclomatic Complexity](https://arxiv.org/abs/2303.07722) (Lenarduzzi et al., 2023) -- Cognitive complexity slightly outperforms CC for readability

## Tools Referenced

- [SonarQube](https://www.sonarsource.com/products/sonarqube/) -- Most widely used static analysis platform
- [CodeScene](https://codescene.com/) -- Behavioral code analysis (churn + complexity + ownership)
- [ESLint](https://eslint.org/) -- JavaScript/TypeScript linter
- [Pylint](https://pylint.readthedocs.io/) -- Python static analyzer
- [SpotBugs](https://spotbugs.github.io/) -- Java bug pattern detector
- [CodeQL](https://codeql.github.com/) -- GitHub's query-based static analyzer
- Adam Tornhill, [Your Code as a Crime Scene](https://pragprog.com/titles/atcrime2/your-code-as-a-crime-scene-second-edition/) -- The book behind CodeScene's approach

## Related Posts

- [Your AI Tests Are Probably Lying to You](/ai/development/testing/2026/06/08/your-ai-tests-are-probably-lying-to-you.html) -- Similar theme: green dashboards that hide real problems
- [Benchmarking Open-Source PII Detection](/python/security/privacy/2026/06/01/benchmarking-open-source-pii-detection.html) -- Same approach: benchmark tools, pick the practical winner
- [Vibe Coding: Product Quality and Democratisation](/ai/development/2026/02/05/vibe-coding-quality-democratisation.html) -- Code quality in the AI era
- [Human in the Loop: Why Your LLM-Assisted Code Still Needs Human Eyes](/ai/llm/development/best-practices/2025/11/14/human-in-the-loop-ai-code-review.html) -- Code review quality with AI assistance
- [Evidence-Based Best Practices as AI Guardrails (Part 1)](/ai/development/best-practices/2026/03/31/evidence-based-best-practices-ai-guardrails.html) -- Same evidence-based methodology applied to AI guardrails
