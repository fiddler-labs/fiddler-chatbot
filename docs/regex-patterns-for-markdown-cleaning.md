# Regex Patterns for Markdown Cleaning - Reference Guide

## Overview

This reference document provides regex patterns for cleaning markdown files at scale using VS Code's Search and Replace functionality. The patterns are designed to handle various GitBook-specific elements and YAML metadata cleaning tasks.

## Table of Contents

1. [YAML Metadata Cleaning](#1-yaml-metadata-cleaning)
2. [GitBook Asset Image Removal](#2-gitbook-asset-image-removal)
3. [GitBook Include Statement Removal](#3-gitbook-include-statement-removal)
4. [Usage Instructions](#4-usage-instructions)
5. [Pattern Components Reference](#5-pattern-components-reference)

---

## 1. YAML Metadata Cleaning

### Purpose

Clean YAML front matter in markdown files to retain only essential fields: `title`, `excerpt`, and `metadata.description`, while removing all other fields like `slug`, `createdAt`, `updatedAt`, `layout`, etc.

### Final Refined Pattern

**Search Pattern:**

```regex
^\n(title: [^\n]*)\n(?:(?!excerpt:).*\n)*(excerpt: >-(?:\n  [^\n]*)*)\n(?:(?!metadata:)(?!).*\n)*(?:(metadata:\n  description: >-(?:\n    [^\n]*)*)\n)?(?:(?!).*\n)*
```

**Replace Pattern:**

```yaml

$1
$2
$3

```

### Pattern Breakdown

1. **`^\n`** - Matches the opening `---` separator line
2. **`(title: [^\n]*)`** - Captures the entire title line in capture group 1
   - `title:` matches the literal text
   - `[^\n]*` matches any characters except newline (the title content)
3. **`(?:(?!excerpt:).*\n)*`** - Skips lines between title and excerpt
   - `(?!excerpt:)` negative lookahead ensures we stop at "excerpt:"
   - `.*\n` matches complete lines
4. **`(excerpt: >-(?:\n  [^\n]*)*)`** - Captures the multiline excerpt in capture group 2
   - `excerpt: >-` matches the YAML multiline indicator
   - `(?:\n  [^\n]*)*` matches indented lines (2 spaces)
5. **`(?:(?!metadata:)(?!).*\n)*`** - Skips lines until metadata or end
   - Stops at either "metadata:" or the closing `---`
6. **`(?:(metadata:\n  description: >-(?:\n    [^\n]*)*)\n)?`** - Optionally captures metadata
   - The entire metadata block is optional with `(?:...)?`
   - Captures in group 3 when present
   - Handles 4-space indentation for description content
7. **`(?:(?!).*\n)*`** - Matches remaining lines until closing separator

### Example Transformations

**Input with metadata:**

```yaml

title: Uploading model artifacts
slug: uploading-model-artifacts
excerpt: >-
  This document provides instructions on how to upload a model artifact into
  Fiddler by creating the model and updating the artifact.
metadata:
  description: >-
    This document provides instructions on how to upload a model artifact into
    Fiddler by creating the model and updating the artifact.
  image: []
  robots: index
createdAt: Fri Apr 05 2024 12:04:04 GMT+0000 (Coordinated Universal Time)
updatedAt: Fri Apr 19 2024 13:25:53 GMT+0000 (Coordinated Universal Time)

```

**Output:**

```yaml

title: Uploading model artifacts
excerpt: >-
  This document provides instructions on how to upload a model artifact into
  Fiddler by creating the model and updating the artifact.
metadata:
  description: >-
    This document provides instructions on how to upload a model artifact into
    Fiddler by creating the model and updating the artifact.

```

**Input without metadata:**

```yaml

title: Publishing production data
slug: publishing-production-data
excerpt: >-
  Navigate our client guide to publishing production data.
hidden: false

```

**Output:**

```yaml

title: Publishing production data
excerpt: >-
  Navigate our client guide to publishing production data.

```

### Key Features

- Handles both cases: with and without metadata/description
- Preserves multiline YAML formatting with proper indentation
- Uses negative lookaheads to properly identify section boundaries
- Maintains the YAML document separators (`---`)

---

## 2. GitBook Asset Image Removal

### Purpose

Remove markdown image links that reference GitBook assets folder, typically used for screenshots and diagrams that aren't needed in the corpus.

### Final Refined Pattern

**Search Pattern:**

```regex
!\[.*?\]\((?:\.\.\/)*\.gitbook\/assets\/[^)]+\)
```

**Replace Pattern:** (empty - to completely remove)

### Pattern Breakdown

1. **`!\[.*?\]`** - Matches the markdown image syntax
   - `!` identifies this as an image (not a regular link)
   - `\[` and `\]` are escaped square brackets
   - `.*?` matches any alt text (non-greedy)
2. **`\(`** - Escaped opening parenthesis for the URL
3. **`(?:\.\.\/)*`** - Matches any number of parent directory references
   - `\.\.\/` matches "../" (dots and slash are escaped)
   - `*` allows zero or more occurrences
   - `(?:...)` makes it a non-capturing group
4. **`\.gitbook\/assets\/`** - The specific GitBook assets path
   - Dots are escaped to match literal periods
5. **`[^)]+`** - Matches the filename
   - `[^)]` matches any character except closing parenthesis
   - `+` requires at least one character
6. **`\)`** - Escaped closing parenthesis

### Example Matches

- `![](../../.gitbook/assets/2b19cf0-Screen_Shot_2023-12-19_at_2.31.43_PM.png)`
- `![Screenshot](.gitbook/assets/dashboard.png)`
- `![](../../../.gitbook/assets/model-upload-flow.jpg)`

### Variations and Edge Cases

The pattern handles:

- Empty alt text or alt text with content
- Multiple levels of parent directory navigation
- Any filename format within the assets folder
- Special characters in filenames (underscores, hyphens, etc.)

---

## 3. GitBook Include Statement Removal

### Purpose

Remove Liquid template include statements that reference GitBook includes folder, typically used for shared content blocks like headers and footers.

### Final Refined Pattern (VS Code Compatible)

**Search Pattern:**

```regex
{%.*\.gitbook\/includes\/.*%}
```

**Replace Pattern:** (empty - to completely remove)

### Alternative Patterns (For Different Regex Engines)

**More Specific Pattern (if VS Code supports):**

```regex
{%[ ]*include[ ]*"(?:\.\.\/)*\.gitbook\/includes\/[^"]*"[ ]*%}
```

**Original Pattern (may cause issues in some editors):**

```regex
{%\s*include\s*"(?:\.\.\/)*\.gitbook\/includes\/[^"]+"\s*%}
```

### Pattern Breakdown (Simplified Version)

1. **`{%`** - Opening Liquid template markers
2. **`.*`** - Any characters (includes "include", spaces, quotes)
3. **`\.gitbook\/includes\/`** - The specific GitBook includes path
4. **`.*`** - Any characters until the end
5. **`%}`** - Closing template markers

### Pattern Breakdown (Detailed Version)

1. **`{%`** - Opening Liquid template markers
2. **`[ ]*`** - Zero or more spaces
   - Using explicit space character class instead of `\s` for compatibility
3. **`include`** - The literal word "include"
4. **`[ ]*`** - More optional spaces
5. **`"`** - Opening quote for the file path
6. **`(?:\.\.\/)*`** - Zero or more parent directory references
7. **`\.gitbook\/includes\/`** - The GitBook includes path
8. **`[^"]*`** - Any characters except quotes (the filename)
9. **`"`** - Closing quote
10. **`[ ]*`** - Optional trailing spaces
11. **`%}`** - Closing template markers

### Example Matches

- `{% include "../.gitbook/includes/main-doc-dev-footer.md" %}`
- `{%include ".gitbook/includes/header.md"%}`
- `{% include "../../../.gitbook/includes/shared/navigation.html" %}`

### VS Code Compatibility Notes

The simplified pattern `{%.*\.gitbook\/includes\/.*%}` is recommended for VS Code because:

- It avoids the "lone quantifier brackets" error
- It's more forgiving of syntax variations
- It's easier to understand and maintain

---

## 4. Usage Instructions

### In VS Code

1. **Open Search and Replace:**
   - Press `Ctrl+Shift+F` (Windows/Linux) or `Cmd+Shift+F` (Mac)
   - Or use Find → Replace in Files from the menu

2. **Enable Regex Mode:**
   - Click the `.*` button in the search box
   - Or press `Alt+R` to toggle regex mode

3. **Enter Patterns:**
   - Paste the search pattern in the "Search" field
   - Paste the replace pattern in the "Replace" field (or leave empty for deletion)

4. **Configure Scope:**
   - Use "files to include" to target specific file types (e.g., `*.md`)
   - Use "files to exclude" to skip certain directories

5. **Preview and Apply:**
   - Click "Replace All" to apply globally
   - Or use "Replace" to review each match individually

### Best Practices

1. **Test First:**
   - Always test patterns on a sample file first
   - Use version control to track changes
   - Create backups before bulk operations

2. **Order of Operations:**
   - Clean metadata first (most complex pattern)
   - Then remove images and includes (simpler patterns)

3. **Preserve Spacing:**
   - To maintain line spacing when removing content, replace with `\n` instead of empty string

4. **File Selection:**
   - Use glob patterns to target specific directories
   - Example: `docs/**/*.md` for all markdown files in docs folder

---

## 5. Pattern Components Reference

### Common Regex Elements Used

| Element | Meaning | Example Usage |
|---------|---------|---------------|
| `^` | Start of line | `^\n` |
| `*` | Zero or more of preceding | `[ ]*` |
| `+` | One or more of preceding | `[^)]+` |
| `?` | Zero or one (optional) | `(?:...)?` |
| `.*` | Any characters | `.*` |
| `.*?` | Any characters (non-greedy) | `\[.*?\]` |
| `[^x]` | Any character except x | `[^\n]*` |
| `(?:...)` | Non-capturing group | `(?:\.\.\/)*` |
| `(?!...)` | Negative lookahead | `(?!excerpt:)` |
| `\` | Escape special character | `\.` for literal dot |
| `(...)` | Capturing group | `(title: [^\n]*)` |
| `$1, $2, $3` | Backreferences in replacement | `$1\n$2\n$3` |

### YAML-Specific Patterns

| Pattern | Matches | Purpose |
|---------|---------|---------|
| `>-` | YAML multiline indicator | Preserves line breaks, strips final newline |
| `\n  ` | Two-space indentation | YAML list items or multiline content |
| `\n    ` | Four-space indentation | Nested YAML content |

### Markdown-Specific Patterns

| Pattern | Matches | Purpose |
|---------|---------|---------|
| `!\[...\]` | Image alt text | Markdown image syntax |
| `(...)` | URL in parentheses | Link/image URL |
| `{%...%}` | Liquid template tags | Template processing |

---

## Troubleshooting

### Common Issues and Solutions

1. **"Lone quantifier brackets" error:**
   - Replace `\s` with `[ ]` for spaces
   - Use simplified patterns when possible

2. **Pattern not matching:**
   - Check for variations in spacing/indentation
   - Verify special characters are properly escaped
   - Test with simpler patterns first

3. **Capturing wrong content:**
   - Use negative lookaheads to stop at boundaries
   - Make quantifiers non-greedy with `?`
   - Test capture groups individually

4. **Performance issues:**
   - Use more specific patterns to reduce backtracking
   - Process files in smaller batches
   - Consider using command-line tools for very large operations

---

## Additional Resources

### Testing Regex Patterns

- Use VS Code's search preview to see matches before replacing
- Test patterns on regex101.com (select PCRE2 flavor)
- Keep sample files with various edge cases for testing

### Alternative Tools

For large-scale operations, consider:

- `sed` command-line tool for Unix/Linux
- PowerShell for Windows
- Python scripts with `re` module for complex transformations

### Pattern Variations

The patterns in this guide can be adapted for:

- Different metadata structures
- Other asset management systems
- Various template engines (Jinja2, Handlebars, etc.)

---

## Summary

This reference guide provides battle-tested regex patterns for cleaning markdown files, specifically:

1. **YAML Metadata Cleaning** - Preserves only essential fields while maintaining proper formatting
2. **GitBook Asset Removal** - Cleans up image references to external assets
3. **GitBook Include Removal** - Removes template include statements

Each pattern has been refined through iterative testing to handle edge cases and maintain compatibility with VS Code's regex engine. The patterns can be used individually or combined in a cleaning workflow to prepare markdown content for various purposes such as documentation systems, static site generators, or content management systems.
