(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- hero video autoplay fallback ---------- */
  var heroVideo = document.querySelector(".hero-video");
  if (heroVideo && !reduceMotion) {
    var playPromise = heroVideo.play();
    if (playPromise) playPromise.catch(function () {});
  }

  /* ---------- mega menu ---------- */
  var megaMenus = ["konsultacje", "problem", "zabiegi", "onas"].map(function (name) {
    return {
      btn: document.getElementById(name + "MenuBtn"),
      panel: document.getElementById(name + "MegaPanel")
    };
  }).filter(function (m) { return m.btn && m.panel; });

  function closeMegaMenu(menu) {
    menu.btn.setAttribute("aria-expanded", "false");
    menu.panel.hidden = true;
  }
  function openMegaMenu(menu) {
    megaMenus.forEach(closeMegaMenu);
    menu.btn.setAttribute("aria-expanded", "true");
    menu.panel.hidden = false;

    /* clamp within the viewport — wide panels (e.g. 3-column "Zabiegi") would
       otherwise overflow past the screen edge depending on where their toggle sits */
    menu.panel.style.left = "0";
    var li = menu.btn.closest("li");
    var liLeft = li.getBoundingClientRect().left;
    var maxLeft = window.innerWidth - menu.panel.offsetWidth - 20;
    var desired = Math.min(liLeft, Math.max(20, maxLeft));
    menu.panel.style.left = (desired - liLeft) + "px";
  }

  megaMenus.forEach(function (menu) {
    menu.btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var isOpen = menu.btn.getAttribute("aria-expanded") === "true";
      isOpen ? closeMegaMenu(menu) : openMegaMenu(menu);
    });
  });

  document.addEventListener("click", function (e) {
    megaMenus.forEach(function (menu) {
      if (!menu.panel.contains(e.target) && e.target !== menu.btn) {
        closeMegaMenu(menu);
      }
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      var openMenu = megaMenus.find(function (menu) {
        return menu.btn.getAttribute("aria-expanded") === "true";
      });
      if (openMenu) {
        closeMegaMenu(openMenu);
        openMenu.btn.focus();
      }
    }
  });

  /* ---------- mobile drawer ---------- */
  var hamburgerBtn = document.getElementById("hamburgerBtn");
  var drawer = document.getElementById("mobileDrawer");
  var drawerDetails = drawer ? Array.prototype.slice.call(drawer.querySelectorAll("details")) : [];

  /* accordion behaviour: opening one category collapses any other that was open */
  drawerDetails.forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (d.open) {
        drawerDetails.forEach(function (other) {
          if (other !== d) other.open = false;
        });
      }
    });
  });

  function openDrawer() {
    if (!drawer) return;
    /* always start fully collapsed, regardless of how it was left last time it was open */
    drawerDetails.forEach(function (d) { d.open = false; });
    drawer.hidden = false;
    requestAnimationFrame(function () { drawer.classList.add("open"); });
    hamburgerBtn.setAttribute("aria-expanded", "true");
    hamburgerBtn.setAttribute("aria-label", "Zamknij menu");
    document.body.style.overflow = "hidden";
  }
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove("open");
    hamburgerBtn.setAttribute("aria-expanded", "false");
    hamburgerBtn.setAttribute("aria-label", "Otwórz menu");
    document.body.style.overflow = "";
    window.setTimeout(function () { drawer.hidden = true; }, reduceMotion ? 0 : 250);
  }

  if (hamburgerBtn && drawer) {
    hamburgerBtn.addEventListener("click", function () {
      var isOpen = hamburgerBtn.getAttribute("aria-expanded") === "true";
      isOpen ? closeDrawer() : openDrawer();
    });
  }
  if (drawer) {
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.classList.contains("open")) closeDrawer();
    });
    /* the hamburger/drawer are mobile-only (hidden above 900px) — if the drawer is left
       open and the viewport is then widened past that breakpoint, both toggles disappear
       with no way to close it and body scroll stays locked, so force-close automatically */
    var desktopMQ = window.matchMedia("(min-width: 1025px)");
    var handleDesktopChange = function (e) {
      if (e.matches) closeDrawer();
    };
    if (desktopMQ.addEventListener) {
      desktopMQ.addEventListener("change", handleDesktopChange);
    } else if (desktopMQ.addListener) {
      desktopMQ.addListener(handleDesktopChange);
    }
  }

  /* ---------- testimonial carousel ---------- */
  var track = document.getElementById("testimonialTrack");
  var mask = document.getElementById("tMask");
  var slides = Array.prototype.slice.call(document.querySelectorAll(".t-slide"));
  var dotsWrap = document.getElementById("tDots");
  var prevBtn = document.getElementById("tPrev");
  var nextBtn = document.getElementById("tNext");
  var current = 0;
  var dots = [];

  var STAR_PATH = "M10 0l2.9 6.9 7.1.7-5.5 5 1.7 7.2-6.2-4-6.2 4 1.7-7.2-5.5-5 7.1-.7z";
  slides.forEach(function (slide) {
    var starsWrap = slide.querySelector(".t-stars");
    if (!starsWrap) return;
    var html = "";
    for (var i = 0; i < 5; i++) {
      html += '<svg viewBox="0 0 20 20"><path d="' + STAR_PATH + '" fill="currentColor"/></svg>';
    }
    starsWrap.innerHTML = html;
  });

  if (dotsWrap) {
    slides.forEach(function (_, i) {
      var dot = document.createElement("button");
      dot.className = "t-dot";
      dot.type = "button";
      dot.setAttribute("aria-label", "Przejdź do opinii " + (i + 1) + " z " + slides.length);
      dot.addEventListener("click", function () { showSlide(i); });
      dotsWrap.appendChild(dot);
      dots.push(dot);
    });
  }

  function showSlide(index) {
    if (!slides.length || !track) return;
    current = (index + slides.length) % slides.length;
    track.style.transform = "translateX(-" + (current * (100 / slides.length)) + "%)";
    if (mask) mask.style.height = slides[current].offsetHeight + "px";
    dots.forEach(function (dot, i) {
      dot.classList.toggle("active", i === current);
      dot.setAttribute("aria-current", i === current ? "true" : "false");
    });
  }
  showSlide(0);

  if (prevBtn) prevBtn.addEventListener("click", function () { showSlide(current - 1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { showSlide(current + 1); });

  var testimonialShell = document.querySelector(".t-shell");
  if (testimonialShell) {
    testimonialShell.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") showSlide(current - 1);
      if (e.key === "ArrowRight") showSlide(current + 1);
    });
  }

  window.addEventListener("resize", function () {
    if (mask && slides.length) mask.style.height = slides[current].offsetHeight + "px";
  });

  /* ---------- newsletter form (no backend — be honest, don't fake success) ---------- */
  var newsletterForm = document.getElementById("newsletterForm");
  var newsletterStatus = document.getElementById("newsletterStatus");

  if (newsletterForm && newsletterStatus) {
    newsletterForm.addEventListener("submit", function (e) {
      e.preventDefault();
      newsletterStatus.hidden = false;
      newsletterStatus.textContent =
        "Zapisy nie są jeszcze podłączone — ten formularz wymaga usługi e-mail (np. Mailchimp, Klaviyo, Formspree), zanim będzie mógł działać.";
    });
  }

  /* ---------- footer year ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ---------- treatments row — scroll progress bar ---------- */
  var trickRow = document.querySelector(".trick-row");
  var progressFill = document.querySelector(".progress-fill");
  if (trickRow && progressFill) {
    trickRow.addEventListener("scroll", function () {
      var max = trickRow.scrollWidth - trickRow.clientWidth;
      var pct = max > 0 ? (trickRow.scrollLeft / max) * 100 : 0;
      progressFill.style.width = pct + "%";
    });
  }

  /* ---------- treatments row — drag to scroll ---------- */
  if (trickRow) {
    var isDragging = false;
    var dragMoved = false;
    var dragStartX = 0;
    var dragStartScroll = 0;

    /* without this, starting the drag on a card (its <a>/<img>) triggers the
       browser's native "drag this link/image" gesture instead of our own —
       CSS -webkit-user-drag:none covers Chrome/Safari, this covers Firefox too */
    trickRow.addEventListener("dragstart", function (e) {
      e.preventDefault();
    });

    trickRow.addEventListener("mousedown", function (e) {
      isDragging = true;
      dragMoved = false;
      dragStartX = e.pageX;
      dragStartScroll = trickRow.scrollLeft;
      trickRow.classList.add("dragging");
    });

    window.addEventListener("mousemove", function (e) {
      if (!isDragging) return;
      var delta = e.pageX - dragStartX;
      if (Math.abs(delta) > 3) dragMoved = true;
      trickRow.scrollLeft = dragStartScroll - delta;
    });

    window.addEventListener("mouseup", function () {
      if (!isDragging) return;
      isDragging = false;
      trickRow.classList.remove("dragging");
    });

    /* a drag that actually moved the row shouldn't also activate the card link underneath */
    trickRow.addEventListener("click", function (e) {
      if (dragMoved) {
        e.preventDefault();
        e.stopPropagation();
        dragMoved = false;
      }
    }, true);
  }

  /* ---------- treatments row — horizontal image parallax (matches archon.au) ----------
     On archon.au each card's photo is rendered at 200% width (see .trick-img) and
     shifted with translateX, recalculated continuously as the row scrolls, so the
     image slides slightly within its frame instead of just riding along with the
     card — a horizontal parallax. Measured directly off the live site: for every
     card, translateX% correlates linearly with that card's own horizontal center
     position in the browser window (translateX% ≈ -(centerX / windowWidth) * 47),
     clamped to ±49% (just under the ±50% where the oversized image would start
     showing a blank edge). Reproduced here with the same scale/clamp. */
  /* only real photos — the ph-gradient placeholder cards (no photo yet) have no
     image detail to slide, so skip them rather than shifting a flat gradient */
  var trickImgs = trickRow ? Array.prototype.slice.call(trickRow.querySelectorAll("img.trick-img")) : [];
  if (trickImgs.length) {
    var PARALLAX_SCALE = 47;
    var PARALLAX_CAP = 49;
    var parallaxRAF = null;

    function applyParallax() {
      parallaxRAF = null;
      var windowWidth = window.innerWidth;
      trickImgs.forEach(function (img) {
        var rect = img.getBoundingClientRect();
        var centerX = rect.left + rect.width / 2;
        var pct = -(centerX / windowWidth) * PARALLAX_SCALE;
        if (pct > PARALLAX_CAP) pct = PARALLAX_CAP;
        if (pct < -PARALLAX_CAP) pct = -PARALLAX_CAP;
        img.style.transform = "translateX(" + pct.toFixed(3) + "%)";
      });
    }
    function scheduleParallax() {
      if (parallaxRAF === null) parallaxRAF = requestAnimationFrame(applyParallax);
    }

    trickRow.addEventListener("scroll", scheduleParallax);
    window.addEventListener("resize", scheduleParallax);
    applyParallax();
  }

  /* ---------- benefits marquee — scroll-linked, not a timed loop (matches archon.au) ----------
     Measured directly off the live site: the ticker's position never changes on
     its own — it sits frozen while the page is still, and only moves in response
     to real scroll input, in either direction (scroll down shifts it one way,
     scroll up reverses it). Reproduced here as a scroll delta applied to a
     wrapping offset.

     The HTML holds exactly ONE tile (one pass through the phrase list). A fixed
     "duplicate it once" isn't enough — that only covers 2 tile-widths, and on a
     wide viewport where one tile is narrower than the section, the wrap point
     falls inside the visible area and the row visibly runs out of content mid-
     scroll. Instead, clone the tile as many times as needed so the track always
     covers (section width + one tile), which guarantees content is available
     for every possible wrapped offset — recomputed on resize too, since the
     tile's own width changes with the viewport (its font-size is vw-based). */
  var marqueeTrack = document.getElementById("marqueeTrack");
  if (marqueeTrack && !reduceMotion) {
    var marqueeSection = marqueeTrack.closest(".marquee");
    var marqueeTile = Array.prototype.slice.call(marqueeTrack.children);
    var MARQUEE_SPEED = 0.26; // measured px-of-shift per px-of-scroll on archon.au
    var marqueeHalfWidth = 0;
    var marqueeOffset = 0;
    var lastMarqueeScrollY = window.scrollY;
    var marqueeRAF = null;

    function fillMarquee() {
      while (marqueeTrack.children.length > marqueeTile.length) {
        marqueeTrack.removeChild(marqueeTrack.lastElementChild);
      }
      marqueeHalfWidth = marqueeTrack.scrollWidth;
      var sectionWidth = marqueeSection.getBoundingClientRect().width;
      while (marqueeTrack.scrollWidth < sectionWidth + marqueeHalfWidth) {
        marqueeTile.forEach(function (el) {
          marqueeTrack.appendChild(el.cloneNode(true));
        });
      }
    }
    function renderMarquee() {
      marqueeTrack.style.transform = "translateX(" + (-marqueeOffset).toFixed(2) + "px)";
    }
    function applyMarquee() {
      marqueeRAF = null;
      var currentScrollY = window.scrollY;
      var delta = currentScrollY - lastMarqueeScrollY;
      lastMarqueeScrollY = currentScrollY;
      marqueeOffset -= delta * MARQUEE_SPEED;
      marqueeOffset = ((marqueeOffset % marqueeHalfWidth) + marqueeHalfWidth) % marqueeHalfWidth;
      renderMarquee();
    }
    function scheduleMarquee() {
      if (marqueeRAF === null) marqueeRAF = requestAnimationFrame(applyMarquee);
    }
    function recalcMarquee() {
      fillMarquee();
      marqueeOffset = ((marqueeOffset % marqueeHalfWidth) + marqueeHalfWidth) % marqueeHalfWidth;
      renderMarquee();
    }

    fillMarquee();
    window.addEventListener("scroll", scheduleMarquee, { passive: true });
    window.addEventListener("resize", recalcMarquee);
  }
})();
