# Tech Knowledge Tree

一个 Claude Code Skill，用于在项目开发过程中自动构建和维护技术知识树。

## 核心理念

**肃清本源，形成知识图谱，起指引作用。**

不是详细的技术文档，而是一个帮你理解技术本质的知识地图。每个技术主题按其内在概念关系层层递进组织，顺着问题驱动的演化脉络，用第一性原理讲清楚。

## 四种模式

| 模式 | 说明 |
|------|------|
| **enrich** (归档) | 完成技术模块后，轻量归档 — 推导层级、创建目录、写入本质 |
| **deepen** (丰富化) | 指定某个主题深入展开细节 |
| **organize** (整理) | 重新梳理目录结构，按逻辑关系组织 |
| **history** (历史脉络) | 为指定主题补充历史发展脉络 |

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
        README.md           # JWT 的本质：从 Session 到无状态认证的演化
        dual-token.md       # 双 Token 机制的具体实现方案
```
