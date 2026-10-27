"""Gera o card neofetch do README: Aang em ASCII colorido + informações."""
import sys
from html import escape
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

src, out = sys.argv[1], sys.argv[2]

COLS, ROWS = 78, 43
AFS, ALH = 8.4, 10.2        # fonte e linha da arte
ACW = AFS * 0.602           # largura de um caractere da arte
FS, LH = 12, 14.5           # fonte e linha do painel
CW = FS * 0.602
RAMP = " .,:;irsXA253hMHGS#9B&@"  # do mais claro ao mais denso (fundo escuro)

img = Image.open(src).convert("RGB").crop((40, 0, 420, 400))
img = ImageEnhance.Contrast(img).enhance(1.25)
img = ImageEnhance.Color(img).enhance(1.35)
small = img.resize((COLS, ROWS), Image.LANCZOS)
gray = ImageOps.autocontrast(ImageOps.grayscale(small), cutoff=2)
# realça contornos (sobrancelhas, olhos, boca) puxando a densidade para baixo nas bordas
edges = ImageOps.autocontrast(ImageOps.grayscale(small).filter(ImageFilter.FIND_EDGES), cutoff=4)

BG = "#0d1117"
lines = []
for y in range(ROWS):
    runs, cur_color, cur_text = [], None, ""
    for x in range(COLS):
        r, g, b = small.getpixel((x, y))
        lum = (gray.getpixel((x, y)) / 255) ** 1.6
        if edges.getpixel((x, y)) > 150:
            lum *= 0.45
        ch = RAMP[min(len(RAMP) - 1, int(lum * (len(RAMP) - 1) + 0.5))]
        # clareia levemente para ler bem no fundo escuro
        r, g, b = (min(255, int(c * 1.12 + 18)) for c in (r, g, b))
        color = f"#{r:02x}{g:02x}{b:02x}"
        if ch == " ":
            color = cur_color or color
        if color != cur_color and cur_text:
            runs.append((cur_color, cur_text))
            cur_text = ""
        cur_color = color
        cur_text += ch
    runs.append((cur_color, cur_text))
    lines.append(runs)

AX, AY = 28, 34
art_w = COLS * ACW
svg_rows = []
for i, runs in enumerate(lines):
    spans = "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for c, t in runs)
    svg_rows.append(
        f'<text class="a" style="animation-delay:{i * 0.025:.3f}s" x="{AX}" y="{AY - 8 + i * ALH:.1f}" '
        f'textLength="{art_w:.1f}" lengthAdjust="spacingAndGlyphs">{spans}</text>'
    )

# painel de informações (estilo neofetch)
K, V, D, T = "#e8a33d", "#e6edf3", "#7d8590", "#58a6ff"
info = [
    ("title", "gabriel@sena"),
    ("rule", ""),
    ("kv", "SO", "Windows 11, Linux"),
    ("kv", "Local", "Sarandi, PR, Brasil"),
    ("kv", "Trabalho", "Desenvolvedor na Simpliza"),
    ("kv", "Faculdade", "Eng. de Software, Unicesumar"),
    ("kv", "Elemento", "Ar (o resto eu ainda estou treinando)"),
    ("gap",),
    ("kv", "Linguagens", "PHP, Java, TypeScript, JavaScript"),
    ("kv", "Back-end", "Laravel, Spring Boot"),
    ("kv", "Front-end", "React, Inertia, Tailwind"),
    ("kv", "Mobile", "React Native (Expo)"),
    ("kv", "Dados", "MySQL, PostgreSQL"),
    ("kv", "Ferramentas", "Docker, Git, Linux"),
    ("gap",),
    ("section", "Projetos"),
    ("kv", "CotaCar", "cotação automotiva, no ar"),
    ("kv", "LIMIO", "marketplace de serviços, em dev"),
    ("gap",),
    ("quote", '"É importante tirar sabedoria de vários'),
    ("quote", '  lugares diferentes." · Tio Iroh'),
]

IX = AX + art_w + 34
iy = AY + 6
info_svg = []
n = 0
for item in info:
    kind = item[0]
    delay = f'style="animation-delay:{0.9 + n * 0.07:.2f}s"'
    if kind == "title":
        info_svg.append(f'<text class="i t" {delay} x="{IX}" y="{iy}"><tspan fill="{K}">gabriel</tspan><tspan fill="{V}">@</tspan><tspan fill="{K}">sena</tspan></text>')
    elif kind == "rule":
        info_svg.append(f'<text class="i" {delay} x="{IX}" y="{iy}" fill="{D}">{"─" * 46}</text>')
    elif kind == "kv":
        _, k, v = item
        info_svg.append(f'<text class="i" {delay} x="{IX}" y="{iy}"><tspan fill="{K}">{escape(k)}</tspan><tspan fill="{D}">: </tspan><tspan fill="{V}">{escape(v)}</tspan></text>')
    elif kind == "section":
        info_svg.append(f'<text class="i" {delay} x="{IX}" y="{iy}"><tspan fill="{D}">── </tspan><tspan fill="{T}">{escape(item[1])}</tspan><tspan fill="{D}"> {"─" * 34}</tspan></text>')
    elif kind == "quote":
        info_svg.append(f'<text class="i q" {delay} x="{IX}" y="{iy}" fill="{D}">{escape(item[1])}</text>')
    if kind != "gap":
        n += 1
    iy += LH * 1.32 if kind != "gap" else LH * 0.7

# paleta do terminal no rodapé
palette = ["#0d1117", "#c0392b", "#e8a33d", "#3fb950", "#58a6ff", "#bc8cff", "#39c5cf", "#e6edf3"]
py = max(iy, AY) + 4
pal = "".join(f'<rect class="i" style="animation-delay:{0.9 + n * 0.07:.2f}s" x="{IX + j * 26}" y="{py:.0f}" width="22" height="12" rx="2" fill="{c}" stroke="#30363d"/>' for j, c in enumerate(palette))

W = int(IX + 46 * CW * 1.04 + 28)
H = int(max(AY - 8 + ROWS * ALH, py + 12) + 22)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="'JetBrains Mono','Cascadia Code',Consolas,Menlo,'DejaVu Sans Mono',monospace" font-size="{FS}">
<style>
.a,.i{{opacity:0;animation:in .5s ease-out forwards}}
.a{{white-space:pre;font-size:{AFS}px}}
.t{{font-weight:700;font-size:{FS + 2}px}}
.q{{font-style:italic}}
@keyframes in{{to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.a,.i{{animation:none;opacity:1}}}}
</style>
<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="#30363d"/>
{"".join(svg_rows)}
{"".join(info_svg)}
{pal}
</svg>'''

with open(out, "w", encoding="utf-8") as f:
    f.write(svg)
print(W, H)
