#!/usr/bin/env python3
"""Checks particular to the AI-Driven Data Automation course.

Two documents that have to agree: the notes are numbered sections, and the
running order is a timetable whose Notes § column points into them. None of
that applies to a course built differently, which is why it lives here
rather than in validate_docs.py.

validate_docs.py imports this file and calls check(course). What it checks:

  * the running order's arithmetic - every start time is the one before it
    plus its duration, and each session heading matches its own rows
  * segments numbered 1, 2, 3 ... without a gap
  * every Notes § the running order cites exists in the notes

The notes are written section by section with /flesh-out, so an empty Notes §
column is not an error - it is the normal state of a course still being
written. A reference to a section that does not exist is.

Run it through validate_docs.py, not on its own:

    python validate_docs.py --course ai_driven_data_automation
"""

from __future__ import annotations

import re

# The names this course's document_settings.toml gives its documents.
NOTES = "notes"
ORDER = "running-order"

DASHES = "–—-"          # en dash, em dash, hyphen
DASH_RE = f"[{DASHES}]"

ROW_RE = re.compile(
    r"^\|\s*([0-9]+|[" + DASHES + r"])\s*"      # segment number, or a dash
    r"\|\s*(\d{1,2}:\d{2})\s*"                  # start time
    r"\|\s*(\d+)\s*"                            # minutes
    r"\|\s*(.*?)\s*"                            # segment name
    r"\|\s*(.*?)\s*"                            # Notes section column
    r"\|.*\|\s*$"                               # what to cover
)

SESSION_RE = re.compile(
    r"^##\s+Session\s+(\d+)\s*.*\((\d{1,2}:\d{2})\s*" + DASH_RE
    + r"\s*(\d{1,2}:\d{2})\)"
)


def check(course) -> None:
    """Everything this course needs checking. Called by validate_docs.py."""
    order_text = course.text(ORDER)
    if not order_text:
        course.error(f"no document named {ORDER!r}, so the timetable cannot "
                     f"be checked")
        return

    segments, sessions = parse_running_order(order_text)
    check_timings(course, segments, sessions)
    check_segment_numbering(course, segments)
    check_order_refs(course, segments, parse_note_sections(course.text(NOTES)))

    taught = [s for s in segments if not s.is_break]
    if taught:
        finish = hhmm(minutes(segments[-1].start) + segments[-1].mins)
        course.note(f"  checked {len(taught)} segments across "
                    f"{len(sessions)} sessions, finishing at {finish}.")


class Segment:
    def __init__(self, num, start, mins, name, refs_raw, line_no, session):
        self.num = num
        self.start = start
        self.mins = mins
        self.name = name
        self.refs_raw = refs_raw
        self.line_no = line_no
        self.session = session

    @property
    def is_break(self) -> bool:
        return not self.num.isdigit()


def parse_running_order(text: str):
    segments: list[Segment] = []
    sessions: dict[int, tuple[str, str]] = {}
    session = 0
    for i, line in enumerate(text.splitlines(), start=1):
        m = SESSION_RE.match(line)
        if m:
            session = int(m.group(1))
            sessions[session] = (m.group(2), m.group(3))
            continue
        m = ROW_RE.match(line)
        if m:
            num, start, mins, name, refs = m.groups()
            segments.append(
                Segment(num, start, int(mins), strip_md(name), refs, i, session))
    return segments, sessions


def parse_note_sections(text: str) -> dict[str, str]:
    """Map section number -> heading title, from '## 4. Title' and '### 4.1 Title'."""
    sections: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^##\s+(\d+)\.\s+(.*)$", line)
        if m:
            sections[m.group(1)] = m.group(2).strip()
            continue
        m = re.match(r"^###\s+(\d+\.\d+)\s+(.*)$", line)
        if m:
            sections[m.group(1)] = m.group(2).strip()
    return sections


def strip_md(s: str) -> str:
    return re.sub(r"[*_`]", "", s).strip()


def minutes(hhmm_str: str) -> int:
    h, m = hhmm_str.split(":")
    return int(h) * 60 + int(m)


def hhmm(total: int) -> str:
    return f"{total // 60:02d}:{total % 60:02d}"


def check_timings(course, segments, sessions) -> None:
    """Each start time must equal the previous start plus the previous duration."""
    if not segments:
        course.error("running order: no segment rows found")
        return

    for prev, cur in zip(segments, segments[1:]):
        expected = minutes(prev.start) + prev.mins
        if minutes(cur.start) != expected:
            course.error(
                f"running order line {cur.line_no}: segment {cur.num} "
                f"({cur.name}) starts at {cur.start}, but segment {prev.num} "
                f"starts at {prev.start} and runs {prev.mins} min, "
                f"so it should start at {hhmm(expected)}")

    for num, (start, end) in sorted(sessions.items()):
        rows = [s for s in segments if s.session == num]
        if not rows:
            course.error(f"running order: session {num} heading has no rows")
            continue
        if rows[0].start != start:
            course.error(
                f"running order: session {num} heading says it starts at "
                f"{start}, but its first row starts at {rows[0].start}")
        # A break is listed inside the session it follows, so the session's
        # end time comes from the last taught segment.
        taught = [s for s in rows if not s.is_break] or rows
        row_end = hhmm(minutes(taught[-1].start) + taught[-1].mins)
        if row_end != end:
            course.error(
                f"running order: session {num} heading says it ends at {end}, "
                f"but its last row ends at {row_end}")


def check_segment_numbering(course, segments) -> None:
    expected = 1
    for seg in (s for s in segments if not s.is_break):
        if int(seg.num) != expected:
            course.error(
                f"running order line {seg.line_no}: segment numbered "
                f"{seg.num}, expected {expected}")
            expected = int(seg.num)
        expected += 1


def check_order_refs(course, segments, sections: dict[str, str]) -> None:
    """Every Notes § cited must exist. An empty column is fine while writing."""
    cited = 0
    for seg in segments:
        raw = strip_md(seg.refs_raw)
        if not raw or re.fullmatch(DASH_RE, raw):
            continue
        for token in (t.strip() for t in raw.split(",")):
            if not token:
                continue
            m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*" + DASH_RE
                             + r"\s*(\d+(?:\.\d+)?)", token)
            refs = expand_range(course, m.group(1), m.group(2), token) if m \
                else [token] if re.fullmatch(r"\d+(?:\.\d+)?", token) else []
            if not refs:
                course.warn(f"running order line {seg.line_no}: could not read "
                            f"Notes section reference {token!r}")
            for ref in refs:
                cited += 1
                if ref not in sections:
                    course.error(
                        f"running order line {seg.line_no}: segment {seg.num} "
                        f"({seg.name}) cites Notes section {ref}, which does "
                        f"not exist")
    if sections and not cited:
        course.warn("the notes have numbered sections, but the running "
                    "order's Notes § column is still empty")


def expand_range(course, lo: str, hi: str, token: str) -> list[str]:
    if "." in lo and "." in hi:
        lo_major, lo_minor = lo.split(".")
        hi_major, hi_minor = hi.split(".")
        if lo_major != hi_major:
            course.warn(f"running order: cross-section range {token!r} not expanded")
            return [lo, hi]
        return [f"{lo_major}.{n}" for n in range(int(lo_minor), int(hi_minor) + 1)]
    if "." not in lo and "." not in hi:
        return [str(n) for n in range(int(lo), int(hi) + 1)]
    course.warn(f"running order: mixed-depth range {token!r} not expanded")
    return [lo, hi]
