# Draft to Blog Post

Transform the draft at `$ARGUMENTS` into a polished blog post for albertsikkema.com.

## Steps

1. **Read the draft** at the provided path and identify the core topic and any external references mentioned

2. **Read 3-4 recent posts** from `_posts/` to match my writing style:
   - Personal, direct, conversational tone
   - Start with real problem or personal experience
   - Structure: Problem → Solution → Implementation → Trade-offs
   - Honest about limitations ("when NOT to use this")
   - End with LinkedIn call-to-action

3. **Search the web** for any tools/projects/references mentioned to include proper links

4. **Write the post** following CLAUDE.md guidelines:
   - Do NOT copy the draft's style if it's AI-generated - use my voice
   - Add front matter: layout, title, date (today), categories, description (150-160 chars), keywords
   - Include inline links to sources, not just in Resources section
   - Keep it concise - cut fluff

5. **Critical self-review** - ask yourself "would I read this?" Check for:
   - Bait and switch (does the intro promise something the post doesn't deliver?)
   - Dry sections that read like documentation instead of a story
   - Abrupt endings with no connection back to the opening
   - Missing practical nuance (when to use, when NOT to use)

6. **Fix structural issues** before presenting:
   - If the intro mentions a project, tie back to it at the end
   - If there are lists/tables, add context around them

7. **Save to** `_posts/YYYY-MM-DD-slug.md` using today's date

8. **Give honest feedback** on what works and what's still weak
