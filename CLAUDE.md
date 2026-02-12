# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Quarto-based blog website (ouilogique.com) configured as `project.type: website` (Quarto does not have a separate `blog` type - blogs are implemented as websites). The site generates static HTML content with:

- Blog posts in the `posts/` directory (organized by date)
- Static pages in the `pages/` directory
- Custom post-render processing for navigation and directory flattening
- Deployment to GitHub Pages via GitHub Actions

## Build Commands

```bash
# Install Python dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r _requirements.txt

# Render the entire site
quarto render

# Preview the site locally
quarto preview
```

## Post-Render Processing Pipeline

After `quarto render` completes, two post-render scripts run automatically (configured in `_quarto.yml` under `project.post-render`):

1. **`_scripts/flatten-pages-to-root.sh`**: Moves subdirectories from `_site/pages/` to `_site/` root (e.g., `_site/pages/radios/` → `_site/radios/`). The `pages/index.html` remains at `_site/pages/`.

2. **`_scripts/create_prev_next_buttons.py`**: Generates prev/next navigation links for all blog posts by:

   - Parsing `_site/sitemap.xml` to get chronologically sorted post URLs
   - Replacing `href="#"` placeholders in `_includes/prev-next-include.html` with relative links
   - For the home page, "Précédent" links to the newest post and "Suivant" to the oldest
   - For individual posts, links navigate chronologically through the post sequence

## Project Structure

- `posts/YYYY-MM-DD-slug/index.qmd`: Blog posts (dated, sorted chronologically)
- `posts/_metadata.yml`: Shared frontmatter for all posts (includes prev-next navigation HTML)
- `pages/*/`: Static pages (cours-html-embarque, enum, radios, scratchpad)
- `_includes/`: HTML snippets injected into pages

  - `prev-next-include.html`: Navigation template with `href="#"` placeholders
  - `scripts.html`: Global scripts
  - `material-symbols.html`: Material Symbols icon font

- `_scripts/`: Build-time processing scripts
- `custom.scss`: Site-wide styling overrides
- `images/`: Site assets (favicon, logo, etc.)

## Navigation Architecture

Posts use a placeholder-based navigation system:

1. Posts include `_includes/prev-next-include.html` twice (before and after body) via `posts/_metadata.yml`
2. The HTML contains `<a href="#">` placeholder links
3. `create_prev_next_buttons.py` replaces these placeholders with actual relative URLs post-render
4. This approach avoids Quarto variable limitations and works with the sitemap-based ordering

## Deployment

The site deploys automatically via `.github/workflows/publish.yml`:

- Triggers on push to `gh-pages` branch
- Sets up Quarto, Python 3.12, and dependencies
- Runs `quarto render`
- Deploys `_site/` to GitHub Pages

## Development Notes

- The site uses the Cyborg theme with custom SCSS overrides
- Execution is disabled (`execute: enabled: false` in `_quarto.yml`)
- Search is disabled
- The logo has a custom animation (see `custom.scss`)
