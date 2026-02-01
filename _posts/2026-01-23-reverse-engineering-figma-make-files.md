---
layout: post
title: "Reverse-Engineering Figma Make: Extracting React Apps from Binary Files"
date: 2026-01-23
categories: AI development tools reverse-engineering
description: "How I reverse-engineered Figma Make's binary format to extract complete React applications. A deep dive into ZIP archives, Kiwi schemas, and dual compression algorithms."
keywords: "Figma Make extract code, reverse engineering Figma, extract React from Figma Make, Kiwi schema, Figma binary format, AI code generation, design tokens extraction"
---

A client came to me with a beautiful UI. They'd built it in Figma Make, the AI-powered prototyping tool. The app looked stunning, animations were smooth. Just one problem: I couldn't get to the actual code. Normally you can use the api or export design files, but not with Make. The Figma API Returns `{"status":400,"err":"File type not supported by this endpoint"}` for Make files.

Why would you not be able to do that? The wonders of corporate lock-in, I suppose. 

That's a problem: no design file. What now? So on to searching for ways to extract the code.

## Update - January 29, 2026

A few useful tips from readers:

- **Use the [`file`](https://man7.org/linux/man-pages/man1/file.1.html) command first**: Before reaching for `xxd`, running `file ClientApp.make` would have identified it as a ZIP archive immediately. Good reminder to start with the obvious tools.
- **Try [`binwalk`](https://github.com/ReFirmLabs/binwalk) for unknown binaries**: It scans for known file signatures and can identify embedded files within a single binary. Worth trying early in the process.

Now let's get into it.

## The Discovery: It's Just a ZIP File

So I started clicking around the Figma interface, looking for anything useful. That's when I noticed you can download the `.make` file itself. Download. A file, interesting!

But I can not read it. Hmmm, what now? Rule number one: never trust the extension. A `.make` file could be anything. After a while I figured out it was a ZIP file. And in it was in essence a React application.

<figure>
  <img src="/assets/images/figma-make-binary-reverse-engineering.jpg" alt="Binary code digits flowing across screen representing file format reverse engineering">
  <figcaption>Photo by <a href="https://www.pexels.com/photo/binary-options-trading-18536263/">Markus Winkler</a></figcaption>
</figure>

## The Discovery: It's Just a ZIP File

First thing I did was look at the raw bytes:

```bash
xxd -l 4 "ClientApp.make"
# Output: 504b 0304
```

`504b` is `PK` in ASCII. That's the ZIP file signature. The whole mysterious `.make` file is just a ZIP archive with a different extension. Learned something new today (about `504b`).

Unzip it:

```
ClientApp.make (ZIP)
├── canvas.fig          # 2.3 MB binary - the interesting part
├── meta.json           # Project metadata
├── ai_chat.json        # 34 MB of AI conversation history
├── thumbnail.png       # Preview image
├── images/             # 110 image assets (hash-named, no extensions)
└── blob_store/         # Additional binary data
```

The `ai_chat.json` was massive. Every prompt, every response, every iteration the client went through while building the app. Not very useful, and not what I needed. (although i did try to extract design tokens from it at first, before turning to the binary file).

The `canvas.fig` file held the actual code. 2.3 MB of binary data. That extension sounds more like a standard Figma design file. How to read that and see if it contains anything useful? Time to dig deeper.

## Decoding the Binary Format

Looking at the header:

```bash
xxd -l 20 canvas.fig
# Output: 6669 672d 6d61 6b65 65... (fig-makee)
```

Standard Figma design files use `fig-kiwi` as their magic header. Make files use `fig-makee`. Different format, same general approach.

The structure:

| Offset | Size | Content |
|--------|------|---------|
| 0 | 9 bytes | Magic: `fig-makee` |
| 9 | 3 bytes | Padding |
| 12 | 4 bytes | Chunk 1 size (little-endian) |
| 16 | N bytes | Chunk 1 data |
| 16+N | 4 bytes | Chunk 2 size |
| 20+N | M bytes | Chunk 2 data |

Two chunks. Two different compression algorithms. Thanks for some AI help here, LLMs are great at spotting patterns in binary data.

## The Compression Puzzle

First attempt: zlib decompression on both chunks.

```
Error: Invalid stored block lengths
```

The first chunk decompressed fine with zlib/deflate. The second chunk refused. Checking its magic bytes: `28 B5 2F FD`. That's Zstandard compression. Different algorithm entirely.

So:
- **Chunk 1 (Schema)**: Deflate compressed, 24KB → 59KB decompressed
- **Chunk 2 (Data)**: Zstandard compressed, 2.2MB → 29MB decompressed

Three npm packages made this work: `pako` for deflate, `fzstd` for Zstandard, and `kiwi-schema` for decoding the binary data format. Again, LLMs to the rescue. I know a bit about compression, but this would have taken me a lot of time to figure out alone. And probably would have given up (rewards vs time invested).  

## Kiwi Schema: Figma's Binary Format

Figma uses the Kiwi binary schema format. It's compact but has no schema definition included. Fortunately, Chunk 1 contains exactly that: the schema.

The schema had 534 type definitions. Nodes, colors, vectors, transforms, fonts, and the one I cared about: `CODE_FILE`.

Decoding the message data revealed a tree structure with 159 nodes:

```javascript
{
  "nodeChanges": [
    {
      "type": "DOCUMENT",
      "children": [...]
    },
    {
      "type": "CODE_FILE",
      "name": "App.tsx",
      "sourceCode": "import React from 'react'..."
    },
    // ... 157 more nodes
  ]
}
```

Every React component, utility function and CSS file were there in the `sourceCode` property. Progress! Now how to get to the content, the actual files?

<figure>
  <img src="/assets/images/figma-make-file-structure.png" alt="Diagram showing Figma Make canvas.fig binary structure: header, deflate-compressed schema chunk, and zstandard-compressed data chunk that decodes to React source files">
  <figcaption>Structure of canvas.fig and how it decodes to source code</figcaption>
</figure>

## Extracting the Content

Finding `CODE_FILE` nodes with source code was straightforward:

```javascript
const codeFiles = nodeChanges.filter(
  node => node.type === 'CODE_FILE' && node.sourceCode
);
```

96 source files extracted:
- React components (`.tsx`)
- TypeScript utilities (`.ts`)
- CSS files including `globals.css`
- Data files
- React hooks

But having files isn't the same as having a working app. Now to piece it all together, in a working structure:

## From Files to Running App

The extracted code had some quirks:

**Versioned package imports**: Figma Make embeds version numbers directly in import statements.
```javascript
// What Figma Make generates
import { Dialog } from '@radix-ui/react-dialog@1.1.6'

// What actually works
import { Dialog } from '@radix-ui/react-dialog'
```

**Custom asset imports**: Images use a proprietary format.
```javascript
// What Figma Make generates
import heroImage from 'figma:asset/a1b2c3d4.png'

// What actually works
const heroImage = '/images/a1b2c3d4.png'
```

**Missing file extensions**: All images in the `images/` folder were hash-named with no extensions. The browser needs `.png` to serve them correctly.

**Tailwind CSS v4 changes**: The PostCSS integration changed between versions. Needed `@tailwindcss/postcss` instead of using `tailwindcss` directly.

**React StrictMode breaking animations**: The original code used Framer Motion. StrictMode double-mounts components, which breaks timers and animations. Removing StrictMode fixed it.

I wrote scripts to handle all of this automatically. Analyze imports, determine folder structure (based on import references in the files), fix paths, copy images with proper extensions, generate `package.json`, Vite config, and TypeScript config.

## The Result

```bash
cd make_extraction
./run-all.sh ../ClientApp.make
cd output/react_app
npm install --legacy-peer-deps
npm run dev
```

A working React application on localhost:5173. Same components, same styling, same animations. No manual conversion work. No information lost.

## Design Token Extraction

Beyond source code, I also extracted design tokens using regex patterns:

- Hex colors: `#1a1a1a`, `#ffffff`
- RGBA values: `rgba(0, 0, 0, 0.5)`
- HSL colors: `hsl(220, 14%, 96%)`
- CSS variables: `--primary-color: #3b82f6`
- Google Fonts: `Inter`, `Roboto`

All exported to `design-tokens.json` for easy reference or migration to a design system.

## Lessons Learned

**Don't assume compression types**: The same file can use multiple compression algorithms for different chunks. Check the magic bytes.

**Figma's internal format is consistent**: Whether it's a design file or a code project, the underlying structure uses Kiwi schemas. Different content, same parsing approach.

**React StrictMode has side effects**: It's great for catching bugs during development, but it can break production code that relies on mount/unmount timing.

**The original code is usually correct**: I wasted time "fixing" fonts that weren't broken. The extraction was accurate; my assumptions weren't.

And most interesting: Figma Make is a great tool, but under the hood it is straightforward React with Radix UI and Tailwind CSS. No magic, just well-structured code generation. (and i have to give it to them, the code quality is pretty good for AI-generated code!).

So after spending 3 hours reverse-engineering and an hour writing this post, I can now finally get to work on the actual app :-) Have a great day!

## Get the Code

The extraction scripts are available here:

**Repository**: [github.com/albertsikkema/figma-make-extractor](https://github.com/albertsikkema/figma-make-extractor)

Quick start:
```bash
git clone https://github.com/albertsikkema/figma-make-extractor.git
cd figma-make-extractor/make_extraction
./run-all.sh ../YourApp.make
cd output/react_app
npm install --legacy-peer-deps
npm run dev
```

The scripts handle:
1. Unzipping the `.make` archive
2. Decoding the `canvas.fig` binary
3. Extracting source files
4. Extracting design tokens
5. Creating a runnable React/Vite project

## When Would You Need This?

- Client hands you a Figma Make prototype but not the design file
- You want to audit AI-generated code before deployment
- You need to migrate away from Figma Make to a different stack
- You want to extract design tokens for your design system
- Pure curiosity about how Figma structures its data

## Resources

**CLI Tools for Binary Analysis:**
- [file](https://man7.org/linux/man-pages/man1/file.1.html) - Identify file types from magic bytes
- [binwalk](https://github.com/ReFirmLabs/binwalk) - Scan for embedded files and compression signatures

**Binary Format Analysis:**
- [Kiwi Schema Format](https://github.com/nicbarker/kiwi)
- [Zstandard Compression](https://facebook.github.io/zstd/)

**npm Packages Used:**
- [pako](https://github.com/nodeca/pako) - Deflate compression
- [fzstd](https://github.com/101arrowz/fzstd) - Zstandard for JavaScript
- [kiwi-schema](https://github.com/nicbarker/kiwi) - Kiwi binary format decoder

---

*Have a Figma Make file you can't crack? Questions about the binary format? <a href="#" onclick="task1(); return false;">Get in touch</a> or open an issue on [GitHub](https://github.com/albertsikkema/figma-make-extractor).*
