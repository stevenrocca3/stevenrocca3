"""Generates the Apple-style README tiles (light + dark) into profile/tiles/.

Run: python3 profile/build.py
"""
import math
from pathlib import Path

OUT = Path(__file__).parent / "tiles"
OUT.mkdir(exist_ok=True)

FONT = '-apple-system,BlinkMacSystemFont,"SF Pro Display","Helvetica Neue",Helvetica,Arial,sans-serif'

# Apple's palette. "alt" is the off-tone tile used to separate sections.
THEMES = {
    "light": dict(page="#ffffff", alt="#f5f5f7", ink="#1d1d1f", muted="#6e6e73",
                  blue="#0071e3", link="#0066cc", inverse="#000000", inv_ink="#f5f5f7", inv_muted="#a1a1a6"),
    "dark": dict(page="#000000", alt="#161617", ink="#f5f5f7", muted="#a1a1a6",
                 blue="#0071e3", link="#2997ff", inverse="#000000", inv_ink="#f5f5f7", inv_muted="#a1a1a6"),
}


def svg(w, h, label, body, bg, radius=22):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
<style>
  text{{font-family:{FONT};text-anchor:middle}}
  .h{{font-weight:600;letter-spacing:-0.022em}}
  .s{{font-weight:400;letter-spacing:-0.01em}}
  .e{{font-weight:600;letter-spacing:0.01em}}
  .b{{font-weight:400;letter-spacing:-0.016em}}
</style>
<rect width="{w}" height="{h}" rx="{radius}" fill="{bg}"/>
{body}
</svg>'''


def pills(cx, y, t, primary, secondary, ink):
    """Apple's paired CTAs: filled blue pill + outlined pill."""
    w1 = 22 + len(primary) * 9.6
    w2 = 22 + len(secondary) * 9.6
    gap = 14
    x1 = cx - (w1 + gap + w2) / 2
    x2 = x1 + w1 + gap
    return f'''<rect x="{x1:.1f}" y="{y}" width="{w1:.1f}" height="40" rx="20" fill="{t['blue']}"/>
<text x="{x1 + w1 / 2:.1f}" y="{y + 26}" class="b" font-size="17" fill="#ffffff">{primary}</text>
<rect x="{x2 + 0.5:.1f}" y="{y + 0.5}" width="{w2 - 1:.1f}" height="39" rx="19.5" fill="none" stroke="{t['link']}"/>
<text x="{x2 + w2 / 2:.1f}" y="{y + 26}" class="b" font-size="17" fill="{t['link']}">{secondary}</text>'''


def write(name, mode, content):
    (OUT / f"{name}-{mode}.svg").write_text(content)


for mode, t in THEMES.items():
    # ── Hero ───────────────────────────────────────────────────────────
    bg = t["page"] if mode == "dark" else t["alt"]
    body = f'''<defs><linearGradient id="g" x1="0" x2="1">
  <stop offset="0" stop-color="#2997ff"/><stop offset="0.5" stop-color="#a855f7"/><stop offset="1" stop-color="#ff6b6b"/>
</linearGradient></defs>
<text x="600" y="128" class="e" font-size="21" fill="{t['muted']}">Computer Science + Statistics · University of Pittsburgh</text>
<text x="600" y="232" class="h" font-size="96" fill="{t['ink']}">Steven Rocca.</text>
<text x="600" y="306" class="s" font-size="32" fill="url(#g)">Tools where the data has to be right.</text>'''
    write("hero", mode, svg(1200, 400, "Steven Rocca — Computer Science and Statistics, University of Pittsburgh", body, bg))

    # ── undercurrent (full-width, always dark — Apple's "Pro" tile) ───
    lines = []
    for i in range(9):
        amp = 18 + i * 5
        phase = i * 0.55
        y0 = 400 + i * 16
        pts = " ".join(
            f"{x},{y0 + amp * math.sin(x / 150 + phase) + 10 * math.sin(x / 47 + i):.1f}"
            for x in range(0, 1201, 20)
        )
        lines.append(f'<polyline points="{pts}" fill="none" stroke="url(#u)" stroke-width="{1.2 + i * 0.25:.2f}" opacity="{0.25 + i * 0.08:.2f}"/>')
    dots = "".join(
        f'<circle cx="{(i * 137) % 1180 + 10}" cy="{430 + (i * 53) % 140}" r="{1.5 + (i % 3)}" fill="#ffffff" opacity="{0.15 + (i % 5) * 0.1:.2f}"/>'
        for i in range(34)
    )
    body = f'''<defs>
  <linearGradient id="u" x1="0" x2="1"><stop offset="0" stop-color="#2997ff"/><stop offset="0.55" stop-color="#5e5ce6"/><stop offset="1" stop-color="#bf5af2"/></linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.9"/></linearGradient>
  <clipPath id="c"><rect width="1200" height="640" rx="22"/></clipPath>
</defs>
<g clip-path="url(#c)">{''.join(lines)}{dots}<rect y="520" width="1200" height="120" fill="url(#fade)"/></g>
<text x="600" y="112" class="h" font-size="64" fill="{t['inv_ink']}">undercurrent</text>
<text x="600" y="168" class="s" font-size="28" fill="{t['inv_ink']}">Every public GitHub event. Accounted for.</text>
<text x="600" y="210" class="s" font-size="19" fill="{t['inv_muted']}">A spec-driven pipeline over GH Archive, verified against fixtures.</text>
{pills(600, 244, dict(t, link="#2997ff"), "Learn more", "View code", t['inv_ink'])}'''
    write("undercurrent", mode, svg(1200, 640, "undercurrent — every public GitHub event, accounted for", body, t["inverse"]))

    # ── DexPresso (half tile) ──────────────────────────────────────────
    bars = ""
    for i, (stat, val) in enumerate([("Attack", 4), ("Defense", 15), ("Stamina", 14)]):
        y = 392 + i * 58
        bars += f'''<text x="118" y="{y + 14}" class="b" font-size="15" fill="{t['muted']}" style="text-anchor:end">{stat}</text>
<rect x="136" y="{y}" width="300" height="18" rx="9" fill="{t['ink']}" opacity="0.08"/>
<rect x="136" y="{y}" width="{300 * val / 15:.0f}" height="18" rx="9" fill="url(#d)"/>
<text x="466" y="{y + 14}" class="h" font-size="16" fill="{t['ink']}">{val}</text>'''
    body = f'''<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="#ff9f0a"/><stop offset="1" stop-color="#ff375f"/></linearGradient></defs>
<text x="295" y="96" class="h" font-size="48" fill="{t['ink']}">DexPresso</text>
<text x="295" y="140" class="s" font-size="22" fill="{t['ink']}">4,096 IV spreads.</text>
<text x="295" y="170" class="s" font-size="22" fill="{t['ink']}">One clear answer.</text>
<text x="295" y="206" class="s" font-size="16" fill="{t['muted']}">PvP IV ranking for Pokémon GO.</text>
{pills(295, 236, t, "Learn more", "View code", t['ink'])}
<text x="295" y="356" class="h" font-size="15" fill="{t['muted']}">RANK #1 OF 4,096 · GREAT LEAGUE</text>
{bars}'''
    write("dexpresso", mode, svg(590, 600, "DexPresso — 4,096 IV spreads, one clear answer", body, t["alt"]))

    # ── Compass (half tile) ────────────────────────────────────────────
    ticks = ""
    for a in range(0, 360, 6):
        r1 = 120 if a % 30 else 110
        rad = math.radians(a)
        ticks += f'<line x1="{295 + r1 * math.sin(rad):.1f}" y1="{445 - r1 * math.cos(rad):.1f}" x2="{295 + 128 * math.sin(rad):.1f}" y2="{445 - 128 * math.cos(rad):.1f}" stroke="{t['ink']}" stroke-width="{2 if a % 30 == 0 else 1}" opacity="{0.55 if a % 90 == 0 else 0.22}"/>'
    body = f'''<defs><linearGradient id="n" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#30d158"/><stop offset="1" stop-color="#0a84ff"/></linearGradient></defs>
<text x="295" y="96" class="h" font-size="48" fill="{t['ink']}">Compass</text>
<text x="295" y="140" class="s" font-size="22" fill="{t['ink']}">Know before</text>
<text x="295" y="170" class="s" font-size="22" fill="{t['ink']}">the market does.</text>
<text x="295" y="206" class="s" font-size="16" fill="{t['muted']}">AI due diligence. Built at SteelHacks XII.</text>
{pills(295, 236, t, "Learn more", "View code", t['ink'])}
<circle cx="295" cy="445" r="128" fill="none" stroke="{t['ink']}" opacity="0.1"/>
{ticks}
<polygon points="295,340 309,445 295,460 281,445" fill="url(#n)" transform="rotate(38 295 445)"/>
<polygon points="295,550 309,445 295,430 281,445" fill="{t['ink']}" opacity="0.18" transform="rotate(38 295 445)"/>
<circle cx="295" cy="445" r="7" fill="{t['alt']}" stroke="{t['ink']}" stroke-width="2"/>'''
    write("compass", mode, svg(590, 600, "Compass — know before the market does", body, t["alt"]))

    # ── Toolkit ────────────────────────────────────────────────────────
    row1 = "Python. Java. TypeScript. React. Vue."
    row2 = "Tailwind. Vite. Postgres. Supabase. Rust. R."
    body = f'''<defs><linearGradient id="k" x1="0" x2="1">
  <stop offset="0" stop-color="#0a84ff"/><stop offset="0.35" stop-color="#5e5ce6"/><stop offset="0.7" stop-color="#bf5af2"/><stop offset="1" stop-color="#ff375f"/>
</linearGradient></defs>
<text x="600" y="96" class="e" font-size="21" fill="{t['muted']}">Toolkit</text>
<text x="600" y="176" class="h" font-size="54" fill="url(#k)">{row1}</text>
<text x="600" y="244" class="h" font-size="54" fill="url(#k)">{row2}</text>
<text x="600" y="306" class="s" font-size="21" fill="{t['muted']}">From Postgres schema to pixel. Statistics all the way down.</text>'''
    bg = t["alt"] if mode == "light" else t["alt"]
    write("toolkit", mode, svg(1200, 380, "Toolkit: Python, Java, TypeScript, React, Vue, Tailwind, Vite, Postgres, Supabase, Rust, R", body, bg))

    # ── Contact pills (separate images so each is clickable) ───────────
    for name, label, filled in [("linkedin", "LinkedIn", True), ("email", "Email me", False)]:
        w = int(36 + len(label) * 10.5)
        if filled:
            shape = f'<rect width="{w}" height="44" rx="22" fill="{t["blue"]}"/>'
            ink = "#ffffff"
        else:
            shape = f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="42.5" rx="21.25" fill="none" stroke="{t["link"]}" stroke-width="1.5"/>'
            ink = t["link"]
        write(f"pill-{name}", mode, f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="44" viewBox="0 0 {w} 44" role="img" aria-label="{label}">
{shape}<text x="{w / 2}" y="28.5" font-family='{FONT}' font-size="17" letter-spacing="-0.016em" text-anchor="middle" fill="{ink}">{label}</text>
</svg>''')

print("wrote", len(list(OUT.glob("*.svg"))), "tiles to", OUT)
