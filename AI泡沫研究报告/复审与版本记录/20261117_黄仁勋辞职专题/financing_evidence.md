# NVIDIA 融资链证据记录

研究时点：2026-11-17 14:20，北京时间。金额除另注外为美元；B 为十亿美元，1B＝10 亿美元。本文只登记融资角色、现金与合同传导，不构成买卖建议，也不替换既有报告。

基线已读：V1.9《02_循环投资网络》2.2—2.5、《01_利润真实性拆解》1.1—1.2；V1.9.2 `author_view_zh.md`。采用 financial-data 的原件优先、期间与状态分离原则，以及 investment-memo-craft 的事实—机制—反证写法。多数财务数可在发行人公告与 SEC 备案间对账，但两者同属发行人披露，**不冒充两项独立经济验证**。

## 一、可交付的判断

**事实与边界：** NVIDIA 已经是设备供应商之外的股权出资方、算力承购方、建设信用支持方和外部资本协调者。黄仁勋离任增加新增交易的协调与风险偏好不确定性；目前核到的官方离任公告没有宣布取消融资平台、撤销既有担保或改变客户承诺。公开合同所列解除条件也不能被替换成“CEO 离任”。

**研究推论：** 最直接的风险路径是新增资金谈判放慢、条件变严或支持规模下降，继而让依赖融资扩建的客户减少设备采购；不是“英伟达利润立即消失”，也不是“1050 亿担保立即到期”。这条路径尚需成交、提款、回款或合同修订来验证。

**本轮实质不确定性：** OpenAI 的 300 亿美元轮融资参与额有官方公告；本轮未取得能逐笔核定 NVIDIA 截至 11/17 累计付款和剩余义务的发行人原件。媒体称最后一笔已付不能替代公司逐笔确认。没有原件，不应写成全数未付；也不能直接升级为已全到账。

## 二、五项交易分账

| 项目、日期 | 已核金额与期间 | 截至本轮核验的状态 | 能说明什么／不能说明什么 |
|---|---|---|---|
| NVIDIA→CoreWeave 股权，2026/1/23交割，1/26官宣 | 2B（20 亿美元）现金，22,935,780 股，每股 87.20 美元 | **已交割现金**；Q3 10-Q 仍记为当年已完成股权发行 | 是风险资本支持；不是贷款、也不是每年重复注资。来源：[成交8-K](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000044/crwv-20260123.htm)、[NVIDIA公告](https://nvidianews.nvidia.com/news/nvidia-and-coreweave-strengthen-collaboration-to-accelerate-buildout-of-ai-factories)。 |
| NVIDIA↔CoreWeave 剩余未售云容量，2025/9/9签约、9/15披露 | 订单**初始价值**6.3B（63 亿美元）；承购安排至2032/4/13 | **附服务交付与可用性条件的合同义务**，不是已支付63亿或授信提款。最新Q3 10-Q未找到该订单的明确修订、终止或累计支付专项披露 | 为CoreWeave未售容量提供需求支持；不等于为其全部设备残值或全部债务兜底。金额是初始订单价值，不能当作今日剩余未付余额。来源：[8-K Item 1.01](https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm)。 |
| NVIDIA→SB Energy/OpenAI建设信用支持，2026/8/17签约 | 累计义务上限105B（1050 亿美元），覆盖约4.25GW；九阶段，首批预计FY2029起生效，各相关租期20年 | **条件性未来义务**。须满足机房服务就绪、起租及约定违约触发；本轮未核到因离任而修订或触发。额外约3.8GW是NVIDIA可自行决定行使的选项 | 保障明确部分租金／电力付款，非整个园区全部成本。旧报告“105”以B计，不能读成105亿美元。来源：[8-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000069/nvda-20260817.htm)、[Q2 10-Q Note 10](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm)。 |
| NVIDIA与六家资本机构的独立融资平台，2026/8/10宣布 | 拟长期动员逾500B（5000 亿美元）第三方资本 | **谅解备忘录与目标**；不是已募集、已提款或NVIDIA自有资金承诺500B。未取得足以把整体目标升级为已落实资金的原件 | 体现NVIDIA协调外部资本的角色；目标不能纳入“已投入生态现金”。[NVIDIA公告](https://nvidianews.nvidia.com/news/nvidia-partners-with-apollo-blackrock-blackstone-brookfield-goldman-sachs-and-kkr-to-establish-ai-compute-infrastructure-financing-platforms-to-mobilize-over-500-billion-of-third-party-capital)、[Apollo同日公告](https://www.apollo.com/insights-news/pressreleases/2026/08/nvidia-partners-with-apollo)。 |
| NVIDIA→OpenAI股权意向／轮融资 | 2025/9/22曾表示随10GW部署逐步投资至多100B；2026/2/27官方轮融资公告列NVIDIA 30B | **历史意向与后续融资参与额分开**；本轮不宣称30B全部未付或全部已付。没有证据支持把旧100B与新30B相加 | NVIDIA有参与模型公司融资的直接角色；不能据此确认130B可用授信或追踪同一笔现金全部回购其GPU。[2025年NVIDIA说明](https://blogs.nvidia.com/blog/openai-nvidia/)、[2026年OpenAI轮融资公告](https://openai.com/index/scaling-ai-for-everyone/)。 |

五行的法律性质、统计日与期限不同，可能服务同一底层建设，**不计算“循环融资总额”**。股权投入、云采购、担保和第三方平台目标也不等于同期收入、净新增融资或损失。

## 三、公司现金缓冲与下游缺口

NVIDIA目前可用的已公布基线仍为FY27Q2（截至7/26），不是尚未发布的FY27Q3。公司定义的季度FCF为21.341B，即24.077B经营现金减2.677B固定资产及无形资产现金购置、再减0.059B相关本金。期末现金、现金等价物与可交易债务证券合计约56.6B。它证明NVIDIA自身产生现金且有缓冲，不证明客户的新AI项目已经回本。[CFO说明及FCF调节表](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27cfocommentary.htm)

下游以CoreWeave为例：2026年1—9月经营现金5.638B，现金购置固定资产（包含资本化内部使用软件）23.558B，简单现金桥为**−17.920B**。Q3单季对应1.975−9.441＝**−7.466B**。这不是说其经营现金为负，也不是拿全年管理层CapEx指引抵减单季现金。公告与10-Q现金流表这两项一致；这是截至9/30的经营结构，早于离任。[11/10业绩公告现金流表](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Third-Quarter-2026-Results/default.aspx)、[11/12备案10-Q现金流表](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000465/crwv-20260930.htm)

CoreWeave同期净融资现金21.346B帮助衔接投入与回款；融资能改善支付能力，但不能被当成经营回本。11/10公司预计未来三个月获得约9B客户预付款及押金，属于预测而非截至9/30已收。新Q3收入3.661B、同比增长168%，也反驳“终端需求已因离任立即断崖”的写法；收入、经营现金、建设现金与借款必须分别看。[11/10公告](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Third-Quarter-2026-Results/default.aspx)

补充状态核验：CoreWeave DDTL 5.5额度为2.6B，9/30债务表余额1.555B，不能写成全部额度均已提款或仍全部未使用；不能仅凭两数相减断定随时可用额度，因为提款还受合同条件约束。其集团有担保责任，贷款以融资子公司资产等担保；这不是NVIDIA为该笔借款提供无条件全额担保。只用于说明抵押和授信状态，不纳入五项交易合计。[Q3 10-Q Note 10](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000465/crwv-20260930.htm)

## 四、离任能否解除既有义务

CoreWeave的公开MSA第10节列出重大违约未补救及破产等因由；2025/9/15的8-K补充了30天通知及破产程序90天未撤销等描述。所阅公开正文未发现以黄仁勋姓名或其离任为自动解除条件。**由于附件含商业条款删节且不能穿透未公开订单，不将“未发现”升级为“所有合同绝无关键人条款”。**[公开MSA第10节](https://www.sec.gov/Archives/edgar/data/1769628/000114036125036118/ny20053122x6_ex10-31.htm)

SB Energy担保的8-K列示：触发是OpenAI相关不履约／破产，而NVIDIA可选择接租、寻找替代租户、出售等处理；终止条件包括租期结束、约定租约终止、OpenAI达到满意信用评级等。担保包含向OpenAI追偿安排，但违约客户的补偿承诺不是现金回收保证。[担保8-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000069/nvda-20260817.htm)

11/12官方公告表达客户承诺、运营和产品路线继续执行，没有披露新融资风险限额；不能从Kress的CFO背景推定公司已经收紧。[官方过渡公告](https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition)

补充而非定论：11/16 Reuters分析引述知情者称六方仍在谈交易，其中一人说NVIDIA未表示暂停；Brookfield负责人表示继续合作。可能暂停或未来风险偏好降低是分析与预期。报道并称平台尚未公告交易。本记录不把报道中的市场人士总额估算写回官方风险账本，也不把它作为停融已发生的证明。[Reuters全文转载](https://www.streetinsider.com/Reuters/Analysis-Nvidias%2BAI%2Bfinancing%2Bmachine%2Bmay%2Bsurvive%2BHuang,%2Bbut%2Bwith%2Bless%2Brisk%2Bappetite/27347181.html)

## 五、两条相反但均有条件的路径

| 路径（研究推论，不是已发生事实） | 近端作用 | 较远端作用 | 可证伪的观察点 |
|---|---|---|---|
| 停止或减少新增支持；按约继续履行旧承诺 | 依赖新增出资、授信或承购的项目可能延迟；借款条件、采购及供给端回款承压 | 新设备、租赁与担保义务累积减慢，可能降低未来放大幅度；不等于风险自动消失 | 正式政策、项目签约至提款时间、取消订单、融资利差、付款逾期；如第三方资金迅速替代则近端冲击弱于预期 |
| 继续支持建设与客户融资 | 缓冲短期资金缺口，推动交付，使客户有时间增长外部付费 | 若净回款追上投入，可消化风险；若继续落后且新硬义务更快增加，回收期与累计承担额共同扩大 | 新投入实际支付、后续支持承诺、投运与租赁开始日、外部客户净回款、利用率及续租价格 |

“延迟即放大”精确表述为：**对同一投资批次和主体，如果经营净回款仍不能按计划覆盖投入回收及尚未重复计入的到期硬付款，而新增设备、租赁和融资义务继续累积，延后出清会放大累计暴露。** 若扩张收敛、回款增长或低回报项目退出，时间可能帮助消化；该判断不能无条件化，也不能从一个供应商高利润直接推出整个生态已回本或未回本。

## 六、GPU、信用与利润的四条线

1. **NVIDIA股票价格**是资本市场对权益的定价。股价下跌可影响募资和信心，但不会机械地以同一比例降低客户GPU抵押估值，也不会自动改变已售GPU的会计折旧。
2. **GPU租价、利用率和二手处置价**决定特定设备未来可赚现金及违约回收。若下降，可能压低贷款价值、增加再融资难度；是否追加抵押、提前还款，要逐份契约核，不能把股票跌幅当保证金通知。
3. **折旧与减值**进入持有设备主体的利润。投产规模扩大，折旧费用可以在收入仍增长时压低利润；经济寿命或残值恶化可能要求调整估计或减值，但新GPU问世不等于旧GPU立即归零。减值是风险被会计确认，不是认定所有设备均已无法运营。
4. **现金付款**在采购、租赁、本息及运营中按各自时点发生。折旧不是第二次购买GPU；FCF已经扣现金购建，不应再完整扣一次折旧。贷款契约可能使信用恶化转成现金压力，但会计费用与契约现金流不能混成一笔。

以上是机制推演。CoreWeave的融资文件支持“设备／合同与债务有联系”，不支持“辞职已经导致GPU抵押品崩盘”。监管、利率和建设许可等并行冲击也应分列，不能全部归因于CEO变更。

## 七、短摘与定位

以下每份来源仅保留短摘，正式结论以上述中文转述及原件为准。

| 原件 | 短摘 | 定位与用途 |
|---|---|---|
| [CoreWeave 2026/1/23交易8-K](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000044/crwv-20260123.htm) | “completed the issuance and sale” | Item 1.01；验证已交割，而非意向 |
| [CoreWeave 2025/9/15 8-K](https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm) | “initial value of $6.3 billion”；“subject to … satisfaction of delivery and availability of service requirements” | Item 1.01；初始订单额及履约条件，合计短摘不超过25英文词 |
| [NVIDIA担保8-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000069/nvda-20260817.htm) | “cumulatively capped at $105 billion” | Residual Value Guaranties；上限而非当期现金 |
| [NVIDIA Q2 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm) | “the first of which is expected in fiscal year 2029” | Note 10；分期生效 |
| [NVIDIA平台公告](https://nvidianews.nvidia.com/news/nvidia-partners-with-apollo-blackrock-blackstone-brookfield-goldman-sachs-and-kkr-to-establish-ai-compute-infrastructure-financing-platforms-to-mobilize-over-500-billion-of-third-party-capital) | “Memorandums of understanding”；“over time” | 2026/8/10开头；MOU与长期动员目标 |
| [OpenAI融资公告](https://openai.com/index/scaling-ai-for-everyone/) | “$30B from NVIDIA” | 2026/2/27开头；参与额，无逐笔支付表 |
| [CoreWeave Q3 10-Q](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000465/crwv-20260930.htm) | “Purchases of property and equipment, including capitalized internal-use software” | 现金流表；明确现金购建口径 |
| [CoreWeave MSA](https://www.sec.gov/Archives/edgar/data/1769628/000114036125036118/ny20053122x6_ex10-31.htm) | “TERM AND TERMINATION” | 第10节；解除条件；公开件存在删节 |
| [NVIDIA过渡公告](https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition) | “customer commitments and product roadmap to continue without interruption” | 11/12董事长表述；是公司预期，不是未来履约担保 |

## 八、待验证与禁止超前使用

- **OpenAI出资：** [The Information 10月报道](https://www.theinformation.com/briefings/exclusive-nvidia-softbank-make-final-20-billion-investment-openais-last-round/)称最后一笔10B已支付，但本轮没有发行人逐笔表；只登记为二级线索，不以SoftBank自己的到账公告替NVIDIA作证。
- **63亿承购：** 已查CoreWeave Q3 10-Q及本轮相关官方披露，未取得该订单剩余义务、已支付额和修订的专项表；“未取得”不等于没有履行，也不等于宣布金额不变。
- **平台：** 尚不能将500B目标转成可用承诺或提款；需要最终协议、第三方基金募集、借款人及实际交割证据。
- **关键人：** 已查公开MSA及担保概要，没有充分材料穿透所有删节／未公开订单，保留条款不确定性。
- **NVIDIA财报：** 官方仍定11/17美西13:20披露FY27Q3，即上海11/18约05:20；电话会约06:00。本研究时点未到，不引用尚未发布的业绩或指导。
- **CoreWeave发布时间：** [SEC索引](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000465/0001769628-26-000465-index.htm)记录Filing Date为2026-11-12、Accepted为07:20:41；报告期9/30。11/10公司已发布业绩公告。财期、公告日与事件日分开。

核验结论：交易性质和主要金额可由原件复查；OpenAI逐笔支付、容量订单执行额、平台成交和全部关键人条款仍有缺口。不附未经校准的概率，也不凭融资关系图推定收入造假或崩盘日期。

## 九、14:21窄范围交叉复审

对象：`专题更新_20261117/黄仁勋辞职_AI融资与泡沫判断_20261117.md`。仅复核交易四行、现金金额与期间、GPU／信用传导；不扩展检索，不复核政治与完整情景，不直接修改正文。

结论：四项交易的主要金额、已交割／条件性承诺／目标状态正确；NVIDIA FY27Q2 FCF 213.41亿美元正确；CoreWeave前九个月56.38−235.58＝−179.20亿美元，以及Q3收入36.61、GAAP经营利润2.07亿美元正确，且没有误归因于11月离任。GPU股价、二手成交价、会计值、抵押值及折旧现金分离符合原件所能支持的机制范围，未发现需要撤回的实质结论。

建议两处精确化：第26行“安排延至2032年4月”改为“合同安排持续至2032年4月13日”，避免把原合同期限写成新近展期；第40行“覆盖建设、计划回收”有把同笔投入与收回投入并列为两笔支出的歧义，建议改成“同一投资批次能否依靠经营净回款按计划收回投入，并在逐期现金桥中覆盖尚未重复计入的到期付款”。

可选补强：63亿美元后加“不是截至今日剩余未付款余额”；合同解除段补“公开MSA存在删节，未穿透所有订单”，并链接本记录所列MSA；CoreWeave“经营现金流入”改为“经营活动现金净流入”。这三项为精确性补强，不改变草稿结论。
