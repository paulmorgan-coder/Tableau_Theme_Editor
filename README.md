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

## How to use the app

1. **Load or create a theme**

   - Start with the default theme provided by the app, **or**
   - Upload an existing Tableau theme file (JSON / TMS) if a file upload widget is available.
   - Once loaded, the theme structure is stored in the app and can be edited visually.

2. **Edit by category**

   - Go to the **“Edit by category”** tab.
   - Work through logical groups such as:
     - Typography
     - Marks and lines
     - Backgrounds and borders
     - Tooltips and panes
   - For each element in a category you can:
     - Add or remove the element from the theme.
     - Adjust colors (Hex / RGB / CMYK).
     - Update font family, size, weight, and line attributes.

3. **Edit all elements**

   - Go to the **“Edit all elements”** tab.
   - Use the search box to filter by:
     - Element key, or  
     - Human-readable name.
   - Quickly scan and tweak multiple elements in one linear view without switching categories.

4. **Use the JSON editor (advanced)**

   - Open the **JSON editor** tab to work with the raw theme definition.
   - Review or modify the full JSON in a large text area.
   - Click **“Validate JSON”** to:
     - Parse your changes, and  
     - Apply them back into the live theme if valid.
   - Recommended: download or save a backup of your theme before making large changes.

5. **View in-app documentation**

   - Open the **Documentation** section (if enabled in the UI).
   - Browse a table of all style elements, including:
     - Element key
     - Category
     - Attributes
     - Description
   - Use this as a reference when deciding which elements to customize.

6. **Download your theme**

   - Once you are happy with the edits:
     - Use the download button(s) to export the theme as JSON or TMS.
   - Save the file locally.
   - Configure Tableau Desktop / Tableau Server / Tableau Cloud to use this theme according to Tableau’s theme configuration docs.



---

## Project structure

If you keep it simple, your repo can look like this:

```text
tabtheme/
  ├─ tabthemeeditor.py        # Main Streamlit app
  ├─ requirements.txt   # Python dependencies
  └─ README.md          # This file
