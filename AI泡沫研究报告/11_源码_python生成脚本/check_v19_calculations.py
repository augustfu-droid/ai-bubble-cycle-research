#!/usr/bin/env python3
"""Recalculate dated V1.9 financial bridges and explicitly hypothetical examples."""
from decimal import Decimal as D
import json


def calc_checks():
    cases = [
        ('MSFT FY27Q1 cash bridge USD B', D('58')-D('39.367'), D('18.633')),
        ('MSFT FY27Q1 after finance lease principal USD B', D('58')-D('39.367')-D('1'), D('17.633')),
        ('GOOG 2026Q3 FCF USD B', D('42.290')-D('51.355'), D('-9.065')),
        ('GOOG 2026Q3 TTM FCF USD B', D('179.551')-D('159.804'), D('19.747')),
        ('GOOG 2026 9M FCF USD B', D('127.149')-D('131.953'), D('-4.804')),
        ('GOOG Q3 simple equity-loss EPS exclusion USD', D('2.12')+D('.55'), D('2.67')),
        ('AMZN Q3 net cash PP&E USD B', D('77.259')-D('1.381'), D('75.878')),
        ('AMZN 2026Q3 FCF USD B', D('42.422')-D('77.259')+D('1.381'), D('-33.456')),
        ('AMZN September TTM FCF USD B', D('168.300')-D('210.657'), D('-42.357')),
        ('AMZN September vs June TTM change USD B', D('-42.357')-D('-7.604'), D('-34.753')),
        ('ZJXC 2026 9M cash bridge CNY 100M', ((D('8008444194.49')-D('9160875564.49'))/D('1e8')).quantize(D('.0001')), D('-11.5243')),
        ('Eoptolink 2026 9M cash bridge CNY 100M', ((D('1464429142.65')-D('1806016532.89'))/D('1e8')).quantize(D('.0001')), D('-3.4159')),
        ('TFC 2026 9M cash bridge CNY 100M', ((D('1461851321.62')-D('491017854.77'))/D('1e8')).quantize(D('.0001')), D('9.7083')),
        ('VRT 2026 9M adjusted FCF USD M', D('2660.6')-D('425')-D('5.3'), D('2230.3')),
        ('VRT implied Q4 FCF low USD M', D('2600')-D('2230.3'), D('369.7')),
        ('VRT implied Q4 FCF high USD M', D('2800')-D('2230.3'), D('569.7')),
        ('VRT implied Q4 revenue midpoint USD M', D('14650')-D('10236.6'), D('4413.4')),
        ('VRT conditional EPS x25, NOT target', D('7.15')*25, D('178.75')),
        ('VRT conditional EPS x30, NOT target', D('7.15')*30, D('214.50')),
        ('VRT conditional EPS x35, NOT target', D('7.15')*35, D('250.25')),
        ('VRT conditional GAAP EPS x30, NOT target', D('6.29')*30, D('188.70')),
        ('US 2Y Oct30 vs Oct26 bp', (D('4.56')-D('4.68'))*100, D('-12')),
        ('US 10Y nominal Oct30 vs Oct26 bp', (D('4.94')-D('5.00'))*100, D('-6')),
        ('US 10Y real Oct30 vs Oct26 bp', (D('2.60')-D('2.66'))*100, D('-6')),
        ('US 2Y-10Y slope Oct30 bp', (D('4.94')-D('4.56'))*100, D('38')),
        ('Samsung Q3 presentation cash bridge KRW T', D('98.6')-D('26.9'), D('71.7')),
        ('SK hynix Q3 presentation cash bridge KRW T', D('54.781')-D('12.670'), D('42.111')),
        ('SK hynix Q3 after reported lease liability repayment KRW T', D('54.781')-D('12.670')-D('.136'), D('41.975')),
        ('Intel Q3 simple cash bridge after finance lease USD B', D('5.082')-D('4.219')-D('.119'), D('.744')),
        ('Intel Q3 adjusted FCF incl government and partner USD B', D('5.082')-D('4.219')-D('.119')+D('.048')+D('.847'), D('1.639')),
        ('Retained Meta Q3 FCF USD B', D('32.786')-D('33.942')-D('.964'), D('-2.120')),
        ('Retained TSMC Q3 cash bridge NTD M', D('919776')-D('443206'), D('476570')),
        ('Retained ASML Q3 FCF EUR M', D('11797.6')-D('413.3')-D('33.9'), D('11350.4')),
        ('Retained Anthropic H1 revenue USD B', D('4.731')+D('11.555'), D('16.286')),
        ('Retained Anthropic H1 operating income USD B', -D('1.667')+D('.974'), D('-.693')),
        ('Illustrative EPS and PE price shock', D('.8')*D('.75')-1, D('-.4')),
        ('Illustrative weighted index return', D('.3')*D('-.4')+D('.7')*D('-.1'), D('-.19')),
        ('Illustrative project NPV base', (-100+60/D('1.1')+60/D('1.1')**2).quantize(D('.01')), D('4.13')),
        ('Illustrative project NPV receipts delayed', (-100+60/D('1.1')**2+60/D('1.1')**3).quantize(D('.01')), D('-5.33')),
        ('Illustrative project NPV all delayed', (-100/D('1.1')+60/D('1.1')**2+60/D('1.1')**3).quantize(D('.01')), D('3.76')),
        ('Illustrative project NPV cheaper assets', (-90/D('1.1')+60/D('1.1')**2+60/D('1.1')**3).quantize(D('.01')), D('12.85')),
        ('Illustrative unit contribution with efficiency', (D('.8')-D('.45'))*130, D('45.5')),
        ('Illustrative unit contribution weaker efficiency', (D('.8')-D('.55'))*130, D('32.5')),
        ('Illustrative electricity price halving gross margin', (100-(60-12+6))/D(100), D('.46')),
        ('Illustrative fusion cost NPV, not project valuation', (-10+sum(6/D('1.1')**i for i in range(1,6))).quantize(D('.01')), D('12.74')),
        ('Illustrative QDII premium effect percent', ((D('.50')*D('.95')/D('1.30')-1)*100).quantize(D('.01')), D('-63.46')),
        ('Illustrative daily inverse two days percent', ((D('.80')*(1+D(2)/11)-1)*100).quantize(D('.01')), D('-5.45')),
        ('Duiba H1 AI drama revenue share percent', (D('222629')/D('434721')*100).quantize(D('.1')), D('51.2')),
        ('Chinese Online derived Q3 CFO CNY', D('42795996.82')-D('126801681.39'), D('-84005684.57')),
        ('Illustrative video generated seconds at 20% yield', D('3600')/D('.2'), D('18000')),
        ('Illustrative video total cost at 20% yield CNY', D('3600')/D('.2')*D('.5')+25000+10000+6000+10000, D('60000')),
        ('Illustrative video generated seconds at 40% yield', D('3600')/D('.4'), D('9000')),
        ('Illustrative video total cost at 40% yield CNY', D('3600')/D('.4')*D('.5')+51000, D('55500')),
        ('Illustrative video finished minute cost CNY', D('55500')/60, D('925')),
        ('Illustrative video total cost saving percent', (D('60000')-D('55500'))/D('60000')*100, D('7.5')),
        ('Illustrative China IAA base receipts CNY', D('100000000')/1000*D('.8')*12*D('.4'), D('384000')),
        ('Illustrative China IAA base contribution CNY', D('384000')-120000-40000-100000-60000, D('64000')),
        ('Illustrative China IAA weaker eCPM receipts CNY', D('100000000')/1000*D('.8')*9*D('.4'), D('288000')),
        ('Illustrative China IAA weaker eCPM contribution CNY', D('288000')-320000, D('-32000')),
        ('Illustrative China IAA break-even eCPM CNY', D('320000')/(D('100000000')/1000*D('.8')*D('.4')), D('10')),
        ('Illustrative China IAA break-even ad opportunities', (D('320000')/(D('.8')*12*D('.4'))*1000).quantize(D('.01')), D('83333333.33')),
        ('Illustrative US 90d net receipts USD', D('100000')*D('.04')*60*D('.95')*D('.8'), D('182400')),
        ('Illustrative US 90d contribution USD', D('182400')-150000-20000-10000, D('2400')),
        ('Illustrative US CAC per paying customer USD', D('150000')/(D('100000')*D('.04')), D('37.5')),
        ('Illustrative US break-even payer percent', (D('180000')/(D('100000')*60*D('.95')*D('.8'))*100).quantize(D('.001')), D('3.947')),
        ('Illustrative US break-even payer receipts USD', (D('180000')/(D('100000')*D('.04')*D('.95')*D('.8'))).quantize(D('.01')), D('59.21')),
        ('Illustrative US day30 receipts USD', D('182400')*D('.35'), D('63840')),
        ('Illustrative US day30 funding gap if all costs paid USD', D('180000')-D('182400')*D('.35'), D('116160')),
    ]
    # Coding, customer ROI and technology-delay examples are conditional, not forecasts.
    for monthly, expected in [('10','4.38'),('20','8.76'),('30','13.14'),('40','17.52'),('100','43.8')]:
        for share in ('0.25','0.5','1'):
            cases.append((f'Historical coding seats month={monthly} share={share} USD B',
                          D('36500000')*D(monthly)*12*D(share)/D('1e9'), D(expected)*D(share)))
    cases.extend([
        ('Illustrative coding 2027 A professional subscription USD B', D('8000000')*25*12/D('1e9'), D('2.4')),
        ('Illustrative coding 2027 A additional usage USD B', D('8000000')*150/D('1e9'), D('1.2')),
        ('Illustrative coding 2027 A nonprofessional USD B', D('4000000')*3*20/D('1e9'), D('.24')),
        ('Illustrative coding 2027 A tasks USD B', D('500000')*200/D('1e9'), D('.1')),
        ('Illustrative coding 2027 A total USD B', D('2.4')+D('1.2')+D('.24')+D('.1'), D('3.94')),
        ('Illustrative coding 2027 B professional subscription USD B', D('12000000')*40*12/D('1e9'), D('5.76')),
        ('Illustrative coding 2027 B additional usage USD B', D('12000000')*400/D('1e9'), D('4.8')),
        ('Illustrative coding 2027 B nonprofessional USD B', D('8000000')*4*25/D('1e9'), D('.8')),
        ('Illustrative coding 2027 B tasks USD B', D('1000000')*300/D('1e9'), D('.3')),
        ('Illustrative coding 2027 B total USD B', D('5.76')+D('4.8')+D('.8')+D('.3'), D('11.66')),
        ('Retained hypothetical coding V1.5 USD B', D('3.6')+1+D('.04'), D('4.64')),
        ('Illustrative accepted coding task baseline USD', D('4')*60, D('240')),
        ('Illustrative accepted coding task A USD', 12+D('1.2')*60+D('.2')*2*60+8, D('116')),
        ('Illustrative accepted coding task B USD', 12+D('3')*60+D('.4')*4*60+8, D('296')),
        ('Illustrative coding task A saving USD', D('240')-116, D('124')),
        ('Illustrative coding task B saving USD', D('240')-296, D('-56')),
        ('Illustrative API price-volume revenue percent', (D('.85')*D('1.1')-1)*100, D('-6.5')),
        ('Illustrative API break-even volume percent', ((1/D('.85')-1)*100).quantize(D('.001')), D('17.647')),
        ('Duolingo Q2 company FCF USD thousands', D('88260')-2734-6896, D('78630')),
        ('Illustrative office gross hours saved', D('1000')*4*12, D('48000')),
        ('Illustrative office gross time value USD', D('48000')*50, D('2400000')),
        ('Illustrative office realizable cash benefit USD', D('2400000')*D('.25'), D('600000')),
        ('Illustrative office full incremental costs USD', D('360000')+150000+120000, D('630000')),
        ('Illustrative office net cash benefit USD', D('600000')-630000, D('-30000')),
        ('Illustrative office break-even cash conversion percent', D('630000')/2400000*100, D('26.25')),
        ('Illustrative office higher cash conversion net benefit USD', D('2400000')*D('.5')-630000, D('570000')),
        ('Illustrative delayed 3y cash at 8 percent, PV fraction percent', (100/D('1.08')**3).quantize(D('.1')), D('79.4')),
        ('Illustrative delayed 3y cash at 10 percent, PV fraction percent', (100/D('1.10')**3).quantize(D('.1')), D('75.1')),
        ('Illustrative delayed 3y cash at 12 percent, PV fraction percent', (100/D('1.12')**3).quantize(D('.1')), D('71.2')),
        ('Illustrative 40 percent business share delayed 3y at 10 percent, value loss percent', ((1-1/D('1.1')**3)*D('.4')*100).quantize(D('.01')), D('9.95')),
    ])
    # V1.9: financial bridges, video production and software-labor economics.
    # All production, staffing, wage and cost inputs below are illustrative unless
    # the label explicitly identifies a dated financial statement or public tariff.
    cases.extend([
        ('MiniMax H1 revenue channel sum USD M', D('42.644')+D('73.929'), D('116.573')),
        ('MiniMax H1 gross profit USD M', D('116.573')-D('95.760'), D('20.813')),
        ('MiniMax H1 platform share percent', (D('73.929')/D('116.573')*100).quantize(D('.1')), D('63.4')),
        ('MiniMax H1 gross margin percent', (D('20.813')/D('116.573')*100).quantize(D('.1')), D('17.9')),
        ('MiniMax H1 gross profit to R&D percent', (D('20.813')/D('296.870')*100).quantize(D('.1')), D('7.0')),
        ('MiniMax H1 adjusted net loss bridge USD M', D('-357.997')+D('28.208')+D('31.025')+D('5.733'), D('-293.031')),
        ('MiniMax FY2025 revenue channel sum USD M', D('53.075')+D('25.963'), D('79.038')),
        ('MiniMax FY2024 revenue channel sum USD M', D('21.805')+D('8.718'), D('30.523')),
        ('Illustrative unused video package cost multiplier', (D('.8')/D('.6')).quantize(D('.001')), D('1.333')),
        ('Illustrative whole drama seconds', D('120')*60, D('7200')),
        ('Illustrative fresh main-video seconds', D('7200')*D('.8')*D('.75'), D('4320')),
        ('Illustrative new advertising seconds', D('48')*15, D('720')),
        ('Illustrative new localization seconds', D('2')*480, D('960')),
        ('Illustrative total newly accepted seconds', D('4320')+720+960, D('6000')),
        ('Illustrative generated seconds incl discarded', D('6000')/D('.25'), D('24000')),
        ('Illustrative paid video seconds', D('24000')*D('.9'), D('21600')),
        ('Illustrative H3 output bill only USD', D('21600')*D('.08'), D('1728')),
        ('Illustrative six-second successful tasks', D('24000')/6, D('4000')),
        ('Illustrative 1000 identical projects USD', D('1728')*1000, D('1728000')),
        ('Illustrative 10000 identical projects USD', D('1728')*10000, D('17280000')),
        ('Illustrative 100000 identical projects USD', D('1728')*100000, D('172800000')),
        ('Illustrative effective revenue per total generated second USD', D('1728')/24000, D('.072')),
        ('Illustrative cost ceiling at 50pct contribution USD', D('1728')*D('.5'), D('864')),
        ('Illustrative cost ceiling per generated second USD', D('864')/24000, D('.036')),
        ('Illustrative new output factor per k', D('.25')/D('.50'), D('.5')),
        ('Illustrative new revenue factor per k', D('.25')/D('.50')*D('.04')/D('.08'), D('.25')),
        ('Illustrative new effective computation factor per k', D('.5')*D('.6'), D('.30')),
        ('Illustrative old contribution per second USD', D('.08')*D('.9')-D('.04'), D('.032')),
        ('Illustrative new contribution per second USD', D('.04')*D('.9')-D('.024'), D('.012')),
        ('Illustrative contribution ratio per k', D('.5')*D('.012')/D('.032'), D('.1875')),
        ('Illustrative revenue breakeven production multiple', 1/D('.25'), D('4')),
        ('Illustrative contribution breakeven production multiple', (1/D('.1875')).quantize(D('.01')), D('5.33')),
        ('Illustrative computation breakeven production multiple', (1/D('.30')).quantize(D('.01')), D('3.33')),
        ('RCT output increase converted to constant-output time saving percent', ((1-1/D('1.2608'))*100).quantize(D('.001')), D('20.685')),
        ('BLS June benefits to wages all-private percent', (D('14.07')/D('32.82')*100).quantize(D('.01')), D('42.87')),
        ('Illustrative US gross freed hours', D('18000')*D('.60')*D('.80')*D('.50'), D('4320')),
        ('Illustrative US added labor hours', D('1080')+540+300, D('1920')),
        ('Illustrative US net freed hours', D('4320')-1920, D('2400')),
        ('Illustrative US equivalent person-years', (D('2400')/1800).quantize(D('.001')), D('1.333')),
        ('Illustrative US first-year net hours', D('2400')-900, D('1500')),
        ('Illustrative US annual tool seat cost USD', D('10')*150*12, D('18000')),
        ('Illustrative US cost plus risk budget USD', D('18000')+12000+6000+4000, D('40000')),
        ('Illustrative US steady resource net USD', D('2400')*100-40000, D('200000')),
        ('Illustrative US first-year resource net USD', D('1500')*100-40000-20000, D('90000')),
        ('Illustrative US all retained steady incremental budget USD', -D('40000'), D('-40000')),
        ('Illustrative US all retained first-year incremental budget USD', -D('40000')-20000, D('-60000')),
        ('Illustrative US avoid one full-year hire USD', D('180000')-40000, D('140000')),
        ('Illustrative US first-year half-year delayed hire USD', D('180000')/2-40000-20000, D('30000')),
        ('Illustrative US one post-transition role removed incl severance USD', D('180000')-40000-45000, D('95000')),
        ('Illustrative China gross freed hours', D('14400')*D('.50')*D('.75')*D('.50'), D('2700')),
        ('Illustrative China added labor hours', D('900')+540+360, D('1800')),
        ('Illustrative China net freed hours', D('2700')-1800, D('900')),
        ('Illustrative China equivalent person-years', D('900')/1800, D('.5')),
        ('Illustrative China first-year net hours', D('900')-540, D('360')),
        ('Illustrative China annual seat cost CNY', D('8')*500*12, D('48000')),
        ('Illustrative China cost plus risk budget CNY', D('48000')+24000+12000+6000, D('90000')),
        ('Illustrative China steady resource net CNY', (D('900')*D('240000')/1800-90000).quantize(D('.01')), D('30000.00')),
        ('Illustrative China first-year resource net CNY', (D('360')*D('240000')/1800-90000-30000).quantize(D('.01')), D('-72000.00')),
        ('Illustrative China avoid external work steady CNY', D('900')*220-90000, D('108000')),
        ('Illustrative China avoid external work first-year CNY', D('360')*220-90000-30000, D('-40800')),
        ('Illustrative US cash conversion breakeven percent', (D('40000')/240000*100).quantize(D('.01')), D('16.67')),
        ('Illustrative China cash conversion breakeven percent', D('90000')/120000*100, D('75')),
        ('Illustrative US fixed-headcount capacity gain percent', ((1/(1-D('2400')/18000)-1)*100).quantize(D('.01')), D('15.38')),
        ('Illustrative China fixed-headcount capacity gain percent', ((1/(1-D('900')/14400)-1)*100).quantize(D('.01')), D('6.67')),
        ('Illustrative US fixed-budget capacity gain constant K percent', (((1-D('40000')/1800000)/(1-D('2400')/18000)-1)*100).quantize(D('.01')), D('12.82')),
        ('Illustrative China fixed-budget capacity gain constant K percent', (((1-D('90000')/1920000)/(1-D('900')/14400)-1)*100).quantize(D('.01')), D('1.67')),
        ('Illustrative 20pct net time saving output required percent', (1/D('.8')-1)*100, D('25')),
        ('Illustrative 10pct output growth labor ratio', D('.8')*D('1.1'), D('.88')),
        ('Illustrative 40pct output growth labor ratio', D('.8')*D('1.4'), D('1.12')),
        ('Illustrative price elasticity threshold at 10pct cut', (D('.8').ln()/D('.9').ln()).quantize(D('.0001')), D('2.1179')),
        ('Illustrative price elasticity threshold at 20pct cut', D('.8').ln()/D('.8').ln(), D('1')),
        ('Illustrative customer saving after tool and governance CNY', D('100')-30-10, D('60')),
        ('Illustrative tool provider contribution CNY', D('30')-18-5, D('7')),
        ('Illustrative tool provider costly-task contribution CNY', D('30')-28-5, D('-3')),
        ('Illustrative outsourcer previous gross profit CNY 10k', D('100')-70, D('30')),
        ('Illustrative outsourcer same-contract gross profit CNY 10k', D('100')-50-10, D('40')),
        ('Illustrative outsourcer renewed-contract gross profit CNY 10k', D('85')-50-10, D('25')),
    ])
    for yield_rate, values in [('0.15',[1440,2880,4320]),('0.25',[864,1728,2592]),('0.40',[540,1080,1620])]:
        for price, expected in zip(['.04','.08','.12'], values):
            cases.append((f'Illustrative video bill yield={yield_rate}, price={price}',
                          D('6000')/D(yield_rate)*D('.9')*D(price), D(expected)))
    for cost, contribution, margin in [('.02','1248','72.2'),('.04','768','44.4'),('.06','288','16.7')]:
        got = D('1728')-D('24000')*D(cost)
        cases.append((f'Illustrative inference contribution USD cost={cost}', got, D(contribution)))
        cases.append((f'Illustrative inference contribution percent cost={cost}', (got/D('1728')*100).quantize(D('.1')), D(margin)))
    for country, hours, exposure, adoption, extra, hourly, budget, expected_thresholds in [
        ('US','18000','.6','.8','1920',D('100'),'40000',['26.85','31.48']),
        ('China','14400','.5','.75','1800',D('240000')/1800,'90000',['45.83','58.33']),
    ]:
        for realized, expected in zip(['1','.5'], expected_thresholds):
            got=(D(extra)+D(budget)/(D(realized)*hourly))/(D(hours)*D(exposure)*D(adoption))*100
            cases.append((f'Illustrative {country} gross-saving threshold f={realized} percent', got.quantize(D('.01')), D(expected)))
    for g, us_hours, us_value, cn_hours, cn_value in [
        ('.4',1536,113600,360,-42000),('.5',2400,200000,900,30000),('.6',3264,286400,1440,102000),
    ]:
        us = D('18000')*D('.6')*D('.8')*D(g)-1920
        cn = D('14400')*D('.5')*D('.75')*D(g)-1800
        cases.extend([
            (f'Illustrative US sensitivity net hours g={g}', us, D(us_hours)),
            (f'Illustrative US sensitivity resource value g={g}', us*100-40000, D(us_value)),
            (f'Illustrative China sensitivity net hours g={g}', cn, D(cn_hours)),
            (f'Illustrative China sensitivity resource value g={g}', (cn*D('240000')/1800-90000).quantize(D('.01')), D(cn_value)),
        ])
    # Each matrix cell is an independently stated scenario, not an industry estimate.
    matrix = [('0.03', [6800, -43200, -93200]),
              ('0.04', [52400, 2400, -47600]),
              ('0.05', [98000, 48000, -2000])]
    for payer, expected_row in matrix:
        for cac, expected in zip(('1', '1.5', '2'), expected_row):
            result = D('100000')*D(payer)*60*D('.95')*D('.8')-D('100000')*D(cac)-30000
            cases.append((f'Illustrative US 90d contribution payer={payer}, CAC={cac}', result, D(expected)))
    return [{'name': name, 'result': str(got), 'expected': str(expected),
             'pass': got == expected} for name, got, expected in cases]


if __name__ == '__main__':
    results = calc_checks()
    print(json.dumps({'checks': len(results), 'passed': sum(r['pass'] for r in results),
                      'failed': [r for r in results if not r['pass']]}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(r['pass'] for r in results) else 1)
