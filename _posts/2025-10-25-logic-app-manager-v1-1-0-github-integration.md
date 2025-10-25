---
layout: post
title: "Logic App Manager v1.1.0: GitHub Integration"
date: 2025-10-25
categories: azure automation devops tools
---

Yesterday I introduced [Logic App Manager](https://github.com/albertsikkema/logic-app-manager), a Chrome extension for backing up and restoring Azure Logic Apps. Today I'm releasing v1.1.0 with the promised GitHub integration.

## What's New

Version 1.1.0 adds **full GitHub integration** for centralized backup and version control:

- **Backup to GitHub** - Push Logic App definitions directly to your repository
- **Version History** - Browse commit history and restore from any previous version
- **Organized Storage** - Files automatically saved as `apps/{workflowName}/{YYYY-MM-DD}-workflow.json`
- **Secure Tokens** - GitHub Personal Access Tokens stored in session storage (cleared on browser close)
- **Configuration Page** - Easy setup through extension options

The original file-based backup and restore functionality remains available as a fallback option.

## Why This Matters

Now you have proper version control for Logic Apps without leaving the Azure Portal. Every backup is committed to GitHub with a timestamp and message. Made a mistake? Need to roll back a change? Browse the commit history and restore any previous version with a click.

Teams can now share a central repository for Logic App backups, track who changed what, and maintain a complete audit trail.

## Installation

Download [logic-app-manager-v1.1.0.zip](https://github.com/albertsikkema/logic-app-manager/releases/download/v1.1.0/logic-app-manager-v1.1.0.zip) from the releases page, extract it, and load as an unpacked extension in Chrome.

For GitHub integration, configure your repository and Personal Access Token in the extension options. Full setup instructions are in the [README](https://github.com/albertsikkema/logic-app-manager#readme).

## Next Steps

I'm currently working on making Logic App Manager available through the **Chrome Web Store** for easier installation and automatic updates. Stay tuned for the official release!

## Announcing Logic App Manager PRO

With the core functionality now solid, I'm working on a **PRO version** for teams and professional workflows.

The free version will remain open source with all current features. PRO will add:

- **Advanced Release Management** - Automated release pipelines and deployment workflows
- **Multiple Environments** - Manage Dev, Test, Accept, and Production
- **Enhanced Diff & Merge Views** - Visual comparison and intelligent merging
- **Team Collaboration** - Multi-user workflows, approval processes, and role-based access
- **Template Generation** - Export to ARM templates, Terraform, Bicep, and other IaC formats
- **Azure Deployment Integration** - Direct deployment via Terraform, Azure CLI, PowerShell, and Azure DevOps
- **Advanced Analytics** - Deployment tracking, change history, and audit logs
- **Enterprise Support** - Priority support and custom integration options

Interested in **PRO**? The more interest there is, the sooner I can build it. Please [reach out](https://albertsikkema.com) for details, pricing, and licensing information, and to share your needs and help shape the roadmap!

Repository: [github.com/albertsikkema/logic-app-manager](https://github.com/albertsikkema/logic-app-manager)

---

*Questions or feedback? Find me on [LinkedIn](https://www.linkedin.com/in/albert-sikkema/) or open an issue on [GitHub](https://github.com/albertsikkema/logic-app-manager/issues).*
