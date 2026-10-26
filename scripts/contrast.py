#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""WCAG contrast gate for the Audio Analyser website's colour tokens.

Adapted from scripts/contrast.py in github.com/sebastienrousseau/ssg-themes.github.io
(MIT): the same ratios and the same token pairs as the Prism theme, read from
this site's _layouts/styles.css in light mode and in both dark blocks (the
prefers-color-scheme one and the explicit toggle). Text needs 7:1 (WCAG AAA),
non-text UI 3:1.

Two additions over the theme's list:

- HOVER_PAIRS: the hover and inherited-text states the theme's list left
  out (a button label on its hover colour, body text on the soft surface
  behind code blocks and hovered menu items).
- rule_pairs(): every rule in the stylesheet that sets both `color` and
  `background` to a single token is checked at 7:1 as well, so a new
  component cannot pair two tokens without the gate seeing it.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

AAA_TEXT = 7.0
AAA_LARGE = 4.5
UI_NONTEXT = 3.0


def _linear(channel: int) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _linear(r) + 0.7152 * _linear(g) + 0.0722 * _linear(b)


def ratio(fg: str, bg: str) -> float:
    l1, l2 = luminance(fg), luminance(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)



def parse_tokens(css: str, selector: str) -> dict[str, str]:
    """Extracts `--name: #hex;` pairs from the first block matching `selector`."""
    idx = css.find(selector)
    if idx == -1:
        return {}
    block = css[idx: css.find("}", idx)]
    return {
        name: value
        for name, value in re.findall(
            r"(--[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\s*;", block
        )
    }



PAIRS = [
    ("--ink", "--bg", AAA_TEXT, "body text on page ground"),
    ("--ink", "--surface", AAA_TEXT, "body text on surface"),
    ("--ink-soft", "--bg", AAA_TEXT, "secondary text on ground"),
    ("--ink-soft", "--surface", AAA_TEXT, "secondary text on surface"),
    ("--ink-muted", "--bg", AAA_TEXT, "muted text on ground"),
    ("--ink-muted", "--surface", AAA_TEXT, "muted text on surface"),
    ("--ink-muted", "--surface-soft", AAA_TEXT, "muted text on soft surface"),
    ("--accent", "--bg", AAA_TEXT, "link on ground"),
    ("--accent", "--surface", AAA_TEXT, "link on surface"),
    ("--accent", "--surface-soft", AAA_TEXT, "link on soft surface"),
    ("--accent-ink", "--accent", AAA_TEXT, "button label on accent"),
    ("--accent-hover", "--surface", AAA_TEXT, "hovered link on surface"),
    ("--on-accent-soft", "--accent-soft", AAA_TEXT, "badge text on accent tint"),
    ("--focus", "--bg", UI_NONTEXT, "focus ring against ground"),
    ("--focus", "--surface", UI_NONTEXT, "focus ring against surface"),
    ("--line", "--surface", UI_NONTEXT, "control border against surface"),
    ("--line", "--bg", UI_NONTEXT, "control border against ground"),
]

PRISM_PAIRS = [
    ("--hero-ink", "--hero-bg", AAA_TEXT, "masthead text on navy"),
    ("--hero-ink-soft", "--hero-bg", AAA_TEXT, "masthead secondary text on navy"),
    ("--hero-ink", "--hero-surface", AAA_TEXT, "masthead text on raised navy"),
    ("--hero-ink-soft", "--hero-surface", AAA_TEXT, "masthead secondary text on raised navy"),
    ("--hero-accent", "--hero-bg", AAA_TEXT, "eyebrow on navy"),
    ("--hero-accent", "--hero-bg", UI_NONTEXT, "masthead focus ring against navy"),
    ("--hero-accent", "--hero-surface", UI_NONTEXT, "masthead focus ring against raised navy"),
    ("--hero-clay", "--hero-bg", AAA_TEXT, "developer eyebrow on navy"),
    ("--hero-clay", "--hero-surface", AAA_TEXT, "notification title on raised navy"),
    ("--hero-gold", "--hero-bg", AAA_TEXT, "wordmark dot on navy"),
    ("--hero-line", "--hero-bg", UI_NONTEXT, "masthead border against navy"),
    ("--hero-bg", "--hero-ink", AAA_TEXT, "hero button label on white"),
    ("--code-plain", "--code-bg", AAA_TEXT, "code text"),
    ("--code-keyword", "--code-bg", AAA_TEXT, "code keyword"),
    ("--code-function", "--code-bg", AAA_TEXT, "code function"),
    ("--code-string", "--code-bg", AAA_TEXT, "code string"),
    ("--code-comment", "--code-bg", AAA_TEXT, "code comment"),
    ("--code-comment", "--code-bar", AAA_TEXT, "code window title"),
    ("--code-property", "--code-bg", AAA_TEXT, "code property"),
    ("--code-number", "--code-bg", AAA_TEXT, "code number"),
    ("--green-text", "--green-soft", AAA_TEXT, "green tag text on tint"),
    ("--green-text", "--surface", AAA_TEXT, "green text on surface"),
    ("--green-text", "--bg-soft", AAA_TEXT, "metric figure on soft ground"),
    ("--green", "--surface", UI_NONTEXT, "green rule against surface"),
    ("--green", "--bg-soft", UI_NONTEXT, "green rule against soft ground"),
    ("--clay-text", "--clay-soft", AAA_TEXT, "clay tag text on tint"),
    ("--clay-text", "--surface", AAA_TEXT, "clay label on surface"),
    ("--gold-text", "--gold-soft", AAA_TEXT, "gold tag text on tint"),
    ("--burgundy-text", "--burgundy-soft", AAA_TEXT, "burgundy tag text on tint"),
    ("--ink-soft", "--bg-soft", AAA_TEXT, "secondary text on soft ground"),
    ("--ink", "--bg-soft", AAA_TEXT, "body text on soft ground"),
    ("--accent", "--bg-soft", AAA_TEXT, "link on soft ground"),
    ("--ink-muted", "--bg-soft", AAA_TEXT, "muted text on soft ground"),
    ("--line", "--bg-soft", UI_NONTEXT, "control border against soft ground"),
    # The white glyph on each icon badge, against the *lightest* stop of
    # that badge's gradient — the stop that decides whether the icon can
    # be seen. WCAG 1.4.11 (3:1). These were literals inside the
    # component rule until the gate could reach them, and two of them
    # sat at 2.5:1.
    ("--badge-ink", "--badge-blue-to", UI_NONTEXT, "glyph on the blue badge"),
    ("--badge-ink", "--badge-clay-to", UI_NONTEXT, "glyph on the clay badge"),
    ("--badge-ink", "--badge-green-to", UI_NONTEXT, "glyph on the green badge"),
    ("--badge-ink", "--badge-gold-to", UI_NONTEXT, "glyph on the gold badge"),
    ("--badge-ink", "--badge-burgundy-to", UI_NONTEXT, "glyph on the burgundy badge"),
    ("--badge-ink", "--badge-navy-to", UI_NONTEXT, "glyph on the navy badge"),
    ("--badge-ink", "--badge-blue-from", UI_NONTEXT, "glyph on the blue badge, dark stop"),
    ("--badge-ink", "--badge-clay-from", UI_NONTEXT, "glyph on the clay badge, dark stop"),
    ("--badge-ink", "--badge-green-from", UI_NONTEXT, "glyph on the green badge, dark stop"),
    ("--badge-ink", "--badge-gold-from", UI_NONTEXT, "glyph on the gold badge, dark stop"),
    ("--badge-ink", "--badge-burgundy-from", UI_NONTEXT, "glyph on the burgundy badge, dark stop"),
    ("--badge-ink", "--badge-navy-from", UI_NONTEXT, "glyph on the navy badge, dark stop"),
]

HOVER_PAIRS = [
    ("--accent-ink", "--accent-hover", AAA_TEXT, "button label on hovered accent"),
    ("--ink", "--surface-soft", AAA_TEXT, "body text on soft surface (code, hovered items)"),
    ("--ink-soft", "--surface-soft", AAA_TEXT, "secondary text on soft surface"),
    ("--hero-bg", "--hero-ink-soft", AAA_TEXT, "hero button label on hover"),
    ("--hero-ink-soft", "--hero-surface", AAA_TEXT, "masthead menu text on raised navy"),
    ("--hero-accent", "--hero-surface", AAA_TEXT, "masthead accent text on raised navy"),
    ("--code-plain", "--code-bar", AAA_TEXT, "code text on the window title bar"),
]

RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
COLOR = re.compile(r"(?<![-\w])color:\s*var\((--[a-z0-9-]+)\)\s*;")
BACKGROUND = re.compile(r"background(?:-color)?:\s*var\((--[a-z0-9-]+)\)\s*;")


def rule_pairs(css: str) -> list[tuple[str, str, float, str]]:
    """Every rule that sets both colour and background to one token each."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    pairs = []
    for selector, body in RULE.findall(css):
        fg, bg = COLOR.search(body), BACKGROUND.search(body)
        if fg and bg:
            label = "rule " + " ".join(selector.split())
            pairs.append((fg.group(1), bg.group(1), AAA_TEXT, label))
    return pairs


MODES = (
    ("light", ":root,"),
    ("dark (system)", ':root:not([data-theme="light"]) {'),
    ("dark (toggle)", ':root[data-theme="dark"] {'),
)


def main() -> int:
    css = (Path(__file__).resolve().parent.parent / "_layouts" / "styles.css").read_text(encoding="utf-8")
    failures, checked = [], 0
    for mode, selector in MODES:
        tokens = parse_tokens(css, selector)
        if not tokens:
            failures.append(f"{mode}: no tokens found for `{selector}`")
            continue
        for fg, bg, target, label in PAIRS + PRISM_PAIRS + HOVER_PAIRS + rule_pairs(css):
            if fg not in tokens or bg not in tokens:
                failures.append(f"{mode}: {fg} or {bg} not declared ({label})")
                continue
            got = ratio(tokens[fg], tokens[bg])
            checked += 1
            if got + 1e-9 < target:
                failures.append(f"{mode}: {label}: {tokens[fg]} on {tokens[bg]} = {got:.2f}:1, need {target}:1")
    if failures:
        print(f"contrast: {len(failures)} failure(s)", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        return 1
    print(f"contrast: {checked} token pairs pass (text 7:1, UI 3:1) in light and dark")
    return 0


if __name__ == "__main__":
    sys.exit(main())
