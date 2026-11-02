#!/usr/bin/env python3
"""Checks particular to the AI in Excel course.

Three documents that have to agree with each other: the notes are numbered
sections, the running order is a minute-by-minute timetable that cites them,
and the trainer manual cites both. None of that applies to a course built
differently, which is why it lives here rather than in validate_docs.py.

validate_docs.py imports this file and calls check(course). What it checks:

  * the running order's arithmetic - every start time is the one before it
    plus its duration, each session heading matches its own rows, and the
    last segment ends when the course says it finishes
  * segments numbered 1, 2, 3 ... without a gap
  * every "Notes section" the running order cites, and every "Notes §N" and
    "Segment N" the trainer manual cites, exists
  * the trainer manual's checkpoint times are real segment start times

Run it through validate_docs.py, not on its own:

    python validate_docs.py --course ai_in_excel_2026
"""

from __future__ import annotations

import re

# The names the course's document_settings.toml gives its three documents.
NOTES = "notes"
ORDER = "running-order"
TRAINER = "trainer"

DASHES = "–—-"          # en dash, em dash, hyphen
DASH_RE = f"[{DASHES}]"


def check(course) -> None:
    """Everything this course needs checking. Called by validate_docs.py."""
    notes_text = course.text(NOTES)
    order_text = course.text(ORDER)
    trainer_text = course.text(TRAINER)

    missing = [name for name, text in
               ((NOTES, notes_text), (ORDER, order_text), (TRAINER, trainer_text))
               if not text]
    if missing:
        course.error("document_settings.toml has no document named "
                     + ", ".join(repr(m) for m in missing)
                     + ", so this course's own checks cannot run")
        return

    sections = parse_note_sections(notes_text)
    segments, sessions = parse_running_order(order_text)

    check_timings(course, segments, sessions)
    check_segment_numbering(course, segments)
    check_order_refs(course, segments, sections)
    check_trainer_refs(course, trainer_text, sections, segments)
    check_checkpoints(course, trainer_text, segments)

    numbered = [s for s in segments if not s.is_break]
    course.note(f"  checked {len(sections)} notes sections, {len(numbered)} "
                f"segments across {len(sessions)} sessions.")


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------

def parse_note_sections(text: str) -> dict[str, str]:
    """Map section number -> heading title.

    Top-level sections are written '## 4. Formulas with AI' (number, full stop)
    and subsections '### 4.1 Create a formula' (number, no full stop).
    Unnumbered headings such as '### Why now?' are not cross-referenced and are
    ignored.
    """
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


class Segment:
    def __init__(self, num: str, start: str, mins: int, name: str,
                 refs_raw: str, line_no: int, session: int):
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

    def __repr__(self) -> str:
        return f"<Segment {self.num} {self.start} {self.name!r}>"


ROW_RE = re.compile(
    r"^\|\s*([0-9]+|[" + DASHES + r"])\s*"      # segment number, or a dash
    r"\|\s*(\d{1,2}:\d{2})\s*"                  # start time
    r"\|\s*(\d+)\s*"                            # minutes
    r"\|\s*(.*?)\s*"                            # segment name
    r"\|\s*(.*?)\s*"                            # Notes section column
    r"\|.*\|\s*$"                               # what to cover
)

SESSION_RE = re.compile(
    r"^##\s+Session\s+(\d+)\s*.*\((\d{1,2}:\d{2})\s*" + DASH_RE + r"\s*(\d{1,2}:\d{2})\)"
)


def parse_running_order(text: str) -> tuple[list[Segment], dict[int, tuple[str, str]]]:
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
                Segment(num, start, int(mins), strip_md(name), refs, i, session)
            )
    return segments, sessions


def strip_md(s: str) -> str:
    """Drop bold/italic markers so names can be compared as plain text."""
    return re.sub(r"[*_`]", "", s).strip()


def minutes(hhmm_str: str) -> int:
    h, m = hhmm_str.split(":")
    return int(h) * 60 + int(m)


def hhmm(total: int) -> str:
    return f"{total // 60:02d}:{total % 60:02d}"


def expand_refs(course, raw: str) -> list[str]:
    """Turn a 'Notes section' cell into a list of section numbers.

    Handles '1', '1, 2', '4.2-4.3', '1-7', '10.3-10.4' and an em dash or an
    empty cell meaning 'no section'.
    """
    raw = strip_md(raw)
    if not raw or re.fullmatch(DASH_RE, raw):
        return []
    out: list[str] = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*" + DASH_RE + r"\s*(\d+(?:\.\d+)?)", token)
        if m:
            out.extend(expand_range(course, m.group(1), m.group(2), token))
        elif re.fullmatch(r"\d+(?:\.\d+)?", token):
            out.append(token)
        else:
            course.warn(
                f"running order: could not read Notes section reference {token!r}")
    return out


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


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_timings(course, segments: list[Segment],
                  sessions: dict[int, tuple[str, str]]) -> None:
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
                f"so it should start at {hhmm(expected)}"
            )

    last = segments[-1]
    finish = hhmm(minutes(last.start) + last.mins)
    if sessions:
        declared = sessions[max(sessions)][1]
        if finish != declared:
            course.error(
                f"running order: the last segment ends at {finish}, but the "
                f"session heading says the course finishes at {declared}"
            )

    # Each session heading's start and end should match its own rows.
    for num, (start, end) in sorted(sessions.items()):
        rows = [s for s in segments if s.session == num]
        if not rows:
            course.error(f"running order: session {num} heading has no segment rows")
            continue
        if rows[0].start != start:
            course.error(
                f"running order: session {num} heading says it starts at "
                f"{start}, but its first row starts at {rows[0].start}"
            )
        # The coffee break is listed inside session 1 but falls after it ends,
        # so the session's end time comes from the last taught segment.
        taught = [s for s in rows if not s.is_break] or rows
        row_end = hhmm(minutes(taught[-1].start) + taught[-1].mins)
        if row_end != end:
            course.error(
                f"running order: session {num} heading says it ends at {end}, "
                f"but its last row ends at {row_end}"
            )


def check_segment_numbering(course, segments: list[Segment]) -> None:
    numbered = [s for s in segments if not s.is_break]
    expected = 1
    for seg in numbered:
        if int(seg.num) != expected:
            course.error(
                f"running order line {seg.line_no}: segment numbered {seg.num}, "
                f"expected {expected}"
            )
            expected = int(seg.num)
        expected += 1


def check_order_refs(course, segments: list[Segment], sections: dict[str, str]) -> None:
    referenced: set[str] = set()
    for seg in segments:
        for ref in expand_refs(course, seg.refs_raw):
            referenced.add(ref)
            if ref not in sections:
                course.error(
                    f"running order line {seg.line_no}: segment {seg.num} "
                    f"({seg.name}) cites Notes section {ref}, which does not exist"
                )
    # A section cited only through its subsections (9.1, 9.2 ...) counts as
    # covered.
    covered = {r.split(".")[0] for r in referenced}
    top_level = {s for s in sections if "." not in s}
    unreferenced = sorted(top_level - covered, key=int)
    if unreferenced:
        course.warn(
            "notes sections never cited by the running order: "
            + ", ".join(f"section {s} ({sections[s]})" for s in unreferenced)
        )


def check_trainer_refs(course, trainer: str, sections: dict[str, str],
                       segments: list[Segment]) -> None:
    valid_segments = {s.num for s in segments if not s.is_break}

    for m in re.finditer(r"§\s*(\d+(?:\.\d+)?)", trainer):
        ref = m.group(1)
        if ref not in sections:
            course.error(
                f"trainer manual line {line_of(trainer, m.start())}: "
                f"cites Notes section {ref}, which does not exist"
            )

    pattern = r"Segments?\s+(\d+)(?:\s*" + DASH_RE + r"\s*(\d+))?"
    for m in re.finditer(pattern, trainer):
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else lo
        for n in range(lo, hi + 1):
            if str(n) not in valid_segments:
                course.error(
                    f"trainer manual line {line_of(trainer, m.start())}: "
                    f"cites Segment {n}, which is not in the running order"
                )


def check_checkpoints(course, trainer: str, segments: list[Segment]) -> None:
    """The trainer manual's checkpoint times must be real segment start times."""
    starts = {s.start for s in segments}
    finish = hhmm(minutes(segments[-1].start) + segments[-1].mins) if segments else None

    in_table = False
    for i, line in enumerate(trainer.splitlines(), start=1):
        if line.startswith("### Checkpoints"):
            in_table = True
            continue
        if in_table and line.startswith("###"):
            break
        if not in_table:
            continue
        m = re.match(r"^\|\s*(\d{1,2}:\d{2})\s*\|\s*(.*?)\s*\|\s*$", line)
        if not m:
            continue
        time, label = m.group(1), strip_md(m.group(2))
        if time in starts or time == finish:
            continue
        if "at the latest" in label.lower():
            continue
        course.error(
            f"trainer manual line {i}: checkpoint {time} ({label}) is not the "
            f"start time of any segment, nor the finish time"
        )
