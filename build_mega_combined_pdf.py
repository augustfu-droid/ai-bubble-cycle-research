"""把6+1份Markdown报告合并为完整百页大合集PDF
特性：
- 封面 / 免责声明 / 美观目录 / 章节扉页 / 正文
- 目录条目可点击跳转到对应章节
- 子小节自动生成锚点（## N.M / ### N.M）
- 正文 URL 引用自动可点击
- 每页大队长出品水印
"""
import sys
sys.path.insert(0, '/home/user/workspace')

import re
src = open("/home/user/workspace/build_pdfs.py", encoding='utf-8').read()
cut = src.find("# === 主报告 ===")
src_lib = src[:cut]
ns = {}
exec(src_lib, ns)

make_cover = ns['make_cover']
make_page_decorator = ns['make_page_decorator']
make_cover_decorator = ns['make_cover_decorator']
STYLES = ns['STYLES']
C = ns['C']

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, KeepTogether,
    Table, TableStyle, Image
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics

# ============== 通用 anchor 注入：扩展 parse_markdown 以支持锚点 ==============
# 复用 build_pdfs.py 中除 parse_markdown 之外的工具
process_inline_orig = ns['process_inline']
escape_xml = ns['escape_xml']
parse_table = ns['parse_table']
build_table = ns['build_table']
is_special_line = ns['is_special_line']

def _section_anchor(title_text):
    """从标题文字中提取章节编号，生成稳定锚点 id。
    规则：开头若匹配 N / N.M / N.M.K，返回 'sec_N' / 'sec_N_M' 等；
         若匹配 A.M / B.M 等附篇编号，返回 'sec_a_M' / 'sec_b_M'。
    """
    m = re.match(r'^([A-Za-z\d]+)(?:\.(\d+))?(?:\.(\d+))?\s', title_text + ' ')
    if m:
        parts = [m.group(1).lower()]
        if m.group(2): parts.append(m.group(2))
        if m.group(3): parts.append(m.group(3))
        return 'sec_' + '_'.join(parts)
    return None

# 重写 parse_markdown，新增章节锚点支持
def parse_markdown(md_text, image_map=None):
    image_map = image_map or {}
    lines = md_text.split('\n')
    story = []
    i = 0
    n = len(lines)
    in_code = False
    code_buf = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # 代码块
        if stripped.startswith('```'):
            if in_code:
                code_text = '\n'.join(code_buf)
                code_style = ParagraphStyle('Code', fontName='CN', fontSize=8.5, leading=12,
                                             textColor=C['text'], leftIndent=10,
                                             backColor=C['subtle_bg'], borderPadding=8,
                                             spaceAfter=10)
                story.append(Paragraph(escape_xml(code_text).replace('\n','<br/>'), code_style))
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # 图表占位符
        m = re.match(r'^\[\[CHART:([^\]]+)\]\](?:\s*(.+))?$', stripped)
        if m:
            chart_file = m.group(1)
            caption = m.group(2) or ''
            chart_path = Path(f"/home/user/workspace/charts/{chart_file}")
            if chart_path.exists():
                max_w = A4[0] - 2*1.8*cm
                from PIL import Image as PILImage
                pim = PILImage.open(chart_path)
                w, h = pim.size
                target_w = max_w * 0.92
                target_h = target_w * h / w
                if target_h > 15*cm:
                    target_h = 15*cm
                    target_w = target_h * w / h
                img = Image(str(chart_path), width=target_w, height=target_h)
                group = [Spacer(1, 4), img]
                if caption:
                    group.append(Paragraph(f'<i>{escape_xml(caption)}</i>', STYLES['caption']))
                else:
                    group.append(Spacer(1, 6))
                story.append(KeepTogether(group))
            i += 1
            continue

        # 表格
        if stripped.startswith('|') and i+1 < n and re.match(r'^\|[\s\-:|]+\|?\s*$', lines[i+1].strip()):
            rows, new_i = parse_table(lines, i)
            tbl = build_table(rows)
            if tbl:
                story.append(Spacer(1, 4))
                story.append(tbl)
                story.append(Spacer(1, 8))
            i = new_i
            continue

        # 一级标题 #
        if stripped.startswith('# '):
            title = stripped[2:]
            story.append(Paragraph(process_inline_orig(title), STYLES['h1']))
            story.append(HRFlowable(width="100%", thickness=1.2, color=C['header_bg'], spaceAfter=6))
            i += 1
            continue

        # 二级 ##
        if stripped.startswith('## '):
            title_text = stripped[3:]
            anchor = _section_anchor(title_text)
            anchor_tag = f'<a name="{anchor}"/>' if anchor else ''
            # 主章节扉页样式（第X篇/章/部分/节）
            if re.match(r'^第[一二三四五六七八九十百零]+[部分章篇节卷]', title_text):
                story.append(PageBreak())
                story.append(Spacer(1, 50))
                major_style = ParagraphStyle('MajorSection', fontName='CN-Bold', fontSize=24,
                                              leading=34, textColor=C['header_bg'],
                                              alignment=TA_LEFT, spaceAfter=10, keepWithNext=1)
                story.append(Paragraph(anchor_tag + process_inline_orig(title_text), major_style))
                story.append(HRFlowable(width="35%", thickness=2.5, color=C['accent'],
                                         spaceBefore=2, spaceAfter=18, hAlign='LEFT'))
            else:
                story.append(Paragraph(anchor_tag + process_inline_orig(title_text), STYLES['h2']))
            i += 1
            continue

        # 三级 ###
        if stripped.startswith('### '):
            title_text = stripped[4:]
            anchor = _section_anchor(title_text)
            anchor_tag = f'<a name="{anchor}"/>' if anchor else ''
            story.append(Paragraph(anchor_tag + process_inline_orig(title_text), STYLES['h3']))
            i += 1
            continue

        # 四级 ####
        if stripped.startswith('#### '):
            title_text = stripped[5:]
            anchor = _section_anchor(title_text)
            anchor_tag = f'<a name="{anchor}"/>' if anchor else ''
            story.append(Paragraph(anchor_tag + process_inline_orig(title_text), STYLES['h4']))
            i += 1
            continue

        # 水平线
        if stripped == '---':
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="100%", thickness=0.5, color=C['border'], spaceAfter=6))
            i += 1
            continue

        # 引用块
        if stripped.startswith('> '):
            quote_lines = []
            while i < n and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip().lstrip('>').strip())
                i += 1
            story.append(Paragraph(process_inline_orig(' '.join(quote_lines)), STYLES['quote']))
            continue

        # 无序列表
        if stripped.startswith('- ') or stripped.startswith('* '):
            story.append(Paragraph('• ' + process_inline_orig(stripped[2:]), STYLES['bullet']))
            i += 1
            continue

        # 有序列表
        m = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if m:
            story.append(Paragraph(f'{m.group(1)}. {process_inline_orig(m.group(2))}', STYLES['bullet']))
            i += 1
            continue

        # 空行
        if not stripped:
            i += 1
            continue

        # 普通段落
        para_lines = [stripped]
        i += 1
        while i < n and lines[i].strip() and not is_special_line(lines[i].strip()):
            para_lines.append(lines[i].strip())
            i += 1
        para_text = ' '.join(para_lines)
        story.append(Paragraph(process_inline_orig(para_text), STYLES['body']))

    return story

# ============== 样式 ==============
chapter_title_style = ParagraphStyle(
    'ChapterTitle', fontName='CN-Bold', fontSize=26, leading=34,
    textColor=C['primary'], alignment=TA_LEFT, spaceAfter=6
)
chapter_num_style = ParagraphStyle(
    'ChapterNum', fontName='CN', fontSize=10.5, leading=15,
    textColor=C['muted'], alignment=TA_LEFT, spaceAfter=3
)
chapter_sub_style = ParagraphStyle(
    'ChapterSub', fontName='CN', fontSize=12.5, leading=19,
    textColor=C['text'], alignment=TA_LEFT, spaceAfter=14
)

# 目录样式 — 三档：标题、一级、二级
toc_h_style = ParagraphStyle(
    'TOCH', fontName='CN-Bold', fontSize=24, leading=32,
    textColor=C['primary'], alignment=TA_LEFT, spaceAfter=4
)
toc_sub_style = ParagraphStyle(
    'TOCSub', fontName='CN', fontSize=10.5, leading=16,
    textColor=C['muted'], alignment=TA_LEFT, spaceAfter=14
)
toc_lvl1_label = ParagraphStyle(
    'TOCLvl1Label', fontName='CN-Bold', fontSize=10.5, leading=15,
    textColor=C['accent'], alignment=TA_LEFT, wordWrap='CJK',
)
toc_lvl1_title = ParagraphStyle(
    'TOCLvl1Title', fontName='CN-Bold', fontSize=12.5, leading=18,
    textColor=C['header_bg'], alignment=TA_LEFT, wordWrap='CJK',
)
toc_lvl1_desc = ParagraphStyle(
    'TOCLvl1Desc', fontName='CN', fontSize=9, leading=13,
    textColor=C['muted'], alignment=TA_LEFT, wordWrap='CJK',
)
toc_lvl2_num = ParagraphStyle(
    'TOCLvl2Num', fontName='CN', fontSize=9.5, leading=15,
    textColor=C['muted'], alignment=TA_LEFT,
)
toc_lvl2_title = ParagraphStyle(
    'TOCLvl2Title', fontName='CN', fontSize=10.5, leading=16,
    textColor=C['text'], alignment=TA_LEFT, wordWrap='CJK',
)

disclaimer_title_style = ParagraphStyle(
    'DisclaimerTitle', fontName='CN-Bold', fontSize=22, leading=30,
    textColor=HexColor('#A12C7B'), alignment=TA_CENTER, spaceAfter=20
)
disclaimer_body_style = ParagraphStyle(
    'DisclaimerBody', fontName='CN', fontSize=11, leading=20,
    textColor=C['text'], alignment=TA_LEFT, wordWrap='CJK', spaceAfter=8
)
disclaimer_emphasis_style = ParagraphStyle(
    'DisclaimerEmphasis', fontName='CN-Bold', fontSize=12, leading=20,
    textColor=HexColor('#A12C7B'), alignment=TA_LEFT, spaceAfter=8
)

def chapter_break(num, title, subtitle, anchor_id=None):
    """章节扉页：新页 + 顶部小间距，并在标题位置放置内部锚点供目录跳转"""
    anchor_tag = f'<a name="{anchor_id}"/>' if anchor_id else ''
    header_block = KeepTogether([
        Spacer(1, 12),
        Paragraph(num, chapter_num_style),
        Paragraph(anchor_tag + title, chapter_title_style),
        HRFlowable(width="30%", thickness=2.5, color=C['primary'],
                    spaceBefore=2, spaceAfter=6, hAlign='LEFT'),
        Paragraph(subtitle, chapter_sub_style),
    ])
    return [PageBreak(), header_block]

# Emoji → CJK 字体可渲染符号的替换表（思源宋体不含 emoji 字形，会出现空盒）
EMOJI_REPLACEMENTS = {
    '✅': '【已核验】',
    '⚠️ 部分核验': '【部分核验】',
    '⚠️': '【注】',
    '⚠': '【注】',
    '❌': '【未核验】',
    '🟢': '●',
    '🟡': '◑',
    '🔴': '■',
    '🟠': '◆',
}

def strip_unrenderable_emoji(text):
    """把 CJK 字体不支持的 emoji 替换为可渲染的语义等价符号。"""
    for k, v in EMOJI_REPLACEMENTS.items():
        text = text.replace(k, v)
    return text

def load_with_charts(md_path, charts_to_inject):
    md_text = Path(md_path).read_text(encoding='utf-8')
    if charts_to_inject:
        for anchor, chart, caption in charts_to_inject:
            placeholder = f"\n\n[[CHART:{chart}]] {caption}\n\n"
            if anchor in md_text:
                idx = md_text.find(anchor)
                line_end = md_text.find('\n', idx)
                if line_end == -1: line_end = len(md_text)
                next_block = md_text.find('\n\n', line_end)
                if next_block == -1: next_block = len(md_text)
                md_text = md_text[:next_block] + placeholder + md_text[next_block:]
    return strip_unrenderable_emoji(md_text)

# ============== 免责声明页 ==============
def build_disclaimer():
    flows = [Spacer(1, 14)]
    flows.append(Paragraph('<a name="disclaimer"/>【重要免责声明】', disclaimer_title_style))
    flows.append(HRFlowable(width="60%", thickness=2, color=HexColor('#A12C7B'),
                             spaceBefore=2, spaceAfter=14, hAlign='CENTER'))
    flows.append(Paragraph("<b>关于报告性质</b>", disclaimer_emphasis_style))
    flows.append(Paragraph(
        "本报告系报告作者大队长基于公开信息独立研究与分析所形成的个人观点，"
        "<b>仅代表大队长个人观点，不代表所在机构观点，亦不构成所在机构的任何官方立场</b>。"
        "本报告所有内容仅供参考与学术交流，<b>不构成任何投资建议、要约或邀约</b>。",
        disclaimer_body_style))
    flows.append(Paragraph("<b>关于投资风险</b>", disclaimer_emphasis_style))
    flows.append(Paragraph(
        "投资有风险，入市需谨慎。本报告基于截至2026年5月的公开数据撰写，市场状况瞬息万变，"
        "数据准确性与时效性可能因发布时点滞后而变化。报告中提及的所有目标价位、概率估算、"
        "情景预测均存在重大不确定性，<b>历史先例不保证未来表现</b>，过往规律不必然在本周期重演。",
        disclaimer_body_style))
    flows.append(Paragraph("<b>关于做空类工具的特别风险警示</b>", disclaimer_emphasis_style))
    flows.append(Paragraph(
        "本报告第六、第七章列举了部分做空类与对冲类工具仅作风险教育对照。"
        "<b>做空类工具风险极高</b>，主要风险包括但不限于以下四项：",
        disclaimer_body_style))
    risk_item_style = ParagraphStyle(
        'RiskItem', fontName='CN', fontSize=11, leading=19,
        textColor=C['text'], alignment=TA_LEFT, spaceAfter=8,
        leftIndent=14, wordWrap='CJK'
    )
    risk_items = [
        "<b>一、理论亏损无上限</b>——标的资产价格可无限上涨，导致空头损失超过本金；在极端轧空行情中，产生的亏损可导致账户爆仓。",
        "<b>二、杠杆与衍生品复杂性</b>——L&amp;I ETF、期权、期货存在时间衰减、保证金追缴、强制平仓等风险，<b>可能在短时间内导致全部本金损失甚至倒欠经纪商债务</b>。",
        "<b>三、择时极难</b>——市场可在非理性状态下持续超出预期，做空者可能在最终方向正确前先因保证金不足被强制出局，"
        "\u201c看对了方向但拿不到钱\u201d是做空最常见的失败原因。",
        "<b>四、政策与流动性风险</b>——监管层可能临时禁止做空、调整保证金或暂停交易，短期内可能造成无法平仓的尾部风险。",
    ]
    for item in risk_items:
        flows.append(Paragraph(item, risk_item_style))
    flows.append(Paragraph(
        "<b>读者在动用任何做空类工具前应充分理解相关风险，咨询持牌专业人士，"
        "并仅以可承受全部损失的资金参与。本报告作者及所在机构对读者据此进行的"
        "任何交易决策与由此产生的盈亏不承担任何责任。</b>",
        disclaimer_emphasis_style))
    flows.append(Paragraph("<b>关于版权与转载</b>", disclaimer_emphasis_style))
    flows.append(Paragraph(
        "本报告版权归报告作者大队长所有。引用请注明来源，未经书面授权，不得用于任何商业用途。"
        "联系邮箱：fqsx@mail.ustc.edu.cn",
        disclaimer_body_style))
    return flows

# ============== 7篇章节配置（含锚点） ==============
CHAPTERS = [
    {
        "num": "第一篇", "anchor": "chap_1",
        "title": "核心结论总览",
        "subtitle": "美股巨头利润真实性 · 资本循环网络 · AI 变现 · AGI 时间表 · 国际格局 · 延迟情景下的放大机制",
        "md": "/home/user/workspace/AI周期与泡沫深度研究报告_全景渲染.md",
        "charts": [
            ("### 1.2 \"三层利润水分\"详解", "04_anthropic_revaluation.png",
             "图1-1：Q1 2026 Alphabet (287亿税后) + Amazon (168亿税前) 来自 Anthropic 股权重估"),
            ("**水分三：Capex已经吞噬自由现金流**", "01_capex.png",
             "图1-2：四大云厂商资本开支2023-2026增长近5倍"),
            ("| Amazon | 835亿", "02_capex_ratio.png",
             "图1-3：Capex已开始超过运营现金流"),
            ("### 1.3 英伟达的\"真客户\"分类", "15_nvidia_customers.png",
             "图1-4：英伟达数据中心收入客户结构高度集中"),
            ("### 1.4 估值层面：现在贵不贵？", "12_cape_history.png",
             "图1-5：标普500 CAPE席勒PE历史，155年来仅2000年和现在超过40"),
            ("### 2.2 核心循环交易明细", "05_circular_deals.png",
             "图1-6：AI产业循环投资网络主要交易金额"),
            ("### 2.5 与2000年朗讯/北电对比", "06_nvidia_vs_lucent.png",
             "图1-7：英伟达 vs 朗讯供应商融资规模与现金流对比"),
            ("### 3.1 14个变现领域规模总览", "07_monetization.png",
             "图1-8：AI变现版图——云和广告占据绝对主导"),
            ("### 3.3 模型层直接变现", "08_anthropic_growth.png",
             "图1-9：Anthropic ARR 80倍年增长，模型层最强需求信号"),
            ("### 3.4 编程市场天花板分析", "09_coding_tam.png",
             "图1-10：编程市场TAM悖论——Cursor估值远超传统市场上限"),
            ("### 4.1 主要预测者立场", "10_agi_predictions.png",
             "图1-11：AGI到来时间预测分布"),
            ("**主要基准饱和速度", "11_benchmarks.png",
             "图1-12：主要AI基准测试一年内被高速饱和"),
            ("### 5.1 中美AI差距", "13_us_china_gap.png",
             "图1-13：中美顶级模型 Arena Elo 差距从 15% 收窄至 2.7%"),
            ("**震中二：OpenAI-甲骨文", "14_oracle_cds.png",
             "图1-14：甲骨文5年期CDS利差扩大至2008金融危机以来新高"),
            ("### 1.3 亚马逊（Amazon）", "03_amazon_fcf.png",
             "图1-15：Amazon TTM自由现金流暴跌95%"),
        ]
    },
    {
        "num": "第二篇", "anchor": "chap_2",
        "title": "AI巨头真实利润拆解",
        "subtitle": "真金白银 vs. 会计游戏 —— 五大巨头利润可信度评级",
        "md": "/home/user/workspace/research/01_profit_breakdown.md",
        "charts": [
            ("## 第二章：资本开支吞噬现金流", "01_capex.png", "图2-1：四大云厂商Capex爆发"),
            ("### 2.2 Capex占运营现金流比率", "02_capex_ratio.png", "图2-2：Capex占运营现金流比例"),
            ("### 2.3 自由现金流变化趋势", "03_amazon_fcf.png", "图2-3：Amazon TTM自由现金流暴跌95%"),
            ("## 第四章:英伟达客户集中度风险", "15_nvidia_customers.png", "图2-4：英伟达数据中心收入客户结构"),
            ("### 5.2 标普500 CAPE比率", "12_cape_history.png", "图2-5：CAPE席勒PE 155年历史"),
            ("### 1.2 Alphabet（Google）", "04_anthropic_revaluation.png", "图2-6：Q1 2026利润中Anthropic股权重估占比"),
        ]
    },
    {
        "num": "第三篇", "anchor": "chap_3",
        "title": "AI产业循环投资网络",
        "subtitle": "名义口径约 6100 亿、四类不同性质安排 · 交易性质分层 · 三个风险集中点",
        "md": "/home/user/workspace/research/02_circular_investment.md",
        "charts": [
            ("## 一、循环投资关系总览", "05_circular_deals.png", "图3-1：主要循环交易金额"),
            ("## 四、历史类比：2000年电信泡沫的镜像", "06_nvidia_vs_lucent.png", "图3-2：英伟达 vs 朗讯对比"),
        ]
    },
    {
        "num": "第四篇", "anchor": "chap_4",
        "title": "AI变现版图与编程市场TAM",
        "subtitle": "云、广告、订阅、编程 —— 谁在真正赚钱？",
        "md": "/home/user/workspace/research/03_monetization_and_coding.md",
        "charts": [
            ("## Part A：AI变现领域全景图", "07_monetization.png", "图4-1：AI变现各领域规模总览"),
            ("**Anthropic / Claude**", "08_anthropic_growth.png", "图4-2：Anthropic ARR 80倍年增长曲线"),
            ("**TAM测算（核心结论）**", "09_coding_tam.png", "图4-3：编程TAM场景分析"),
        ]
    },
    {
        "num": "第五篇", "anchor": "chap_5",
        "title": "AGI预测与国际格局重塑",
        "subtitle": "谁会到达AGI？谁在主导新秩序？",
        "md": "/home/user/workspace/research/04_agi_and_geopolitics.md",
        "charts": [
            ("### AGI时间预测汇总表", "10_agi_predictions.png", "图5-1：各家AGI到来时间预测分布"),
            ("### 三、关键基准测试进展曲线", "11_benchmarks.png", "图5-2：主要AI基准一年内饱和速度"),
            ("## Part B：国际格局重塑", "13_us_china_gap.png", "图5-3：中美前沿模型差距收窄"),
        ]
    },
    {
        "num": "第六篇", "anchor": "chap_6",
        "title": "AI泡沫崩盘剧本",
        "subtitle": "六维拆解 · 三阶段时间表 · 冲击大但不是末日级",
        "md": "/home/user/workspace/research/05_collapse_scenario.md",
        "charts": [
            ("## 一、体量维度：超过历史上任何一次科技泡沫", "16_bubble_scale_radar.png",
             "图6-1：泡沫体量五维对比（2000 vs 2026）"),
            ("## 二、传导链条：六条同步触发的传染路径", "17_transmission_paths.png",
             "图6-2：六条同步触发的传染路径"),
            ("## 三、三阶段时间表", "18_three_phase_timeline.png",
             "图6-3：三阶段崩盘时间表（次情景）"),
            ("### 6.2 辅助监测指标仪表盘", "19_signal_dashboard.png",
             "图6-4：八大监测信号仪表盘"),
        ]
    },
    {
        "num": "第七篇", "anchor": "chap_7",
        "title": "延迟情景下的放大机制（核心观点）",
        "subtitle": "为什么 AI 泡沫可能延后至 2027-2028 以更大幅度方式爆发",
        "md": "/home/user/workspace/research/06_delay_amplifies.md",
        "charts": [
            ("## 一、历史先例:延迟救市如何放大泡沫", "21_historical_precedents.png",
             "图7-1：三次延迟救市的放大代价（LTCM/次贷/日本）"),
            ("## 二、当前延迟动力", "23_sovereign_ai_ammunition.png",
             "图7-2：主权AI弹药盘点 · 万亿级流动性尚未充分部署"),
            ("## 三、Capex累积上限", "22_capex_cumulative.png",
             "图7-3：四大云厂商Capex累积曲线 · 2026-2028超4万亿临界点"),
            ("## 五、破裂幅度估算", "20_scenario_comparison.png",
             "图7-4：三情景概率与破裂幅度对比"),
            ("## 六点五、能源即新硬约束:2027-2028年的物理极限", "01_capex.png",
             "图7-5：能源变压器与并网期3-5年 · 推理占AI能耗80-90%"),
            ("## 八、中国投资者可触达的做空类工具画像与结构性风险（仅作风险教育）", "24_short_tools_risk_matrix.png",
             "图7-6：中国投资者做空类工具风险-收益矩阵【风险警示】"),
        ]
    },
    {
        "num": "附篇 A", "anchor": "chap_8",
        "title": "证据基础、反方论证与方法论",
        "subtitle": "核心事实口径表 · 五个反方场景 · 概率生成机制 · 历史类比边界",
        "md": "/home/user/workspace/research/07_methodology_and_counterview.md",
        "charts": []
    },
    {
        "num": "附篇 B", "anchor": "chap_9",
        "title": "大湾区跨境理财通（南向通 2.0）客户实操指南",
        "subtitle": "300 万额度路径 · 三阶段动作 · 纳指 15 年回本档案",
        "md": "/home/user/workspace/research/08_southbound_playbook.md",
        "charts": []
    },
    {
        "num": "附篇 C", "anchor": "chap_10",
        "title": "页岩油-AI 同构性测试",
        "subtitle": "八点同构 · 三点差异 · 最终赢家映射 · 时机坐标",
        "md": "/home/user/workspace/research/09_shale_ai_analogy.md",
        "charts": []
    },
    {
        "num": "附篇 D", "anchor": "chap_appd",
        "title": "伯克希尔抄底神话的祛魅【V0.8.1 新增】",
        "subtitle": "与 2008-2022 抽底范本五项对照 · Abel 仓位轨迹 · 七巨头估值最便宜 · 对 AI 板块整体利空",
        "md": "/home/user/workspace/附篇D_伯克希尔抄底神话的祛魅.md",
        "charts": []
    },
    {
        "num": "附篇 E", "anchor": "chap_appe",
        "title": "54 项核心数据事实审计表【V0.7 新增 · V1.2 顺延】",
        "subtitle": "NVDA 营收 · 云商 Capex/FCF · 资本循环网络 · 监管处罚 · 估值与信用利差五大类别审计（V1.2 新增 SpaceX/NVDA 发债 + 大摩 $2T 表外 + 信贷脉冲 8 项）",
        "md": "/home/user/workspace/AI周期与泡沫_事实审计表_V1.2.md",
        "charts": []
    },
    {
        "num": "附篇 F", "anchor": "chap_appf",
        "title": "续命假设的证伪——聚变能否拯救 AI 叙事【V0.8 扩充 · V0.8.1 顺延】",
        "subtitle": "四层证伪 · 股权融资续命悖论（V0.8 新增）· Alphabet $80B 错配· 2029-2031 聚变 Watchlist",
        "md": "/home/user/workspace/附篇F_续命假设的证伪_聚变能否拯救AI叙事.md",
        "charts": []
    },
]

# ============== 目录数据结构 ==============
# 每项 (level, label_main, label_desc_or_None, anchor)
# level 0=一级章节, 1=二级小节
TOC_ITEMS = [
    (0, "免责声明", "个人观点声明 · 投资风险提示 · 做空类工具风险警示", "disclaimer"),
    (0, "投委一页纸（IC One-Pager）【V0.7 新增】",
     "一句话核心 thesis · 三证据 · 三风险 · 三证伪条件 · 两监测窗口 · 我可能错在哪里", "ic_onepager"),
    (0, "第一篇　核心结论总览",
     "美股巨头利润真实性 · 资本循环网络 · AGI 时间表 · 国际格局 · 延迟情景下的放大机制", "chap_1"),
    (1, "1.1", "美股AI巨头利润真实性五级评分", "sec_1_1"),
    (1, "1.2", "名义口径约 6100 亿资本循环网络", "sec_1_2"),
    (1, "1.3", "AI变现五大领域", "sec_1_3"),
    (1, "1.4", "AGI 2027-2030 时间窗口", "sec_1_4"),
    (1, "1.5", "六大历史泡沫横向对比表【V0.6.0 扩写】", "sec_1_5"),
    (1, "1.5.1", "横向对比表（核心矩阵）", "sec_1_5_1"),
    (1, "1.5.2", "案例一 · 南海泡沫（1720）—— 世界上第一个现代金融泡沫", "sec_1_5_2"),
    (1, "1.5.3", "案例二 · 英国铁路狂热（1845-1847）—— 第一次技术泡沫", "sec_1_5_3"),
    (1, "1.5.4", "案例三 · 1929 大崩盘 —— 杠杆如何毁灭一切", "sec_1_5_4"),
    (1, "1.5.5", "案例四 · 日本泡沫经济（1986-1991）—— 泡沫后最漫长的冬天", "sec_1_5_5"),
    (1, "1.5.6", "案例五 · 互联网泡沫（1995-2002）—— 最接近 AI 泡沫的历史蓝本", "sec_1_5_6"),
    (1, "1.5.7", "案例六 · 次贷危机（2004-2009）—— 杠杆的倍增破坏力", "sec_1_5_7"),
    (1, "1.5.8", "八维度横向对比扩展矩阵", "sec_1_5_8"),
    (1, "1.5.9", "泡沫破裂的三种动力学模式", "sec_1_5_9"),
    (1, "1.5.10", "AI 与互联网 2000 的关键差异", "sec_1_5_10"),
    (1, "1.5.11", "AI 与铁路 1846 的相似之处（隐藏镜像）", "sec_1_5_11"),
    (1, "1.6", "延迟情景下的放大机制（核心观点）", "sec_1_6"),
    (1, "1.7", "反方路径表：五条证伪路径【V0.7 新增】", "sec_1_7"),
    (0, "第二篇　AI巨头真实利润拆解",
     "Anthropic股权重估 · GPU折旧政策套利 · Capex吞噬FCF · 英伟达客户集中度", "chap_2"),
    (0, "第三篇　AI产业循环融资网络",
     "交易性质分层 · 三个风险集中点 · 朗讯历史对比", "chap_3"),
    (0, "第四篇　AI变现版图与编程市场TAM",
     "14个变现领域规模 · Anthropic ARR 80倍增长 · 编程TAM 131亿悖论", "chap_4"),
    (0, "第五篇　AGI预测与国际格局重塑",
     "AGI 2027-2030 中位预测 · 基准饱和速度 · 顶级模型 Arena Elo 2.7% · 防务AI · 能源核电", "chap_5"),
    (0, "第六篇　AI泡沫崩盘剧本",
     "情景框架升级 · 六维拆解 · 三阶段时间表 · 冲击大但不是末日级", "chap_6"),
    (1, "6.1", "情景框架升级声明", "sec_6_1"),
    (1, "6.2", "体量维度：CAPE/巴菲特/Mag 7", "sec_6_2"),
    (1, "6.3", "六条传染路径", "sec_6_3"),
    (1, "6.4", "三阶段时间表", "sec_6_4"),
    (1, "6.5", "与2000和2008的关键不同", "sec_6_5"),
    (1, "6.6", "三大触发信号 + 八指标仪表盘", "sec_6_6"),
    (1, "6.7", "两年滚动决策日历（季度检查清单）", "sec_6_7"),
    (1, "6.8", "跨境券商监管处罚—2026/05/22 证监会重大监管事件【V0.6.1 新增】", "sec_6_8"),
    (0, "第七篇　延迟情景下的放大机制（核心观点）",
     "历史先例 · 延迟动力 · Capex 累积 · AGI 叙事 · 破裂幅度 · 中国投资者做空类工具与风险", "chap_7"),
    (1, "7.1", "历史先例：LTCM / 次贷 / 日本BIS", "sec_7_1"),
    (1, "7.2", "当前延迟动力", "sec_7_2"),
    (1, "7.3", "Capex累积上限", "sec_7_3"),
    (1, "7.4", "AGI叙事自我强化", "sec_7_4"),
    (1, "7.5", "破裂幅度估算", "sec_7_5"),
    (1, "7.6", "预警信号", "sec_7_6"),
    (1, "7.7", "中国投资者含义 · 能源硬约束", "sec_7_7"),
    (1, "7.8", "做空类工具画像与风险警示", "sec_7_8"),
    (0, "末篇　综合结论 6 灯——AI 泡沫现状评估",
     "三红两黄一绿·均衡评分·最终综合判断【V0.6.0 新增·组件 9】", "sec_8_1"),
    (1, "8.1", "综合结论 6 灯评分表", "sec_8_1"),
    (1, "8.2", "综合判断", "sec_8_2"),
    (0, "附篇 A　证据基础、反方论证与方法论",
     "核心事实口径表 · 五个反方场景 · 概率生成机制 · 历史类比边界", "chap_8"),
    (1, "A.1", "证据基础：核心事实口径表", "sec_a_1"),
    (1, "A.2", "反方场景：如果本报告是错的", "sec_a_2"),
    (1, "A.3", "概率与跌幅生成方法论", "sec_a_3"),
    (1, "A.4", "历史类比的边界", "sec_a_4"),
    (1, "A.5", "三栏制：本报告判断可信度自评", "sec_a_5"),
    (0, "附篇 B　大湾区跨境理财通（南向通 2.0）客户实操指南",
     "300 万额度路径 · 三阶段实操 · 纳指 15 年回本档案", "chap_9"),
    (1, "B.1", "通道定位与硬约束", "sec_b_1"),
    (1, "B.2", "三阶段实操路径", "sec_b_2"),
    (1, "B.2.4", "A 股场内 QDII 溢价崩塌窗口（并行路径）", "sec_b_2_4"),
    (1, "B.3", "美股泡沫后反弹路径历史档案", "sec_b_3"),
    (1, "B.4", "大湾区跨境理财通客户视角下的具体推论", "sec_b_4"),
    (1, "B.5", "必要的合规边界与风险提示", "sec_b_5"),
    (1, "B.6", "信源说明", "sec_b_6"),
    (0, "附篇 C　页岩油-AI 同构性测试",
     "八点同构 · 三点差异 · 赢家映射 · 时机坐标", "chap_10"),
    (1, "C.1", "页岩油革命的完整叙事回顾", "sec_c_1"),
    (1, "C.2", "八点同构性测试", "sec_c_2"),
    (1, "C.3", "三个关键差异点", "sec_c_3"),
    (1, "C.4", "最终赢家映射表", "sec_c_4"),
    (1, "C.5", "时机判断：AI 在页岩油坐标上的位置", "sec_c_5"),
    (1, "C.6", "与本报告其他章节的接口", "sec_c_6"),
    (1, "C.7", "信源说明与方法论局限", "sec_c_7"),
    (0, "附篇 D　伯克希尔抄底神话的祛魅【V0.8.1 新增】",
     "与 2008-2022 抽底范本五项对照 · Abel 仓位轨迹 · 七巨头估值最便宜 · 对 AI 板块整体利空", "chap_appd"),
    (1, "D.1", "表面悖论：抄底之神为何参与顶部融资", "sec_d_1"),
    (1, "D.2", "历史抄底范本：四次教科书交易的共同特征", "sec_d_2"),
    (1, "D.3", "三个关键事实，重新定义这笔交易", "sec_d_3"),
    (1, "D.4", "那么这到底是利好还是利空——分两层", "sec_d_4"),
    (1, "D.5", "一个更尖锐的解读：阿贝尔 implicitly 押注七巨头分化", "sec_d_5"),
    (1, "D.6", "一句话结论", "sec_d_6"),
    (1, "D.7", "我可能错在哪里【V0.8.1 自我审视】", "sec_d_7"),
    (1, "D.8", "信源清单【附篇 D】", "sec_d_8"),
    (0, "附篇 E　27 项核心数据事实审计表【V0.7 新增 · V0.8.1 顺延】",
     "NVDA 营收 · 云商 Capex/FCF · 资本循环网络 · 监管处罚 · 估值与信用利差五大类别审计", "chap_appe"),
    (1, "E.1", "Nvidia 营收与回购（5 项）", "sec_e_1"),
    (1, "E.2", "Hyperscaler Capex 与 FCF（4 项）", "sec_e_2"),
    (1, "E.3", "AI 资本循环网络（7 项·V0.8 新增 Alphabet $80B 4 项）", "sec_e_3"),
    (1, "E.4", "监管处罚与跨境合规（4 项）", "sec_e_4"),
    (1, "E.5", "估值水位与信用利差（4 项）", "sec_e_5"),
    (0, "附篇 F　续命假设的证伪——聚变能否拯救 AI 叙事【V0.8 扩充 · V0.8.1 顺延】",
     "四层证伪 · 股权融资续命悖论（V0.8 新增）· Alphabet $80B 错配· 2029-2031 聚变 Watchlist", "chap_appf"),
    (1, "F.1", "短答与结构", "sec_f_1"),
    (1, "F.2", "第一层证伪——时间错配：聚变救不了 2026-2028 的 AI 折旧周期", "sec_f_2"),
    (1, "F.3", "第二层证伪——经济性：即使聚变如期到来，仍不解 AI 核心矛盾", "sec_f_3"),
    (1, "F.4", "第三层证伪——聚变 ≠ AGI：因果链断开", "sec_f_4"),
    (1, "F.5", "第四层观察——聚变可能成为泡沫破裂后的下一个故事", "sec_f_5"),
    (1, "F.6", "股权融资续命的悖论——以 Alphabet $80B 事件为锚【V0.8 新增】", "sec_f_6"),
    (1, "F.7", "对主报告框架的影响——零修改", "sec_f_7"),
    (1, "F.8", "长尾观察——2029-2031 聚变标的研究 Watchlist", "sec_f_8"),
    (1, "F.9", "我可能错在哪里【V0.8 扩充·附篇 F 自我审视】", "sec_f_9"),
    (1, "F.10", "信源清单【附篇 F】", "sec_f_10"),
]

# 预扫描所有章节 markdown，识别实际存在的 sec_X_Y 锚点
def _scan_anchors():
    found = set()
    for ch in CHAPTERS:
        text = Path(ch["md"]).read_text(encoding='utf-8')
        # 提取所有 ## / ### / #### 标题
        for line in text.split('\n'):
            s = line.strip()
            if s.startswith('## ') or s.startswith('### ') or s.startswith('#### '):
                title = s.lstrip('#').strip()
                aid = _section_anchor(title)
                if aid:
                    found.add(aid)
        # 主章节锚点总是存在
        found.add(ch["anchor"])
    found.add("disclaimer")
    return found

_VALID_ANCHORS = _scan_anchors()

def _safe_anchor(aid, fallback):
    return aid if aid in _VALID_ANCHORS else fallback

def _hex(color_key):
    """返回带 # 前缀的颜色字符串供 <link color=...> 使用"""
    h = C[color_key].hexval()  # 例如 '0x20808d'
    return '#' + h[2:].lower()

# ============== 目录页（表格化、可点击） ==============
def build_toc():
    flows = []
    flows.append(Spacer(1, 18))
    flows.append(Paragraph("目　录", toc_h_style))
    flows.append(HRFlowable(width="100%", thickness=2, color=C['primary'],
                            spaceBefore=2, spaceAfter=4))
    flows.append(Paragraph("点击任意条目可跳转到对应章节", toc_sub_style))

    # 构建条目：用表格控制对齐
    rows = []
    # 用上一个一级章节作为二级锚点的 fallback
    last_chap_anchor = "chap_1"
    for level, main, desc, anchor in TOC_ITEMS:
        if level == 0 and anchor.startswith('chap_'):
            last_chap_anchor = anchor
        anchor = _safe_anchor(anchor, last_chap_anchor)
        if level == 0:
            # 一级：左侧色块编号 + 右侧标题与描述
            # 分离编号与标题名（按全角空格）
            if '　' in main:
                num_part, title_part = main.split('　', 1)
            else:
                num_part, title_part = '', main
            num_para = Paragraph(
                f'<link href="#{anchor}" color="{_hex("accent")}">{num_part}</link>'
                if num_part else '',
                toc_lvl1_label)
            title_para = Paragraph(
                f'<link href="#{anchor}" color="{_hex("header_bg")}">{title_part}</link>',
                toc_lvl1_title)
            desc_para = Paragraph(
                f'<link href="#{anchor}" color="{_hex("muted")}">{desc}</link>'
                if desc else '',
                toc_lvl1_desc)
            from reportlab.platypus import Table as _T
            inner = _T(
                [[title_para], [desc_para]] if desc else [[title_para]],
                colWidths=[14.4*cm],
            )
            inner.setStyle(TableStyle([
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
            rows.append([num_para, inner])
        else:
            # 二级：缩进的小行
            num_para = Paragraph(
                f'<link href="#{anchor}" color="{_hex("muted")}">　　{main}</link>',
                toc_lvl2_num)
            title_para = Paragraph(
                f'<link href="#{anchor}" color="{_hex("text")}">{desc}</link>',
                toc_lvl2_title)
            rows.append([num_para, title_para])

    tbl = Table(rows, colWidths=[2.4*cm, 14.4*cm])
    # 给每行加分隔线、一级行加底色
    styles = [
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]
    for ridx, (level, *_rest) in enumerate(TOC_ITEMS):
        if level == 0:
            styles.append(('BACKGROUND', (0,ridx), (-1,ridx), HexColor('#F2F8F9')))
            styles.append(('LINEABOVE', (0,ridx), (-1,ridx), 0.7, C['border']))
            styles.append(('TOPPADDING', (0,ridx), (-1,ridx), 7))
            styles.append(('BOTTOMPADDING', (0,ridx), (-1,ridx), 7))
        else:
            styles.append(('LINEBELOW', (1,ridx), (-1,ridx), 0.3, HexColor('#EAEAEA')))
    tbl.setStyle(TableStyle(styles))
    flows.append(tbl)
    return flows

# ============== 构建 ==============
OUT = Path("/home/user/workspace/pdfs/2026年AI泡沫研究 · 全景版.pdf")
OUT.parent.mkdir(exist_ok=True)

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=2*cm, bottomMargin=1.8*cm,
    title="2026年AI泡沫研究 · 全景版",
    author="大队长",
    subject="AI 泡沫研究 · 延迟情景下的放大机制（核心观点）",
    keywords="AI泡沫,延迟情景放大,AGI,做空类工具风险教育,大队长",
)

story = []

# 封面
story += make_cover(
    title="2026年AI泡沫研究 · 全景版",
    subtitle="2026年AI资本周期个人研究：泡沫、真实变现与风险监测<br/>大队长个人深度研究笔记 · 基于公开信息 · 不构成投资建议<br/>V1.2 · 2026/06/22 公开发布版 · 全景版（投委一页纸 + V1.1/V1.2 数据快照页（SpaceX/NVDA 集体发债 + 大摩 $2T 表外 + 信贷脉冲）+ 七篇正文（含《分项 1§7.4 OBBBA 立法反转·光模块抢装互证》）+ 6 灯末篇 + 方法论附篇 A + 理财通附篇 B + 页岩油同构附篇 C + 伯克希尔祛魅附篇 D + 事实审计附篇 E（54 项）+ 续命假设证伪附篇 F）",
    meta_lines=[
        "美股巨头真实盈利 · 循环投资网络 · AGI时间表 · 国际格局",
        "压力测试情景 · 延迟情景下的放大机制 · 中国投资者做空类工具画像",
        "",
        "报告时间：2026年5月25日 · 版本：V1.2 · 2026/06/22 公开发布版",
        "数据基准：2025财年报告 + 2026 Q1 季报 + V1.0/V1.1/V1.2 增量事件（OpenAI/Anthropic S-1 · SpaceX 上市 + 发债 · NVDA $250 亿首发 · 大摩 $2T 表外承诺 · 信贷脉冲 +$8000 亿）；截至 2026/06/23 公开信源",
        "数据信源：200+ 独立信源 · 92+ 内联引用链接",
        "",
        "报告作者：大队长",
        "联系邮箱：fqsx@mail.ustc.edu.cn",
        "",
        "本报告仅代表个人观点 · 不构成投资建议 · 做空类工具风险极高",
    ]
)

# 作者后记页（V0.4.1 起移至全报告末尾，作为"作者后记"，不再做开篇题词页）
def build_author_postscript():
    flows = [PageBreak()]
    flows.append(Spacer(1, 3.5*cm))
    KAI = 'CN-Kai' if 'CN-Kai' in pdfmetrics.getRegisteredFontNames() else 'CN'
    DED_COLOR = HexColor('#1F2937')
    DED_SIZE = 14
    DED_LEAD = 28
    title_style = ParagraphStyle(
        'PSTitle', fontName=KAI, fontSize=DED_SIZE, leading=DED_LEAD,
        textColor=DED_COLOR, alignment=TA_CENTER, spaceAfter=18,
    )
    line_style = ParagraphStyle(
        'PSLine', fontName=KAI, fontSize=DED_SIZE, leading=DED_LEAD,
        textColor=DED_COLOR, alignment=TA_CENTER, spaceAfter=2,
    )
    emph_style = ParagraphStyle(
        'PSEmph', fontName=KAI, fontSize=DED_SIZE, leading=DED_LEAD,
        textColor=DED_COLOR, alignment=TA_CENTER, spaceAfter=2,
    )
    sign_style = ParagraphStyle(
        'PSSign', fontName=KAI, fontSize=DED_SIZE, leading=DED_LEAD,
        textColor=DED_COLOR, alignment=TA_CENTER, spaceBefore=24,
    )
    flows.append(Paragraph("作者后记 · 自勉", title_style))
    flows.append(HRFlowable(width="22%", thickness=1.2, color=C['primary'],
                            hAlign='CENTER', spaceBefore=0, spaceAfter=18))
    flows.append(Paragraph("三年研一报，七篇加两附，", line_style))
    flows.append(Paragraph("不为预言市场，只为看清自己。", line_style))
    flows.append(Spacer(1, 14))
    flows.append(Paragraph("真正的研究，不在于看对几次顶底，", line_style))
    flows.append(Paragraph("而在于建立一套可验证、可证伪、可随证据迭代的判断框架。", line_style))
    flows.append(Spacer(1, 14))
    flows.append(Paragraph("<b>不断学习，提升自我</b>。", emph_style))
    flows.append(Paragraph("愿在未来可能的金融惊涛中<b>稳健穿越</b>，", emph_style))
    flows.append(Paragraph("在长期复利中追求<b>自由与从容</b>。", emph_style))
    flows.append(Spacer(1, 16))
    coda_style = ParagraphStyle(
        'PSCoda', fontName=KAI, fontSize=DED_SIZE, leading=DED_LEAD,
        textColor=DED_COLOR, alignment=TA_CENTER, spaceAfter=2,
        leftIndent=1.2*cm, rightIndent=1.2*cm,
    )
    flows.append(Paragraph("市场起伏于历史长河中不过一瞬，", coda_style))
    flows.append(Paragraph("研究者所能做的，是在每一次周期来临前，", coda_style))
    flows.append(Paragraph("准备好属于自己的判断框架与纪律。", coda_style))
    flows.append(Paragraph("—— 大队长 · 2026 年 5 月 19 日", sign_style))
    flows.append(PageBreak())
    return flows

# 免责声明（含 anchor name="disclaimer"）
story += build_disclaimer()

# 目录
story.append(PageBreak())
story += build_toc()

# 各篇章
for ch in CHAPTERS:
    story += chapter_break(ch["num"], ch["title"], ch["subtitle"], anchor_id=ch["anchor"])
    md_text = load_with_charts(ch["md"], ch["charts"])
    story += parse_markdown(md_text)

# 作者后记（移至末尾）
story += build_author_postscript()

# 构建
decorator = make_page_decorator("2026年AI泡沫研究 · 全景版")
doc.build(story, onFirstPage=make_cover_decorator(), onLaterPages=decorator)
print(f"✓ {OUT} ({OUT.stat().st_size//1024}KB)")
