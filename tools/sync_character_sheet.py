#!/usr/bin/env python3
"""Erzeugt das Character-Sheet-Artefakt (HTML) aus dem kanonischen Markdown-Bogen.

Quelle : player/nathan_character_sheet.md   (bleibt der Haupt-Bogen)
Ziel   : player/nathan_character_sheet.html (wird zum Artefakt deployt)

Aufruf:
  python3 tools/sync_character_sheet.py          -> baut das HTML neu
  python3 tools/sync_character_sheet.py --hook    -> Hook-Modus: liest die
      PostToolUse-Payload von stdin und baut nur neu, wenn der Markdown-Bogen
      bearbeitet wurde; gibt dann eine Redeploy-Erinnerung aus.

Die Ausgabe ist ein Artifact-kompatibles Fragment (nur <style> + Inhalt, kein
<html>/<head>/<body>). Es enthaelt keinen Zeitstempel, damit die Regenerierung
deterministisch ist und Git-Diffs nur bei echten Aenderungen entstehen.
"""

import sys
import os
import re
import json
import html

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "player", "nathan_character_sheet.md")
OUT = os.path.join(REPO, "player", "nathan_character_sheet.html")
EQUIP_SRC = os.path.join(REPO, "player", "nathan_equipment.md")
SOURCE_REL = "player/nathan_character_sheet.md"
EQUIP_REL = "player/nathan_equipment.md"

# --------------------------------------------------------------------------
# Theme-Tokens (ein Satz Werte, in alle vier Theme-Kontexte injiziert)
# --------------------------------------------------------------------------
LIGHT_TOKENS = """
  --bg:#efe8db; --surface:#faf6ee; --surface-2:#f2ebdd; --ink:#221d17;
  --muted:#6d6454; --line:#e3d9c7; --brass:#8a5a1e; --brass-bright:#a8722a;
  --indigo:#2f3a63; --num:#8a5a1e; --exp:#8a5a1e; --prof:#2f3a63;
  --jack:#a99b81; --shadow:rgba(60,45,20,.10);
"""

DARK_TOKENS = """
  --bg:#13151d; --surface:#1b1e29; --surface-2:#20242f; --ink:#ece4d5;
  --muted:#9a9fb0; --line:#2b2f3d; --brass:#d9a24c; --brass-bright:#e7b566;
  --indigo:#9db0dd; --num:#e2b463; --exp:#d9a24c; --prof:#9db0dd;
  --jack:#8b8fa0; --shadow:rgba(0,0,0,.42);
"""

COMPONENT_CSS = """
*{box-sizing:border-box}
.sheet{max-width:1000px;margin:0 auto;padding:clamp(1rem,3vw,2.25rem);
  color:var(--ink);background:var(--bg);
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  line-height:1.55;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
.sheet a{color:var(--brass);text-underline-offset:2px}
.sheet :focus-visible{outline:2px solid var(--brass);outline-offset:2px;border-radius:4px}
.serif{font-family:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif}

.banner{margin-bottom:1.4rem}
.kicker{font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;
  color:var(--brass-bright);font-weight:600}
.name{font-family:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  font-weight:600;font-size:clamp(2rem,5vw,3rem);line-height:1.04;margin:.14em 0 .12em;
  text-wrap:balance;letter-spacing:.005em}
.subtitle{color:var(--muted);font-size:1rem;margin:0}
.rule{height:2px;background:linear-gradient(90deg,var(--brass),transparent);
  margin:1rem 0 1.2rem;border-radius:2px}

.quickstats{display:grid;grid-template-columns:repeat(auto-fit,minmax(82px,1fr));gap:.55rem}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:.5rem .7rem;box-shadow:0 1px 2px var(--shadow)}
.stat .lbl{font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);font-weight:700}
.stat .val{font-family:"Iowan Old Style",Palatino,Georgia,serif;font-size:1.5rem;
  font-weight:600;font-variant-numeric:tabular-nums;color:var(--num);line-height:1.15}

.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;
  align-items:start;margin-top:1.2rem}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;
  padding:1.05rem 1.15rem 1.2rem;box-shadow:0 1px 3px var(--shadow)}
.card.span-all{grid-column:1/-1}
.card h2{font-family:"Iowan Old Style",Palatino,Georgia,serif;font-size:1.16rem;
  font-weight:600;margin:0 0 .8rem;padding-bottom:.45rem;border-bottom:1px solid var(--line);
  position:relative;text-wrap:balance}
.card h2::after{content:"";position:absolute;left:0;bottom:-1px;width:2.2rem;height:2px;
  background:var(--brass)}
.card--spellcasting h2::after{background:var(--indigo)}
.card h3{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
  margin:1rem 0 .35rem;font-weight:700}
.card p{margin:.5rem 0}
.card ul{margin:.4rem 0;padding-left:1.1rem}
.card li{margin:.26rem 0}
.term{font-family:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;
  font-size:.84em;background:var(--surface-2);border:1px solid var(--line);border-radius:5px;
  padding:.05em .38em;color:var(--ink);white-space:nowrap}

.ability-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(116px,1fr));gap:.7rem}
.ability{background:var(--surface-2);border:1px solid var(--line);border-radius:12px;
  padding:.7rem .5rem;text-align:center}
.ability .an{font-size:.64rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);
  font-weight:700}
.ability .asc{font-family:"Iowan Old Style",Palatino,Georgia,serif;font-size:2rem;font-weight:600;
  color:var(--num);font-variant-numeric:tabular-nums;line-height:1.1;margin:.08rem 0}
.ability .asub{display:flex;justify-content:center;gap:.7rem;font-size:.72rem;color:var(--muted);
  font-variant-numeric:tabular-nums}
.ability .asub b{color:var(--ink);font-weight:600}

.skill-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:.4rem .8rem}
.skill{display:flex;align-items:center;gap:.55rem;padding:.34rem .55rem;border-radius:8px;
  border-left:3px solid var(--jack);background:var(--surface-2)}
.skill.exp{border-left-color:var(--exp)}
.skill.prof{border-left-color:var(--prof)}
.skill .sn{flex:1;font-size:.9rem}
.skill .sm{font-variant-numeric:tabular-nums;font-weight:600;color:var(--num);min-width:2.1em;
  text-align:right}
.skill .sb{font-size:.58rem;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);
  font-weight:700;min-width:4.4em;text-align:right}

.table-wrap{overflow-x:auto;margin:.5rem 0}
.table-wrap table{border-collapse:collapse;width:100%;font-size:.9rem}
.table-wrap th{text-align:left;font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);border-bottom:1px solid var(--line);padding:.4rem .5rem;font-weight:700}
.table-wrap td{padding:.4rem .5rem;border-bottom:1px solid var(--line);
  font-variant-numeric:tabular-nums}

.equip-cols{columns:240px auto;column-gap:1.6rem}
.equip-block{break-inside:avoid;margin-bottom:.8rem}
.equip-block h3{margin-top:.1rem}

.foot{margin-top:1.5rem;color:var(--muted);font-size:.74rem;text-align:center}
.foot .term{font-size:.9em}
@media (max-width:640px){.grid{grid-template-columns:1fr}}
"""


def build_css():
    return (
        ":root{" + LIGHT_TOKENS + "}\n"
        "@media (prefers-color-scheme: dark){:root{" + DARK_TOKENS + "}}\n"
        ':root[data-theme="light"]{' + LIGHT_TOKENS + "}\n"
        ':root[data-theme="dark"]{' + DARK_TOKENS + "}\n"
        + COMPONENT_CSS
    )


# --------------------------------------------------------------------------
# Inline-Markdown
# --------------------------------------------------------------------------
def esc(s):
    return html.escape(s, quote=True)


def inline(s):
    s = esc(s)
    stash = []

    def keep(m):
        stash.append('<code class="term">' + m.group(1) + "</code>")
        return "\x00%d\x00" % (len(stash) - 1)

    s = re.sub(r"`([^`]+)`", keep, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], s)
    return s


# --------------------------------------------------------------------------
# Block-Parser
# --------------------------------------------------------------------------
def _cells(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [c.strip() for c in row.split("|")]


def _col(header, *names):
    low = [h.lower() for h in header]
    for nm in names:
        if nm in low:
            return low.index(nm)
    return None


def render_ability(header, rows):
    ai = _col(header, "ability")
    si = _col(header, "score")
    mi = _col(header, "modifier")
    vi = _col(header, "saving throw", "save")
    cards = []
    for r in rows:
        if not r or ai is None or ai >= len(r):
            continue
        name = r[ai]
        score = r[si] if si is not None and si < len(r) else ""
        mod = r[mi] if mi is not None and mi < len(r) else ""
        sav = r[vi] if vi is not None and vi < len(r) else ""
        cards.append(
            '<div class="ability"><div class="an">%s</div>'
            '<div class="asc">%s</div>'
            '<div class="asub"><span>mod&nbsp;<b>%s</b></span>'
            "<span>save&nbsp;<b>%s</b></span></div></div>"
            % (esc(name), esc(score), esc(mod), esc(sav))
        )
    return '<div class="ability-grid">' + "".join(cards) + "</div>"


def render_skills(header, rows):
    si = _col(header, "skill")
    mi = _col(header, "modifier")
    ni = _col(header, "note")
    out = []
    for r in rows:
        if not r or si is None or si >= len(r):
            continue
        name = r[si]
        mod = r[mi] if mi is not None and mi < len(r) else ""
        note = r[ni] if ni is not None and ni < len(r) else ""
        nl = note.lower()
        if "expertise" in nl:
            tier, label = "exp", "Expertise"
        elif "jack" in nl:
            tier, label = "jack", "Jack"
        elif "proficient" in nl:
            tier, label = "prof", "Proficient"
        else:
            tier, label = "", note
        out.append(
            '<div class="skill %s"><span class="sn">%s</span>'
            '<span class="sm">%s</span>'
            '<span class="sb" title="%s">%s</span></div>'
            % (tier, esc(name), esc(mod), esc(note), esc(label))
        )
    return '<div class="skill-grid">' + "".join(out) + "</div>"


def render_table(header, rows):
    th = "".join("<th>%s</th>" % inline(h) for h in header)
    body = []
    for r in rows:
        tds = "".join("<td>%s</td>" % inline(c) for c in r)
        body.append("<tr>%s</tr>" % tds)
    return (
        '<div class="table-wrap"><table><thead><tr>%s</tr></thead>'
        "<tbody>%s</tbody></table></div>" % (th, "".join(body))
    )


def _collect_table(lines, i):
    rows = []
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        rows.append(lines[i])
        i += 1
    header = _cells(rows[0])
    data = [_cells(r) for r in rows[2:]] if len(rows) > 2 else []
    low = [h.lower() for h in header]
    if "ability" in low and "score" in low:
        return render_ability(header, data), i
    if "skill" in low and "modifier" in low:
        return render_skills(header, data), i
    return render_table(header, data), i


def _collect_list(lines, i):
    items = []
    while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
        items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]).rstrip())
        i += 1
    return "<ul>" + "".join("<li>%s</li>" % inline(x) for x in items) + "</ul>", i


def _collect_para(lines, i):
    buf = []
    while i < len(lines):
        ln = lines[i]
        if (not ln.strip() or ln.lstrip().startswith("|")
                or re.match(r"^\s*[-*]\s+", ln) or ln.startswith("#")):
            break
        buf.append(ln.strip())
        i += 1
    return " ".join(buf), i


def parse_blocks(lines):
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("### "):
            out.append("<h3>%s</h3>" % inline(ln[4:].strip()))
            i += 1
        elif ln.lstrip().startswith("|"):
            frag, i = _collect_table(lines, i)
            out.append(frag)
        elif re.match(r"^\s*[-*]\s+", ln):
            frag, i = _collect_list(lines, i)
            out.append(frag)
        else:
            para, i = _collect_para(lines, i)
            if para:
                out.append("<p>%s</p>" % inline(para))
    return "\n".join(out)


# --------------------------------------------------------------------------
# Dokument-Struktur
# --------------------------------------------------------------------------
def split_sections(md):
    lines = md.splitlines()
    title = "Character Sheet"
    sections = []
    cur_title = None
    cur_body = []
    started = False
    for ln in lines:
        if ln.startswith("# ") and not ln.startswith("## "):
            title = ln[2:].strip()
            continue
        if ln.startswith("## "):
            if cur_title is not None:
                sections.append((cur_title, cur_body))
            cur_title = ln[3:].strip()
            cur_body = []
            started = True
            continue
        if started:
            cur_body.append(ln)
    if cur_title is not None:
        sections.append((cur_title, cur_body))
    return title, sections


def first_bullet(body):
    for ln in body:
        m = re.match(r"^\s*[-*]\s+(.*)$", ln)
        if m:
            return m.group(1).strip()
    return ""


def load_equipment_sections():
    """Sections aus player/nathan_equipment.md, um Equipment ins Sheet zu ziehen."""
    try:
        with open(EQUIP_SRC, "r", encoding="utf-8") as fh:
            md = fh.read()
    except OSError:
        return []
    _t, secs = split_sections(md)
    return secs


def quick_stats(md):
    def find(pat):
        m = re.search(pat, md)
        return m.group(1) if m else None

    tiles = []

    def add(label, val):
        if val:
            tiles.append((label, val))

    add("AC", find(r"Armor Class:\s*([0-9]+)"))
    add("HP", find(r"Hit Points:\s*([0-9]+)"))
    add("Hit Dice", find(r"Hit Dice:\s*([0-9]+d[0-9]+)"))
    add("Init", find(r"Initiative:\s*([+\-]?[0-9]+)"))
    sp = find(r"Speed:\s*([0-9]+)\s*feet")
    add("Speed", (sp + " ft") if sp else None)
    add("Prof", find(r"Proficiency Bonus:\s*([+\-]?[0-9]+)"))
    add("Spell DC", find(r"Spell Save DC:\s*([0-9]+)"))
    return tiles


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def render_html(md):
    title, sections = split_sections(md)

    # Kopf: Name + Kicker aus H1 (an Gedankenstrich getrennt)
    if "—" in title:
        name, kicker = [p.strip() for p in title.split("—", 1)]
    elif " - " in title:
        name, kicker = [p.strip() for p in title.split(" - ", 1)]
    else:
        name, kicker = title, "Character Sheet"

    subtitle = ""
    for st, body in sections:
        if st.lower().startswith("identity"):
            subtitle = first_bullet(body)
            break

    tiles = quick_stats(md)
    tiles_html = "".join(
        '<div class="stat"><div class="lbl">%s</div><div class="val">%s</div></div>'
        % (esc(l), esc(v))
        for l, v in tiles
    )

    equip_sections = load_equipment_sections()
    cards = []
    for st, body in sections:
        sg = slug(st)
        if sg == "equipment-and-appearance" and equip_sections:
            blocks = "".join(
                '<div class="equip-block"><h3>%s</h3>%s</div>'
                % (inline(est), parse_blocks(ebody))
                for est, ebody in equip_sections
            )
            cards.append(
                '<section class="card card--equipment span-all"><h2>Equipment</h2>'
                '<div class="equip-cols">%s</div></section>' % blocks
            )
            continue
        cls = "card card--%s" % sg
        if sg in ("ability-scores", "skills"):
            cls += " span-all"
        cards.append(
            '<section class="%s"><h2>%s</h2>%s</section>'
            % (cls, inline(st), parse_blocks(body))
        )

    parts = ['<style>%s</style>' % build_css()]
    parts.append('<main class="sheet">')
    parts.append('<header class="banner">')
    parts.append('<div class="kicker">%s</div>' % esc(kicker))
    parts.append('<h1 class="name">%s</h1>' % esc(name))
    if subtitle:
        parts.append('<p class="subtitle">%s</p>' % inline(subtitle))
    parts.append('<div class="rule"></div>')
    if tiles_html:
        parts.append('<div class="quickstats">%s</div>' % tiles_html)
    parts.append("</header>")
    parts.append('<div class="grid">%s</div>' % "".join(cards))
    parts.append(
        '<footer class="foot">Generiert aus <code class="term">%s</code> — '
        "der Markdown-Bogen bleibt der kanonische Haupt-Bogen.</footer>" % SOURCE_REL
    )
    parts.append("</main>")
    return "\n".join(parts)


def build():
    with open(SRC, "r", encoding="utf-8") as fh:
        md = fh.read()
    out = render_html(md)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(out)
    return out


# --------------------------------------------------------------------------
# Einstieg / Hook-Modus
# --------------------------------------------------------------------------
def main():
    hook = "--hook" in sys.argv
    if hook:
        raw = sys.stdin.read()
        edited = None
        try:
            payload = json.loads(raw) if raw.strip() else {}
            ti = payload.get("tool_input") or {}
            edited = ti.get("file_path") or payload.get("file_path")
        except Exception:
            edited = None
        if edited is not None:
            norm = str(edited).replace("\\", "/")
            triggers = (SOURCE_REL, EQUIP_REL)
            hit = any(norm.endswith(t) for t in triggers) or \
                os.path.abspath(edited) in (SRC, EQUIP_SRC)
            if not hit:
                return 0  # weder Bogen noch Equipment -> still beenden
        build()
        print(
            "🎼 Character-Sheet-Artefakt neu generiert (%s). "
            "Bitte im Chat mit dem Artifact-Tool (gleicher file_path) neu deployen, "
            "damit die gehostete Version aktualisiert wird."
            % os.path.relpath(OUT, REPO)
        )
        return 0
    build()
    print("Geschrieben: %s" % os.path.relpath(OUT, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
