# AGI与国际格局

大队长出品 · V1.7 · 2026-10-27

联系邮箱：fqsx@mail.ustc.edu.cn

## 免责声明

本报告为“大队长”基于公开资料形成的个人研究，不代表任何任职机构，不构成个性化投资建议、收益保证或交易指令。研究判断可能错误，公开信息可能随后修订。

资料核验截至2026年10月27日（北京时间），各财务、市场、技术与政策数据使用正文注明的报告期或观察日，并非全部是同日现值。公司指引、条件算例和已实现结果分开；没有证据的输入留空，未完成校准的情景不提供精确概率。

这是按现行判断重新组织的正文，不是历史原页加滚动校注。旧稿独立存档；原预测条件不倒改。段落中的核验范围以具体来源为准，不等于对全部历史事实重新审计。

## 本次更新

1. 把历史原页与校注叠加改为现行正文，原339页中的独有主题保留，重复分册合并；本册不嵌入旧版。

2. 目录、书签和页码全部由本册正文重建；变更一条一段，集中列出参考资料，保留淡蓝色图表并加“大队长出品”水印。

<!-- BODY_START -->

口径截至2026年10月27日（北京时间）。技术测试保留发布时的版本、预算与观察日，政策状态以文中注明日期的已取得文件为依据；本轮抽核GAO法律决定，未完成全部EAR沿革及所有模型的当日重测。历史统计、机构预测与作者情景分别列示。

## 第四部分：AGI何时到来？

9月初的新模型，使“能力还没有进步”越来越难成为谨慎定价的理由。Anthropic 在9月1日发布 Fable 5.1 与 Mythos 5.1，Google 在9月2日发布 Gemini 3.8 Flash 与 Flash Cyber，OpenAI 在9月3日发布 GPT-6 Astra；这些产品既拓展长流程任务，也呈现不同的部署限制。对本报告而言，需要重估的是从任务能力到经济产出的传导速度，而不是因为过去担心泡沫，就维持一个必然推迟的 AGI 时间表。[Anthropic 发布说明](https://www.anthropic.com/claude-fable-and-mythos-5-1)、[Google 发布说明](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/)、[OpenAI 发布说明](https://openai.com/index/gpt-6-astra/)

模型在某类测试中跨过人类参照线，是技术证据；企业敢不敢交给它连续执行真实业务，要加上可靠性、权限、数据和责任；能力创造的收益最终由模型厂商、应用商、员工还是客户取得，则由竞争和合同决定。把这几层压成一个AGI年份，再让该年份解释估值与市场转折，会漏掉最重要的商业传导。

### 4.1 实验室的时间表，应怎样读

公开预测的价值，在于暴露预测者对技术路径的假设。它不是一组口径一致的测量值。有人讨论能否完成多数高价值工作，有人要求跨领域学习达到人类水平，还有人谈的是远超专家群体的超级智能；把这些年份排在一起取中位数，得到的只是一个数字，并没有得到共同定义下的概率。

Dario Amodei 在2026年1月《The Adolescence of Technology》中继续讨论短时间内出现强大 AI 的可能，并保留时间可能更远的限定。他设想的是具备广泛专业能力、可大规模复制的系统，不只是一个聊天产品升级。本文把它作为实验室负责人提出的风险情景，不作为“2027年已经得到确认”的事实。其商业利益需要识别，技术论证也不能仅因商业利益就被忽略。[Amodei 原文](https://darioamodei.com/essay/the-adolescence-of-technology)

另一种更便于研究的进展，是 Google DeepMind 2026年3月16日公布的认知评估框架：把一般认知能力拆成十类，并要求用有保留测试、有人类参照的任务形成能力画像。这一方法没有解决所有定义争议，却比“某位负责人说还差几年”更适合持续更新，因为可以明确看到某一能力改善、另一能力仍薄弱。[DeepMind 认知框架](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf)

实验室管理者与研究者的观点可以提供技术路径和风险假设，却不适合按人物声望加权成一张AGI时间表。引用任何人的预测，都应取得原始访谈、发布日期、定义和限定条件；商业利益值得披露，不能替代对论证本身的检查。

预测市场也遵守同一纪律。要保留一个数字，至少要同时存下问题的结算条件、截止日期、观察时点和聚合方式；“通用智能首次宣布”“多数职业自动化”“超级智能”不能互相替代。未保存这些条件及同期快照的预测市场数字，不进入当前时间判断；交易价格也不能脱离流动性、参与者与结算规则被称为客观共识。

**本篇的时间判断是：能力继续快速改善有证据，通用性和经济替代程度仍须分别验收；暂不提供统一 AGI 到达年份或经校准概率。** 一个可用的时间判断，必须先说明什么算到达，以及什么新证据会使判断前移或后移。

### 4.2 Scaling：从“算得更多”转向“交付同一结果花多少代价”

预训练、后训练、推理时计算和外部工具共同改变系统能力，不能用其中一代模型的表现宣告整条路径结束。某代模型未达预期，不足以证明预训练缩放失效；推理预算增长，也不是“思考越久越好”的普遍规律。预算增加后，某些任务会改善，某些任务可能更早到达收益平台；若增加搜索只是反复走入错误路径，更多计算并不自动变成更可靠的答案。

评估应固定任务、工具和质量门槛，再比较成本，而不是只比每百万 token 的价目表。一项业务的有效成本至少包含模型调用、重试、工具调用、基础设施、人工复核和失败返工。模型 A 单次调用更便宜，若需要多次尝试和大量人工检查，交付一个合格结果未必便宜；模型 B 单次更贵，但能减少流程往返，也可能更有经济性。这是本篇的研究方法，不是对任何厂商成本的实测结论。

9月的公开评测提供了一个具体例子。同一模型发布页上的高分项目和低分项目并存，不能挑最醒目的一个分数代表全部能力。下表仅记录当次发布披露，不制作跨年份“智能总量”曲线。

| 当次披露 | 可核结果及条件 | 应怎样使用 |
|---|---|---|
| OpenAI GPT-6 Astra，9月3日 | FrontierMath Tier 4（v2）97.6%；AutomationBench 41.4%；发布页注明各推理预算中的最高结果，研究/API环境可能不同于产品环境 | 专门数学测试与业务流程测试进展不均，不能用前者代替后者 |
| Anthropic Fable 5.1，9月1日 | OSWorld 2.0 部分计分77.9%、严格计分41.7%；HLE无工具60.9%、有工具65.0%，且有生产防护参与 | 同一模型换验收规则或工具，结论会明显变化；不能与其他设置的分数直接排行 |

来源：[OpenAI 评测表及脚注](https://openai.com/index/gpt-6-astra/)、[Anthropic 评测表及防护说明](https://www.anthropic.com/claude-fable-and-mythos-5-1)。这些是厂商披露，不是本文完成的独立复测。

SWE-bench、HLE、ARC-AGI、GPQA和FrontierMath分别测量不同任务。建立趋势图时，每个观测点应绑定模型版本、数据集版本、工具、尝试次数、预算和测试日期；关键设置变化就另开序列，不能把不同基准的饱和速度画成统一的智能增长曲线。

长任务能力的进展也需要这样读。METR 的50%时间跨度，是根据人类完成任务所需时间拟合出的成功率尺度，不是“AI已能稳定独立工作这么久”。METR 在2026年3月20日说明，修正拟合错误会改变既有结果，任务分布与统计选择也会显著影响估计。因此，时间跨度结果必须连同成功率、样本范围和拟合方法阅读，不能直接改写为若干小时稳定自主工作。[METR 方法与修订](https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/)

对 DeepSeek 的讨论回到已公开产品与技术材料。官方透明中心列明 DeepSeek-V4 于2026年4月24日发布，提供模型卡和技术报告入口；模型卡、技术报告和实际部署配置应相互对应，未取得原件支持的模型名称、参数、分数和显存组合不能用作低成本突破的证据。API报价也不等于训练成本，低报价可能包含效率改善、补贴或商业选择，只有完整成本口径才能区分。[DeepSeek 官方透明中心](https://www.deepseek.com/en/transparency/)

我的判断是：**竞争正在从一次回答的能力，延伸到一项工作能否在可接受的预算和风险内结束。** 如果高分没有减少人工检查，企业支付的对象仍然是辅助工具；若任务验收率提高、复核成本下降且能持续复现，应用收入的扩张才有更扎实的基础。

9月22日，OpenAI发布Sol与Luna，Anthropic发布Opus 5.5，竞争继续向不同能力与成本层级展开。Anthropic称Opus 5.5典型工作成本比Opus 5低40%，但其中包含标价与任务耗用量变化；这一厂商声明需用固定任务和验收标准复测，不能直接推出企业人员成本下降40%。这些产品扩大了可选的部署方案，仍没有给出统一AGI到达日期。[OpenAI官方变更记录](https://developers.openai.com/api/docs/changelog)、[Anthropic发布说明](https://www.anthropic.com/claude-opus-5-5)

### 4.3 AGI定义：能力、通用性与自主性不能互相替代

本文保留三类讨论，但不把它们当作已排好先后的三个到达日期。

| 讨论对象 | 真正需要回答的问题 | 不足以单独证明它的证据 |
|---|---|---|
| 经济上有用的强 AI | 在什么行业、质量和总成本条件下，能够完成多少付费工作？ | 竞赛高分、用户数、单次演示 |
| 广泛的人类水平认知能力 | 在未专门准备的新任务上，学习、推理、记忆和迁移是否足够稳定？ | 少数任务超人、长上下文长度、模型自己声称理解 |
| 超级智能与高度自主系统 | 在广泛领域能超越多强的人类参照，且可以多大范围独立行动？ | 更快回答、更多并行实例、某项安全阈值被触发 |

DeepMind 2023年的“Levels of AGI”把表现深度、能力广度与自主性区分开来；2026年6月12日“From AGI to ASI”继续讨论 AGI 之后的多种发展路径，而不是给出一个从当前模型直接通向超级智能的保证。本文采用这一区分，但表中的经济验收问题属于作者用于产业研究的操作化方法。[AGI 层级论文](https://arxiv.org/abs/2311.02462)、[DeepMind 后AGI研究](https://deepmind.google/research/publications/239142/)

安全限制也不能简单当作能力不足。模型可能具备一项潜在能力，但部署方因为风险而限制访问；反过来，移除防护后的研究成绩，也不能等同于客户可购买的生产能力。OpenAI 9月3日称 Astra 达到其内部准备度框架的网络安全 Critical 等级，同时披露监控难度与额外部署防护。这是厂商风险分类及测试结果，并非跨机构共同认可的 AGI 认证，也不能推成现实世界普遍失控已经发生。[OpenAI 安全说明](https://openai.com/index/safety-overview-gpt-6-astra/)

Google 的同次发布提供了另一种对照：3.8 Flash与Flash Cyber使用同一基础智能，但网络安全防护和开放对象不同。前者进入API、企业及订阅产品，后者因网络安全限制更宽松，仅通过Fairwind计划提供给可信防御方。这个差异提醒我们，评估客户实际可用的能力，必须连同产品版本、权限和防护配置记录，不能把受限环境的成绩全部折算为普通客户能够购买的服务。[Google部署与防护说明](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/)

投资研究需要同时保留这两种方向：能力变强可能拓宽收入来源，防护、审批、责任和数据隔离也可能增加交付成本。把产品受限全部解释成“模型不行”，或把实验室上限全部折算成即期收入，都会误读商业化速度。

### 4.4 算力、电力和数据，怎样约束而非决定时间表

推断AGI时间，需要同时考虑算法、数据、评估方式和组织能力。算力是重要投入，但投入扩张和能力进展之间没有一张经验证的 AGI 年份换算表；同样的硬件规模，可以因利用率、通信、故障和训练方案不同而产出不同结果。

安全工程也会改变训练进度。OpenAI9月1日说明，在此前Hugging Face事件后，曾暂停部分前沿训练两周，其中包含部分Astra训练；某些更大的强化学习运行暂停更久，8月28日已恢复此前暂停的一项大型运行，部分小规模实验仍暂缓。公司同时明确Astra没有参与原事件。这是特定训练流程的暂停与恢复，不能写成所有训练停摆，也不能据此推算AGI统一延期；它说明硬件就绪之后，隔离、监控和安全验收仍可能约束有效研发进度。[OpenAI训练与恢复说明](https://openai.com/index/path-to-astra/)

**先看能够运行的集群，而不是宣布的功率。** 一处站点的公告可能分别提到土地容量、获批供电、已通电容量、已安装服务器及正在提供服务的能力。它们不是五种说法指向同一个数量。从规划功率推算有效训练算力，必须有项目清单、投运节奏与利用率；缺少这条转换链，就不能得到可靠的扩张倍数或AGI年份。

**电力约束是地方性的，也会被重新分配。** 数据中心关心的不只是全国发电量，还有特定节点的变压器、输电、备用电源、许可和可用时间。发电项目排队接入电网的统计，不能直接套给所有新增用电负荷；自备电源也有设备、燃料和监管约束，并非天然快捷通道。第五部分用 IEA 更新说明需求规模，本节只保留机制：某个地点延误，可能带来迁址、降密度、分期投运或推迟交付，不能直接宣布全球技术路线因此延后若干年。

**先进制造约束要穿透到系统交付。** 先进制程、HBM高带宽存储器、先进封装、网络设备和整机集成都可能限制数量，但“封装晶圆/月”不能直接换算成“每年几座训练中心”。需要知道晶圆尺寸、产品组合、良率、每个封装所需资源、芯片互联方式及单站配置。在这条计算链缺失时，封装扩产数量不足以确定能建成多少训练中心，更不能直接推出固定年数的技术延期。

**数据约束应按任务讨论。** 高质量、新颖、可合法使用的数据更有价值，不等于互联网文本已全部用完。可自动验证的数学或代码任务，与依靠现实反馈、隐性知识和复杂评价的任务，获得可靠训练信号的难度不同；合成数据能扩展某些训练，也需要筛选与独立检验。对于未披露训练集的模型，无法据公开文本存量推定它已经消耗了多少比例的可用数据。

下表将能力、部署和定价拆成三种可检验情景，不分配概率，也不据此预测某年到达AGI。

| 情景 | 需要观察到的变化 | 研究含义 | 使该情景失效的证据 |
|---|---|---|---|
| 能力与部署共同加速 | 新任务稳定通过，单位合格任务成本下降，客户从试点扩为持续使用 | 应提高商业化速度假设，复查过度保守的采用率 | 成绩只在特定工具或高预算下成立，客户留存和验收未改善 |
| 能力改善、交付受阻 | 评测提高，但接入、数据治理、责任或供应交付持续拖延 | 延后受影响业务现金流，保留其他已可用场景收入 | 客户在同等合规要求下快速规模部署 |
| 成本改善、价值被竞争让渡 | 替代模型多、降价快，客户获得明显收益而厂商利润率承压 | 区分产业生产率提高与模型供应商的投资回报 | 产品差异和迁移成本使净价格、续约及利润率保持稳定 |

这张表留下的开放问题很具体：下一次能力跃迁，能否让需要反复人工复核的任务真正减少复核？新建算力是先满足增长的付费需求，还是先成为固定成本？这比保留一个看似精确的 AGI 年份更值得跟踪。

### 4.5 从技术时间表到估值：只折现受影响的现金流

AI 公司的现金流可以来自广告效率、云服务、代码工具和企业自动化，不必等到所有人都承认 AGI 已经到达。因此，即便没有统一的AGI认定，既有业务也可以用现金流估值；某些远期估值确实可能依赖尚未验证的大规模采用，必须通过公司模型识别，不能先给整个行业统一贴上一个比例。

没有现有业务、未来业务、资本投入和融资条款的拆分，就无法从一个融资估值倒推出AGI叙事占比，也无法预先给延期套用统一折价。私募不同轮次的权利条款还会影响表面估值的可比性；应先识别被延期的是哪一段现金流。

可以保留的是一个透明的折现计算。假设某一段原本会产生的现金流**整体后移三年，金额与风险不变**，它的新旧现值比为 `1 / (1+r)^3`。这不是任何公司的目标价，也没有纳入额外投入或业务流失。

| 年折现率 r（情景输入） | 该段现金流后移三年的现值保留比例 | 该段现值减少 |
|---|---:|---:|
| 8% | 79.4% | 20.6% |
| 10% | 75.1% | 24.9% |
| 12% | 71.2% | 28.8% |

如果仅有40%的企业价值来自这段被延后的现金流，那么在10%折现率这一简化情景下，企业价值的纯时间损失为 `40% × [1 − 1/(1.1)^3] ≈ 9.95%`，不是24.9%，更不是自动变成40—55%。40%只是演示输入，不能反向称为市场已经给 AGI 分配了40%的价值。

竞争可能进一步降低远期净价格，新增训练或服务支出可能减少净现金流，融资可能稀释普通股权益；这些因素都需要进入对应年度的模型，而不是在纯折现损失之上再随意加一个折价。需求超预期、成本下降或者其他业务改善，也可能部分抵消延期损失。方向必须由模型输入决定。

能力到现金流确有时滞，但不同企业与业务不适用统一的采购周期或投产空窗。应逐场景看付费试点、扩容、续约、合同责任和回款：开发工具的用户可能当天尝试，金融核心流程则可能经过数据权限、审计和多层验收。把两者放进同一个采用率，会高估某些业务，也低估另一些业务。

同理，电力和半导体资产不因 AGI 推迟就天然安全。有明确客户、可执行长约和可承受债务的项目，与依靠未来租约填满的投机性扩建，风险截然不同。能源或设备需求增加，最终还要经过竞争、定价、资本开支和营运资金才到股东回报。本文保留对兑现时间和资本错配的警惕，不提供一个只凭 AGI 判断即可成立的对冲组合。

### 4.6 我可能错在哪里

第一，9月的新模型可能正处于企业采用加速的早期，既有收入与就业数据天然滞后。如果多家客户持续披露同类业务的验收率、人员投入和净收益改善，只用历史落地慢来压低采用率，会低估这一轮变化。

第二，过度强调榜单限制，也可能漏掉真实技术跃迁。标准化评测不是全部，但也不是没有价值；应保留可复现进步，同时用新任务、不同预算和实际交付补充，而不是因为结果与原判断冲突就否定评测。

第三，物理瓶颈和数据瓶颈会随着架构、调度与算法变化而移动。如果同等质量的工作需要明显更少的计算，旧产能可能获得更多产出；若更便宜的能力诱发更多调用，绝对需求又可能上升。不能只选择有利于看多或看空的一半机制。

最后，本篇没有完成 AGI 概率校准，也没有把全部前沿模型放进同一个独立测试。保留缺口意味着暂时少说一个数字，不意味着可以停止研究；后续研究需要优先补真实工作样本，而不是再添一张名人预测时间表。

## 第五部分：AI如何颠覆国际格局？

中美模型的竞争不等于两国完整产业能力已经相同，芯片受限也不等于受限的一方无法做出有价值的应用。AI 对国际格局的影响，要沿着模型、制造、能源、资本、制度和应用扩散分别观察；其中一层收敛，另一层完全可能仍受约束。排行榜接近不能证明所有产业能力等同，某类芯片销售受限也不能代表中国AI市场消失。

### 5.1 中美模型差距：先修正量尺，再讨论追赶

衡量中美模型差距，首先要检查量尺能否支持百分比。Arena 的配对偏好和 Bradley–Terry 类评分反映特定样本中哪种回答更常被选中，分数原点和尺度不提供“智能相差百分之几”的意义；将30分除以某个总分，不能得到30分所代表的能力比例。即使榜单采用不同评分实现，这条“相对评分不等于能力比率”的限制仍然成立。[Arena 评分方法说明](https://arxiv.org/html/2403.04132v1)

Stanford《2026 AI Index》确实认为中美前沿模型表现差距大幅收窄。这支持“竞争更接近”的方向，但报告有统计截点，不能当成10月27日所有模型、所有任务的实时排名，也不能推出成本、长任务、安全和商业化能力全面一致。这是一项有统计截点的收窄判断，不提供可直接用于当前估值的“智能百分比”。[Stanford 2026 AI Index](https://hai.stanford.edu/ai-index/2026-ai-index-report)

要形成一张对投资有用的比较表，我会同时记录任务正确率、同质量成本、响应时延、中文及专业数据适配、部署权限、工具调用和失败恢复。中国模型在中文应用和本地部署上可能更符合某些客户需要，美国模型在另一些复杂任务上可能有优势；两者都应在目标场景里验证，而不是用国别替代模型版本和工作负载。

DeepSeek-V4 的官方发布和华为云2026年4月24日首发适配说明，能够核实模型与国产平台服务适配的进展。这是有意义的工程证据，但模型可在某平台运行，不等于它全部训练阶段都在该平台完成，更不等于所有企业迁移成本已经消失。完整前沿训练的自主供给，需要另取训练配置与系统证据。[DeepSeek 官方透明中心](https://www.deepseek.com/en/transparency/)、[华为云首发适配](https://www.huaweicloud.com/news/2026/20260424172129152.html)

### 5.2 主权AI：比较实际能力，而不是把公告金额相加

主权 AI 的合理诉求包括数据治理、关键服务连续性、本地语言、产业能力和政策自主。买到外国芯片、租到海外模型与拥有本地长期运维能力，满足的是不同层次的需要；国有资本参与也不自动等于项目具有商业回报。

**美国：把 Stargate 的承诺与运行分开。** OpenAI 2026年1月20日官方更新称，Abilene 已在训练和服务前沿系统，同时把2029年10GW目标及超过半程的数量明确称为规划容量。已经提供服务是比签约更强的证据，却不能据此宣布整个10GW都已投运。多年投资目标、各站点预算和供应商合同可能指向同一项目，不应重复加总。[Stargate 官方进展](https://openai.com/index/stargate-community/)

**沙特：首期、五年规划与当地吸收能力不同。** NVIDIA 与 HUMAIN 2025年5月13日公告的范围是未来五年最高500MW、数十万颗GPU的规划，首期为18,000颗GB300系统；这不能写成“已采购50万颗GPU”。芯片到货以后，还要解决机房、电力、网络、运维与客户需求，才形成可出售的计算服务。本轮仍未取得各期验收与利用率的连续一手记录，因此不把旧规划升级成2026年10月27日已验证投运规模。[NVIDIA—HUMAIN 公告](https://nvidianews.nvidia.com/news/saudi-arabia-and-nvidia-to-build-ai-factories-to-power-next-wave-of-intelligence-for-the-age-of-reasoning)

**欧洲：动员投资不是财政已经支出。** 欧盟 InvestAI 的2000亿欧元目标包括动员公共和私人资本，其中200亿欧元用于巨型AI设施的安排也不等于全部资金已拨付。欧委会的具体设施页面强调以欧盟、成员国与金融机构资金降低风险、吸引私营投资。研究时要继续跟踪项目遴选、融资关闭、建设和使用，不把政策目标直接放进年度设备收入。[欧盟AI行动计划](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A52025DC0165)、[欧委会AI Gigafactories](https://commission.europa.eu/topics/competitiveness/competitiveness-coordination-tool-projects/ai-gigafactories_en)

**印度：区分已供给与拟增购。** 印度政府2026年2月17日披露现有38,000颗GPU，并宣布随后增加20,000颗；同一声明中的未来两年超过2000亿美元投资，是预期而不是到账记录。本文保留这些数值的公告日期，不把38,000与20,000相加后称为10月已验证运行的58,000颗。[印度PIB公告](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2229171&lang=1&reg=1)

**中国：应用扩散需要比装机更细的验收。** 国家发展改革委2025年8月26日对国务院“人工智能+”意见的解读，把科学、产业、消费、民生、治理和全球合作列为重点，并强调应用与基础能力供给协同。政策目标应与实际采用分开；也不能从安全可控要求推出所有国资云和政务云拥有同一个全国强制国产比例。[国家发展改革委政策解读](https://www.ndrc.gov.cn/xxgk/jd/jd/202508/t20250826_1400058.html)

英国、日本及阿联酋等地仍是重要观察对象，但本次没有逐个复核其全部项目进度，不再给出缺少边界的“全球主权AI总投入”排名。对这些项目，后续应统一收集投运容量、可用时间、单位成本、外部客户收入和对单一海外供应商的依赖；把地区间可比较的指标补齐，比把各种意向金额汇总成一个更大的数字更有价值。

### 5.3 军事与安全：采购需求、可部署能力和实战效果三层证据

AI 的军用价值不能靠公司估值证明，估值也不能用每一份政府合同总额直接解释。美国国防部2025年5月21日公布 Palantir Maven Smart System 软件许可合同的7.95亿美元修改金额，是可核的采购记录；它不是当年已确认收入，更不提供模型在某次行动中的效果测量。[美国国防部合同公告](https://www.defense.gov/News/Contracts/Contract/Article/4194643/)

军用AI公司的私募估值、资金和调用次数，与可交付能力之间没有固定换算关系；如果没有原始合同条款、客户验收和可公开验证的任务结果，不能写成军事 AI 已全面规模化成熟。

从产业研究角度，可以按证据强度逐步推进：先核正式预算和采购，再核可部署范围、权限与责任，最后才讨论持续服务收入、毛利和续约。某项实验、演习或厂商演示能够说明技术方向，但不能越级成为实战效果的证据。军工客户还可能要求专有集成、离线环境和长周期认证，这些成本不能被“软件毛利率高”的一般印象遮住。

前沿模型的网络安全能力使这一问题更紧迫，但安全发布材料主要说明受控测试和防护边界，不应被用来渲染未经证实的作战能力。对投资者，更可核的影响是客户安全预算、产品可用范围和部署责任怎样变化，而不是凭一次演示押注全部军事格局已经重写。

### 5.4 就业冲击：年轻群体、招聘变化与因果边界

本节采用 Stanford Digital Economy Lab 2026年8月修订的“Canaries in the Coal Mine?”。作者报告：在其分析中，22—25岁、从事AI高暴露职业的年轻人，就业相对较低暴露同龄人的参照路径落后19%；分化主要通过招聘减少而非离职增加体现。同时，研究没有发现全经济范围的普遍岗位替代，作者把这些结果定位为描述性早期信号，不是AI造成失业的因果估计。[Stanford 修订研究](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/)

这项结果不能改写成“初级程序员岗位下降19%”：年龄不等于工作年限，高暴露职业不只包括程序员，相对参照路径的落后不等于绝对岗位同比下降19%。此外，教育控制、样本选择和部分既有趋势都会影响解释，不能省略这些限制后宣称AI已经消灭了对应比例的岗位。

Anthropic Economic Index 更适合回答用户把什么任务交给模型、如何使用，而不是用来计算全国就业变化。2026年3月24日发布的“Learning curves”研究观察的是2月Claude使用，用户自选样本不等于全部劳动者或企业。使用量上升既可能是自动化，也可能是增强工作，两者对招聘和产出的影响不同。[Anthropic 研究与样本说明](https://www.anthropic.com/research/economic-index-march-2026-report)

IMF此前关于发达经济体约60%岗位可能受AI影响的结论，讨论的是暴露和互补/替代潜力，不是60%岗位消失。其2026年1月的新技能研究继续把劳动市场变化拆为技能需求、工资和机会差异，提示单一失业总量并不能概括转型。[IMF 暴露度原文](https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity)、[IMF 2026技能研究](https://www.imf.org/en/blogs/articles/2026/01/14/new-skills-and-ai-are-reshaping-the-future-of-work)

这会怎样进入国际竞争分析？如果入门任务减少而资深人员产出提高，短期生产率和长期人才培养可能朝相反方向走；企业节省的成本，也未必全部转成利润，可能通过降价交给客户。应跟踪招聘结构、岗位职责、单位产出、工资和培训，而不是仅盯一份裁员名单。中国、印度和美国在服务出口、产业结构和人才路径上不同，不能把美国某一年龄组样本直接外推成全球就业预测。

本篇据此提高对年轻劳动者入门机会和组织培养机制的关注，但没有把该研究升级为“AI已经引发宏观衰退”，也没有给出净失业人数预测。

### 5.5 能源格局：采用IEA 2026更新，区分需求与投资回报

IEA 2026年4月16日《Key Questions on Energy and AI》把全球数据中心用电估计更新为2025年485TWh，并在其中心预测中给出2030年约950TWh、约占届时全球用电3%；其中AI导向数据中心用电预计增长更快。这里的485和950均是**全部数据中心**口径，2030数字是预测，不是已经发生的需求。[IEA 2026更新](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary)

IEA 2025年报告的2024年415TWh、2030年945TWh可以用于说明预测沿革，不能与新基年混成一条实际增长序列。全球数据中心、美国数据中心和AI子集的用电范围也不能混用，年度用电量与用电增量占比应另列。[IEA 2025版](https://www.iea.org/reports/energy-and-ai/executive-summary)

| 比较项 | IEA 2025年报告 | IEA 2026年报告 | 可得出的结论 |
|---|---|---|---|
| 全球数据中心基年用电 | 2024年415TWh | 2025年485TWh，IEA2026年估计 | 基年向前推进一年，不能称为原年数值被上修 |
| 全球数据中心2030年用电 | 2025版预测945TWh | 2026版预测950TWh | 中心预测接近；不能据此说全部近期瓶颈已经解决 |

用电增长首先改变的是地区负荷结构。对于已有稳定低成本电源、网络和变压器余量的地区，新增负荷可能提高现有资产利用率；对于本已紧张的地区，新增负荷则需要扩建，建设成本由谁承担、能否收回，会成为居民、监管机构、开发商与公用事业公司的分配问题。因此，“需求更大”与“现有股东赚得更多”之间，还隔着电价机制和资本成本。

核电重启是一个可核的案例，但仍要区分融资与投运。美国能源部2025年11月18日宣布为835MW的 Crane Clean Energy Center 重启项目提供10亿美元贷款；贷款协议完成交割并不代表机组已经重启，更不能从单一项目推算美国2030年前会新增25GW核电。后续应查许可、施工、试验和实际发电，而不是把长期购电协议当成当期电源。[美国能源部项目公告](https://www.energy.gov/articles/energy-department-closes-loan-restart-nuclear-power-plant-pennsylvania)

中东的能源和资本、北欧部分地区的电源与气候、中国东西部的负荷和能源互补，都可能影响选址，但低电价不是完整竞争力。训练、推理与实时交互对延迟要求不同，电费优势可能被数据跨境、网络、人才、设备和低利用率抵消。我们需要的是可用、稳定、合规且有客户的计算服务，不是孤立比较一度电的价格。

能源与电网是重要约束，但电力需求增长不保证所有相关企业受益。能够锁定优质客户、合理分担扩建成本且不承担过量闲置风险的企业，更可能把新增需求变成回报；若项目依赖高利用率才能覆盖债务，而客户仍处于试用阶段，技术乐观反而可能放大财务风险。

### 5.6 从货币到制度：国家议价力来自什么

先进计算资源可以影响谈判，但它不是字面意义上的硬通货。芯片有迭代、故障和使用场景，计算服务有时效和地域限制，无法像统一货币那样直接互换。从某个项目使用美元结算，到美元体系地位变化，还隔着贸易、储备、资产供给和资本流动，不能跳过这些环节建立直接因果。

更值得研究的是控制权落在哪里：模型接口能否被单方面关闭，数据与日志由谁处理，软件更新依赖谁，芯片与备件是否持续可得，关键岗位由本地团队还是外部供应商运行。主权基金可以买股份，也可以买服务或建基础设施，三种行为的现金流、稀释、控制权和政治目标并不一样，不能合并成一个“主权资金托底”的利好。

规则本身也是竞争因素。欧委会2026年7月31日说明，8月2日起开始相关执法及新的透明度要求，包括部分系统告知用户正与AI交互、特定合成内容标识。这些是已进入实施阶段的事项，不再只是未来日历；也不能把这一日期写成所有高风险系统义务在同一天全部生效。[欧委会7月31日说明](https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august)

对供应商，这类要求可能增加标识、日志、评估和客户支持成本，也可能让已具备合规能力的企业获得采购信任。究竟形成壁垒还是压缩利润，要看新增成本、可执行的统一标准和客户是否愿意支付，不能预先假定“监管强就必然落后”或“监管强就必然拥有定价权”。具体法律适用仍需按产品、主体及正式文本另行判断，本文不是合规意见。

贸易影响应分开观察服务出口与设备资本流入。代码、翻译和数据处理成本下降，可能压低依赖标准化工时收费的服务出口价格，也可能让企业承接更多项目；建设数据中心带来的进口设备和资本流入，则是另一条现金流，不能自动抵销前者对收入与就业的影响。制造业也需要分别验证自动化投入、单位成本与产品需求，不把劳动力价格优势弱化写成所有新兴经济体必然失去竞争力。这些是传导假设，而非本轮已估计的国别GDP影响。

先进制造的地域集中同样有双重性：既能形成议价力，也使供应中断的影响更集中。所谓“硅盾”不是可以直接代入估值的安全保证，应通过供应商、产能地区、备份能力和关键交付期分析风险。技术地位重要，并不意味着地缘风险已经被技术地位抵消。

### 5.7 模型与硬件：两条曲线保留为可检验框架

9月28—29日Sonnet 5.5和GPT-6.1 Sol继续降低部分工作流的用量或缓存费用，但能力提高、任务成本下降与企业回报仍是三道验证。厂商测试及公开价目支持预算重算，不支持提前给出统一AGI年份或行业利润率。[Sonnet 5.5发布](https://www.anthropic.com/claude-sonnet-5-5)、[GPT-6.1 Sol发布](https://openai.com/index/introducing-gpt-6-1-sol/)

“模型竞争更接近、训练硬件差距仍大、推理替代更快”可以作为研究假设，但不是已经量化确认的统一事实。模型能力、训练集群效率和推理部署成本之间有联系，却没有一一对应关系，需要独立测量。

**前沿训练关注的是系统效率。** 单颗芯片的理论浮点算力只是输入之一。大规模训练还取决于存储带宽、互联、通信算法、编译器、容错、调度、有效利用率与整轮训练能否完成。把某国产芯片说成“H100的70%”，若不说明精度、模型、并行规模、软件栈和功耗，就不足以形成采购或产业判断；用这个百分比再推国家落后几代，更不可靠。

**推理关注的是目标工作负载。** 固定模型、上下文、输出质量和延迟后，比较吞吐、每个合格任务成本和运维投入，才可能判断国产设备在哪些场景具有竞争力。短文本批处理、长上下文检索、低延迟对话和复杂多轮代理，对算力、带宽与存储的要求不同，不能从某一种任务成功迁移推出整个推理市场已完成替代。

**后训练进展不能冒充预训练已全面替代。** 适配、微调、全参数后训练、完整预训练的计算规模和目标不同。例如，910C后训练材料不能替代完整预训练证据；具体科研结果若没有原始论文、配置和独立复现，就不再往前补猜厂商的整套训练来源。

| 研究层 | 验收时应取的证据 | 仍不可直接推出 |
|---|---|---|
| 模型 | 同任务质量、预算、版本和独立复测 | 国家综合AI实力相同 |
| 前沿训练硬件 | 训练日志、集群规模、利用率、故障与实际成本 | 单卡理论算力等于整集群效率 |
| 推理硬件 | 指定服务质量下的吞吐、延迟、能耗和迁移成本 | 一个适配案例覆盖全部企业 |
| 产业兑现 | 交付、客户验收、复购、回款及利润 | 出货规划等于收入或利润 |

国产替代可能提供订单机会，但并非所有环节都能同时获得高利润。下游替代加速时，上游设备、存储或关键材料也可能遭遇限制；进口产品重新进入时，本地客户可能受益而本地供应商面临压价。测算替代率必须明确分母是出货、算力、工作负载还是客户支出，并给出同期一手来源；没有统一分母的百分比不进入模型。

**开放生态的入口也在变化，但交易状态必须说清。** NVIDIA于9月2日签署收购Hugging Face的协议，9月3日向SEC提交披露，预期在2027年上半年完成，仍须监管批准及满足交割条件。因此，截至截至已核证据只能称“已签约”，不能称“已完成收购”。研究意义在于芯片平台与模型、数据集分发入口可能联系更紧；这属于对竞争结构的判断，不是已经实现的排他控制。[交易8-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000078/nvda-20260902.htm)、[SEC披露日期](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000078/0001045810-26-000078-index.htm)

NVIDIA承诺继续支持开放模型和数据集，并保留用户对云、框架及不同硬件的选择，不要求使用NVIDIA算力。这是收购方的公开承诺，后续仍须验证平台治理和实际兼容性，不能由承诺推定开放性永久不变，也不能反过来断言中国模型会被自动排除。对国际竞争，值得跟踪的是跨芯片分发、模型可得性和监管适用怎样变化，而不只是交易规模。[NVIDIA开放生态说明](https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/)

本篇的判断是：**中国模型和应用有参与全球竞争的基础，硬件约束须按训练、推理和具体供应环节拆开；研究公司时，最终仍要核客户愿意为哪种可交付能力付多少钱。**

9月16日的MLPerf Inference v6.1提供了一组预览证据：NVIDIA披露Vera Rubin NVL72在Qwen3-VL和DeepSeek-R1上的吞吐最高分别达到GB300的3.7倍和2.5倍，软件栈及负载不同。MLCommons次日分析确认Preview类别；本文未独立复跑，不能把测试倍数当收入或利润倍数。[NVIDIA测试说明](https://blogs.nvidia.com/blog/vera-rubin-nvl72-mlperf-inference/)、[MLCommons方法与分析](https://mlcommons.org/2026/09/chairs-mlperf-inference-v6-1/)

9月30日证据已从预览推进到有限生产使用：CoreWeave称Rubin NVL72向指定客户有限提供，涉及数百颗GPU，Cognition是首个生产客户；其SWE-2推理在相同交互性能条件下，每GPU总token吞吐最高达到GB200 NVL72的4.8倍。这是客户测试、供应商发布，不是本报告独立验收；与前述不同模型、GB300基准的MLPerf不能拼成同一增长序列。设备小时成本及实际利用率尚缺，不能直接把单位成本除以4.8。[CoreWeave工程说明](https://www.coreweave.com/blog/cognition-becomes-first-customer-for-nvidia-vera-rubin-nvl72-on-coreweave-cloud)

NVIDIA同日称CoreWeave的V100仍在运行客户工作负载，反驳了“每次换代旧卡就立即无用途”的极端说法，却没有给出租价、余下成本或项目回收率。仍在使用不等于租金不降，也不等于所有旧卡投资已经回本。[NVIDIA生产部署说明](https://blogs.nvidia.com/blog/coreweave-agentic-ai-vera-rubin/)

对资本回收，效率改善有两面：同样设备投入可能支持更多收费任务，也可能降低旧设备的可承受租价。只有利用率、任务需求、功耗和实际采购成本进入同一模型，才能判断哪一面更强；不能将基准吞吐改善直接换算成全行业算力需求减少。

AMD于10月8日补充解释MI455X相对MI355X的测试：在DeepSeek-V4-Flash、输入输出各1,024 token的单GPU比较中，每用户20 token/秒门槛下总吞吐比为2.47倍，90 token/秒门槛下才达到33.98倍。测试来自AMD于7月使用预发布硬件与软件的厂商测量，不是10月交付验收，也不是对NVIDIA的比较。工作负载和交互门槛一变，倍数随之改变，不能把最高点直接除进全行业推理成本或转成投资回报。[AMD技术说明及测试脚注](https://rocm.blogs.amd.com/software-tools-optimization/mi455x-vs-mi355x/README.html)

### 5.8 出口管制：更新法律和商业事实，不把传闻写成规则

先看法律状态。BIS于2025年5月13日宣布不执行AI Diffusion Rule，并启动正式撤销程序；GAO于2026年5月12日公布的决定援引商务部答复，指出程序完成前规则仍载于CFR。因此，不能把宣布撤销写成已经完成正式废止，也不能不加执行状态说明地沿用旧三层安排。本轮重开GAO决定确认了这项历史法律状态，但未完成截至10月27日的全部EAR修订沿革核验。[GAO B-337935](https://www.gao.gov/products/b-337935)不执行该规则也不等于其他先进计算、最终用途和实体限制一并取消。[BIS 2025年公告](https://www.bis.gov/press-release/department-commerce-rescinds-biden-era-artificial-intelligence-diffusion-rule-strengthens-chip-related)

2026年1月13日还有一项已公布的调整。BIS 对 NVIDIA H200、AMD MI325X 及类似芯片向中国出口的申请改为在安全条件下逐案审查，并提出美国供给、买方合规和第三方检测等要求。这不是全面自由出口，也不是所有买方都已获许可。[BIS 2026年1月13日公告](https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china)

还要补上2026年5月31日的BIS指引：对于总部或最终母公司总部位于D:5国家组或澳门的主体，即使实体设在其他境外地区，出口属于该指引范围的先进计算物项仍须申请许可，除非适用规定的许可例外。该要求源自2023年，不能把2025年不执行AI Diffusion新增要求理解成一并取消。研究海外供给时，要同时核最终母公司、物项与具体许可，不能只看机房所在地。[BIS 5月31日正式指引](https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf)

同一指引也保留存量运行边界：其他活动符合EAR的正常数据中心运营商，在进一步通知前，无须仅因此停止现有物项的使用、存储、处置或维护。它并不是要求所有境外存量机房停运的新禁令，不能省略这项限定后推算全面断供的规模。[BIS指引末段](https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf)

商业落地还需另核。NVIDIA 截至2026年7月26日季度的10-Q说明，美方已给予针对特定中国客户的小量H200许可，但中国方面的限制使公司未能出售所有获许可产品；已完成的部分许可项下发货，占最近季度Data Center收入不足1%。8月26日发布的下一季展望仍不假设中国 Data Center compute 收入。这个组合说明少量交货与下一季指引采用什么假设是两件事，不能缩写成“英伟达全部对华营收为零”，更不能说“中国AI需求归零”。[NVIDIA 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm)、[NVIDIA 8月26日展望](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027)

阅读后续消息时，按“正式规则—个别许可—目的地许可—交货验收—收入回款”逐层记录；任何一层未完成，就不能自动标记下一层完成。

| 情景（不赋概率） | 先核的触发证据 | 可能改善的方面 | 可能恶化的方面 |
|---|---|---|---|
| 部分供给限制缓解 | 正式规则或具体许可，随后有可验证交付 | 下游获得更多设备选择，部分建设成本或等待时间下降 | 国产供应商面临进口竞争、价格与订单压力 |
| 限制延续但有个案通道 | 审查政策稳定，个别许可与实际销售分化 | 已完成认证的替代方案可能获得持续订单 | 关键配套仍受限，客户项目可能延误 |
| 限制扩大 | 已生效的规则、清单或正式许可变化 | 部分替代研发和本地采购动机增强 | 上游断供、迁移成本、利用率和资本回收可能同时受损 |

上述政策情景不赋予概率，也不预设每种情景都能产生投资机会。政策带来的情绪交易与公司形成现金流是两件事；没有历史样本和估计程序，这张表只用于压力测试，不能包装成客观概率或直接交易信号。

### 5.9 我可能错在哪里

模型层的收敛可能被下一次架构或数据突破重新拉开，也可能比现有榜单显示得更快。如果只盯公开英语问答榜，既可能忽视某些领域的落后，也可能漏掉中文与企业专有场景的优势。

国产设备的工程改进也可能快于公开证据出现的速度。本篇对未公开配置不补猜，不意味着断言它没有发生；应把这类信息留在待核层，等待可复核的训练、推理或客户验收材料，而不是先写成确定突破再等待来源。

主权项目不完全服从商业资本回报，安全和公共服务目标可能支持较长的投资周期。因此，单用普通企业回收期判断所有项目都会停工，会低估政策投入的持续性；但政策持续投入同样不能证明每一家供应商估值合理。

最后，出口政策、劳动市场和能源数据的变化速度不同。规则可能当天变化，采购与就业统计需要更长时间出现。下一次更新应分别刷新这几条证据链，不以一个新日期给全部旧数据盖章，也不让一个刚发布的模型覆盖仍然未知的产业结果。

### 5.10 技术与国际主题来源索引

以下为正文保留的主题来源入口。除本轮明确注明抽核的GAO决定外，其余材料采用文中列明的发布与观察日，本轮未逐条重新抓取，也未独立复跑厂商测试；原始页面可能后续更新。

- OpenAI：[GPT-6 Astra](https://openai.com/index/gpt-6-astra/)、[9月3日安全说明](https://openai.com/index/safety-overview-gpt-6-astra/)。厂商能力与风险披露。

- Anthropic：[Fable/Mythos 5.1发布](https://www.anthropic.com/claude-fable-and-mythos-5-1)、[官方模型页及9月1日日期](https://www.anthropic.com/claude/fable)、[2026年3月使用研究](https://www.anthropic.com/research/economic-index-march-2026-report)。厂商评测与自选使用样本。

- Dario Amodei：[The Adolescence of Technology](https://darioamodei.com/essay/the-adolescence-of-technology)。作者公开预测与风险论证，不作经校准概率。

- Google DeepMind：[2026年认知评估框架](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf)、[Levels of AGI](https://arxiv.org/abs/2311.02462)、[From AGI to ASI](https://deepmind.google/research/publications/239142/)。原作者方法研究。

- METR：[时间跨度拟合与修订说明](https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/)。独立评估机构的方法与局限。

- Arena：[Bradley–Terry评分说明](https://arxiv.org/html/2403.04132v1)；Stanford：[2026 AI Index](https://hai.stanford.edu/ai-index/2026-ai-index-report)。分别用于量尺解释和年度趋势，非10月实时统一排行榜。

- DeepSeek：[透明中心](https://www.deepseek.com/en/transparency/)；华为云：[2026年4月24日适配公告](https://www.huaweicloud.com/news/2026/20260424172129152.html)。产品与适配证据，不外推未披露训练来源。

- 主权AI：[OpenAI Stargate](https://openai.com/index/stargate-community/)、[NVIDIA—HUMAIN](https://nvidianews.nvidia.com/news/saudi-arabia-and-nvidia-to-build-ai-factories-to-power-next-wave-of-intelligence-for-the-age-of-reasoning)、[欧盟行动计划](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A52025DC0165)、[欧委会设施安排](https://commission.europa.eu/topics/competitiveness/competitiveness-coordination-tool-projects/ai-gigafactories_en)、[印度PIB](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2229171&lang=1&reg=1)、[国家发展改革委政策解读](https://www.ndrc.gov.cn/xxgk/jd/jd/202508/t20250826_1400058.html)。公告、政策和各自限定的运行口径。

- 安全与就业：[美国国防部合同](https://www.defense.gov/News/Contracts/Contract/Article/4194643/)、[Stanford2026年8月就业修订](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/)、[IMF暴露度](https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity)、[IMF2026技能研究](https://www.imf.org/en/blogs/articles/2026/01/14/new-skills-and-ai-are-reshaping-the-future-of-work)。合同、描述性研究和宏观研究不可互相替代。

- 能源：[IEA2026版](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary)、[IEA2025版](https://www.iea.org/reports/energy-and-ai/executive-summary)、[美国能源部Crane贷款](https://www.energy.gov/articles/energy-department-closes-loan-restart-nuclear-power-plant-pennsylvania)。历史估计、预测与项目融资分别使用。

- 出口与监管：[BIS2025公告](https://www.bis.gov/press-release/department-commerce-rescinds-biden-era-artificial-intelligence-diffusion-rule-strengthens-chip-related)、[BIS2026逐案审查](https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china)、[NVIDIA10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm)、[NVIDIA8月26日展望](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027)、[欧委会7月31日实施说明](https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august)。正式公告与公司披露；不把媒体草案传闻视为现行规则。

<!-- REFERENCES_START -->

## 参考资料索引

本册按URL去重收录48项参考资料，保留正文中的就近链接，下面按首次引用顺序集中列出完整网址，便于打印后追溯。名称采用已核对的公司、报告期与文档类型或正文来源简称，并非一律为官方原标题；资料的期间、核验程度和访问限制以对应段落为准，不表示全部旧引文都在本轮重新取得原件。

1. [Anthropic 评测表及防护说明](https://www.anthropic.com/claude-fable-and-mythos-5-1) · www.anthropic.com

    <span class="ref-url">https://www.anthropic.com/claude-fable-and-mythos-5-1</span>

2. [Google部署与防护说明](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) · blog.google

    <span class="ref-url">https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/</span>

3. [OpenAI 评测表及脚注](https://openai.com/index/gpt-6-astra/) · openai.com

    <span class="ref-url">https://openai.com/index/gpt-6-astra/</span>

4. [The Adolescence of Technology](https://darioamodei.com/essay/the-adolescence-of-technology) · darioamodei.com

    <span class="ref-url">https://darioamodei.com/essay/the-adolescence-of-technology</span>

5. [DeepMind 认知框架](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) · storage.googleapis.com

    <span class="ref-url">https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf</span>

6. [时间跨度拟合与修订说明](https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/) · metr.org

    <span class="ref-url">https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/</span>

7. [DeepSeek 官方透明中心](https://www.deepseek.com/en/transparency/) · www.deepseek.com

    <span class="ref-url">https://www.deepseek.com/en/transparency/</span>

8. [OpenAI官方变更记录](https://developers.openai.com/api/docs/changelog) · developers.openai.com

    <span class="ref-url">https://developers.openai.com/api/docs/changelog</span>

9. [Anthropic发布说明](https://www.anthropic.com/claude-opus-5-5) · www.anthropic.com

    <span class="ref-url">https://www.anthropic.com/claude-opus-5-5</span>

10. [Levels of AGI](https://arxiv.org/abs/2311.02462) · arxiv.org

    <span class="ref-url">https://arxiv.org/abs/2311.02462</span>

11. [DeepMind 后AGI研究](https://deepmind.google/research/publications/239142/) · deepmind.google

    <span class="ref-url">https://deepmind.google/research/publications/239142/</span>

12. [OpenAI 安全说明](https://openai.com/index/safety-overview-gpt-6-astra/) · openai.com

    <span class="ref-url">https://openai.com/index/safety-overview-gpt-6-astra/</span>

13. [OpenAI训练与恢复说明](https://openai.com/index/path-to-astra/) · openai.com

    <span class="ref-url">https://openai.com/index/path-to-astra/</span>

14. [Bradley–Terry评分说明](https://arxiv.org/html/2403.04132v1) · arxiv.org

    <span class="ref-url">https://arxiv.org/html/2403.04132v1</span>

15. [Stanford 2026 AI Index](https://hai.stanford.edu/ai-index/2026-ai-index-report) · hai.stanford.edu

    <span class="ref-url">https://hai.stanford.edu/ai-index/2026-ai-index-report</span>

16. [2026年4月24日适配公告](https://www.huaweicloud.com/news/2026/20260424172129152.html) · www.huaweicloud.com

    <span class="ref-url">https://www.huaweicloud.com/news/2026/20260424172129152.html</span>

17. [OpenAI Stargate](https://openai.com/index/stargate-community/) · openai.com

    <span class="ref-url">https://openai.com/index/stargate-community/</span>

18. [NVIDIA—HUMAIN 公告](https://nvidianews.nvidia.com/news/saudi-arabia-and-nvidia-to-build-ai-factories-to-power-next-wave-of-intelligence-for-the-age-of-reasoning) · nvidianews.nvidia.com

    <span class="ref-url">https://nvidianews.nvidia.com/news/saudi-arabia-and-nvidia-to-build-ai-factories-to-power-next-wave-of-intelligence-for-the-age-of-reasoning</span>

19. [欧盟AI行动计划](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A52025DC0165) · eur-lex.europa.eu

    <span class="ref-url">https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A52025DC0165</span>

20. [欧委会AI Gigafactories](https://commission.europa.eu/topics/competitiveness/competitiveness-coordination-tool-projects/ai-gigafactories_en) · commission.europa.eu

    <span class="ref-url">https://commission.europa.eu/topics/competitiveness/competitiveness-coordination-tool-projects/ai-gigafactories_en</span>

21. [印度PIB公告](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2229171&lang=1&reg=1) · www.pib.gov.in

    <span class="ref-url">https://www.pib.gov.in/PressReleasePage.aspx?PRID=2229171&amp;lang=1&amp;reg=1</span>

22. [国家发展改革委政策解读](https://www.ndrc.gov.cn/xxgk/jd/jd/202508/t20250826_1400058.html) · www.ndrc.gov.cn

    <span class="ref-url">https://www.ndrc.gov.cn/xxgk/jd/jd/202508/t20250826_1400058.html</span>

23. [美国国防部合同公告](https://www.defense.gov/News/Contracts/Contract/Article/4194643/) · www.defense.gov

    <span class="ref-url">https://www.defense.gov/News/Contracts/Contract/Article/4194643/</span>

24. [Stanford2026年8月就业修订](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/) · digitaleconomy.stanford.edu

    <span class="ref-url">https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/</span>

25. [Anthropic 研究与样本说明](https://www.anthropic.com/research/economic-index-march-2026-report) · www.anthropic.com

    <span class="ref-url">https://www.anthropic.com/research/economic-index-march-2026-report</span>

26. [IMF 暴露度原文](https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity) · www.imf.org

    <span class="ref-url">https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity</span>

27. [IMF 2026技能研究](https://www.imf.org/en/blogs/articles/2026/01/14/new-skills-and-ai-are-reshaping-the-future-of-work) · www.imf.org

    <span class="ref-url">https://www.imf.org/en/blogs/articles/2026/01/14/new-skills-and-ai-are-reshaping-the-future-of-work</span>

28. [IEA 2026更新](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) · www.iea.org

    <span class="ref-url">https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary</span>

29. [IEA 2025版](https://www.iea.org/reports/energy-and-ai/executive-summary) · www.iea.org

    <span class="ref-url">https://www.iea.org/reports/energy-and-ai/executive-summary</span>

30. [美国能源部Crane贷款](https://www.energy.gov/articles/energy-department-closes-loan-restart-nuclear-power-plant-pennsylvania) · www.energy.gov

    <span class="ref-url">https://www.energy.gov/articles/energy-department-closes-loan-restart-nuclear-power-plant-pennsylvania</span>

31. [欧委会7月31日实施说明](https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august) · digital-strategy.ec.europa.eu

    <span class="ref-url">https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august</span>

32. [Sonnet 5.5发布](https://www.anthropic.com/claude-sonnet-5-5) · www.anthropic.com

    <span class="ref-url">https://www.anthropic.com/claude-sonnet-5-5</span>

33. [GPT-6.1 Sol发布](https://openai.com/index/introducing-gpt-6-1-sol/) · openai.com

    <span class="ref-url">https://openai.com/index/introducing-gpt-6-1-sol/</span>

34. [交易8-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000078/nvda-20260902.htm) · www.sec.gov

    <span class="ref-url">https://www.sec.gov/Archives/edgar/data/1045810/000104581026000078/nvda-20260902.htm</span>

35. [SEC披露日期](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000078/0001045810-26-000078-index.htm) · www.sec.gov

    <span class="ref-url">https://www.sec.gov/Archives/edgar/data/1045810/000104581026000078/0001045810-26-000078-index.htm</span>

36. [NVIDIA开放生态说明](https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/) · blogs.nvidia.com

    <span class="ref-url">https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/</span>

37. [NVIDIA测试说明](https://blogs.nvidia.com/blog/vera-rubin-nvl72-mlperf-inference/) · blogs.nvidia.com

    <span class="ref-url">https://blogs.nvidia.com/blog/vera-rubin-nvl72-mlperf-inference/</span>

38. [MLCommons方法与分析](https://mlcommons.org/2026/09/chairs-mlperf-inference-v6-1/) · mlcommons.org

    <span class="ref-url">https://mlcommons.org/2026/09/chairs-mlperf-inference-v6-1/</span>

39. [CoreWeave工程说明](https://www.coreweave.com/blog/cognition-becomes-first-customer-for-nvidia-vera-rubin-nvl72-on-coreweave-cloud) · www.coreweave.com

    <span class="ref-url">https://www.coreweave.com/blog/cognition-becomes-first-customer-for-nvidia-vera-rubin-nvl72-on-coreweave-cloud</span>

40. [NVIDIA生产部署说明](https://blogs.nvidia.com/blog/coreweave-agentic-ai-vera-rubin/) · blogs.nvidia.com

    <span class="ref-url">https://blogs.nvidia.com/blog/coreweave-agentic-ai-vera-rubin/</span>

41. [AMD技术说明及测试脚注](https://rocm.blogs.amd.com/software-tools-optimization/mi455x-vs-mi355x/README.html) · rocm.blogs.amd.com

    <span class="ref-url">https://rocm.blogs.amd.com/software-tools-optimization/mi455x-vs-mi355x/README.html</span>

42. [GAO B-337935](https://www.gao.gov/products/b-337935) · www.gao.gov

    <span class="ref-url">https://www.gao.gov/products/b-337935</span>

43. [BIS 2025年公告](https://www.bis.gov/press-release/department-commerce-rescinds-biden-era-artificial-intelligence-diffusion-rule-strengthens-chip-related) · www.bis.gov

    <span class="ref-url">https://www.bis.gov/press-release/department-commerce-rescinds-biden-era-artificial-intelligence-diffusion-rule-strengthens-chip-related</span>

44. [BIS 2026年1月13日公告](https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china) · www.bis.gov

    <span class="ref-url">https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china</span>

45. [BIS 5月31日正式指引](https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf) · www.bis.gov

    <span class="ref-url">https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf</span>

46. [NVIDIA 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm) · www.sec.gov

    <span class="ref-url">https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm</span>

47. [NVIDIA 8月26日展望](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027) · nvidianews.nvidia.com

    <span class="ref-url">https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027</span>

48. [官方模型页及9月1日日期](https://www.anthropic.com/claude/fable) · www.anthropic.com

    <span class="ref-url">https://www.anthropic.com/claude/fable</span>
