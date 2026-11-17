"""Translate chart lettering while preserving every plotted geometric element."""
from pathlib import Path
import hashlib,json,re
import xml.etree.ElementTree as ET
import fitz

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'V1.9现行正文版/assets'
DEST=ROOT/'V1.9_English_Full_Report/assets'
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
ET.register_namespace('xlink','http://www.w3.org/1999/xlink')

LABELS={
'亿元人民币':'RMB 100 million',
'中际旭创':'Zhongji Innolight', '新易盛':'Eoptolink',
'归母净利润':'Attributable\nnet profit',
'经营活动现金流量净额（合并）':'Consolidated operating cash flow',
'光模块公司：半年利润与经营现金流':'Optical modules: half-year earnings and operating cash flow',
'2026年上半年  ·  公司披露值  ·  金额按原始元数据换算':'H1 2026 | Company disclosures | Amounts converted from the original data',
'口径：归母净利润归属母公司股东；合并经营现金流包含控股子公司的全部经营现金流。':'Basis: profit is attributable to owners of the parent; consolidated operating cash flow includes all operating cash flow of controlled subsidiaries.',
'本图仅比较金额量级，不以两者的比值代替严格现金转换率。两份半年报均未经审计。':'The chart compares amounts; their ratio is not a strict cash-conversion ratio. Both interim reports are unaudited.',
'来源：中际旭创2026年半年报第8页（公告日8月22日）；新易盛2026年半年报第7页（公告日8月25日）。':'Sources: Zhongji Innolight 2026 interim report, p. 8 (22 August); Eoptolink 2026 interim report, p. 7 (25 August).',
'原件：巨潮资讯、深交所  ·  核验截至2026年9月8日  ·  金额未年化':'Originals: CNINFO and SZSE | Verified through 8 September 2026 | Amounts not annualized',
'HPC分部收入（百万美元）':'HPC segment revenue (USD million)',
'基础租金':'Base rent','客户装修收入':'Customer fit-out revenue','成本回收':'Cost recovery',
'APLD：增长中的收入，不全是可持续租金':'APLD: revenue growth is not all recurring rent',
'FY27Q1截至2026年8月31日 · HPC收入262.6百万美元 · 基础租金占25.1%':'FY27Q1 ended 31 August 2026 | HPC revenue USD 262.6 million | Base rent: 25.1%',
'另看集团现金：经营现金63.921 − 购建2,074.698 = −2,010.777百万美元。':'Group cash, separately: operating cash 63.921 - asset purchases 2,074.698 = -2,010.777 (USD million).',
'上图为分部收入，下方为集团简单现金桥，不是同一分部的利润或公司定义FCF。':'Bars show segment revenue; the calculation is a simple group cash bridge, not segment profit or company-defined FCF.',
'10月1日新增75MW交付属于期后；可服务容量不等于实际用电或客户利用率。':'The additional 75MW delivered on 1 October is a subsequent event; serviceable capacity is not actual power use or utilization.',
'来源：Applied Digital FY27Q1业绩及10-Q现金表。':'Sources: Applied Digital FY27Q1 results and Form 10-Q cash-flow statement.',
'发行本金':'Principal issued','购买人折扣':'Purchasers\' discount','capped call成本':'Capped-call cost','扣上述两项后':'After both deductions',
'十亿美元':'USD billion',
'CoreWeave：42亿美元本金，不等于42亿美元可用现金':'CoreWeave: USD 4.2B of principal does not mean USD 4.2B of available cash',
'9月22日完成发行 · 4.2000 − 0.0630 − 0.5662 = 3.5708B':'Issue completed on 22 September | 4.2000 - 0.0630 - 0.5662 = 3.5708B',
'3.5708B仍未扣其他发行费用；capped call用于减轻部分转换稀释，并非经营支出。':'The 3.5708B is before other issuance expenses; capped calls mitigate some conversion dilution and are not operating expenses.',
'年现金票息：4.2B × 2.875% = 120.75百万美元；不等于综合融资成本。':'Annual cash coupon: 4.2B x 2.875% = USD 120.75 million; this is not the all-in financing cost.',
'来源：CoreWeave 2026年9月22日SEC 8-K，发行及Capped Call条款。':'Source: CoreWeave SEC Form 8-K, 22 September 2026, issuance and capped-call terms.',
'经营现金流':'Operating cash flow','现金购建固定资产':'Cash purchases\nof PP&E','政府激励及资产出售':'Government incentives\nand asset sales','公司调整后自由现金流':'Company-adjusted\nfree cash flow',
'美光：强现金已兑现，客户押金不在这条经营现金桥中':'Micron: strong realized cash; customer deposits are outside this operating cash bridge',
'FY26Q4截至9月3日 · 43.973 − 11.110 + 0.327 + 0.009 = 33.199B':'FY26Q4 ended 3 September | 43.973 - 11.110 + 0.327 + 0.009 = 33.199B',
'仅按经营现金减现金购建：32.863B；公司调整后口径另加激励及资产出售回款。':'Operating cash less cash purchases alone: 32.863B. The company-adjusted measure adds incentives and asset-sale proceeds.',
'约12.3B本季客户押金列融资活动，不应重复从经营现金扣除；Q4为14周。':'About 12.3B of quarterly customer deposits is classified as financing, not deducted again from operating cash. Q4 had 14 weeks.',
'来源：美光FY26Q4业绩、官方Deck第43页及讲稿第8—9页；财务表未经审计。':'Sources: Micron FY26Q4 results, official deck p. 43 and script pp. 8-9. Financial statements are unaudited.',
'Oracle FY27Q1：增长、现金与融资必须同时看':'Oracle FY27Q1: read growth, cash and financing together',
'单位：十亿美元；财季截至2026-08-31。负数向左，正数向右。':'USD billion | Quarter ended 2026-08-31 | Negative to the left; positive to the right',
'总收入':'Total revenue','其中：客户预付款':'Of which: customer advances','资本开支':'Capital expenditure','自由现金流':'Free cash flow','ATM增发净到账':'Net ATM equity proceeds',
'长期义务另表看：RPO 664；尚未起租的数据中心租赁承诺约288，通常15—19年。':'Long-term obligations, separately: RPO 664; uncommenced data-center leases about 288, typically 15-19 years.',
'RPO、未起租租赁承诺、当季资本开支和ATM融资不是同一种量，图中不相加。':'RPO, uncommenced leases, quarterly capex and ATM financing are different quantities and are not added together.',
'经营现金流含11.363客户预付款且具有重大融资成分；季度报表未经审计。':'Operating cash includes 11.363 of customer advances with a significant financing component; quarterly statements are unaudited.',
'来源：Oracle 2026-09-10 FY27Q1业绩新闻稿及2026-09-11 Form 10-Q。':'Sources: Oracle FY27Q1 earnings release, 2026-09-10, and Form 10-Q, 2026-09-11.',
'先扣除已实现部分，再理解剩余指引':'Subtract the realized half before interpreting the remaining guidance',
'维谛 · 2026年调整后自由现金流 · 百万美元 · 指引发布于2026-07-29':'Vertiv | 2026 adjusted free cash flow | USD million | Guidance issued 2026-07-29',
'全年指引中点 2500.0':'Full-year guidance midpoint: 2500.0','H1已实现 1578.1':'H1 actual: 1578.1','H2隐含 921.9':'Implied H2: 921.9',
'全年范围 2400—2600 → H2算术差额 821.9—1021.9':'Full-year range 2400-2600 -> implied H2 arithmetic remainder 821.9-1021.9',
'全年指引 − 已实现半年 = 剩余半年隐含额':'Full-year guidance - realized first half = implied remaining half',
'Q2的925.3不能直接乘四；半年现金含营运资本变化，非正常化FCFF。':'Do not simply multiply Q2 cash of 925.3 by four; H1 includes working-capital changes and is not normalized FCFF.',
'来源：维谛Q2业绩公告、2026Q2 10-Q；作者按同口径算术拆分，非额外盈利预测。':'Sources: Vertiv Q2 earnings release and 2026 Q2 Form 10-Q. Author\'s like-for-like arithmetic, not a new earnings forecast.',
'Meta：经营现金为正，扣除建设与租赁付款后单季为负':'Meta: positive operating cash, but a quarterly deficit after capex and lease payments',
'2026Q3 · 十亿美元 · 柱高比较金额大小，支出在上方算式中扣减':'2026 Q3 | USD billion | Bars compare amounts; outflows are deducted in the formula',
'流入 32.786':'Inflow: 32.786','经营现金':'Operating cash','支出 33.942':'Outflow: 33.942','固定资产付款':'PP&E payments','支出 0.964':'Outflow: 0.964','租赁本金':'Lease principal',
'来源：Meta 10月21日业绩及FCF调节表；前三季度FCF仍为 +11.049，不外推全年。':'Sources: Meta earnings and FCF reconciliation, 21 October. Nine-month FCF remains +11.049; do not extrapolate a full year.',
'大队长 · V1.9 · 2026-10-27；实际数据各按标注期间':'Daduizhang | V1.9 | 2026-10-27 | Actuals retain their stated observation periods',
'台积电：季度收入继续增长，毛利率边际回落':'TSMC: quarterly revenue rises while gross margin eases',
'收入柱形为十亿美元；毛利率与新台币现金桥单独标明，不混币种':'Revenue bars: USD billion. Gross margin and the TWD cash bridge are shown separately; currencies are not mixed.',
'Q2 实际':'Q2 actual','Q3 实际':'Q3 actual','毛利率：67.7% → 66.4%':'Gross margin: 67.7% -> 66.4%',
'收入美元口径环比 +16.2%':'Revenue in USD: +16.2% QoQ','毛利率环比 −1.3 个百分点':'Gross margin: -1.3pp QoQ',
'Q3 经营现金 − 现金购建':'Q3 operating cash - cash capex','= 476.570 十亿新台币':'= TWD 476.570 billion',
'不代表终端AI项目已回本':'Does not prove end-user AI projects paid back',
'来源：TSMC 10月15日管理报告第1页、财务表第4页；Q4指引未画成实际收入。':'Sources: TSMC management report, 15 October, p. 1; financial statements, p. 4. Q4 guidance is not plotted as actual revenue.',
}

NAMES={
'V1.4_光模块半年报利润与现金_20260908.svg':'figure_01_optical_modules.svg',
'V1.5.1_APLD收入构成_20261009.svg':'figure_02_apld_revenue.svg',
'V1.5.1_CoreWeave融资现金桥_20260924.svg':'figure_03_coreweave_financing.svg',
'V1.5.1_Oracle_FY27Q1资金桥_20260915.svg':'figure_04_oracle_cash.svg',
'V1.5.1_维谛现金指引桥_20260908.svg':'figure_05_vertiv_guidance.svg',
'V1.5.1_美光现金桥_20261001.svg':'figure_06_micron_cash.svg',
'V1.6.1_Meta现金桥_20261027.svg':'figure_07_meta_cash.svg',
'V1.6.1_台积电季度_20261027.svg':'figure_08_tsmc_quarters.svg',
}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def local(e):return e.tag.rsplit('}',1)[-1] if isinstance(e.tag,str) else ''
def geometry(root):
    result=[]
    def walk(e):
        if local(e)=='defs' or e.get('id','').startswith('text_'):return
        if local(e) in ('path','rect','line','circle','ellipse','polygon','polyline'):
            result.append((local(e),sorted(e.attrib.items())))
        for child in e:walk(child)
    walk(root)
    return result

def fontfit(text,size,width):
    longest=max((fitz.get_text_length(line,fontname=font,fontsize=size)
                 for line in text.splitlines() for font in ('helv','hebo')),default=0)
    return min(size,size*width*.96/longest) if longest else size

def main():
    DEST.mkdir(parents=True,exist_ok=True);records={}
    for source_name,english_name in NAMES.items():
        source=SOURCE/source_name
        parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
        root=ET.fromstring(source.read_text(encoding='utf-8'),parser)
        original_geometry=geometry(root);width=float(root.get('viewBox').split()[2]);changes=[]
        # Matplotlib SVGs store lettering as glyph paths; replace each relevant
        # text group with searchable English text, preserving all graph geometry.
        for group in list(root.iter()):
            if not group.get('id','').startswith('text_'):continue
            comments=[c.text.strip() for c in group if c.tag is ET.Comment]
            if not comments or not re.search(r'[\u4e00-\u9fff]',comments[0]):continue
            old=comments[0];new=LABELS[old]
            child=next(c for c in group if c.tag is not ET.Comment)
            transform=child.get('transform','');position=re.search(r'translate\(([-\d.]+) ([-\d.]+)\)',transform)
            scale=re.search(r'scale\(([-\d.]+)',transform)
            x,y=map(float,position.groups());size=abs(float(scale[1]))*100
            color=(re.search(r'fill:\s*([^;]+)',child.get('style','')) or [None,'#294d6b'])[1]
            attrs={'x':str(x),'y':str(y),'fill':color,'font-family':'Arial, sans-serif'}
            available=width-x-35
            if old in ('中际旭创','新易盛'):
                attrs.update(x='132',**{'text-anchor':'end'});available=90
            elif old in ('基础租金','客户装修收入','成本回收'):
                attrs.update(x='160',**{'text-anchor':'end'});available=120
            elif source_name.startswith('V1.5.1_美光') and old in ('经营现金流','现金购建固定资产','政府激励及资产出售','公司调整后自由现金流'):
                centers={'经营现金流':169.19307,'现金购建固定资产':350.92569,'政府激励及资产出售':532.65831,'公司调整后自由现金流':714.39093}
                attrs.update(x=str(centers[old]),**{'text-anchor':'middle'});available=163
            elif old in ('发行本金','购买人折扣','capped call成本','扣上述两项后'):
                centers={'发行本金':168.94268,'购买人折扣':348.010227,'capped call成本':527.137773,'扣上述两项后':706.14532}
                attrs.update(x=str(centers[old]),**{'text-anchor':'middle'});available=164
            if old=='归母净利润':available=85
            if 'rotate(-90)' in transform:
                attrs['transform']=f'rotate(-90 {x} {y})';available=150
            size=fontfit(new,size,available)
            attrs['font-size']=f'{size:.3f}'
            for c in list(group):group.remove(c)
            text=ET.SubElement(group,f'{{{NS}}}text',attrs)
            for i,line in enumerate(new.splitlines()):
                span=ET.SubElement(text,f'{{{NS}}}tspan',{'x':attrs['x'],'dy':'0' if i==0 else f'{size*1.1:.3f}'})
                span.text=line
            changes.append({'source':old,'english':new})
        # The remaining charts already contain text nodes.
        for node in root.iter():
            if local(node)!='text' or not node.text or not re.search(r'[\u4e00-\u9fff]',node.text):continue
            old=node.text;new=LABELS[old];node.text=new
            x=float(node.get('x','0'));available=width-x-35
            if node.get('text-anchor')=='middle':available=230
            if source_name.startswith('V1.6.1_台积电') and x==680:available=330
            style_class=node.get('class','')
            default={'title':34,'sub':20,'label':20,'value':22,'note':17}.get(style_class,20)
            size=float(node.get('font-size',default))
            if source_name.startswith('V1.5.1_Oracle') and old=='自由现金流':available=145
            node.set('font-size',f'{fontfit(new,size,available):.3f}')
            # A presentation attribute would lose to a class font-size rule.
            node.set('style',f'font-size:{fontfit(new,size,available):.3f}px;font-family:Arial,sans-serif')
            changes.append({'source':old,'english':new})
        visible=[''.join(e.itertext()) for e in root.iter() if local(e)=='text']
        for e in root.iter():
            if local(e)=='title' and e.text and re.search(r'[\u4e00-\u9fff]',e.text):e.text=visible[0]
            if local(e)=='desc' and e.text and re.search(r'[\u4e00-\u9fff]',e.text):e.text=' '.join(visible)
        assert geometry(root)==original_geometry,source_name
        assert not any(re.search(r'[\u4e00-\u9fff]',t) for t in visible),source_name
        dest=DEST/english_name
        ET.ElementTree(root).write(dest,encoding='utf-8',xml_declaration=True)
        records[english_name]={'source':source_name,'source_sha256':sha(source),'output_sha256':sha(dest),
                              'plotted_geometry_unchanged':True,'translated_labels':changes,
                              'scope':'Lettering translation and text fit only; plotted values, geometry, observation periods and source URLs retained. Optical-module chart retains RMB 100 million units.'}
    (DEST.parent/'asset-provenance.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Translated {len(records)} figures; plotted geometry unchanged.')

if __name__=='__main__':main()
