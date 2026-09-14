---
name: social-carousel
description: |
  A three-card social-media carousel laid out as 1080×1080 squares —
  three cinematic, on-brand panels with display headlines that connect
  across the series ("onwards." → "to the next one." → "looking ahead.").
  Each card has a brand mark, a number / total, a caption, and a "loop"
  affordance. Use when the brief asks for a "carousel post", "social
  carousel", "Instagram carousel", "LinkedIn series", "X thread cards",
  or "三连发".
triggers:
  - "social carousel"
  - "carousel post"
  - "instagram carousel"
  - "linkedin carousel"
  - "x thread cards"
  - "social series"
  - "三连发"
  - "轮播图"
od:
  mode: prototype
  platform: desktop
  scenario: marketing
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  example_prompt: "Design a 3-card cinematic social carousel — ‘onwards.’, ‘to the next one.’, ‘looking ahead.’. 1080×1080 squares, drop-into-Instagram ready."
---

# Social Carousel Skill

Produce a 3-panel social carousel on a single dark stage. Each panel is a
1080×1080 cinematic still — connected as a series, but each readable on its
own.

## Multi-Agent Execution Setup

When this skill is invoked, the executing agent MUST spawn and consult four specialized subagents to collaborate on the generation:
1. **Design Gráfico Expert:** Reviews the visual composition, background gradients, styling tokens, and compliance with the design system.
2. **HTML Expert:** Audits markup semantics, structural cleanlines, and verifies target data-od-id attributes.
3. **Social Media Expert:** Optimizes copy layout, text hierarchy, and guarantees structures commonly engaging for Instagram posts.
4. **UX Expert:** Checks readability, contrast ratios, and ensures perfect geometric alignment and spacing for all icons and captions.

## Workflow

1. **Read the active DESIGN.md** (injected above). Pick the loudest serif
   token for the headline lockups and a mono token for stamps / counters.
2. **Icons Setup (CDN):** Load an open-source icon library (e.g., Lucide Icons, Font Awesome, or Google Material Symbols) via a public CDN inside the `<head>` or via `<script>`.
3. **Pick the theme + 3 captions** from the brief. The captions must read
   as one sentence when stacked: ("onwards." → "to the next one." →
   "looking ahead." or "input." → "iterate." → "ship.").
4. **Stage** — full-bleed dark page. Top header strip:
   - Left: serif italic display "Three posts. One beat."
   - Just below the title: a one-line description in muted mono ("1080×1080
     · cinematic video loops · minimal type. Drop into Instagram, LinkedIn,
     or X — each post stands on its own or runs as a three-part series.").
   - Right: small mono badge "SERIES · 01 → 03".
5. **Cards** — 3 squares in a horizontal row (wraps to stack on narrow
   viewports). Each card is `aspect-ratio: 1 / 1` with rounded 12px corners
   and a subtle 1px border, plus a soft drop shadow.
   - Background: a layered gradient that *suggests* a cinematic photo — for
     example, panel 1 = warm dawn meadow (stacked greens with a cyan sky
     wash); panel 2 = forest dusk (warm oranges fading into deep teals);
     panel 3 = pink-mountain ridge (rosy peaks against a dim violet sky).
     Use `radial-gradient` + `linear-gradient` only — no images.
   - Top-left chip: brand wordmark in serif italic ("Jerrod Lew") with a
     small accent dot.
   - Top-left below chip: micro mono index "AI · 01 / 03" (and 02, 03).
   - Bottom-left: the headline lockup in white serif display, italic accent
     on one word.
   - Bottom-right corner: a `1× LOOP` mono stamp inside a thin border.
   - Bottom strip caption: small caps mono describing the imagined frame
     ("Man, walking forward — close.", "Woman, stepping into frame.",
     "Woman, overlooking the city.").
6. **Icons Layout & Alignment (UX & HTML Review):**
   - Place relevant open-source icons alongside wordmarks, indexes, or captions.
   - All icon containers must use Flexbox (`display: inline-flex; align-items: center; justify-content: center; gap: [X]px;`) to achieve perfect vertical and horizontal alignment.
   - Icons must have a fixed bounding box (e.g., `width: 16px; height: 16px;`) so layout spacing remains identical regardless of the icon's shape.
7. **Write** a single HTML document:
   - `<!doctype html>` through `</html>`, CSS inline.
   - Cards are sized via `width: clamp(280px, 30vw, 380px)` so 3 fit
     comfortably across most desktops and stack at < 1100px.
   - `data-od-id` on stage, each card, each headline.
8. **Self-check**:
   - The three headlines together form one sentence and feel cinematic.
   - Mono is used only for the wordmark index, the loop stamp, and the
     bottom captions. The headlines stay serif.
   - Each panel's color story is distinct — no two share a dominant hue.
   - Icons are loaded correctly via CDN, spaced symmetrically, and fully aligned.

## Output contract

Emit between `<artifact>` tags:

```
<artifact identifier="carousel-slug" type="text/html" title="Carousel — Title">
<!doctype html>
<html>...</html>
</artifact>
```

One sentence before the artifact, nothing after.
