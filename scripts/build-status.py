"""Builds the animated "status" terminals shown on the profile.

Edit MOTD and STATUS below, then run:
    python3 scripts/build-status.py assets/status
One SVG is written per style; the weekly workflow copies one to assets/status.svg.
"""
import sys
from html import escape

MOTD = "!Pro chess player, Grandmaster at Smite, big potato developer."
# (marker, label, text)
STATUS = [
    ("+", "building", "the new BlackArch Linux website"),
    ("+", "hacking on", "my personal page, ru44.github.io"),
    ("+", "learning", "Rust"),
    ("*", "goals", "master (T,J)S, Rust and GitOps"),
    ("!", "fun fact", "RuM does not mean R u M"),
]

BG, BORDER = "#0a0a0b", "#26262b"
RED, TEXT, DIM, BLUE, GREEN, WHITE = "#e60000", "#c9c9ce", "#6b6b74", "#5c9dff", "#3fb950", "#ffffff"
MONO = "ui-monospace, 'JetBrains Mono', 'Fira Code', Menlo, Consolas, monospace"
WIDTH, LEFT, TOP, LINE = 760, 24, 62, 22
TYPE_SPEED, LINE_GAP, HOLD = 0.055, 0.16, 7.0  # seconds


class Terminal:
    """Collects lines with the time at which each one appears."""

    def __init__(self, title):
        self.title, self.rows, self.clock = title, [], 0.4

    def blank(self):
        self.rows.append(None)

    def out(self, *segments, pause=LINE_GAP):
        """Prints a whole line at once. A segment is (text, colour)."""
        self.rows.append([(text, colour, self.clock) for text, colour in segments])
        self.clock += pause

    def typed(self, prompt, command):
        """Shows the prompt, then types the command one character at a time."""
        row = [(text, colour, self.clock) for text, colour in prompt]
        self.clock += 0.35
        for char in command:
            row.append((char, WHITE, self.clock))
            self.clock += TYPE_SPEED
        self.rows.append(row)
        self.clock += 0.45

    def svg(self, label):
        cycle = self.clock + HOLD
        visible = 100 * (cycle - self.clock - 0.6) / cycle  # every line is gone before the loop restarts
        height = TOP + len(self.rows) * LINE + 14
        lines = []
        for i, row in enumerate(self.rows):
            if not row:
                continue
            spans = "".join(
                f'<tspan class="s" style="animation-delay:{start:.2f}s" fill="{colour}">{escape(text)}</tspan>'
                for text, colour, start in row
            )
            lines.append(f'<text x="{LEFT}" y="{TOP + i * LINE}" xml:space="preserve">{spans}</text>')
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" height="{height}" role="img" aria-label="{escape(label)}">
<style>
  text {{ font: 14px {MONO}; white-space: pre; }}
  .bar {{ font-size: 12px; fill: {DIM}; }}
  .s {{ opacity: 0; animation: show {cycle:.2f}s linear infinite; }}
  @keyframes show {{ 0% {{ opacity: 0; }} 0.2% {{ opacity: 1; }} {visible:.1f}% {{ opacity: 1; }} {visible + 1.5:.1f}%, 100% {{ opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .s {{ animation: none; opacity: 1; }} }}
</style>
<rect width="{WIDTH}" height="{height}" rx="14" fill="{BG}"/>
<rect x=".5" y=".5" width="{WIDTH - 1}" height="{height - 1}" rx="14" fill="none" stroke="{BORDER}"/>
<circle cx="24" cy="18" r="5" fill="{RED}"/><circle cx="42" cy="18" r="5" fill="#3a3a40"/><circle cx="60" cy="18" r="5" fill="#3a3a40"/>
<text class="bar" x="82" y="22">{escape(self.title)}</text>
<line x1="0" y1="34" x2="{WIDTH}" y2="34" stroke="{BORDER}"/>
{chr(10).join(lines)}
</svg>
"""


MARKER_COLOUR = {"+": GREEN, "*": BLUE, "!": RED}


def prompt_style():
    """Kali-style prompt: commands are typed, output prints."""
    term = Terminal("ru44@github: ~")
    top = [("┌──(", BLUE), ("ru44㉿github", RED), (")-[", BLUE), ("~", WHITE), ("]", BLUE)]
    bottom = [("└─", BLUE), ("$ ", RED)]

    def run(command):
        term.out(*top, pause=0.1)
        term.typed(bottom, command)
        term.blank()

    run("cat /etc/motd")
    term.out(("  " + MOTD, TEXT), pause=0.5)
    term.blank()
    run("./status --now")
    width = max(len(label) for _, label, _ in STATUS)
    for marker, label, text in STATUS:
        term.out(("  [", DIM), (marker, MARKER_COLOUR[marker]), ("] ", DIM), (label.ljust(width + 2), WHITE), (text, TEXT))
    term.blank()
    term.out(*top, pause=0.1)
    term.out(*bottom, ("█", RED))
    return term


def nmap_style():
    """The same facts as an nmap scan report."""
    term = Terminal("ru44@github: ~/recon")
    term.typed([("ru44@github", RED), (":~$ ", TEXT)], "nmap -sV --script=whoami ru44")
    term.out(("Starting Nmap ( https://nmap.org )", DIM), pause=0.5)
    term.out(("Nmap scan report for ", TEXT), ("ru44", RED), (" (push stealer)", TEXT))
    term.out(("Host is up (0.0013s latency).", TEXT), pause=0.5)
    term.blank()
    ports = ["22/tcp", "80/tcp", "443/tcp", "1337/tcp", "31337/tcp"]
    state = {"+": ("open", GREEN), "*": ("filtered", BLUE), "!": ("open", RED)}
    width = max(len(label) for _, label, _ in STATUS)
    term.out(("PORT".ljust(11) + "STATE".ljust(10) + "SERVICE".ljust(width + 2) + "VERSION", DIM))
    for port, (marker, label, text) in zip(ports, STATUS):
        word, colour = state[marker]
        term.out((port.ljust(11), WHITE), (word.ljust(10), colour), (label.ljust(width + 2), WHITE), (text, TEXT), pause=0.3)
    term.blank()
    term.out(("Service Info: ", DIM), (MOTD, TEXT), pause=0.4)
    term.blank()
    term.out(("Nmap done: 1 human scanned, ", DIM), ("5 ports of interest", RED))
    return term


def systemd_style():
    """The same facts as `systemctl status`."""
    term = Terminal("ru44@github: ~")
    term.typed([("ru44@github", RED), (":~$ ", TEXT)], "systemctl status rum.service")
    term.out(("● ", GREEN), ("rum.service", WHITE), (" - " + MOTD, TEXT), pause=0.4)
    term.out(("     Loaded: ", DIM), ("loaded (/home/ru44/.config/rum.service; ", TEXT), ("enabled", GREEN), (")", TEXT))
    term.out(("     Active: ", DIM), ("active (running)", GREEN), (" since boot", TEXT))
    term.out(("      Tasks: ", DIM), (f"{len(STATUS)}", TEXT))
    term.out(("     CGroup: ", DIM), ("/user.slice/ru44", TEXT), pause=0.4)
    width = max(len(label) for _, label, _ in STATUS)
    for i, (marker, label, text) in enumerate(STATUS):
        branch = "└─" if i == len(STATUS) - 1 else "├─"
        term.out(("             " + branch + " ", DIM), (label.ljust(width + 2), MARKER_COLOUR[marker]), (text, TEXT), pause=0.3)
    term.blank()
    term.out(("ru44@github", RED), (":~$ ", TEXT), ("█", RED))
    return term


STYLES = {"prompt": prompt_style, "nmap": nmap_style, "systemd": systemd_style}

if __name__ == "__main__":
    out = sys.argv[1]
    label = f"{MOTD} " + " ".join(f"{name}: {text}." for _, name, text in STATUS)
    for name, build in STYLES.items():
        with open(f"{out}/{name}.svg", "w", encoding="utf-8") as file:
            file.write(build().svg(label))
        print(f"{out}/{name}.svg")
