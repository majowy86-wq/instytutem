(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- page scroll-progress bar (above the header, every page) ----------
     archon.au's real bar doesn't snap to the scroll ratio — it eases toward it,
     still visibly catching up for ~1s after scrolling stops (measured live: an
     instant window.scrollTo with no native scroll momentum still left the bar's
     scaleX interpolating for ~900ms). Sampled the decay rate directly
     (residual shrinks to ~0.858x every ~51ms, i.e. every ~3 frames at 60fps) —
     that resolves to ~0.05 (5%) closer to the target per animation frame, a
     standard lerp, not a CSS transition (which wouldn't restart correctly on
     every scroll event). Animates `width` (not `transform:scaleX`, which
     archon.au itself uses) — scaleX renders through GPU texture scaling and
     showed a real, visible soft/blurred trailing edge at fractional scale
     factors (screenshot-confirmed); `width` goes through normal layout/paint
     and is always pixel-crisp, so a deliberate 1:1 departure from archon.au's
     own implementation detail here, not from its visible behavior. */
  var progressBar = document.querySelector(".progress-bar");
  if (progressBar) {
    var progressTarget = 0;
    var progressCurrent = 0;
    var progressRunning = false;
    var tickProgressBar = function () {
      progressCurrent += (progressTarget - progressCurrent) * 0.05;
      if (Math.abs(progressTarget - progressCurrent) < 0.0005) {
        progressCurrent = progressTarget;
        progressBar.style.width = progressCurrent * 100 + "%";
        progressRunning = false; /* idle once converged — an rAF loop that never
          stops keeps the layer mid-transform forever, which on some browsers
          renders a continuously-animating thin bar slightly soft/anti-aliased
          instead of crisp; stopping once settled avoids that entirely */
        return;
      }
      progressBar.style.width = progressCurrent * 100 + "%";
      requestAnimationFrame(tickProgressBar);
    };
    var updateProgressTarget = function () {
      var scrollable = document.documentElement.scrollHeight - window.innerHeight;
      progressTarget = scrollable > 0 ? window.scrollY / scrollable : 0;
      if (reduceMotion) {
        progressCurrent = progressTarget;
        progressBar.style.width = progressTarget * 100 + "%";
      } else if (!progressRunning) {
        progressRunning = true;
        requestAnimationFrame(tickProgressBar);
      }
    };
    window.addEventListener("scroll", updateProgressTarget, { passive: true });
    window.addEventListener("resize", updateProgressTarget);
    updateProgressTarget();
  }

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

  if (track && slides.length) {
    track.style.width = slides.length * 100 + "%";
    slides.forEach(function (slide) {
      slide.style.flex = "0 0 " + 100 / slides.length + "%";
      slide.style.width = 100 / slides.length + "%";
    });
  }

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
     Requested in chat, not on the reference site: one small clickable label per
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
      /* on mobile (≤767px, same tier the CSS already hides every label but
         the active one) the label is pinned to the bar's start instead of
         its own segment's start — requested in chat, so whichever category
         is active always reads in the same spot ("Zabiegi Hi-Tech"'s spot),
         rather than jumping around the bar as different segments activate. */
      var mobile = window.innerWidth <= 767;
      catLabels.forEach(function (label, i) {
        if (bounds[i] === undefined) return;
        label.style.left = mobile ? "0%" : bounds[i] + "%";
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
    window.addEventListener("resize", layoutCatLabels);
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

     The row's real card width (measured off the reference site — see the CSS
     comment on .trick-card) doesn't divide evenly into every possible
     viewport width, so left alone the trailing card gets cut by a
     different, arbitrary fraction depending on viewport width — sometimes
     a sliver, sometimes almost whole. Fixed by solving for a slightly
     nudged card width — --tc-card-w, a CSS custom property the base
     width:22% falls back to — such that exactly (k + 0.5) cards fit the
     row's visible width (after the left gutter) for some whole number k:
     k full cards, then one cut exactly in half. Recomputed on resize;
     min-width/max-width in CSS still clamp it to the bounds measured on the
     reference site as a safety net.

     This only guarantees the half-cut card at scrollLeft:0 (the first
     view) — holding it at every later rest position too would need
     scroll-snap, which was tried and reverted (see the CSS comment on
     .trick-card): it broke free dragging and ate the left gutter. The
     first view is where the signal matters most anyway.

     On mobile (≤479px, same tier the rest of this file treats as
     "mobile") the card count is fixed at 2.5 instead of auto-solved —
     requested in chat, so cards read as a compact carousel on a phone
     screen instead of the 1.5 cards the reference-site bounds would
     otherwise produce there. That means going narrower than the
     173–315px bounds measured off the reference site (deliberate
     deviation, this tier already isn't reference-matched — see the
     mobile-only min-width override in the CSS .trick-card rule). */
  if (trickRow) {
    var CARD_MOBILE_MAX_WIDTH = 479; /* matches the CSS ≤479px card tier */
    var CARD_MOBILE_MIN_W = 100;
    var CARD_MOBILE_MAX_W = 250;
    var CARD_MIN_W = 173;
    var CARD_MAX_W = 315;
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
      var isMobile = window.innerWidth <= CARD_MOBILE_MAX_WIDTH;
      var minW = isMobile ? CARD_MOBILE_MIN_W : CARD_MIN_W;
      var maxW = isMobile ? CARD_MOBILE_MAX_W : CARD_MAX_W;
      var wholeCards = isMobile ? 2 : Math.max(1, Math.floor(usable / step));
      var newCardWidth = (usable - wholeCards * gap) / (wholeCards + 0.5);
      if (!isMobile) {
        /* the width solved for a given card count can land outside the
           bounds measured on the reference site (173–315px, see CSS) — e.g. "2.5 wide
           cards" fitting a mid-size viewport might solve to ~330px, past the
           max. Rather than let min/max-width clamp it (which would silently
           break the half-cut math, since the clamped width no longer matches
           what was solved for), pick a different card COUNT whose solved
           width actually fits the bounds. Mobile skips this — the count is
           fixed at 2.5 there by design, not auto-solved. */
        var guard = 0;
        while ((newCardWidth > maxW || newCardWidth < minW) && guard < 20) {
          wholeCards += newCardWidth > maxW ? 1 : -1;
          if (wholeCards < 1) { wholeCards = 1; break; }
          newCardWidth = (usable - wholeCards * gap) / (wholeCards + 0.5);
          guard++;
        }
      }
      newCardWidth = Math.max(minW, Math.min(maxW, newCardWidth));
      trickRow.style.setProperty("--tc-card-w", newCardWidth + "px");
    };
    layoutCardHalfCut();
    window.addEventListener("resize", layoutCardHalfCut);
  }

  /* ---------- treatments row — scroll-jack: a few cards scroll sideways before
     the page continues scrolling down (requested in chat — not present on
     the reference site, a deliberate deviation, documented in DOKUMENTACJA.md).

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

  /* ---------- treatments row — horizontal image parallax (matches the reference site) ----------
     On the reference site each card's photo is rendered at 200% width (see .trick-img) and
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

  /* ---------- benefits marquee — scroll-linked, not a timed loop (matches the reference site) ----------
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
    var MARQUEE_SPEED = 0.26; // measured px-of-shift per px-of-scroll on the reference site
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

  /* ---------- treatment page — sticky quick-nav tabs (scroll-spy + smooth scroll) ---------- */
  var treatmentTabs = document.querySelectorAll(".treatment-tab");
  if (treatmentTabs.length) {
    var tabSections = [];
    treatmentTabs.forEach(function (tab) {
      var id = tab.getAttribute("href").slice(1);
      var section = document.getElementById(id);
      if (section) tabSections.push({ tab: tab, section: section });
    });
    var setActiveTab = function () {
      var pos = window.scrollY + 160;
      var current = tabSections[0];
      tabSections.forEach(function (entry) {
        if (entry.section.offsetTop <= pos) current = entry;
      });
      tabSections.forEach(function (entry) {
        entry.tab.classList.toggle("is-active", entry === current);
      });
    };
    window.addEventListener("scroll", setActiveTab, { passive: true });
    setActiveTab();

    /* the reference site scrolls smoothly to the target section instead of
       jumping instantly — offset is the sticky nav (80px) + sticky tabs bar's
       own height, so the section heading lands clear of both, not hidden
       underneath them */
    var siteNav = document.querySelector(".site-nav");
    var tabsBar = document.querySelector(".treatment-tabs");
    tabSections.forEach(function (entry) {
      entry.tab.addEventListener("click", function (e) {
        e.preventDefault();
        var offset = (siteNav ? siteNav.offsetHeight : 0) + (tabsBar ? tabsBar.offsetHeight : 0);
        var top = entry.section.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: top, behavior: reduceMotion ? "auto" : "smooth" });
      });
    });
  }

  /* ---------- treatment page — Care sub-tabs (Przeciwwskazania/Przygotowanie/Postępowanie) ----------
     archon.au's real tab-pane switch (measured on the live Webflow w-tabs element:
     data-duration-in="300" data-duration-out="100" data-easing="ease") — cross-fades
     out the old panel then fades in the new one, instead of an instant hidden-attribute
     swap. */
  var careTabs = document.querySelectorAll(".care-tab");
  if (careTabs.length) {
    careTabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        if (tab.classList.contains("is-active")) return;
        var targetId = tab.getAttribute("aria-controls");
        var targetPanel = document.getElementById(targetId);
        var currentPanel = document.querySelector(".care-panel:not([hidden])");
        careTabs.forEach(function (t) { t.classList.toggle("is-active", t === tab); });
        if (reduceMotion || !currentPanel || currentPanel === targetPanel) {
          document.querySelectorAll(".care-panel").forEach(function (panel) {
            panel.hidden = panel.id !== targetId;
          });
          return;
        }
        currentPanel.style.transition = "opacity .1s ease";
        currentPanel.style.opacity = "0";
        window.setTimeout(function () {
          currentPanel.hidden = true;
          currentPanel.style.opacity = "";
          currentPanel.style.transition = "";
          targetPanel.hidden = false;
          targetPanel.style.transition = "none";
          targetPanel.style.opacity = "0";
          targetPanel.getBoundingClientRect();
          targetPanel.style.transition = "opacity .3s ease";
          requestAnimationFrame(function () { targetPanel.style.opacity = "1"; });
          window.setTimeout(function () {
            targetPanel.style.opacity = "";
            targetPanel.style.transition = "";
          }, 300);
        }, 100);
      });
    });
  }

  /* ---------- treatment page — accordion (Efekty/Technologia/Przeciwwskazania/FAQ):
     smooth height+opacity open/close, replacing the native <details> instant snap.
     Matches archon.au's real "Accordion Open"/"Accordion Close" IX2 action lists
     (measured via window.Webflow.require('ix2').store.getState(): height→auto and
     opacity 0→1 both 300ms outQuad, arrow rotate 300ms) — outQuad's CSS equivalent
     is the same cubic-bezier(.25,.46,.45,.94) already used elsewhere on this site. */
  document.querySelectorAll(".treatment-accordion-body").forEach(function (body) {
    var inner = document.createElement("div");
    inner.className = "treatment-accordion-body-inner";
    while (body.firstChild) inner.appendChild(body.firstChild);
    body.appendChild(inner);
  });
  document.querySelectorAll(".treatment-accordion details").forEach(function (details) {
    var summary = details.querySelector(":scope > summary");
    var body = details.querySelector(":scope > .treatment-accordion-body");
    if (!summary || !body) return;
    summary.addEventListener("click", function (e) {
      e.preventDefault();
      if (reduceMotion) {
        details.open = !details.open;
        body.style.height = "";
        body.style.opacity = "";
        return;
      }
      if (details.open) {
        var closeFrom = body.scrollHeight;
        body.style.height = closeFrom + "px";
        body.getBoundingClientRect();
        requestAnimationFrame(function () {
          body.style.height = "0px";
          body.style.opacity = "0";
        });
        window.setTimeout(function () { details.open = false; }, 300);
      } else {
        details.open = true;
        var openTo = body.scrollHeight;
        body.style.height = "0px";
        body.style.opacity = "0";
        body.getBoundingClientRect();
        requestAnimationFrame(function () {
          body.style.height = openTo + "px";
          body.style.opacity = "1";
        });
        window.setTimeout(function () { body.style.height = ""; }, 300);
      }
    });
  });

  /* ---------- magnetic button (archon.au's real .magnetic-wrapper effect on
     its CTA banner "Book Now" button) — measured directly on the live site:
     synthetic mousemove events don't trigger it (same tooling limitation as
     DOKUMENTACJA.md's "Ważne odkrycia" #11/15/18/19), so probed with a tiny
     marker element placed at a known offset inside the button, then a real
     hover on that marker: resulting pull was translate3d(-0.66em, -0.18em)
     for a cursor offset of (-65px, -19.5px) from the button's own center —
     i.e. a pull strength of ≈0.15-0.16× the offset on both axes. Also
     confirmed transitionDuration:0s on the live element (both mid-hover and
     right after leaving) — no CSS transition is involved, consistent with a
     JS-driven per-frame follow rather than an eased transition, so
     implemented the same way: a requestAnimationFrame loop lerping the
     current offset toward the target. Strength bumped from the raw-measured
     0.15 to 0.35 per direct user feedback comparing our button side-by-side
     with the live archon.au one ("BARDZIEJ ruszać, w większym zakresie" —
     should move more, in a larger range). */
  if (!reduceMotion) {
    document.querySelectorAll(".magnetic-btn").forEach(function (btn) {
      var strength = 0.35;
      var targetX = 0, targetY = 0, curX = 0, curY = 0, raf = null;
      function loop() {
        curX += (targetX - curX) * 0.2;
        curY += (targetY - curY) * 0.2;
        btn.style.transform = "translate(" + curX.toFixed(2) + "px, " + curY.toFixed(2) + "px)";
        if (Math.abs(targetX - curX) > 0.1 || Math.abs(targetY - curY) > 0.1) {
          raf = requestAnimationFrame(loop);
        } else {
          curX = targetX; curY = targetY;
          btn.style.transform = "translate(" + curX.toFixed(2) + "px, " + curY.toFixed(2) + "px)";
          raf = null;
        }
      }
      btn.addEventListener("mousemove", function (e) {
        var r = btn.getBoundingClientRect();
        targetX = (e.clientX - r.left - r.width / 2) * strength;
        targetY = (e.clientY - r.top - r.height / 2) * strength;
        if (!raf) raf = requestAnimationFrame(loop);
      });
      btn.addEventListener("mouseleave", function () {
        targetX = 0;
        targetY = 0;
        if (!raf) raf = requestAnimationFrame(loop);
      });
    });
  }

  /* ---------- CTA banner parallax (archon.au's real #Solution .section-parallax:
     an oversized <img> — measured 1200px tall inside a 400px-tall section, i.e.
     800px of vertical slack — translated on scroll via a Webflow IX2 scroll
     trigger). Measured live on archon.au by reading the img's computed
     transform at controlled scroll positions: roughly linear, translateY ≈
     -0.22 × the section's own viewport-relative top offset, over the section's
     full transit through the viewport (the exact edges of Webflow's own IX2
     curve weren't cleanly reproducible from outside — same class of limitation
     as the magnetic button — so this is the measured core ratio, not a guess,
     applied with a plain scroll-linked rAF loop instead of chasing Webflow's
     internal easing). Our own image is oversized by 180px (90px top+bottom,
     see .cta-banner-image CSS) — offset is clamped to that slack so the
     oversized image never reveals an empty edge. */
  (function () {
    var img = document.querySelector(".cta-banner-image");
    if (!img || reduceMotion) return;
    var section = img.closest(".cta-banner");
    var ticking = false;
    function update() {
      var rect = section.getBoundingClientRect();
      var maxOffset = (img.offsetHeight - rect.height) / 2;
      var offset = -0.22 * rect.top;
      if (offset > maxOffset) offset = maxOffset;
      if (offset < -maxOffset) offset = -maxOffset;
      img.style.transform = "translateY(" + offset.toFixed(2) + "px)";
      ticking = false;
    }
    function onScroll() {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    update();
  })();

  /* ---------- treatment page — scroll-reveal (the reference site's real
     "slideInBottom"/"fadeIn" IX2 presets, see the CSS comment on [data-reveal]) --------- */
  var revealEls = document.querySelectorAll("[data-reveal]");
  if (revealEls.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealEls.forEach(function (el) { el.classList.add("is-revealed"); });
    } else {
      var revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-revealed");
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15 });
      revealEls.forEach(function (el) { revealObserver.observe(el); });
    }
  }
})();
