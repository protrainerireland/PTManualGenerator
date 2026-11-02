#!/usr/bin/env python3
"""Consistency checks for a course's documents.

There is no build or test step for this project, so this script stands in for
one. It checks what can be checked about any course - that the settings make
sense, and that every image a document asks for is really there - and then
hands over to the course's own checks, if it has any.

A course's own checks live in validate_course.py in its folder, and are the
place for anything particular to it: this course's running order has to add
up to 13:30, which is no business of a course that has no running order. That
file is optional; a course without one is checked only by what is here.

    python validate_docs.py                          check every course
    python validate_docs.py --course ai_in_excel_2026

Exit status is 0 if nothing is wrong, 1 if there are errors. Warnings do not
fail the run.
"""

from __future__ import annotations

import sys

# This is an authoring folder, not a code tree: importing the build script to
# share its settings loader should not leave a __pycache__ behind in it.
sys.dont_write_bytecode = True

import argparse
import importlib.util
import re
from pathlib import Path

from build_deliverables import HERE, SETTINGS_NAME, find_courses

HOOK_NAME = "validate_course.py"

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}


class CourseDocs:
    """One course's documents, and somewhere to report what is wrong with them.

    This is what a course's own validate_course.py is handed. Its documents
    are keyed by the names their settings give them - "notes", "trainer" -
    rather than by filename, so that a course can rename a file without
    rewriting its checks.
    """

    def __init__(self, course):
        self.course = course
        self.name = course.name
        self.folder = course.folder
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []
        self.docs: dict[str, str] = {}
        for document in course.documents:
            self.docs[document.name] = (
                course.folder / document.file).read_text(encoding="utf-8")

    def text(self, name: str) -> str:
        """One document by name, or "" if this course has no such document."""
        return self.docs.get(name, "")

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        """Something worth saying that is not a complaint - what was checked."""
        self.notes.append(msg)


def check_images(docs: CourseDocs) -> None:
    """Every image a document asks for exists; note any that nothing uses."""
    course = docs.course
    folder_name = course.images.name
    if not course.images.is_dir():
        if any(f"{folder_name}/" in text for text in docs.docs.values()):
            docs.error(f"missing {folder_name}/ folder")
        return

    # Only pictures count towards "nothing uses this": a README explaining
    # what the folder is for is not an orphaned screenshot.
    on_disk = {p.name for p in course.images.iterdir()
               if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES}
    used: set[str] = set()

    # Markdown images, and the raw <img> tags the cover page uses so that it
    # can carry a class for the stylesheet to size the logos by.
    pattern = (r"!\[[^\]]*\]\(" + re.escape(folder_name) + r"/([^)]+)\)"
               r"|<img[^>]+src=[\"']" + re.escape(folder_name) + r"/([^\"']+)[\"']")

    sources = dict(docs.docs)
    # The client logo is named in the settings rather than in any document,
    # so it has to be counted here or it would look orphaned.
    if course.client_logo:
        sources[SETTINGS_NAME] = f"![client logo]({course.client_logo})"

    for name, text in sources.items():
        for m in re.finditer(pattern, text):
            filename = m.group(1) or m.group(2)
            used.add(filename)
            if filename not in on_disk:
                line = text.count("\n", 0, m.start()) + 1
                docs.error(f"{name} line {line}: "
                           f"{folder_name}/{filename} does not exist")

    orphans = sorted(on_disk - used)
    if orphans:
        docs.warn("images not used by any current document: " + ", ".join(orphans))


def check_cover(docs: CourseDocs) -> None:
    """The cover's own files exist, wherever the cover itself lives.

    A shared cover sits beside the courses and refers to files of its own -
    the Professional Training logo - so its paths are resolved against its
    own folder, not against the course's images.
    """
    cover = docs.course.cover_page
    if not cover:
        return
    text = cover.read_text(encoding="utf-8")
    pattern = r"!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src=[\"']([^\"']+)[\"']"
    for m in re.finditer(pattern, text):
        url = m.group(1) or m.group(2)
        if re.match(r"^([a-z]+:|/|#|\{\{)", url, re.I):
            continue        # a URL, an anchor, or a placeholder filled later
        if not (cover.parent / url).exists():
            line = text.count("\n", 0, m.start()) + 1
            docs.error(f"{cover.name} line {line}: {url} does not exist "
                       f"(looked beside {cover.name})")


def check_settings(docs: CourseDocs) -> None:
    """The handful of settings that can be wrong without stopping the build."""
    course = docs.course
    if not course.cover_title:
        docs.warn(f"{SETTINGS_NAME} sets no cover_title, so the covers are "
                  f"headed by nothing")
    if course.files and not any(course.files.iterdir()):
        docs.warn(f"{course.files.name}/ is empty, so the zip would be too")


def run_course_checks(docs: CourseDocs) -> None:
    """The course's own validate_course.py, if it has one."""
    hook = docs.folder / HOOK_NAME
    if not hook.exists():
        return
    spec = importlib.util.spec_from_file_location(
        f"{docs.name}_checks", hook)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        docs.error(f"{HOOK_NAME} could not be loaded: {exc}")
        return
    check = getattr(module, "check", None)
    if check is None:
        docs.error(f"{HOOK_NAME} has no check(course) function, so its "
                   f"checks were not run")
        return
    check(docs)


def report(docs: CourseDocs, show_name: bool) -> None:
    if show_name:
        print(f"=== {docs.name} ===")
    for msg in docs.notes:
        print(msg)
    for msg in docs.errors:
        print(f"  ERROR: {msg}")
    for msg in docs.warnings:
        print(f"  warning: {msg}")
    if docs.errors:
        print(f"{len(docs.errors)} error(s), {len(docs.warnings)} warning(s).")
    elif docs.warnings:
        print(f"{len(docs.warnings)} warning(s), no errors.")
    else:
        print("No errors.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a course's documents for consistency.")
    parser.add_argument(
        "--course",
        help="check just this course (a folder name under courses/); "
             "the default is to check them all")
    args = parser.parse_args()

    courses = find_courses(args.course)
    failed = False
    for course in courses:
        docs = CourseDocs(course)
        check_settings(docs)
        check_cover(docs)
        check_images(docs)
        run_course_checks(docs)
        report(docs, show_name=len(courses) > 1)
        failed = failed or bool(docs.errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
