# Deepen & Walk 设计文档

## 背景

Tech Knowledge Tree 的 README 采用第一性原理 + 问题驱动演进风格，回答「它为什么存在」。但 README 只是知识树的起点——读完 README 后，读者会追问更深入、更具体的问题。

**当前问题：** deepen 模式定义过于粗略（"Add detailed documents"），缺乏设计哲学和运作框架。

**目标：** 为 deepen 设计完整的运作机制，并新增 walk 模式作为补充。

## 哲学定位

### 认知层次

> 知其然 → 知其所以然 → 知其所以不然

- **README** = 知其然（它是什么、为什么存在）
- **Deepen** = 知其所以然 + 知其所以不然（通过具体问题深入）

### 学习的终极目标

学技术的目的是：**应用到实际场景中，并能够用专业且高级的术语、清晰的思路向别人讲解。** Deepen 的每个文档都应该服务于此目标。

### 三个内在方向

Deepen 文档的内容自然触达以下方向（内在视角，非外在分类）：

| 方向 | 追问的本质 | 举例 |
|---|---|---|
| **全景定位** | 在更广阔的图景中，它站在哪？ | 「JWT 和 OAuth 什么关系？」 |
| **边界探测** | 它在什么条件下失效？ | 「无状态真的比有状态好吗？」 |
| **工程转化** | 从知道到做到，中间缺什么？ | 「密钥轮换怎么做？」 |

三个方向是常见的深化切入点，但不是穷举。其他维度包括：内部机理、跨域连接、教学视角等。

## Deepen 运作机制

### 触发方式

#### 主动触发

用户说 `deepen <topic>`，系统：

1. 读取该目录下所有已有文档
2. 基于已有内容的密度和广度，生成 3-5 个候选问题
3. 向用户展示候选问题，用户选择要深入哪些
4. 为每个选定的问题写文档

#### Walk 触发

通过 walk 模式发现值得追问的问题后，一键转化为 deepen 任务（见下文 Walk 部分）。

### 问题生成原则

候选问题应该满足：

1. **读过 README 后自然追问**——不问基础问题
2. **有实际讨论价值**——不是搜索引擎能查到的事实
3. **覆盖不同方向**——至少触达全景/边界/工程中的两个
4. **用专业术语但不晦涩**——目标是「能向别人讲清楚」

### 问题生成示例

输入：用户说 `deepen jwt`，目录下已有 `README.md` + `dual-token【RLSys】.md`

系统分析已有内容后生成候选：

```
基于现有 JWT 文档（README + 双 Token 机制），以下是值得深入的方向：

1. jwt-vs-session-real-world.md
   生产环境中 JWT 和 Session 到底怎么选？各自的坑在哪？
   [全景定位 + 边界探测]

2. stateless-myth.md
   「无状态」真的是 JWT 的优势吗？什么时候有状态反而更好？
   [边界探测]

3. key-rotation.md
   JWT 签名密钥轮换怎么做？不停服的方案是什么？
   [工程转化]

4. jwt-without-oauth.md
   不用 OAuth，仅靠 JWT 能搭建完整认证体系吗？缺什么？
   [全景定位 + 工程转化]
```

用户选择 1 和 3，系统为这两个问题各写一个文档。

### 写作框架

每个 deepen 文档：

- **文件名 = 问题本身**（kebab-case 英文，如 `stateless-vs-stateful-auth.md`）
- **开宗明义**：第一段直接回答问题，给出结论
- **展开论证**：用推理和事实支撑结论
- **关联 README**：显式引用 README 中的概念，构建知识网络
- **项目标签**：如果内容来源于特定项目实践，加 `【ProjectName】`
- **中文内容，英文文件名**

### 文件结构示例

```
jwt/
  README.md                              # 本质：为什么存在
  dual-token【RLSys】.md                 # 已有：具体实现
  stateless-myth.md                      # 「无状态」真的是 JWT 的优势吗？
  jwt-vs-session-real-world.md           # 生产环境，JWT 和 Session 怎么选？
  key-rotation【RLSys】.md               # 密钥轮换怎么做？
```

## Walk 运作机制

### 定位

Walk 是**漫步于已有知识之间，在行走中觉察**。

| | Deepen | Walk |
|---|---|---|
| 姿态 | 挖掘（向下） | 漫步（向四周） |
| 驱动力 | 问题 | 觉察 |
| 输出 | 新的深度文档 | 对现有知识的重新理解、发现遗漏和连接 |

Walk 既是独立的知识活动（重新理解和连接已有知识），也可以作为 deepen 的上游（发现值得追问的问题）。

### 触发方式

用户说 `walk <topic-or-directory>`，系统：

1. 通读目录下的所有文档
2. 输出**觉察报告**：
   - **知识覆盖**：哪些方向已有覆盖、哪些空白
   - **知识关联**：文档间的连接和断裂
   - **候选问题**：值得追问的问题（可直接转化为 deepen 任务）
3. 用户决定下一步：什么都不做 / deepen 某个问题 / 其他

### Walk 不生产文档

Walk 的输出是觉察报告（直接展示给用户），不是新的文件。它的价值在于让用户重新审视已有知识。

## 与其他模式的关系

```
enrich（归档）  → 完成实现后，创建 README + 具体实现文档
deepen（深化）  → 基于问题，扩展知识的深度和广度
walk（漫步）    → 审视已有知识，发现遗漏和连接
organize（整理）→ 按逻辑关系重组目录结构
history（脉络） → 添加历史演进上下文
```

Walk 发现的问题 → Deepen 解答。
Deepen 新增的文档可能触发 → Organize 重构。
History 添加的演进脉络可以成为 → Deepen 的素材。

## 文件命名约定（按模式区分）

不同模式生成的文件遵循不同的命名约定：

| 模式 | 命名规则 | 举例 |
|---|---|---|
| **enrich** | 主题名 + 项目标签 | `dual-token【RLSys】.md` |
| **deepen** | 问题本身（kebab-case 英文）+ 可选项目标签 | `stateless-myth.md`、`key-rotation【RLSys】.md` |

已存在的 enrich 风格文件（如 `dual-token【RLSys】.md`）是有效内容，不需要迁移。两种命名方式可以共存。

项目标签 `【ProjectName】` 是共享约定，适用于任何来源有具体项目实践的文档。定义在 Key Principles 中，enrich 和 deepen 都使用。

## Walk 交互细节

### 话题解析

Walk 需要目标目录已存在（由 enrich 或之前的 deepen 创建）。解析规则：
- `walk jwt` → 在 docs/ 树中搜索名为 `jwt` 的目录
- `walk web-security/authentication` → 直接按路径定位
- 未找到目录 → 提示用户先运行 enrich
- `walk /`（根目录）→ 扫描整棵知识树

### 从 Walk 到 Deepen 的转化

Walk 报告中的每个候选问题带编号。用户可以说 `deepen <topic> #2` 指定要深入的问题编号，系统跳过问题生成步骤，直接进入写作阶段。

### 觉察报告格式

```markdown
## Walk: jwt

### 知识覆盖
- ✅ 本质理解（README）
- ✅ 具体实现模式（dual-token）
- ⬜ 全景对比（无替代方案分析）
- ⬜ 边界分析（无失效条件讨论）
- ⬜ 工程实践（无密钥管理、部署方案）

### 知识关联
- README → dual-token：README 末尾提到了双 Token，dual-token 详细展开，衔接良好
- 缺少：README 中提到「签名验证」，但没有文档展开签名算法选择

### 候选问题
1. jwt-vs-session-real-world — 生产环境，JWT 和 Session 怎么选？
2. stateless-myth — 「无状态」真的是 JWT 的优势吗？
3. key-rotation — JWT 密钥轮换怎么做？
```

## 实现范围

修改 `tech-knowledge-tree/SKILL.md`：

1. "Four Modes" → "Five Modes"
2. 更新 deepen 模式的描述和运作规则
3. 新增 walk 模式
4. 在 Key Principles 中添加项目标签 `【ProjectName】` 的共享约定
5. 保留 enrich、organize、history 不变
