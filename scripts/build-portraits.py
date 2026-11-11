"""Builds the three animated, self-contained SVG portraits from an avatar image.

Usage: python3 scripts/build-portraits.py <avatar image> assets/portraits   (needs Pillow)
"""
import base64, io, random, sys
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
random.seed(1337)
BG, RED, TEXT, DIM = "#0a0a0b", "#e60000", "#c9c9ce", "#6b6b74"
MONO = "ui-monospace, 'JetBrains Mono', 'Fira Code', Menlo, Consolas, monospace"

img = Image.open(src).convert("RGB")
small = img.resize((240, 240), Image.LANCZOS)
buf = io.BytesIO(); small.save(buf, "JPEG", quality=82)
DATA = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------------------------------------------------------------- 1. glitch
def glitch():
    X, Y, S = 36, 30, 180
    slices = "".join(
        f'<g class="tear t{i}" clip-path="url(#s{i})"><image href="{DATA}" x="{X}" y="{Y}" width="{S}" height="{S}"/></g>'
        for i in range(3))
    clips = "".join(
        f'<clipPath id="s{i}"><rect x="{X}" y="{Y + y}" width="{S}" height="{h}"/></clipPath>'
        for i, (y, h) in enumerate([(34, 16), (88, 10), (132, 22)]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 240" width="720" height="240" role="img" aria-label="RuM, glitching portrait">
<defs>
  <filter id="red"><feColorMatrix type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0"/></filter>
  <filter id="cyan"><feColorMatrix type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1 0"/></filter>
  <clipPath id="frame"><rect x="{X}" y="{Y}" width="{S}" height="{S}" rx="10"/></clipPath>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".35"/></pattern>
  {clips}
</defs>
<style>
  .r {{ animation: r 5s steps(1) infinite; mix-blend-mode: screen; }}
  .c {{ animation: c 5s steps(1) infinite; mix-blend-mode: screen; }}
  .tear {{ opacity: 0; }}
  .t0 {{ animation: tear 5s steps(1) infinite; }}
  .t1 {{ animation: tear 5s steps(1) -0.12s infinite; }}
  .t2 {{ animation: tear 5s steps(1) -0.05s infinite; }}
  .scan {{ animation: scan 3.2s linear infinite; }}
  .name {{ font: 700 64px {MONO}; letter-spacing: -2px; }}
  .n-r {{ fill: {RED}; animation: r 5s steps(1) infinite; }}
  .n-c {{ fill: #00e5ff; opacity: .55; animation: c 5s steps(1) infinite; }}
  .n-w {{ fill: #fff; animation: flick 5s steps(1) infinite; }}
  .sub {{ font: 15px {MONO}; fill: {TEXT}; }}
  .dim {{ font: 12px {MONO}; fill: {DIM}; }}
  .cur {{ animation: blink 1.1s steps(1) infinite; fill: {RED}; }}
  @keyframes r {{ 0%, 100% {{ transform: translate(0, 0); }} 62% {{ transform: translate(-7px, 1px); }} 64% {{ transform: translate(5px, -1px); }} 66% {{ transform: translate(-2px, 0); }} 68% {{ transform: translate(0, 0); }} 90% {{ transform: translate(4px, 0); }} 92% {{ transform: translate(0, 0); }} }}
  @keyframes c {{ 0%, 100% {{ transform: translate(0, 0); }} 62% {{ transform: translate(7px, -1px); }} 64% {{ transform: translate(-5px, 1px); }} 66% {{ transform: translate(2px, 0); }} 68% {{ transform: translate(0, 0); }} 90% {{ transform: translate(-4px, 0); }} 92% {{ transform: translate(0, 0); }} }}
  @keyframes tear {{ 0%, 100% {{ opacity: 0; transform: translateX(0); }} 62% {{ opacity: 1; transform: translateX(18px); }} 64% {{ opacity: 1; transform: translateX(-14px); }} 66% {{ opacity: 0; }} 90% {{ opacity: 1; transform: translateX(9px); }} 92% {{ opacity: 0; }} }}
  @keyframes scan {{ from {{ transform: translateY(-70px); }} to {{ transform: translateY(190px); }} }}
  @keyframes flick {{ 0%, 100% {{ opacity: 1; }} 62% {{ opacity: .4; }} 64% {{ opacity: 1; }} 65% {{ opacity: .2; }} 67% {{ opacity: 1; }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<rect width="720" height="240" rx="14" fill="{BG}"/>
<rect x=".5" y=".5" width="719" height="239" rx="14" fill="none" stroke="#26262b"/>
<g clip-path="url(#frame)">
  <rect x="{X}" y="{Y}" width="{S}" height="{S}" fill="#000"/>
  <image class="r" filter="url(#red)" href="{DATA}" x="{X}" y="{Y}" width="{S}" height="{S}"/>
  <image class="c" filter="url(#cyan)" href="{DATA}" x="{X}" y="{Y}" width="{S}" height="{S}"/>
  {slices}
  <rect x="{X}" y="{Y}" width="{S}" height="{S}" fill="url(#lines)"/>
  <rect class="scan" x="{X}" y="{Y}" width="{S}" height="70" fill="url(#scan)"/>
</g>
<rect x="{X}" y="{Y}" width="{S}" height="{S}" rx="10" fill="none" stroke="{RED}" stroke-width="1.5"/>
<text class="name n-c" x="262" y="112">RuM</text>
<text class="name n-r" x="262" y="112">RuM</text>
<text class="name n-w" x="262" y="112">RuM</text>
<text class="sub" x="264" y="150"><tspan fill="{RED}">ru44@github</tspan>:~$ whoami <tspan class="cur">&#9608;</tspan></text>
<text class="sub" x="264" y="176">push stealer // zone-&#1071;</text>
<text class="dim" x="264" y="206">[ signal locked :: port 1337 ]</text>
</svg>'''

# -------------------------------------------------------------- 2. terminal
def terminal():
    cols, rows = 58, 30
    ramp = " .,:;i1tfLCG08@"
    g = img.convert("L").resize((cols, rows), Image.LANCZOS)
    px = g.load()
    lines = ["".join(ramp[px[x, y] * (len(ramp) - 1) // 255] for x in range(cols)) for y in range(rows)]
    X, Y, W, LH = 34, 44, 232, 7.4
    text = "".join(
        f'<text class="a" style="animation-delay:{i * 0.07:.2f}s" x="{X}" y="{Y + i * LH:.1f}" textLength="{W}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{esc(l)}</text>'
        for i, l in enumerate(lines))
    log = [("$ ./render --input avatar.png", TEXT), ("[*] sampling 58x30 cells", DIM), ("[*] mapping luminance to glyphs", DIM),
           ("[*] writing to /dev/tty1", DIM), ("[+] done. resolving image...", RED), ("", TEXT), ("ru44@github:~$ whoami", TEXT), ("RuM // push stealer", RED)]
    side = "".join(
        f'<text class="l" style="animation-delay:{0.3 + i * 0.45:.2f}s" x="300" y="{70 + i * 22}" fill="{c}">{esc(t)}</text>'
        for i, (t, c) in enumerate(log))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 290" width="720" height="290" role="img" aria-label="RuM, portrait rendered by a terminal">
<defs><clipPath id="f"><rect x="{X}" y="{Y - 8}" width="{W}" height="{rows * LH + 6:.0f}" rx="6"/></clipPath></defs>
<style>
  .a {{ font: 7.2px {MONO}; fill: {RED}; opacity: 0; animation: row 10s linear infinite; }}
  .pic {{ opacity: 0; animation: pic 10s ease infinite; }}
  .l {{ font: 14px {MONO}; opacity: 0; animation: line 10s linear infinite; }}
  .bar {{ font: 12px {MONO}; fill: {DIM}; }}
  @keyframes row {{ 0% {{ opacity: 0; }} 1% {{ opacity: 1; }} 46% {{ opacity: 1; }} 54% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
  @keyframes pic {{ 0%, 44% {{ opacity: 0; }} 56%, 90% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
  @keyframes line {{ 0% {{ opacity: 0; }} 1% {{ opacity: 1; }} 61% {{ opacity: 1; }} 64%, 100% {{ opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .a, .l {{ animation: none; opacity: 0; }} .pic {{ animation: none; opacity: 1; }} .l {{ opacity: 1; }} }}
</style>
<rect width="720" height="290" rx="14" fill="{BG}"/>
<rect x=".5" y=".5" width="719" height="289" rx="14" fill="none" stroke="#26262b"/>
<circle cx="24" cy="18" r="5" fill="{RED}"/><circle cx="42" cy="18" r="5" fill="#3a3a40"/><circle cx="60" cy="18" r="5" fill="#3a3a40"/>
<text class="bar" x="82" y="22">ru44@github: ~/avatar</text>
<line x1="0" y1="34" x2="720" y2="34" stroke="#26262b"/>
{text}
<g clip-path="url(#f)"><image class="pic" href="{DATA}" x="{X}" y="{Y - 8}" width="{W}" height="{rows * LH + 6:.0f}" preserveAspectRatio="xMidYMid slice"/></g>
{side}
</svg>'''

# --------------------------------------------------------------- 3. decrypt
def decrypt():
    X, Y, S, N = 36, 40, 200, 10
    c = S / N
    shades = ["#16161a", "#1f1f25", "#2a0a0a", "#3d0c0c", "#111114", "#52100f"]
    hexd = "0123456789abcdef"
    cells = []
    order = [(r, k) for r in range(N) for k in range(N)]
    random.shuffle(order)
    for i, (r, k) in enumerate(order):
        d = 0.4 + i * (4.2 / len(order))
        x, y = X + k * c, Y + r * c
        cells.append(
            f'<g class="cell" style="animation-delay:{d:.2f}s"><rect x="{x:.0f}" y="{y:.0f}" width="{c + .5:.1f}" height="{c + .5:.1f}" fill="{random.choice(shades)}"/>'
            f'<text x="{x + c / 2:.0f}" y="{y + c / 2 + 4:.0f}" text-anchor="middle">{random.choice(hexd)}{random.choice(hexd)}</text></g>')
    dump = []
    for i in range(7):
        off = f"{i * 16:08x}"
        by = " ".join("".join(random.choice(hexd) for _ in range(2)) for _ in range(8))
        dump.append(f'<text class="hex" style="animation-delay:{i * 0.35:.2f}s" x="270" y="{62 + i * 20}"><tspan fill="{DIM}">{off}</tspan>  {by}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 280" width="720" height="280" role="img" aria-label="RuM, portrait being decrypted">
<defs><clipPath id="f"><rect x="{X}" y="{Y}" width="{S}" height="{S}" rx="10"/></clipPath></defs>
<style>
  .cell {{ animation: cell 11s steps(1) infinite both; }}
  .cell text {{ font: 9px {MONO}; fill: {RED}; opacity: .8; }}
  .hex {{ font: 13px {MONO}; fill: {TEXT}; animation: hex 1.4s steps(1) infinite; }}
  .t {{ font: 14px {MONO}; fill: {TEXT}; }}
  .fill {{ animation: fill 11s linear infinite; }}
  .wait {{ animation: wait 11s steps(1) infinite; }}
  .ok {{ animation: ok 11s steps(1) infinite; fill: {RED}; font-weight: 700; }}
  @keyframes cell {{ 0% {{ opacity: 1; }} 1% {{ opacity: 0; }} 84% {{ opacity: 0; }} 86% {{ opacity: 1; }} 100% {{ opacity: 1; }} }}
  @keyframes hex {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .45; }} }}
  @keyframes fill {{ 0% {{ width: 0; }} 44% {{ width: 396px; }} 86% {{ width: 396px; }} 87%, 100% {{ width: 0; }} }}
  @keyframes wait {{ 0% {{ opacity: 1; }} 44% {{ opacity: 0; }} 87%, 100% {{ opacity: 1; }} }}
  @keyframes ok {{ 0% {{ opacity: 0; }} 44% {{ opacity: 1; }} 87%, 100% {{ opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .cell {{ animation: none; opacity: 0; }} .fill {{ animation: none; width: 396px; }} .wait {{ animation: none; opacity: 0; }} .ok {{ animation: none; opacity: 1; }} .hex {{ animation: none; }} }}
</style>
<rect width="720" height="280" rx="14" fill="{BG}"/>
<rect x=".5" y=".5" width="719" height="279" rx="14" fill="none" stroke="#26262b"/>
<g clip-path="url(#f)">
  <image href="{DATA}" x="{X}" y="{Y}" width="{S}" height="{S}"/>
  {"".join(cells)}
</g>
<rect x="{X}" y="{Y}" width="{S}" height="{S}" rx="10" fill="none" stroke="{RED}" stroke-width="1.5"/>
{"".join(dump)}
<text class="t wait" x="270" y="214">decrypting avatar.enc ...</text>
<text class="t ok" x="270" y="214">[+] access granted: RuM // push stealer</text>
<rect x="270" y="226" width="396" height="8" rx="4" fill="#1f1f25"/>
<rect class="fill" x="270" y="226" width="0" height="8" rx="4" fill="{RED}"/>
</svg>'''

for name, fn in (("glitch", glitch), ("terminal", terminal), ("decrypt", decrypt)):
    open(f"{out}/{name}.svg", "w").write(fn())
    print(name, len(fn()) // 1024, "KB")
