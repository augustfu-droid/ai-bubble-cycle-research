#!/usr/bin/env python3
"""Read-only regression checks for V1.9 publication numbering; no PDF render."""
from __future__ import annotations

import re
import unittest

import build_v19_current as builder
import numbering_v19 as numbering


class PublicationNumberingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.keys = list(dict.fromkeys(k for row in builder.CATALOG for k in row[2]))
        cls.raw = {key: builder.source(key) for key in cls.keys}
        cls.published = {key: numbering.render_numbered_source(key, text)
                         for key, text in cls.raw.items()}

    def test_full_report_has_thirteen_ordered_chapters_and_six_appendices(self):
        text = builder.publication_body(builder.FULL)
        actual = re.findall(r'^## (第[^：]+章)：', text, re.M)
        self.assertEqual(actual, ['第一章', '第二章', '第三章', '第四章', '第五章',
                                  '第六章', '第七章', '第八章', '第九章', '第十章',
                                  '第十一章', '第十二章', '第十三章'])
        self.assertEqual(re.findall(r'^## 附篇([A-F])：', text, re.M), list('ABCDEF'))

    def test_expected_chapter_order_in_every_edition(self):
        expected = [
            list(range(1, 12)), [], [1], [2], [3, 4, 5, 6], [7, 8], [],
            [1, 3, 4, 7, 8, 9], [10, 9], [], [], list(range(1, 14)),
            list(range(1, 14)), list(range(1, 12)), [13, 2], [12, 11],
            [], [4], [5], [6],
        ]
        cn = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
              '十一', '十二', '十三']
        for item, numbers in zip(builder.CATALOG, expected, strict=True):
            with self.subTest(slug=item[0]):
                body = builder.prepare_body(item[2])
                labels = re.findall(r'^## 第([^：]+)章：', body, re.M)
                self.assertEqual(labels, [cn[n] for n in numbers])
                self.assertIn('完整报告统一编号', numbering.numbering_note(item[2]))
                if numbers and numbers != list(range(1, 14)):
                    self.assertIn('本册按专题选编', numbering.numbering_note(item[2]))

    def test_sections_agree_with_current_chapter(self):
        cn = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
              '十一', '十二', '十三']
        body = builder.publication_body(builder.FULL)
        chapter, labels = None, []
        for line in body.splitlines():
            top = re.match(r'^## 第([^：]+)章：', line)
            if top:
                chapter = cn.index(top[1])
            section = re.match(r'^#{3,6} (\d+)\.(\d+(?:\.\d+)*) ', line)
            if section:
                self.assertEqual(int(section[1]), chapter, line)
                labels.append(section[1] + '.' + section[2])
        self.assertEqual(len(labels), len(set(labels)))
        for chapter, count in [(4, 20), (5, 15), (6, 11), (7, 6), (8, 10), (12, 8), (13, 8)]:
            self.assertEqual([x for x in labels if re.fullmatch(fr'{chapter}\.\d+', x)],
                             [f'{chapter}.{n}' for n in range(1, count + 1)])

    def test_every_url_and_current_citation_label_is_byte_identical(self):
        # No current citation label contains a publication chapter reference.
        # Compare ordered URL/label pairs, not merely a set of destinations.
        for key in self.keys:
            with self.subTest(key=key):
                self.assertEqual(builder.reference_entries(self.raw[key]),
                                 builder.reference_entries(self.published[key]))
                self.assertEqual(re.findall(r'\]\((.*?)\)', self.raw[key]),
                                 re.findall(r'\]\((.*?)\)', self.published[key]))

    def test_named_joint_references_and_international_index(self):
        self.assertIn('见第四章、第五章', self.published['agi'])
        self.assertIn('8.10列明逐节观察范围', self.published['agi'])
        self.assertIn('开放权重与许可边界见8.1。', self.published['agi'])
        self.assertIn('第八章用 IEA', self.published['agi'])
        self.assertIn('| 7.1 时间表 |', self.published['agi'])
        self.assertIn('| 7.6 反证 |', self.published['agi'])
        self.assertIn('| 8.1 中美模型 |', self.published['agi'])
        self.assertIn('| 8.9 反证 |', self.published['agi'])
        self.assertIn('见第三章、第七章、第八章及技术更新记录', self.published['audit'])
        self.assertIn('完整复盘见第五章、第六章', self.published['short:snowball'])

    def test_specific_cross_references_have_real_targets(self):
        expected = {
            'monetization': ['第五章5.1、5.4', '第五章5.6', '第五章5.3。',
                             '第五章5.8同时比较', '5.11—5.12再把人工复核',
                             '需求弹性见5.10—5.13', '第六章6.7—6.9'],
            'audit': ['市场证据见5.1—5.6', '传播链详见4.2', '原件页码见4.8',
                      '4.12的120分钟', '4.19价格减半', '5.9—5.10保留原始期间',
                      '逐式复算见5.11—5.14'],
            'video': ['用4.12基准继续算'],
            'coding': ['与5.5的终端支出去重方法相容'],
        }
        for key, fragments in expected.items():
            for fragment in fragments:
                self.assertIn(fragment, self.published[key])
        full = builder.publication_body(builder.FULL)
        targets = set(re.findall(r'^#{3,6} (\d+(?:\.\d+)+) ', full, re.M))
        for rule in numbering.REFERENCE_RULES:
            self.assertTrue(set(rule.targets) <= targets, rule)

    def test_history_rows_and_source_names_remain_exact(self):
        historical_rows = [line for line in self.raw['coding'].splitlines()
                           if line.startswith(('| V1.0', '| 同分册', '| V1.4合成源', '| V1.5第3篇'))]
        self.assertEqual(len(historical_rows), 7)
        for row in historical_rows:
            self.assertIn(row, self.published['coding'])
        for fragment in ['`8caf2c1`', 'V0.8.2·2026/06/03', '14.4—19.5亿美元',
                         'V1.4合成源3.4', 'V1.5第3篇', 'V1.7第3篇']:
            self.assertIn(fragment, self.published['coding'])

    def test_sensitive_numeric_facts_and_external_page_references_are_unchanged(self):
        examples = {
            'profit': ['−4.804', '+19.747', '18.633', '7.388', '19.909'],
            'circular': ['DDTL 5.5', 'SOFR+5.50%', '19.063'],
            'monetization': ['| 4.00 | 20.00 |', 'GPT-6.1 Sol', 'Opus 5.5', '3.94B与11.66B'],
            'agi': ['Fable 5.1', 'Opus 4.6', '第748部分附录2(dd)', '§742.6(b)(10)(iii)(A)(1)'],
            'valuation': ['7.10—7.20', '7.15美元', '6.29', '6.70'],
            'video': ['7.18亿', '20.079', '20.813', '印刷第6、416页'],
            'coding': ['20.685%', '6.25%', '7.5人'],
            'delay': ['| 4.13 |', '−5.33', '9.47'],
        }
        for key, fragments in examples.items():
            for fragment in fragments:
                self.assertGreater(self.raw[key].count(fragment), 0, (key, fragment))
                self.assertEqual(self.raw[key].count(fragment),
                                 self.published[key].count(fragment), (key, fragment))

    def test_code_urls_paths_and_link_labels_have_distinct_behaviour(self):
        text = ('专题三、四；[专题三](https://example.com/专题三/18.12(x))\n'
                '`专题四 19.5 V1.0`\nC:\\资料\\专题四.md\n'
                '[专题五](../专题五/20.7.md)\n'
                '```text\n专题三 18.12\n```\n'
                '<!-- 专题三 18.12 -->\n')
        actual = numbering.render_numbered_source('short:fixture', text)
        self.assertIn('第四章、第五章；[第四章](https://example.com/专题三/18.12(x))', actual)
        self.assertIn('`专题四 19.5 V1.0`', actual)
        self.assertIn('C:\\资料\\专题四.md', actual)
        self.assertIn('[第六章](../专题五/20.7.md)', actual)
        self.assertIn('```text\n专题三 18.12\n```', actual)
        self.assertIn('<!-- 专题三 18.12 -->', actual)

    def test_changed_reviewed_sources_fail_instead_of_silently_missing_references(self):
        with self.assertRaisesRegex(ValueError, 'exact reference'):
            numbering.render_numbered_source('video', self.raw['video'].replace('用18.12基准继续算', '用旧基准继续算'))
        with self.assertRaisesRegex(ValueError, 'expected one'):
            numbering.render_numbered_source('agi', self.raw['agi'].replace('## 第五部分：', '## 未审查标题：'))

    def test_source_api_does_not_expose_publication_numbers(self):
        before = {path: builder.sha(path) for path in builder.SRC.glob('*') if path.is_file()}
        for key in self.keys:
            self.assertEqual(builder.source(key), self.raw[key])
        self.assertIn('## 专题三：', builder.source('video'))
        self.assertIn('## 第四部分：', builder.source('agi'))
        after = {path: builder.sha(path) for path in builder.SRC.glob('*') if path.is_file()}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main(verbosity=2)
