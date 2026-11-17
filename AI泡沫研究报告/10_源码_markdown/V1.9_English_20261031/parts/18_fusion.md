## Appendix F: What Fusion Energy Can Change, and What It Cannot Replace

In this round of review, the official Helion Orion and CFS SPARC pages were reread on 31 October 2026 (Beijing time): Orion still lists initial operations in 2028 and a design capacity of at least 50MW as targets, while SPARC still lists Q>1 in 2027 as a target. Neither can be reclassified as having achieved commercial electricity supply. The original disclosure and observation dates are retained for the other projects; no site-by-site acceptance review was conducted. New power sources can change construction constraints and cost curves, but whether they improve recovery of AI capital still has to pass four tests: commercial electricity supply, system cost, competitive pass-through and customer payment.

### F.1 First Separate the Three Clocks

The first is the time for an experimental device to reach its physical target; the second is the time for a power plant to deliver net electricity continuously to the grid; the third is the time for electricity to reach data centers where it is needed, at a competitive price. A faster first clock warrants greater attention to the other two, but does not allow future cheap electricity to be entered directly into this year's inference costs.

Demonstration devices, first-of-a-kind power plants and large-scale replication must each have separate validation conditions. Projects may be delayed or brought forward, but without engineering progress, contractual acceptance terms and an independent probability model, one cannot predict that a particular power purchase agreement will certainly be fulfilled or is highly likely to default. A construction announcement is not commercial operation either.

### F.2 Disclosed Milestones for Two Approaches

| Approach | Company disclosures and observation boundaries | Items that cannot yet be treated as completed |
|---|---|---|
| Helion Orion | The company's project page lists site construction in 2025 and generator-building construction in 2026; initial operations are targeted for 2028, with a facility design supply capacity of at least 50MW to fulfill the Microsoft power purchase agreement; initial operations are not equated with acceptance of full supply capacity | Continuous net generation, contractual electricity-supply acceptance, availability, operating and maintenance costs, and the pace of subsequent replication |
| CFS SPARC | The official technology page still lists Q>1 in 2027 as a target; this is a device intended to validate technology for a subsequent power plant | Q>1 does not mean an existing commercial power plant is selling electricity to the grid, or that all engineering and economic hurdles have been cleared |
| CFS ARC | The first power plant targets approximately 400MW of grid supply in the early 2030s; papers on its physics basis were published in June 2026, and progress on design and engineering milestones was reported in August | Physics-design papers and milestone reviews do not mean that 400MW has been delivered; final capital cost and the economics of electricity sales remain to be realized |

Sources: [Helion Orion project page](https://www.helionenergy.com/orion), [CFS SPARC technology explanation](https://www.cfs.energy/technology/sparc/), [ARC project description](https://cfs.energy/technology/arc/), [June 2026 physics-basis paper announcement](https://www.cfs.energy/news-and-media/commonwealth-fusion-systems-builds-on-learnings-from-sparc-to-publish-five-peer-reviewed-papers-validating-the-physics-of-the-arc-fusion-power-plant/), [August 2026 engineering progress](https://blog.cfs.energy/sparc-progress-doe-milestone-approvals-reflect-cfs-power-plant-maturity/). The targets come from the project developers; they are not independent forecasts of success probabilities.

The system boundary must also be stated when measuring Q: the ratio of energy released by fusion to plasma-heating input is not the ratio of electricity output from the entire plant to all electricity consumed. Even if physical gain reaches its target, auxiliary systems, conversion efficiency, maintenance outages and material lifetimes still affect the electricity available for sale. These different measures cannot all be abbreviated as "net generation validated."

Another, nearer-term engineering milestone was NVIDIA's launch of the DSX Ready program on September 21, initially covering BESS (battery energy storage systems) and CDU (coolant distribution units), with Vertiv and others participating in the liquid-cooling equipment qualification process. It helps check whether components meet requirements, but cannot replace site engineering design and is not evidence of commercial electricity supply from a fusion plant. Component qualification, whole-site acceptance and actual customer payment should be kept separate. [NVIDIA DSX Ready explanation](https://blogs.nvidia.com/blog/dsx-ready-ai-factories-power-cooling/)

On September 28, Crusoe confirmed that it is the developer of Google's campus in Armstrong County, Texas. Construction began in June 2025 and is still underway; it cannot be recorded as a new start this week. The power plan includes direct connections to two wind farms of 265.5MW each, one operating and the other under construction. Rated wind capacity of 531MW is neither energized data-center IT load nor continuously available power. The announcement did not disclose the project's investment amount or cash payback period; it is not added to the table of realized capital expenditures or treated as a breakthrough in fusion. [Crusoe project announcement](https://www.crusoe.ai/resources/newsroom/crusoe-developing-data-center-campus-in-armstrong-county-texas)

On October 2, Oracle announced plans to subscribe to part of the power purchase arrangements for the existing Point Beach nuclear plant, expecting to absorb approximately USD 300 million in energy costs for local residents; approval by the Public Service Commission of Wisconsin is still required. This reminds researchers to include energy and local infrastructure responsibilities in data-center costs, but does not represent payment already made, approved electricity supply, or new nuclear generation capacity. Specific duration and annual payment schedules were not disclosed, so USD 300 million is not deducted directly from this quarter's free cash flow, and this nuclear-fission arrangement is certainly not treated as fusion implementation. [Oracle Point Beach announcement](https://www.oracle.com/news/announcement/oracle-announces-commitment-to-absorb-rising-point-beach-energy-costs-2026-10-02/)

### F.3 How Cheap Electricity Enters a Cost Statement

The cost of inference services includes not only electricity but also depreciation of accelerators and data-center facilities, networking and storage, personnel, software, spare parts, financing and other operations and maintenance. Cost structures, equipment utilization and accounting classifications vary across companies, and there is no uniform electricity-cost share for training, inference or different data centers. A model should use the target facility's electricity expenditure, effective consumption and total costs as its calculation bases, rather than replacing project data with an industry percentage.

A more reliable approach is an explicitly hypothetical calculation. Assume a service has revenue of 100 and a cost of service of 60, including electricity costs of 12. Electricity then accounts for 20% of service costs, and the original gross margin is 40%. If the electricity price falls by half and all other variables are unchanged, cost falls from 60 to 54 and gross margin rises to 46%, an improvement of 6 percentage points. In the extreme case of electricity costs falling to zero, gross margin becomes 52%; one must not add "electricity is 20% of costs" directly to the 40% gross margin to obtain 60%.

| Electricity price relative to baseline | Electricity cost | Total cost of service | Gross margin |
|---:|---:|---:|---:|
| 100% | 12 | 60 | 40% |
| 75% | 9 | 57 | 43% |
| 50% | 6 | 54 | 46% |
| 0% (extreme sensitivity case) | 0 | 48 | 52% |

All figures in the table are teaching assumptions; they represent neither electricity prices for any fusion project nor actual cloud-provider gross margins. A real model must also include the costs of connecting a new power source, transmission and distribution, backup power and retrofits. It cannot simply lower the electricity price while omitting the capital investment required to obtain that price.

The cost statement can also be taken one step further into cash flow: if revenue of 100 and original electricity costs of 12 are both annual figures, halving the electricity price saves 6 annually, but obtaining the low-cost source requires an additional investment of 10 at the outset. Temporarily excluding taxes, financing, maintenance differences and residual value, and assuming the savings arrive at each year-end for five consecutive years, discounted at 10%, the incremental project's net present value is approximately 12.74. If competitive price cuts pass all the savings to customers, the incremental cash retained by the service provider becomes zero, and the additional investment has a value of −10 under these assumptions. Both numbers are merely examples with clear boundaries; they are not used to value fusion-power projects before actual electricity prices, operating life and customer pricing have been validated.

At project level, the levelized cost of electricity also needs to be calculated: using the same discount rate and lifetime boundaries, divide the present value of construction, operation, fuel, maintenance, decommissioning and other costs by the present value of deliverable net electricity. This denominator must deduct internal consumption and outage effects; the instantaneous power of a reactor cannot substitute for annual electricity sales. Transmission and distribution, backup and data-center retrofit costs beyond the grid connection point must then be added to the customer's delivered cost. Even if a particular approach has cheap fuel, that does not mean the electricity customer's full bill approaches zero.

### F.4 Who Receives the Profit Matters as Much as Lower Costs

If cheap electricity is available in only a few locations, owners controlling power sources and grid-connection resources may retain some of the gains. If competitors can all obtain the same electricity price, cloud-service and API price cuts may pass the savings to customers. Industry output may therefore grow without supplier margins necessarily rising alongside it.

In the illustration above, if the price also falls from 100 to 94 and cost is 54, gross profit remains 40 and gross margin is approximately 42.6%. Customers obtain a lower price, while the service provider does not receive the full profit improvement in the earlier scenario. This does not mean price cuts must harm service providers: if usage, customer retention and the spreading of fixed costs improve, total profit may still increase. Volume, price and unit cost must be calculated together.

Fusion power may therefore relieve physical bottlenecks, but may also drive additional supply and another round of price competition. Its effect on AI valuations depends on whether the gains ultimately accrue to generators, cloud providers, application companies or end customers; it cannot uniformly be labeled positive or negative.

### F.5 An Energy Breakthrough Does Not Mean AGI Has Been Achieved

More and cheaper electricity can expand affordable training and inference budgets, but does not directly establish that models can consistently handle long tasks, recognize errors, respect permissions or act reliably in unfamiliar environments. Capability, reliability and economics are related but distinct variables, and should be validated separately.

Conversely, this also provides insufficient evidence to conclude that algorithms have hit a fixed ceiling or that usable data has been exhausted. Algorithmic improvements, better data quality, inference-time compute and task decomposition can all change how much electricity is needed to obtain a given capability. If computing efficiency improves substantially, additional electricity remains valuable, but its scarcity and the allocation of rents may change.

### F.6 Which Links Fusion and Equity Financing Each Change

If commercialized, fusion primarily changes available electricity, construction locations and service costs. Equity financing primarily changes the source of cash, debt pressure and the allocation of equity per share. Both may extend the time over which a project can be executed, but neither alone proves that its net present value is positive.

Equity financing is not sufficient evidence of "failure to earn a return on capital." If proceeds from new shares are invested in high-return projects, existing shareholders may gain per-share value despite dilution. If new funds merely sustain expansion without end-customer cash collection, an improved cash balance and value creation diverge. For Alphabet's actual financing status, see Section 2.8 of the circular-investment chapter. Planned capacity, securities issued and net proceeds received are checked separately; the full financial statements are not repeated here.

### F.7 Why the Year of the Next Bubble Cannot Be Fixed in Advance

A new technology may attract narratives and capital, but that is still insufficient to conclude that "2028–2029 will inevitably be the turn of the fusion bubble." Research should observe whether financing valuations, engineering milestones, customer payments, generation costs and available exit routes diverge, rather than impose a calendar on capital rotation.

Comparing fusion-company valuations requires current original financing documents and capital structures; IPO dates require formal filings and issuance arrangements, not technological milestones as substitutes. Even a genuine valuation cannot replace technological readiness, and even genuine engineering progress cannot guarantee public-market liquidity.

In terms of research coverage, Helion and CFS have the project materials listed in this chapter. TAE Technologies, Tokamak Energy and Pacific Fusion remain candidate approaches followed in the original report; company valuations, commissioning dates and IPO years that have not been rechecked for the current period are not carried forward. Before upgrading them to formal company research, obtain equipment configurations, independent measurements, engineering costs and customer contracts, rather than wait for a preset year of the "next bubble."

| Research subject | Information usable in this chapter | Decisive evidence still missing |
|---|---|---|
| Helion / Orion | Construction status, initial-operations target and design supply capacity on the company project page | Actual continuous net electricity output, commercial acceptance, cost and availability |
| CFS / SPARC, ARC | The experimental-gain target and first-power-plant plans disclosed separately by the company | Q boundaries, whole-plant net electricity, construction schedule, capital cost and electricity-sale terms |
| TAE, Tokamak Energy, Pacific Fusion | Retained as candidate approaches for verification; no current valuations or commissioning years entered | Original engineering materials, completed milestones and independent verification |

### F.8 Evidence Ledger for Follow-Up

| Evidence to record | Why it affects the judgment | Materials that cannot replace it |
|---|---|---|
| Verifiable continuous net electricity output, operating duration and outage records | Distinguishes a one-off physical achievement from an available power source | News headlines, rendered model images |
| Whole-plant capital cost, financing cost, maintenance and material-replacement costs | Enables calculation of levelized electricity cost and stress scenarios | Fuel cost alone or experimental energy gain |
| Grid-connection progress and actual deliverable location | Determines whether a specific data center can be served | Total national generation potential |
| Customer-contract prices, duration, minimum purchases and acceptance conditions | Shows who bears technology and delivery risk | Maximum MW announced in a contract |
| Changes in cloud-service prices, usage and gross profit | Determines how savings are allocated | A single electricity-price reduction percentage |
| Cash payback period for new AI assets | Tests whether power improvements translate into shareholder returns | The company's overall share price or new financing amount |

### F.9 What Would Change the Judgment

If a project completes commercial power-supply, reliability and cost acceptance early, the available-power scenario should be brought forward and the benefiting data centers recalculated, rather than adhering to the original timetable. If electricity has been delivered but connection and backup costs offset most savings, the nominal reduction in generation cost cannot be copied directly into cloud-service costs.

If cheap electricity significantly reduces the cost per successful task, expands end-customer payments, and generates incremental cash flow sufficient to cover construction and maintenance investment, the assessment of improved commercial capital recovery should be raised. If capacity expands quickly, price pass-through is even faster, and profits do not remain with suppliers, the distribution of industry-chain gains should be reassessed, rather than broadly marking down the value of the entire AI industry.

This chapter's conclusion is conditional: energy innovation can change the constraints on the AI industry, and capital markets can change the financing conditions for construction. Only when these changes ultimately enter sustainable cash flow do they change asset value. One cannot preemptively reject new evidence on the grounds that "the bubble must burst," or skip cash recovery on the grounds that "fusion is about to succeed."
