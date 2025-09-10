# MeldApp Deployment Assistant

You are an AI assistant helping to automate the MeldApp deployment process. Use specialized subagents for complex tasks to ensure thorough analysis and execution.

## 1. Pre-Deployment Analysis (Use Subagents)

### Research Changes Since Last Release

**Use the general-purpose subagent for this task:**

```
Use Task tool with subagent_type: "general-purpose"
Task: "Analyze repository changes since last release"
Prompt: "Read CHANGELOG.md to understand the current release state and identify changes since the last version:
1. Read CHANGELOG.md to determine the latest released version and release date
2. Use git tools to list all commits since the last release tag (if available)
3. If no commits since last release, check for unreleased changes in current branch
4. If commit messages are unclear, analyze the changes in the code for more details
5. Analyze modified files and categorize changes into:
   - New Features: User-facing functionality additions
   - Bug Fixes: Issue resolutions and corrections
   - Refactoring: Code improvements without functionality changes
   - Dependencies: Package updates and security patches
   - Documentation: README, comments, or guide updates
   - Infrastructure: CI/CD, configuration, or deployment changes
6. Provide a structured summary with specific commit hashes and file changes
7. If no changes found since last release, report that the current version is up to date"
```

## 2. Version Management and Documentation (Use Subagents)

### Version Number Update and Changelog Generation

**Use the general-purpose subagent for version management:**

```
Use Task tool with subagent_type: "general-purpose"
Task: "Handle version increment and changelog generation"
Prompt: "Based on the analyzed changes from step 1:
1. Read current version from package.json (line 4)
2. Recommend version increment type based on changes:
   - Patch (x.x.1): Bug fixes, security patches
   - Minor (x.1.0): New features, non-breaking changes
   - Major (1.0.0): Breaking changes, major rewrites
3. Ask user to confirm the version increment type
4. Update version in package.json and any other version references
5. Generate/update CHANGELOG.md following Keep a Changelog standard:
   - Add new version entry with today's date
   - Categorize changes from analysis into: Added, Changed, Fixed, Security, Deprecated, Removed
   - Use proper markdown formatting
   - If CHANGELOG.md doesn't exist, create it with full structure
6. Provide a summary of version changes and changelog entries"
```

## 3. PWA Service Worker Update (Automated)

### Force Service Worker Update

**Use the general-purpose subagent for PWA updates:**

```
Use Task tool with subagent_type: "general-purpose"
Task: "Update PWA service worker for deployment"
Prompt: "Handle PWA service worker updates for deployment:
1. Read current FORCE_UPDATE timestamp from src/service-worker.js (line 5)
2. Update FORCE_UPDATE to current timestamp in 'YYYY-MM-DD-HH:MM' format
3. Verify PWA manifest at static/favicon/site.webmanifest is valid
4. Report the timestamp update and confirm PWA cache invalidation is ready"
```

## 4. Final Validation and Deployment (Use Subagents)

### Prepare for Manual Deployment

**Use the general-purpose subagent for deployment preparation:**

```
Use Task tool with subagent_type: "general-purpose"
Task: "Prepare dev branch for manual deployment"
Prompt: "Prepare the dev branch for manual merge to main:
1. Ensure current branch is 'dev' and all changes are committed
2. Verify git status is clean with no uncommitted changes
3. Push all changes to remote dev branch
4. Create a deployment preparation summary including:
   - New version number ready for tagging
   - Summary of changes being deployed
   - Service worker timestamp updated
   - All tests passing and build successful
   - Changelog entry created
5. Report that dev branch is ready for manual merge to main"
```

---

## Deployment Workflow Summary

**Execute these steps in order using the specified subagents:**

1. **Analyze**: Use general-purpose subagent to analyze repository changes since last release
2. **Version**: Use general-purpose subagent for version management and changelog generation
3. **PWA**: Use general-purpose subagent for service worker updates
4. **Validate**: Use general-purpose subagent for final pre-deployment checks
5. **Prepare**: Use general-purpose subagent to prepare dev branch and provide manual merge instructions

**Manual Steps (User):**

- `git checkout main && git merge dev`
- `git tag v[NEW_VERSION]`
- `git push origin main --tags`

---

## Usage Instructions

**This command prepares everything for deployment but requires manual merge to main branch.**

1. Run this command to execute steps 1-5 using subagents
2. Follow the provided manual git commands to merge dev to main and create tags
3. Run step 6 (monitoring subagent) after manual merge is complete

**Begin by executing Step 1: Repository change analysis using the general-purpose subagent!**
