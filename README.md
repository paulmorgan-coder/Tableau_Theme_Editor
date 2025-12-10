# Tableau Theme Builder (Streamlit)

Interactive Streamlit app for building and editing Tableau theme JSON files.

This app lets you:

- Edit Tableau style elements with a visual UI
- Work with colors in Hex, RGB, and CMYK
- Apply predefined color palettes across your theme
- Inspect and edit the raw JSON directly
- Download your theme as a `.tms` or `.json` file

Perfect for experimenting with Tableau themes without hand-editing JSON in a text editor.

---

## Features

### Visual style editor

- Edit style elements grouped by category (titles, headers, marks, lines, backgrounds, etc.)
- Or edit all style elements in a single list view
- Each element shows:
  - Human readable name
  - Description
  - All supported attributes for that element

### Color controls

For any color attribute, you can:

- Pick a color using a standard color picker
- Switch between:
  - Hex input
  - RGB input
  - CMYK input
- Convert between modes and apply back to the theme

### Typography and line styling

- Font family from a curated list of Tableau friendly fonts
- Font size, weight, and visibility controls
- Line width and visibility
- Optional pattern selection where supported

### JSON editor

- Raw JSON editor with syntax highlighted text area
- Validate JSON and apply it back to the live theme
- Great for advanced users who want full control

### Documentation view

- In-app documentation that:
  - Lists all style elements
  - Shows categories, attributes, and descriptions
- Helpful reference while editing themes

---

## Project structure

If you keep it simple, your repo can look like this:

```text
tabtheme/
  ├─ tabthemeeditor.py        # Main Streamlit app
  ├─ requirements.txt   # Python dependencies
  └─ README.md          # This file
