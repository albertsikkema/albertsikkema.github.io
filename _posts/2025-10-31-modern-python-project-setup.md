---
layout: post
title: "Modern Python Project Setup: My 2025 Developer's Stack"
date: 2025-10-31
categories: python development best-practices
description: "Modern Python development stack for 2025 featuring uv, ruff, pytest, pydantic, and Docker. Fast, type-safe, and production-ready project setup."
keywords: "Python 3.14, uv package manager, ruff formatter, pytest, pydantic, Python project setup, modern Python development"
---

I've set up dozens of Python projects over the years, and I've watched the tooling evolve from pip and virtualenv to poetry, pipenv, and back to pip. So let me share what my current go-to setup is!

## The Stack

- **Python 3.14** - Latest stable release
- **uv** - Fast package management
- **ruff** - Linter and formatter
- **pytest** - Given the name: it tests
- **pydantic** - data validation: solving the missing type integration in python
- **pydanticai** - LLM integration
- **pylance** - Type checking in VS Code
- **docker** - Deploy in containers
- **pre-commit** - Catch issues early (and keep your codebase as clean as possible)

So how do these tools work?

## Python 3.14

The latest Python release is 3.14. If you want to know what exactly changed: look it up at the website or one of the trillion tutorials and blogs a search will provide you with. Starting a new project? just use the latest version. And the next one (3.15) is scheduled for release in October 2026. 

## uv: Package Management That's Actually Fast

A lot faster than the old 'pip': [uv](https://github.com/astral-sh/uv). It's written in Rust and it's **fast**. I haven't measured exactly, but I think it is at least 10x faster.

Besides the speed benefit, the dependencies are handled better, for instance you can now specify whether a dependency is used in dev only or in dev and production etc. So more consistency and control.

Oh, and it handles your virtual environment for you. No more manual venv handling.

## ruff: One Tool to Rule Them All

Up until not too long ago I was used to needing black for formatting and flake8 for linting. [ruff](https://github.com/astral-sh/ruff) replaces both.

Written in Rust, it's 10-100x faster than the tools it replaces. (not checked myself, but that is what I read and matches my experience so far)

The same command for checking and formatting in almost no time. Easy!

## pytest: Testing

[pytest](https://docs.pytest.org/) has been the standard for years, and for good reason. Simple assertions, powerful fixtures, excellent plugin ecosystem.

As you know from previous posts: I hate writing tests. Combine pytest with an AI assistant and away we go!

## pydantic: Type Safety That Works at Runtime

Python's type hints are great for static analysis, but they don't validate at runtime. [pydantic](https://docs.pydantic.dev/) fixes that. Using models it is quite easy to model your data at different stages of your application, helping to make sure strange type errors do not show up in production but are solved during development. Not quite as good as Rust, but a nice improvement compared to basic Python (which has no inherent typing at all. Which does have its benefits BTW.)

## pydanticai: LLM Integration with Types

If you're building LLM-powered features (and in 2025, who isn't?), [pydanticai](https://ai.pydantic.dev/) makes it simpler. Built on top of pydantic, it gives you type-safe LLM interactions. Why bother? well, for once it makes it easier to have the LLM return structured responses.

And the 'new' graph library for pydanticai is really helpful for more complex agent setups.

## pylance: Type Checking in Your Editor

[Pylance](https://github.com/microsoft/pylance-release) is the default language server for Python in VS Code. Nothing more to say apart from that it just works. 

## docker: Deploy Consistently

The standard for deploying containerized applications, consistency between environments and server configs is key here. There are some alternatives like Podman, or when you have higher requirements for uptime and scalability Kubernetes (K3S). But for most stuff this is great!

## pre-commit: Catch Issues Early

[pre-commit](https://pre-commit.com/) runs checks before you commit. Formatting, linting, type checking—all happen locally before code review. The hook won't let you commit code that does not pass the steps you defined. And because it is part of the application setup itself, it works for your entire team. (in contrast to the precommit hook in .github, which every developer would have to install and maintain themselves. Quite annoying. So precommit solves that)


## Why This Stack

**Speed** - uv and ruff are written in Rust. Noticeably faster than pure Python alternatives.

**Simplicity** - One package manager, one linter/formatter, one testing framework. No decision fatigue.

**Type Safety** - pydantic validates at runtime, pylance catches errors in your editor, pre-commit enforces before commit.

**AI-Ready** - pydanticai makes LLM integration straightforward and type-safe.

**Deployment** - Docker ensures consistency across environments.

**Developer Experience** - Tools work together without configuration hell.

## What About X?

**Poetry?** uv is faster and simpler.

**mypy?** pylance handles type checking needs.

**black?** ruff format implements black's style.

**Virtual environments?** uv handles this automatically with `uv sync`.


## Try It

Set up your next project with this stack. The initial configuration takes 5 minutes. The time savings and fewer bugs will pay back immediately. (or even better, create a template repo you can clone every time you start a new project)

The goal isn't to use the newest tools for their own sake. It's to use tools that genuinely improve the development experience—faster feedback loops, fewer bugs in production, less time debugging dependency issues.

That's what this stack delivers for me.

## Resources

### Package Management
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [pyenv](https://github.com/pyenv/pyenv) - Python version management

### Code Quality
- [ruff](https://github.com/astral-sh/ruff) - Fast Python linter and formatter
- [pylance](https://github.com/microsoft/pylance-release) - Python language server
- [pre-commit](https://pre-commit.com/) - Git hook framework

### Testing
- [pytest](https://docs.pytest.org/) - Testing framework
- [pytest-cov](https://pytest-cov.readthedocs.io/) - Coverage plugin
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) - Async test support

### Type Safety & Data Validation
- [pydantic](https://docs.pydantic.dev/) - Data validation using type hints
- [pydantic-ai](https://ai.pydantic.dev/) - LLM integration framework

### Deployment
- [Docker](https://www.docker.com/) - Containerization platform
- [uvicorn](https://www.uvicorn.org/) - ASGI server

### Python
- [Python 3.14](https://www.python.org/downloads/) - Latest Python release
- [What's New in Python 3.14](https://docs.python.org/3.14/whatsnew/3.14.html) - Release notes

---

*What's your Python setup looking like in 2025? Found tools that work better? I'd love to hear about it—<a href="#" onclick="task1(); return false;">get in touch</a>.*
