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
description: "SEO-optimized meta description with target keywords (150-160 characters)"
keywords: "keyword1, keyword2, keyword3"
---
```

**Required fields:**
- `layout`: Always "post" for blog posts
- `title`: Post title (appears in search results)
- `date`: Publication date (YYYY-MM-DD format)

**Optional but recommended for SEO:**
- `description`: Meta description for search engines (150-160 chars, include primary keywords)
- `keywords`: Comma-separated list of relevant keywords
- `categories`: Used for site organization and schema markup

### SEO & Keyword Strategy

**Primary Niche Keywords** (use strategically in content):
- AI-assisted development
- Production-ready AI systems
- AI implementation
- Claude AI development / Claude AI integration
- OpenAI integration
- LLM integration
- AI agent orchestration
- Enterprise AI adoption
- AI-driven development

**Secondary Keywords**:
- Prompt engineering
- AI code generation
- Python AI development
- Azure AI solutions
- DevOps for AI
- AI security best practices
- Government AI compliance
- Healthcare AI systems

**Keyword Usage Guidelines**:
1. **Title**: Include 1-2 primary keywords naturally
2. **Meta description**: Include primary keyword + 1-2 related terms (150-160 chars)
3. **First paragraph**: Use primary keyword within first 100 words
4. **Headings (H2/H3)**: Include keywords in at least 2 section headings
5. **Throughout content**: Use keyword variations naturally (avoid stuffing)
6. **Conclusion**: Reinforce primary keyword in call-to-action or summary

**Example - Good SEO Title:**
- ✅ "Building Production-Ready AI Systems with Claude: A Practical Guide"
- ✅ "AI-Assisted Development: How I Built 10 Enterprise Apps in 3 Months"
- ❌ "How I Built Some Stuff with AI" (too vague, no keywords)

**Example - Good Meta Description:**
- ✅ "Learn AI-assisted development strategies for building production-ready AI systems. Step-by-step guide to Claude AI integration, prompt engineering, and enterprise AI adoption." (159 chars)
- ❌ "This post is about AI and how to use it for development." (too generic, no specifics)

### Writing Style Guidelines
- **Tone**: Personal, direct, practical. Avoid corporate/generic language
- **Opening**: Start with a real problem or personal experience (include primary keyword in first 100 words)
- **Structure**: Problem → Solution → Implementation → Trade-offs → Results
- **Code examples**: Complete and immediately usable
- **Honesty**: Include when NOT to use a pattern
- **Audience**: Backend developers, DevOps engineers, technical practitioners
- **SEO**: Naturally incorporate primary keywords throughout without keyword stuffing

### Image Formatting & Accessibility

**IMPORTANT**: Always include images with proper alt text for WCAG 2.1 AA compliance and better SEO.

Always use this HTML structure for images:

```html
<figure>
  <img src="/assets/images/[image-filename].png" alt="Descriptive alt text explaining what the image shows">
  <figcaption>This is what AI thinks an image for this blog should look like...</figcaption>
</figure>
```

**File Management**:
- Place images in `/assets/images/` directory
- Use descriptive filenames with hyphens (e.g., `gdpr-logging-diagram.png`)
- Preferred formats: WebP (best compression), PNG (diagrams/screenshots), JPG (photos)
- Optimize images before upload (aim for < 500KB for blog post images)

**Alt Text Best Practices** (WCAG 2.1 Level AA):
1. **Be descriptive and specific**: Describe what the image shows, not just its topic
   - ✅ "GDPR-compliant Python logging architecture diagram showing background thread filtering process"
   - ❌ "Logging diagram"
   - ✅ "Thermal printer setup on desk showing printed message from web interface with Raspberry Pi"
   - ❌ "Printer"

2. **Context matters**: Alt text should relate to the surrounding content
   - If the image illustrates a technical concept, describe the concept
   - If it shows a workflow, describe the steps
   - If it's a screenshot, describe what's visible and relevant

3. **Length guidelines**:
   - Aim for 125 characters or less (screen reader sweet spot)
   - For complex diagrams, consider adding a longer description in the caption or text

4. **Don't include**:
   - "Image of" or "Picture of" (screen readers announce it's an image)
   - File extensions or technical jargon unless relevant
   - Decorative information irrelevant to content

5. **SEO benefits**: Alt text helps search engines understand images
   - Include relevant keywords naturally
   - Helps images appear in Google Image Search
   - Contributes to overall page SEO

**When to use images**:
- Technical diagrams explaining architecture or workflows
- Screenshots showing UI/UX implementations
- Code structure visualizations
- Real-world examples of implementations
- Before/after comparisons

**Accessibility Tools**:
- Use [WebAIM's alt text decision tree](https://www.webaim.org/articles/alt/) for guidance
- Test with screen readers (VoiceOver on Mac, NVDA on Windows)
- Validate with [WAVE Web Accessibility Tool](https://wave.webaim.org/)

**Standard figcaption**: Use the humorous "This is what AI thinks an image for this blog should look like..." format unless the image is a screenshot, diagram, or technical illustration that needs specific attribution.

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
- `assets/js/`: JavaScript files (e.g., analytics scripts)
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
- `python development hardware raspberry-pi`

### Analytics
- **Analytics Platform**: Umami (self-hosted at umami.test001.nl)
- **Script Location**: `/assets/js/client.js` (served locally to bypass ad blockers)
- **Website ID**: b5fc2406-b860-447d-a93d-e0c02bc71263
- **Implementation**: Script tag in `_includes/head.html`

**Note**: The Umami script is downloaded and served locally from `/assets/js/client.js` (renamed from umami.js) instead of remotely to prevent ad blockers (like uBlock Origin) from blocking it. The generic filename helps avoid detection by ad blocker filter lists.

### Schema Markup (SEO)
The site uses JSON-LD structured data for enhanced search engine understanding:

- **WebSite Schema** (`_includes/website-schema.html`): Applied to all pages
  - Defines site metadata and search functionality
  - Enables Google search box in SERPs

- **Person Schema** (`_includes/schema.html`): Applied to homepage only
  - Professional profile with job title, skills, location
  - Work affiliations (ePublic Solutions, Albert Sikkema Consultancy)
  - Notable clients (Dutch government ministries, enterprises)
  - Awards (Smart City Award 2023)
  - Social media profiles (LinkedIn, GitHub)

- **BlogPosting Schema** (`_includes/article-schema.html`): Applied to blog posts
  - Article metadata (headline, description, dates)
  - Author information with social profiles
  - Categories and keywords
  - Enables rich results in Google Search

- **BreadcrumbList Schema** (`_includes/breadcrumb-schema.html`): Applied to all non-homepage pages
  - Navigation hierarchy for search engines
  - Improves site structure understanding

**Validation Tools**:
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema Markup Validator: https://validator.schema.org/

**Note**: Schema includes are managed in `_includes/head.html` with conditional logic based on page layout.

### Updating Blog Posts
When adding updates to existing blog posts:

1. Add update section with date as a heading: `## Update - November 9, 2024`
2. Place updates at the top of the post (after the introduction, before the first technical section)
3. Keep updates concise and conversational, matching the blog's tone
4. Add transition text like "Now let's get into it" to bridge back to the original content

**Example**:
```markdown
## Update - November 9, 2024

Thanks for all the messages so far! Really kind!

## Now let's get into it

[Original content continues...]
```

## Notes for Best Practices Documentation

When creating Blog Posts:
1. Focus on core insight
2. Remove verbose documentation and code references
3. Add personal intro explaining real-world problem
4. Include external resources in "Resources" section
5. Keep code examples but make them self-contained
