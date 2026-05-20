# Tech Knowledge Tree

一个 Claude Code Skill，用于在项目开发过程中自动构建和维护技术知识树。

## 核心理念

**肃清本源，形成知识图谱，起指引作用。**

不是详细的技术文档，而是一个帮你理解技术本质的知识地图。每个技术主题按其内在概念关系层层递进组织，顺着问题驱动的演化脉络，用第一性原理讲清楚。

## 七种模式

| 模式 | 说明 |
|------|------|
| **enrich** (归档) | 完成技术模块后，轻量归档 — 推导层级、创建目录、写入本质 |
| **mastery** (快速投产) | 用现成工具快速接入生产，30 分钟跑通，可累积多种方式 |
| **deepen** (深化) | 问题驱动深入理解，生成有深度的候选问题，写出有论证的分析文档 |
| **walk** (漫步) | 漫步知识树，觉察已有知识的覆盖、连接和缺口 |
| **organize** (整理) | 按逻辑关系重组目录结构，自动生成知识索引 (INDEX.md) |
| **history** (历史脉络) | 为指定主题补充历史发展脉络 |
| **interview** (面试题) | 从 deepen 文档提取面试题到 CSV，自动评定难度 |

## 配置

知识树存放路径通过环境变量 `TECH_DOCS_PATH` 配置：

```json
// .claude/settings.json
{
  "env": {
    "TECH_DOCS_PATH": "/Users/yourname/Project/docs"
  }
}
```

未配置时默认使用 `~/Project/docs`。

## 示例

完成 JWT 双 Token 机制后，知识树结构如下：

```
~/Project/docs/
  web-security/
    authentication/
      jwt/
        README.md                     # JWT 的本质：从 Session 到无状态认证的演化
        dual-token【RLSys】.md       # 双 Token 机制的具体实现方案
        mastery/
          jsonwebtoken.md             # 用 jsonwebtoken 库接入
          auth0.md                    # 用 Auth0 SaaS 接入
        deepen/
          stateless-myth.md           # 「无状态」真的是优势吗？
          key-rotation.md             # 密钥轮换怎么做？
```
