# ResearchFleet ⛵

> **一条命令，组建你的科研团队。**
> Claude Code 插件：一键初始化结构化科研项目（代码+论文+实验资产），同时配齐一支七人 agent 军团——你的主会话就是 PI（leader）。
>
> *又名 **PI 模拟器**：让每个研究生都能体验一把当 PI 的感觉——你的组员不睡觉、不闹情绪、没有审计 trace 绝不敢报结果。*

[English](README.md) · [中文](README.zh-CN.md) · MIT License

---

**一条 `/research-init`** 给你：

- 📁 **科研项目骨架**——宪法（口径锁定）、预注册、claim 文件、审计 trace、交接页，全部单一权威源接线
- 🧑‍🔬 **七 agent 军团**——scout（文献）/ engineer（实验）/ auditor（审计）/ writer（写作）/ presenter（汇报）/ steward（管家）/ coach（自我改进），各有硬规则和禁区
- 🧭 **Leader 宪法**（项目 CLAUDE.md）——主会话自动成为 PI，负责路由调度；你只需要说人话

框架的每一个机制都来自一整年 LLM-agent 科研的真实血泪——一次 borderline-reject 的完整复盘 + 一次成功投稿的实战沉淀（**[docs/lessons.md](docs/lessons.md)**：15 个踩坑 → 15 个机制）。

## 理念：从一颗种子到一棵树

目标不是一份 PDF，而是**你自己的科研体系，和 agent 团队一起长成**。每个判断都留在你手里（问题、判据、gate、叙事），agent 照料其余；进度永远可见：每条工作线在一页纸上从 🌰 想法 → 🌱 预注册 → 🌿 数据落地 → 🪴 过审 → 🌳 verified claim → 🍎 进论文 生长，草稿随 verified claims 自行装配；`python tools/growth_tree.py` 还能把整个历史回放成一棵**会生长的动画树**（`docs/fleet/tree.html`：时间滑杆、点叶子溯源、枯枝作为诚实历史保留在树上）。盲点被暴露（confusion 账本、占位符）而不是被抹平——项目结束时你懂得**更多**而非更少。论文"完成"那天，它其实已经完成好几周了：最后一次编译是收获，不是赶工。

## 为什么做这个

agent 科研工具有个悖论：**内部记录越诚实，论文越难看**——负结果和自我批判涌进写作上下文，论文写得像检讨书。规则写得越多，赶 deadline 时被跳过的越多。

ResearchFleet 的两个回答：

1. **双上下文隔离**（招牌机制）：内部账本 `docs/findings/` 保持残酷诚实；writer agent 被防火墙隔离——只能读 `claims/`（经审计门控的 verified 结果+使用边界）和叙事合同 `paper/NARRATIVE.md`。诚实与叙事各自获得一个可以彻底的上下文。
2. **强制力活在文件里，不靠自觉**：claim 升级 `verified` 需要磁盘上的 `audit_passed` marker；跑实验需要预注册文件先存在；论文只认 verified claim。写在文档里的规则会被跳过，写进文件格式的不会。

## 为什么不用全自动"AI 科学家"？

对自动科学家系统（AI Scientist / Agent Laboratory 等）的独立评测反复得出同一个结论：查新流于关键词、无法批判性评估自己的结果、幻觉引用、离不开它声称要取代的人工监督。多 agent 框架则另收一笔税：约 3× 的 token 开销、聊天死循环、协调开销压过有效工作。

ResearchFleet 从这些评测的结论出发：**监督本身就是产品。** 判断留给你，军团把监督变得便宜且机械化（独立敌手审计、文件级 gate、零常驻 agent 成本）。完整的竞品失败模式分析（带出处）：[docs/landscape.md](docs/landscape.md)。

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
| **presenter** 📽️ | 论文精读 deck（反向学习法）、进展汇报、会议 talk | 图必来自 PDF 截图禁 AI 重绘；局限/总结等判断页**留白不代笔**；盲点记 confusion.md 回流成研究问题 |
| **steward** 📋 | 交接页、claim 索引、journal、墓地 | 只总结不判定；无进展如实写无进展 |
| **coach** 🎯 | 自我改进：挖 outcome 账本里的反复摩擦 → 对 CLAUDE.md/agent/模板的改进提案 | 每条提案必须引 ≥2 条账本证据；**只提案不擅改**；禁编造指标 |

Leader 不做成 agent——战略与 gate 决策本来就需要你在场，而常驻监工 agent 会死于 token 成本（我们试过）。

**军团会带证据地自我进化。** 每个 agent 结束任务时往 `.fleet/outcomes.jsonl` 追加一行诚实记录：什么起了作用、什么在拖后腿。coach 定期挖这本账（连同审计 trace 和墓地），对项目宪法、agent 定义、模板提出升级提案——每条提案引用触发它的账本条目，未经你批准一条也不落地。

## 一个结果的完整节奏

```
预注册 → 设计审计 → smoke → production（3 seed）→ 实验审计
      → claim（under-review → verified，由 audit marker 解锁）→ 论文
```

跳过某一步不会让结果来得更快，只会让它来第二次——第二次是审稿人送来的。

## 状态 — v0.1，年轻且有主见

按我们自己的纪律如实说：**纪律本身**来自一整年有据可查的真实科研周期（含一次完整复盘）；**插件这个载体**还很新、里程尚在累积。按我们自己的口径，这个框架目前算 `indicative`，还不算 `verified`——欢迎拿真项目试跑，你的 `.fleet/outcomes.jsonl` 加一个 issue，正是 coach agent 生来要吃的反馈。

## 出身与致谢

ResearchFleet 是对 [**ARIS**](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)（Auto-Research-In-Sleep，AAAI'26）及其对偶项目 [**Anti-Autoresearch**](https://github.com/wanshuiyin/Anti-Autoresearch) 一年实战经验的角色化重组——保留了什么、反转了什么、为什么，见 [docs/design.md](docs/design.md)。想要睡觉时全自动科研，用 ARIS；想要一支纪律严明、你当 PI 的团队，就是这个仓库。

## License

MIT
