import os
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import shutil

BASE_DIR = Path(r"C:\Users\estefanozappa\.gemini\antigravity\scratch\carreras-chaco-corrientes")
DIST_DIR = BASE_DIR / "dist"
SITE_DIR = BASE_DIR / "site"
XML_FILE = Path(r"C:\Users\estefanozappa\Downloads\WordPress.2026-10-19.xml")
IMAGES_DIR = DIST_DIR / "assets" / "images"
CSS_DIR = DIST_DIR / "assets" / "css"
JS_DIR = DIST_DIR / "assets" / "js"
VENDOR_DIR = DIST_DIR / "assets" / "vendor" / "leaflet"

# 1. Collect Image Mappings
files = list(IMAGES_DIR.iterdir())
base_map = {}
for f in files:
    m = re.match(r"^(.*?)(?:_\d+)?(\.[^.]+)$", f.name)
    if m:
        prefix = m.group(1).lower()
        base_map[prefix] = f.name
    base_map[f.stem.lower()] = f.name

base_map["gemini_generated_image_r7xxvvr7xxvvr7xx-edited"] = "site_logo.jpg"
base_map["site_logo"] = "site_logo.jpg"

def resolve_image(url):
    clean = url.split("?")[0].strip()
    filename = os.path.basename(clean).lower()
    stem = os.path.splitext(filename)[0]
    
    for f in files:
        if f.name.lower() == filename:
            return f"assets/images/{f.name}"
            
    if stem in base_map:
        return f"assets/images/{base_map[stem]}"
        
    for prefix, target in base_map.items():
        if prefix in stem or stem in prefix:
            return f"assets/images/{target}"
            
    return url

# 2. Load Base CSS from permanent wp_extracted_styles.json
styles_json_file = BASE_DIR / "wp_extracted_styles.json"
wp_block_lib = ""
global_styles = ""
jetpack_styles = ""
theme_css = ""

if styles_json_file.exists():
    styles_data = json.loads(styles_json_file.read_text(encoding="utf-8"))
    wp_block_lib = styles_data.get("wp_block_lib", "")
    global_styles = styles_data.get("global_styles", "")
    jetpack_styles = styles_data.get("jetpack_styles", "")
    theme_css = styles_data.get("theme_css", "")

# 3. Master Responsive & Assembler Styles
additional_css = """
/* === FULL RESPONSIVE OVERRIDES & ASSEMBLER INTEGRATION === */
*, *::before, *::after {
  box-sizing: border-box;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
  width: 100%;
  height: 100%;
}

body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  min-height: 100vh;
  background-color: var(--wp--preset--color--theme-1, #ffffff);
  color: var(--wp--preset--color--theme-4, #1e1e1e);
  font-family: var(--wp--preset--font-family--inter, 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif);
  line-height: 1.65;
  overflow-x: hidden;
}

/* CRUCIAL FIX: Cancel 620px constraint that was locking page to mobile size */
.wp-site-blocks {
  width: 100% !important;
  max-width: 100% !important;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  margin: 0 !important;
  padding: 0 !important;
}

main.wp-site-main {
  flex: 1 0 auto;
  width: 100% !important;
  max-width: 100% !important;
}

.entry-content {
  width: 100%;
}

/* Global Content Widths & Breakpoints */
:root {
  --wp--style--global--content-size: 960px !important;
  --wp--style--global--wide-size: 1400px !important;
}

.alignfull {
  width: 100% !important;
  max-width: 100% !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
}

.alignwide {
  width: 100% !important;
  max-width: var(--wp--style--global--wide-size, 1400px) !important;
  margin-left: auto !important;
  margin-right: auto !important;
  padding-left: clamp(1rem, 4vw, 2.5rem) !important;
  padding-right: clamp(1rem, 4vw, 2.5rem) !important;
  box-sizing: border-box;
}

.aligncenter {
  margin-left: auto !important;
  margin-right: auto !important;
  text-align: center;
}

/* Constrained flow for text reading */
.entry-content > :where(:not(.alignfull):not(.alignwide):not(.wp-block-cover)) {
  max-width: var(--wp--style--global--content-size, 960px);
  margin-left: auto !important;
  margin-right: auto !important;
  padding-left: clamp(1rem, 3vw, 2rem);
  padding-right: clamp(1rem, 3vw, 2rem);
}

/* Page Titles */
.wp-block-post-title {
  font-size: clamp(2rem, 3.5vw, 3rem);
  font-weight: 700;
  line-height: 1.2;
  margin-top: 2.5rem;
  margin-bottom: 1.5rem;
  color: var(--wp--preset--color--theme-4, #1e1e1e);
}

/* HEADER & RESPONSIVE NAVIGATION */
header.wp-block-template-part {
  background: var(--wp--preset--color--theme-1, #ffffff);
  border-bottom: 1px solid var(--wp--preset--color--theme-2, #eeeeee);
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 6px rgba(0,0,0,0.04);
  width: 100%;
}

.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem clamp(1rem, 3vw, 2rem);
  gap: 1.5rem;
  max-width: var(--wp--style--global--wide-size, 1400px);
  margin: 0 auto;
}

.site-logo-link img {
  height: 52px;
  width: auto;
  display: block;
}

.wp-block-navigation {
  display: block;
}

.wp-block-navigation__container {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 0.35rem;
  flex-wrap: wrap;
}

.wp-block-navigation-item {
  position: relative;
}

.wp-block-navigation-item > a {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.55rem 0.9rem;
  color: var(--wp--preset--color--theme-4, #1e1e1e);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.925rem;
  border-radius: 6px;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.wp-block-navigation-item:hover > a,
.wp-block-navigation-item.current-menu-item > a {
  color: #0066cc;
  background-color: var(--wp--preset--color--theme-2, #f1f5f9);
}

.wp-block-navigation-item.has-children > a::after {
  content: "▾";
  font-size: 0.75rem;
  margin-left: 0.2rem;
}

/* Submenu dropdown */
.wp-block-navigation__submenu-container {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background: #ffffff;
  min-width: 320px;
  padding: 0.5rem 0;
  margin: 0;
  list-style: none;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.12);
  z-index: 1050;
}

.wp-block-navigation-item.has-children:hover > .wp-block-navigation__submenu-container,
.wp-block-navigation-item.has-children:focus-within > .wp-block-navigation__submenu-container {
  display: block;
}

.wp-block-navigation__submenu-container .wp-block-navigation-item > a {
  padding: 0.65rem 1.25rem;
  display: block;
  font-size: 0.885rem;
  white-space: normal;
  border-radius: 0;
  color: #334155;
  border-bottom: 1px solid #f8fafc;
}

.wp-block-navigation__submenu-container .wp-block-navigation-item > a:hover {
  background-color: #f1f5f9;
  color: #0066cc;
}

/* Mobile Toggle */
.menu-toggle {
  display: none;
  background: none;
  border: 1px solid #cbd5e1;
  padding: 0.5rem 0.85rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
}

@media (max-width: 900px) {
  .menu-toggle {
    display: block;
  }
  .wp-block-navigation {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: #ffffff;
    border-bottom: 2px solid #e2e8f0;
    padding: 1rem 1.5rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
  }
  .wp-block-navigation.is-open {
    display: block;
  }
  .wp-block-navigation__container {
    flex-direction: column;
    align-items: stretch;
    gap: 0.25rem;
  }
  .wp-block-navigation__submenu-container {
    position: static;
    display: block;
    box-shadow: none;
    border: none;
    padding-left: 1rem;
    background: transparent;
  }
}

/* HERO COVER BLOCK */
.wp-block-cover {
  position: relative;
  width: 100% !important;
  min-height: 75vh;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  overflow: hidden;
  margin: 0 0 3rem 0;
}

.wp-block-cover__image-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100% !important;
  height: 100% !important;
  object-fit: cover;
  z-index: 1;
}

.wp-block-cover__background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  opacity: 0.45;
}

.wp-block-cover__inner-container {
  position: relative;
  z-index: 3;
  width: 100%;
  max-width: var(--wp--style--global--wide-size, 1400px);
  padding: 3rem 1.5rem;
  box-sizing: border-box;
  text-align: center;
}

.wp-block-cover h1 {
  font-size: clamp(2.2rem, 5.5vw, 4.5rem) !important;
  line-height: 1.1;
  text-shadow: 0 3px 12px rgba(0,0,0,0.6);
  background: rgba(0,0,0,0.4);
  padding: 1.75rem 2.5rem;
  backdrop-filter: blur(6px);
  margin: 0 auto;
  max-width: 950px;
  color: #ffffff !important;
  border-radius: 9999px !important;
}

/* COLUMNS RESPONSIVENESS */
.wp-block-columns {
  display: flex;
  box-sizing: border-box;
  gap: var(--wp--preset--spacing--30, 2rem);
  margin-top: 2rem;
  margin-bottom: 2rem;
}

@media (min-width: 782px) {
  .wp-block-columns {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
  }
}

@media (max-width: 781px) {
  .wp-block-columns {
    flex-direction: column !important;
  }
}

.wp-block-column {
  flex: 1 1 0;
  min-width: 0;
}

/* IMAGES & FIGURES */
figure.wp-block-image {
  margin: 2rem auto;
  text-align: center;
}

figure.wp-block-image img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  display: inline-block;
}

/* BUTTONS */
.wp-block-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: center;
  margin: 1.5rem 0;
}

.wp-block-button__link {
  display: inline-block;
  cursor: pointer;
  text-decoration: none;
  font-weight: 500;
  border-radius: 9999px;
  padding: 0.8rem 1.85rem;
  background-color: var(--wp--preset--color--theme-4, #1e1e1e);
  color: var(--wp--preset--color--theme-1, #ffffff) !important;
  transition: transform 0.15s, background-color 0.15s;
}

.wp-block-button__link:hover {
  transform: translateY(-2px);
  background-color: #000000;
}

/* TABS COMPONENT */
.wp-block-tabs {
  margin: 3rem 0;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  background: #ffffff;
}

.wp-block-tab-list {
  display: flex;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  padding: 0.5rem 1rem 0;
  gap: 0.5rem;
  overflow-x: auto;
}

.wp-block-tab-list button[role="tab"] {
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  padding: 0.9rem 2rem;
  font-size: 1.15rem;
  font-family: inherit;
  font-weight: 600;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.wp-block-tab-list button[role="tab"]:hover {
  color: #0f172a;
}

.wp-block-tab-list button[role="tab"][aria-selected="true"],
.wp-block-tab-list button[role="tab"].active {
  color: #0066cc;
  border-bottom-color: #0066cc;
  background: #ffffff;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.wp-block-tab-panel {
  display: none;
  padding: clamp(1.5rem, 3vw, 2.5rem);
  animation: tabFadeIn 0.25s ease-in-out;
}

.wp-block-tab-panel.active {
  display: block;
}

@keyframes tabFadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* SOCIAL ICONS */
.wp-block-social-links {
  display: flex;
  gap: 0.85rem;
  list-style: none;
  padding: 0;
  margin: 2rem 0;
}

.wp-social-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: #f1f5f9;
  color: #334155;
  transition: transform 0.15s, background-color 0.15s;
}

.wp-social-link:hover {
  transform: scale(1.1);
  background: #0066cc;
  color: #ffffff;
}

.wp-social-link a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: inherit;
  text-decoration: none;
}

.wp-social-link svg {
  width: 22px;
  height: 22px;
  fill: currentColor;
}

/* SLIDESHOW COMPONENT */
.wp-block-jetpack-slideshow {
  margin: 2.5rem 0;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.wp-block-jetpack-slideshow_container {
  position: relative;
  overflow: hidden;
}

.wp-block-jetpack-slideshow_swiper-wrapper {
  display: flex;
  margin: 0;
  padding: 0;
  list-style: none;
  transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1);
}

.wp-block-jetpack-slideshow_slide {
  min-width: 100%;
  flex-shrink: 0;
  box-sizing: border-box;
}

.wp-block-jetpack-slideshow_slide figure {
  margin: 0;
}

.wp-block-jetpack-slideshow_slide img {
  width: 100%;
  height: clamp(320px, 45vw, 520px);
  object-fit: cover;
  display: block;
}

.wp-block-jetpack-slideshow_button-prev,
.wp-block-jetpack-slideshow_button-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.65);
  color: #ffffff;
  border: none;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  font-size: 22px;
  text-decoration: none;
  transition: background 0.2s, transform 0.15s;
}

.wp-block-jetpack-slideshow_button-prev:hover,
.wp-block-jetpack-slideshow_button-next:hover {
  background: rgba(0, 0, 0, 0.9);
  transform: translateY(-50%) scale(1.05);
}

.wp-block-jetpack-slideshow_button-prev { left: 16px; }
.wp-block-jetpack-slideshow_button-next { right: 16px; }

.wp-block-jetpack-slideshow_button-prev::after {
  content: "❮";
}

.wp-block-jetpack-slideshow_button-next::after {
  content: "❯";
}

.wp-block-jetpack-slideshow_pagination {
  position: absolute;
  bottom: 16px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 8px;
  z-index: 10;
}

.wp-block-jetpack-slideshow_pagination .dot {
  width: 11px;
  height: 11px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.wp-block-jetpack-slideshow_pagination .dot.active {
  background: #ffffff;
  transform: scale(1.3);
}

/* INTERACTIVE MAP CONTAINER & LEAFLET FIXES */
.map-block-card {
  margin: 2.5rem 0;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 18px rgba(0,0,0,0.06);
  background: #ffffff;
}

.wp-block-jetpack-map {
  width: 100% !important;
  height: 440px !important;
  min-height: 440px;
  background: #e2e8f0;
  position: relative;
  z-index: 5;
}

@media (max-width: 640px) {
  .wp-block-jetpack-map {
    height: 320px !important;
    min-height: 320px;
  }
}

.leaflet-container {
  font-family: inherit !important;
}

.map-location-chips {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  padding: 1rem 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
}

.map-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.45rem 0.95rem;
  border-radius: 9999px;
  background: #ffffff;
  color: #334155;
  font-size: 0.85rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.15s ease;
  border: 1px solid #cbd5e1;
}

.map-chip:hover {
  background: #0066cc;
  color: #ffffff;
  border-color: #0066cc;
  transform: translateY(-1px);
}

.map-chip::before {
  content: "📍";
  font-size: 0.9rem;
}

/* TABLES */
table.wp-block-table, .wp-block-table table {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  font-size: 0.95rem;
}

.wp-block-table th, .wp-block-table td {
  padding: 0.85rem 1rem;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.wp-block-table thead, .wp-block-table tr:first-child td {
  background: #f8fafc;
  font-weight: 600;
}

/* LISTS */
ul.wp-block-list, ol.wp-block-list {
  margin: 1.25rem 0 1.5rem 2rem;
  padding: 0;
}

ul.wp-block-list li, ol.wp-block-list li {
  margin-bottom: 0.45rem;
}

/* FOOTER */
footer.wp-block-template-part {
  background: var(--wp--preset--color--theme-4, #1e1e1e);
  color: var(--wp--preset--color--theme-1, #ffffff);
  padding: 3.5rem 0 2rem;
  margin-top: 4rem;
  width: 100%;
}

footer.wp-block-template-part a {
  color: #38bdf8;
  text-decoration: none;
}

footer.wp-block-template-part a:hover {
  text-decoration: underline;
}

.footer-inner {
  max-width: var(--wp--style--global--wide-size, 1400px);
  margin: 0 auto;
  padding: 0 clamp(1rem, 3vw, 2.5rem);
}
"""

master_css = f"""/* WORDPRESS CORE & ASSEMBLER THEME STYLESHEET */
{global_styles}

{wp_block_lib}

{jetpack_styles}

{theme_css}

{additional_css}
"""

CSS_DIR.mkdir(parents=True, exist_ok=True)
(CSS_DIR / "wordpress-assembler.css").write_text(master_css, encoding="utf-8")
print(f"Generated wordpress-assembler.css ({len(master_css)} bytes)")

# 4. Generate Interactive JavaScript with Robust Leaflet Handling
site_js = """
// Interactive Features for WordPress Static Reproduction
document.addEventListener("DOMContentLoaded", function() {
  
  // 1. Mobile Menu Toggle
  const toggleBtn = document.querySelector(".menu-toggle");
  const navContainer = document.querySelector(".wp-block-navigation");
  if (toggleBtn && navContainer) {
    toggleBtn.addEventListener("click", function() {
      const isOpen = navContainer.classList.toggle("is-open");
      toggleBtn.setAttribute("aria-expanded", isOpen);
    });
  }

  // 2. Leaflet Icon Configuration (Ensure local images are found)
  if (typeof L !== 'undefined') {
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'assets/vendor/leaflet/images/marker-icon-2x.png',
      iconUrl: 'assets/vendor/leaflet/images/marker-icon.png',
      shadowUrl: 'assets/vendor/leaflet/images/marker-shadow.png',
    });
  }

  // 3. Map Initialization Function (Safely initializes when element is visible)
  function initMapInstance(mapEl) {
    if (!mapEl || mapEl._leaflet_map || typeof L === 'undefined') return;
    if (mapEl.offsetWidth === 0 || mapEl.offsetHeight === 0) return; // Wait until visible

    const rawPoints = mapEl.getAttribute("data-points");
    let points = [];
    try {
      if (rawPoints) points = JSON.parse(rawPoints);
    } catch (e) {
      console.warn("Could not parse map data-points", e);
    }

    let centerLat = parseFloat(mapEl.getAttribute("data-center-lat") || "-27.1467617");
    let centerLng = parseFloat(mapEl.getAttribute("data-center-lng") || "-59.59842295");
    let zoom = parseInt(mapEl.getAttribute("data-zoom") || "11", 10);

    // If points exist and center is not explicitly set
    if (points.length > 0 && (!mapEl.hasAttribute("data-center-lat") || isNaN(centerLat))) {
      centerLat = points[0].coordinates.latitude;
      centerLng = points[0].coordinates.longitude;
      zoom = 14;
    }

    // Clear fallback content
    mapEl.innerHTML = "";

    const map = L.map(mapEl, {
      scrollWheelZoom: false
    }).setView([centerLat, centerLng], zoom > 0 ? zoom : 12);
    mapEl._leaflet_map = map;

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    const bounds = L.latLngBounds();
    let validCount = 0;

    points.forEach(p => {
      if (p.coordinates && typeof p.coordinates.latitude === 'number' && typeof p.coordinates.longitude === 'number') {
        const lat = p.coordinates.latitude;
        const lng = p.coordinates.longitude;
        const marker = L.marker([lat, lng]).addTo(map);
        bounds.extend([lat, lng]);
        validCount++;

        const title = p.title || p.placeTitle || "Sede";
        const desc = p.caption || p.placeTitle || "";
        const gmapsUrl = `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`;
        marker.bindPopup(`
          <div style="font-family:inherit;min-width:180px;">
            <strong style="font-size:1.05em;color:#0066cc;">${title}</strong><br>
            <span style="font-size:0.9em;color:#475569;">${desc}</span><br>
            <a href="${gmapsUrl}" target="_blank" rel="noopener" style="display:inline-block;margin-top:6px;font-size:0.85em;color:#2563eb;text-decoration:underline;">Ver en Google Maps ↗</a>
          </div>
        `);
      }
    });

    if (validCount > 1) {
      map.fitBounds(bounds, { padding: [35, 35] });
    } else if (validCount === 1) {
      map.setView([points[0].coordinates.latitude, points[0].coordinates.longitude], 15);
    }
  }

  // 4. Tabs Component (wp-block-tabs)
  document.querySelectorAll(".wp-block-tabs").forEach(tabsBlock => {
    const tabButtons = tabsBlock.querySelectorAll(".wp-block-tab-list button[role='tab']");
    const tabPanels = tabsBlock.querySelectorAll(".wp-block-tab-panel");

    tabButtons.forEach((btn, index) => {
      btn.addEventListener("click", () => {
        tabButtons.forEach(b => {
          b.classList.remove("active");
          b.setAttribute("aria-selected", "false");
        });
        tabPanels.forEach(p => {
          p.classList.remove("active");
          p.style.display = "none";
        });

        btn.classList.add("active");
        btn.setAttribute("aria-selected", "true");
        if (tabPanels[index]) {
          tabPanels[index].classList.add("active");
          tabPanels[index].style.display = "block";
          
          // Initialize or resize map in this tab
          setTimeout(() => {
            const mapEl = tabPanels[index].querySelector(".wp-block-jetpack-map");
            if (mapEl) {
              if (!mapEl._leaflet_map) {
                initMapInstance(mapEl);
              } else {
                mapEl._leaflet_map.invalidateSize();
              }
            }
          }, 150);
        }
      });
    });

    // Activate first tab by default
    if (tabButtons.length > 0 && !tabsBlock.querySelector(".wp-block-tab-list button.active")) {
      tabButtons[0].click();
    }
  });

  // 5. Initialize All Visible Maps & Setup Location Chips
  document.querySelectorAll(".wp-block-jetpack-map").forEach(mapEl => {
    initMapInstance(mapEl);

    // Create location chips below map if not already present
    const rawPoints = mapEl.getAttribute("data-points");
    if (rawPoints && !mapEl.parentElement.querySelector(".map-location-chips")) {
      try {
        const points = JSON.parse(rawPoints);
        if (points.length > 0) {
          const chipsContainer = document.createElement("div");
          chipsContainer.className = "map-location-chips";
          points.forEach(p => {
            const lat = p.coordinates ? p.coordinates.latitude : null;
            const lng = p.coordinates ? p.coordinates.longitude : null;
            const title = p.title || p.placeTitle || "Sede";
            const chip = document.createElement("a");
            chip.className = "map-chip";
            chip.textContent = title;
            if (lat && lng) {
              chip.href = `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`;
              chip.target = "_blank";
              chip.rel = "noopener";
              chip.title = p.placeTitle || title;
            }
            chipsContainer.appendChild(chip);
          });
          mapEl.parentElement.appendChild(chipsContainer);
        }
      } catch (e) {}
    }
  });

  // Resize listener
  window.addEventListener("resize", () => {
    document.querySelectorAll(".wp-block-jetpack-map").forEach(mapEl => {
      if (mapEl._leaflet_map && mapEl.offsetWidth > 0) {
        mapEl._leaflet_map.invalidateSize();
      }
    });
  });

  // 6. Slideshow Component (wp-block-jetpack-slideshow)
  document.querySelectorAll(".wp-block-jetpack-slideshow").forEach(slideshow => {
    const container = slideshow.querySelector(".wp-block-jetpack-slideshow_container") || slideshow;
    const wrapper = slideshow.querySelector(".wp-block-jetpack-slideshow_swiper-wrapper");
    const slides = slideshow.querySelectorAll(".wp-block-jetpack-slideshow_slide");
    if (!wrapper || slides.length === 0) return;

    let currentIndex = 0;
    const totalSlides = slides.length;

    let prevBtn = slideshow.querySelector(".wp-block-jetpack-slideshow_button-prev");
    let nextBtn = slideshow.querySelector(".wp-block-jetpack-slideshow_button-next");
    if (!prevBtn) {
      prevBtn = document.createElement("button");
      prevBtn.className = "wp-block-jetpack-slideshow_button-prev";
      container.appendChild(prevBtn);
    }
    if (!nextBtn) {
      nextBtn = document.createElement("button");
      nextBtn.className = "wp-block-jetpack-slideshow_button-next";
      container.appendChild(nextBtn);
    }

    let pagination = slideshow.querySelector(".wp-block-jetpack-slideshow_pagination");
    if (!pagination) {
      pagination = document.createElement("div");
      pagination.className = "wp-block-jetpack-slideshow_pagination";
      container.appendChild(pagination);
    }
    pagination.innerHTML = "";
    for (let i = 0; i < totalSlides; i++) {
      const dot = document.createElement("button");
      dot.className = "dot" + (i === 0 ? " active" : "");
      dot.setAttribute("aria-label", "Diapositiva " + (i + 1));
      dot.addEventListener("click", () => goToSlide(i));
      pagination.appendChild(dot);
    }

    function goToSlide(index) {
      currentIndex = (index + totalSlides) % totalSlides;
      wrapper.style.transform = `translateX(-${currentIndex * 100}%)`;
      pagination.querySelectorAll(".dot").forEach((d, i) => {
        d.classList.toggle("active", i === currentIndex);
      });
    }

    prevBtn.addEventListener("click", (e) => { e.preventDefault(); goToSlide(currentIndex - 1); });
    nextBtn.addEventListener("click", (e) => { e.preventDefault(); goToSlide(currentIndex + 1); });

    let timer = setInterval(() => goToSlide(currentIndex + 1), 6000);
    slideshow.addEventListener("mouseenter", () => clearInterval(timer));
    slideshow.addEventListener("mouseleave", () => {
      clearInterval(timer);
      timer = setInterval(() => goToSlide(currentIndex + 1), 6000);
    });
  });
});
"""

JS_DIR.mkdir(parents=True, exist_ok=True)
(JS_DIR / "site.js").write_text(site_js, encoding="utf-8")
print(f"Generated site.js ({len(site_js)} bytes)")

# 5. Build All 16 Pages
tree = ET.parse(XML_FILE)
root = tree.getroot()
channel = root.find("channel")
namespaces = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/"
}

pages = []
for item in channel.findall("item"):
    pt = item.find("wp:post_type", namespaces)
    st = item.find("wp:status", namespaces)
    if pt is not None and pt.text in ["page", "post"] and st is not None and st.text == "publish":
        title = item.find("title").text or "Sin título"
        link = item.find("link").text or ""
        content = item.find("content:encoded", namespaces).text or ""
        pages.append({
            "title": title,
            "link": link,
            "content": content,
            "post_type": pt.text
        })

# Map old URLs to local HTML filenames
url_to_local_file = {}
for p in pages:
    orig_link = p["link"].rstrip("/")
    slug = orig_link.split("/")[-1]
    if "acerca-de" in orig_link or slug == "carreraschacocorrientes.wordpress.com" or slug == "":
        local_filename = "index.html"
    else:
        local_filename = f"{slug}.html"
    url_to_local_file[orig_link] = local_filename
    url_to_local_file[orig_link + "/"] = local_filename
    p["filename"] = local_filename

# Social Icons SVGs
SOCIAL_SVGS = {
    "youtube": '<svg viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>'
}

def render_navigation(current_filename):
    def active(fn):
        return ' current-menu-item' if current_filename == fn else ''

    return f"""<nav class="wp-block-navigation is-responsive order-1 md:order-0" aria-label="Navegación principal">
      <ul class="wp-block-navigation__container">
        <li class="wp-block-navigation-item{active('index.html')}">
          <a href="index.html">Inicio</a>
        </li>
        
        <li class="wp-block-navigation-item has-children{active('utn-facultad-regional-resistencia-utn-frre.html')}">
          <a href="utn-facultad-regional-resistencia-utn-frre.html">UTN FRRe</a>
          <ul class="wp-block-navigation__submenu-container">
            <li class="wp-block-navigation-item{active('ingenieria-en-sistemasutn.html')}"><a href="ingenieria-en-sistemasutn.html">ISI (Ing. en Sistemas de Información)</a></li>
            <li class="wp-block-navigation-item{active('iem-ing-electro-mecanica.html')}"><a href="iem-ing-electro-mecanica.html">IEM (Ing. Electromecánica)</a></li>
            <li class="wp-block-navigation-item{active('iq-ingenieria-quimica.html')}"><a href="iq-ingenieria-quimica.html">IQ (Ing. Química)</a></li>
            <li class="wp-block-navigation-item{active('ing-mecatronica.html')}"><a href="ing-mecatronica.html">IM (Ing. Mecatrónica)</a></li>
            <li class="wp-block-navigation-item{active('licenciatura-en-adm-rural.html')}"><a href="licenciatura-en-adm-rural.html">LAR (Lic. en Administración Rural)</a></li>
            <li class="wp-block-navigation-item{active('seminario-universitario-curso-de-ingreso.html')}"><a href="seminario-universitario-curso-de-ingreso.html">Seminario Universitario (Ingreso)</a></li>
          </ul>
        </li>

        <li class="wp-block-navigation-item has-children{active('universidad-nacional-del-nordeste-unne.html')}">
          <a href="universidad-nacional-del-nordeste-unne.html">UNNE</a>
          <ul class="wp-block-navigation__submenu-container">
            <li class="wp-block-navigation-item{active('facena-facultad-de-ciencias-exactas-y-naturales-y-agrimensura.html')}"><a href="facena-facultad-de-ciencias-exactas-y-naturales-y-agrimensura.html">FaCENA (Exactas y Naturales)</a></li>
            <li class="wp-block-navigation-item{active('facultad-de-medicina-unne.html')}"><a href="facultad-de-medicina-unne.html">Facultad de Medicina</a></li>
            <li class="wp-block-navigation-item{active('facultad-de-odontologia-unne.html')}"><a href="facultad-de-odontologia-unne.html">Facultad de Odontología</a></li>
            <li class="wp-block-navigation-item{active('facultad-de-ciencias-veterinarias-unne.html')}"><a href="facultad-de-ciencias-veterinarias-unne.html">Facultad de Ciencias Veterinarias</a></li>
          </ul>
        </li>

        <li class="wp-block-navigation-item{active('universidad-nacional-del-chaco-austral-uncaus.html')}">
          <a href="universidad-nacional-del-chaco-austral-uncaus.html">UNCAUS</a>
        </li>

        <li class="wp-block-navigation-item{active('facultad-de-arquitectura-y-urbanismo.html')}">
          <a href="facultad-de-arquitectura-y-urbanismo.html">Arquitectura (FAU)</a>
        </li>

        <li class="wp-block-navigation-item{active('facultad-de-ingenieria.html')}">
          <a href="facultad-de-ingenieria.html">Facultad de Ingeniería</a>
        </li>
      </ul>
    </nav>"""

FOOTER_HTML = """<footer class="wp-block-template-part">
  <div class="footer-inner">
    <div class="wp-block-columns alignwide" style="display:flex;flex-wrap:wrap;justify-content:center;text-align:center;margin-bottom:2rem;">
      <div class="wp-block-column">
        <h3 class="wp-block-heading" style="font-size:1.6rem;margin-bottom:1rem;color:#ffffff;">Sedes Universitarias Regionales</h3>
        <p style="margin-bottom:0.4rem;color:#cbd5e1;">📍 <strong>Corrientes (Capital)</strong>, Corrientes</p>
        <p style="margin-bottom:0.4rem;color:#cbd5e1;">📍 <strong>Resistencia</strong>, Chaco</p>
        <p style="margin-bottom:1rem;color:#cbd5e1;">📍 <strong>Presidencia Roque Sáenz Peña</strong>, Chaco</p>
      </div>
    </div>
    
    <!-- Footer Map with all 8 academic campuses -->
    <div class="alignwide">
      <div class="map-block-card">
        <div class="wp-block-jetpack-map" id="footer-map" data-points='[
          {"placeTitle":"H3699ACI, Presidencia Roque Sáenz Peña, Chaco, Argentina","title":"UNCAUS","caption":"Universidad Nacional del Chaco Austral","coordinates":{"longitude":-60.427852,"latitude":-26.8200944}},
          {"placeTitle":"French 414, Resistencia, Chaco, Argentina","title":"UTN FRRe","caption":"Facultad Regional Resistencia","coordinates":{"longitude":-58.9791914,"latitude":-27.4510225}},
          {"placeTitle":"Avenida Laprida 405, Resistencia, Chaco, Argentina","title":"Anexo UTN","caption":"Anexo Facultad Regional Resistencia","coordinates":{"longitude":-58.975603,"latitude":-27.447799}},
          {"placeTitle":"Avenida Las Heras 727, Resistencia, Chaco, Argentina","title":"UNNE - Campus Resistencia","caption":"Universidad Nacional del Nordeste","coordinates":{"longitude":-58.985616,"latitude":-27.463379}},
          {"placeTitle":"Avenida Juan José Castelli 1300, Resistencia, Chaco, Argentina","title":"FADyCC (UNNE)","caption":"Facultad de Artes, Diseño y Ciencias de la Cultura","coordinates":{"longitude":-58.9819258,"latitude":-27.4681518}},
          {"placeTitle":"Moreno 1240, Corrientes, Corrientes, Argentina","title":"Facultad de Medicina (UNNE)","caption":"Sede Moreno","coordinates":{"longitude":-58.835821,"latitude":-27.473429}},
          {"placeTitle":"Sargento Juan Bautista Cabral 2001, Corrientes, Corrientes, Argentina","title":"Campus Sargento Cabral (UNNE)","caption":"Veterinarias y Agronomía","coordinates":{"longitude":-58.8243498,"latitude":-27.4593115}},
          {"placeTitle":"Avenida Libertad 5460A, Corrientes, Corrientes, Argentina","title":"Campus Deodoro Roca (UNNE)","caption":"FaCENA y Odontología","coordinates":{"longitude":-58.7689939,"latitude":-27.4614404}}
        ]' data-zoom="11" data-center-lat="-27.1467617" data-center-lng="-59.59842295">
        </div>
      </div>
    </div>

    <div style="text-align:center;font-size:0.875rem;color:#94a3b8;border-top:1px solid #334155;padding-top:1.5rem;margin-top:2rem;">
      <p>© 2026 Carreras Chaco y Corrientes — Portal Académico Regional Chaco & Corrientes. Todos los derechos reservados.</p>
    </div>
  </div>
</footer>"""

for page in pages:
    filename = page["filename"]
    title = page["title"]
    content = page["content"]

    print(f"Rendering: {title} -> {filename}")

    # 1. Resolve all image URLs to local assets
    def img_replacer(match):
        orig_url = match.group(1)
        resolved = resolve_image(orig_url)
        return f'src="{resolved}"'

    content = re.sub(r'src=["\'](https?://[^"\']+\.(?:png|jpg|jpeg|webp|svg|gif)[^"\']*)["\']', img_replacer, content, flags=re.IGNORECASE)

    # Also resolve background image URLs in style attributes
    def bg_replacer(match):
        orig_url = match.group(1)
        resolved = resolve_image(orig_url)
        return f'url("{resolved}")'
    content = re.sub(r'url\(["\']?(https?://[^"\'\)]+\.(?:png|jpg|jpeg|webp|svg|gif)[^"\'\)]*)["\']?\)', bg_replacer, content, flags=re.IGNORECASE)

    # 2. Rewrite internal WordPress page URLs to local .html links
    for orig_url, target_local in url_to_local_file.items():
        content = content.replace(f'href="{orig_url}"', f'href="{target_local}"')
        content = content.replace(f"href='{orig_url}'", f"href='{target_local}'")

    # 3. Handle Social Link blocks (insert official SVGs)
    def social_replacer(match):
        full_comment = match.group(0)
        m_url = re.search(r'"url":"([^"]+)"', full_comment)
        m_srv = re.search(r'"service":"([^"]+)"', full_comment)
        url = m_url.group(1) if m_url else "#"
        srv = m_srv.group(1) if m_srv else "share"
        svg = SOCIAL_SVGS.get(srv.lower(), "")
        return f"""<li class="wp-social-link wp-social-link-{srv} wp-block-social-link">
          <a href="{url}" class="wp-block-social-link-anchor" target="_blank" rel="noopener nofollow" aria-label="{srv}">
            {svg}
          </a>
        </li>"""

    content = re.sub(r'<!-- wp:social-link \{.*?\} /-->', social_replacer, content)

    # 4. Wrap Jetpack Map blocks in .map-block-card for proper responsive frame
    def map_wrapper(match):
        full_map_tag = match.group(0)
        return f'<div class="map-block-card">{full_map_tag}</div>'

    # 5. Remove remaining Gutenberg block comments while preserving the inner HTML
    content = re.sub(r'<!--\s*/?wp:[^>]*-->', '', content)

    # 6. Assemble Full Page
    nav_html = render_navigation(filename)

    # Render post title only on non-home pages
    title_header_html = ""
    if filename != "index.html":
        title_header_html = f"""<header class="entry-header alignwide">
          <h1 class="wp-block-post-title">{title}</h1>
        </header>"""

    full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} – Carreras Chaco y Corrientes</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Favicon -->
  <link rel="shortcut icon" href="assets/images/favicon_379.ico" type="image/x-icon">
  <link rel="icon" href="assets/images/favicon_379.ico" type="image/x-icon">
  <link rel="apple-touch-icon" href="assets/images/webclip_639091.png">

  <!-- WordPress Core & Assembler Theme CSS -->
  <link rel="stylesheet" href="assets/css/wordpress-assembler.css">
  
  <!-- Local Leaflet CSS for Map Block -->
  <link rel="stylesheet" href="assets/vendor/leaflet/leaflet.css" />
</head>
<body class="wp-embed-responsive">
  <div class="wp-site-blocks">
    
    <!-- HEADER -->
    <header class="wp-block-template-part">
      <div class="header-inner">
        <div class="site-branding">
          <a href="index.html" class="site-logo-link">
            <img src="assets/images/site_logo.jpg" alt="Carreras Chaco y Corrientes">
          </a>
        </div>
        <button class="menu-toggle" aria-expanded="false" aria-label="Abrir menú">
          &#9776;
        </button>
        {nav_html}
      </div>
    </header>

    <!-- MAIN CONTENT -->
    <main class="wp-site-main">
      <div class="entry-content">
        {title_header_html}
        {content}
      </div>
    </main>

    <!-- FOOTER -->
    {FOOTER_HTML}

  </div>

  <!-- Local Leaflet JS & Interactive Components JS -->
  <script src="assets/vendor/leaflet/leaflet.js"></script>
  <script src="assets/js/site.js"></script>
</body>
</html>"""

    # Save to dist
    (DIST_DIR / filename).write_text(full_html, encoding="utf-8")

print("\nAll 16 pages built in dist/ successfully!")

# Synchronize all assets into site/ as well!
for f in ["wordpress-assembler.css"]:
    (SITE_DIR / "assets" / "css").mkdir(parents=True, exist_ok=True)
    shutil.copy2(CSS_DIR / f, SITE_DIR / "assets" / "css" / f)

(SITE_DIR / "assets" / "js").mkdir(parents=True, exist_ok=True)
shutil.copy2(JS_DIR / "site.js", SITE_DIR / "assets" / "js" / "site.js")

(SITE_DIR / "assets" / "images").mkdir(parents=True, exist_ok=True)
for img in IMAGES_DIR.glob("*.*"):
    shutil.copy2(img, SITE_DIR / "assets" / "images" / img.name)

# Vendor leaflet sync
site_vendor = SITE_DIR / "assets" / "vendor" / "leaflet"
site_vendor.mkdir(parents=True, exist_ok=True)
(site_vendor / "images").mkdir(parents=True, exist_ok=True)
for f in VENDOR_DIR.glob("*.*"):
    shutil.copy2(f, site_vendor / f.name)
for f in (VENDOR_DIR / "images").glob("*.*"):
    shutil.copy2(f, site_vendor / "images" / f.name)

for p in pages:
    shutil.copy2(DIST_DIR / p["filename"], SITE_DIR / p["filename"])

print("Synchronized all pages and assets into site/ folder as well!")
