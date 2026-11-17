from datetime import date, timedelta
import re
import unittest
import xml.etree.ElementTree as ET

from contributions import CalendarParser, render


def calendar_html(count=1, length=367, start=date(2025, 11, 16)):
    heading = f'<h2 id="js-contribution-activity-description">{count:,} contributions in the last year</h2>'
    cells = []
    for index in range(length):
        day = start + timedelta(days=index)
        value = count if index == length - 1 else 0
        level = 4 if value else 0
        tip = f'{value:,} contributions on test day.' if value else 'No contributions on test day.'
        cells.append(f'<td id="d{index}" data-date="{day}" data-level="{level}"></td>'
                     f'<tool-tip for="d{index}">{tip}</tool-tip>')
    return heading + ''.join(cells)


def parse(html):
    parser = CalendarParser()
    parser.feed(html)
    return parser.result()


class CalendarTests(unittest.TestCase):
    def test_counts_are_associated_by_id_not_html_order(self):
        html = calendar_html(1234)
        tips = re.findall(r'<tool-tip.*?</tool-tip>', html)
        html = re.sub(r'<tool-tip.*?</tool-tip>', '', html) + ''.join(reversed(tips))
        total, days = parse(html)
        self.assertEqual(total, 1234)
        self.assertEqual(sum(day[1] for day in days), total)
        self.assertEqual(days[-1], (date(2026, 11, 17), 1234, 4))

    def test_zero_activity_is_valid(self):
        total, days = parse(calendar_html(0))
        self.assertEqual(total, 0)
        self.assertTrue(all(day[1] == 0 for day in days))

    def test_singular_contribution(self):
        html = calendar_html().replace('1 contributions', '1 contribution')
        self.assertEqual(parse(html)[0], 1)

    def test_bad_responses_do_not_become_empty_calendars(self):
        for html in ['<h1>Rate limited</h1>', calendar_html().replace('in the last year', 'in 2026')]:
            with self.subTest(html=html[:60]), self.assertRaises(ValueError):
                parse(html)

    def test_missing_tooltip_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Missing or unrecognised'):
            parse(calendar_html().replace('for="d366"', 'for="other"'))

    def test_missing_and_duplicate_dates_are_rejected(self):
        for replacement in ['2026-11-16', '2026-11-19']:
            with self.subTest(replacement=replacement), self.assertRaisesRegex(ValueError, 'duplicated or missing'):
                parse(calendar_html().replace('2026-11-17', replacement))

    def test_total_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'displayed total'):
            parse(calendar_html().replace('>1 contributions in', '>2 contributions in'))

    def test_svg_handles_leap_year_and_54_columns(self):
        total, days = parse(calendar_html(length=372, start=date(2023, 12, 31)))
        for theme in ['light', 'dark']:
            root = ET.fromstring(render(total, days, '32KZ', theme))
            ns = {'s': 'http://www.w3.org/2000/svg'}
            cells = [r for r in root.findall('.//s:rect', ns) if r.find('s:title', ns) is not None]
            self.assertEqual(len(cells), len(days))
            self.assertTrue(all(float(r.attrib['x']) + float(r.attrib['width']) < 1352 for r in cells))
            self.assertIn('2024-02-29', render(total, days, '32KZ', theme))


if __name__ == '__main__':
    unittest.main()
