
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
