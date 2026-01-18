# Cursor AI Configuration Files

This directory contains configuration and reference files to help maintain consistency when working with Cursor AI on this project.

## Files Overview

### `.cursorrules` (Root directory)
**Main configuration file** - Cursor AI automatically reads this file to understand project standards, conventions, and best practices.

Contains:
- Complete design system documentation (colors, typography, spacing)
- Layout structure standards
- SEO requirements and checklist
- Accessibility standards (WCAG 2.1 AA)
- Code style guidelines
- Common patterns and examples

**This is the primary reference file that Cursor AI will use for all prompts.**

### `.cursor/QUICK_REFERENCE.md`
Quick lookup guide with:
- Common code patterns
- Quick checklists
- Don'ts list
- Validation commands

Use this for fast reference during development.

## How It Works

When you use Cursor AI in this project:

1. **Cursor automatically reads** `.cursorrules` to understand project context
2. **AI suggestions follow** the design system, SEO standards, and code patterns defined
3. **Consistency is maintained** across all AI-assisted edits
4. **Quality is ensured** through documented checklists and standards

## When to Update

Update `.cursorrules` when:
- Design system changes (new colors, fonts, spacing)
- New SEO requirements are added
- Accessibility standards evolve
- Project structure significantly changes
- New code patterns become standard

## Usage Tips

- Reference `.cursorrules` when asking AI to make changes - it will follow these standards
- Use `QUICK_REFERENCE.md` for quick lookups during development
- Keep these files in version control for team consistency

---

**Note**: The `.cursorrules` file uses a simple text format that Cursor AI reads automatically. No special setup required - just ensure the file exists in the project root.

