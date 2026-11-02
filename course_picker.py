#!/usr/bin/env python3
"""Ask which courses to build, when the command line does not say.

Run `python build_deliverables.py` with no arguments and this puts up a list
of the courses to tick off:

    ? Which courses would you like to build?
    > [x] ai_in_excel_2026     3 documents, 2 files, last built 29/10/2026
      [ ] data_analysis_2027   2 documents, never built

A single course is listed too, ticked already - seeing what is there and
when it was last built is worth the keystroke - so Enter builds it.

Space ticks a course, A ticks them all, Enter builds what is ticked.

The list is drawn with questionary (pip install questionary), but the build
does not depend on it: without it, or when the output is not a terminal - a
scheduled build, a pipe, a CI job - this falls back to a plain numbered
prompt, and to building everything when there is nobody there to ask.
"""

from __future__ import annotations

import sys
from datetime import datetime


def _describe(course) -> str:
    """The one-line summary beside a course's name."""
    bits = [f"{len(course.documents)} document"
            + ("s" if len(course.documents) != 1 else "")]
    if course.files and course.files.is_dir():
        count = sum(1 for p in course.files.iterdir() if p.is_file())
        if count:
            bits.append(f"{count} file" + ("s" if count != 1 else ""))

    # When it was last built, which is the thing you actually want to know
    # when deciding whether to build it again.
    pdfs = sorted(course.deliverables.glob("*.pdf")) if course.deliverables.is_dir() else []
    if pdfs:
        built = max(p.stat().st_mtime for p in pdfs)
        bits.append("last built " + datetime.fromtimestamp(built).strftime("%d/%m/%Y %H:%M"))
    else:
        bits.append("never built")
    return ", ".join(bits)


def _ask_with_questionary(courses, **kwargs):
    import questionary

    rows = [
        questionary.Choice(
            title=f"{course.name:<22} {_describe(course)}",
            value=course,
            # A lone course is ticked already, so Enter builds it: the list
            # is still shown, because seeing what is there and when it was
            # last built is worth a keystroke.
            checked=len(courses) == 1,
        )
        for course in courses
    ]
    picked = questionary.checkbox(
        "Which courses would you like to build?",
        choices=rows,
        instruction="(space to tick, a for all, enter to build)",
        # kwargs is how a test drives the list without a terminal: questionary
        # takes a prompt_toolkit input and output.
        **kwargs,
    ).ask()
    # ask() returns None when the question is cancelled with Ctrl-C.
    return picked


def _ask_with_input(courses):
    """The same question without questionary: a numbered list and a prompt."""
    print("Courses:")
    for i, course in enumerate(courses, start=1):
        print(f"  {i}. {course.name:<22} {_describe(course)}")
    print()
    answer = input("Which would you like to build? "
                   "(numbers like 1,3 - or 'all', blank to cancel) ").strip()
    if not answer:
        return []
    if answer.lower() in {"a", "all"}:
        return list(courses)
    picked = []
    for token in answer.replace(" ", ",").split(","):
        if not token:
            continue
        if not token.isdigit() or not 1 <= int(token) <= len(courses):
            print(f"  {token!r} is not one of the numbers listed.")
            return None
        picked.append(courses[int(token) - 1])
    return picked


def choose_courses(courses, interactive: bool | None = None, **kwargs):
    """Which of these courses to build. [] means the person said none.

    Returns None if they cancelled, which the caller should treat as "stop",
    and every course when there is nobody to ask. `interactive` is for tests,
    which have a scripted keyboard but no terminal; left alone, it is decided
    by whether there is one.
    """
    if interactive is None:
        interactive = sys.stdin.isatty() and sys.stdout.isatty()
    if not interactive:
        return list(courses)        # a pipe or a scheduled run: build them all

    try:
        picked = _ask_with_questionary(courses, **kwargs)
    except ImportError:
        print("  (install questionary for a nicer list: pip install questionary)\n")
        picked = _ask_with_input(courses)
    except (KeyboardInterrupt, EOFError):
        return None
    return picked
