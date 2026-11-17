# TPU研究交叉复核

复核日：2026-11-17北京时间。复核对象：tpu_research.md、tpu_claims.json。复核人：alternative_platforms_research。范围仅本次TPU竞争与融资专题，不声称重新审核旧报告全部财务数据。

## 核验结论

主要竞争结论、可用性与关键金额均得到所列原始材料支持。发现两处需要作者修正的口径：Google融资20B应明确为9月末剩余额度；Broadcom租赁的受让融资实体不能未经证明写为其关联方。均已于本日发送给研究作者及中文整合作者，作者修订后已实际回读确认；处理记录见文末。

| 核验项目 | 复核证据与裁决 |
|---|---|
| 产品GA／Coming soon | [官方产品页](https://cloud.google.com/tpu)11/17读取仍将8t、8i、8tx、8i Max列Coming soon；[官方发布日志](https://docs.cloud.google.com/tpu/docs/release-notes)明确Ironwood TPU7x于3/31 GA。不能写所有8代已全面GA，但这也不能排除特定客户导入。通过。 |
| 新芯片与新系统配置 | [11/9公告](https://cloud.google.com/blog/topics/ai-infrastructure/tpu-8tx-and-tpu-8i-max)确认8tx采用8t硅片与第五代EPYC主机；这不是AMD Instinct订单。通过。 |
| 系统销售与Cloud总收入 | [Alphabet Q3 10-Q](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000084/goog-20260930.htm)Revenue Recognition及MD&A明确TPU系统包含硬件、软件、安装、支持、延保；Q2已确认、相关少数协议显著多数收入预计2027。不能把Cloud全额收入或利润归于TPU。通过。 |
| TPU回购担保 | 同一10-Q Note10金额6.6B，特定条件及设备保持工作状态；公允价值不重大，行权激励不足属公司判断。不是已损失。通过。 |
| Google CSP最低承诺 | [Anthropic 11/10 S-1/A2](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm)p180明确121.3B、2026年4月至2033年7月，有true-up及限定例外。旧114.5B不能相加，不能把差额全解释为纯新订单。通过。 |
| 额外TPU125–150B | 同件p180明确额外TPU估计125–150B，2028–31交付，路径可能为云、直购或第三方采购租赁，未进合同义务表。p178全公司其他无固定金额安排为150–175B，属于更广口径，不能据此判TPU125–150B过期或相加。通过。 |
| Google融资框架 | 同件F-42明确原2026 NPA上限30B，5月Series H投入10B使余量降20B；9/30无该NPA普通股或票据已发行。p176及F-67的IPO同步拟10B再占用该剩余框架。T14写“原20B/originally20B”不够准确，须改“9/30剩余20B”。 |
| Broadcom租赁主体 | 同件p181写Broadcom及转让后融资实体，租金总额161.2B不含利息；并未证明受让人均为Broadcom affiliate或会计关联方。T15应改“Broadcom及受让租约的融资实体”。同页还说明Q2、10月转让未增加总租金，为重要防双算证据。 |
| Crux关联方 | Alphabet同一10-Q Note2明确16.8B backlog属于未合并权益法关联方合资企业；Note5及MD&A注明未来设施能源backstop10B。是真实相关交易证据，但不是独立圈外终端付款、现金或已损失。通过。 |

## 对正文的实质影响

这两处修正不会改变“硬件替代可以分散供给、共同模型客户信用风险仍集中”的结论，却影响已出资与剩余额度的时序，以及相关方交易的边界，必须修正后才可写终审PASS。保持：产品级利润未披露；融资安排不能加成需求；系统销售会转移部分建设和利用率风险，但回购及担保可能留下尾部风险；不能将TPU胜出等同所有旧GPU回本或行业总CapEx必降。

## 作者处理状态

作者已确认并完成T14、T15对应笔记及claims修改；复核人实际重读修改行，确认：30B→Series H占用10B→9/30余20B→IPO拟占用10B的链条已写清，租赁主体改为Broadcom及转让后融资实体，并补“转让本身未增加租金总额”。这两项已关闭。TPU专项交叉复核通过；本文件仍不替代中文四稿终审PASS。
