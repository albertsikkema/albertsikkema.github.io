# albertsikkema.com

Personal blog about software engineering, Python development, AI/LLM integration, and technical best practices.

**Live site**: https://www.albertsikkema.com

## Quick Start

```bash
# Install dependencies
bundle install

# Run local dev server
bundle exec jekyll serve

# Site available at http://localhost:4000
```

## Creating Posts

Posts go in `_posts/` with naming: `YYYY-MM-DD-title-slug.md`

```yaml
---
layout: post
title: "Your Post Title"
date: 2026-01-04
categories: python development
description: "SEO meta description (150-160 chars)"
keywords: "keyword1, keyword2"
---
```

## Tech Stack

- **Framework**: Jekyll
- **Theme**: Minima
- **Hosting**: GitHub Pages
- **Analytics**: Umami (self-hosted)

## SEO & AEO

The site includes:
- JSON-LD schema markup (Person, FAQPage, Article, Breadcrumb)
- `llms.txt` for AI crawlers and answer engines

**Remember to update `llms.txt`** when:
- Adding new services or expertise areas
- Changing site structure
- Adding notable projects

## License

Content is copyrighted. Code examples in blog posts are MIT licensed unless otherwise noted.
