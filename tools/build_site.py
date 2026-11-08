"""Build the session pages and PDFs of the course website.

Usage: python tools/build_site.py <site_dir>

<site_dir> is the Jekyll output (_site). The script expects <site_dir>/Notebooks/*.ipynb
(Jekyll copies them there) and writes:
  <site_dir>/Notebooks/SNN_Name.html   one web page per session, with download buttons
  <site_dir>/pdf/SNN_Name.pdf          one PDF per finished session
  <site_dir>/pdf/Python-Course-All.pdf all finished sessions in one PDF (cover + bookmarks)

A session counts as "finished" unless it is still the generated skeleton
(its markdown contains the placeholder line "- ...").
"""
import glob
import html
import json
import os
import re
import sys
from datetime import date

import nbformat
from nbconvert import HTMLExporter
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

SITE = sys.argv[1]
NB_DIR = os.path.join(SITE, "Notebooks")
PDF_DIR = os.path.join(SITE, "pdf")
ALL_PDF = "Python-Course-All.pdf"
COURSE_FA = "پایتون برای علوم داده"
COURSE_EN = "Python for Data Science"
INSTRUCTOR = "دکتر حسین حق‌بین"
os.makedirs(PDF_DIR, exist_ok=True)

STYLE = """
<style>
@font-face { font-family: 'Vazirmatn'; font-weight: 400; src: url('../assets/fonts/Vazirmatn-Regular.woff2') format('woff2'); }
@font-face { font-family: 'Vazirmatn'; font-weight: 700; src: url('../assets/fonts/Vazirmatn-Bold.woff2') format('woff2'); }
body { max-width: 1000px; margin: 0 auto !important; }
.jp-RenderedHTMLCommon, .jp-RenderedHTMLCommon * { font-family: 'Vazirmatn', Tahoma, sans-serif; line-height: 1.9; }
.jp-RenderedHTMLCommon code, .jp-RenderedHTMLCommon pre, .jp-RenderedHTMLCommon pre * , .jp-InputArea, .jp-OutputArea {
  font-family: 'DejaVu Sans Mono', Consolas, monospace !important; line-height: 1.5; direction: ltr; }
.jp-RenderedHTMLCommon table { margin-left: auto; margin-right: auto; }
.pc-bar { direction: rtl; font-family: 'Vazirmatn', Tahoma, sans-serif; position: sticky; top: 0; z-index: 10;
  display: flex; flex-wrap: wrap; align-items: center; gap: 8px; padding: 10px 14px; margin: 0 0 12px 0;
  background: #1f2a36; color: #fff; border-radius: 0 0 10px 10px; }
.pc-bar .pc-title { flex: 1 1 auto; font-weight: 700; }
.pc-bar a { color: #fff; text-decoration: none; font-size: 14px; padding: 5px 12px; border-radius: 6px;
  background: rgba(255,255,255,.12); white-space: nowrap; }
.pc-bar a:hover { background: rgba(255,255,255,.25); }
.pc-bar a.pc-main { background: #2f80ed; }
.pc-note { direction: rtl; font-family: 'Vazirmatn', Tahoma, sans-serif; background: #fff4dc; border: 1px solid #d79a2b;
  border-radius: 8px; padding: 10px 14px; margin: 8px 0 16px; }
@media print {
  .pc-bar, .pc-note { display: none !important; }
  body { max-width: none; }
  pre { white-space: pre-wrap !important; word-break: break-word; }
  .jp-CodeCell { break-inside: avoid; }
  h1, h2, h3 { break-after: avoid; }
  img { max-width: 100% !important; break-inside: avoid; }
}
</style>
"""


def is_finished(nb):
    for c in nb.cells:
        if c.cell_type == "markdown" and re.search(r"^- \.\.\.\s*$", c.source, re.M):
            return False
    return True


def session_title(nb, fallback):
    for c in nb.cells:
        if c.cell_type == "markdown":
            m = re.search(r"^# (.+)$", c.source, re.M)
            if m:
                return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return fallback


def bar(name, title, finished):
    links = ['<a href="../">صفحه‌ی اصلی درس</a>']
    if finished:
        links.append(f'<a class="pc-main" href="../pdf/{name}.pdf" download>دانلود PDF این جلسه</a>')
    links.append(f'<a href="../pdf/{ALL_PDF}" download>دانلود PDF همه‌ی جلسات</a>')
    links.append(f'<a href="{name}.ipynb" download>دانلود نوت‌بوک</a>')
    out = f'<nav class="pc-bar"><span class="pc-title">{html.escape(title)}</span>{"".join(links)}</nav>'
    if not finished:
        out += '<div class="pc-note">این جلسه هنوز در دست تهیه است.</div>'
    return out


def build_pages():
    exporter = HTMLExporter(template_name="lab")
    exporter.exclude_input_prompt = True
    exporter.exclude_output_prompt = True
    sessions = []
    for path in sorted(glob.glob(os.path.join(NB_DIR, "S[0-9][0-9]_*.ipynb"))):
        name = os.path.splitext(os.path.basename(path))[0]
        nb = nbformat.read(path, as_version=4)
        finished = is_finished(nb)
        title = session_title(nb, name)
        body, _ = exporter.from_notebook_node(nb)
        body = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} | {COURSE_FA}</title>", body, count=1, flags=re.S)
        body = body.replace("</head>", STYLE + "</head>", 1)
        body = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + bar(name, title, finished), body, count=1)
        out = os.path.join(NB_DIR, name + ".html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(body)
        sessions.append((name, title, finished, out))
        print("page:", name, "(finished)" if finished else "(skeleton)")
    return sessions


FOOTER = ('<div style="width:100%;font-size:8px;color:#888;text-align:center;font-family:DejaVu Sans,sans-serif;">'
          '{label} &middot; <span class="pageNumber"></span> / <span class="totalPages"></span></div>')


def to_pdf(page, html_path, pdf_path, label):
    page.goto("file://" + os.path.abspath(html_path), wait_until="networkidle")
    page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
    page.evaluate("document.fonts.ready")
    page.pdf(path=pdf_path, format="A4", print_background=True,
             margin={"top": "15mm", "bottom": "15mm", "left": "12mm", "right": "12mm"},
             display_header_footer=True, header_template="<div></div>",
             footer_template=FOOTER.format(label=label))


def cover_html(done):
    rows = "".join(f"<li>{html.escape(t)}</li>" for _, t, _, _ in done)
    return f"""<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">{STYLE}
<style>body{{font-family:'Vazirmatn',Tahoma,sans-serif;text-align:center;padding-top:30mm}}
h1{{font-size:34px;margin:0}} h2{{font-size:22px;color:#555;font-weight:400}}
ol{{text-align:right;display:inline-block;font-size:15px;line-height:2;margin-top:12mm}}</style></head>
<body><h1>{COURSE_FA}</h1><h2 dir="ltr">{COURSE_EN}</h2><p style="font-size:18px">{INSTRUCTOR}</p>
<p style="color:#777">دانشگاه خلیج فارس</p><ol>{rows}</ol>
<p style="color:#999;font-size:12px;margin-top:10mm" dir="ltr">{date.today().isoformat()}</p></body></html>"""


def build_pdfs(sessions):
    done = [s for s in sessions if s[2]]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for name, title, _, out in done:
            to_pdf(page, out, os.path.join(PDF_DIR, name + ".pdf"), f"{COURSE_EN} - {name[:3]}")
            print("pdf:", name)
        cover = os.path.join(NB_DIR, "_cover.html")
        with open(cover, "w", encoding="utf-8") as f:
            f.write(cover_html(done))
        page.goto("file://" + os.path.abspath(cover), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.pdf(path=os.path.join(PDF_DIR, "_cover.pdf"), format="A4", print_background=True)
        browser.close()
    os.remove(cover)

    writer = PdfWriter()
    writer.append(os.path.join(PDF_DIR, "_cover.pdf"))
    for name, title, _, _ in done:
        start = len(writer.pages)
        writer.append(os.path.join(PDF_DIR, name + ".pdf"))
        writer.add_outline_item(title, start)
    writer.add_metadata({"/Title": f"{COURSE_EN} - {INSTRUCTOR}"})
    with open(os.path.join(PDF_DIR, ALL_PDF), "wb") as f:
        writer.write(f)
    os.remove(os.path.join(PDF_DIR, "_cover.pdf"))
    print("pdf:", ALL_PDF, len(done), "sessions")


if __name__ == "__main__":
    build_pdfs(build_pages())
