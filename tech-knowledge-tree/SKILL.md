---
name: tech-knowledge-tree
description: Two categories of triggers. (1) Project-bound: after completing a technical module in current conversation/project, archive it into the knowledge tree (enrich). (2) Abstract/project-independent: quickly learn how to integrate a technology into production using existing tools (mastery), deepen understanding through question-driven analysis (deepen), walk the knowledge tree to discover gaps (walk), organize directory structure, or add historical evolution context. All abstract modes operate on the knowledge tree itself, not on current project context.
---

# Tech Knowledge Tree

## Quick Reference

When user says `help` or asks what this skill can do, show this:

```
用法: tech-knowledge-tree <command> [topic]

Commands:
  help               显示本帮助
  enrich <tech>      归档刚做完的技术模块
  mastery <topic>    快速接入生产（可多次，累积不同方式）
  deepen <topic>     问题驱动深入理解
  walk <topic>       漫步知识树，发现遗漏和连接
  walk /             扫描整棵知识树
  organize           按逻辑关系重组目录结构
  history <topic>    添加历史演进脉络

Options:
  refresh            mastery: 换一种接入方式
  #N                 deepen: 直接写第 N 个候选问题的文档
```

用户不需要记住命令——用自然语言描述意图，系统自动匹配模式。

## Overview

Maintain a living knowledge tree that organizes technologies by conceptual hierarchy. Grows organically as the project encounters new technologies.

Core purpose: **肃清本源，形成知识图谱，起指引作用。** Not a comprehensive reference, but a compass.

## Path Configuration
- Configurable via environment variable `TECH_DOCS_PATH`
- Default: `~/Project/docs`
- Each user sets their own path

## Two Categories

### 项目绑定：enrich（归档）
enrich 是唯一的上下文绑定模式。它从当前对话/项目中提取知识，输入源是「你刚刚做了什么」。

### 抽象操作：mastery / deepen / walk / organize / history
这五个模式与当前项目无关。输入源是知识树本身，不关心你在做什么项目。

---

## Mode Details

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
6. Write specific implementation doc, named by topic + project tag (e.g., `dual-token【RLSys】.md`)
7. Keep it lightweight — only the essence, don't over-document

### mastery (快速投产)
**Trigger:** User wants to quickly learn how to integrate a technology into production.

**Philosophy:** 用现成工具快速接入，不造轮子。30 分钟内跑通，验证效果。

**核心原则：**
- 不手撸底层实现——用成熟的库和服务
- 追求最快接入路径——30 分钟内看到效果
- 理解和底层原理不是 mastery 的职责，那是 deepen 的事

**流程：**

1. Read all existing docs in the topic directory（避免重复已有内容）
2. 确定一种接入方式（选择主流的、生产验证过的库/服务）
3. Generate a `mastery-<approach>.md` containing:
   - **场景（Scenario）**: 真实应用场景（不是抽象练习题）
   - **目标（Target）**: 完成后的可验证交付物
   - **技术选型（Tooling）**: 使用的具体库/服务及理由
   - **分步引导（Steps）**: 每步包含「做什么」「怎么做」「为什么」
4. 分步数量 3-6 步，每步 5-10 分钟
5. 文件命名体现接入方式，如 `mastery-jsonwebtoken.md`、`mastery-auth0.md`
6. 每次调用生成一种新的接入方式，可累积多个 mastery 文档
7. 用户说 `refresh` → 重新生成一种不同的接入方式

**多方式累积示例：**
```
jwt/
  mastery/
    jsonwebtoken.md          # 第1次：用 jsonwebtoken 库自己签发
    auth0.md                 # 第2次：用 Auth0 SaaS 接入
    nextauth.md              # 第3次：用 NextAuth 框架集成
```

### deepen (深化)
**Trigger:** User wants to deeply understand a topic.

**Philosophy:** 问题驱动，追问本质。生成有深度的问题，写出有论证的分析文档。

**流程：**

1. 读取该目录下所有已有文档
2. 生成 3-5 个候选问题，每个问题满足：
   - 读过 README 后自然追问（不问基础问题）
   - 有实际讨论价值（不是搜索引擎能查到的事实）
   - 覆盖不同方向（全景定位 / 边界探测 / 工程转化 中至少两个）
   - 用专业术语但不晦涩
3. 向用户展示候选问题，用户选择要深入哪些
4. 为每个选定的问题写文档，遵循写作框架：
   - **文件名 = 问题本身**（kebab-case 英文，如 `stateless-myth.md`）
   - **开宗明义**：第一段直接回答问题，给出结论
   - **展开论证**：用推理和事实支撑
   - **关联 README**：显式引用 README 中的概念
   - 中文内容，英文文件名

**三个内在方向**（不是外在分类，是问题自然触达的视角）：

| 方向 | 追问的本质 | 举例 |
|---|---|---|
| **全景定位** | 在更广阔的图景中，它站在哪？ | 「JWT 和 OAuth 什么关系？」 |
| **边界探测** | 它在什么条件下失效？ | 「无状态真的比有状态好吗？」 |
| **工程转化** | 从知道到做到，中间缺什么？ | 「密钥轮换怎么做？」 |

### walk (漫步)
**Trigger:** User wants to review and sense existing knowledge.

Walk 是漫步于已有知识之间，在行走中觉察。不生产文档，输出觉察报告。

1. 通读目标目录下所有文档
2. 输出**觉察报告**：
   - **知识覆盖**：哪些方向已有覆盖、哪些空白
   - **知识关联**：文档间的连接和断裂
   - **候选问题**：值得追问的问题（带编号，可直接 `deepen <topic> #N`）
3. 用户决定下一步：什么都不做 / deepen 某个问题 / 其他

话题解析：`walk jwt` 搜索 docs/ 树中名为 `jwt` 的目录；`walk /` 扫描整棵树；未找到则提示先运行 enrich。

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
- **Project tag**: 文件名可加 `【ProjectName】` 标注来源项目（enrich 和 deepen 通用）

## Mode Relationships

```
enrich（归档）  → 创建知识（README + 实现文档）
mastery（投产） → 快速接入（多种方式，可累积）
deepen（深化）  → 深化理解（问题驱动分析）
walk（漫步）    → 觉察知识（发现遗漏和连接）
organize（整理）→ 重组知识（按逻辑关系调整结构）
history（脉络） → 追溯知识（添加历史演进上下文）
```

Walk 发现的问题 → Deepen 解答。
Deepen 新增的文档可能触发 → Organize 重构。
History 添加的演进脉络可以成为 → Deepen 的素材。
Mastery 的多种接入方式 → 互补覆盖，每种对应不同场景。

## Example

After implementing JWT dual token mechanism:

```
docs/
  web-security/
    authentication/
      jwt/
        README.md                     # Why JWT exists: the evolution from session to stateless auth
        dual-token【RLSys】.md        # The specific access+refresh token pattern implemented
```

User explores the `jwt` topic over time:

```
docs/
  web-security/
    authentication/
      jwt/
        README.md                       # 本质：为什么存在
        dual-token【RLSys】.md         # enrich：具体实现
        mastery/
          jsonwebtoken.md               # mastery 第1次：用 jsonwebtoken 库接入
          auth0.md                      # mastery 第2次：用 Auth0 SaaS 接入
        stateless-myth.md               # deepen：「无状态」真的是优势吗？
        jwt-vs-session-real-world.md    # deepen：生产环境怎么选？
        key-rotation【RLSys】.md        # deepen：密钥轮换
```
