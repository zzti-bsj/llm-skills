---
name: tech-knowledge-tree
description: Use when completing a technical module and wanting to archive the implementation as knowledge, or when user wants to organize, deepen, or add historical context to the docs/ knowledge tree. Triggers include finishing any technical feature implementation, wanting to restructure docs/, or wanting to expand a specific technology topic.
---

# Tech Knowledge Tree

## Overview
Maintain a living knowledge tree that organizes technologies by conceptual hierarchy. Grows organically as the project encounters new technologies.

Core purpose: **肃清本源，形成知识图谱，起指引作用。** Not a comprehensive reference, but a compass.

## Path Configuration
- Configurable via environment variable `TECH_DOCS_PATH`
- Default: `~/Project/docs`
- Each user sets their own path

## Four Modes

### enrich (归档)
**Trigger:** After completing a technical module.

1. Analyze the technology's conceptual chain (e.g., JWT → Authentication → Web Security)
2. Scan existing `docs/` structure
3. Match from most specific to broadest:
   - Deepest matching directory exists → nest under it
   - Partial match → extend from the matching point
   - No match → create full hierarchy
4. **Each technology = directory**, not a file
5. Write `README.md` following problem-driven evolution style (see below)
6. Write specific implementation doc (e.g., `dual-token.md`)
7. Keep it lightweight — only the essence, don't over-document

### deepen (丰富化)
**Trigger:** User specifies a topic to expand.

- Add detailed documents under the topic directory
- Can include: variations, edge cases, comparisons, deeper analysis, examples

### organize (整理)
**Trigger:** User asks to restructure.

- Scan directory structure only, not content
- Reorganize by logical relationships between topics
- Ensure progressive layering (broad → specific)

### history (历史脉络)
**Trigger:** User explicitly requests.

- Add historical development context for a specified topic
- Trace the evolution thread of the technology

## README Writing Style

The README in each topic directory is the most important document. It should:

**Do:**
- Follow **problem-driven evolution**: start from the fundamental problem, trace how solutions evolved step by step
- Use **first principles**: explain from fundamental truths, not jargon or analogies
- Answer **why** at every step — why did this solution emerge, why did it evolve this way
- Make the reader truly understand the technology's essence

**Don't:**
- Use textbook format (definition → structure → usage)
- List facts without explaining the reasoning behind them
- Be rigid about format — follow the natural narrative flow of the technology's evolution

## Key Principles

- **Directory > File**: Every technology topic is a directory with a `README.md`
- **Lightweight start**: Begin with minimal content, grow as needed
- **Auto-derive hierarchy**: Don't hardcode top-level categories, let the structure emerge from the technology's conceptual relationships
- **Chinese content, English directory names**

## Example

After implementing JWT dual token mechanism:

```
docs/
  web-security/
    authentication/
      jwt/
        README.md           # Why JWT exists: the evolution from session to stateless auth
        dual-token.md       # The specific access+refresh token pattern implemented
```

Later, user deepens the `jwt` topic:

```
docs/
  web-security/
    authentication/
      jwt/
        README.md
        dual-token.md
        structure.md        # JWT structure deep dive
        security-notes.md   # Security considerations
```
