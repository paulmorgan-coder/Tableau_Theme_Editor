import streamlit as st
import json
import pandas as pd
# Tableau Theme Editor 
# Author : Paul Morgan (paul.morgan@salesforce.com)
# Requiements - Streamlit and Python 
# run as "streamlit run tabthemeeditor.py"

# --- CONFIGURATION ---
st.set_page_config(
    page_title="The Unofficial Tableau Theme Editor",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONSTANTS ---
TABLEAU_VERSION = "1.0.0"

# Comprehensive font list (Tableau built-in + Google Fonts now supported)
TABLEAU_FONTS = [
    "Tableau Light", "Tableau Book", "Tableau Medium", "Tableau Regular",
    "Tableau Semibold", "Tableau Bold",
    "Arial", "Courier New", "Georgia", "Times New Roman", "Trebuchet MS", "Verdana",
    "Lato", "Montserrat", "Noto Sans", "Open Sans", "Oswald", "Poppins", "Raleway",
    "Roboto", "Source Sans Pro", "Work Sans", "Inter", "Nunito", "PT Sans"
]

BASE_THEMES = {
    "smooth": "Tableau Desktop 10.x and newer",
    "clean": "Tableau Desktop 8.0.x – 9.3.x",
    "modern": "Tableau Desktop 3.5 – 7.0",
    "classic": "Tableau Desktop 1.0 – 3.2"
}

# Complete style elements from Tableau 2025.1 documentation
STYLE_ELEMENTS = {
    "all": {
        "name": "All Fonts",
        "description": "Formats all fonts across the entire workbook",
        "attributes": ["font-color", "font-family"],
        "category": "Global"
    },
    "worksheet": {
        "name": "Worksheet Default",
        "description": "Formats the worksheet default font",
        "attributes": ["font-color", "font-family", "font-size"],
        "category": "Worksheet"
    },
    "worksheet-title": {
        "name": "Worksheet Title",
        "description": "Formats the worksheet title font",
        "attributes": ["font-color", "font-family", "font-size"],
        "category": "Worksheet"
    },
    "tooltip": {
        "name": "Tooltip",
        "description": "Formats the tooltip font",
        "attributes": ["font-color", "font-family", "font-size"],
        "category": "Worksheet"
    },
    "dashboard-title": {
        "name": "Dashboard Title",
        "description": "Formats the dashboard title",
        "attributes": ["font-color", "font-family", "font-size", "font-weight"],
        "category": "Dashboard"
    },
    "story-title": {
        "name": "Story Title",
        "description": "Formats the story title font",
        "attributes": ["font-color", "font-family", "font-size"],
        "category": "Story"
    },
    "header": {
        "name": "Header",
        "description": "Formats the header font",
        "attributes": ["font-color", "font-family"],
        "category": "Worksheet"
    },
    "legend": {
        "name": "Legend Body",
        "description": "Formats the legend body font and background color",
        "attributes": ["font-color", "font-family", "font-size", "background-color"],
        "category": "Controls"
    },
    "legend-title": {
        "name": "Legend Title",
        "description": "Formats the legend title font",
        "attributes": ["font-color", "font-family", "font-size"],
        "category": "Controls"
    },
    "filter": {
        "name": "Filter Body",
        "description": "Formats the filter body font and background color",
        "attributes": ["font-color", "font-family", "font-size", "background-color"],
        "category": "Controls"
    },
    "filter-title": {
        "name": "Filter Title",
        "description": "Formats the filter title font",
        "attributes": ["font-color", "font-family", "font-size"],
        "category": "Controls"
    },
    "parameter-ctrl": {
        "name": "Parameter Control Body",
        "description": "Formats the parameter body font and background color",
        "attributes": ["font-color", "font-family", "font-size", "background-color"],
        "category": "Controls"
    },
    "parameter-ctrl-title": {
        "name": "Parameter Control Title",
        "description": "Formats the parameter control title font",
        "attributes": ["font-color", "font-family", "font-size"],
        "category": "Controls"
    },
    "highlighter": {
        "name": "Highlighter Body",
        "description": "Formats the highlighter body font and background color",
        "attributes": ["font-color", "font-family", "font-size", "background-color"],
        "category": "Controls"
    },
    "highlighter-title": {
        "name": "Highlighter Title",
        "description": "Formats the highlighter control title font",
        "attributes": ["font-color", "font-family", "font-size"],
        "category": "Controls"
    },
    "page-ctrl-title": {
        "name": "Page Card Title",
        "description": "Formats the page card title font",
        "attributes": ["font-color", "font-family"],
        "category": "Controls"
    },
    "gridline": {
        "name": "Grid Lines",
        "description": "Formats the gridlines on a view",
        "attributes": ["line-visibility", "line-pattern", "line-width", "line-color"],
        "category": "View"
    },
    "zeroline": {
        "name": "Zero Line",
        "description": "Formats the zeroline on a view",
        "attributes": ["line-visibility", "line-pattern", "line-width", "line-color"],
        "category": "View"
    },
    "mark": {
        "name": "Mark Color",
        "description": "Formats the mark color on a view",
        "attributes": ["mark-color"],
        "category": "View"
    },
    "view": {
        "name": "View Background",
        "description": "Formats the background color on a view",
        "attributes": ["background-color"],
        "category": "View"
    }
}

# Preset color palettes for quick theming
COLOR_PALETTES = {
    "Corporate Blue": {
        "primary": "#003B5C",
        "secondary": "#0072CE",
        "accent": "#00A3E0",
        "background": "#F5F7FA"
    },
    "Modern Purple": {
        "primary": "#6B46C1",
        "secondary": "#9F7AEA",
        "accent": "#D6BCFA",
        "background": "#F7FAFC"
    },
    "Financial Green": {
        "primary": "#0F4C3A",
        "secondary": "#16A085",
        "accent": "#1ABC9C",
        "background": "#E8F5F1"
    },
    "Elegant Dark": {
        "primary": "#1A202C",
        "secondary": "#2D3748",
        "accent": "#4A5568",
        "background": "#EDF2F7"
    },
    "Warm Autumn": {
        "primary": "#C05621",
        "secondary": "#DD6B20",
        "accent": "#ED8936",
        "background": "#FFFAF0"
    }
}

# --- HELPER FUNCTIONS ---

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    """Convert RGB to hex string"""
    return '#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))

def cmyk_to_hex(c, m, y, k):
    """Convert CMYK (0-100) to hex string"""
    c_val, m_val, y_val, k_val = c/100, m/100, y/100, k/100
    r = round(255 * (1 - c_val) * (1 - k_val))
    g = round(255 * (1 - m_val) * (1 - k_val))
    b = round(255 * (1 - y_val) * (1 - k_val))
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def validate_hex(color):
    """Validate and fix hex color codes"""
    if not color:
        return "#000000"
    color = color.strip()
    if not color.startswith('#'):
        color = '#' + color
    if len(color) == 7:
        return color
    elif len(color) == 9:  # With transparency
        return color
    return "#000000"

def create_default_theme():
    """Create a default theme template"""
    return {
        "version": TABLEAU_VERSION,
        "base-theme": "smooth",
        "styles": {
            "all": {
                "font-family": "Tableau Regular",
                "font-color": "#000000"
            },
            "worksheet": {
                "font-family": "Tableau Regular",
                "font-color": "#000000",
                "font-size": 10
            }
        }
    }

def validate_theme(data):
    """Comprehensive theme validation"""
    errors = []
    warnings = []
    
    if not isinstance(data, dict):
        errors.append("Theme file must be a JSON object")
        return errors, warnings
    
    # Check required fields
    if "version" not in data:
        errors.append("Missing required 'version' field")
    elif data["version"] != TABLEAU_VERSION:
        warnings.append(f"Version {data['version']} may not match Tableau 2025.1 (expected {TABLEAU_VERSION})")
    
    if "styles" not in data:
        errors.append("Missing required 'styles' object")
        return errors, warnings
    
    # Validate base-theme
    base_theme = data.get("base-theme", "smooth")
    if base_theme not in BASE_THEMES:
        warnings.append(f"Unknown base theme '{base_theme}'. Valid options: {', '.join(BASE_THEMES.keys())}")
    
    # Validate style elements
    styles = data.get("styles", {})
    for element, properties in styles.items():
        if element not in STYLE_ELEMENTS:
            warnings.append(f"Unknown style element '{element}' - it may not be supported")
        
        if not isinstance(properties, dict):
            errors.append(f"Style element '{element}' must be an object")
            continue
        
        # Validate attributes
        for attr, value in properties.items():
            if "color" in attr:
                if not isinstance(value, str) or not value.startswith("#"):
                    errors.append(f"Color attribute '{attr}' in '{element}' must be a hex color code (e.g., #FF0000)")
            elif "font-size" in attr or "line-width" in attr:
                if not isinstance(value, int) or value < 1 or value > 99:
                    errors.append(f"Size attribute '{attr}' in '{element}' must be an integer between 1-99")
            elif "font-family" in attr:
                if not isinstance(value, str) or len(value) > 50:
                    errors.append(f"Font family '{attr}' in '{element}' must be a string (max 50 characters)")
    
    return errors, warnings

def apply_palette(theme_data, palette_colors):
    """Apply a color palette to the theme"""
    if "styles" not in theme_data:
        theme_data["styles"] = {}
    
    # Apply primary to titles
    for element in ["worksheet-title", "dashboard-title", "story-title"]:
        if element not in theme_data["styles"]:
            theme_data["styles"][element] = {}
        theme_data["styles"][element]["font-color"] = palette_colors["primary"]
    
    # Apply secondary to controls
    for element in ["legend-title", "filter-title", "parameter-ctrl-title"]:
        if element not in theme_data["styles"]:
            theme_data["styles"][element] = {}
        theme_data["styles"][element]["font-color"] = palette_colors["secondary"]
    
    # Apply accent to marks
    if "mark" not in theme_data["styles"]:
        theme_data["styles"]["mark"] = {}
    theme_data["styles"]["mark"]["mark-color"] = palette_colors["accent"]
    
    # Apply background
    if "view" not in theme_data["styles"]:
        theme_data["styles"]["view"] = {}
    theme_data["styles"]["view"]["background-color"] = palette_colors["background"]
    
    return theme_data

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .element-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN APP ---

def main():
    """Main application entry point"""
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎨 Tableau Theme Editor</h1>
        <p style='font-size: 1.1rem; margin-bottom: 0;'>
            Theme builder for Tableau Classic 2025.1+ | Create, edit, and validate custom themes with live preview
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "theme_data" not in st.session_state:
        st.session_state.theme_data = None
    if "history" not in st.session_state:
        st.session_state.history = []
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Theme Management")
        
        # File operations
        st.subheader("📁 File Operations")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🆕 New", use_container_width=True):
                st.session_state.theme_data = create_default_theme()
                st.rerun()
        
        with col2:
            uploaded_file = st.file_uploader("📤 Upload", type=["json"], label_visibility="collapsed")
            if uploaded_file:
                try:
                    st.session_state.theme_data = json.load(uploaded_file)
                    st.success("✅ Loaded!")
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON - please check your local file.")
        
        if st.session_state.theme_data:
            st.divider()
            
            # Global settings
            st.subheader("🌍 Global Settings")
            
            data = st.session_state.theme_data
            
            # Version (read-only)
            st.text_input("Version", value=data.get("version", TABLEAU_VERSION), disabled=True)
            
            # Base theme
            current_base = data.get("base-theme", "smooth")
            base_options = list(BASE_THEMES.keys())
            base_idx = base_options.index(current_base) if current_base in base_options else 0
            new_base = st.selectbox(
                "Base Theme",
                base_options,
                index=base_idx,
                format_func=lambda x: f"{x.title()} - {BASE_THEMES[x]}"
            )
            data["base-theme"] = new_base
            
            st.divider()
            
            # Quick palette application
            st.subheader("🎨 Quick Color Palettes")
            selected_palette = st.selectbox(
                "Apply Palette",
                ["None"] + list(COLOR_PALETTES.keys())
            )
            
            if selected_palette != "None":
                if st.button("Apply Palette", use_container_width=True):
                    st.session_state.theme_data = apply_palette(
                        st.session_state.theme_data,
                        COLOR_PALETTES[selected_palette]
                    )
                    st.success(f"✅ Applied {selected_palette}")
                    st.rerun()
            
            st.divider()
            
            # Validation
            st.subheader("✅ Validation")
            errors, warnings = validate_theme(data)
            
            if errors:
                st.error(f"❌ {len(errors)} Error(s)")
                with st.expander("View Errors"):
                    for err in errors:
                        st.write(f"• {err}")
            elif warnings:
                st.warning(f"⚠️ {len(warnings)} Warning(s)")
                with st.expander("View Warnings"):
                    for warn in warnings:
                        st.write(f"• {warn}")
            else:
                st.success("✅ Theme Valid")
            
            st.divider()
            
            # Export
            st.subheader("💾 Export")
            
            theme_name = st.text_input("Theme Name", "custom_theme")
            json_output = json.dumps(data, indent=2)
            
            st.download_button(
                label="📥 Download JSON",
                data=json_output,
                file_name=f"{theme_name}.json",
                mime="application/json",
                use_container_width=True
            )
            
            # File size check
            file_size = len(json_output.encode('utf-8'))
            if file_size > 15000:
                st.error(f"⚠️ File too large: {file_size} bytes (max: 15,000)")
            else:
                st.caption(f"File size: {file_size} bytes")
    
    # Main content area
    if st.session_state.theme_data:
        data = st.session_state.theme_data
        
        # Tabs for different editing modes
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Edit by Category",
            "🔍 Edit All Elements",
            "💻 JSON Editor",
            "📚 Documentation"
        ])
        
        with tab1:
            edit_by_category(data)
        
        with tab2:
            edit_all_elements(data)
        
        with tab3:
            json_editor(data)
        
        with tab4:
            show_documentation()
    
    else:
        # Welcome screen with getting started options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; text-align: center; color: white; min-height: 200px;'>
                <h2>🆕 Create New</h2>
                <p>Start with a blank theme template</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Create New Theme", use_container_width=True, type="primary"):
                st.session_state.theme_data = create_default_theme()
                st.rerun()
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 10px; text-align: center; color: white; min-height: 200px;'>
                <h2>📤 Upload Existing</h2>
                <p>Edit an existing theme file</p>
            </div>
            """, unsafe_allow_html=True)
            upload = st.file_uploader("Choose JSON file", type=["json"], key="main_upload")
            if upload:
                try:
                    st.session_state.theme_data = json.load(upload)
                    st.success("✅ Theme loaded!")
                    st.rerun()
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON file")
        
        with col3:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 10px; text-align: center; color: white; min-height: 200px;'>
                <h2>🎨 Use Template</h2>
                <p>Start from a color palette</p>
            </div>
            """, unsafe_allow_html=True)
            template = st.selectbox("Choose palette", list(COLOR_PALETTES.keys()), key="template_select")
            if st.button("Create from Template", use_container_width=True):
                new_theme = create_default_theme()
                st.session_state.theme_data = apply_palette(new_theme, COLOR_PALETTES[template])
                st.success(f"✅ Created theme with {template} palette!")
                st.rerun()
        
        st.markdown("---")
        
        # Feature showcase
        st.subheader("✨ What You Can Do")
        
        feat1, feat2, feat3, feat4 = st.columns(4)
        
        with feat1:
            st.markdown("#### 🎨 Color Tools")
            st.write("• Hex, RGB, CMYK support")
            st.write("• Color palettes")
            st.write("• Live preview")
        
        with feat2:
            st.markdown("#### 📝 20+ Elements")
            st.write("• Worksheets & Dashboards")
            st.write("• Filters & Parameters")
            st.write("• Legends & Tooltips")
        
        with feat3:
            st.markdown("#### ✅ Validation")
            st.write("• Real-time checking")
            st.write("• Error detection")
            st.write("• Size monitoring")
        
        with feat4:
            st.markdown("#### 💾 Export Ready")
            st.write("• Tableau 2025.1+ compatible")
            st.write("• JSON validation")
            st.write("• Download instantly")
        
        st.markdown("---")
        
        # Show example
        with st.expander("📖 Example Theme Structure"):
            example = create_default_theme()
            st.json(example)
        
        # Quick guide
        with st.expander("📚 Quick Start Guide"):
            st.markdown("""
            ### How to Use This Editor
            
            1. **Create or Upload**: Start by creating a new theme or uploading an existing `.json` file
            2. **Edit Elements**: Use the category tabs to customize colors, fonts, and styles
            3. **Validate**: Check the sidebar for real-time validation feedback
            4. **Export**: Download your theme and import it into Tableau Desktop 2025.1+
            
            ### Importing to Tableau
            
            In Tableau Desktop:
            1. Go to **Format** → **Import Custom Theme**
            2. Select your downloaded JSON file
            3. Choose **Override** or **Preserve** existing formatting
            4. Your theme is applied!
            
            ### Tips
            
            - Start with a base theme that's closest to your goal
            - Use color palettes for quick professional looks
            - Keep your file under 15KB for best performance
            - Test on a sample workbook before rolling out widely
            """)

def json_editor(data):
    """Direct JSON editor with syntax highlighting"""
    st.subheader("Direct JSON Editor")
    st.caption("⚠️ Advanced users only - Edit the raw JSON. Invalid JSON will cause errors.")
    
    json_str = json.dumps(data, indent=2)
    
    edited = st.text_area(
        "Theme JSON",
        json_str,
        height=600,
        key="json_editor"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Validate JSON", key="validate_json"):
            try:
                parsed = json.loads(edited)
                st.success("✅ JSON is valid")
                # Overwrite live data
                data.clear()
                data.update(parsed)
                st.session_state.theme_data = data
                st.rerun()
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON: {str(e)}")

    with col2:
        st.caption("Changes here immediately affect the theme. Make sure to download a backup first.")

def edit_by_category(data):
    """Edit theme elements organized by category"""
    st.subheader("Edit Elements by Category")
    
    # Group elements by category
    categories = {}
    for element_key, element_info in STYLE_ELEMENTS.items():
        category = element_info["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append((element_key, element_info))
    
    # Create tabs for each category
    category_tabs = st.tabs(list(categories.keys()))
    
    for tab, (category_name, elements) in zip(category_tabs, categories.items()):
        with tab:
            for element_key, element_info in elements:
                render_element_editor(data, element_key, element_info, context="bycat")

def edit_all_elements(data):
    """Edit all theme elements in a list"""
    st.subheader("Edit All Style Elements")
    
    # Search/filter
    search = st.text_input("🔍 Search elements...", "")
    
    for element_key, element_info in STYLE_ELEMENTS.items():
        if search.lower() in element_key.lower() or search.lower() in element_info["name"].lower():
            render_element_editor(data, element_key, element_info, context="all")


def render_element_editor(data, element_key, element_info, context=""):
    """Render editor for a single style element"""
    prefix = f"{context}_" if context else ""
    styles = data.setdefault("styles", {})
    properties = styles.setdefault(element_key, {})
    
    with st.expander(f"**{element_info['name']}** - {element_info['description']}", expanded=False):
        
        # Check if element is in theme
        is_active = element_key in styles and bool(properties)
        
        col_toggle, col_remove = st.columns([4, 1])
        with col_toggle:
            if not is_active:
                if st.button(
                    f"➕ Add {element_info['name']}",
                    key=f"{prefix}add_{element_key}"
                ):
                    styles[element_key] = {}
                    st.rerun()
                return
        
        with col_remove:
            if st.button(
                "🗑️",
                key=f"{prefix}remove_{element_key}",
                help="Remove this element"
            ):
                del styles[element_key]
                st.rerun()
                return
        
        # Edit attributes
        for attr in element_info["attributes"]:
            render_attribute_editor(properties, element_key, attr, context=context)


def render_attribute_editor(properties, element_key, attr, context=""):
    """Render editor for a specific attribute"""
    prefix = f"{context}_" if context else ""
    
    if "color" in attr:
        # Color editor
        st.markdown(f"**{attr.replace('-', ' ').title()}**")
        col1, col2, col3 = st.columns([1, 1.5, 2])
        
        current_color = validate_hex(properties.get(attr, "#000000"))
        
        with col1:
            picked = st.color_picker(
                "Color",
                current_color,
                key=f"{prefix}picker_{element_key}_{attr}",
            )
            if picked != current_color:
                properties[attr] = picked
        
        with col2:
            mode = st.radio(
                "Mode",
                ["Hex", "RGB", "CMYK"],
                horizontal=True,
                key=f"{prefix}mode_{element_key}_{attr}",
                label_visibility="collapsed"
            )
        
        with col3:
            if mode == "Hex":
                manual = st.text_input(
                    "Hex",
                    current_color,
                    key=f"{prefix}hex_{element_key}_{attr}",
                    max_chars=9
                )
                if manual != current_color:
                    properties[attr] = validate_hex(manual)
            
            elif mode == "RGB":
                rgb = hex_to_rgb(current_color)
                c1, c2, c3 = st.columns(3)
                r = c1.number_input("R", 0, 255, rgb[0], key=f"{prefix}r_{element_key}_{attr}")
                g = c2.number_input("G", 0, 255, rgb[1], key=f"{prefix}g_{element_key}_{attr}")
                b = c3.number_input("B", 0, 255, rgb[2], key=f"{prefix}b_{element_key}_{attr}")
                new_hex = rgb_to_hex(r, g, b)
                if st.button(f"Apply {new_hex}", key=f"{prefix}apply_rgb_{element_key}_{attr}"):
                    properties[attr] = new_hex
            
            elif mode == "CMYK":
                c1, c2, c3, c4 = st.columns(4)
                c = c1.number_input("C%", 0, 100, 0, key=f"{prefix}c_{element_key}_{attr}")
                m = c2.number_input("M%", 0, 100, 0, key=f"{prefix}m_{element_key}_{attr}")
                y = c3.number_input("Y%", 0, 100, 0, key=f"{prefix}y_{element_key}_{attr}")
                k = c4.number_input("K%", 0, 100, 0, key=f"{prefix}k_{element_key}_{attr}")
                calc_hex = cmyk_to_hex(c, m, y, k)
                if st.button(f"Apply {calc_hex}", key=f"{prefix}apply_cmyk_{element_key}_{attr}"):
                    properties[attr] = calc_hex
    
    elif attr == "font-family":
        current = properties.get(attr, TABLEAU_FONTS[0])
        new_font = st.selectbox(
            "Font Family",
            TABLEAU_FONTS,
            index=TABLEAU_FONTS.index(current) if current in TABLEAU_FONTS else 0,
            key=f"{prefix}font_{element_key}_{attr}"
        )
        properties[attr] = new_font
    
    elif attr in ["font-size", "line-width"]:
        current = properties.get(attr, 10 if "size" in attr else 1)
        new_val = st.number_input(
            attr.replace("-", " ").title(),
            min_value=1,
            max_value=99,
            value=int(current),
            key=f"{prefix}size_{element_key}_{attr}"
        )
        properties[attr] = new_val
    
    elif attr == "font-weight":
        current = properties.get(attr, "normal")
        new_weight = st.radio(
            "Font Weight",
            ["normal", "bold"],
            index=0 if current == "normal" else 1,
            horizontal=True,
            key=f"{prefix}weight_{element_key}_{attr}"
        )
        properties[attr] = new_weight
    
    elif attr == "line-visibility":
        current = properties.get(attr, "on")
        new_vis = st.radio(
            "Line Visibility",
            ["on", "off"],
            index=0 if current == "on" else 1,
            horizontal=True,
            key=f"{prefix}vis_{element_key}_{attr}"
        )
        properties[attr] = new_vis
    
    elif attr == "pattern":
        current = properties.get(attr, "none")
        new_pattern = st.selectbox(
            "Pattern",
            ["none", "dotted", "dashed"],
            index=["none", "dotted", "dashed"].index(current) if current in ["none", "dotted", "dashed"] else 0,
            key=f"{prefix}pattern_{element_key}_{attr}"
        )
        properties[attr] = new_pattern

def show_documentation():
    """Show comprehensive documentation"""
    st.subheader("📚 Tableau Custom Themes Documentation")
    
    st.markdown("""
    ### Overview
    
    Custom Themes in Tableau 2025.1+ allow you to quickly apply consistent formatting across your workbooks using JSON files.
    
    ### Key Features
    
    - **20 Style Elements**: Control fonts, colors, and layouts across your entire workbook
    - **Base Themes**: Build on top of existing Tableau themes (smooth, clean, modern, classic)
    - **Export & Import**: Save themes from existing workbooks and apply to others
    - **File Limits**: Max 15KB file size, 256 character file path
    
    ### Supported Style Elements
    """)
    
    # Display all style elements in a table

    
    element_data = []
    for key, info in STYLE_ELEMENTS.items():
        element_data.append({
            "Element": info["name"],
            "Key": key,
            "Category": info["category"],
            "Attributes": ", ".join(info["attributes"])
        })
    
    df = pd.DataFrame(element_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### Best Practices
    
    1. **Start with a Base Theme**: Choose a base theme that's close to your desired look
    2. **Test Incrementally**: Apply your theme to a test workbook before rolling out
    3. **Use Override vs Preserve**: Override replaces all formatting, Preserve keeps manual edits
    4. **Validate Before Export**: Use the validation panel to catch errors
    5. **Keep Files Small**: Stay under 15KB for best performance
    
    ### Color Formats
    
    - **Standard Hex**: `#FF0000` (red)
    - **With Transparency**: `#FF000080` (red with 50% opacity)
    - Transparency is supported for: background-color and line-color attributes
    
    ### Font Guidelines
    
    - Use fonts installed with Tableau or available in your environment
    - Google Fonts are now supported in newer versions
    - Font names are case-sensitive
    - Max 50 characters for font-family values
    
    ### Troubleshooting
    
    **Fonts not displaying?**
    - Verify the font is installed on all machines that will use the theme
    - Check font name spelling and capitalization
    
    **Theme not applying?**
    - Validate JSON syntax at jsonschemavalidator.net
    - Check file size (max 15KB)
    - Ensure version is "1.0.0"
    
    **Some formatting preserved?**
    - Rich text editor formatting always persists
    - Use "Override" option when importing to replace most formatting
    
    ### Resources
    
    - [Official Tableau Documentation](https://help.tableau.com/current/pro/desktop/en-us/formatting_custom_themes.htm)
    - [JSON Schema Validator](https://www.jsonschemavalidator.net)
    - [Tableau Community Forums](https://community.tableau.com)
    """)
    
    # Run the app
if __name__ == "__main__":
    main()