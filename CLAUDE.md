# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Jekyll-based static site blog deployed via GitHub Pages. The blog focuses on software engineering, Python development, AI/LLM integration, and technical best practices.

**Site URL**: https://www.albertsikkema.com
**Theme**: Minima (Jekyll default theme)
**Hosting**: GitHub Pages

## Development Commands

### Local Development
```bash
# Install dependencies
bundle install

# Run local development server
bundle exec jekyll serve

# The site will be available at http://localhost:4000
# Note: Changes to _config.yml require server restart
```

### Content Management
Blog posts are in `_posts/` with naming convention: `YYYY-MM-DD-title-slug.md`

## Blog Post Creation

### Post Front Matter Structure
```yaml
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD
categories: python security best-practices gdpr
---
```

### Writing Style Guidelines
- **Tone**: Personal, direct, practical. Avoid corporate/generic language
- **Opening**: Start with a real problem or personal experience
- **Structure**: Problem → Solution → Implementation → Trade-offs → Results
- **Code examples**: Complete and immediately usable
- **Honesty**: Include when NOT to use a pattern
- **Audience**: Backend developers, DevOps engineers, technical practitioners

### Image Formatting
Always use this HTML structure for images:

```html
<figure>
  <img src="/assets/images/[image-filename].png" alt="Descriptive alt text">
  <figcaption>This is what AI thinks an image for this blog should look like...</figcaption>
</figure>
```

**Guidelines**:
- Place images in `/assets/images/` directory
- Use descriptive filenames with hyphens (e.g., `gdpr-logging-diagram.png`)
- Always include meaningful alt text for accessibility
- Use the standard humorous figcaption format

### LinkedIn Post Format
When creating promotional posts for LinkedIn, follow this pattern:

```
My series of posts about Python you may find interesting (or not).

[2-3 sentences describing the problem and solution]

[Key metric or result]

[Link to post]

#Python #RelevantTags
```

## Architecture Notes

### Content Organization
- `_posts/`: Published blog posts (markdown files with YAML front matter)
- `_includes/`: Reusable HTML components (header, footer, etc.)
- `assets/images/`: Image files for blog posts
- `thoughts/`: Internal notes and best practices documents (not published)
- `about.markdown`: About page content

### Jekyll Configuration
- Theme: Minima 2.5
- Plugins: jekyll-feed (RSS feed generation)
- GitHub Pages version: 232 (locked for compatibility)

### Post Categories
Common categories used:
- `python development best-practices`
- `python security best-practices gdpr`
- `AI LLM development`

## Notes for Best Practices Documentation

When creating Blog Posts:
1. Focus on core insight
2. Remove verbose documentation and code references
3. Add personal intro explaining real-world problem
4. Include external resources in "Resources" section
5. Keep code examples but make them self-contained
