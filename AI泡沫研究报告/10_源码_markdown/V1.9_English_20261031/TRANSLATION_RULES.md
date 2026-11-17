# English translation rules

This is a complete, faithful English translation of the corrected Chinese V1.9 full report, not a new research edition or a summary. The observation cutoff stays 31 October 2026, Beijing time. Do not add research, forecasts, recommendations, certainty, or facts. Preserve source limitations, attribution, dates, conditional language, counterarguments and explicit unknowns. No outside translation service or network upload is authorized or needed.

## Files and structure

- Read the assigned files in `translation_inputs/` and write the same filenames into `parts/`. Do not edit the inputs, Chinese report, other groups' parts, builders or entrypoints.
- Translate every heading, paragraph, bullet, table cell, note, link label, chart caption, quote and research qualification. Do not abridge or replace long passages with summaries. Keep the original blank-line structure and one source line to one English line. Keep Markdown levels, table rows and columns, link destinations, image paths, HTML comments and code literals intact.
- Translate chapter titles as `Chapter 1: ...` through `Chapter 13: ...`; retain all subsection numbers exactly, including 3.4.9. Translate `附篇A` through `附篇F` as `Appendix A` through `Appendix F`. Translate chapter cross-references consistently (e.g. 第四章 -> Chapter 4). Original historical numbering and source page numbers stay historical.
- All URLs and image destinations must remain byte-identical to the assigned input. Translate link labels into useful English, keeping source identity and reporting period. Do not replace or shorten URLs.
- Preserve formulas, operators, signs, numeric precision and quantitative qualifications. A range, upper bound, commitment, guidance or hypothetical example must not become an observed result.
- Produce natural, direct English suitable for an investor research report. Do not imitate Chinese syntax word for word. Faithfulness takes precedence over rhetorical polish. Keep the source's first-person admissions of uncertainty and mistakes.

## Quantities and terminology

- Distinguish revenue recognized from cash collected, cash profit from adjusted earnings, bookings from revenue, ARR from period revenue, gross from net amounts, and commitments from drawdowns.
- Chinese units require correct conversion: 万 = 10,000; 亿 = 100,000,000; 万亿 = 1,000,000,000,000. Convert to natural English million/billion/trillion units without changing the amount. Existing `B`, `M`, dollar signs, percentages, dates and model version numbers should normally remain identical. Do not silently round.
- Record every numeric-token change caused by unit conversion or translation in the group's JSON ledger, with input filename, source line number (1-based), source excerpt, English excerpt and a short arithmetic explanation. An automated scan will flag all other numeric differences for independent review.
- 美元 = USD; 亿元 with a stated RMB context = RMB/CNY, never USD. If currency is unclear in the source, retain that ambiguity rather than inventing one. Use USD and RMB consistently.
- 短剧/微短剧 = microdrama (explain short-form episodic drama on first occurrence); 真人短剧 = live-action microdrama; AI主生成 = primarily AI-generated; AI辅助 = AI-assisted; 漫剧 = animated microdrama; 投流 = paid user acquisition or paid media placement according to context.
- 观看时长 = viewing time; 使用时长 = app usage time; 累计片长 = total running time of a title. Do not substitute one for another. Daily time per monthly user is not automatically a per-active-day measure or continuous session.
- 可用率 = usable-output rate / acceptance yield in video generation; 付费生成秒数 = paid generated seconds; 成片秒数 = seconds of finished footage; 重试 = retries; 重复播放 = repeat viewing (not repeated generation).
- 净工时节约 = net hours saved; 产能 = capacity; 避免招聘 = avoided hires; 岗位替代 = job displacement; 任务替代 = task automation; 现金节省 = cash savings. Keep each separate.
- 资本回收 = return/recovery of invested capital according to context, not automatically profitability; 利润真实性 = quality and substance of reported earnings; 循环投资 = circular financing/investment; 条件算例 = conditional illustration/scenario calculation; 反证 = disconfirming evidence; 单源 = single-source evidence; 转存件 = archived copy.
- Use established English company/product names already present in the source. Keep proper names and their legal entities distinct. When no English name is supported, use a cautious transliteration, optionally retain the original Chinese name in parentheses. Never invent an official corporate name.
- The author brand is `Daduizhang`; Chinese author identity is not to be expanded into a real personal name or employer.

## Handoff and checks

- Work one file at a time and save finished files promptly. Send a short progress note after each completed file so the parent can start validation.
- Before marking a file complete, compare all source lines against its translation, check there are no omitted table rows, and compare URL/image destination sequences and all numbered headings. Check currency/unit conversions yourself.
- Write a group ledger to `../../复审与版本记录/V1.9_English_20261031/translation_group_<a|b|c>.json` relative to this source folder (the parent will give the absolute path as well). Include completed files, source/output hashes, numeric changes, material terminology decisions, checks performed, and any unresolved problems. The parent will run independent mechanical checks and cross-review.
- No recursive delegation. Do not touch another group's files. If a factual/source issue is noticed, report it without silently correcting the Chinese research claim in English.
