import streamlit as st
import base64
import zipfile
import io
import os
import webbrowser
from streamlit.components.v1 import html

# Role & Concept
st.set_page_config(page_title="QuickSite Intake Engine", layout="wide")

# Initialize Session State
if 'site_generated' not in st.session_state:
    st.session_state.site_generated = False
if 'final_html' not in st.session_state:
    st.session_state.final_html = ""
if 'business_name' not in st.session_state:
    st.session_state.business_name = "Business"

st.markdown("""
# ✧ QuickSite Intake Engine 
### Professional Website Architect & Automation Dashboard
Build your finalized 70k-tier business landing page in seconds.
""")

def get_base64_image(file):
    if file is not None:
        return base64.b64encode(file.getvalue()).decode()
    return ""

def open_preview_os():
    preview_filename = "preview_site.html"
    abs_path = os.path.abspath(preview_filename)
    # Using raw path sometimes works better than file:/// for local OS browsers
    webbrowser.open(f"file:///{abs_path}")

# Sidebar for branding
st.sidebar.header("1. BRANDING")
b_name = st.sidebar.text_input("Business Name", "AURELIAN STUDIO")
logo_file = st.sidebar.file_uploader("Upload Logo", type=['png', 'jpg', 'jpeg'])

# Main Form
with st.form("intake_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("2. HERO SECTION")
        slogan = st.text_input("Slogan (4-5 words)", "Elevating the Standard of Excellence")
        hero_desc = st.text_area("Hero Description", "A sanctuary of precision and creativity designed for the discerning client.")
        hero_image = st.file_uploader("Upload Hero Image", type=['png', 'jpg', 'jpeg'])
        
        st.header("3. ABOUT & TRUST")
        about_text = st.text_area("About Paragraph", "At Aurelian Studio, we believe that luxury is not loud; it is felt in the spaces between lines and the harmony of materials.")
        p1 = st.text_input("Trust Pillar 1", "Precision-driven design philosophy")
        p2 = st.text_input("Trust Pillar 2", "Sustainably sourced noble materials")
        p3 = st.text_input("Trust Pillar 3", "A private, white-glove experience")

    with col2:
        st.header("4. SERVICES")
        s1_name = st.text_input("Service 1 Name", "Architectural Sculpting")
        s1_desc = st.text_area("Service 1 Desc", "Transforming raw space into living art through meticulous structural design.")
        
        s2_name = st.text_input("Service 2 Name", "Interior Curation")
        s2_desc = st.text_area("Service 2 Desc", "Selection of noble materials and bespoke furniture.")
        
        s3_name = st.text_input("Service 3 Name", "Landscape Integration")
        s3_desc = st.text_area("Service 3 Desc", "Bridging the gap between the built environment and nature.")

        st.header("5. CONTACT & SOCIALS")
        phone = st.text_input("Phone", "+1 (555) 782-9104")
        email = st.text_input("Email", "concierge@aurelian.studio")
        address = st.text_input("Address", "728 Heritage Boulevard, Mayfair, London")
        hours = st.text_input("Hours", "Mon — Fri: 09:00 - 18:00")
        
        st.subheader("Social Links")
        ig_link = st.text_input("Instagram URL", "#")
        li_link = st.text_input("LinkedIn URL", "#")
        yt_link = st.text_input("YouTube URL", "#")
        wa_number = st.text_input("WhatsApp Number (Digits Only)", "15557829104")

    st.header("6. PORTFOLIO")
    portfolio_images = st.file_uploader("Upload 6 Portfolio Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

    submit_button = st.form_submit_button("Generate Site")

if submit_button:
    # 1. READ TEMPLATES
    try:
        with open("template/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        with open("template/style.css", "r", encoding="utf-8") as f:
            css_content = f.read()
        with open("template/script.js", "r", encoding="utf-8") as f:
            js_content = f.read()
    except Exception as e:
        st.error(f"Error reading templates: {e}")
        st.stop()

    # 2. IMAGE CONVERSION
    logo_b64 = get_base64_image(logo_file)
    hero_b64 = get_base64_image(hero_image)
    port_b64s = [get_base64_image(img) for img in portfolio_images] if portfolio_images else []
    while len(port_b64s) < 6:
        port_b64s.append("")

    # 3. REPLACEMENTS
    slogan_words = slogan.split()
    slogan_injected = f"<span>{slogan_words[0]}</span> {' '.join(slogan_words[1:])}" if slogan_words else slogan

    replacements = {
        "{{business_name}}": b_name,
        "{{slogan}}": slogan_injected,
        "{{hero_desc}}": hero_desc,
        "{{about_text}}": about_text,
        "{{p1}}": p1, "{{p2}}": p2, "{{p3}}": p3,
        "{{s1_name}}": s1_name, "{{s1_desc}}": s1_desc,
        "{{s2_name}}": s2_name, "{{s2_desc}}": s2_desc,
        "{{s3_name}}": s3_name, "{{s3_desc}}": s3_desc,
        "{{phone}}": phone, "{{email}}": email,
        "{{address}}": address, "{{hours}}": hours,
        "{{port1}}": "", "{{port2}}": "", "{{port3}}": "",
        "{{port4}}": "", "{{port5}}": "", "{{port6}}": "",
        "{{meta_description}}": f"Bespoke landing page for {b_name}",
    }

    if logo_b64:
        logo_tag = f'<img src="data:image/png;base64,{logo_b64}" style="height:30px;">'
        html_content = html_content.replace('{{logo}}✧', logo_tag)
    else:
        html_content = html_content.replace('{{logo}}', '')

    if hero_b64:
        html_content = html_content.replace('hero.png', f'data:image/png;base64,{hero_b64}')

    portfolio_sources = [
        "portfolio_detail.png",
        "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1600566753190-17f0bcd2a6c4?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1600585154526-990dcea4db0d?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1600573472591-ee6b68d14c68?auto=format&fit=crop&q=80&w=800"
    ]
    for i, src in enumerate(portfolio_sources):
        if i < len(port_b64s) and port_b64s[i]:
            html_content = html_content.replace(src, f'data:image/png;base64,{port_b64s[i]}')

    html_content = html_content.replace('href="#"', f'href="{ig_link}"', 1)
    html_content = html_content.replace('href="#"', f'href="{li_link}"', 1)
    html_content = html_content.replace('href="#"', f'href="{yt_link}"', 1)
    html_content = html_content.replace('wa.me/15557829104', f'wa.me/{wa_number}')

    for key, value in replacements.items():
        html_content = html_content.replace(key, value)

    # Compile Full HTML (for preview and zip)
    preview_full = html_content.replace('<link rel="stylesheet" href="style.css">', f'<style>{css_content}</style>')
    preview_full = preview_full.replace('<script src="script.js"></script>', f'<script>{js_content}</script>')

    # Store in session state
    st.session_state.final_html = preview_full
    st.session_state.index_html = html_content # For zip download
    st.session_state.style_css = css_content
    st.session_state.script_js = js_content
    st.session_state.business_name = b_name
    st.session_state.site_generated = True

# Display Generated Results
if st.session_state.site_generated:
    st.markdown("---")
    st.success("✨ Website Generated Successfully!")
    
    # Write to file immediately so Launch button always has the latest
    preview_filename = "preview_site.html"
    with open(preview_filename, "w", encoding="utf-8") as f:
        f.write(st.session_state.final_html)

    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🚀 Launch Live Preview (New Tab)"):
            abs_path = os.path.abspath(preview_filename)
            open_preview_os()
            st.info("The preview should now open in your default browser.")
            # Fallback direct link
            clean_path = abs_path.replace('\\', '/')
            st.code(f"If it didn't open, copy and paste this in your browser:\nfile:///{clean_path}")

    with col_btn2:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "x") as zip_file:
            zip_file.writestr("index.html", st.session_state.index_html)
            zip_file.writestr("style.css", st.session_state.style_css)
            zip_file.writestr("script.js", st.session_state.script_js)
        
        st.download_button(
            label="📦 Download Final Website (.zip)",
            data=buf.getvalue(),
            file_name=f"{st.session_state.business_name.lower().replace(' ', '_')}_website.zip",
            mime="application/zip"
        )

    st.subheader("In-App View")
    html(st.session_state.final_html, height=800, scrolling=True)
