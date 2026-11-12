
from PIL import Image, ImageOps, ImageEnhance
from xml.sax.saxutils import escape
from pathlib import Path

# Input and output
INPUT = "assets/profile.jpeg"
OUTPUT = "assets/dev-panel.svg"

# ASCII character ramp: dark to bright
CHARS = " .,:;!|/\\()[]{}?+=-*#%@ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Portrait dimensions
COLS = 48
ROWS = 45
CELL_W = 9
CELL_H = 10

# Load and process photograph
img = Image.open(INPUT).convert("RGB")
img = ImageOps.fit(img, (COLS, ROWS))
img = ImageOps.grayscale(img)
img = ImageEnhance.Contrast(img).enhance(1.5)

# Generate SVG
svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="1100" height="570" viewBox="0 0 1100 570">',
    '<rect width="1100" height="570" rx="16" fill="#0D1117"/>',
    '<rect width="1100" height="55" rx="16" fill="#161B22"/>',
    '<rect y="40" width="1100" height="15" fill="#161B22"/>',

    # Window controls
    '<circle cx="25" cy="27" r="7" fill="#FF5F57"/>',
    '<circle cx="48" cy="27" r="7" fill="#FEBC2E"/>',
    '<circle cx="71" cy="27" r="7" fill="#28C840"/>',

    '<text x="105" y="33" fill="#8B949E" '
    'font-family="monospace" font-size="17">'
    'kshitij@developer: ~/profile</text>',

    '<text x="930" y="33" fill="#7EE787" '
    'font-family="monospace" font-size="14">● ONLINE</text>',

    '<text x="25" y="85" fill="#79C0FF" '
    'font-family="monospace" font-size="15">'
    '01  developer_identity.js</text>',

    '<line x1="455" y1="105" x2="455" y2="545" '
    'stroke="#30363D"/>',

    '<g font-family="monospace" font-size="9" '
    'xml:space="preserve">'
]

# Convert each pixel into a code character
for y in range(ROWS):
    for x in range(COLS):
        brightness = img.getpixel((x, y))

        index = int(brightness / 255 * (len(CHARS) - 1))
        char = CHARS[index]

        # Subtle blue-to-white character shading
        intensity = int(95 + brightness * 0.62)
        blue = min(255, intensity + 15)
        color = f"#{intensity:02x}{min(255, intensity + 8):02x}{blue:02x}"

        if char != " ":
            svg.append(
                f'<text x="{25 + x * CELL_W}" '
                f'y="{120 + y * CELL_H}" '
                f'fill="{color}">{escape(char)}</text>'
            )

svg.append('</g>')

# Right-side syntax-highlighted developer information
code_lines = [
    ("const developer = {", "#D2A8FF"),
    ('  name: "Kshitij Jha",', "#7EE787"),
    ('  username: "kshitij1029",', "#7EE787"),
    ('  role: "Full Stack Developer",', "#7EE787"),
    ('  education: "B.Tech CSE | GGSIPU",', "#7EE787"),
    ('  cgpa: 9.15,', "#F2CC60"),
    ('  additional: "IIT Madras BS DS Foundation",', "#FFA657"),
    ('', "#8B949E"),
    ('  languages: ["Java", "Python",', "#79C0FF"),
    ('              "JavaScript"],', "#79C0FF"),
    ('  frontend: ["React", "HTML", "Tailwind"],', "#79C0FF"),
    ('  backend: ["Node.js", "Express.js"],', "#79C0FF"),
    ('  database: ["MongoDB", "MySQL"],', "#79C0FF"),
    ('  tools: ["Git", "GitHub", "Figma"],', "#79C0FF"),
    ('', "#8B949E"),
    ('  currentlyLearning: ["AI", "ML", "DSA"],', "#FFA657"),
    ('  interests: ["Development", "Design"],', "#FFA657"),
    ('  status: "Always building something new"', "#7EE787"),
    ("};", "#D2A8FF"),
]

svg.append(
    '<g font-family="Courier New, monospace" font-size="17">'
)

for i, (line, color) in enumerate(code_lines):
    if line:
        svg.append(
            f'<text x="490" y="{125 + i * 23}" '
            f'fill="{color}">{escape(line)}</text>'
        )

svg.append('</g>')

# Footer
svg.append(
    '<rect x="0" y="535" width="1100" height="35" '
    'fill="#161B22"/>'
)
svg.append(
    '<text x="25" y="558" fill="#8B949E" '
    'font-family="monospace" font-size="12">'
    'ASCII PORTRAIT  |  DEVELOPER PROFILE  |  UTF-8'
    '</text>'
)
svg.append(
    '<text x="950" y="558" fill="#7EE787" '
    'font-family="monospace" font-size="12">'
    'BUILD v1.0</text>'
)
svg.append('</svg>')

Path(OUTPUT).write_text("\n".join(svg), encoding="utf-8")

print(f"Successfully generated: {OUTPUT}")
