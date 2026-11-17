# Google TPU竞争与资本回收研究材料

研究截至2026年11月17日（北京时间）；核验时间15:52起。应用financial-data与investment-memo-craft的证据与写作规范。本材料不重新核定作者风险窗口，不使用11月18日及以后才发布的业绩。旧版已提到TPU系统产品销售，本次补足其竞争、交付、利润归属与融资含义，不能把本次展开写成对旧版“只有云租赁”的纠错。

## 可并入正文的分析

**TPU改变的不只是英伟达的芯片份额，还可能改变谁承担算力资产、谁取得节约额，以及资本何时收回。** Google既是自用算力大户，也是云商、模型商和系统卖方。因此“TPU成功”等于四种不同结果：内部Gemini和搜索等服务成本下降、Cloud出售算力、向客户交付整系统、模型与应用收费增加。这些结果可能同时发生，却不能把内部节约记成外部芯片收入，也不能把Google Cloud全部利润归给TPU。[产品范围](https://cloud.google.com/tpu)、[Alphabet Q3电话会](https://abc.xyz/investor/events/event-details/2026/2026-Q3-Earnings-Call-2026-Ujou16CTw9/)

首先必须分清产品已发布与可以普遍采购。Ironwood TPU7x已于2026年3月31日GA；11月17日读取的官方产品页仍把8t、8i及11月9日新增的8tx、8i Max列为Coming soon。因此不能把营销演示、特定客户导入和普遍可用混成规模供给。8t面向大规模训练，8i面向推理及后训练；8tx是使用8t硅片、配AMD EPYC主机的保密计算系统，8i Max则组合两颗8i。新系统并非四次全新芯片迭代，EPYC配套也不是AMD Instinct取得同等加速器订单。[发布记录](https://docs.cloud.google.com/tpu/docs/release-notes)、[系统公告](https://cloud.google.com/blog/topics/ai-infrastructure/tpu-8tx-and-tpu-8i-max)

软件壁垒正在变薄，但迁移仍有账单。10月20日开放的TorchTPU把原生PyTorch执行引入TPU，与JAX路线并存；PyTorch官方同时说明，旧PyTorch/XLA存在侵入式修改、编译延迟等问题，新路线仍受动态形状、编译和定制内核约束。判断替代性应比较相同模型质量、输入输出长度、并发、延迟SLA下，每个验收任务的全成本，纳入迁移人力、失败重跑、主机与网络、空闲容量及合同期限。训练关注收敛与有效训练时间，推理关注质量、尾延迟和真实付费量；峰值算力或厂商某项性能宣传不能跨任务排名。[Google开源公告](https://cloud.google.com/blog/topics/ai-infrastructure/torchtpu-is-now-open-source-run-native-pytorch-on-tpus)、[PyTorch技术说明](https://pytorch.org/blog/introducing-torchtpu/)

多平台已经是实际经营选择。Apple确认在Cloud TPU扩大预训练，部分模型又为NVIDIA GPU部署优化；Google仍推进NVIDIA基础设施，A5X在11月6日更新为GA。TPU争取的可能是新增负载、客户议价权或部分GPU预算，并非所有任务一比一迁移。客户可用多种硬件也不等于随时无成本搬家：模型内核、调度、数据位置、运维人才和最低采购承诺仍会形成锁定。[Apple研究](https://machinelearning.apple.com/research/introducing-third-generation-of-apple-foundation-models)、[Google与NVIDIA](https://cloud.google.com/blog/topics/ai-infrastructure/google-cloud-infrastructure-at-nvidia-gtc-berlin-2026)

商业模式也在分叉。云租赁按消耗或订阅收费；整系统销售包含硬件、软件和服务，已从2026年Q2开始确认收入；客户自有机房或专用设施只是部署地点，可能采用购买、租赁或第三方服务，不能自动等于裸片外售。Oracle宣布的TPU服务要到2027年才开始供应。整系统路线可减少Google自己建设机房的需要，却先产生库存占款，客户也会承担融资与利用率风险。Alphabet还披露部分已售TPU附带回购担保，9月末最大潜在付款66亿美元：外售并未把残值风险完全转走；它不是已发生损失，公司也认为按折价条款对手缺乏经济行权动机。[Alphabet 10-Q](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000084/goog-20260930.htm)、[Oracle公告](https://www.oracle.com/news/announcement/ai-world-oracle-brings-google-tpus-to-oracle-cloud-infrastructure-2026-10-27/)

融资循环需要两边一起看。Anthropic的11月10日修订招股书把Google CSP最低承诺更新为约1213亿美元，覆盖2026年4月至2033年7月；这替换旧版1145亿美元口径，不能把两者相加。另列2028—2031年额外TPU付款估计1250亿—1500亿美元，交付方式和融资未固定，且不在合同义务表内。Google又签约拟在IPO同步认购100亿美元，该安排占用截至9月底尚可用的200亿美元融资框架，不能再全部累加，更不能提前算到账。Broadcom披露约3.5GW扩展自2027年开始，仍以Anthropic持续商业成功为条件。芯片竞争因此可能分散供应商，却未必分散最终付款人的预算风险。[修订S-1](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm)、[Google认购协议](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/exhibit1015-sx1ax2.htm)、[Broadcom 8-K](https://www.sec.gov/Archives/edgar/data/1730168/000119312526144028/d87999d8k.htm)

成本节约归属没有预定答案。Google内部负载降本，首先改善相关服务经济性；对外Cloud若维持价格，云商可能留利，若竞争传导降价，模型客户与应用客户受益；模型商若又下调API价，毛利未必上升。Broadcom可通过定制芯片、网络及交付取得收入，代工与封装也可能分走稀缺环节收益；没有TPU产品级毛利披露，就不能倒算Google、Broadcom或TSMC各获多少。广告现金提供等待能力，但还须验证新AI资产自己的回款，不能以传统现金补贴证明回本。

支持作者风险判断的路径是：TPU等替代供给降低同质量任务价格，新GPU与旧GPU同时面临更便宜的选择；老资产租价和残值下降快于债务摊还，外售、关联方采购和融资把压力分散到更多主体，而非消除压力。强反方是：更便宜的有效任务扩大新用途，多平台减少短缺与单一供货风险，旧GPU转向合适负载，投资逐步放缓且现金持续改善。于是TPU成功既可能加快旧资本重定价，也可能帮助行业消化建设，不能预设为泡沫必破的证据。

最终判断要跟踪同批资产的收费和付款：若降本后新增付费任务与利用率足够补偿单价下降，竞争帮助回收；若供给、最低采购与担保继续增长，而圈外客户现金追不上，竞争会让“延迟即放大”的条件更扎实。硬件份额转移也不等于行业总CapEx下降：服务转系统销售可降低某家平台自建支出，同时在客户、合资云或融资租赁端增加相应投入。需要逐笔去重，而不是只看一家公司的CapEx线。

## 事实、状态、日期与限制

| ID | 已核事实与状态 | 日期/期间 | 原始URL | 限制 |
|---|---|---|---|---|
| T01 | Ironwood TPU7x已GA；此前为预览 | 2026-03-31 GA；2025-11-24 Preview | [Cloud发布记录](https://docs.cloud.google.com/tpu/docs/release-notes) | GA不等于任何地区无限供给，也不说明客户实际租量 |
| T02 | 8t、8i、8tx、8i Max官方均列Coming soon | 2026-11-17读取 | [产品页](https://cloud.google.com/tpu) | 是当日网页快照；不能排除部分客户导入，但无依据写全面GA |
| T03 | 8tx/8i Max为新系统配置；8tx配第五代EPYC，非Instinct | 2026-11-09发布 | [Google公告](https://cloud.google.com/blog/topics/ai-infrastructure/tpu-8tx-and-tpu-8i-max) | 性能数字属厂商宣传；本稿不作跨平台排名 |
| T04 | 云TPU有按chip-hour报价与承诺价；READY状态计费 | 2026-11-17读取 | [定价](https://cloud.google.com/tpu/pricing) | 标价不等于大客户实际价格；空闲/等候对有效单位成本仍有影响 |
| T05 | TPU系统外售已有收入，Q2起确认；少数合同显著多数收入预计2027 | 2026Q3 10-Q | [Alphabet SEC](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000084/goog-20260930.htm) | 不能推成普遍裸片零售；硬件转移控制、服务期间确认不同 |
| T06 | 公司明确不披露TPU产品级财务或利润率 | 2026-10-28电话会 | [Alphabet IR](https://abc.xyz/investor/events/event-details/2026/2026-Q3-Earnings-Call-2026-Ujou16CTw9/) | Cloud收入及营业利润不能当TPU收入利润；“未单列”不等于“没有收入” |
| T07 | TPU部分回购担保最大潜在付款$6.6B，须按约返还可用设备 | 截至2026-09-30 | [10-Q Note 10](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000084/goog-20260930.htm) | 单一发行人金额；公允价值不重大，公司判断行权动机不足；不是已损失$6.6B |
| T08 | Oracle将提供TPU，由OCI提供电力、冷却和数据中心网络 | 10/27公告，2027开始且多年爬坡 | [Oracle](https://www.oracle.com/news/announcement/ai-world-oracle-brings-google-tpus-to-oracle-cloud-infrastructure-2026-10-27/) | 合作已宣布，容量收费与回款尚不能当实绩；Google同步公告属同一联合发布 |
| T09 | Apple证实Cloud TPU用于扩大预训练，部分模型面向NVIDIA部署优化 | 2026年第三代模型研究页，11/17读取 | [Apple原件](https://machinelearning.apple.com/research/introducing-third-generation-of-apple-foundation-models) | 客户侧互证真实用途，未给TPU采购额、利用率或系统外售量 |
| T10 | TorchTPU已开源；PyTorch说明原生执行及仍存限制 | 2026-10-20 Google公告 | [Google](https://cloud.google.com/blog/topics/ai-infrastructure/torchtpu-is-now-open-source-run-native-pytorch-on-tpus)、[PyTorch](https://pytorch.org/blog/introducing-torchtpu/) | 两方技术互证不是独立性能评测；支持框架不代表所有CUDA内核无改动可移植 |
| T11 | Google NVIDIA A5X更新为GA | 2026-11-06更新 | [Google NVIDIA合作](https://cloud.google.com/blog/topics/ai-infrastructure/google-cloud-infrastructure-at-nvidia-gtc-berlin-2026) | 可用性不等于采购量；证明业务共存，不证明NVIDIA份额不受影响 |
| T12 | Broadcom/Google/Anthropic扩展约3.5GW，自2027开始 | 2026-04-06协议披露 | [Broadcom SEC](https://www.sec.gov/Archives/edgar/data/1730168/000119312526144028/d87999d8k.htm)、[Google合作](https://www.googlecloudpresscorner.com/2026-04-06-Anthropic-Expands-Use-of-Google-Cloud-and-TPUs) | 3.5GW是Broadcom单方量化；与多个GW总体安排嵌套，不重复加总；商业成功条件仍在 |
| T13 | Anthropic Google CSP最低约$121.3B，欠用有补差及例外；额外TPU$125–150B为估计 | CSP 2026-04至2033-07；额外计算2028–31；11/10文件 | [S-1/A2](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm) | 同主体披露，未获独立交易对手逐项金额互证。替换$114.5B旧值；额外估计不在合同义务表，不视作已付款 |
| T14 | Google NPA三月额度$30B；五月Series H投入$10B后，9/30可用$20B且NPA未发行；拟IPO认购再占$10B，剩余变$10B | 11/10协议、11/11 EEA文件；9/30余额 | [认购协议](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/exhibit1015-sx1ax2.htm)、[EEA招股书](https://www.sec.gov/Archives/edgar/data/2130357/000162828026073040/anthropicpbc-fwpxeeaprospea.htm) | 不是独立第二账簿；IPO尚未交割，不能把$10B提前当到账；受持股上限和交割条款影响 |
| T15 | Anthropic与Broadcom及转让后融资主体的设备租赁合计约$161.2B不含利息；其中2026 Lease Arrangement约$125.2B；配套最高$42B融资框架，9/30未提用 | 11/10 S-1；部分容量2026已开始上线，其余预计2027起 | [S-1/A2](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm) | 一手单方披露。租金通常ready-for-service开始，但机房延误等情况下可能更早起付；$42B只资助2026安排部分季度租金且附条件，不加成采购，不视作全部已运行；转让本身未增加租金总额 |
| T16 | Crux合资云：Blackstone承诺最高$5B；首500MW计划2027 | 2026-05-18发布 | [Blackstone](https://www.blackstone.com/news/press-releases/blackstone-announces-joint-venture-with-google-to-create-new-tpu-cloud/) | 承诺不等于已出资；发电/机房/租量均需投运验证 |
| T17 | Crux为Alphabet关联方权益法合资企业；backlog含$16.8B，Alphabet有条件未来设施/能源backstop最高$10B | 2026-09-30 | [10-Q Notes 2、3](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000084/goog-20260930.htm) | 单方披露；backlog不是现金，backstop不是现金投入，也不能与$6.6B回购当确定损失合计 |
| T18 | Broadcom长期供应Google定制TPU及网络部件至最晚2031；其大部分外包晶圆来自TSMC | 4/6协议；FY26前三季 | [Broadcom 8-K](https://www.sec.gov/Archives/edgar/data/1730168/000119312526144028/d87999d8k.htm)、[Broadcom 10-Q](https://investors.broadcom.com/static-files/96641754-401f-4090-a4ab-210728c83a28) | 未取得TPU专项代工收入或利润分成；总公司晶圆比例不能推成所有TPU型号供应份额 |

## 正方、强反方与可观测检验

| 推论 | 支持风险累积的观察 | 足以削弱该推论的强反证 |
|---|---|---|
| 更低同质量任务成本可能压低旧GPU回收 | 同型号旧设备续约净租价与处置价下降、融资期限不变、毛利扣运维后收缩 | 利用率和付费任务增加抵消降价，迁移/路由让旧卡继续贡献足额现金 |
| TPU渠道扩大增加行业总供给 | Oracle/Crux/客户机房实际投运，新增机架和最低采购义务快于终端净回款 | 增量填补短缺、取消不经济扩建，新增需求由客户经营预算持续支付 |
| 外售可减Google自建投入，却转移而未消灭风险 | 库存及应收增加、回购或担保范围扩大、融资支持占客户采购提高 | 交付后收款良好、库存转快、担保自然到期无损失，客户独立现金覆盖采购 |
| 框架开放削弱迁移壁垒 | 同质量/SLA实测任务能低成本迁移，生产负载持续续约 | 自定义CUDA依赖、编译/运维成本、数据迁移及最低承诺吃掉节约 |
| 广告现金是缓冲 | 传统现金可支付建设/融资并维持流动性 | 仅证明偿付能力；只有AI投资批次客户净现金超过完整投入，才能证明该批回本 |

整系统检验口径：单位已验收任务成本＝（设备或租赁的本期经济成本＋电力冷却＋CPU/内存/网络/存储＋工程迁移与运维＋失败重跑）÷符合质量及SLA的任务数；与逐期现金支付/回款另表衔接，避免把折旧与购建设备现金重复扣除。

## 不该下的结论

- “第八代已全面GA”“Oracle已大规模贡献收入”“3.5GW已经部署”，均超出截至日证据。
- “TPU只能在Google云租赁”已不符合当前模式；但“Google公开零售裸片给所有人”亦未获证据。
- “Google自用节约＝外售收入”“Cloud利润＝TPU利润”“厂商性能提升＝客户同质量TCO同幅下降”，均混淆口径。
- “TPU成功所以NVIDIA订单或总CapEx必降”“多芯片所以融资风险已分散”，均忽略新增需求和共同付款人。
- 不将IPO拟认购、融资可用额、未来采购、担保、backlog与已收到现金相加；不把相关方交易本身称为收入造假。
- 无可核产品利润拆分，不写TPU利润率、NVIDIA份额损失幅度、确定泡沫破裂日期或未经校准概率。

## 资料纪律与待补缺口

关键金融金额均已回到SEC/公司原件，但除Blackstone与Alphabet对合资框架的交叉披露外，仍缺独立交易对手对多项金额的逐项验证；已在表中标单方，不把同份财报镜像、EEA转录、公司电话会和SEC财报当两套独立账簿。未采纳第三方镜像“GA”字样，产品状态以官方页及发布日志为准。没有发现独立TPU收入与利润拆分；没有取得8代全面GA通知、分型号外售量/现金回款、客户同质量跨平台TCO或TPU对应TSMC利润。本材料因此不量化市场份额和投资回报，观测期限继续沿用主报告。主要TPU合作与软件发布早于11月11日治理事件，不能当作黄仁勋离任已经导致转单的证据。
