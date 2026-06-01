---
layout: post
title: "Benchmarking Open-Source PII Detection Across Domains (1/2)"
date: 2026-06-01
categories: python security privacy
description: "I tested five PII detection tools across four datasets. None are good. When accuracy is equally mediocre, the framework matters more than the model."
keywords: "PII detection, GLiNER, Piiranha, Presidio, NER, GDPR, privacy, benchmark, named entity recognition, data anonymization"
image: /assets/images/benchmarking-open-source-pii-detection-blog.png
---

<figure>
  <img src="/assets/images/pii-detection-benchmark.jpg" alt="Coastal mudflat landscape under dramatic cloudy sky, visibility fading into the distance" width="1920" height="1280" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>Photo by <a href="https://www.pexels.com/@jornt-hornstra-108388438">Jornt Hornstra</a> on <a href="https://www.pexels.com">Pexels</a></figcaption>
</figure>

About seven months ago I wrote about [zero-latency PII filtering in Python logging](/python/security/best-practices/gdpr/2025/11/06/zero-latency-pii-filtering-python-logging.html): how to sanitize personal data from logs without blocking your main thread. That solved the *where* and *when* of filtering. But it implied that detection itself was a solved problem. Throw some regex at it, done. And when handling logs, this is somewhat easier, since you can define certain keys to be filtered etc. 

However filtering PII in text is not a solved problem. When I started planning to build PII redaction into a production pipeline that handles legal documents and Dutch-language content (part of a broader push toward [security by design](/ai/development/security/2026/04/07/security-by-design-with-project-codeguard.html) in our projects), the question became: which detection tool actually works across all of that?

So first thing to do is get your bearings: find the most common approaches and some datasets and run a benchmark. Five detection approaches, four datasets, two languages (Dutch (since this was the language for the legal documents) and English (testing this will give some more insight and means I can reuse what I learn here)). This post covers what I found. A follow-up (part 2) will take the winners and push them further: more entity types, domain-specific tuning, the stuff you actually need for production.

Warning: this is not a scientific paper. It is a practical comparison I ran to figure out which tool to bet on for our pipeline. The difficulty with comparing these tools is that they are fundamentally different: different architectures, different label schemes, different assumptions about what PII even is. There is no clean apples-to-apples comparison possible. I did my best to make it fair (shared label set, multiple datasets), but four datasets and five models is not enough for strong statistical claims. What it *is* enough for is picking a direction.

## Why Comparing PII Detection Tools Is Hard

Comparing PII detection tools is getting complicated veryfast. Every tool uses different labels, supports different entity types, and has different ideas about what counts as PII.

[Piiranha](https://huggingface.co/iiiorg/piiranha-v1-detect-personal-information) outputs fine-grained types: GIVENNAME, SURNAME, CITY, STREET, BUILDINGNUM. [Presidio](https://github.com/microsoft/presidio) outputs coarse types: PERSON, LOCATION. [GLiNER](https://huggingface.co/urchade/gliner_multi_pii-v1) accepts whatever labels you define at inference time. A "person name" in one system is two separate entities in another.

Coverage gaps make it worse. Piiranha detects 17 PII types but has no DATE entity. Presidio has DATE_TIME but cannot detect passwords or usernames. No two tools cover the same set.

And every dataset has its own taxonomy. [AI4Privacy](https://huggingface.co/datasets/ai4privacy/pii-masking-300k) uses GIVENNAME/SURNAME. [Gretel](https://huggingface.co/datasets/gretelai/synthetic_pii_finance_multilingual) uses "name." [Nemotron](https://huggingface.co/datasets/nvidia/Nemotron-PII) uses first_name/last_name. [CoNLL-2002](https://huggingface.co/datasets/eriktks/conll2002) uses PER.

A naive benchmark that ignores all this is misleading. A model scoring F1 0.63 on one dataset and 0.13 on another might not have "collapsed." It might simply lack entity types that dataset emphasizes (dates accounting for 25% of spans, for example).

## Three Questions People Conflate

When evaluating PII detection, three separate questions get mixed together:

1. How good is the model at detecting entity types it supports?
2. How many entity types does it support?
3. How well does it generalize to text from different domains?

Evaluating all entity types on a single dataset mixes all three. A model might score poorly not because detection is bad, but because it lacks entity types the dataset emphasizes. And a model that scores well might just be evaluated on data similar to its training set.

I wanted to isolate question 1 first. So I defined a shared label set of six entity types that *all* models can detect: PERSON_NAME, EMAIL, PHONE, LOCATION, CREDITCARD, and IBAN. Every model gets scored only on these. Fair fight.

Question 3 gets answered by testing across four independent datasets. Question 2 (which additional types each model uniquely supports) is left for part 2.

## The Models

Five detection approaches, covering the major architectural categories:

**Regex**: Compiled patterns for email, phone (via Python `phonenumbers` for international format parsing), IBAN, credit card (with Luhn validation), and IPv4. Deterministic, no ML.

**[Piiranha](https://huggingface.co/iiiorg/piiranha-v1-detect-personal-information)**: 86M-parameter DeBERTa-v3-base, fine-tuned for token classification on 17 PII entity types. Trained on AI4Privacy PII-Masking-300k. Supports English and Dutch.

**[Presidio](https://github.com/microsoft/presidio)** (Microsoft, v2.2): Orchestration framework combining spaCy NER (`en_core_web_lg` / `nl_core_news_md`) with built-in pattern recognizers for structured entities.

**[GLiNER v1](https://huggingface.co/urchade/gliner_multi_pii-v1)**: ~209M-parameter zero-shot NER model. Entity types are defined as natural-language descriptions at inference time. You tell it what to look for, and it looks. Schema-agnostic. This is the [GLiNER architecture](https://arxiv.org/abs/2311.08526) fine-tuned on synthetic PII data.

**[GLiNER v2](https://huggingface.co/fastino/gliner2-base-v1)**: 205M-parameter multi-task model from Fastino Labs. A separate project from v1 with different architecture and training. Included because v2 claims improved multi-task capabilities.

## The Datasets

Four datasets, two languages, different domains:

| Dataset | Languages | Domain | Why |
|---|---|---|---|
| [AI4Privacy](https://huggingface.co/datasets/ai4privacy/pii-masking-300k) | EN + NL | Mixed synthetic | In-distribution baseline for Piiranha (it trained on this) |
| [Gretel Finance](https://huggingface.co/datasets/gretelai/synthetic_pii_finance_multilingual) | EN + NL | Financial docs | Out-of-distribution; formal financial text style |
| [Nemotron-PII](https://huggingface.co/datasets/nvidia/Nemotron-PII) | EN only | 50+ industries | Broadest domain diversity |
| [CoNLL-2002](https://huggingface.co/datasets/eriktks/conll2002) | NL only | Newspaper | Gold-standard human annotations; the only non-synthetic dataset |

The combination is imperfect. No single dataset covers both languages with non-synthetic, human-annotated PII spans. As far as I can tell, such a dataset does not exist publicly.

## Evaluation

**Accuracy**: Precision, recall, and F1 with relaxed span matching (+/-5 character tolerance). Micro-averaged across all entity types.

**Speed**: Median latency per text and throughput in texts/sec. Measured on Apple Silicon M1 Pro CPU.

**Reversibility**: Detected spans get replaced with typed placeholders (`[PERSON_NAME_1]`, `[EMAIL_1]`). Same entity text gets the same placeholder throughout a document. Pass rate = percentage of documents where `restore(redact(text)) == text`. This matters: if you cannot perfectly restore the original after redaction, your redaction system is lossy and you will corrupt data.

## Results

### Cross-Dataset Accuracy

| Model | AI4Privacy | Gretel | Nemotron | CoNLL-2002 (NL) | **AVG** |
|---|---|---|---|---|---|
| **Piiranha** | **0.780** | 0.169 | **0.699** | 0.519 | **0.542** |
| **GLiNER v1** | 0.455 | **0.607** | 0.484 | 0.595 | **0.535** |
| Presidio | 0.359 | 0.298 | 0.487 | **0.780** | 0.481 |
| GLiNER v2 | 0.469 | 0.373 | 0.510 | 0.558 | 0.478 |
| Regex | 0.207 | 0.179 | 0.297 | 0.000 | 0.171 |

The first thing that jumps out: none of these models are good. The best average F1 across four datasets is 0.542. Commercial systems claim 0.92-0.99. That is a big gap.

The second thing: the top three (Piiranha, GLiNER v1, Presidio) are closer to each other than any of them are to "good enough." The difference between first and third place is 0.061 F1. A paired t-test across the four datasets shows none of the pairwise differences reach statistical significance (p>>0.10, n=4). They are all mediocre, just in different ways. Piiranha swings wildly (0.169 to 0.780). GLiNER v1 is more consistent (0.455 to 0.607). Presidio sits in between.

### Generalization

How much does each model degrade on unfamiliar text?

| Model | In-distribution (AI4Privacy) | Worst OOD dataset | Drop |
|---|---|---|---|
| Piiranha | 0.780 | 0.169 (Gretel) | -78% |
| GLiNER v1 | 0.455 | 0.455 (AI4Privacy) | 0% |
| GLiNER v2 | 0.469 | 0.373 (Gretel) | -20% |
| Presidio | 0.359 | 0.298 (Gretel) | -17% |
| Regex | 0.207 | 0.000 (CoNLL-2002) | -100% |

Piiranha's 78% drop on financial text looks dramatic, and it is. But GLiNER v1's "consistent" performance means it never goes above 0.607 either. Presidio's drop is a moderate 17%. The variance differs (Piiranha std=0.271, GLiNER v1 std=0.077, Presidio std=0.213), but all three models land in the same general territory of "not good enough for production without additional work." Regex scores zero on CoNLL-2002 because that dataset only has person names and locations.

### Person Names (The Hard Part)

Person names are the most common PII entity and the hardest to detect because they are context-dependent (is "Holland" a person or a location?).

| Model | AI4Privacy | Gretel | Nemotron | CoNLL-2002 |
|---|---|---|---|---|
| Piiranha | 0.787 | 0.139 | 0.749 | 0.561 |
| GLiNER v1 | 0.446 | 0.564 | 0.327 | 0.759 |
| GLiNER v2 | 0.435 | 0.439 | 0.325 | 0.641 |
| Presidio | 0.179 | 0.365 | 0.360 | 0.781 |

Piiranha excels on synthetic data (AI4Privacy, Nemotron) but fails hard on formal financial text and is mediocre on newspaper text. GLiNER v1 and Presidio are more stable but with lower peaks. Regex cannot detect person names at all.

### Phone Numbers (Format Matters)

| Model | AI4Privacy | Gretel | Nemotron |
|---|---|---|---|
| GLiNER v1 | 0.874 | 0.882 | 0.834 |
| Piiranha | 0.874 | 0.707 | 0.606 |
| GLiNER v2 | 0.497 | 0.377 | 0.639 |
| Presidio | 0.348 | 0.390 | 0.541 |

GLiNER v1 is the most consistent phone detector across all domains. GLiNER v2 is significantly worse than v1 here. Presidio struggles because spaCy was not designed for this.

### Email (Where Patterns Win)

| Model | AI4Privacy | Gretel | Nemotron |
|---|---|---|---|
| Presidio | 0.960 | 0.930 | 0.996 |
| Piiranha | 0.934 | 0.553 | 0.974 |
| GLiNER v1 | 0.854 | 0.576 | 0.966 |
| GLiNER v2 | 0.792 | 0.568 | 0.848 |

Presidio's pattern-based email recognizer beats all NER models. This is one of the few entity types where pattern matching outperforms learned models. Emails have rigid structure, and a well-written regex does not need to "understand" context. The transformer models still do well on AI4Privacy and Nemotron, but drop on Gretel's financial documents where email formats are embedded in formal text.

### Speed

| Model | Median (ms) | Texts/sec |
|---|---|---|
| Regex | 0.1 | 3,861 |
| Presidio | 15.1 | 63 |
| Piiranha | 118.5 | 8.3 |
| GLiNER v1 | 161.3 | 5.9 |
| GLiNER v2 | 197.7 | 5.0 |

Presidio is 8-11x faster than transformer models (spaCy's backbone is small). Among transformers, Piiranha's 86M parameters make it fastest. All measured on CPU. GPU may change the picture, but the relative speed differences will probably be comparable.

### Reversibility

| Model | Pass Rate |
|---|---|
| Regex | 100% |
| Piiranha | 100% |
| GLiNER v1 | 100% |
| GLiNER v2 | 100% |
| Presidio | 64% |

Presidio fails on 36% of documents. The cause: its internal tokenization produces character offsets that do not precisely match the original text. This will require further work but can be improved.

### Does Regex Help?

A reasonable improvement could be to add regex to the mix, so I tested this. Both regex and the model are running on the same text and the results are merged.

| Model | Base AVG | +Regex AVG | Delta |
|---|---|---|---|
| Piiranha | 0.542 | 0.553 | +0.012 |
| GLiNER v1 | 0.535 | 0.536 | +0.001 |
| Presidio | 0.481 | 0.481 | +0.001 |

Conclusion: adding regex to NER is not worth it. The largest gain is +0.012 for Piiranha, and even that is driven entirely by the Gretel dataset where Piiranha is already failing. For GLiNER v1 and Presidio, the improvement is within noise.

Regex actually *hurts* accuracy on AI4Privacy for all three models (-0.010 to -0.011 F1) because the merge logic occasionally displaces correct NER detections with regex false positives. The model choice matters far more than layering regex on top.

## So Which One Do You Pick?

If the accuracy differences are not significant and none of the models are production-ready on their own, what *does* differentiate them?

| Property | Piiranha | GLiNER v1 | Presidio |
|---|---|---|---|
| Average F1 | 0.542 | 0.535 | 0.481 |
| Best single dataset | 0.780 (AI4Privacy) | 0.607 (Gretel) | 0.780 (CoNLL-2002) |
| Worst single dataset | 0.169 (Gretel) | 0.455 (AI4Privacy) | 0.298 (Gretel) |
| Catastrophic failure? | Yes (Gretel) | No | No |
| Reversibility | 100% | 100% | 64% |
| Speed (median ms) | 119 | 161 | 15 |
| Framework/ecosystem | Model only | Model only | Full framework |

Piiranha and GLiNER v1 are standalone models. They give you detections and that is it. You build the anonymization pipeline, the recognizer registry, the deanonymization logic, the operator pipeline, the multilingual engine configuration, all of it yourself.

[Presidio](https://github.com/microsoft/presidio) gives you most of that out of the box. Recognizer registry, operator pipeline for anonymization and deanonymization, built-in pattern recognizers for entity types the NER models lack (DATE_TIME, URL), multilingual NLP engine support, and active maintenance by Microsoft. Its accuracy gap to the top two is 0.054-0.061 F1, which is not statistically significant with our sample size.

And to keep in mind: Presidio's NER backend is replaceable. Its architecture is designed for plugging in custom recognizers. You are not hard bound to just spaCy. You can plug in GLiNER v1, Piiranha, or anything else as a custom recognizer and possible get better detection quality while keeping the framework.

When accuracy is equally mediocre across the board, the framework wins. **Presidio is the logical choice.** Not because it detects PII best (it does not), but because it provides the infrastructure you need regardless of which detection model you use, and you can swap the detection model later without rebuilding everything else. This is a very practical benefit over the others.

The reversibility issue (36% failure rate) is real but can be improved. It is caused by span boundary misalignment in Presidio's tokenization, not by its detection quality. Post-processing Presidio's output to align spans with the source text before replacement solves this.

Speed is another Presidio advantage. At 15ms per text it is 8-11x faster than the transformer models. For batch processing this matters less, but for real-time pipelines it is significant.

## What I Learned

The main takeaway: **none of these tools are good at cross-domain PII detection.** Not the open-source ones I tested, and not the commercial ones either. [Tonic.ai](https://www.tonic.ai/blog/benchmarking-openai-privacy-filter-pii-detection) reports F1 0.92-0.99 on their own corpus. [AWS Comprehend](https://docs.aws.amazon.com/ai/responsible-ai/comprehend-detectpii/overview.html) claims 0.87-0.91. [OpenAI's Privacy Filter](https://openai.com/index/introducing-openai-privacy-filter/) hits 0.96 on PII-Masking-300k. But these are all in-distribution numbers. When [PIIBench](https://arxiv.org/abs/2604.15776) tested eight systems across 10 unified datasets with 48 entity types, the *best* system scored F1 0.14. OpenAI's Privacy Filter drops from 0.96 to 0.18-0.65 on Tonic's out-of-distribution test groups. Cross-domain PII detection is genuinely unsolved.

So in the end the decision stops being about which model detects best, since hey are all mediocre. The decision becomes: which tool is the most practical to build on, the easiest to use, the most actively maintained, and the most complete? That is [Presidio](https://github.com/microsoft/presidio). It gives you the framework, the pipeline, the pattern recognizers, and a swappable NER backend so you can improve detection quality over time without rebuilding everything else.

A few other things worth noting:

**In-distribution benchmarks are misleading.** Piiranha's F1 of 0.78 on its training data drops to 0.17 on financial text. If a model's benchmark only shows results on familiar data, that number is not useful as a predictor for real-world use.

**Zero-shot models generalize better than fine-tuned ones.** GLiNER v1 beats Piiranha on every out-of-distribution dataset. Its schema-agnostic architecture seems to help. This makes it a strong candidate for plugging into Presidio as a custom recognizer.

**Hybrid regex+NER is oversold.** Common recommendation in the literature (including [RECAP](https://arxiv.org/abs/2510.07551) and other [hybrid approaches](https://doi.org/10.1038/s41598-025-91846-2)). Our results show it adds almost nothing (+0.001 F1 for GLiNER v1).

**GLiNER v2 is worse than v1 for PII.** The multi-task rewrite hurt NER quality. v2 underperforms v1 on three of four datasets.

## What This Benchmark Does Not Prove

This is a practical comparison to pick a direction, not a rigorous evaluation. Here is what is wrong with it and why I ran it anyway.

**Three of four datasets are synthetic.** AI4Privacy, Gretel, and Nemotron are all machine-generated text. CoNLL-2002 is the only real-world data, and it is Dutch newspaper text from 2000. So when I say "cross-domain," I mostly mean "across different synthetic data generators." The gap between synthetic financial text and actual financial documents could be larger than the gap between two synthetic datasets. I used what was publicly available with character-level PII span annotations in both English and Dutch. That combination barely exists. A proper evaluation would include real legal documents, real customer support transcripts, real medical records. Unfortunately they are out of reach to test this on.

**AI4Privacy is Piiranha's training distribution.** I use the validation split, not the training split, so it is not literal data leakage. But validation data from the same generator is not independent. Piiranha's 0.78 on AI4Privacy is inflated compared to what it would score on truly held-out data, and the "78% drop to Gretel" headline is partly an artifact of that inflated baseline.

**The +/-5 character tolerance is a judgment call.** Span matching in NER evaluation is sensitive to boundary definitions. Strict matching (exact character positions) penalizes models for including or excluding a space, a period, or a title like "Mr." Relaxed matching with a 5-character window allows for these tokenization differences without being so loose that partial detections count as hits. Five characters is roughly one token or one word boundary. I picked it because it felt right for this use case, so it was a choice without real base. Other benchmarks use token-level overlap or IoU thresholds. The choice affects absolute F1 numbers but not the relative ranking between models (all models benefit equally from relaxed matching).

**CoNLL-2002 only tests two of six shared entity types.** It has person names and locations but no email, phone, credit card, or IBAN. Presidio's 0.780 on CoNLL-2002 is driven entirely by spaCy's person/location NER, not by its pattern recognizers. If CoNLL-2002 had structured PII entities, Presidio's score there would likely be higher (its email recognizer is the best in the benchmark) and the other models' scores might shift too. This dataset tests a subset of the shared label set, not the full thing.

**No per-entity sample counts.** I do not report how many instances of each entity type appear per dataset. If Gretel has 12 credit card numbers and AI4Privacy has 400, the per-entity tables are not equally powered. A model scoring 0.139 on person names in Gretel might be based on hundreds of spans or dozens.

**Six shared entity types is a narrow view.** In practice you need more: dates of birth, social security numbers, IP addresses, Dutch BSN numbers. Piiranha detects 17 types. GLiNER can attempt any type you define (with varying accuracy). The choice depends not just on detection quality but on which entities you need. Part 2 covers this.

All that said: I needed to pick a tool and waiting for a perfect benchmark could take a long time. In the end my question was answered in the sense that there is no 'best', just different flavours. And in that light choosing Presidio is the practical choice.

## What Comes Next

The direction is set: Presidio as the framework, with a better NER model plugged in.

Part 2 will:
1. Test Presidio with GLiNER v1 and Piiranha as custom recognizers to see how much the detection quality improves while keeping the framework
2. Evaluate [OpenAI's Privacy Filter](https://openai.com/index/introducing-openai-privacy-filter/), which claims F1 0.96 on PII-Masking-300k but drops significantly on out-of-distribution text according to [Tonic.ai's benchmark](https://www.tonic.ai/blog/benchmarking-openai-privacy-filter-pii-detection). It is relatively new and worth testing on our datasets
3. Evaluate on the full set of entity types we actually need for production: person names, emails, phone numbers, physical addresses, dates of birth, social security numbers, IBANs, credit cards, IP addresses, and Dutch-specific identifiers (BSN)
4. Fix the reversibility issue (span boundary alignment)
5. Determine where we still need to augment with additional detection methods

*Building PII detection into your pipeline and wondering which tool to pick? <a href="#" onclick="task1(); return false;">Get in touch</a> to compare notes.*

## Resources

- [PIIBench: A Unified Multi-Source Benchmark for PII Detection](https://arxiv.org/abs/2604.15776) - Cross-domain benchmark where all tested systems scored below F1 0.14
- [Tonic.ai: Benchmarking OpenAI's Privacy Filter](https://www.tonic.ai/blog/benchmarking-openai-privacy-filter-pii-detection) - Independent cross-domain evaluation showing commercial systems degrade significantly on out-of-distribution text
- [AWS Comprehend Detect PII Service Card](https://docs.aws.amazon.com/ai/responsible-ai/comprehend-detectpii/overview.html) - AWS's own accuracy claims per entity type
- [OpenAI Privacy Filter](https://openai.com/index/introducing-openai-privacy-filter/) - F1 0.96 on PII-Masking-300k, much lower cross-domain
- [GLiNER: Generalist Model for Named Entity Recognition](https://arxiv.org/abs/2311.08526) (Zaratiana et al., NAACL 2024) - The architecture behind GLiNER v1
- [Hybrid Rule-based NLP and Machine Learning for PII in Financial Documents](https://doi.org/10.1038/s41598-025-91846-2) (Nature Scientific Reports, 2025)
- [RECAP: Hybrid Methods for Multilingual PII Detection](https://arxiv.org/abs/2510.07551) (NeurIPS, 2025)

### Models and datasets tested

- [Piiranha v1](https://huggingface.co/iiiorg/piiranha-v1-detect-personal-information) - DeBERTa-v3-base fine-tuned for PII detection
- [GLiNER v1 (multi_pii)](https://huggingface.co/urchade/gliner_multi_pii-v1) - Zero-shot NER fine-tuned on synthetic PII data
- [GLiNER v2 (gliner2-base)](https://huggingface.co/fastino/gliner2-base-v1) - Multi-task NER from Fastino Labs
- [Presidio](https://github.com/microsoft/presidio) - Microsoft's PII detection and anonymization framework
- [AI4Privacy PII-Masking-300k](https://huggingface.co/datasets/ai4privacy/pii-masking-300k) - Mixed synthetic PII dataset (EN + NL)
- [Gretel Synthetic PII Finance](https://huggingface.co/datasets/gretelai/synthetic_pii_finance_multilingual) - Multilingual financial documents
- [Nemotron-PII](https://huggingface.co/datasets/nvidia/Nemotron-PII) - NVIDIA's multi-industry PII dataset
- [CoNLL-2002](https://huggingface.co/datasets/eriktks/conll2002) - Dutch/Spanish NER with human annotations
