#!/usr/bin/env python3
"""Independent arithmetic checks; not a financial forecast or a fact audit."""
from decimal import Decimal as D
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'10_源码_markdown/V1.5.1正文修订'
checks=[]
def check(name, actual, expected, tolerance='0.000001'):
    passed=abs(actual-D(expected))<=D(tolerance)
    checks.append({'name':name,'actual':str(actual),'expected':expected,'passed':passed})
    assert passed, name

check('VRT H1 adjusted FCF',D('1866.6')-D('285.9')-D('2.6'),'1578.1')
check('VRT H2 guidance low implied',D('2400')-D('1578.1'),'821.9')
check('VRT H2 guidance high implied',D('2600')-D('1578.1'),'1021.9')
check('VRT H2 guidance midpoint implied',D('2500')-D('1578.1'),'921.9')
check('VRT naive Q2 x 4 rejected as forecast',D('925.3')*4,'3701.2')
check('VRT H1 working capital contribution',sum(map(D,['-644.2','-1048','-145.3','685.3','1822.7','22.2','-13.9'])),'678.8')
check('VRT H2 revenue midpoint implied',D('14000')-D('5923.8'),'8076.2')
for multiple in [25,30,35]:
    check(f'VRT conditional adjusted EPS x {multiple}',D('6.70')*multiple,{25:'167.50',30:'201.00',35:'234.50'}[multiple])
check('VRT conditional GAAP EPS x 30',D('5.87')*30,'176.10')
check('Lumentum annual defined cash bridge',D('751.4')-D('451.3'),'300.1')
check('Coherent annual defined cash bridge',D('79.514')-D('1102.909'),'-1023.395')
check('Coherent annual bridge also deducting intangibles',D('79.514')-D('1102.909')-D('7.174'),'-1030.569')
check('Dell quarterly FCF',D('2225')-D('1239'),'986')
check('Dell adjusted FCF reconciliation',D('986')+D('6667')+D('496'),'8149')
check('HPE company quarterly FCF',D('1641')-D('745')+D('92')-D('30'),'958')
check('Marvell quarterly defined cash bridge',D('605.5')-D('126.7'),'478.8')
check('Marvell bridge also deducting technology licenses',D('605.5')-D('126.7')-D('4.5'),'474.3')
check('InnoLight H1 defined cash bridge CNY100M',(D('1799674832.02')-D('4802161195.37'))/D('100000000'),'-30.0248636335')
check('Eoptolink H1 defined cash bridge CNY100M',(D('1616408524.15')-D('1263841519.77'))/D('100000000'),'3.5256700438')
pv=sum(D(25)/D('1.1')**n for n in range(1,6))
check('Framework original NPV',pv-D(100),'-5.23','0.005')
check('Framework one year delayed NPV',pv/D('1.1')-D(100),'-13.85','0.005')
check('Framework delay loss',pv-pv/D('1.1'),'8.62','0.005')
check('Energy incremental savings NPV',sum(D(6)/D('1.1')**n for n in range(1,6))-D(10),'12.74','0.005')
check('Energy cost halved gross margin',(D(100)-D(54))/D(100),'0.46')
check('Energy savings passed to customer gross margin',(D(94)-D(54))/D(94),'0.42553','0.000005')
check('Oracle FY27Q1 free cash flow',D('23.103')-D('28.499'),'-5.396')
check('Oracle FY27Q1 RPO sequential increase',D('664')-D('638'),'26')
check('Oracle FY27Q1 total borrowings',D('7.625')+D('117.712'),'125.337')
check('TSMC 2026 August sequential revenue growth',D('514.806')/D('467.580')-D(1),'0.101000','0.000005')
check('Broadcom FY27 and FY28 purchase commitments',D('52.674')+D('72.952'),'125.626')
check('CoreWeave purchaser discounts B',D('4.2')-D('4.137'),'0.063')
check('CoreWeave proceeds after capped calls before other expenses B',D('4.137')-D('0.5662'),'3.5708')
check('CoreWeave annual cash coupon USD million',D('4.2')*D('0.02875')*1000,'120.75')
check('Treasury 2y September 22 vs September 11 bp',(D('4.71')-D('4.63'))*100,'8')
check('Treasury 10y September 22 vs September 11 bp',(D('4.96')-D('4.96'))*100,'0')
check('Sol fixed-token invoice USD',D('2')+D('.2')*D('10'),'4')
check('Luna fixed-token invoice USD',D('.1')+D('.2')*D('.5'),'0.2')
check('Opus 5.5 fixed-token invoice USD',D('4')+D('.2')*D('20'),'8')
check('Opus input output price reduction',1-D('4')/D('5'),'0.2')
check('Opus cache read price reduction',1-D('.2')/D('.5'),'0.6')
ledger=json.loads((ROOT/'12_增量素材/2026-10-01_证据台账.json').read_text())
facts={x['id']:x for x in ledger['facts']}
assert len(facts)==12 and len(ledger['facts'])==12
mu=facts['MU-20260930-01']
for period in ['q4_usd_b','fy26_usd_b']:
    row={k:D(str(v)) for k,v in mu[period].items()}
    check(f'Micron {period} simple bridge',row['ocf']-row['cash_ppe'],str(row['simple_cash_bridge']))
    check(f'Micron {period} net CapEx',row['cash_ppe']-row['government_incentives']-row['ppe_sales'],str(row['net_capex']))
    check(f'Micron {period} adjusted FCF',row['ocf']-row['net_capex'],str(row['adjusted_fcf']))
check('Micron Q4 QoQ percent',(D('54.229')/D('41.456')-1)*100,'30.81','0.005')
check('Micron per week mechanical QoQ percent',((D('54.229')/14)/(D('41.456')/13)-1)*100,'21.47','0.005')
rates=facts['H15-20260930-01']
for key,expected in [('treasury_2y_pct','18'),('treasury_10y_pct','30'),('treasury_real_10y_pct','28')]:
    v=rates[key]
    check(f'{key} Sept29 minus Sept22 bp',(D(str(v[-1]))-D(str(v[0])))*100,expected)
check('Nominal curve September29 bp',(D('5.26')-D('4.89'))*100,'37')
check('Nominal real September29 difference pct',D('5.26')-D('2.91'),'2.35')
check('Sol 6.1 cache reduction',1-D('.1')/D('.2'),'0.5')
check('Sonnet 5.5 fixed token bill',D(2)+D('.2')*10,'4')
check('Crusoe wind nameplate not IT load MW',D('265.5')*2,'531')
oct9_path=ROOT/'12_增量素材/2026-10-09_证据台账.json'
oct9=json.loads(oct9_path.read_text())
new={x['id']:x for x in oct9['facts']}
assert len(new)==13 and len(oct9['facts'])==13
tsm=new['TSMC-20261008-01']
check('TSMC Q2 monthly sum TWD million',D(sum(tsm['revenue'][:3])),str(tsm['q2_monthly_sum']))
check('TSMC Q3 monthly sum TWD million',D(sum(tsm['revenue'][3:])),str(tsm['q3_monthly_sum']))
check('TSMC Q3 monthly sum QoQ pct',(D(tsm['q3_monthly_sum'])/D(tsm['q2_monthly_sum'])-1)*100,'17.62','0.005')
check('TSMC September MoM rounded pct',(D(tsm['revenue'][-1])/D(tsm['revenue'][-2])-1)*100,'-0.6','0.05')
check('TSMC September YoY rounded pct',(D(tsm['revenue'][-1])/D(tsm['september_2025'])-1)*100,'54.6','0.05')
check('TSMC YTD YoY rounded pct',(D(tsm['ytd_2026'])/D(tsm['ytd_2025'])-1)*100,'41.1','0.05')
ap={k:D(str(v)) for k,v in new['APLD-20261007-01'].items() if isinstance(v,(float,int))}
check('APLD HPC revenue component sum',ap['base_rent']+ap['tenant_fitout']+ap['tenant_recoveries'],str(ap['hpc_revenue']))
check('APLD base rent share pct',ap['base_rent']/ap['hpc_revenue']*100,'25.1','0.05')
check('APLD fitout share pct',ap['tenant_fitout']/ap['hpc_revenue']*100,'69.9','0.05')
check('APLD consolidated simple cash bridge USD million',ap['ocf']-ap['ppe_and_other_assets_purchases'],str(ap['simple_cash_bridge']))
ss=new['SAMSUNG-20261008-01']
for key in ['revenue','operating_profit']:
    check('Samsung preliminary midpoint '+key,sum(D(str(x)) for x in ss[key+'_range'])/2,str(ss[key]))
rr=new['RATES-20261008-01']
for key,expected in [('treasury_2y_pct','-14'),('treasury_10y_pct','-4'),('treasury_real_10y_pct','-4')]:
    check(f'{key} Oct8 minus Sept29 bp',(D(str(rr[key][-1]))-D(str(rr[key][0])))*100,expected)
check('October8 2s10s slope bp',(D('5.22')-D('4.75'))*100,'47')
check('October8 nominal real difference pct',D('5.22')-D('2.87'),'2.35')
emp=new['BLS-EMP-20261002-01']
check('July August payroll revisions thousand',D(emp['july_revised']-emp['july_old']+emp['august_revised']-emp['august_old']),'-60')
an=new['ANTHROPIC-20261007-01']
for batch, tier in [('short_batch','haiku_up_to_100k'),('long_batch','haiku_over_100k')]:
    row,price=an[batch],an[tier]
    assert row['output_tokens_per_request']<=128000
    assert (row['input_tokens_per_request']<=100000)==(tier=='haiku_up_to_100k')
    invoice=D(row['requests'])*(D(row['input_tokens_per_request'])*D(str(price['input']))+D(row['output_tokens_per_request'])*D(str(price['output'])))/1000000
    check('Haiku valid request batch '+batch,invoice,str(row['bill_usd']))
check('Haiku same total input',D(an['short_batch']['requests']*an['short_batch']['input_tokens_per_request']-an['long_batch']['requests']*an['long_batch']['input_tokens_per_request']),'0')
check('Haiku same total output',D(an['short_batch']['requests']*an['short_batch']['output_tokens_per_request']-an['long_batch']['requests']*an['long_batch']['output_tokens_per_request']),'0')
check('Sonnet cache reduction October7',1-D(str(an['sonnet']['cache_read']))/D(str(an['sonnet']['old_cache_read'])),'0.5')
source_checks={
    '01_利润真实性拆解.md':['23.103','28.499','−5.396','5,148.06','4,675.80','10.1%'],
    '02_循环投资网络.md':['125.337','664','638','52.674','72.952','4.137','0.5662','3.5708','0.12075'],
    '03_AI变现与编程TAM.md':['272k','4美元','0.20美元','8美元'],
    '08_风险与综合结论.md':['3.75%—4.00%','5.22%','2.87%','9月中旬曾','10月8日'],
    '13_事实审计处置表.md':['2026年10月9日增量核验附表（13组','2026年10月1日增量核验附表（历史12组','APLD-20261007-01','RATES-20261008-01'],
    '07_公司分化与估值.md':['1578.1','821.9','1021.9','8076.2','167.50','201.00','234.50','176.10'],
    '09_框架与页岩油类比.md':['−5.23','−13.85','8.62'],
    '10_聚变能源与资本回收.md':['12.74','−10'],
}
for name, expected in source_checks.items():
    text=(SRC/name).read_text()
    for token in expected:
        assert token in text, f'missing result in current source: {name} {token}'
record={'status':'PASS_ARITHMETIC','checked_at_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'source_results_present':True,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SRC.glob('*.md'))},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limitations':['Checks arithmetic only; source evidence is in separate review notes.','Periods and company definitions differ: no cross-company cash total.','Conditional PE is not a target price; no complete 2027 FCFF model.']}
target=ROOT/'复审与版本记录/V1.5.1_算式复核.json'
target.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':record['status'],'checks':len(checks),'record':str(target)},ensure_ascii=False))
