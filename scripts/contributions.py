"""Render the public GitHub calendar as README-safe SVGs (standard library only).

Usage: python scripts/contributions.py --user 32KZ
Offline: python scripts/contributions.py --html path/to/calendar.html
Only public calendar data is fetched; no personal access token is needed.
"""

import argparse
import calendar
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.request import Request, urlopen


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tooltips = {}
        self.total_text = ""
        self._tip = None
        self._heading = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "td" and "data-date" in attrs:
            key = attrs["id"]
            if key in self.cells:
                raise ValueError("Duplicate calendar cell")
            self.cells[key] = (date.fromisoformat(attrs["data-date"]), int(attrs["data-level"]))
        if tag == "tool-tip" and attrs.get("for"):
            self._tip = attrs["for"]
            self.tooltips[self._tip] = ""
        if tag == "h2" and attrs.get("id") == "js-contribution-activity-description":
            self._heading = True

    def handle_data(self, data):
        if self._heading:
            self.total_text += data
        if self._tip:
            self.tooltips[self._tip] += data

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            self._tip = None
        if tag == "h2":
            self._heading = False

    def result(self):
        title = re.fullmatch(r"\s*([\d,]+)\s+contributions?\s+in the last year\s*", self.total_text)
        if not title:
            raise ValueError("GitHub's heading changed or the response is not a yearly calendar")
        total = int(title[1].replace(",", ""))
        days = []
        for key, (day, level) in self.cells.items():
            tip = self.tooltips.get(key, "").strip()
            count_match = re.match(r"([\d,]+) contributions? on ", tip)
            if count_match:
                count = int(count_match[1].replace(",", ""))
            elif tip.startswith("No contributions on "):
                count = 0
            else:
                raise ValueError(f"Missing or unrecognised contribution count for {day}")
            if level not in range(5) or (count == 0) != (level == 0):
                raise ValueError(f"Inconsistent contribution level for {day}")
            days.append((day, count, level))
        days.sort()
        # GitHub aligns the last year to the preceding Sunday, including leap years.
        if not 365 <= len(days) <= 372:
            raise ValueError("Expected a complete year of contributions")
        if any(b[0] - a[0] != timedelta(days=1) for a, b in zip(days, days[1:])):
            raise ValueError("Calendar dates are duplicated or missing")
        if sum(day[1] for day in days) != total:
            raise ValueError("Daily counts do not match GitHub's displayed total")
        return total, days


THEMES = {
    "dark": {"bg": "#0d1117", "text": "#f0f6fc", "muted": "#9198a1", "border": "#3d444d",
             "levels": ["#151b23", "#033a16", "#196c2e", "#2ea043", "#56d364"]},
    "light": {"bg": "#ffffff", "text": "#1f2328", "muted": "#59636e", "border": "#d1d9e0",
              "levels": ["#eff2f5", "#aceebb", "#4ac26b", "#2da44e", "#116329"]},
}


def render(total, days, user, theme):
    colors = THEMES[theme]
    start = days[0][0] - timedelta(days=(days[0][0].weekday() + 1) % 7)
    weeks = (days[-1][0] - start).days // 7 + 1
    pitch = min(22.5, 1170 / max(1, weeks - 1))
    cell = min(16.25, pitch - 5)
    noun = "contribution" if total == 1 else "contributions"
    summary = f"{total:,} {noun} in the last year"
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1367" height="332" viewBox="0 0 1367 332" role="img" aria-labelledby="title description">',
        f'<title id="title">{escape(user)}: {summary}</title>',
        f'<desc id="description">Public GitHub contribution calendar, {days[0][0]} to {days[-1][0]}. Green squares indicate contribution activity. Generated from the public calendar.</desc>',
        f'<rect width="1367" height="332" fill="{colors["bg"]}"/>',
        f'<g font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" fill="{colors["text"]}">',
        f'<text x="9" y="34" font-size="24">{summary}</text>',
        f'<rect x="9.5" y="54.5" width="1343" height="268" rx="9" fill="none" stroke="{colors["border"]}"/>',
    ]
    previous_month = None
    for week in range(weeks):
        sunday = start + timedelta(weeks=week)
        if sunday.month != previous_month:
            out.append(f'<text x="{113 + week * pitch:g}" y="99" font-size="18">{calendar.month_abbr[sunday.month]}</text>')
            previous_month = sunday.month
    for label, row in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        out.append(f'<text x="63" y="{129 + row * 22.5:g}" font-size="18">{label}</text>')
    for day, count, level in days:
        offset = (day - start).days
        x, y = 113 + (offset // 7) * pitch, 113 + (offset % 7) * 22.5
        label = f"{day}: {count} {'contribution' if count == 1 else 'contributions'}"
        out.append(f'<rect x="{x:g}" y="{y:g}" width="{cell:g}" height="16.25" rx="2.5" fill="{colors["levels"][level]}"><title>{label}</title></rect>')
    out.append(f'<g fill="{colors["muted"]}" font-size="18">')
    out.append('<text x="70" y="297">Learn how we count contributions</text>')
    out.append('<text x="1105" y="297">Less</text>')
    for level, color in enumerate(colors["levels"]):
        out.append(f'<rect x="{1145 + level * 21}" y="283" width="15" height="15" rx="4" fill="{color}"/>')
    out.append('<text x="1250" y="297">More</text>')
    out.append('</g></g></svg>')
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default="32KZ")
    parser.add_argument("--html", type=Path, help="Use a previously downloaded public calendar (offline)")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "assets")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", args.user):
        parser.error("Invalid GitHub username")
    if args.html:
        html = args.html.read_text(encoding="utf-8")
    else:
        request = Request(f"https://github.com/users/{args.user}/contributions",
                          headers={"User-Agent": "github-profile-calendar", "Accept-Language": "en-US"})
        with urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8")
    calendar_parser = CalendarParser()
    calendar_parser.feed(html)
    total, days = calendar_parser.result()
    # Validate and render everything before replacing any last-good output.
    images = {theme: render(total, days, args.user, theme) for theme in THEMES}
    args.output.mkdir(parents=True, exist_ok=True)
    for theme, svg in images.items():
        target = args.output / f"contributions-{theme}.svg"
        temporary = target.with_suffix(".tmp")
        temporary.write_text(svg, encoding="utf-8", newline="\n")
        temporary.replace(target)
    print(f"Generated {len(images)} calendars: {total} contributions across {len(days)} days, through {days[-1][0]}.")


if __name__ == "__main__":
    main()
