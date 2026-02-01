---
layout: post
title: "Securing YOLO Mode: How I Stop Claude Code from Nuking My System"
date: 2026-02-01
categories: ai security development tools
description: "Comprehensive guide to securing Claude Code with hooks, covering PreToolUse validation, dangerous command blocking, path traversal prevention, and practical security patterns."
keywords: "Claude Code security, hooks, PreToolUse, PostToolUse, input validation, path traversal, command injection, AI security, development security"
---

I always run Claude Code in YOLO mode. I have `cly` aliased to `claude --dangerously-skip-permissions` in my `.zshrc` because I want Claude to just get things done without asking me to approve every file write.

This works great for productivity, but it also means Claude has free rein to do whatever it wants. Format my hard disk? Sure. Leak my `.env` secrets to some random API? Why not. Force push to main? Go for it.

Obviously, I'd prefer to avoid those outcomes. The main thing here is: I don't let Claude run unsupervised for hours on my system, and I add plenty of other guardrails too. If you do want to experiment with that, please do it on a Raspberry Pi or a VPS, with nothing special on it. But that's not the subject here.

This post is about hooks: one specific defense layer I researched (again) while updating my claude workflow. Hooks let you intercept and block dangerous operations before they execute, even in YOLO mode. This post documents what I learned. Maybe it helps you too.

Hooks are also fun to use for alerts. This afternoon I added audio phrases from Command & Conquer and Red Alert to some of my hooks. Adding those sounds brought back a lot of fun memories of hours of playing. "Well done, Commander!"

<figure>
  <img src="/assets/images/claude-code-hooks-red-alert.jpg" alt="Command and Conquer Red Alert 2 artwork featuring Soviet and Allied forces">
  <figcaption>Well done, Commander! Your hooks are ready. (Source: <a href="https://wallpapercave.com/w/wp10090474">Wallpaper Cave</a>, uploaded by kallie)</figcaption>
</figure>

From here on, this has nothing to do with Red Alert or Command & Conquer. But it *is* about defending your computer and software, so there is some sort of match there :-)

**Reader warning:** This is a long and boring post. Only read if you're interested in securing your Claude Code setup with hooks, blocking dangerous commands, preventing path traversal attacks, or protecting sensitive files. Use it as a reference, but never trust it blindly. Don't say I didn't warn you!

## Table of Contents

- [Why Hooks Matter for Security](#why-hooks-matter-for-security)
- [The Hook Lifecycle](#the-hook-lifecycle)
- [Blocking Dangerous Commands](#blocking-dangerous-commands)
- [Input Validation Best Practices](#input-validation-best-practices)
- [Path Traversal Prevention](#path-traversal-prevention)
- [Protecting Sensitive Files](#protecting-sensitive-files)
- [Complete Real-World Implementation](#complete-real-world-implementation)
- [PermissionRequest Hooks](#permissionrequest-hooks)
- [Known CVEs and Vulnerabilities](#known-cves-and-vulnerabilities)
- [Exit Code Reference](#exit-code-reference)
- [Comprehensive Security Checklist](#comprehensive-security-checklist)
- [Defense in Depth](#defense-in-depth)
- [Final Thoughts](#final-thoughts)
- [Sources and Further Reading](#sources-and-further-reading)

## Why Hooks Matter for Security

Hooks are user-defined shell commands or LLM prompts that execute automatically at specific points in Claude Code's lifecycle. They execute with your full user permissions, meaning they can read, modify, or delete any file your account can access.

This is both the opportunity and the risk. Without proper controls, Claude Code could:
- Execute destructive shell commands like `rm -rf`
- Access sensitive files containing credentials
- Modify system configurations
- Expose secrets in logs or outputs

Hooks let you build guardrails that operate deterministically: unlike CLAUDE.md instructions that are "parsed by LLM, weighed against other context, maybe followed," hooks execute regardless of what Claude thinks it should do.

## The Hook Lifecycle

Understanding when hooks fire is essential for effective security. Here are the most relevant events for security purposes (Claude Code has additional events like `Notification`, `SubagentStart`, `SubagentStop`, and `PreCompact`):

| Event                | When it fires                                        |
| :------------------- | :--------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                     |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it |
| `PreToolUse`         | Before a tool call executes: can block it             |
| `PermissionRequest`  | When a permission dialog appears                     |
| `PostToolUse`        | After a tool call succeeds                           |
| `PostToolUseFailure` | After a tool call fails                              |
| `Stop`               | When Claude finishes responding                      |
| `SessionEnd`         | When a session terminates                            |

For security, `PreToolUse` is your primary defense: it runs before dangerous operations execute and can block them entirely.

## Blocking Dangerous Commands

The most common security use case is blocking destructive shell commands. The examples below show the concepts step by step. If you want to skip ahead to a complete, production-ready implementation, jump to [Complete Real-World Implementation](#complete-real-world-implementation).

Here's a practical implementation:

### Basic Configuration

Add this to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-dangerous.sh"
          }
        ]
      }
    ]
  }
}
```

### The Blocking Script

```bash
#!/bin/bash
# .claude/hooks/block-dangerous.sh

COMMAND=$(jq -r '.tool_input.command' < /dev/stdin)

# Block rm -rf variants (handles -rf, -fr, -r -f, etc.)
if echo "$COMMAND" | grep -qE 'rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-rf|-fr)\b'; then
  echo "Blocked: rm -rf commands are not allowed" >&2
  exit 2
fi

# Block force pushes to main/master
if echo "$COMMAND" | grep -qE 'git\s+push.*--force.*(main|master)'; then
  echo "Blocked: Force push to main/master not allowed" >&2
  exit 2
fi

# Block sudo rm
if echo "$COMMAND" | grep -qE 'sudo\s+rm'; then
  echo "Blocked: sudo rm commands require manual approval" >&2
  exit 2
fi

# Block chmod 777
if echo "$COMMAND" | grep -qE 'chmod\s+777'; then
  echo "Blocked: chmod 777 is a security risk" >&2
  exit 2
fi

exit 0  # Allow the command
```

Exit code 2 tells Claude Code to block the operation and feed the error message back to Claude, who can then explain the issue and suggest alternatives.

### Configurable Safety Levels

For more flexibility, consider implementing configurable safety levels:

- **critical**: Block only catastrophic operations (rm -rf ~, fork bombs, dd to disk)
- **high**: Add risky operations (force push main, secrets exposure, git reset --hard)
- **strict**: Add cautionary items (any force push, sudo rm, docker prune)

## Input Validation Best Practices

Hook input arrives via JSON on stdin. Never trust it blindly. Here are essential validation patterns:

### Always Quote Variables

```bash
# Bad - breaks with spaces or special characters
FILE_PATH=$TOOL_INPUT

# Good - handles all path types
FILE_PATH="$TOOL_INPUT"
```

### Validate Before Processing

```bash
#!/bin/bash
INPUT=$(cat)

# Extract with fallbacks
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Check if value exists
if [ -z "$FILE_PATH" ]; then
  exit 0  # No file path to validate
fi

# Validate the path looks reasonable (don't check existence - file might be new)
# Add your validation logic here
```

### Check Tool Availability

```bash
if ! command -v prettier &> /dev/null; then
  exit 0  # Tool not available, skip gracefully
fi
```

## Path Traversal Prevention

Path traversal attacks like `../../etc/passwd` are a significant risk. Here's how to prevent them:

### Simple Detection

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Block obvious path traversal
if echo "$FILE_PATH" | grep -q '\.\.'; then
  echo '{"decision":"block","reason":"Path traversal detected"}'
  exit 0
fi

# Ensure path is within project (CVE-2025-54794: use trailing separator)
PROJECT_DIR="$CLAUDE_PROJECT_DIR"
RESOLVED_PATH=$(realpath -m "$FILE_PATH" 2>/dev/null)

# Add trailing slash to prevent /project matching /project_malicious
if [[ ! "$RESOLVED_PATH" == "$PROJECT_DIR" && ! "$RESOLVED_PATH" == "$PROJECT_DIR/"* ]]; then
  echo '{"decision":"block","reason":"Path is outside project directory"}'
  exit 0
fi

exit 0
```

### Python Implementation

For more robust validation, use Python:

```python
#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

input_data = json.load(sys.stdin)
file_path = input_data.get('tool_input', {}).get('file_path', '')

if not file_path:
    sys.exit(0)

project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())).resolve()
target_path = (project_dir / file_path).resolve()

# CVE-2025-54794: Must check with trailing separator to prevent
# /project matching /project_malicious
project_str = str(project_dir)
target_str = str(target_path)

if not (target_str == project_str or target_str.startswith(project_str + os.sep)):
    print(json.dumps({
        "decision": "block",
        "reason": "Path is outside project directory"
    }))
    sys.exit(0)

sys.exit(0)
```

## Protecting Sensitive Files

Create a blocklist for files that should never be accessed:

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Sensitive file patterns
SENSITIVE_PATTERNS=(
  "\.env$"
  "\.env\."
  "\.pem$"
  "\.key$"
  "\.p12$"
  "credentials\.json"
  "secrets\.yaml"
  "\.git/config$"
  "id_rsa"
  "id_ed25519"
)

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
  if echo "$FILE_PATH" | grep -qE "$pattern"; then
    echo "Blocked: Access to sensitive file not allowed" >&2
    exit 2
  fi
done

exit 0
```

## Complete Real-World Implementation

The snippets above are useful for understanding individual concepts, but here's the actual Python hook I use. It combines all the security checks into a single, comprehensive PreToolUse hook:

```python
#!/usr/bin/env python3
"""
PreToolUse security hook that blocks dangerous operations.

Checks for:
- Dangerous rm commands
- Fork bombs
- Dangerous git commands (push to main/master, force push)
- Disk write attacks (dd to /dev/)
- Sensitive file access (.env, .pem, .key, credentials, etc.)
- Path traversal attacks
- Project directory escape

Set CLAUDE_HOOKS_DEBUG=1 to enable debug logging.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# Debug mode for troubleshooting
DEBUG = os.environ.get('CLAUDE_HOOKS_DEBUG', '').lower() in ('1', 'true')

# Pre-compiled regex patterns for performance
DANGEROUS_RM_PATTERNS = [
    re.compile(r'\brm\s+.*-[a-z]*r[a-z]*f'),  # rm -rf, rm -fr, rm -Rf, etc.
    re.compile(r'\brm\s+.*-[a-z]*f[a-z]*r'),  # rm -fr variations
    re.compile(r'\brm\s+--recursive\s+--force'),
    re.compile(r'\brm\s+--force\s+--recursive'),
    re.compile(r'\brm\s+-r\s+.*-f'),
    re.compile(r'\brm\s+-f\s+.*-r'),
]

DANGEROUS_RM_PATH_PATTERNS = [
    re.compile(r'\s/$'),          # Root directory
    re.compile(r'\s/\*'),         # Root with wildcard
    re.compile(r'\s~/?'),         # Home directory
    re.compile(r'\s\$HOME'),      # Home environment variable
    re.compile(r'\s\.\./?'),      # Parent directory references
    re.compile(r'\s\.$'),         # Current directory
]

RM_RECURSIVE_PATTERN = re.compile(r'\brm\s+.*-[a-z]*r')

FORK_BOMB_PATTERNS = [
    re.compile(r':\(\)\s*\{\s*:\|:&\s*\}\s*;:'),  # Classic bash fork bomb
    re.compile(r'\.\/\w+\s*&\s*\.\/\w+'),  # Self-replicating pattern
    re.compile(r'while\s+true.*fork', re.IGNORECASE),
    re.compile(r'fork\s*\(\s*\)\s*while', re.IGNORECASE),
]

DANGEROUS_GIT_PATTERNS = [
    # Block ALL pushes to main/master (including regular push)
    re.compile(r'git\s+push\s+.*\b(main|master)\b'),
    re.compile(r'git\s+push\s+origin\s+(main|master)'),
    # Block force push without explicit branch (might be on main)
    re.compile(r'git\s+push\s+.*--force'),
    re.compile(r'git\s+push\s+.*-f\b'),
    # Other dangerous commands
    re.compile(r'git\s+reset\s+--hard\s+origin/'),
    re.compile(r'git\s+clean\s+-fd'),  # Force delete untracked files
]

DANGEROUS_DISK_PATTERNS = [
    re.compile(r'\bdd\s+.*of=/dev/'),  # dd to device
    re.compile(r'\bmkfs\.'),  # Format filesystem
    re.compile(r'>\s*/dev/sd'),  # Write to disk device
]

ENV_ACCESS_PATTERNS = [
    re.compile(r'\bcat\s+[^\|]*\.env\b(?!\.sample|\.example|\.template)'),
    re.compile(r'\bless\s+[^\|]*\.env\b(?!\.sample|\.example|\.template)'),
    re.compile(r'\bhead\s+[^\|]*\.env\b(?!\.sample|\.example|\.template)'),
    re.compile(r'\btail\s+[^\|]*\.env\b(?!\.sample|\.example|\.template)'),
    re.compile(r'>\s*[^\s]*\.env\b(?!\.sample|\.example|\.template)'),
    re.compile(r'\bcp\s+[^\|]*\.env\b(?!\.sample|\.example|\.template)'),
    re.compile(r'\bmv\s+[^\|]*\.env\b(?!\.sample|\.example|\.template)'),
    re.compile(r'\bsource\s+[^\|]*\.env\b(?!\.sample|\.example|\.template)'),
    re.compile(r'\.\s+[^\|]*\.env\b(?!\.sample|\.example|\.template)'),
]

SENSITIVE_FILE_PATTERNS = [
    (re.compile(r'\.pem$'), 'PEM certificate/key file'),
    (re.compile(r'\.key$'), 'Key file'),
    (re.compile(r'\.p12$'), 'PKCS12 certificate'),
    (re.compile(r'\.pfx$'), 'PFX certificate'),
    (re.compile(r'credentials\.(json|yaml|yml|xml|ini|conf)$'), 'Credentials file'),
    (re.compile(r'secrets?\.(json|yaml|yml|xml|ini|conf)$'), 'Secrets file'),
    (re.compile(r'\.kube/config'), 'Kubernetes config'),
    (re.compile(r'\.aws/credentials'), 'AWS credentials'),
    (re.compile(r'\.ssh/'), 'SSH directory'),
    (re.compile(r'\.gnupg/'), 'GPG directory'),
    (re.compile(r'\.netrc'), 'Netrc file'),
    (re.compile(r'\.npmrc'), 'NPM config with tokens'),
    (re.compile(r'\.pypirc'), 'PyPI config with tokens'),
]

SENSITIVE_FILES = {
    '.env', '.env.local', '.env.production', '.env.development',
    'id_rsa', 'id_ed25519', 'id_ecdsa', 'id_dsa',
}

ALLOWED_ENV_FILES = {'.env.sample', '.env.example', '.env.template'}


def debug_log(message: str) -> None:
    """Log debug message if debug mode is enabled."""
    if DEBUG:
        print(f"[DEBUG] {message}", file=sys.stderr)


def is_dangerous_rm_command(command: str) -> bool:
    """Detect dangerous rm commands."""
    normalized = ' '.join(command.lower().split())

    for pattern in DANGEROUS_RM_PATTERNS:
        if pattern.search(normalized):
            return True

    if RM_RECURSIVE_PATTERN.search(normalized):
        for pattern in DANGEROUS_RM_PATH_PATTERNS:
            if pattern.search(normalized):
                return True
    return False


def is_fork_bomb(command: str) -> bool:
    """Detect fork bomb patterns."""
    for pattern in FORK_BOMB_PATTERNS:
        if pattern.search(command):
            return True
    return False


def is_dangerous_git_command(command: str) -> bool:
    """Detect dangerous git commands."""
    normalized = ' '.join(command.lower().split())
    for pattern in DANGEROUS_GIT_PATTERNS:
        if pattern.search(normalized):
            return True
    return False


def is_dangerous_disk_write(command: str) -> bool:
    """Detect dangerous disk write operations."""
    normalized = ' '.join(command.lower().split())
    for pattern in DANGEROUS_DISK_PATTERNS:
        if pattern.search(normalized):
            return True
    return False


def is_sensitive_file(file_path: str) -> tuple[bool, str | None]:
    """Check if file path points to sensitive files."""
    if not file_path:
        return False, None

    path_lower = file_path.lower()
    basename = os.path.basename(path_lower)

    if basename in ALLOWED_ENV_FILES:
        return False, None

    if basename in SENSITIVE_FILES:
        return True, f"Access to {basename} files is prohibited"

    for pattern, description in SENSITIVE_FILE_PATTERNS:
        if pattern.search(path_lower):
            return True, f"Access to {description} is prohibited"

    return False, None


def is_path_escape(file_path: str, project_dir: str) -> tuple[bool, str | None]:
    """Check if path escapes the project directory."""
    if not file_path or not project_dir:
        return False, None

    try:
        abs_path = Path(file_path).resolve()
        abs_project = Path(project_dir).resolve()

        # CVE-2025-54794: Must check with trailing separator to prevent
        # /project matching /project_malicious
        project_str = str(abs_project)
        path_str = str(abs_path)

        if not (path_str == project_str or path_str.startswith(project_str + os.sep)):
            return True, "Path is outside project directory"

        if '..' in file_path:
            return True, "Path traversal attempt detected"

    except (ValueError, OSError):
        return True, "Invalid path"

    return False, None


def check_bash_command(command: str) -> str | None:
    """Check bash command for dangerous patterns."""
    if is_dangerous_rm_command(command):
        return "Dangerous rm command detected"
    if is_fork_bomb(command):
        return "Fork bomb detected"
    if is_dangerous_git_command(command):
        return "Dangerous git command detected (push to main/master or force push)"
    if is_dangerous_disk_write(command):
        return "Dangerous disk write operation detected"

    for pattern in ENV_ACCESS_PATTERNS:
        if pattern.search(command):
            return "Access to .env files is prohibited"

    return None


def check_file_operation(tool_name: str, tool_input: dict, project_dir: str) -> str | None:
    """Check file operations for security issues."""
    file_path = tool_input.get('file_path', '')

    if tool_name == 'Grep':
        file_path = tool_input.get('path', '') or file_path
    if tool_name == 'Glob':
        file_path = tool_input.get('path', '') or file_path

    if not file_path:
        return None

    is_sensitive, reason = is_sensitive_file(file_path)
    if is_sensitive:
        return reason

    if os.path.isabs(file_path) or '..' in file_path:
        is_escape, reason = is_path_escape(file_path, project_dir)
        if is_escape:
            return reason

    return None


def main() -> None:
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())

        debug_log(f"Checking tool: {tool_name}")

        if tool_name == 'Bash':
            command = tool_input.get('command', '')
            error = check_bash_command(command)
            if error:
                print(f"BLOCKED: {error}", file=sys.stderr)
                sys.exit(2)

        if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write', 'Glob', 'Grep']:
            error = check_file_operation(tool_name, tool_input, project_dir)
            if error:
                print(f"BLOCKED: {error}", file=sys.stderr)
                sys.exit(2)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)  # Fail open on parse errors
    except Exception:
        sys.exit(0)  # Fail open on unexpected errors


if __name__ == '__main__':
    main()
```

Save this as `.claude/hooks/pre_tool_use.py` and configure it in your settings:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py\""
          }
        ]
      }
    ]
  }
}
```

Key design decisions in this implementation:

1. **Pre-compiled regex patterns** for better performance on repeated checks
2. **Fail-open on errors** (`sys.exit(0)`) so parsing failures don't break your workflow
3. **Debug mode** via `CLAUDE_HOOKS_DEBUG=1` for troubleshooting
4. **CVE-2025-54794 fix** with proper path prefix checking using `os.sep`
5. **Allows safe variants** like `.env.sample` and `.env.example`
6. **Covers multiple tools** including Bash, Read, Edit, Write, Glob, and Grep

## PermissionRequest Hooks

The `PermissionRequest` hook (v2.0.45+) triggers when Claude Code displays a permission dialog, allowing automatic approve/deny decisions:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/permission-handler.sh"
          }
        ]
      }
    ]
  }
}
```

### Auto-Approve Safe Operations

```bash
#!/bin/bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Auto-approve read-only tools
if [[ "$TOOL_NAME" =~ ^(Read|Glob|Grep)$ ]]; then
  echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}'
  exit 0
fi

# Auto-approve safe npm commands
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$COMMAND" =~ ^npm\ (test|run\ lint|run\ build) ]]; then
  echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}'
  exit 0
fi

# Deny dangerous patterns
if echo "$COMMAND" | grep -qE 'rm\s+-rf'; then
  echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"deny","message":"Destructive command blocked"}}}'
  exit 0
fi

# Default: show permission prompt
exit 0
```

Note: `PermissionRequest` hooks do not fire in non-interactive mode (`-p`). Use `PreToolUse` hooks for automated permission decisions.

## Known CVEs and Vulnerabilities

Several vulnerabilities have been discovered in Claude Code over time. If you're running a recent version (2.1.12 at time of writing), these are all patched. They're listed here to illustrate the types of attacks that hooks can help defend against:

| CVE | Issue |
|-----|-------|
| CVE-2025-54794 | Path restriction bypass via matching directory prefixes |
| CVE-2025-54795 | Command injection via improper input sanitization |
| CVE-2025-52882 | WebSocket authentication bypass allowing remote code execution |
| CVE-2025-66032 | [8 different command execution bypasses](https://flatt.tech/research/posts/pwning-claude-code-in-8-different-ways/) (led to blocklist → allowlist redesign) |

Check [Anthropic's releases](https://github.com/anthropics/claude-code/releases) for the latest patched versions.

### General Mitigation

- Never execute development tools in untrusted directories
- Use strong sandboxing and isolation
- Treat Claude Code output as unverified
- Keep prompts precise and exclude sensitive data

## Exit Code Reference

Understanding exit codes is essential:

| Exit Code | Meaning | Effect |
|-----------|---------|--------|
| 0 | Success | Allow operation; JSON on stdout is processed |
| 2 | Blocking error | Block operation; stderr shown to Claude |
| Other | Non-blocking error | Continue; stderr shown to user only |

Choose one approach per hook, either exit codes alone or exit 0 with JSON output. Don't mix them; Claude Code ignores JSON when you exit 2.

## Comprehensive Security Checklist

Before deploying hooks in production:

- [ ] Validate all input from stdin
- [ ] Quote all file paths and variables
- [ ] Use absolute paths for scripts (via `$CLAUDE_PROJECT_DIR`)
- [ ] Block sensitive files (.env, *.key, .git/*)
- [ ] Handle missing tools gracefully
- [ ] Set reasonable timeout (default 60s)
- [ ] Log errors to stderr or log file
- [ ] Test with edge cases (spaces, Unicode, missing files)
- [ ] Test hooks before deploying (see below)
- [ ] Consider disabling hooks when not needed

### Testing Your Hooks

Before deploying, test your hooks with sample input:

```bash
# Test dangerous command blocking
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | python3 .claude/hooks/pre_tool_use.py
echo $?  # Should be 2 (blocked)

# Test safe command
echo '{"tool_name":"Bash","tool_input":{"command":"ls -la"}}' | python3 .claude/hooks/pre_tool_use.py
echo $?  # Should be 0 (allowed)

# Test sensitive file blocking
echo '{"tool_name":"Read","tool_input":{"file_path":".env"}}' | python3 .claude/hooks/pre_tool_use.py
echo $?  # Should be 2 (blocked)
```

## Defense in Depth

Implement security at multiple layers:

1. **UserPromptSubmit** - Validate prompts before Claude processes them
2. **PreToolUse** - Block dangerous operations before execution
3. **PermissionRequest** - Auto-approve safe operations, deny dangerous ones
4. **PostToolUse** - Validate results and provide feedback
5. **Deny lists** - Add explicit permission denials in settings

```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(terraform destroy:*)",
      "Bash(docker system prune:*)"
    ]
  }
}
```

## Final Thoughts

Claude Code hooks provide powerful security controls, but they require careful implementation. The key principles:

1. **Hooks execute deterministically** - Unlike CLAUDE.md rules, hooks cannot be bypassed
2. **Validate everything** - Never trust input data
3. **Exit code 2 blocks** - Use it for security violations
4. **Defense in depth** - Implement multiple security layers
5. **Stay updated** - Patch promptly when vulnerabilities are discovered

Security isn't about preventing all possible risks: it's about reducing attack surface while maintaining productivity. Well-designed hooks let you work confidently with AI assistance while protecting your systems from accidental or malicious damage.

## Sources and Further Reading

### Official Documentation

- [Hooks Reference - Claude Code Docs](https://code.claude.com/docs/en/hooks) - The official reference documentation
- [Automate Workflows with Hooks Guide](https://code.claude.com/docs/en/hooks-guide) - Quickstart guide with examples
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Anthropic's official best practices
- [Agent SDK Hooks](https://platform.claude.com/docs/en/agent-sdk/hooks) - Hooks in the Agent SDK

### Security Resources

- [Claude Code Security Best Practices - Backslash](https://www.backslash.security/blog/claude-code-security-best-practices)
- [A Deep Dive into Security for Claude Code - Eesel](https://www.eesel.ai/blog/security-claude-code)
- [Claude Code Security: Enterprise Best Practices - MintMCP](https://www.mintmcp.com/blog/claude-code-security)
- [Claude Hooks Best Practices - PRPM](https://prpm.dev/blog/claude-hooks-best-practices)
- [Are Claude Skills Secure? Threat Model & Permissions - Skywork](https://skywork.ai/blog/ai-agent/claude-skills-security-threat-model-permissions-best-practices-2025/)

### CVE Details and Security Advisories

- [CVE-2025-54795: InversePrompt - Cymulate](https://cymulate.com/blog/cve-2025-547954-54795-claude-inverseprompt/)
- [CVE-2025-52882: WebSocket Authentication Bypass - Datadog Security Labs](https://securitylabs.datadoghq.com/articles/claude-mcp-cve-2025-52882/)
- [Arbitrary Code Execution Advisory - Redguard](https://www.redguard.ch/blog/2025/12/19/advisory-anthropic-claude-code/)
- [Claude AI Flaws: Unauthorized Commands - GBHackers](https://gbhackers.com/claude-ai-flaws/)

### Tutorials and Guides

- [Claude Code Hooks: A Practical Guide - DataCamp](https://www.datacamp.com/tutorial/claude-code-hooks)
- [The Ultimate Claude Code Guide - DEV Community](https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45)
- [Claude Code Hook Examples - Steve Kinney](https://stevekinney.com/courses/ai-development/claude-code-hook-examples)
- [Block Dangerous Commands - Perrotta.dev](https://perrotta.dev/2025/12/claude-code-block-dangerous-commands/)
- [Hooks for Automated Quality Checks - Luiz Tanure](https://www.letanure.dev/blog/2025-08-06--claude-code-part-8-hooks-automated-quality-checks)
- [Claude Code Hooks: Guardrails That Work - Paddo.dev](https://paddo.dev/blog/claude-code-hooks-guardrails/)
- [How to Configure Hooks - Claude Blog](https://claude.com/blog/how-to-configure-hooks)

### GitHub Repositories

- [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - Comprehensive hooks examples and patterns
- [claude-code-bash-guardian](https://github.com/RoaringFerrum/claude-code-bash-guardian) - Automated security layer for Bash hooks
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - Curated list of skills, hooks, and plugins
- [claude-code-hooks](https://github.com/karanb192/claude-code-hooks) - Collection of useful hooks
- [claude-code-damage-control](https://github.com/disler/claude-code-damage-control) - Safety hooks
- [everything-claude-code](https://github.com/affaan-m/everything-claude-code) - Complete configuration collection
- [claude-code-security-review](https://github.com/anthropics/claude-code-security-review) - AI-powered security review GitHub Action

### Community Resources

- [ClaudeLog - Hooks Documentation](https://claudelog.com/mechanics/hooks/)
- [.claude Directory - Hooks](https://dotclaude.com/hooks)
- [Claude Code CLI Cheatsheet - Shipyard](https://shipyard.build/blog/claude-code-cheat-sheet/)
- [GitButler - Claude Code Hooks](https://docs.gitbutler.com/features/ai-integration/claude-code-hooks)
- [Permission Hook Guide - Claude Fast](https://claudefa.st/blog/tools/hooks/permission-hook-guide)

---

*No, I didn't read every single detail of every link. I also use this post as a reference for myself when I need to look something up later.*

*Working with Claude Code in production? I'd love to hear about your security patterns and hook implementations. [Get in touch](/contact) to share your experiences.*
