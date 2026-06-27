# 对标分析：机构研报 vs 大队长报告（2026/06/27 整理）

> 本档为 V1.3 规划的工作底稿。汇总 2026 年 5-6 月主流机构关于 AI 泡沫与算力周期的研报，与《AI 周期与泡沫深度研究报告》进行横向对标，识别**单点压倒**与**广度独占**两类差距，作为后续版本补缺与方法论迭代的依据。

---

## 一、对标结论一句话

> 截至 2026/06/27，**没有任何单一机构报告在「综合广度 + 反方压测 + 中国投资者实操路径」三维同时超过大队长报告**。但**在 4 个单点**（算力 TAM 三层拆解、IG 信贷结构、HBM 利润迁移、延长场景）存在机构研报值得吸收的增量信息。

---

## 二、A 档：单点压倒大队长的机构报告（必须补缺）

| 机构 | 报告/日期 | 单点优势 | 计划吸收路径 |
|------|----------|---------|------------|
| **Goldman Sachs** | "Tracking the Trillions" 2026/06/06 | $7.6T 累计 capex 三层拆解：compute $5.1T / DC $2.1T / power $358B | V1.3 §3 算力 TAM 加三层表 |
| **Morgan Stanley** | "AI Dispersion in Credit" 2026/06/23 | IG 债结构性变化、Oracle D/E 500%、AI 债占 IG 发行 30%+ | V1.3 §2 加 IG 债结构小节 |
| **SemiAnalysis** | "US Grid Constraints — 40GW BTM" 2026/06/25 | HBM 占 hyperscaler capex 30%→48%、BTM 燃机 40GW by 2028 | V1.3 §2 加 HBM 利润迁移 + 物理约束 |
| **Sequoia Capital** | "$600B Question" (David Cahn) 持续更新 | Q1 VC 80% 投 AI、$240B/$297B 比值 | V1.3 §1.2 引用比值（已部分覆盖，强化引用） |

### 2.1 Goldman "Tracking Trillions" 详解
- **关键数据**：2025-2030 全球 AI 累计 capex $7.6T，三层拆解：
  - **Compute 芯片层** $5.1T（67%）—— NVDA/AMD/HBM/CoWoS
  - **数据中心物理层** $2.1T（28%）—— 土建、冷却、机柜
  - **电力层** $358B（5%）—— 燃机、变电、并网
- **方法论亮点**：用 IRR + 折现现金流倒推不同算力价格下的 capex 可承受边界
- **与大队长报告关系**：大队长 §3 用 1.36-2.06 万亿 TAM 框架，Goldman 是**绝对规模 vs 收入比的另一视角**，可互补
- **来源**：[Business Insider — Goldman Sachs AI capex boom report](https://www.businessinsider.com/ai-capex-boom-meta-microsoft-amazon-alphabet-goldman-sachs-2026-6)

### 2.2 Morgan Stanley "AI Dispersion in Credit" 详解
- **关键数据**：
  - AI 相关债券占 IG 新发行比重 2024 年 8% → 2026H1 30%+
  - Oracle 净杠杆 D/E 500%、CDS 利差从 60bp 跳升至 145bp
  - Meta/Amazon 杠杆水平相对温和（D/E < 100%）
- **方法论亮点**：把"AI 信贷"作为独立的资产类别看待，识别信用利差分化为崩盘前置信号
- **与大队长报告关系**：大队长 V1.2 已捕获"集体发债+信贷脉冲 $8000 亿"，MS 提供**结构性视角**（不是总量，而是谁在借、利差分化结构）
- **来源**：[Morgan Stanley IM — AI Dispersion in Credit](https://www.morganstanley.com/im/en-us/individual-investor/insights/articles/ai-dispersion-in-credit.html)

### 2.3 SemiAnalysis "40GW BTM" 详解
- **关键数据**：
  - HBM 占 hyperscaler AI capex 2024 30% → 2026 48%（与 CLSA 联合估算）
  - BTM（Behind-the-Meter）燃机部署 40GW by 2028，弥补并网延迟
  - 单机柜功率密度 120kW → 250kW（B100/B200 时代）
- **方法论亮点**：从供应链物理约束反推叙事可信度，HBM/CoWoS/电力三重瓶颈量化
- **与大队长报告关系**：大队长 §2 利润真实性主要在财务层，SemiAnalysis 提供**供应链层的利润迁移证据**——NVDA 利润越来越多被 HBM 厂商（SK 海力士、三星、美光）瓜分
- **来源**：[SemiAnalysis — US Grid Constraints Towards 40GW BTM](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw)

### 2.4 Sequoia "$600B Question"
- **关键数据**：Q1 2026 VC 全球募资 $297B，其中 $240B（80%）投 AI；累计未来需 $600B 年化收入才能合理化当前估值
- **与大队长报告关系**：大队长 §1.2 已引用此比值，**V1.3 可强化对 Cahn 系列后续更新的追踪**
- **来源**：[Sequoia Capital — David Cahn $600B Question series](https://www.sequoiacap.com/article/follow-the-gpus-perspective/)

---

## 三、B 档：与大队长高度重合（无需补，可作交叉验证）

| 机构 | 报告/日期 | 重合内容 |
|------|----------|---------|
| Goldman Sachs | "AI 巨头 ROE" 2026/06/12 | 七巨头 ROE 分化、capex/营收比 — 大队长 §7 已覆盖 |
| Morgan Stanley | "$1.8T 表外负债" 早期版本 | SPV/数据中心租赁表外化 — 大队长 §2.3 已覆盖 |
| MIT NANDA | "Enterprise AI Adoption Survey" 2026 | 95% AI 项目未产生 ROI — 大队长 §1.1 利润真实性已覆盖 |
| BofA | Vivek Arya "AI Cycle" 2026/06/23 | **反方观点**：投资周期延至 2028 — V1.3 作为压测引用 |

### 3.1 BofA Arya 反方观点详解（V1.3 §6 A 场景敏感性分析素材）
- **核心立场**：当前算力短缺为真，超大规模厂商 capex 周期延长至 2028 而非 2027 见顶
- **关键论据**：HBM 供给 + 电力并网双瓶颈，导致需求消化期被动拉长
- **与大队长报告关系**：A 场景（42% 概率，软着陆）需做"延长 18 个月"敏感性，把崩盘时点从 2026H2 推到 2028H1，看四情景概率分布如何调整
- **来源**：BofA Global Research 2026/06/23（Bloomberg 终端引用）

---

## 四、大队长不可替代的 5 维（机构没有的）

| 维度 | 大队长报告独有内容 | 为什么机构难以复制 |
|------|------------------|------------------|
| **1999-2000 同构性映射** | 朗讯/北电/Cisco vs NVDA/Oracle/CoreWeave 三层对照 | 机构受立场约束，难做历史泡沫直接类比 |
| **三阶段崩盘剧本** | 触发期→急跌→去叙事化的时间形态与价位分布 | 机构合规不允许给"剧本式"前瞻 |
| **四情景概率框架** | A42/B22/C11/D25 显式概率 + 触发条件 | 卖方研报通常单一基准 + 上下行；不公开概率 |
| **南向通实操路径（附篇 B）** | 单人 300 万额度配置、跨境理财通、QDII 溢价窗口 | 美资机构不针对中国境内投资者写实操 |
| **反叙事压测（附篇 D/E）** | 伯克希尔抄底神话祛魅、聚变能否拯救 AI 叙事 | 机构倾向跟随主流叙事，反叙事写作风险高 |

---

## 五、V1.3 升级路线图（来自本档对标分析）

| 优先级 | 来源 | 可补内容 | 落点章节 | 工作量 |
|--------|------|---------|---------|--------|
| ① | Goldman $7.6T 模型 | §3 加 compute/DC/power 三层拆解表 | §3.1 后 | 中 |
| ② | Morgan Stanley 信贷结构 | §2 加 "IG 债市场结构性变化" 小节 | §2.5 后 | 小 |
| ③ | SemiAnalysis HBM 48% / 40GW | §2 加 "HBM 层利润迁移 + 物理约束" | §2.6 后或新增 §2.11 | 中 |
| ④ | BofA Arya "2028 延长" | §6 A 场景 "延长 18 个月" 敏感性分析 | §6.1 后 | 小 |

**完成后定位升级**：
- 当前 V1.2：「独立研究者的优质综合框架」
- V1.3 目标：「综合广度超过任何单一机构 + 中国视角独有」

---

## 六、信源说明

本档所有机构引用均来自 2026/05-06 公开渠道。Bloomberg/Reuters 终端引用与公开报道交叉验证。**大队长报告作者不就任何机构研报的准确性背书**，所有数据以原始机构发布版本为准。

【风险提示】所有内容仅代表个人基于公开信息的研究与观点表达，不构成任何投资建议、买卖要约或操作指令。股市有风险，投资需谨慎。

---

*文档版本：2026/06/27 初版 · 大队长出品*
