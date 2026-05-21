---
name: tech-knowledge-tree
description: Two categories of triggers. (1) Project-bound: after completing a technical module in current conversation/project, archive it into the knowledge tree (enrich). (2) Abstract/project-independent: quickly learn how to integrate a technology into production using existing tools (mastery), deepen understanding through question-driven analysis (deepen), polish document quality including writing and code correctness (optimize), generate interview questions based on knowledge tree (interview), walk the knowledge tree to discover gaps (walk), organize directory structure and generate knowledge index, or add historical evolution context. All abstract modes operate on the knowledge tree itself, not on current project context.
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
  optimize <topic>   打磨已有文档的质量（目录级或文件级）
  walk <topic>       漫步知识树，发现遗漏和连接
  walk /             扫描整棵知识树
  interview <topic>  生成面向高级工程师/架构师的面试题
  organize           按逻辑关系重组目录结构
  history <topic>    添加历史演进脉络

Options:
  refresh            mastery: 换一种接入方式
  #N                 deepen: 直接写第 N 个候选问题的文档
  #N                 optimize: 直接执行第 N 条修改建议
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

### 抽象操作：mastery / deepen / optimize / walk / organize / history / interview
这七个模式与当前项目无关。输入源是知识树本身，不关心你在做什么项目。

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
3. Generate a `mastery/<approach>.md` containing:
   - **场景（Scenario）**: 真实应用场景（不是抽象练习题）
   - **目标（Target）**: 完成后的可验证交付物
   - **技术选型（Tooling）**: 使用的具体库/服务及理由
   - **参考资料（References）**: 官方文档、GitHub repo、API reference 等链接锚点
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
   - **文件名 = 问题本身**（kebab-case 英文，如 `deepen/stateless-myth.md`）
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

### optimize (打磨)
**Trigger:** 用户指定一个 topic 目录或具体文件，要求优化质量。

**Philosophy:** 在已有文档上打磨质量。不创建新文档、不移动文件——只诊断问题、提出修改建议，由用户决定是否执行。

**与相邻模式的边界：**
- organize 管**目录层级和文件移动**，optimize 不管结构
- deepen 管**新建深化文档**，optimize 管已有文档的**内容质量**
- walk 输出知识覆盖的觉察，optimize 输出具体到段落和代码行的修改建议

**两种工作模式：**

#### 目录级（`optimize <topic>`）

对指定 topic 目录下的文档组成和关系进行质量审查：

1. 读取该目录下所有文档
2. 输出**打磨报告**：
   - **文档间关系**：是否有重复内容、交叉引用是否准确、逻辑递进是否合理（README → 具体实现 → 深化 → 快速投产的递进链是否通顺）
   - **覆盖完整性**：README 讲了本质后，具体实现文档是否覆盖了关键场景；深化文档的方向是否互补
   - **一致性**：术语、命名、代码风格是否统一；同一概念在不同文档中的描述是否矛盾
   - **具体修改建议**：每条建议说明「改哪个文件」「改什么」「为什么改」（带编号，可直接 `optimize <topic> #N` 执行）
3. 用户决定：选择要执行的修改 / 全部执行 / 不执行

#### 文件级（`optimize <topic> <file>` 或指定具体文件路径）

对指定文档的行文质量、代码正确性进行打磨：

1. 读取目标文件及其上下文（同目录下的 README 和相关文档）
2. 输出**打磨报告**：
   - **行文质量**：论证是否充分、逻辑是否连贯、是否有空话套话、标题是否准确传达内容
   - **代码正确性**：示例是否能跑通、是否有 bug、是否遵循最佳实践（如同目录下 deepen 文档指出的陷阱是否在代码中被正确处理）
   - **内容准确性**：技术描述是否有过时或错误、与同目录下其他文档的交叉引用是否准确
   - **具体修改建议**：每条建议给出具体的修改内容（带编号，可直接 `optimize <topic> <file> #N` 执行）
3. 用户决定：选择要执行的修改 / 全部执行 / 不执行

### organize (整理)
**Trigger:** User asks to restructure.

- Scan directory structure only, not content
- Reorganize by logical relationships between topics
- Ensure progressive layering (broad → specific)
- **移动文件前先判断位置语义** — 文件的层级表达其概念范畴（如 `authentication/why-bearer.md` 表示 Bearer 是认证层概念）。位置语义正确的不动，语义错位的才移动（如 `ai-llm/llm-application/jwt/` 放错了领域）
- **自动生成知识索引**：organize 完成后，在根目录生成 `INDEX.md`
  - Markdown 格式：`##` / `###` 表示层级，`-` 列表项 + `[中文名](英文路径)` 链接
  - **中文名称基于内容理解，不是翻译文件名** — 必须阅读每个文档的内容，根据它实际在讲什么来命名。名称应同时满足两个条件：(1) 独立阅读时能准确传达文档核心议题；(2) 在其层级位置上有语义——位置本身就表达了"它属于哪个范畴"。例如 `authentication` 在 `web-security` 下不是泛泛的"认证"，而是"身份认证"这个安全子领域
  - Mode 分类名用中文：`深化` (deepen)、`快速投产` (mastery)；仅在实际存在时显示
  - **必须保留所有中间目录层级** — 即使某目录没有自己的 README.md，只要它是实际存在的目录，就必须作为 `###` 层级体现，因为目录层级本身就是语义
  - 完全覆盖根目录下所有目录和文件
  - 示例格式：
    ```markdown
    ## Web安全

    ### 身份认证

    - [为什么token前面要加Bearer](web-security/authentication/why-bearer.md)
    - [JWT认证全景](web-security/authentication/jwt/README.md)
      - [双Token机制——安全刷新与撤销的完整方案【RLSys】](web-security/authentication/jwt/dual-token【RLSys】.md)
      - 深化
        - [JWT"无状态"在生产中的真实边界](web-security/authentication/jwt/deepen/stateless-myth.md)
      - 快速投产
        - [PyJWT + FastAPI 认证实战](web-security/authentication/jwt/mastery/pyjwt-fastapi.md)
    ```

### history (历史脉络)
**Trigger:** User explicitly requests.

- Add historical development context for a specified topic
- Trace the evolution thread of the technology

### interview (面试题)
**Trigger:** User says "interview", "面试题", or "面试"，**必须带 topic 参数**。

**Philosophy:** 面向高级开发工程师和架构师，基于对知识树的深度理解生成考察生产决策力的面试题。

**流程：**

1. 定位 topic 目录（如 `interview jwt` → 搜索知识树中 `jwt` 目录）
2. 读取该目录下**所有文档**（README、enrich、deepen、mastery），形成完整理解
3. **范围判断**：如果该 topic 覆盖的知识范畴过大（如 `web-security`），无法生成有针对性的高质量面试题，则：
   - 列出该 topic 下的子目录
   - 建议用户指定更具体的范围
   - 不强行生成
4. 基于对文档内容的深度理解，生成 N 道面试题（数量自适应，取决于内容丰富度）
5. 每道题目考察的应是：
   - 生产中的设计决策（选型、取舍、边界判断）
   - 架构层面的思考（分布式、高并发、安全等）
   - 从「知道」到「能做」的工程转化能力
   - **不是**事实回忆，**不是**概念解释
6. 调用 `interview.py add` 逐条写入 `questions.csv`（自动去重）
7. 完成后报告统计

**CSV 格式：** `title,tags,category,difficulty`
- title：面试题本身（问句形式，中文）
- tags：直接父目录名
- category：顶级目录名
- difficulty：生成时直接评定

**难度级别：**

| 级别 | 含义 |
|------|------|
| 入门 | 基础概念认知 |
| 简单 | 基本理解和应用 |
| 中等 | 需要实际经验 |
| 困难 | 架构/设计层面 |
| 非常困难 | 深度理解，挑战常规 |

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

- **Directory > File**: 新建技术主题时，每个主题是一个目录（含 `README.md`），不是单个文件。已有文件的位置携带语义（层级即语义），organize 时需先理解位置含义再决定是否移动。
- **Lightweight start**: Begin with minimal content, grow as needed
- **Auto-derive hierarchy**: Don't hardcode top-level categories, let the structure emerge from the technology's conceptual relationships
- **Chinese content, English directory names**
- **Project tag**: 文件名可加 `【ProjectName】` 标注来源项目（enrich 和 deepen 通用）

## Mode Relationships

```
enrich（归档）  → 创建知识（README + 实现文档）
mastery（投产） → 快速接入（多种方式，可累积）
deepen（深化）  → 深化理解（问题驱动分析）
optimize（打磨）→ 质量审查（行文、代码、文档间关系）
walk（漫步）    → 觉察知识（发现遗漏和连接）
organize（整理）→ 重组知识（按逻辑关系调整结构）+ 生成知识索引
history（脉络） → 追溯知识（添加历史演进上下文）
interview（面试）→ 生成面试题（基于知识树深度理解，CSV 格式）
```

Walk 发现的问题 → Deepen 解答。
Deepen / enrich 新增的文档 → Optimize 打磨质量。
Optimize 发现的结构问题 → Organize 重组。
History 添加的演进脉络可以成为 → Deepen 的素材。
Mastery 的多种接入方式 → 互补覆盖，每种对应不同场景。
Interview 的输入源是 → 整个 topic 目录下的全部文档。

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
        deepen/
          stateless-myth.md             # 「无状态」真的是优势吗？
          jwt-vs-session-real-world.md  # 生产环境怎么选？
          key-rotation【RLSys】.md      # 密钥轮换
```
