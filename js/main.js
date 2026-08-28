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

  /* ---------- treatments row — scroll progress bar, category labels + map ----------
     Requested in chat, not on archon.au: one small clickable label per
     category (Zabiegi Hi-Tech / Iniekcyjne / Manualne — the same 3 groups
     as the "Zabiegi" nav menu), fixed at the START of its own segment of
     the bar below (small left margin, not flush with the tick); whichever
     one matches the card CENTERED in the viewport is highlighted, the
     other two stay dimmed. Two tick marks on the bar mark where the next
     category starts — a miniature timeline — and share the exact dimmed
     styling of the .trick-cat-divider rules between the cards themselves
     (see CSS), so a divider and its tick read as the same marker in two
     places, not two unrelated devices.

     The viewport CENTER, not the leading/left edge, is what both "which
     category is current" and "where a clicked label jumps to" are anchored
     to — one consistent reference point for the whole feature, not a mix.

     Progress (fill width) means "how far through the 24 cards" — a
     fraction of CARD INDEX (centered card / (total - 1)), not of raw
     scrollLeft/maxScroll pixels like the bar originally was. Pixel-based
     fractions skew toward whatever's already visible at rest: with ~3-4
     cards fitting in view at once, the last category (only 4 of 24 cards)
     ended up squeezed into a sliver of the bar a few percent wide — easy to
     miss entirely, which is exactly what got reported. Index-based, every
     card (and so every category) gets its proportionate, honest share of
     the bar regardless of viewport width. To still flow smoothly rather
     than visibly jump at each of the 24 card boundaries, the fraction is
     interpolated continuously between the current card and the next
     (fractionalIndex), not snapped to whole numbers — only the *active
     label* decision snaps (a label is either the current category or it
     isn't, there's no "half current"). Tick and label positions are pure
     constants (11/23, 20/23 of the way through) — they never need
     recomputing on resize. */
  var trickRow = document.querySelector(".trick-row");
  var progressFill = document.querySelector(".progress-fill");
  var catLabels = document.querySelectorAll(".trick-cat-label");
  var progressTicks = document.getElementById("progressTicks");
  if (trickRow && progressFill) {
    var trickCards = trickRow.querySelectorAll(".trick-card");

    /* bounds: category boundary positions as a % of the bar (one more
       entry than categories — 0 and 100 bookend it, e.g. [0, 47.8, 87.0,
       100] for 3 categories). firstIndex: the card index each category
       starts at (e.g. [0, 11, 20]), same order as catLabels in the DOM. */
    var categoryInfo = function () {
      var bounds = [0];
      var firstIndex = [0];
      var prevCat = null;
      for (var i = 0; i < trickCards.length; i++) {
        var cat = trickCards[i].dataset.cat;
        if (cat && cat !== prevCat && prevCat !== null) {
          bounds.push((i / (trickCards.length - 1)) * 100);
          firstIndex.push(i);
        }
        prevCat = cat || prevCat;
      }
      bounds.push(100);
      return { bounds: bounds, firstIndex: firstIndex };
    };

    var layoutProgressTicks = function () {
      if (!progressTicks || trickCards.length < 2) return;
      progressTicks.innerHTML = "";
      var bounds = categoryInfo().bounds;
      for (var b = 1; b < bounds.length - 1; b++) {
        var tick = document.createElement("div");
        tick.className = "progress-tick";
        tick.style.left = bounds[b] + "%";
        progressTicks.appendChild(tick);
      }
    };

    var layoutCatLabels = function () {
      if (!catLabels.length || trickCards.length < 2) return;
      var bounds = categoryInfo().bounds;
      catLabels.forEach(function (label, i) {
        if (bounds[i] === undefined) return;
        label.style.left = bounds[i] + "%";
      });
    };

    var centerCardIndex = function () {
      var center = trickRow.scrollLeft + trickRow.clientWidth / 2;
      var idx = 0;
      for (var i = 0; i < trickCards.length; i++) {
        if (trickCards[i].offsetLeft <= center) idx = i;
      }
      return idx;
    };

    var fractionalIndex = function (idx, center) {
      var a = trickCards[idx].offsetLeft;
      if (idx >= trickCards.length - 1) return idx;
      var b = trickCards[idx + 1].offsetLeft;
      var span = b - a;
      var frac = span > 0 ? (center - a) / span : 0;
      return idx + Math.max(0, Math.min(1, frac));
    };

    var updateProgress = function () {
      if (trickCards.length < 2) return;
      var center = trickRow.scrollLeft + trickRow.clientWidth / 2;
      var idx = centerCardIndex();
      var smoothPct = (fractionalIndex(idx, center) / (trickCards.length - 1)) * 100;
      progressFill.style.width = smoothPct + "%";
      var activeCat = trickCards[idx].dataset.cat;
      catLabels.forEach(function (label) {
        label.classList.toggle("is-active", label.dataset.cat === activeCat);
      });
    };

    catLabels.forEach(function (label, i) {
      label.addEventListener("click", function () {
        /* a click is an explicit, deliberate scroll — never fight it with
           the scroll-jack's auto-drive if the row happens to be pinned */
        if (typeof takeOverRow === "function") takeOverRow();
        if (i === 0) {
          /* Zabiegi Hi-Tech: card 0 can't be meaningfully centered (there's
             nothing before it to center against) — just the start */
          trickRow.scrollTo({ left: 0, behavior: "smooth" });
          return;
        }
        var cardIdx = categoryInfo().firstIndex[i];
        var card = trickCards[cardIdx];
        if (!card) return;
        var target = card.offsetLeft - (trickRow.clientWidth - card.offsetWidth) / 2;
        var maxScroll = trickRow.scrollWidth - trickRow.clientWidth;
        target = Math.max(0, Math.min(maxScroll, target));
        trickRow.scrollTo({ left: target, behavior: "smooth" });
      });
    });

    trickRow.addEventListener("scroll", updateProgress);
    window.addEventListener("resize", updateProgress);
    layoutProgressTicks();
    layoutCatLabels();
    updateProgress();
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

  /* ---------- treatments row — always end on a half-cut card (requested in
     chat: whichever card is last in view, unless it's genuinely the last
     card in the whole row, should always be cut exactly in half by the
     viewport edge — a constant, deliberate signal that there's more to
     scroll. Applies at every viewport width, mobile included — unlike the
     scroll-jack below, this isn't disabled there.

     The row's real card width (measured off archon.au — see the CSS
     comment on .trick-card) doesn't divide evenly into every possible
     viewport width, so left alone the trailing card gets cut by a
     different, arbitrary fraction depending on viewport width — sometimes
     a sliver, sometimes almost whole. Fixed by solving for a slightly
     nudged card width — --tc-card-w, a CSS custom property the base
     width:22% falls back to — such that exactly (k + 0.5) cards fit the
     row's visible width (after the left gutter) for some whole number k:
     k full cards, then one cut exactly in half. Recomputed on resize;
     min-width/max-width in CSS still clamp it to the archon.au-measured
     bounds as a safety net.

     This only guarantees the half-cut card at scrollLeft:0 (the first
     view) — holding it at every later rest position too would need
     scroll-snap, which was tried and reverted (see the CSS comment on
     .trick-card): it broke free dragging and ate the left gutter. The
     first view is where the signal matters most anyway. */
  if (trickRow) {
    var layoutCardHalfCut = function () {
      var cards = trickRow.querySelectorAll(".trick-card");
      if (cards.length < 2) return;
      var cardWidth = cards[0].offsetWidth;
      var step = cards[1].offsetLeft - cards[0].offsetLeft;
      var gap = step - cardWidth;
      /* at rest (scrollLeft:0, no snap pulling it anywhere else) the visible
         window covers contentX [0, clientWidth) — card 0 starts only after
         the row's own left padding, so that's dead space to subtract first. */
      var paddingLeft = parseFloat(getComputedStyle(trickRow).paddingLeft) || 0;
      var usable = trickRow.clientWidth - paddingLeft;
      var wholeCards = Math.max(1, Math.floor(usable / step));
      var newCardWidth = (usable - wholeCards * gap) / (wholeCards + 0.5);
      /* the width solved for a given card count can land outside the
         archon.au-measured bounds (173–315px, see CSS) — e.g. "2.5 wide
         cards" fitting a mid-size viewport might solve to ~330px, past the
         max. Rather than let min/max-width clamp it (which would silently
         break the half-cut math, since the clamped width no longer matches
         what was solved for), pick a different card COUNT whose solved
         width actually fits the bounds. */
      var guard = 0;
      while ((newCardWidth > 315 || newCardWidth < 173) && guard < 20) {
        wholeCards += newCardWidth > 315 ? 1 : -1;
        if (wholeCards < 1) { wholeCards = 1; break; }
        newCardWidth = (usable - wholeCards * gap) / (wholeCards + 0.5);
        guard++;
      }
      newCardWidth = Math.max(173, Math.min(315, newCardWidth));
      trickRow.style.setProperty("--tc-card-w", newCardWidth + "px");
    };
    layoutCardHalfCut();
    window.addEventListener("resize", layoutCardHalfCut);
  }

  /* ---------- treatments row — scroll-jack: a few cards scroll sideways before
     the page continues scrolling down (requested in chat — not present on
     archon.au, a deliberate deviation, documented in DOKUMENTACJA.md).

     Deliberately NOT wheel-event interception (that reads differently per
     device — mouse wheel vs trackpad vs touch — and this project has twice
     been burned by scroll-linked JS that only half-worked, see CLAUDE.md).
     Instead: .trick-pin-outer wraps the WHOLE section's content — the
     heading/intro text AND the row, not just the row — and is a plain block
     whose height JS sets to (that content's natural height + reveal
     distance); .trick-pin-inner inside it is CSS position:sticky, held
     centered in the viewport (never above the nav). Pinning just the row
     left the heading/intro scrolling away on its own beforehand, so by the
     time the row reached its pinned position the top of the section was
     long gone — pinning the pair together keeps the heading in view right
     above the cards for the whole reveal, instead of leaving it stranded
     above the fold. As the user scrolls down with ANY input method, the
     browser's own sticky implementation holds this whole block in place
     while .trick-pin-outer's extra height passes by underneath — we just
     read how much of that extra height has passed (via getBoundingClientRect,
     recalculated on the real "scroll" event, not simulated) and mirror that
     progress onto trickRow.scrollLeft. Once fully consumed, the sticky box
     naturally runs out of room and releases — ordinary page scroll resumes
     with no explicit "hand back control" step needed.

     Mobile (<=1024px, the site's own hamburger-nav breakpoint) skips all of
     this — a finger already scrolls the row directly and naturally there,
     and there's no scroll wheel to hijack in the first place.

     Accepted trade-off: that reserved extra height is genuinely part of the
     document while this row's section is around — the section after it (RX
     Facials) ends up sitting reveal-distance further down than it would
     without this feature. An earlier version clawed that space back with a
     negative margin-bottom on .trick-pin-outer, but margin doesn't affect
     when CSS sticky itself releases (that's governed by the box's own
     height only) — so the next section's document position moved up while
     the release point didn't, and it started sliding into view from behind
     the still-frozen row well before the reveal finished. Removed: a
     slightly larger permanent gap is the honest cost of a real freeze, not
     something to paper over with a mismatched hack.

     Manual scroll of the row is never blocked — it's always real native
     scrolling — and takes over instantly and unambiguously from the input
     event itself (mousedown, touchstart, or a wheel event with more
     horizontal than vertical delta), not by inferring intent from trickRow's
     own "scroll" event. The earlier version did the latter with a
     set-flag-before-write/clear-flag-after dance, which raced against the
     browser's own (async, sometimes coalesced) firing of that scroll event:
     a run of rapid scroll ticks could clear the flag before the write it
     belonged to was actually observed, so a later, purely auto-driven write
     got misread as a manual takeover and silently froze the row until the
     page was reloaded. Reading real input events sidesteps that entirely.
     Scrolling back above the pinned zone re-arms auto-driving for the next
     pass, instead of it staying off for the rest of the page's life. */
  if (trickRow) {
    var pinOuter = document.getElementById("trickPinOuter");
    var pinInner = pinOuter ? pinOuter.querySelector(".trick-pin-inner") : null;
    if (pinOuter && pinInner) {
      var revealDistance = 0;
      var stuckAt = 80;
      var userTookOverRow = false;

      var computeRevealDistance = function () {
        var cards = trickRow.querySelectorAll(".trick-card");
        if (cards.length < 2) return 0;
        var step = cards[1].offsetLeft - cards[0].offsetLeft;
        var cardsToReveal = Math.min(4, cards.length - 1);
        var maxScroll = trickRow.scrollWidth - trickRow.clientWidth;
        return Math.max(0, Math.min(step * cardsToReveal, maxScroll));
      };

      var MOBILE_MAX_WIDTH = 1024; /* matches the site's own mobile/hamburger breakpoint */

      var layoutPin = function () {
        if (window.innerWidth <= MOBILE_MAX_WIDTH) {
          /* touch already scrolls the row directly with a finger — no
             scroll-jack on mobile, so no pin either (not even a fleeting
             one — the CSS position:sticky fallback is turned off outright,
             not just left with nothing to hold onto) */
          revealDistance = 0;
          pinInner.style.position = "static";
          pinInner.style.top = "";
          pinOuter.style.height = "";
          return;
        }
        pinInner.style.position = "";
        revealDistance = computeRevealDistance();
        /* center the pinned block in the viewport; 80px (nav height) is the
           floor so it never sits underneath/above the sticky nav */
        stuckAt = Math.max(80, Math.round((window.innerHeight - pinInner.offsetHeight) / 2));
        pinInner.style.top = stuckAt + "px";
        pinOuter.style.height = pinInner.offsetHeight + revealDistance + "px";
      };

      var onPageScroll = function () {
        var rectTop = pinOuter.getBoundingClientRect().top;
        if (userTookOverRow) {
          /* scrolled back above the pinned zone entirely — safe to re-arm */
          if (rectTop > stuckAt + 4) userTookOverRow = false;
          return;
        }
        if (revealDistance <= 0) return;
        var scrolledIntoPin = Math.max(0, Math.min(revealDistance, stuckAt - rectTop));
        if (Math.abs(trickRow.scrollLeft - scrolledIntoPin) > 1) {
          trickRow.scrollLeft = scrolledIntoPin;
        }
      };

      var takeOverRow = function () {
        userTookOverRow = true;
      };
      trickRow.addEventListener("mousedown", takeOverRow);
      trickRow.addEventListener("touchstart", takeOverRow, { passive: true });
      trickRow.addEventListener("wheel", function (e) {
        if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) takeOverRow();
      }, { passive: true });

      window.addEventListener("scroll", onPageScroll, { passive: true });
      window.addEventListener("resize", layoutPin);
      layoutPin();
      onPageScroll();
    }
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
