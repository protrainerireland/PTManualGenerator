#!/usr/bin/env python3
"""Build a course's deliverables: PDFs of its documents, plus a zip of its files.

This script knows how to turn Markdown into a branded PDF. It knows nothing
about any particular course: what to build comes from the
document_settings.toml in each folder under courses/, and how it looks comes
from tools/styles/professional_training_styles.css. Both are shared by every
course; neither is edited to add one.

    courses/<course>/document_settings.toml   what this course builds
    courses/<course>/*.md                     its documents
    courses/<course>/images/                  its screenshots
    courses/<course>/files/                   its workbooks and hand-outs
    courses/<course>/deliverables/            where the output lands

Usage:

    python build_deliverables.py                   build every course
    python build_deliverables.py --course ai_in_excel_2026
    python build_deliverables.py --only trainer    one document
    python build_deliverables.py --no-zip          skip the file zip
    python build_deliverables.py --skip-validate   build despite doc errors

Each course is validated first (see validate_docs.py); errors stop the build.
Exit status is 0 on success, 1 on failure.
"""

from __future__ import annotations

import sys

# An authoring folder, not a code tree: no __pycache__ litter in it.
sys.dont_write_bytecode = True

import argparse
import datetime
import os
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from course_picker import choose_courses

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"
COURSES = HERE / "courses"
RENDERER = TOOLS / "render_md.js"
PRINTER = TOOLS / "print_pdf.js"
VALIDATOR = HERE / "validate_docs.py"

# The cover layout, shared by every course unless one keeps its own copy.
SHARED_COVER = HERE / "cover_page.md"

SETTINGS_NAME = "document_settings.toml"

# Everything a course hands out, other than its documents: workbooks,
# datasets, whatever else. Only these are zipped.
HANDOUT_SUFFIXES = {".xlsx", ".xlsm", ".xls", ".csv", ".docx", ".pptx", ".pdf", ".txt"}

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

# The date the covers carry, as dd/mm/yyyy. Settled once per run, so that a
# build straddling midnight cannot date one document a day after another.
PUBLISHED = datetime.date.today().strftime("%d/%m/%Y")

TOC_MARKER = "<!-- toc -->"

# Anything printed below this height, in points from the foot of the page,
# belongs to the footer rather than to the document.
FOOTER_BAND = 40


def fail(msg: str) -> None:
    print(f"  ERROR: {msg}")
    sys.exit(1)


def as_html_lines(text: str) -> str:
    """Turn the line breaks written into a cover setting into <br>.

    So a title can be split where it reads best, by writing a newline escape
    in document_settings.toml (or using a TOML multi-line string). The
    conversion happens here rather than in the renderer because the value
    travels as a command-line argument, and a newline inside one of those is
    not safe to pass through a Windows shell.
    """
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n")]
    return "<br>".join(line for line in lines if line)


class Document:
    """One document of a course, as its settings describe it.

    `output` is what the PDF is called. It defaults to the Markdown file's
    own name, so a source file can be short and working ("notes.md") while
    the file handed over is formal ("AI in Excel - Participant Manual.pdf").
    """

    def __init__(self, name: str, file: str, subtitle: str, output: str):
        self.name = name
        self.file = file
        self.subtitle = subtitle
        self.output = output

    def __repr__(self) -> str:
        return f"<Document {self.name} {self.file} -> {self.output}>"


class Course:
    """One folder under courses/, as its document_settings.toml describes it.

    Kept deliberately forgiving to read and strict to validate: the settings
    file is meant to be edited by whoever maintains the course, not by a
    programmer, so a mistake in it should name itself rather than surface as
    a stack trace or, worse, a quietly wrong cover.
    """

    def __init__(self, folder: Path, raw: dict):
        self.folder = folder
        self.name = folder.name
        where = f"{self.name}/{SETTINGS_NAME}"

        # The images folder is settled first: a client logo given as a bare
        # filename is looked for inside it.
        self.images = folder / (raw.get("images") or "images")

        self.cover_title = as_html_lines(raw.get("cover_title", ""))
        self.cover_page = self._find_cover(raw.get("cover_page"), where)
        self.client_logo = self._find_client_logo(raw.get("client_logo"), where)

        self.footer_link_text = (raw.get("footer_link_text") or "").strip()
        self.footer_link_url = (raw.get("footer_link_url") or "").strip()
        if self.footer_link_url and not self.footer_link_text:
            fail(f"{where} sets footer_link_url with no footer_link_text to "
                 f"print it on")

        files_name = raw.get("files")
        self.files = folder / files_name if files_name else None
        if self.files and not self.files.is_dir():
            fail(f"{where} sets files to {files_name}, which is not a folder")
        self.zip_name = raw.get("zip_name") or f"{self.name}.zip"
        self.deliverables = folder / "deliverables"

        self.documents = self._read_documents(raw.get("documents"), where)

    def _find_cover(self, name: str | None, where: str) -> Path | None:
        """The course's own cover layout if it has one, else the shared one."""
        if name is None:
            name = SHARED_COVER.name
        if not name:
            return None
        own = self.folder / name
        if own.exists():
            return own
        shared = HERE / name
        if shared.exists():
            return shared
        fail(f"{where} points at {name}, which is in neither {self.name}/ "
             f"nor the project root")
        raise AssertionError("unreachable")

    def _find_client_logo(self, logo: str | None, where: str) -> str | None:
        """A path relative to the course folder, as the renderer wants it.

        A bare filename means the images folder. Either way it has to exist:
        a cover silently missing the client's logo is worse than a build that
        stops.
        """
        logo = (logo or "").strip()
        if not logo:
            return None
        if "/" not in logo and "\\" not in logo:
            logo = f"{self.images.name}/{logo}"
        if not (self.folder / logo).exists():
            fail(f"{where} sets client_logo to {logo}, which does not exist")
        return logo

    def _read_documents(self, entries, where: str) -> list[Document]:
        if not entries:
            fail(f"{where} lists no documents to build")
        documents: list[Document] = []
        seen: set[str] = set()
        outputs: dict[str, str] = {}
        for i, entry in enumerate(entries, start=1):
            at = f"document {i} in {where}"
            name = entry.get("name")
            filename = entry.get("file")
            if not name or not filename:
                fail(f"{at} needs both a name and a file")
            if name in seen:
                fail(f"{at} repeats the name {name!r}")
            seen.add(name)
            if not (self.folder / filename).exists():
                fail(f"{at} points at {filename}, which does not exist")

            output = (entry.get("output") or "").strip()
            if not output:
                output = Path(filename).stem + ".pdf"
            if not output.lower().endswith(".pdf"):
                output += ".pdf"
            if "/" in output or "\\" in output:
                fail(f"{at} gives output as {output!r}: it names a file in "
                     f"deliverables/, not a path")
            if output in outputs:
                fail(f"{at} would write {output}, which document "
                     f"{outputs[output]!r} already writes")
            outputs[output] = name

            documents.append(Document(
                name, filename, as_html_lines(entry.get("subtitle", "")), output))
        return documents


def load_course(folder: Path) -> Course:
    try:
        import tomllib
    except ModuleNotFoundError:  # Python 3.10 and earlier
        fail(f"reading {SETTINGS_NAME} needs Python 3.11 or newer")

    settings_file = folder / SETTINGS_NAME
    if not settings_file.exists():
        fail(f"{folder.name}/ has no {SETTINGS_NAME}, so there is nothing to "
             f"say what to build")
    try:
        with settings_file.open("rb") as handle:
            raw = tomllib.load(handle)
    except Exception as exc:  # a syntax error in the settings file
        fail(f"{folder.name}/{SETTINGS_NAME} could not be read: {exc}")
    return Course(folder, raw)


def find_courses(wanted: list[str] | str | None = None) -> list[Course]:
    """Every course under courses/, or the one named.

    A folder is a course if it holds a settings file; anything else there -
    notes to self, a folder of source material - is passed over in silence.
    A folder whose name begins with _ is skipped as well, which is what
    keeps courses/_template from being built, and leaves an obvious way to
    park a course that should not be built for now.
    """
    if not COURSES.is_dir():
        fail(f"missing {COURSES.name}/ folder, which holds the courses")
    folders = sorted(
        p for p in COURSES.iterdir()
        if p.is_dir() and not p.name.startswith("_")
        and (p / SETTINGS_NAME).exists()
    )
    if not folders:
        fail(f"no courses found in {COURSES.name}/ (a course is a folder "
             f"containing {SETTINGS_NAME})")
    if wanted:
        names = [wanted] if isinstance(wanted, str) else list(wanted)
        known = sorted(p.name for p in COURSES.iterdir() if p.is_dir())
        for name in names:
            if name not in {p.name for p in folders}:
                fail(f"no course called {name!r} in {COURSES.name}/ "
                     f"(found: {', '.join(known)})")
        folders = [p for p in folders if p.name in names]
    return [load_course(folder) for folder in folders]


def find_chrome() -> str:
    """Chrome or Edge, either of which can print a page to PDF."""
    override = os.environ.get("CHROME")
    if override:
        if Path(override).exists():
            return override
        fail(f"CHROME is set to {override}, which does not exist")
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    for name in ("chrome", "chrome.exe", "msedge", "msedge.exe"):
        found = shutil.which(name)
        if found:
            return found
    fail(
        "could not find Chrome or Edge. Set the CHROME environment variable to "
        "the browser executable."
    )
    raise AssertionError("unreachable")


def ensure_node_modules() -> None:
    """Install the renderer's dependencies on first run."""
    if (TOOLS / "node_modules" / "markdown-it").is_dir():
        return
    if not shutil.which("npm"):
        fail("npm is not on PATH, so the renderer's dependencies cannot be installed")
    print("  installing renderer dependencies (first run only)...")
    result = subprocess.run(
        ["npm", "install", "--no-audit", "--no-fund", "--loglevel=error"],
        cwd=TOOLS,
        shell=(os.name == "nt"),
    )
    if result.returncode != 0:
        fail("npm install failed")


def validate(course: Course) -> None:
    if not VALIDATOR.exists():
        print("  warning: validate_docs.py not found, skipping validation")
        return
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--course", course.name], cwd=HERE)
    if result.returncode != 0:
        fail(
            "document validation failed (see above). Fix the documents, or "
            "re-run with --skip-validate to build anyway."
        )


def squash(text: str) -> str:
    """Text with all whitespace removed, for comparing against a PDF.

    Extracted PDF text breaks lines and spaces words unpredictably, so both
    sides of every comparison go through this.
    """
    return "".join(text.split())


def section_pages(pdf_path: Path, sections: list[dict]) -> dict[str, int]:
    """The printed page each numbered section starts on, keyed by section id.

    Page numbers are the ones the footer shows, counting the cover as page 1.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        fail(
            "the contents page needs pypdf to find the page numbers "
            "(pip install pypdf)"
        )
    texts = [squash(page.extract_text() or "") for page in PdfReader(pdf_path).pages]

    needles = [squash(s["number"] + ". " + s["title"]) for s in sections]

    # Skip the contents page itself: it is the only page carrying both the
    # first and the last section title.
    first_body = 0
    for i, text in enumerate(texts):
        if needles[0] in text and needles[-1] in text:
            first_body = i + 1

    pages: dict[str, int] = {}
    at = first_body
    for section, needle in zip(sections, needles):
        for i in range(at, len(texts)):
            if needle in texts[i]:
                pages[section["id"]] = i + 1
                at = i
                break
        else:
            fail(
                f"could not find section {section['number']} "
                f"({section['title']}) in the printed PDF"
            )
    return pages


def print_html(course: Course, html_path: Path, pdf_path: Path,
               md_name: str, chrome: str) -> None:
    extra = (["--footer-left", course.footer_link_text]
             if course.footer_link_text else [])
    result = subprocess.run(
        ["node", str(PRINTER), chrome, str(html_path), str(pdf_path), *extra],
        cwd=course.folder,
        shell=(os.name == "nt"),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not pdf_path.exists():
        detail = ((result.stderr or "") + (result.stdout or "")).strip().splitlines()
        tail = detail[-1] if detail else "no output"
        fail(f"printing {md_name} to PDF failed: {tail}")


def render_html(course: Course, md_path: Path, html_path: Path,
                subtitle: str, extra: list[str]) -> None:
    """Render one document, with the cover page in front of it."""
    cover: list[str] = []
    if course.cover_page:
        cover = ["--cover", str(course.cover_page),
                 "--title", course.cover_title, "--subtitle", subtitle,
                 "--published", PUBLISHED]
        if course.client_logo:
            cover += ["--client-logo", course.client_logo]
    else:
        print(f"      note: no cover page is configured, so {md_path.name} "
              f"gets none")
    result = subprocess.run(
        ["node", str(RENDERER), str(md_path), str(html_path), *cover, *extra],
        cwd=course.folder,
        shell=(os.name == "nt"),
    )
    if result.returncode != 0:
        fail(f"rendering {md_path.name} to HTML failed")


def add_footer_links(pdf_path: Path, text: str, url: str) -> int:
    """Make the footer's web address clickable, on every page.

    Chrome draws header and footer templates outside the page's own content
    and ignores any link in them, so the words are printed by the template
    and the clickable area is laid over them here. The rectangle is measured
    from where the words actually landed rather than calculated from the
    margins, so it follows the footer if the stylesheet moves it.
    """
    from pypdf import PdfReader, PdfWriter
    from pypdf.annotations import Link

    wanted = squash(text)
    reader = PdfReader(pdf_path)
    writer = PdfWriter(clone_from=reader)
    linked = 0

    for number, page in enumerate(writer.pages):
        runs: list[tuple[float, float, float, str]] = []

        def visit(piece, cm, tm, font_dict, font_size):
            if not piece.strip():
                return
            x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
            y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            size = (font_size or 0) * abs(cm[3] or 1)
            runs.append((x, y, size, piece))

        page.extract_text(visitor_text=visit)
        # The footer sits below everything else on the page. Its pieces are
        # taken left to right and joined until they spell out the address -
        # testing each piece for membership instead would match far too
        # readily: "of", from "Page 3 of 7", is inside "professional".
        footer = sorted((r for r in runs if r[1] < FOOTER_BAND), key=lambda r: r[0])
        hit: list[tuple[float, float, float, str]] = []
        for i, run in enumerate(footer):
            hit, joined = [], ""
            for piece in footer[i:]:
                joined += squash(piece[3])
                hit.append(piece)
                if joined == wanted:
                    break
                if not wanted.startswith(joined):
                    hit = []
                    break
            if hit and joined == wanted:
                break
            hit = []
        if not hit:
            continue
        x0 = min(r[0] for r in hit)
        y = min(r[1] for r in hit)
        size = max(r[2] for r in hit)
        # No width is recorded for a run, so the end of the text is estimated
        # from its length - then held short of whatever is printed next, so a
        # generous estimate cannot reach across the page number.
        x1 = hit[-1][0] + len(hit[-1][3]) * size * 0.55
        after = [r[0] for r in footer if r[0] > hit[-1][0] + 1]
        if after:
            x1 = min(x1, min(after) - 2)
        writer.add_annotation(
            page_number=number,
            annotation=Link(rect=(x0 - 1, y - 2, x1 + 1, y + size + 1), url=url),
        )
        linked += 1

    if linked:
        with pdf_path.open("wb") as handle:
            writer.write(handle)
    return linked


def render_pdf(course: Course, md_path: Path, pdf_path: Path,
               subtitle: str, chrome: str) -> None:
    """Markdown -> HTML -> PDF.

    The intermediate HTML is written beside the source document, not in a temp
    directory, so that its relative image references still resolve. Printing
    goes through tools/print_pdf.js rather than chrome --print-to-pdf, because
    the "Page N of M" footer can only be set over the DevTools protocol.

    A document carrying the <!-- toc --> marker is printed more than once: the
    first pass lays out the contents page with the page numbers left blank,
    which is what tells us where each section fell; the numbers are then filled
    in and it is printed again. Blank or filled, the rows are the same height,
    so the second pass repaginates to the same pages - but it is printed a
    third time if it does not, and the build says so if the numbers never
    settle.
    """
    html_path = md_path.with_suffix(".build.html")
    try:
        with tempfile.TemporaryDirectory() as tmp:
            sections_file = Path(tmp) / "sections.json"
            pages_file = Path(tmp) / "pages.json"

            render_html(course, md_path, html_path, subtitle,
                        ["--sections", str(sections_file)])
            print_html(course, html_path, pdf_path, md_path.name, chrome)

            sections = json.loads(sections_file.read_text(encoding="utf-8"))
            if TOC_MARKER not in md_path.read_text(encoding="utf-8") or not sections:
                return

            previous: dict[str, int] = {}
            for _ in range(3):
                pages = section_pages(pdf_path, sections)
                if pages == previous:
                    return
                previous = pages
                pages_file.write_text(json.dumps(pages), encoding="utf-8")
                render_html(course, md_path, html_path, subtitle,
                            ["--pages", str(pages_file)])
                print_html(course, html_path, pdf_path, md_path.name, chrome)
            if section_pages(pdf_path, sections) != previous:
                print(
                    "      warning: the contents page numbers did not settle; "
                    "check them by hand"
                )
    finally:
        html_path.unlink(missing_ok=True)


def build_zip(course: Course, zip_path: Path) -> list[str]:
    """Zip the course's hand-out files, flat, under their on-disk names.

    That is the layout already distributed to participants: no containing
    folder, original filenames.
    """
    handouts = sorted(
        p for p in course.files.iterdir()
        if p.is_file() and p.suffix.lower() in HANDOUT_SUFFIXES
        and not p.name.startswith("~$")  # Office lock files
    )
    if not handouts:
        fail(f"no files to zip in {course.name}/{course.files.name}/")

    # Write to a temporary name first so a failure can't leave a half-written
    # zip in deliverables/.
    staging = zip_path.with_suffix(".zip.tmp")
    try:
        with zipfile.ZipFile(staging, "w", zipfile.ZIP_DEFLATED) as zf:
            for handout in handouts:
                zf.write(handout, arcname=handout.name)
        staging.replace(zip_path)
    finally:
        staging.unlink(missing_ok=True)
    return [h.name for h in handouts]


def human(size: int) -> str:
    for unit in ("B", "KB", "MB"):
        if size < 1024 or unit == "MB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    raise AssertionError("unreachable")


def build_course(course: Course, args) -> list[tuple[str, int]]:
    """Everything for one course. Returns what it produced, for the summary."""
    wanted = [
        document for document in course.documents
        if args.only is None or document.name == args.only
    ]
    if args.only and not wanted:
        names = ", ".join(d.name for d in course.documents)
        fail(f"{course.name} has no document called {args.only!r} "
             f"(it has: {names})")

    if not args.skip_validate:
        validate(course)
        print()

    course.deliverables.mkdir(exist_ok=True)
    built: list[tuple[str, int]] = []

    if wanted:
        ensure_node_modules()
        chrome = find_chrome()
        print(f"  using {Path(chrome).name} to print")
        for document in wanted:
            md_path = course.folder / document.file
            pdf_path = course.deliverables / document.output
            print(f"  building {pdf_path.name} ...")
            render_pdf(course, md_path, pdf_path, document.subtitle, chrome)
            if course.footer_link_text and course.footer_link_url:
                pages = add_footer_links(pdf_path, course.footer_link_text,
                                         course.footer_link_url)
                if not pages:
                    print(f"      warning: could not find "
                          f"{course.footer_link_text!r} in the footer, so "
                          f"it is printed but not clickable")
            built.append((pdf_path.name, pdf_path.stat().st_size))

    if not args.no_zip and course.files:
        zip_path = course.deliverables / course.zip_name
        print(f"  building {course.zip_name} ...")
        names = build_zip(course, zip_path)
        built.append((zip_path.name, zip_path.stat().st_size))
        for n in names:
            print(f"      + {n}")

    return built


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a course's deliverables into its deliverables/ folder."
    )
    parser.add_argument(
        "--course",
        action="append",
        metavar="NAME",
        help="build this course (a folder name under courses/); repeat the "
             "flag for several. Without it you are asked which to build",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="build every course without asking",
    )
    parser.add_argument(
        "--only",
        help="build just one document of the course, by the name its "
             "settings give it (e.g. notes, trainer)",
    )
    parser.add_argument("--no-zip", action="store_true",
                        help="skip zipping the course's files")
    parser.add_argument("--skip-validate", action="store_true",
                        help="build even if the documents fail validation")
    args = parser.parse_args()

    courses = find_courses(args.course)
    if not args.course and not args.all:
        # Nothing on the command line: ask, unless there is nobody to ask.
        chosen = choose_courses(courses)
        if chosen is None:
            print("  cancelled.")
            return 0
        if not chosen:
            print("  no courses chosen, so nothing was built.")
            return 0
        courses = chosen

    for course in courses:
        if len(courses) > 1:
            print(f"\n=== {course.name} ===")
        built = build_course(course, args)
        where = course.deliverables.relative_to(HERE)
        print(f"\nDeliverables in {where.as_posix()}/:")
        for name, size in built:
            print(f"  {name:<52} {human(size):>9}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
