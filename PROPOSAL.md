# Sheet Music Transformation Service

---

## Problem

Finding sheet music is easy. Finding the *right* sheet music is not.

- The piece is perfect, but too difficult to play at your current level
- You found a piano score, but you play a different instrument
- You want to play a classical piece in a jazz style
- Arranging for students takes too much time

Arranging by hand requires music theory knowledge. Outsourcing takes time and money.
This project automates that with AI.

---

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Difficulty adjustment** | Make a piece easier or harder while preserving the melody |
| 2 | **Instrument transposition** | Re-arrange a score for a different instrument (range, playability) |
| 3 | **Style transfer** | Re-arrange in the style of jazz, pop, baroque, etc. |
| 4 | **Personalized generation** | Generate a score tailored to a player's level and preferences |

---

## Architecture

```
[Input]
 ┌─────────────────────────────────────┐
 │  MusicXML / PDF / Image / MIDI      │
 └──────────────────┬──────────────────┘
                    │ Format conversion (OMR, parsing)
                    ▼
           [ MusicXML (internal standard) ]
                    │
                    ▼
 ┌──────────────────────────────────────────┐
 │             Transformation Engine        │
 │                                          │
 │  Rule Engine  ←────── LLM               │
 │  (note manipulation,    (high-level      │
 │   transposition,         decisions:      │
 │   rhythm editing)        which rules     │
 │                          to apply)       │
 └──────────────────┬───────────────────────┘
                    │ supports N-pass transformation
                    ▼
           [ Transformed MusicXML ]
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
  [Score rendering]          [Download]
  (in-browser playback)      (MusicXML, PDF)
```

**Rule Engine:** Deterministic transformations with clear rules — note duration changes, range adjustment, ornament removal, etc.

**LLM:** Makes high-level creative decisions (e.g. "arrange in jazz style") and determines which rules to apply and how.

**N-pass transformation:** The output of one transformation can be fed back into the engine for further refinement.

---

## Roadmap

### Phase 1 — MVP
Build a working version with 1–2 killer features. Release to a community, collect feedback, and reset direction based on what we learn.

- [x] MusicXML upload → render → playback
- [x] Difficulty adjustment (LLM prototype)
- [ ] Transformation quality stabilization (Rule Engine rewrite)
- [ ] Score download
- [ ] **Community release and feedback collection** (musician forums, music teacher groups, etc.)

**Key question for this phase:** Is the output actually usable? What do people want most?

#### Domain Expert Involvement in Phase 1

The domain expert's role evolves as the phase progresses:

```
Early Phase 1                        Later Phase 1
──────────────────────────────────────────────────────────────

 Upload score                         Upload score
      │                                    │
      ▼                                    ▼
 Review output          ──────►      Tune prompts directly
      │                                    │
      ▼                                    ▼
 Report issues                       Observe output change
 (what's wrong,                      (no coding required —
  how to fix it)                      edit system/user prompt
                                       text in the UI)
```

Once the basic pipeline is stable, the domain expert can tune the LLM behavior directly — without touching code. By feeding in various scores and adjusting the system/user prompts, the transformation quality can be improved from a purely musical perspective.

---

### Backlog (reprioritized after Phase 1 feedback)

- [ ] Instrument transposition (major instruments)
- [ ] Key transposition
- [ ] PDF / image score input (OMR)
- [ ] Style transfer (jazz, pop, baroque, etc.)
- [ ] Personalized transformation based on player level and preferences
- [ ] Mobile / tablet UX
- [ ] User accounts and score storage

---

## Collaboration

Code is handled by the developer. Two things are needed from the domain expert:

### 1. Feedback on AI-generated scores
Play through the transformed scores and report:
- What is wrong (out-of-range notes, unplayable passages, musically awkward moments)
- How it should be fixed

This feedback directly drives Rule Engine improvements and prompt refinement.

### 2. Arranging techniques
Share how human arrangers actually work:
- What do you change first when simplifying a piece?
- What do you consider when adapting for a different instrument?
- What are the defining characteristics of each style?

This knowledge forms the foundation of the Rule Engine and LLM prompts.
