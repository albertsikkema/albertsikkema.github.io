---
layout: post
title: "gtk: Filtering CLI Noise to Save LLM Tokens"
date: 2026-04-09
categories: ai development tools
description: "How a CLI proxy filters shell command output to reduce token usage in AI coding sessions with Claude Code. The concept, the implementation, and what it actually saves."
keywords: "CLI output filter, token optimization, Claude Code, LLM token reduction, context window management, AI coding agent, reduce AI costs, RTK, PreToolUse hook"
image: /assets/images/gtk-cutting-llm-token-costs-cli-output-blog.png
---

<figure>
  <img src="/assets/images/gtk-coffee-filter.jpg" alt="Pour-over coffee filter with dark coffee dripping through, filtering grounds from liquid" width="1920" height="1280" fetchpriority="high" style="width:100%;height:auto">
  <figcaption>Filtering out what you don't need. Photo by <a href="https://unsplash.com/@eilivaceron">Eiliv Aceron</a> on <a href="https://unsplash.com/photos/XP5zW2ngk9w">Unsplash</a>.</figcaption>
</figure>

A few weeks ago I ran into [rtk](https://github.com/rtk-ai/rtk) (Rust Token Killer), a CLI proxy that filters command output before it reaches your AI coding agent. The idea is brilliant: most of what `git log` or `cargo test` spits out is noise the model doesn't need. Strip it, and you save tokens. (and limit the total context you build up over the run of several back and forths)

I liked the concept but not the scope. rtk is written in Rust and supports a lot of features I'll never use. And for a lot of my workflow it is important to have a full response on git diff and PR: rtk does not do that and I found no easy way to alter this. So I did what any reasonable developer would do: I took the principle and rewrote it in Go with only the parts I care about.

The result is gtk (Go Token Kit): a quick-and-dirty single static binary with no dependencies and 87 filters across the tools I actually use. It is not public (it is not polished enough for that, and rtk already exists), but the principles behind it are worth sharing.

Does it save as much as rtk suggests? I don't know because I do not measure the total tokens saved. And every now and then you have to rerun the command to get the output without gtk intervention, so that is an extra call which makes a lot of what you saved before not useful anymore. So overall I think that I do not save as much as rtk claims, my guesstimate is at 10-15%: still more than enough to justify using it.

## Why This Is Worth Caring About

In a typical Claude Code session, CLI output is the largest source of (wasted) tokens. Run `go test ./...` with 100 passing tests: hundreds of lines of noise. Multiply that by dozens of commands per session. And all you actually need for that step is: did the tests pass? Nothing more. One analysis found that [AI coding agents spend 60-80% of their token budget](https://medium.com/@jakenesler/context-compression-to-reduce-llm-costs-and-frequency-of-hitting-limits-e11d43a26589) on orientation (finding things, reading output), not on actual problem-solving.

Tokens aren't free, every token gets consumed by the LLM and costs money, and since the context is passed on every interaction, this adds up. Also tokens eat into your context window, which means shorter useful conversations before the model starts forgetting earlier context. They slow down responses (more input to process) and [irrelevant context actively degrades LLM performance](https://redis.io/blog/context-window-overflow/).

gtk (and rtk) cuts that down. A `git log -20` that would produce 2,000 tokens comes out as ~120 tokens (hash, subject, date, author). A test run with 100 passing tests becomes a single summary line. The savings add up fast.

```
[gtk: 2054 -> 118 tokens, 94% saved]
```

That hint prints to stderr after every filtered command. It's a nice reminder that the thing is actually working. And gives an idea about what is passed to the LLM instead of the full output of the previous step.

## How It Works

gtk operates in three stages:

**Argument injection.** Before running the command, gtk can modify arguments to get more parseable output. It injects `-json` into `go test`, `--pretty=format:...` into `git log`, `--reporter=json` into `vitest`. It checks whether you already specified these flags, so it never overrides your intent.

**Execution.** Runs the real command, captures stdout and stderr, preserves the original exit code. If `go test` fails with exit code 1, gtk returns exit code 1.

**Filtering.** Applies one of 87 registered filters to compress the output. If no filter matches, output passes through unchanged. If a filter errors, you get the raw output as fallback. It never blocks you.

The filter strategies vary by what makes sense for each command:

| Strategy | What it does | Example |
|----------|-------------|---------|
| Elimination | Strips passing tests, compilation progress, hint lines | `cargo test` only shows failures |
| Compression | One line per item instead of multi-line blocks | `git log` becomes hash + subject + date |
| Deduplication | Replaces timestamps and UUIDs with placeholders, counts occurrences | Repeated log lines collapse |
| Structured parsing | Parses JSON output into summaries | `go test -json` becomes "100 passed in 2 packages" |
| Truncation | Caps long lines and large result sets | Lines cut to 80-120 chars |
| Masking | Replaces sensitive values with `****` | Env vars containing "secret", "token", "password" |

## The Part That Makes It Actually Work

If the AI has to remember to prefix every command with `gtk`, it probably will (sometimes). Inconsistency is the norm with LLMs.

So to make sure this always runs, we need to make sure that Claude does not have to remember it: Claude just runs `git log -10` normally. A [PreToolUse hook](https://code.claude.com/docs/en/hooks) is called: it intercepts the command and rewrites it to `gtk git log -10` transparently. You can compare it to a proxy in a way (or middleware): it intercepts the command, does some things to it, runs the altered command and then returns the cleaned output.

The hook checks if the command starts with a known prefix and prepends the gtk binary path. Commands with pipes or chains are left alone, since those already have their own filtering. (and also more pragmatic: are too difficult to reliably recreate with gtk)

```go
var gtkPrefixes = []string{
    "git ", "cargo ", "go test", "go build", "gh ",
    "docker ", "kubectl ", "npm ", "pytest ", "curl ",
    // ... 24 prefixes total
}

func tryGtkRewrite(command string) string {
    if strings.ContainsAny(command, "|") { return "" }
    if strings.Contains(command, "&&")   { return "" }

    for _, prefix := range gtkPrefixes {
        if strings.HasPrefix(command, prefix) {
            return gtkBin + " " + command
        }
    }
    return ""
}
```

This is the same hook I wrote about in [Securing YOLO Mode](/ai/security/development/tools/2026/02/01/securing-claude-code-hooks-best-practices.html), except now it does three jobs instead of one:

1. **Security patterns** -- blocks dangerous `rm`, fork bombs, force pushes to main, reverse shells, credential exfiltration
2. **Deny list** -- project-specific glob patterns from settings.json converted to regex at runtime
3. **GTK rewrite** -- the token optimization layer

One binary, three layers. In container mode (`CLAUDE_CONTAINER_MODE=1`), local-only threats like `rm -rf` are skipped since the container is disposable, but network and escape checks stay active.

## Why Go Instead of Rust

The original I took inspiration from is written in Rust. It works well. But I like Go, had little time and thought this should work just as well: Go compiles to a static binary just like Rust and is more than fast enough. Cross-compilation is trivial (`GOOS=linux GOARCH=amd64 go build`). And adding a new filter is just writing a function and registering it in a map. Easy does it.

I also dropped everything I don't use. rtk supports Gradle, Maven, Swift, .NET, Terraform, and others, and integrates with Cursor, Gemini CLI, Aider, and other agents. I don't work with any of those tools, and I only use Claude Code. My version covers git, go, cargo, docker, kubectl, npm, pnpm, pytest, eslint, tsc, prettier, vitest, curl, and a few more. That's it.

## Bypass When Needed

Sometimes filtered output hides what you need. The escape hatch is `gtk proxy`:

```bash
gtk proxy git log -10   # full unfiltered output
```

You need this when:
- Filtered output doesn't explain a failure
- You want to see passing tests, not just failures
- You need full diff content, not just stats
- A warning or log line might be relevant to the issue

Claude is aware of the option to bypass and is instructed to use `gtk proxy` whenever the output is not clear (for instance a failing test is only labeled as failed, without the details). When confronted with that, Claude can rerun the command with `gtk proxy` to get the full original output.

In practice I see Claude using this a few times a day. The filters are conservative enough that failures and errors always come through, but since this happens regularly, the savings are not as great as one would expect at first.

## What It Doesn't Do

gtk is not a general-purpose output compressor. It doesn't try to summarize arbitrary text or use any AI to decide what's relevant. Each filter is hand-written for a specific command and knows exactly what matters for that command. There's no magic, no heuristics beyond "does this line match a known noise pattern."

It also doesn't help with non-CLI token costs. If you're burning tokens on large file reads or massive prompts, gtk won't touch those. It only filters shell command output. It only works on bash commands.

## The End Result?

Inconclusive. I think I save tokens, but not as much as I hoped: it is not a day and night difference. It is hard to properly measure. Does the LLM result improve? Hard to say. Do I get more meaningful conversations? Hard to say. Does Claude's regular use of `gtk proxy` negate the savings? Not completely, but it happens often enough to have an impact.

The only way to say for sure requires a lot more data and a lot more proper testing. Not something I am going to do. For now I will keep it running in my setup: it does no harm and I think I see a benefit in token usage, but I cannot prove it.

If the concept interests you, just use [rtk](https://github.com/rtk-ai/rtk). It is well-maintained, supports more tools than my version, and integrates with most AI coding agents out of the box. I built my own because I wanted to customize the filters for my specific workflow, but for most people rtk will do everything you need.

---

*Building your own Claude Code tooling? <a href="#" onclick="task1(); return false;">Get in touch</a> to compare notes.*

## Resources

- [rtk (Rust Token Killer)](https://github.com/rtk-ai/rtk) -- the original Rust project that inspired gtk
- [rtk website](https://www.rtk-ai.app/) -- documentation and install instructions for rtk
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) -- how PreToolUse hooks work
- [Securing YOLO Mode](/ai/security/development/tools/2026/02/01/securing-claude-code-hooks-best-practices.html) -- my earlier post on using hooks for security
