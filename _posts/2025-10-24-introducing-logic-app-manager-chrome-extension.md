---
layout: post
title: "Introducing Logic App Manager"
date: 2025-10-24
categories: azure automation devops tools
description: "Chrome extension for Azure Logic Apps backup and restore. Simple version control directly from Azure Portal with local JSON storage."
keywords: "Azure Logic Apps, Logic Apps backup, Azure automation, Chrome extension, DevOps tools, workflow management"
---

Today I released the first version of a Chrome extension for backing up and restoring Azure Logic Apps directly from the Azure Portal. This is the first step toward bringing full version control to Logic Apps.

Managing Logic Apps can be unwieldy. Making changes to production workflows without an easy way to back up and restore is risky. Export through ARM templates or Azure CLI works, but it's friction when you just need a quick snapshot. Of course there are versions hidden somewhere, but can you remember what version did what after some time has passed?

## What It Does

[Logic App Manager](https://github.com/albertsikkema/logic-app-manager) adds backup and restore functionality to the Azure Portal:

- Click the extension while viewing a Logic App to save it as a timestamped JSON file
- Restore any saved backup by selecting the file
- Uses your existing Azure Portal authentication
- All operations stay local - no external servers or data collection

The extension reads Logic App identifiers from the page URL, uses MSAL tokens from your browser session, and calls Azure Management API endpoints directly. Built with vanilla JavaScript and Manifest V3.

## What's Next

This is the first step. The goal is to make Logic Apps management easier and more reliable.

The next major release will add Git-based version control:
- Automatic commits to GitHub (or similar)
- Full history of changes
- Proper branching and merging for teams
- Rollback to any previous version

## Installation

**Download zip:**
- Download from [GitHub releases](https://github.com/albertsikkema/logic-app-manager/releases)
- Extract the zip file
- Load as unpacked extension in Chrome

Repository: [github.com/albertsikkema/logic-app-manager](https://github.com/albertsikkema/logic-app-manager)

---

*Questions or feedback? Find me on [LinkedIn](https://www.linkedin.com/in/albert-sikkema/) or open an issue on [GitHub](https://github.com/albertsikkema/logic-app-manager).*
