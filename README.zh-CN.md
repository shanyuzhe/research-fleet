<div align="center">

# ⛵ ResearchFleet

**一条命令，组建你的科研团队。**

Claude Code 插件：一键初始化结构化科研项目，
并配齐一支七人 agent 军团——你的主会话就是 PI。

*又名 **PI 模拟器**——你的组员不睡觉、不闹情绪、
没有审计 trace 绝不敢报结果。*

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](https://claude.com/claude-code)
[![Version](https://img.shields.io/badge/version-0.1-green.svg)](ROADMAP.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[English](README.md) · **中文**

</div>

---

一条 `/research-init`，给你三样东西：

| | |
|---|---|
| 📁 **纪律齐全的项目骨架** | 宪法 · 预注册 · claim 文件 · 审计 trace · 交接页——全部单一权威源接线 |
| 🧑‍🔬 **七人 agent 科研团队** | scout · engineer · auditor · writer · presenter · steward · coach——各有硬规则和禁区 |
| 🧭 **Leader 宪法** | 主会话自动成为 PI：负责路由调度，你只需要说人话 |

这里的每一个机制都对应一次我们亲身付过学费的科研失败——
**[docs/lessons.md](docs/lessons.md)**：15 个踩坑 → 15 个机制。

## ⚡ 快速开始

```bash
# 1 · 安装（二选一）
claude --plugin-dir /path/to/research-fleet      # 本地克隆
#     …或发布后经 plugin marketplace 安装

# 2 · 初始化——回答三个问题：项目名 / 研究领域 / 目标 venue
claude
> /research-init

# 3 · 用人话做科研
> "有人探测过 VLM 隐层表征的判断质量吗？"    # → scout 出动
> "我们把 probing 实验预注册一下"             # → leader 和你一起写
> "实现并跑起来"                               # → auditor 先审设计，engineer 执行
> "把结果章节写了"                             # → writer（只见 verified claims）
> "给我看看树"                                 # → 🌳 看项目生长
```

除了 `/research-init` 不需要记任何命令——生成的 `CHEATSHEET.md` 只有一页，路由是 leader 的事。

## 🌰 理念：从一颗种子到一棵树

目标不是一份 PDF，而是**你自己的科研体系，和 agent 团队一起长成**：

- **掌控感**——问题、判据、gate 判定、叙事，每个判断按契约留在你手里；agent 搭台，绝不替你拍板。
- **进度永远可见**——每条工作线在一页纸上从 🌰 想法 → 🌱 预注册 → 🌿 数据 → 🪴 过审 → 🌳 verified → 🍎 进论文生长，还有一棵会动的树（见下）。
- **结束时你懂得更多而非更少**——盲点被暴露（confusion 账本、占位符）而不是被抹平，每日 Obsidian 复盘笔记把它们变成你的学习清单。
- **完成是收获不是赶工**——草稿随 verified claims 成熟自行装配；论文"完成"那天，它其实已经完成好几周了。

## 🌳 看着你的研究生长

同一份 append-only 生长日志（`.fleet/growth.jsonl`），三种视图：

```bash
python tools/growth_tree.py            # docs/fleet/tree.html — SVG 动画树：
                                       #   时间滑杆 · 点叶子溯源 · 枯枝作为诚实历史保留
python tools/growth_tree.py --ascii    # 同一棵树，任何终端 / ssh 里直接看
```

```
  2026-07-03
  │
  ├─🍎 readout_gap              [paper]    已进论文 §4.1
  ├─✝  fusion_gate              [data]     被 kill：baseline 混淆
  └─🪴 visual_leg               [audited]  production 排队中

  verified+: 1/3 · graveyard: 1
```

每日复盘走 **Obsidian 学习库**（`notes/`）：steward 维护"今天什么动了"+"值得搞懂什么"（从 confusion 账本和审计判决收割成概念卡，答案由你亲笔写），每条研究线一篇带链笔记——知识图谱随树一起长，手写区机器永不触碰。

## 🧑‍🔬 军团分工

| agent | 吸收的能力 | 保命硬规则 |
|---|---|---|
| **scout** 🔭 | 文献检索 · 查新 · 引用核实 | 零编造——每条引用当场联网验证，验不了标 `[UNVERIFIED]` |
| **engineer** 🔧 | 实现 · smoke · 跑 · 监控 · 统计 | fail loud · 3 seed · held-out 铁律 · **无权改协议** |
| **auditor** 🔍 | 设计/执行/论文三层审计 · 审稿人取证 | 设计审计先于实现；verdict 逐条引 `file:key=value` |
| **writer** ✍️ | 大纲 · LaTeX · 图表 · 编译 · 快照草稿 | 上下文隔离：只读 `claims/` + `NARRATIVE.md`；数字只复制不凭记忆 |
| **presenter** 📽️ | 论文精读 deck（反向学习法）· 进展汇报 · 会议 talk | 图必 PDF 截图禁重绘；判断页留白——**不代笔** |
| **steward** 📋 | 交接页 · 生长日志 · Obsidian 库 · 命名 lint | 只总结不判定；无进展如实写无进展 |
| **coach** 🎯 | 从 outcome 账本做自我改进 | 无证据即沉默；**只提案不擅改**；禁编造指标 |

Leader 不做成 agent——战略本来就需要你在场，而常驻监工舰队死于 token 成本（我们试过）。

## 🔁 一个结果的完整节奏

```
预注册 → 设计审计 → smoke → production（3 seed）→ 实验审计
      → claim（under-review → verified，由 audit marker 解锁）→ 论文
```

跳过某一步不会让结果来得更快，只会让它来第二次——第二次是审稿人送来的。（想随便玩去无门的 `experiments/scratch/`，只是 scratch 的数字永远进不了 claim。）

## 🛡️ 区分度在哪

1. **双上下文隔离**（招牌）——内部账本 `docs/findings/` 残酷诚实；writer 被防火墙隔离，只从审计门控的 claims + 叙事合同写作。诚实与叙事各得其所。
2. **强制力活在文件里，不靠自觉**——claim 升级要磁盘上的 `audit_passed` marker，实验要预注册文件。写在文档里的规则会被跳过，写进文件格式的不会。
3. **军团带证据自我进化**——每个任务结束记一行诚实账；coach 挖账本出提案，每条引证据，未经你批准一条不落地。
4. **机制化反 slop**——判断不代笔、图不重绘、数字不凭记忆、负结果作为一等边界陈述保留。

对自动"AI 科学家"的独立评测反复得出同一结论：它们离不开自己声称要取代的人工监督。ResearchFleet 从这个结论出发：**监督本身就是产品**——我们把它做得便宜且机械化。完整竞品失败模式分析（带出处）：[docs/landscape.md](docs/landscape.md)。

## 📦 仓库里有什么

```
agents/                 七个 agent 定义（纯 Markdown，不锁模型）
skills/
  research-init/        /research-init 脚手架 + 全套项目模板
  shared/references/    契约层：claims · traces · verdicts · run 包 ·
                        outcome 账本 · 生长日志 · 汇报 · 仓库纪律 · Obsidian 库
docs/
  design.md             架构与理由（对 ARIS 保留了什么、反转了什么）
  lessons.md            ★ 本框架由之铸成的 15 次失败
  landscape.md          竞品失败模式调研 + 区分度分析
examples/demo-project/  一个已初始化的示例项目，带一棵活的生长树
```

## 🚧 状态 — v0.1，年轻且有主见

按我们自己的纪律如实说：**纪律**来自一整年有据可查的真实科研周期（含一次完整复盘）；**插件载体**还很新。按我们自己的口径它算 `indicative` 不算 `verified`——欢迎试跑，你的 `.fleet/outcomes.jsonl` 加一个 issue 正是 coach 生来要吃的反馈。路线图：[ROADMAP.md](ROADMAP.md)。

## 🙏 出身与致谢

ResearchFleet 是对 [**ARIS**](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)（Auto-Research-In-Sleep，AAAI'26）及其对偶项目 [**Anti-Autoresearch**](https://github.com/wanshuiyin/Anti-Autoresearch) 一年实战经验的角色化重组——保留、反转与理由见 [docs/design.md](docs/design.md)。想要睡觉时全自动科研，用 ARIS；想要一支纪律严明、你当 PI 的团队，就是这个仓库。

## License

[MIT](LICENSE)
