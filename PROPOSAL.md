# Sheet Music Transformation Service

---

## Problem Statement

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
[Client]
 ┌─────────────────────────────────────┐
 │       Web App / Mobile & Tablet     │
 └──────────────────┬──────────────────┘
                    │ upload score + transformation request
                    ▼
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

## Why a Domain Expert Is Needed

During initial development, the full transformation was delegated to an LLM without structured musical guidance. The results exposed a fundamental limitation:

**LLMs default to statistically safe, surface-level transformations.**

Without an explicit model of what "easier" or "idiomatic" means in musical terms, the LLM has no basis for making musically intelligent decisions. What it produces instead:

- **Difficulty reduction** → uniform note value stretching (e.g. all 16ths → 8ths), with no consideration of which passages are technically demanding and why
- **No awareness of structural hierarchy** → melody notes, passing tones, and ornaments are treated as equivalent; the wrong ones get modified
- **No idiomatic reasoning** → transformations are harmonically and rhythmically plausible on paper, but ignore instrument-specific constraints (hand position, breath phrasing, bow technique, etc.)

The core issue is that musical arranging is not a pattern-matching problem — it requires a decision hierarchy:

```
What is the musical intent of this passage?
        │
        ▼
Which elements are structurally essential vs. expendable?
        │
        ▼
What transformations preserve musical coherence at the target difficulty/style/instrument?
        │
        ▼
In what order should those transformations be applied?
```

An LLM prompted without this hierarchy collapses it into a single step, producing output that is technically valid but musically shallow. The role of the domain expert is to encode this decision hierarchy — as rules, prompt structure, and evaluation criteria — so the system can produce transformations that reflect how a trained arranger actually thinks.

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

---

## References

### 1. Optical Music Recognition (OMR)

Converting PDF or image scores into structured digital formats (MusicXML, MIDI).

- **[Deep Learning for Optical Music Recognition: A Review](https://arxiv.org/abs/1907.12328)**
  Survey paper covering the full OMR technology stack and its limitations. Best starting point for understanding the field.

- **[End-to-End Optical Music Recognition using Neural Networks](https://arxiv.org/abs/1801.07115)**
  CRNN-based approach that reads an entire score as a sequence rather than recognizing individual symbols. Strong performance-to-complexity ratio.

### 2. Score Simplification & Arrangement

Compressing complex scores into playable, simplified forms.

- **[Automatic Piano Reduction from Ensemble Scores (ISMIR 2014)](https://ismir2014.ismir.net/ismir2014/papers/15_Paper.pdf)**
  HMM-based mathematical model for reducing multi-instrument or dense chord textures to a single piano part. A solid foundation for simplification rule design.

- **[The Skyline Algorithm for Musical Melody Extraction](https://www.researchgate.net/publication/220854483)**
  Standard algorithm for extracting the most salient melody line from a complex score. Essential reference for building a rule-based simplification engine.

### 3. Style Transfer & Symbolic Music Generation

Adjusting difficulty or changing style while preserving musical context.

- **[Music Transformer: Generating Music with Long-Term Structure](https://arxiv.org/abs/1809.04281)**
  Google Magenta research on how AI learns the repetitive structural patterns in music. Reference architecture for treating MusicXML as a sequence model input.

- **[PopMAG: Pop Music Accompaniment Generation](https://arxiv.org/abs/2008.07703)**
  Automatic accompaniment generation from a melody line. Relevant for generating idiomatic easy accompaniments alongside a simplified melody.

---

## Meeting Agenda

0. Are you still interested in working on this project together after our conversation?

1. If yes — how many hours per week are you available to commit?

2. Alignment on direction
   - Does the concept feel worth your time?
   - Any features you'd add or change?

3. Open questions / anything else
