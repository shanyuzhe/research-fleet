# ResearchFleet ⛵

> **一条命令，组建你的科研团队。**
> Claude Code 插件：一键初始化结构化科研项目（代码+论文+实验资产），同时配齐一支五人 agent 军团——你的主会话就是 PI（leader）。

[English](README.md) · [中文](README.zh-CN.md) · MIT License

---

**一条 `/research-init`** 给你：

- 📁 **科研项目骨架**——宪法（口径锁定）、预注册、claim 文件、审计 trace、交接页，全部单一权威源接线
- 🧑‍🔬 **五 agent 军团**——scout（文献）/ engineer（实验）/ auditor（审计）/ writer（写作）/ steward（管家），各有硬规则和禁区
- 🧭 **Leader 宪法**（项目 CLAUDE.md）——主会话自动成为 PI，负责路由调度；你只需要说人话

框架的每一个机制都来自一整年 LLM-agent 科研的真实血泪——一次 borderline-reject 的完整复盘 + 一次成功投稿的实战沉淀（**[docs/lessons.md](docs/lessons.md)**：15 个踩坑 → 15 个机制）。

## 为什么做这个

agent 科研工具有个悖论：**内部记录越诚实，论文越难看**——负结果和自我批判涌进写作上下文，论文写得像检讨书。规则写得越多，赶 deadline 时被跳过的越多。

ResearchFleet 的两个回答：

1. **双上下文隔离**（招牌机制）：内部账本 `docs/findings/` 保持残酷诚实；writer agent 被防火墙隔离——只能读 `claims/`（经审计门控的 verified 结果+使用边界）和叙事合同 `paper/NARRATIVE.md`。诚实与叙事各自获得一个可以彻底的上下文。
2. **强制力活在文件里，不靠自觉**：claim 升级 `verified` 需要磁盘上的 `audit_passed` marker；跑实验需要预注册文件先存在；论文只认 verified claim。写在文档里的规则会被跳过，写进文件格式的不会。

## 快速开始

```bash
# 1. 安装插件（二选一）
claude --plugin-dir /path/to/research-fleet      # 本地
# 或发布后通过 plugin marketplace 安装

# 2. 在（新）项目目录里
claude
> /research-init
# 回答三个问题：项目名 / 研究领域 / 目标 venue

# 3. 用人话做科研
> "有人探测过 VLM 隐层表征的判断质量吗？"       # → scout 出动
> "我们把 probing 实验预注册一下"                # → leader 和你一起写
> "实现并跑起来"                                  # → auditor 先审设计，engineer 执行
> "把结果章节写了"                                # → writer（只见 verified claims）
```

## 军团分工

| agent | 吸收的能力 | 保命硬规则 |
|---|---|---|
| **scout** 🔭 | 文献检索、查新、引用核实、anchor 论文 | 零编造——每条引用当场联网验证，验不了标 `[UNVERIFIED]` |
| **engineer** 🔧 | 实现、smoke、跑、监控、统计 | fail loud；3 seed；held-out 铁律；**无权改协议** |
| **auditor** 🔍 | 设计层/执行层/论文层审计 + 审稿人取证 | 设计审计先于实现；verdict 逐条引 `file:key=value`；先怪自己的代码再怪结论 |
| **writer** ✍️ | 大纲、LaTeX、图表、编译 | 上下文隔离：只读 `claims/` + `NARRATIVE.md`；数字只复制、不凭记忆 |
| **steward** 📋 | 交接页、claim 索引、journal、墓地 | 只总结不判定；无进展如实写无进展 |

Leader 不做成 agent——战略与 gate 决策本来就需要你在场，而常驻监工 agent 会死于 token 成本（我们试过）。

## 一个结果的完整节奏

```
预注册 → 设计审计 → smoke → production（3 seed）→ 实验审计
      → claim（under-review → verified，由 audit marker 解锁）→ 论文
```

跳过某一步不会让结果来得更快，只会让它来第二次——第二次是审稿人送来的。

## 出身与致谢

ResearchFleet 是对 [**ARIS**](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)（Auto-Research-In-Sleep，AAAI'26）及其对偶项目 [**Anti-Autoresearch**](https://github.com/wanshuiyin/Anti-Autoresearch) 一年实战经验的角色化重组——保留了什么、反转了什么、为什么，见 [docs/design.md](docs/design.md)。想要睡觉时全自动科研，用 ARIS；想要一支纪律严明、你当 PI 的团队，就是这个仓库。

## License

MIT
