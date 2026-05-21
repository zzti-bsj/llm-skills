# Interview Mode & Knowledge Index Design

## Background

The tech-knowledge-tree skill currently has 6 modes: enrich, mastery, deepen, walk, organize, history. Two new features:

1. **Interview mode** — extract interview Q&A from deepen documents
2. **Knowledge index** — auto-generated structural index on organize

## Feature 1: Interview Mode

### Decision

Add a new `interview` mode as an independent command. Deepen mode remains unchanged.

**Division of labor:**
- Python script handles mechanical work: directory scanning, title extraction, CSV management, dedup
- AI handles intelligent work: difficulty rating

### Script: `tech-knowledge-tree/interview.py`

Placed in the skill directory. Two subcommands:

#### `scan [--topic <topic>]`

- Scans `$TECH_DOCS_PATH` for all `deepen/` subdirectories
- If `--topic` is provided, only scans that topic's deepen directory
- For each `.md` file in deepen directories:
  - `title`: extracted from document content (first line or heading, which is the conclusion statement)
  - `content`: full document content
  - `tags`: direct parent directory name of the deepen directory
  - `category`: top-level directory name (first level under root)
  - `difficulty`: empty string (filled by AI later)
- Reads existing `questions.csv` at root, deduplicates by title
- Appends new entries to `questions.csv`
- Creates `questions.csv` with header if it doesn't exist

#### `set-difficulty <title> <difficulty>`

- Finds the row matching the given title in `questions.csv`
- Updates the difficulty field
- Title matching should handle quoting properly

### Output Format

CSV file at `$TECH_DOCS_PATH/questions.csv`:

```
title,content,tags,category,difficulty
"无状态真的比有状态更好吗？","<full document content...>","jwt","authentication",""
```

Fields:
- `title`: Chinese question extracted from deepen document's first line/heading
- `content`: complete deepen document content (no truncation)
- `tags`: parent directory name of the deepen directory (single tag, e.g. `jwt`)
- `category`: top-level directory name
- `difficulty`: one of [入门, 简单, 中等, 困难, 非常困难], initially empty

### Difficulty Levels

| Level | Meaning |
|-------|---------|
| 入门 | Basic concept awareness |
| 简单 | Basic understanding and application |
| 中等 | Requires practical experience |
| 困难 | Architecture/design level understanding |
| 非常困难 | Deep understanding, challenges conventional wisdom |

### Skill Instructions (SKILL.md additions)

```
interview (面试题) — 从 deepen 文档提取面试题

触发：用户说 "interview"、"面试题" 或 "面试"
调用方式：
  interview          → 扫描整个知识树
  interview <topic>  → 扫描指定 topic

流程：
1. 调用 interview.py scan [--topic <topic>]
2. 报告新增了多少条面试题
3. 读取 CSV 中 difficulty 为空的条目
4. 逐条阅读 content，评定难度
5. 调用 interview.py set-difficulty 写回
6. 完成后报告统计
```

Quick reference section update to include interview.

---

## Feature 2: Knowledge Index

### Decision

On every `organize` run, automatically regenerate a `INDEX.md` at the knowledge tree root. This is a pure structural index with clickable links — no descriptions, just the hierarchy in Chinese.

### Format

```markdown
# 知识索引

## authentication
### jwt
- [README](authentication/jwt/README.md)
- 深化
  - [stateless-myth](authentication/jwt/deepen/stateless-myth.md)
  - [key-rotation](authentication/jwt/deepen/key-rotation.md)
- 快速投产
  - [node-jose](authentication/jwt/mastery/node-jose.md)

### oauth
- [README](authentication/oauth/README.md)
```

### Rules

- Mode names in Chinese: 深化 (deepen), 快速投产 (mastery), 归档 (enrich)
- File links are relative paths from root, clickable as anchors
- No descriptions from README — pure structure
- Sub-sections only appear if that mode's directory exists (e.g., no "深化" heading if no deepen/ dir)
- Organize mode appends index generation as its final step

### Implementation

No separate script needed — the AI generates the index by reading the directory structure during organize. This is a natural extension of organize's existing behavior (which already scans directory structure).

---

## Cross-Mode Relationships

- interview depends on deepen documents as input source
- walk mode can suggest running interview after discovering deepen content
- interview is purely read-only from deepen's perspective (does not modify deepen docs)
- organize now produces INDEX.md as a side effect

## Files Changed

| File | Change |
|------|--------|
| `tech-knowledge-tree/interview.py` | New file - Python script for scan and set-difficulty |
| `tech-knowledge-tree/SKILL.md` | Add interview mode, update organize mode (index), update quick reference |
