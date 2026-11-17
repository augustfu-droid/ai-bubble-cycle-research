## Chapter 3: How AI Makes Money—The Monetization Landscape and Coding TAM

Definitions and observations are current through 31 October 2026 (Beijing time). B denotes USD billions; 1B equals USD 1 billion. ARR, run-rate and recognized financial-statement revenue are used separately. Anthropic's public S-1 and cloud providers' latest fiscal quarters retain their respective reporting periods; product pricing, channel partnerships and free allowances on 26—30 October receive additional checks. Population statistics, historical product prices and tests retain their own observation dates; no comprehensive same-day retest was performed.

### Chapter Map and Chain of Reasoning

Anthropic's public S-1 reports 2026Q2 operating income of 0.974B, yet first-half operating loss of 0.693B; Meta's latest quarterly advertising revenue grew 26% while FCF turned negative. These figures make the commercialization debate more concrete: paid demand can grow and operations improve while cash recovery on new facilities may still lag. The following identifies payers, traces money among clouds, models and applications, then tests whether customer benefits and supplier profits can coexist. Sources appear in 3.2—3.3.

| Research question | Location | Conclusion and boundaries |
|---|---|---|
| Who pays, and what is sold? | 3.1—3.3 | Distinguish cloud services, advertising, subscriptions and APIs; total business revenue is not pure-AI revenue |
| Were earlier coding estimates correct? | 3.4 and Chapter 5 | Arithmetic holds conditionally; the fixed low-price seat ceiling should be withdrawn; consistent realized market totals remain unavailable |
| Can applications beyond coding earn money? | 3.5 and Chapter 6 | Some have revenue/cash evidence, alongside restructuring and loss cases; verify attribution and full costs individually |
| Can revenue absorb capital investment? | 3.6—3.8 | Model asset cohorts, service costs and cash flows; revenue ratios cannot replace IRR |
| What facts would change the judgment? | 3.9—3.10 | Track consistent growth, paid retention, cost per successful task and payback; retain unknowns as unknowns |

This chapter does not present “total AI revenue,” because public disclosures cannot support full-chain eliminations. A business pays an application company, which buys model APIs, whose provider rents cloud compute: all three may recognize revenue, but society has not therefore made three end payments. This gap limits aggregate measurement reliability; it does not deny real services at each layer.

### 3.1 14 Monetization Domains: Identify Payers and Billing Units First

Revenue, run-rate, investment and corporate valuation measure different things and cannot form one monetization-size ranking. The following 14 categories span infrastructure through end workflows. Each first asks what customers buy and how they pay, then examines costs and renewals. Charging for a product does not imply positive product profits; positive company net income does not prove every AI product is profitable.

| Domain | Main payer and billing unit | Available evidence | What does not directly follow |
|---|---|---|---|
| Cloud compute/model hosting | Enterprises and model companies; compute time, tokens and committed usage | Cloud-segment revenue and selected AI-specific run-rates; 3.2 | Total cloud revenue is not pure AI; long commitments are not collected cash |
| Advertising optimization | Advertisers; impressions, clicks or conversions | Advertising revenue, impressions/prices; new ChatGPT Ads disclosures, 3.2 | Not all advertising growth is AI-driven; advertisers' transaction volume is not platform revenue |
| Enterprise productivity | Enterprises; seats plus extra usage | Paid M365 Copilot seats; 3.3 | Seats × list price is not actual ARR or profit |
| Chat subscriptions/APIs | Consumers, developers and enterprises | Company run-rates/API prices; 3.3 and 3.7 | Annualized pace is not completed full-year revenue |
| Coding/development agents | Developers and engineering organizations; seats, usage and tasks | Subscriptions, billing rules and some revenue growth; 3.4 | Registered users are not paying developers; generated code is not accepted output |
| Customer service/CRM | Enterprises; seats, conversations, actions or successful resolutions | Agentforce ARR and definitions; 3.5 | Billed actions are neither unique customers nor successful resolutions |
| Legal technology | Law firms/in-house legal teams; users, documents or projects | Named deployments, procurement and renewals require individual checks | Deployment announcements do not replace contract values or legal-liability costs |
| Financial research/information | Financial institutions/enterprises; content subscriptions and workflows | AlphaSense Q2 ARR update; 3.5 and Chapter 6 | Data licensing/expert-network revenue is not all incremental generative AI |
| Medical documentation/assisted diagnosis | Hospitals, doctors or payers; seats or visits | Procurement contracts, actual usage and clinical evaluation | Signed value is not recognized revenue; saved time is not improved clinical quality |
| Audio/video/content generation | Creators/enterprises; subscriptions, duration and generation volume | ElevenLabs company ARR; 3.5 | Total content-market size is not the billable generation-tool market |
| Education | Students, families and schools; subscriptions or courses | Paid retention, tests and learning outcomes | All traditional education-app revenue is not incremental AI revenue |
| Autonomous driving/robotics | Passengers, logistics and industrial customers; transport volume, work hours or equipment | Paid-operation permits, unit operating costs and deliveries | Valuations, financing and demos do not replace repeatable operating profits |
| Research/biopharma | Pharma companies/labs; services, licensing and milestones | Collected service fees, R&D milestones and clinical results | Maximum contractual milestone value is not current revenue |
| Sovereign AI/defense | Governments/contractors; project and maintenance contracts | Appropriations, signing, performance and acceptance | Budget intentions are not orders; orders are not current fiscal payments |

The last eight lack sufficiently consistent public data for industry profit rankings; they cannot all be labeled loss-making. Research can first track customer value and contract execution, then determine which companies warrant earnings models. One ARR label cannot flatten every use case.

### 3.2 Cloud and Advertising: Mature Billing Channels, Not Entirely AI Revenue

#### 3.2.1 Actual Cloud-Segment Revenue and AI-Specific Disclosures

| Company/period | Recognized revenue or operating metric | AI-attribution boundary |
|---|---|---|
| Amazon AWS, 2026Q3 | Revenue 45.984B, operating income 17.773B, recalculated margin 38.7% | Includes conventional cloud and AI; not all pure AI; AI run-rate retains its company-disclosure date |
| Microsoft Azure, FY2027Q1 ended 9/30 | Azure revenue 33.165B, YoY +48%; group operating cash 58.000B is a separate group measure | New Azure definition with restated comparatives; not directly joined to old “Azure and other cloud services,” Microsoft Cloud or group revenue |
| Google Cloud, 2026Q3 | Revenue 30.709B, operating income 11.121B, recalculated margin 36.2% | Includes cloud, Workspace and TPU-system sales; not all recurring compute rent or pure AI; segment profits do not prove payback for each AI asset cohort |

Sources: [Amazon third-quarter earnings](https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Third-Quarter-Results/default.aspx), [Microsoft FY27Q1 earnings](https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast), [Alphabet third-quarter earnings](https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf). All three have now reported quarters ended 30 September, but fiscal-year labels and business definitions still differ; their sum is not the end-customer AI market.

These figures prove real platform billing and segment profitability, not the return on this round of incremental compute. Profits from mature databases, storage, networking and existing customers coexist with new AI. Using all cloud-segment profits to cover new AI assets and then claiming each cohort has paid back substitutes legacy earnings for evidence on new investment.

The three reports awaiting verification in the prior edition are now published. Actuals still support cloud billing and profits, but cash is more divergent: Microsoft group operating cash less cash PP&E is 18.633B; Alphabet company FCF is −9.065B; Amazon TTM FCF is −42.357B. Periods, CapEx and lease definitions differ, so no ranking is made. Separate legacy cash buffers, current new-asset payments and future recovery; neither “record cloud revenue” nor “negative group FCF” supports a one-direction verdict alone. [Microsoft Q1 10-Q](https://www.sec.gov/Archives/edgar/data/789019/000119312526436133/msft-20260930.htm), [Alphabet Q3 10-Q](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000084/goog-20260930.htm), [Amazon Q3 10-Q](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000040/amzn-20260930.htm)

As historical anchors, AWS separately disclosed Q2 AI-business and chip-business run-rates exceeding 25B. These old observations are not Q3 current values. Their workloads may overlap; without a company elimination schedule, they cannot sum to “50B of incremental AI revenue.” Likewise, cloud financing of model companies may help customers pay cloud bills, requiring funding-source monitoring, but does not make all revenue from actual compute use fictitious.

#### 3.2.2 Two Forms of AI Advertising Monetization

Meta's 2026Q3 advertising revenue, released on 21 October, was 63.061B, up 26% year on year; impressions rose 10% and average price 14%. Alphabet's newly released same-quarter advertising revenue was 82.012B: Search 63.350B, YouTube 11.207B and Network 7.455B, replacing the prior Q2 historical anchor of 81.629B. Actual payments demonstrate monetization, but attribution among AI recommendation, customer mix, ad demand and FX still needs breakdowns or experiments. Neither company's entire advertising business is incremental generative-AI revenue. [Meta Q3 earnings](https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Third-Quarter-2026-Results/default.aspx), [Alphabet Q3 advertising breakdown](https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf)

Billing growth and construction pressure coexist in Meta's report: Q3 operating cash of 32.786B less cash fixed-asset purchases of 33.942B and finance-lease principal of 0.964B yields company FCF of 32.786－33.942－0.964＝−2.120B. Nine-month FCF remained positive at 11.049B, with ending cash/equivalents/marketable securities totaling 82.45B; one negative quarter does not mean cash exhausted for the year. Full-year CapEx guidance including lease principal narrowed from 130—145B to 135—145B and remains a forecast. GAAP operating income includes 9.89B in legal expense; the entire profit decline cannot be attributed to AI investment. [Meta Q3 earnings, cash reconciliation and CFO outlook](https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Third-Quarter-2026-Results/default.aspx)

One monetization route improves conversion or lowers advertiser acquisition costs within existing advertising; another sells ads directly at a new AI entry point. OpenAI disclosed on 31 August 2026 that ChatGPT Ads reached 1B in annualized revenue run-rate within fewer than 200 days of launch. This is more direct evidence of new billing than “AI optimized a USD 400 billion advertising market,” but neither 1B of completed annual advertising revenue nor separately disclosed advertising profit. Source: [OpenAI advertising announcement](https://openai.com/index/expanding-access-to-ai-with-chatgpt-ads/).

Advertising can subsidize free users' inference costs while adding constraints: sufficient inventory, commercial intent and conversion measurement; whether commercial content harms trust; and whether budgets merely move from other platforms. Winning share can grow an individual platform; budget transfers do not create equal new end demand industry-wide.

On 5 October OpenAI announced visual ads in image-generation contexts, planned for testing among US Free/Go users later that month, plus expanded attribution/incrementality measurement partnerships. This adds testable monetization contexts, but the format was not fully launched and the announcement supplied no additional advertising revenue/profit figure. Individual advertiser cases cannot establish platform-wide ROI. [OpenAI advertising and measurement update](https://openai.com/index/new-chatgpt-ads-format-and-measurement/)

An official engineering article on 21 October additionally disclosed over 100,000 advertisers since launch: cumulative participants, not monthly active advertisers, persistent repeat buyers or standalone profit. Its conclusion reiterated advertising run-rate above 1B, without a new precise amount or recognized financial revenue; do not add it to August's figure. This round also obtained no later overall-revenue original of equivalent quality to replace OpenAI's March anchor. [ChatGPT advertising-system explanation](https://openai.com/index/building-chatgpt-ad-stack/).

### 3.3 Models and Enterprise Subscriptions: Public Statements Begin Testing Annualized-Revenue Narratives

#### 3.3.1 Distinguish Three Kinds of “Annual Revenue”

Financial-statement revenue covers performance already delivered during a reporting period. ARR is a company-defined annualization of recurring contractual revenue, with definitions varying across companies; run-rate extrapolates the latest month/quarter into a year. Fast-growing businesses' ending run-rates usually exceed preceding-year recognized revenue; usage businesses also reflect concentrated purchases, seasonality and short campaigns.

This chapter therefore retains disclosure dates and leaves newer values unresolved rather than turning “the older anchor publicly verified so far” into “the company currently reaches only this scale.”

| Entity | Disclosure and observation date | Use |
|---|---|---|
| OpenAI | 2026-03-31 company announcement: monthly revenue 2B | Arithmetically approximately 24B annualized; March operating pace, not 2025 annual revenue or October current performance |
| Anthropic | Public S-1 on 10/26: 2025 revenue 4.585B; 2026H1 revenue 16.286B, operating loss 0.693B | 2026H1 unaudited interim statements; May's 47B run-rate remains historical pace, no substitute for actual revenue/cash |
| Claude Code | 2026-02-12 company disclosure: run-rate above 2.5B | Product within Anthropic; cannot be added to the parent total or treated as October current value |
| M365 Copilot | 2026-07-29 official call: over 30 million paid seats; October FY27Q1 call did not update paid seats | Retain July anchor; activity/automated-task growth cannot extrapolate October paid seats or ARR |
| ChatGPT Ads | 2026-08-31 company disclosure: ad run-rate 1B | Evidence of billing through a new channel; not mechanically added to OpenAI overall revenue |

Sources: [OpenAI March announcement](https://openai.com/index/accelerating-the-next-phase-ai/), [Anthropic October public S-1](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm), [Anthropic May Series H announcement](https://www.anthropic.com/news/series-h), [Anthropic April announcement](https://www.anthropic.com/news/anthropic-amazon-compute), [Claude Code February disclosure](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation), [Microsoft July call](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4), [OpenAI August advertising announcement](https://openai.com/index/expanding-access-to-ai-with-chatgpt-ads/).

Anthropic's evidence has progressed: its 26 October public S-1 reports Q1/Q2 revenue of 4.731B/11.555B and Q2 operating income of 0.974B, while first-half operating loss remains 0.693B. These coexist because Q1 operating loss was 1.667B. Quarterly profitability belongs in the assessment but cannot establish full-year, all-model or all-new-compute profitability. These interim figures are unaudited; appearing at the SEC does not make them audited Q3 results. [Anthropic S-1, consolidated operations and Quarterly Results of Operations](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm)

The easiest misreading is the first-half net loss of 80.748B. The cash-flow statement reverses 72.388B of fair-value changes in convertible notes, derivative liabilities and SAFEs, plus 8.720B of recognition/fair-value changes in other financial instruments. Net loss therefore cannot directly be called “USD 80.7 billion burned in half a year.” Operating cash was positive 3.929B, which the company attributes both to operating improvement after noncash adjustments and to customer/supplier payment timing; net financing inflow of 110.774B is a different cash category, not customer payments. [S-1, Cash Flows and consolidated cash-flow statement](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm)

| 2026H1 financial observation, USD B | Disclosed value | What it answers, and what it does not |
|---|---:|---|
| Usage-recognized revenue | 13.064 | Usage business dominates revenue, but is not exclusively coding |
| Subscription revenue | 3.222 | Sums with usage to 16.286; subscription run-rate cannot be added again |
| Q1 operating result | −1.667 | Shows profitability was not continuous through the half |
| Q2 operating result | +0.974 | Quarterly operating profit; adding Q1 leaves H1 −0.693 |
| H1 net loss | −80.748 | Contains large noncash financial-instrument items, not direct cash consumption |
| H1 operating cash flow | +3.929 | Current net operating inflow; payment timing and future firm spending still need analysis |

All interim figures are unaudited. Revenue breakdowns come from the S-1 financial-note Revenue section, and operating results from quarterly operating results. They cannot be mixed with adjusted operating income or converted into a particular product's gross profit. [Anthropic 2026-10-26 S-1, Revenue and Quarterly Results of Operations](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm)

This narrows the claim that “the model layer always depends solely on financing without operating improvement,” but does not prove long-term self-sufficiency. One positive operating-cash observation does not prove that all future minimum purchases/lease payments in Chapter 2 can be covered, nor can all short-term securities purchases in investing cash be called infrastructure CapEx. Align sustained customer collections, working capital, actual equipment investment and lease payments quarterly. Later media run-rates and funding negotiations for OpenAI still lack equivalent formal statements in this review and cannot form a consistent ranking with Anthropic's new accounts.

Rereading also fills the prior edition's omitted September operating metric: the S-1 reports approximately 900% net revenue retention at 30 September, based on the three months one year earlier, including only customers with at least USD 1 of base-period revenue and excluding fixed-price Pro/Max subscribers. Current-period revenue is compared with that same cohort's base-period revenue. It supports substantial expansion among existing enterprise/usage customers, not 900% customer retention or guaranteed repetition next year. The filing says these internal-system metrics lack independent third-party verification; full interim statements still end in June, so September's metric cannot manufacture a Q3 income statement. [S-1 metric definitions, risk qualifications and September customer expansion](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm)

#### 3.3.2 Why Billing Growth Still Does Not Prove Unit Economics

Attracting users is only step one. Stable subscription revenue alongside rapidly rising use can increase inference, tool-call and human-support consumption per paid seat, separating revenue growth from gross-margin improvement. Conversely, caching, model routing and cheaper models can let use outgrow costs; profits need not fall with API list prices.

Monthly models should track paying customers/seats, actual revenue per seat, extra usage revenue, discounts/free allowances, activity, cancellation/downgrades, inference and support costs. “Paid seats × public monthly price” ignores enterprise discounts, annual-payment timing, product mix and trials; M365 Copilot seat evidence cannot yield an undisclosed precise ARR.

I now place more weight on the same customers' paid usage and gross profit across quarters than on total users. Anthropic's newly disclosed net revenue retention closes one information gap, but product margins, customer cash collection and durability remain incomplete; other companies cannot borrow its metric. Heavy users may drive growth; run-rate size alone still cannot identify the ultimate winner.

Microsoft's latest call still did not update M365 Copilot paid seats. Activity, automated tasks and product-mode choices help observe adoption, but do not replace paid contracts or actual receipts per seat. This report retains July's 30 million historical anchor, without calling it October current value or inferring no growth from the absence of an update. [Microsoft FY27Q1 call](https://www.microsoft.com/en-us/Investor/events/fy-2027/earnings-fy-2027-q1)

#### 3.3.3 Gross versus Net Cloud-Channel Recognition Does Not Determine Whether Profits Are Real

Anthropic's public S-1 notes F-21—F-22 explain that in cloud-marketplace distribution it still contracts directly with customers, provides intelligence services and sets prices. Cloud providers do not control services before transfer, so Anthropic recognizes revenue gross as principal. Usage services recognize revenue as tokens are consumed; subscriptions recognize over service periods. This formal policy supplies a basis for testing channel revenue. [Anthropic S-1, Revenue Recognition, F-21—F-22](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm)

Gross/net methods first answer who controls delivered services, not “gross is unreal, net is real.” Cross-company comparison needs consistent channel scope, performance responsibility, revenue periods and associated costs. Without corresponding contracts/policies, a uniform 25%—40% haircut to Anthropic revenue cannot create “true net ARR” comparable with another company. Expenses affect profits, and internal industry payments need elimination when estimating end demand; neither adjustment authorizes arbitrary rewriting of recognized issuer revenue.

### 3.4 Coding TAM: Review the Old Forecast before Rebuilding Billing Boundaries

**The ruling on the old estimate: conditional multiplication holds; calling it an absolute market ceiling does not; whether realized industry totals have exceeded it remains unverified.** Comparison with original Git history found that the V1.0 snapshot's original volume listed USD 43.8 billion at monthly prices above USD 100 while calling USD 17.5 billion at USD 40 the “absolute ceiling”; the main report also wrote USD 13.1 billion as $131B. Later market growth cannot hide conflicting assumptions and a tenfold unit error. V1.5 withdrew the hard ceiling and replaced it with sensitivities; this edition retains that correction. See Chapter 5, 5.1 and 5.4 for original locations, individual rulings and validation windows.

#### 3.4.1 Population Base and Actual Billing Boundaries

The 36.50 million professional developers come from SlashData's early-2025 survey estimate, with approximately 47.20 million total developers. Its population page currently shows 48.40 million total developers, explicitly updated for 2025Q3; citation in a 2026Q1 article is not a new population survey. No updated, consistently defined professional subset was obtained, so 36.50 million remains a historical sensitivity base, not an exact October-2026 population. Sources: [SlashData 2025 population research](https://www.slashdata.co/post/global-developer-population-trends-2025-how-many-developers-are-there), [Population definitions page](https://www.slashdata.co/research/developer-population).

GitHub platform users and Copilot users disclosed in Microsoft's FY26Q4 call are two other populations. Registered platform accounts cannot replace professional population, nor can all Copilot users be counted as paying. When one engineer subscribes to several tools, deduplicate people but record actual payments to different vendors separately. Vendors' upstream model payments require elimination in industry-wide end-market totals.

In June 2026 GitHub began moving Copilot billing to token-consumption AI Credits, allowing usage beyond seat-included allowances, with transition arrangements for old annual contracts. The market therefore no longer wholly obeys “each programmer buys one fixed USD 20 monthly software subscription.” Sources: [GitHub billing-plan announcement](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/), [June launch details](https://github.blog/changelog/2026-06-01-updates-to-github-copilot-billing-and-plans/).

#### 3.4.2 Seat Sensitivity: Population × Penetration × Price

Annual pure-seat market revenue = addressable professionals N × paid penetration s × average actual monthly revenue P × 12.

The table is mechanical sensitivity, not a market forecast. N=36.50 million, excluding new nonprofessional users and assuming one product per person; prices are scenario variables, not any company's realized average selling price.

| Average actual monthly revenue | 25% paid penetration | 50% paid penetration | 100% paid penetration |
|---|---:|---:|---:|
| USD 10 | USD 1.095 billion | USD 2.190 billion | USD 4.380 billion |
| USD 20 | USD 2.190 billion | USD 4.380 billion | USD 8.760 billion |
| USD 30 | USD 3.285 billion | USD 6.570 billion | USD 13.140 billion |
| USD 40 | USD 4.380 billion | USD 8.760 billion | USD 17.520 billion |
| USD 100 | USD 10.950 billion | USD 21.900 billion | USD 43.800 billion |

At 100% penetration and USD 30 monthly, 36.50 million×30×12＝USD 13.14 billion, or 13.14B. People, dollars and billions must remain dimensionally consistent. This is annual revenue under one seat assumption, not a measured market value.

Seat models remain useful for clarifying customer scale, ability to pay and share assumptions, but are not hard ceilings immune to changing business models. Heavy enterprise users may allocate tools to R&D budgets and pay per task/compute. Nondevelopers may pay only while building sites, cleaning data or automating projects; new users may not remain all year.

#### 3.4.3 Expanded Model: Do Not Count Seats and the Same Usage Twice

Revenue can be expressed as base-seat revenue＋usage revenue beyond included allowances＋independent task/service revenue－refunds and discounts. “Beyond included allowances” matters: adding token value already included in subscriptions overstates revenue.

A purely illustrative enterprise scenario: 10 million paid seats at actual average subscriptions of USD 30 monthly produce USD 3.6 billion annually; an extra USD 100 per seat each year adds USD 1 billion, totaling USD 4.6 billion. If 1 million nondevelopers separately purchase only two months at USD 20 monthly, they add USD 40 million, not USD 240 million of full-year subscriptions. All user counts, prices and consumption are research assumptions, not industry actuals.

Task billing has another boundary: willingness to pay for a migration, fix or build depends on total alternative cost, not code volume. Cheap generation can expand demand, but if requirements, testing, launch, compliance and maintenance still require people, application vendors capture only some value. The entire outsourcing market cannot be transferred without discount into AI-coding-tool revenue potential.

Chapter 5, 5.6 puts professional paid person-months, incremental usage, nonprofessional paid months and nonoverlapping task contracts into a conditional calendar-2027 model, yielding 3.94B and 11.66B. Inputs are not calibrated to measured industry data; these are neither a forecast range nor confidence bounds. Bundles also require coding-use allocation; hosting and noncoding work cannot all count, and vendors' own API procurement cannot be added outside end-customer bills.

#### 3.4.4 Current Competitive Evidence and Valuation Methods

Cursor's November 2025 announcement reported annualized revenue exceeding 1B and post-money valuation of 29.3B, now a historical funding anchor. On 14 August 2026 it formally announced completion of its acquisition by SpaceX, without consideration disclosed. The old financing valuation cannot remain a current independent-company valuation, and negotiation rumors cannot supply the acquisition price. Current packages also contain noncoding features; bundle revenue is not pure coding. [Historical funding announcement](https://cursor.com/blog/series-d), [Acquisition completion](https://cursor.com/blog/joining-spacex), [Current pricing](https://cursor.com/pricing).

Microsoft's July official call reported GitHub Copilot revenue growing over 60% sequentially and effects of new usage billing on revenue and gross margin. October disclosed agent-feature credit consumption more than doubling, without a new absolute product-revenue figure. Anthropic S-1 Q3 heavy Code-user spending distributions show high usage, not average spending across all users; Code cannot be added to parent revenue. Codex official active users are not paying users, and Replit's year-end 1B run-rate target is not yet due. Adding figures across different periods, units and statuses produces an unauditable total. [Microsoft July call](https://www.microsoft.com/en-us/Investor/events/fy-2026/earnings-fy-2026-q4), [October call](https://www.microsoft.com/en-us/Investor/events/fy-2027/earnings-fy-2027-q1), [Anthropic S-1](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm), [Replit target announcement](https://replit.com/blog/replit-raises-400-million-dollars). See Chapter 5, 5.3 for product originals and gaps.

Valuation exceeding traditional seat TAM alone does not establish a bubble: valuation is a stock of future cash flows and TAM an annual revenue flow, with no requirement that their ratio be below 1. The relevant inputs are future serviceable market, share, net/cash profit margins, competitive pricing, capital consumption and dilution; whether growth brings current high multiples down, and profits arrive when growth slows. Without these inputs, no deceptively precise fair valuation is given.

#### 3.4.5 Productivity: Individual Impressions Cannot Directly Become TAM

Positive evidence must be included. Three enterprise field randomized experiments published in 2026 covered 4867 developers, with a pooled 26.08% increase in completed tasks and a standard error of 10.3 percentage points. Company and Microsoft researchers participated; task/adoption differences limit generalization. More tasks are not proportionate wage savings or a universal productivity multiple for the latest agents. Chapter 5, 5.8 compares enterprise experiments, maintainer acceptance and long-task reconstruction; 5.11—5.12 includes human review and failure remediation in equal-quality delivery costs. [Original Management Science study](https://pubsonline.informs.org/doi/10.1287/mnsc.2025.00535).

A counterexample merits retention. METR randomized early-2025 tools across 16 open-source developers familiar with their repositories and 246 tasks; allowing AI increased average completion time 19%. This applies to those tools, tasks and sample, not all current coding AI. METR's February 2026 follow-up explicitly says developers/tasks unwilling to work without AI dropping out, parallel-agent timing and other problems make it difficult to estimate acceleration reliably in the new experiment. Sources: [Original METR paper](https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf), [Follow-up experiment explanation](https://metr.org/blog/2026-02-24-uplift-update/).

Unqualified “5—10 times efficiency” is insufficient for procurement or forecasts. Customers should measure total time from a real task's proposal to acceptance, including prompting, review, retries, integration and maintenance, alongside defects and risk. Willingness to pay indicates perceived value, not that every customer has accurately converted it into cash benefits.

#### 3.4.6 Expanding Software Demand Can Coexist with Job Displacement

If the same software demand takes fewer hours, fixed seats may face pressure; if lower development costs make previously unaffordable projects viable, new projects and nondeveloper usage may expand. These mechanisms cannot be offset in advance, nor can code growth become paid growth. Separately observe existing customers' seat reductions and extra usage, and whether new customers keep paying after trials.

Easier generation does not remove requirements judgment, architecture, data permissions, distribution or maintenance responsibility. Verify which value slice tool providers can charge for, and whether software-company customers demand lower prices from cheaper substitutes or still pay premiums for data, integration and reliability. This neither assumes every software moat disappears nor counts all software services without discount in coding-tool TAM.

#### 3.4.7 From Task Substitution to Team Change: What Lies Between?

Between “the model writes this code” and “the company can employ one fewer person” lie task coverage, actual adoption, review/rework, collaboration and business demand. Developers still clarify requirements, design interfaces, check permissions, handle legacy systems and bear deployment responsibility. Multiplying generation speedup by all wages overstates substitutable labor. Conversely, stable reductions in testing, repair and delivery hours have economic value even without immediate layoffs.

Start with net hours for equivalent-quality delivery, then inspect team bottlenecks. Faster code without improved business acceptance, senior review or deployment queues may not increase releases. Junior roles may first see fewer hires, unfilled departures or reduced outsourcing rather than immediate incumbent removal; job, hiring, wage and delivery data must show which occurs. Fewer junior training opportunities may also affect future senior talent, an organizational cost not measured by current-quarter code volume.

Chapter 5 deepens original labor research and US/China cost scenarios, separating individual activity from company revenue, releases and employment. Vendor cases, surveys, self-reports and observational studies are not randomized causal conclusions. New evidence changes task/organization assessments, not a uniform industry layoff rate.

#### 3.4.8 Hours, Capacity and Cash Belong in Separate Accounts

| Change | Measurable benefit | When cash expenditure changes |
|---|---|---|
| Original team finishes the same work faster | Net hours after review/rework; capacity for other tasks | With everyone retained at unchanged pay, no equivalent wage cash saving arises; tool costs increase |
| Original team delivers more accepted work | Incremental contribution from new demand; value of earlier delivery | Requires new charges, reduced delay losses or other verifiable cash outcomes; more code is insufficient |
| Fewer additional hires or unfilled departures | Employment costs avoided against the original hiring plan | Requires a credible original plan, time window and maintained quality, not an invented retrospective baseline |
| Cancellable outsourcing/overtime reduced | Contractual and actual payment reductions | Deduct minimum commitments, exit fees, handover, internal takeover and ongoing tool costs |
| Existing headcount reduced | Steady-state pay and related avoidable costs | Also deduct severance, transition overlap, training, knowledge loss and future understaffing costs |

The same released hours cannot be valued at wages and fully counted again as outsourcing savings and new sales. Different realization paths require separate counterfactuals. Competition also affects customer-retained savings: lower software prices or shorter service contracts can pass gains downstream rather than leave everything with IDE, model or cloud providers. Chapter 5 therefore separates capacity value, net cash benefits and supplier billable potential, instead of relabeling a labor-cost table TAM.

#### 3.4.9 Latest Organizational Evidence and Two Cash Outcomes

New research observes what happens after generation. Chen and Stratton's 28 October revision covers 655 firms, 720542 workers observed cumulatively and approximately 445 million events. Code-output growth exceeds final-delivery changes, review becomes a constraint, and no significant overall employment change is detected. “Not detected” does not prove zero displacement: preserve statistical intervals, adoption duration and agents' incremental effect over existing assistants. Stanford's ADP study through June finds employment trajectories for ages 22—25 in high-AI-exposure occupations lagging low-exposure peers by 19%, mainly through reduced hiring. Authors explicitly call this descriptive, not a causal AI layoff rate. Both can hold: some firms have not cut staff while market entry has narrowed. [Chen–Stratton revision](https://fion.ac/jellyfish.pdf), [Original Stanford study](https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf)

Chapter 5 translates this distinction into budgets with equivalent acceptance criteria. All are author assumptions, including review, rework, governance and risk budgets, not US/China industry averages. A US team of 10 releases 2400 net steady-state hours, valued at USD 240,000 using original employment costs; after USD 40,000 for tools and other items, net capacity value is USD 200,000. Retaining everyone without additional operating benefits instead increases cash/risk budget by USD 40,000. Only if a full-year USD 180,000 hire is genuinely avoidable is steady-state net benefit USD 140,000. A Chinese team of 8 releases 900 net hours valued internally at RMB 120,000; subtracting RMB 90,000 leaves net capacity value RMB 30,000. If these hours replace cancellable outsourcing of 900 hours at RMB 220/hour, net benefit is RMB 108,000. Internal resource valuation and outsourcing savings are alternative uses and cannot be added.

These assumptions do not seek an attractive average ROI; they expose procurement's deciding variables: truly cancellable contracts/hiring, maintained equivalent quality, savings concentrated into usable people/time, and first-year integration consuming capacity. The US first-year example releases only 1500 net hours, insufficient to remove a full person-year; China's first-year net capacity value is negative. See 5.10—5.13 for itemized inputs, transition costs, fixed-headcount/fixed-budget cases and demand elasticity.

### 3.5 Beyond Coding: Find Renewable Demand in Workflows

#### 3.5.1 Customer Service and CRM: Outcomes and Changing Measurements

Salesforce disclosed on 26 August 2026 that Agentforce ARR exceeded 1.5B and combined Agentforce/Data360 ARR approached 3.9B, while noting Agentforce ARR now includes its AI offerings, Slackbot and Headless360. This is newer than 0.8B but changes product scope. Not all year-on-year growth is organic growth of the same product, and Agentforce, the combined figure and company revenue cannot be summed. Source: [Salesforce FY27Q2 earnings](https://www.salesforce.com/news/press-releases/2026/08/26/fy27-q2-earnings/).

Customer service can form a measurable feedback loop through ticket cost, resolution, human-transfer rates and complaints. Still beware “action counts”: splitting one problem into ten actions may raise billing without resolving ten problems. Value should rest on successful resolutions, repeat contacts, handling time and customer losses, not agent activity alone.

OpenAI's expanded ServiceNow partnership on 28 October adds evidence of moving from generated answers to permissioned enterprise actions. The ServiceNow MCP plugin was available that day; enhanced features, voice, security and Codex workflows remained planned or in preview. No new contract value, minimum purchase, recognized revenue or profit was disclosed. This counts as channel/workflow expansion; planned employee coverage is not paid seats, and mutual product use does not prove circular cash. [OpenAI—ServiceNow announcement and availability](https://openai.com/index/openai-servicenow-partnership-expansion/)

#### 3.5.2 Legal and Financial Research: Ability to Pay Comes from Responsibility and Content

Harvey's 28 July announcement disclosed its first quarter adding over 0.1B of ARR; September's said 80% of Am Law 100 firms used its products. Added ARR is not total ARR or quarterly revenue, and firm usage is not payment by every lawyer. Original financial detail sufficient to reconstruct late-October total ARR, collections and profits remains unavailable. [Harvey July announcement](https://www.harvey.ai/blog/harvey-announces-strategic-investment-from-goldman-sachs-and-jp-morgan), [September announcement](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence).

Legal-workflow value includes citation checks, case permissions, version records and responsibility allocation, beyond faster text. Financial research likewise has existing budgets for licensed content, expert interviews, filing retrieval and workflows. AlphaSense's original 27 August release says 2026Q2 ARR exceeded 0.7B, replacing the old 0.5B anchor. It still includes existing information/workflow businesses, not quarterly revenue or pure AI additions. October investment-banking subbusiness growth/new users cannot imply a new total platform ARR. [AlphaSense Q2 ARR disclosure](https://www.alpha-sense.com/press/alphasense-named-the-only-leader-in-market-and-competitive-intelligence-platforms/), [October banking disclosure](https://www.alpha-sense.com/press/alphasense-adds-over-10000-investment-banking-users-in-most-recent-quarter/).

These businesses may retain users better than general chat, but incur licensing, review and enterprise-sales costs. Pricing power depends on renewal, substitution by cheaper general models plus existing content, and who bears error costs.

#### 3.5.3 Audio and Content: Model Subscription Growth alongside Rights Costs

ElevenLabs' 5 May announcement reported ARR exceeding 0.5B in the first four months of 2026, versus 0.35B at 2025-end. Page-maintenance dates do not change that reporting window or make it October current revenue. Source: [ElevenLabs company announcement](https://elevenlabs.io/blog/500m-arr-and-new-investors).

The 30 September announcement said enterprises represented 55% of company revenue and ElevenAgents exceeded 15 million weekly conversations. The figure more than tripling since February was ElevenAgents ARR, not total company ARR. No latest absolute company ARR was supplied; 0.5B from another scope/base period cannot be multiplied by three. A tender offer is not customer revenue. [ElevenLabs September announcement](https://elevenlabs.io/blog/tender-22bn).

See Chapter 4 for US/China AI-video microdrama comparisons and model-provider analysis. Model demand comes from production: finished footage, failed retries, character/shot iteration, acquisition creatives, localization and audio. More viewers watching finished content chiefly increases content/distribution activity, not regeneration for every viewer. Without new titles or real-time personalized generation, viewing minutes cannot directly multiply into an API market.

Seedance, MiniMax/Hailuo and Kling should not be treated as the same business. APIs, consumer creation subscriptions, self-hosted open weights, internal platform usage and distribution channels have different payers and profit attribution. Better usable-output rates may reduce paid attempts per drama while enabling more titles. Price cuts, yield and output jointly determine model revenue. Chapter 4 constrains this reasoning with named products and financials, separating effects on video, dubbing and text-planning models.

Financials support a more specific assessment. MiniMax 2026 first-half group revenue was USD 116.573 million, gross profit USD 20.813 million and R&D USD 296.870 million. Open platform/enterprise services represented 63.4%, without a video/microdrama breakdown. Hailuo product revenue of USD 17.464 million in the first nine months of 2025 proves real video billing, but its historical share cannot explain today's group growth. Kling revenue exceeded RMB 650 million and RMB 850 million in the two first-half quarters, but cannot supply standalone video net income. These strengthen application-demand evidence without resolving R&D recovery. [MiniMax interim results](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0826/2026082600680.pdf), [MiniMax prospectus](https://www1.hkexnews.hk/listedco/listconews/sehk/2025/1231/2025123100025.pdf), [Kuaishou Q1 results](https://ir.kuaishou.com/node/11461/pdf), [Kuaishou Q2 results](https://ir.kuaishou.com/zh-hans/news-releases/news-release-details/kuaishoukejifabu2026niandierjidujizhongqiweijingshenhecaiwuyeji)

Chapter 4 also illustrates transmission using 120 minutes of finished footage. With explicit AI share, reuse, advertising/localization assumptions, newly accepted output of 6000 seconds, acceptance yield 25% and 90% charged, H3's official 768p output rate of USD 0.08/second gives restricted output fees of USD 1728. This excludes separate input, high-definition and service charges and is not an actual title budget. If same-specification prices halve and acceptance yield doubles, newly accepted output must quadruple to maintain output revenue; compute and contribution profit have separate thresholds. This is more testable than “microdrama viewing exceeds movies, so model revenue explodes.” [Current H3 billing items](https://platform.minimax.io/docs/pricing/overview)

These products have clearly paying users, but creators, enterprise customer service and media production differ. Individuals may subscribe per project and cancel; enterprises may pay more for low latency, licensed voices and service quality. More synthesis brings inference, storage, moderation and licensing costs. Generated minutes cannot project annual subscriptions, nor can all model-cost savings be assumed retained by application vendors.

#### 3.5.4 Healthcare, Education and the Physical World: Value Takes Longer to Establish

Financial reports added in V1.8 distinguish business models rather than label them all “not commercialized.” Duolingo Q2 revenue of 0.298454B and company FCF of 0.078630B show a complete education product generating cash, not isolated AI-feature contribution. Tempus revenue was 0.382486B, operating loss 0.075913B and net income 0.005642B, including unrealized securities gains of 0.0985B. Positive net income alone does not establish profitable healthcare-AI operations. Pony.ai Q2 Robotaxi service revenue of approximately 0.0121B includes joint-deployment revenue, not only fares; the group still had an operating loss. Use each on its own scope, without summing an AI-application market. [Duolingo Q2 10-Q](https://www.sec.gov/Archives/edgar/data/1562088/000162828026053603/duol-20260630.htm), [Tempus Q2 earnings](https://investors.tempus.com/files/doc_news/2026/07/Tempus-Reports-Second-Quarter-2026-Results.pdf), [Pony.ai Q2 earnings](https://ir.pony.ai/news-releases/news-release-details/pony-ai-inc-reports-second-quarter-2026-financial-results-total). See Chapter 6, 6.7—6.9 for full costs, periods and counterinterpretations.

Medical documentation can first be assessed through recording time, review rates and chart quality; diagnosis assistance also needs clinical safety and payer acceptance. Education needs retention/learning outcomes, not all subscriptions relabeled AI monetization. Autonomous driving and robotics must include human intervention, maintenance, insurance and utilization in unit operating costs.

Research/drug development often has large contractual ceilings but little near-term cash. Milestones need conditions, trigger probabilities and timing separated; cooperation demonstrates willingness to try, not an approved drug. Sovereign AI/defense also require separate intentions, budgets, contracts, acceptance and collection; political priority is not annual revenue. These require different models, not aggregate “AI-application ARR.”

Evidence on 27—30 October sharpens this boundary. Anthropic disclosed six drug-research partnerships, explicitly mostly preclinical; the next day's expanded AI for Science offers research institutions free credits. OpenAI launched GPT-6 Rosalind on 30 October for approved institutions' internal research, with standard API input/output at USD 15/75 per million tokens. A priced product exists, but customer count, realized revenue and standalone drug-research returns are undisclosed. Scientific-workflow adoption, free support, paid calls and ultimate drug revenue need separate accounts, not one realized healthcare TAM. [Anthropic drug-research stage](https://www.anthropic.com/research/early-progress-drug-development), [Research-credit program](https://www.anthropic.com/news/ai-for-science-expands-foundations-research-institutions), [OpenAI 30 October release record](https://developers.openai.com/api/docs/changelog), [Rosalind pricing/scope](https://developers.openai.com/api/docs/pricing), [Access scope](https://help.openai.com/en/articles/20001193-gpt-rosalind-for-life-sciences-research)

Government billing likewise distinguishes nominal budgets from consumption. On 27 October Anthropic announced 40% discounts on Enterprise, Government and API for government customers, immediately for direct procurement and over subsequent months for cloud channels, explicitly without minimum spending commitments. Approximately 500 government organizations using it and estimated savings of USD 1 billion are company disclosures; the latter is not USD 1 billion of orders. Discounts may encourage adoption while lowering revenue for equal use; subsequent usage, renewals and costs determine net effects. [Anthropic—GSA agreement explanation](https://www.anthropic.com/news/expanding-partnership-gsa)

#### 3.5.5 Consumer Apps and Chinese Mixed Segments: Revenue Growth Does Not Ensure Continued Operation

Character.ai entered a voluntary Chapter 11 court-supervised sale process on 12 October, with services continuing then, not already shut down or sold. The CEO's court declaration disclosed approximately USD 5.3 million August revenue and USD 8.2 million net cash burn, citing legal, staffing and financing pressures. Compute cost alone cannot explain this, nor can it establish failure of all companionship products. This case requires examining revenue, full service costs and financing dependence together. [Official announcement](https://blog.character.ai/an-update-on-character-ai/), [Court Doc 18, pages 4—5, 11—12](https://cases.stretto.com/public/x936/14939/PLEADINGS/1493910132680000000119.pdf).

China also requires business boundaries. Baidu's internal-management Q2 AI Applications revenue was RMB 2.5 billion and AI-native marketing RMB 2.6 billion, respectively +3% year on year and broadly flat. Alibaba's new AI Labs and Applications segment in the June-quarter report had revenue RMB 3.338 billion and adjusted EBITA loss RMB 13.861 billion, including model labs and apps, not entirely one consumer app's losses. The former establishes named AI billing; the latter shows mixed businesses still needing funding. Neither defines China-wide AI-application profits. [Baidu Q2 earnings and footnotes](https://www.sec.gov/Archives/edgar/data/1329099/000119312526355431/d112854dex991.htm), [Alibaba June-quarter report](https://data.alibabagroup.com/ecms-files/1532295521/fa5d65fc-9b3e-4e82-a8fc-4ce1c3e2c407/Alibaba%20Group%20Announces%20June%20Quarter%202026%20Results.pdf).

Thus “applications lack real payments” is not a universal explanation. The report's original fourteen domains already recognized multiple billing channels; this review adds operating figures and counterexamples, continuing to test demand, profit attribution, capital recovery and valuation alignment. Coding, microdrama and other-application sections give separate methods: one successful product does not prove industry-wide payback, and one restructuring does not prove technology worthless.

### 3.6 Three Layers of Global CapEx and Asset Recovery

Compute chips, data-center physical infrastructure and power correspond to different assets and payments. Summing revenue across three layers does not mean end users invested the same additional capital. Chips sold to server vendors and servers sold to clouds create revenue at separate companies; equipment, leases and power purchases may fall respectively into CapEx, leases and operating costs.

| Layer | Investment to record | Recovery/risk variables | Link to monetization |
|---|---|---|---|
| Compute chips/networking | Equipment, servers and network configuration | Effective utilization, service life, replacement and cost per task | Convert into billable compute/successful tasks; peak performance does not directly project revenue |
| Data-center physical layer | Construction, distribution, cooling, racks and leases | Service-ready dates, ramp, construction cost and repurposability | Uncommissioned assets cannot be matched to live revenue at assumed full same-year capacity |
| Power/interconnection | Generation/grid investment, connection and long-term power purchase | Timely delivery, price, minimum purchases and curtailment constraints | Power bottlenecks can constrain revenue or postpone spending, not necessarily destroy demand |

Global multiyear cumulative CapEx and one-year investment forecasts for selected clouds differ in sample, start/end years and asset scope. Without complete original models, two similar totals do not validate one another. Multiyear forecasts are not signed capital commitments; testing front-loaded investment needs annual payment paths, not only selected years' shares.

#### 3.6.1 Endpoint Revenue Cannot Directly Yield Capital-Recovery Rates

Fifth-year revenue multiplied by five and divided by cumulative CapEx gives neither actual cumulative revenue nor IRR. It omits revenue paths, operating expenses, tax, working capital, investment dates and residual value. Revenue is not cash returnable to investors; depreciation cannot be deducted again as a cash outflow after cash investment.

Even mathematically, “a linear five-year ramp” does not justify endpoint × five. If annual revenue rises continuously from zero to R at year-five end, the five-year revenue area is 2.5R. If five year-end annual revenues are defined as 0.2R, 0.4R, 0.6R, 0.8R and R, the discrete sum is 3R. Neither is 5R. These are exercises, not forecasts of real AI-industry revenue.

#### 3.6.2 Use Project or Asset-Cohort Cash Flows Instead

For enterprise free cash flow, FCFF = after-tax operating income＋depreciation/amortization－capital expenditure－increase in working capital; enterprise value discounts future FCFF and terminal value. Project returns require period-by-period construction investment, commissioning/ramp, revenue, service costs, replacement capital and exit residual value. Without full cash flows, retain “returns unproven,” not a crude revenue ratio upgraded to a yield.

This also qualifies cycle judgments: high CapEx, rising cloud profits and application revenue can coexist without eliminating risk. Temporarily slower CapEx may reflect grid/construction constraints, not automatically demand collapse. Track commissioned cohorts' revenue utilization, service gross profit and payback periods against the next investment cohort.

### 3.7 API Pricing and Revenue Equations: Price Cuts, Usage and Cost per Successful Task

#### 3.7.1 Disclosed Rates by Product, Observation Date and Context Tier

Price competition exists, but cheaper caching, a cheap new model and lower standard prices for the same model are different events. Older rows retain September—9 October 2026 announcement observations; Terra, Rosalind, Haiku, Argon and DeepSeek pricing was reread on 31 October. Adding previously omitted Argon/DeepSeek does not mean all launched in the last four days. Unrefetched old rows are not live prices. Units are USD per million tokens; fast modes, tools, cache writes and other nonstandard charges are additional. These are not vendors' actual average revenue.

| Product and pricing observation | Uncached input | Output | Cache read | Limitations |
|---|---:|---:|---:|---|
| Fable 5.1, released 1 September | 10.00 | 50.00 | 0.25 | Cache writing extra; comparison with previous-generation USD 1 caching concerns only that item |
| Gemini 3.8 Flash, 2 September promotional announcement | 0.75 | 3.75 | Not shown here | Announced through 2026-12-31; planned from 2027-01-01: input 1.50, output 7.50 |
| GPT-6 Sol, 22 September announcement | 2.00 | 10.00 | 0.20 | Prompt input no more than 272k tokens |
| GPT-6 Luna, 22 September announcement | 0.10 | 0.50 | 0.01 | Same condition; different capability tier, not an equal-quality price comparison |
| Claude Opus 5.5, released 22 September | 4.00 | 20.00 | 0.20 | Standard mode; cache writing/fast mode extra |
| GPT-6.1 Sol, released 29 September | 2.00 | 10.00 | 0.10 | Launch observation retained; cache change does not alter uncached bills |
| Sonnet 5.5, repriced 7 October, reread 9 October | 2.00 | 10.00 | 0.10 | Replaces September launch cache price 0.20 |
| Haiku 5.5, released 7 October, reread 9 October | 0.10 | 0.50 | 0.01 | Per-request prompt input no more than 100k tokens |
| Haiku 5.5, high-context tier | 0.50 | 2.50 | 0.05 | Per-request prompt input above 100k; entire request charged at high tier |
| GPT-6.1 Terra, released 26 October, reread 31 October | 1.00 | 5.00 | 0.05 | Standard API; capability/task consumption differs from Sol, so half-price does not establish half cost |
| GPT-6 Rosalind, released 30 October, reread 31 October | 15.00 | 75.00 | 1.50 | Approved research uses only; cache writing, tools and other services extra |
| Gemini 4 Argon, released 13 October, reread 31 October | 2.00 | 10.00 | 0.10 | Live API launch promotion; announcement footnote ends promotion 30 November, then 4/20 |
| DeepSeek V4.1-Flash-1017, 31 October pricing, peak | 0.30 | 1.20 | 0.006 | Off-peak 0.15/0.60/0.003; context and tool billing require separate verification |
| DeepSeek V4-Pro-0813, 31 October pricing, peak | 1.32 | 3.96 | 0.044 | Off-peak 0.66/1.98/0.022; capability not equivalent to Flash |

Sources: Anthropic, [Fable/Mythos 5.1 release](https://www.anthropic.com/claude-fable-and-mythos-5-1), [Opus 5.5 release/pricing](https://www.anthropic.com/claude-opus-5-5), [Sonnet 5.5 release](https://www.anthropic.com/claude-sonnet-5-5), [Haiku 5.5 and cache repricing](https://www.anthropic.com/claude-haiku-5-5), [Official pricing/tiers](https://platform.claude.com/docs/en/about-claude/pricing); Google, [2 September release and price footnotes](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/); OpenAI, [22 September API changelog](https://developers.openai.com/api/docs/changelog), [29 September GPT-6.1 Sol release](https://openai.com/index/introducing-gpt-6-1-sol/).

Sources for the two new rows: [GPT-6.1 Terra launch pricing](https://openai.com/index/introducing-gpt-6-1-terra/), [30 October Rosalind release record](https://developers.openai.com/api/docs/changelog), [OpenAI standard API pricing, short-context tier](https://developers.openai.com/api/docs/pricing). Pricing has Standard, Flex/Batch, Fast and other modes; half-price batching is not universal standard pricing. This review did not reconstruct every long-context tier; requests beyond scope require the original table.

Added sources: [Gemini 4 Argon release/promotional footnote](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/), [DeepSeek official pricing/aliases](https://api-docs.deepseek.com/quick_start/pricing/). DeepSeek peak periods are Monday—Friday UTC 01:00—04:00 and 06:00—10:00, excluding Chinese statutory holidays; all other times, including weekends, are off-peak. Old Flash aliases are accepted but route to V4.1-Flash-1017, so an alias does not establish use of the original model. Search/Fetch charge separately per successful request; at this edition's cutoff, related server-side calls remained free, with billing starting 1 November at 00:00 Beijing time as stated on the page, not October revenue already collected.

Gemini 4 Carbon's 28 October announcement also lists promotional rates, but initial access is for cyber defenders and approved program participants; general developer, enterprise and consumer access remains future. It is therefore excluded from generally purchasable current rows. Restricted access and published pricing are separate conditions. [Carbon release/access scope](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/)

Opus 5.5 input/output list prices fell from Opus 5's USD 5/25 to USD 4/20, down 20%; cache reads fell from USD 0.50 to 0.20, down 60%. The company's claimed 40% typical-work cost reduction also includes changed task consumption: vendor workflow testing, not independent measurement or a 40% gross-profit increase. The claim of approximately 20% lower cost for most Sonnet agent tasks needs the same qualification.

For requests all meeting their context conditions, 1 million uncached input and 200,000 billed output tokens cost USD 4 for Sol, USD 0.20 for Luna and USD 8 for Opus 5.5; GPT-6.1 Sol and Sonnet 5.5 both cost USD 4. This is a fixed-usage bill. Real tasks may use different token counts, retries, tools and human review; proportional bills do not establish proportional changes in actual delivery cost.

Haiku thresholds apply per request; prompt input includes cached read/write input, and the premium is not only on tokens above 100,000. Ten requests each with 100,000 uncached input and 20,000 output total 1 million input/200,000 output and cost USD 0.20. Splitting the same total into five requests each with 200,000 input/40,000 output puts every request in the high tier, totaling USD 1. Equal total tokens do not mean equal tiered charges.

Open weights also cannot be plotted at zero cost. They may remove some licensing fees, but inference still needs servers, energy, operations and service-quality investment; tokenizers may count identical text differently. Pricing research should fix tasks, quality, latency and full bills rather than connect minimum input prices across generations/capabilities into a “prices going to zero” curve.

Commercial billing is extending into longer tasks. Microsoft's 25 September announcement put Cowork, Code and Autopilot long tasks under usage billing with budget/consumption management. Home/Code were planned to roll out through Frontier over subsequent weeks, and Autopilot to expand private preview at month-end. Announcement status is retained; actual coverage was not separately verified. Usage billing can match heavy-task consumption but does not yet prove repeat purchasing or positive product gross profit. [Microsoft 25 September announcement, “Managing AI spend”](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)

From 28 October, eligible ChatGPT Pro/Business subscriptions can claim API credits up to USD 500 monthly; Business is calculated per paid seat, subject to workspace caps. This is an included subscription benefit, not another equal API cash payment. As an inference, it may promote trials/cross-product retention while reducing some developers' incremental payments. Token analysis must separate promotional-credit consumption, purchased credits and recognized revenue; credit face value cannot be added directly to end demand. [Release record](https://developers.openai.com/api/docs/changelog), [Credit rules/validity](https://developers.openai.com/api/docs/guides/chatgpt-api-credits)

#### 3.7.2 Discrete Growth Must Retain the Cross-Term

For a consistently defined billed category, revenue R=P×Q. If actual average unit price changes p and billed volume q this month, revenue growth is:

**g = (1+p)×(1+q)－1 = p＋q＋p×q.**

The continuous-time differential approximation is dR/R=dP/P+dQ/Q, but is not an exact formula for large monthly changes. The following compares stress scenarios with a consistent discrete method; inputs are not observations.

| Assumed scenario, not observed fact | Monthly price change p | Monthly billed-volume change q | Monthly revenue change g |
|---|---:|---:|---:|
| Stronger usage | -15% | +20% | +2.00% |
| Intermediate stress case | -15% | +10% | -6.50% |
| Weaker usage | -15% | +5% | -10.75% |
| Unchanged revenue | -15% | +17.65% | Approximately 0.00% |

With a fixed -15% price cut, required volume growth to maintain revenue is 1/0.85－1=17.647%. This chapter has no evidence that all platforms continuously face this combination; disclosed billing expansion also means the intermediate stress case cannot be treated as most platforms' realized revenue path.

Multiproduct revenue is the sum of each category's P×Q, plus subscriptions/other revenue. More cheap-model use can lower blended prices while longer agent tasks raise billed volume; caching also changes price structure. Lower blended prices across periods do not necessarily mean an equal price war for the same service.

#### 3.7.3 Recalculating an API Bill

This example uses public Fable5.1 prices, not actual customer traffic: 1 million uncached input, 10 million cached-read and 200,000 output tokens cost USD 10, USD 2.5 and USD 10, totaling USD 22.5. Replacing only cache-read pricing with the previous generation's USD 1, everything else unchanged, gives USD 30: a 25% bill reduction, not 75%.

This simplified bill assumes the cache is already written, excluding new cache writes, tools, runtimes, regional premiums, taxes and contractual discounts. Real budgets must add them and compare task success. Prices 25% lower with retries doubling may still raise cost per success; one successful expensive-model call may cost less than repeated cheap-model calls.

### 3.8 Unit Economics and Customer ROI: Separate Profit, Cash and Value

#### 3.8.1 Application Revenue and Gross-Profit Bridge

Start with assumptions, not any company's earnings forecast: 100,000 paying users averaging USD 30 monthly generate USD 3 million revenue. Monthly inference/hosting costs USD 1.2 million, plus USD 600,000 delivery costs including support, content licenses and payment fees, leave USD 1.2 million gross profit and 40% gross margin. R&D, sales, administration, interest and tax are not deducted, so this is not net margin.

If inference/hosting unit prices fall 30% and total usage rises 20%, that cost falls from USD 1.2 million to USD 1.008 million. With revenue and other delivery costs unchanged, gross profit becomes USD 1.392 million and gross margin 46.4%. Upstream API cuts therefore need not reduce application gross margins. If competition also cuts application selling prices 20%, monthly revenue falls to USD 2.4 million and the same costs leave only 33.0% gross margin. Outcomes depend on whether users, application vendors or model providers retain savings.

#### 3.8.2 Is Paying Worthwhile for the Customer?

Monthly customer net benefit = realizable incremental gross profit/cost savings－tool fees－additional integration/review costs－error/compliance losses. Saved time becomes financial benefit only through usable capacity, less overtime or new business; multiplying salaries by minutes does not make all time savings cash savings.

For example, assume a workflow saves 20 hours monthly at RMB 200 fully loaded hourly cost, with only 40% convertible into realizable capacity or cost savings. Initial monthly benefit is RMB 1600; tools/review costing RMB 1000 leave RMB 600 net. Defining simple monthly ROI as “net benefit/current investment of RMB 1000” gives 60%. At only 20% realizability, benefit is RMB 800 and net loss RMB 200. This predicts no firm's ability to achieve that fraction; it exposes variables needing investigation.

Healthcare, law, finance and production code cannot optimize only this average. Low-probability severe losses may require human review, so automated task completion is not a directly replaceable personnel share.

#### 3.8.3 From Gross Profit to Capital Returns

Application prepayments can raise cash before revenue recognition; cloud capital investment precedes later depreciation/revenue; model companies need continuing training/R&D. Comparing layers' profits requires R&D treatment, licensing, stock compensation and lease definitions, plus checks against misclassifying investment gains as operations.

Determining where each USD 1 of end spending ends up requires full contracts and eliminations. Mixing corporate margins, equipment investment and supply-chain revenue slices cannot yield global profit allocation. A more feasible approach selects one project with bills/contracts, reconciles end payments, channel shares, model fees, cloud resources and equipment depreciation, then assesses replicability.

### 3.9 Verification Checklist for the Rest of 2026 and 2027

Observation thresholds need interpretation within consistent revenue, asset and cash definitions. Annual run-rate and annual CapEx cover different asset lives, revenue scopes and cash flows. Their ratio can indicate pressure, not establish payback. Checks roll forward with each company's next formal disclosure/contract review; unannounced dates are not calendar facts.

| Test | Currently established | Further evidence needed | What would force a revised judgment |
|---|---|---|---|
| Coding expands from seats into usage | GitHub changed billing and disclosed revenue growth | Consistent paid retention, spending per customer and gross profit | Sustained usage-revenue growth/stable retention warrant more potential beyond fixed seats |
| Enterprises pay rather than only trial AI | Paid seats, Agentforce ARR and Anthropic's defined-cohort net revenue retention disclosed; some new channels include credits/discounts | Renewals, discounts, scope changes and consistent growth | Expansion mainly from price cuts, consolidation or credits lowers revenue-quality assessment |
| Conversational advertising is repeatable | ChatGPT Ads disclosed 1B run-rate | Subsequent actual revenue, repeat advertisers and costs | Multiperiod growth/repeat spending with maintained experience supports the channel; short campaigns do not extrapolate |
| Sustainable model-layer profits | Anthropic S-1 shows Q2 operating profit, H1 operating loss but positive operating cash | Subsequent quarters, product costs, working capital and long-term payments | Sustained improvement weakens the pure-cash-burn view; one profitable quarter does not prove all construction repaid |
| Cheaper APIs reduce cost per successful task | Specific items such as caching fell | Fixed-task bills, retries and review | Lower success cost plus better customer net benefit expands payable use cases |
| New assets recover investment | Cloud segments retain real revenue/profit | Commissioning cohorts, utilization and incremental FCF | Improving cohort returns reduce capital-misallocation concern; repeated financing dependence does the opposite |

### 3.10 Where I May Be Wrong

I may still underestimate task billing's market expansion. A small set of intensive enterprise users buying expensive but reliable outcomes consistently can take revenue beyond traditional developer seats. But not all theoretically saved labor costs belong to tool providers. New API credits, government discounts and free research resources also require checking how much growth is incremental cash payment.

I may overestimate company-metric comparability. Changes in subscriptions, usage, channel revenue or contract scope break growth-series consistency. Anthropic's public S-1 improves overall operating/cash visibility, but unaudited interim statements, historical run-rate and product gross margins remain different evidence. Precise decimals cannot fill undisclosed product costs or subsequent quarterly cash.

Another risk is underestimating how cheaper hardware/inference and greater compute efficiency help applications. If unit-task costs fall faster than prices, profits can improve without explosive revenue; more reliable models reducing review can also improve actual customer ROI. Test quality, usage and expenses together, not list prices alone.

The current assessment: AI billing channels have broadened, and “prices going to zero” cannot erase revenue growth. Capital returns still require company-by-company, asset-cohort checks. The focus shifts from “is anyone paying?” to “whose payments are not double-counted, who bears delivery costs, and who ultimately retains cash?”
