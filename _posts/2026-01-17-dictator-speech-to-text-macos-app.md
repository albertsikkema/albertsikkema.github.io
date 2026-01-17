---
layout: post
title: "Dictator: A Push-to-Talk Speech-to-Text App for macOS"
date: 2026-01-17
categories: python development macos productivity
description: "Dictator is a lightweight macOS menu bar app that converts speech to text using whisper.cpp with GPU acceleration. Push-to-talk, instant paste, no cloud required."
keywords: "speech to text, whisper.cpp, macOS app, voice transcription, push-to-talk, Python development, local AI, offline transcription"
---

I built [Dictator](https://github.com/albertsikkema/dictator), a simple push-to-talk speech-to-text app for macOS. Hold a key, speak, release, and the transcribed text gets pasted wherever your cursor is.

The name is a play on words. "Dictation" because that's what it does. "Dictator" because that's how I sometimes view my relationship with this computer—I tell it what to do. And maybe a small nod to the times we live in.

I know, there are a lot of speech-to-text solutions out there, but I wanted something that was:

- **100% Local**: All processing happens on-device using whisper.cpp—your audio never leaves your Mac
- **No Internet Required**: Works completely offline once installed
- **Fast**: Metal GPU acceleration for near-instant transcription on Apple Silicon
- **Free**: no hidden costs, no subscriptions
- **Lightweight**: Minimal resource usage, stays out of your way
- **Non-obtrusive**: Lives quietly in your menu bar, not the dock
- **Easy to Use**: Just hold a hotkey to record, release to transcribe and paste
- **Push-to-talk**: Natural workflow—hold to speak, release to transcribe
- **Visual Feedback**: Icon animates (red → orange → yellow) based on audio level
- **Configurable**: Choose your preferred hotkey (Right Option, Right Command, Left Option, or Left Command)
- **Auto-start**: Option to launch at login
- **Self-contained**: Model bundled in the app (no external dependencies)

And also important: I built it for myself to improve my productivity when writing code.

<figure>
  <img src="/assets/images/sm7-side.jpg" alt="Shure SM7 microphone, a classic dynamic microphone used for voice recording">
  <figcaption>The venerable SM7 classic...</figcaption>
</figure>

## How It Works

1. Hold your configured hotkey (default: Right Option)
2. Speak
3. Release the hotkey
4. Text appears at your cursor

The menu bar icon animates based on your voice volume so you know it's hearing you. All transcription happens locally using [whisper.cpp](https://github.com/ggerganov/whisper.cpp) with Metal acceleration—no cloud, no API keys.

**Note:** English only for now.

## Installation

Grab the `.dmg` from the [releases page](https://github.com/albertsikkema/dictator/releases), drag the app to Applications, right-click and select "Open". Grant microphone and accessibility permissions when prompted, and you're set. OSX may complain about unverified developers, but rest assured it's safe (you can verify the source code on GitHub).


## Resources

- [Dictator on GitHub](https://github.com/albertsikkema/dictator)
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp)

---

*Questions or feedback? Connect with me on [LinkedIn](https://www.linkedin.com/in/albert-sikkema/).*
