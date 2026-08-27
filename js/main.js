(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- sticky nav shrink ---------- */
  var nav = document.getElementById("siteNav");
  if (nav) {
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        nav.classList.toggle("nav--scrolled", window.scrollY > 40);
        ticking = false;
      });
    }, { passive: true });
  }

  /* ---------- mega menu ---------- */
  var skinBtn = document.getElementById("skinMenuBtn");
  var skinPanel = document.getElementById("skinMegaPanel");

  function closeMegaMenu() {
    if (!skinBtn || !skinPanel) return;
    skinBtn.setAttribute("aria-expanded", "false");
    skinPanel.hidden = true;
  }
  function openMegaMenu() {
    if (!skinBtn || !skinPanel) return;
    skinBtn.setAttribute("aria-expanded", "true");
    skinPanel.hidden = false;
  }

  if (skinBtn && skinPanel) {
    skinBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var isOpen = skinBtn.getAttribute("aria-expanded") === "true";
      isOpen ? closeMegaMenu() : openMegaMenu();
    });

    document.addEventListener("click", function (e) {
      if (!skinPanel.contains(e.target) && e.target !== skinBtn) {
        closeMegaMenu();
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        closeMegaMenu();
        skinBtn.focus();
      }
    });
  }

  /* ---------- mobile drawer ---------- */
  var hamburgerBtn = document.getElementById("hamburgerBtn");
  var drawerCloseBtn = document.getElementById("drawerCloseBtn");
  var drawer = document.getElementById("mobileDrawer");

  function openDrawer() {
    if (!drawer) return;
    drawer.hidden = false;
    requestAnimationFrame(function () { drawer.classList.add("open"); });
    hamburgerBtn.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  }
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove("open");
    hamburgerBtn.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
    window.setTimeout(function () { drawer.hidden = true; }, reduceMotion ? 0 : 250);
  }

  if (hamburgerBtn && drawer) {
    hamburgerBtn.addEventListener("click", openDrawer);
  }
  if (drawerCloseBtn) {
    drawerCloseBtn.addEventListener("click", closeDrawer);
  }
  if (drawer) {
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.classList.contains("open")) closeDrawer();
    });
  }

  /* ---------- testimonial carousel ---------- */
  var slides = Array.prototype.slice.call(document.querySelectorAll(".testimonial-slide"));
  var dotsWrap = document.getElementById("tDots");
  var prevBtn = document.getElementById("tPrev");
  var nextBtn = document.getElementById("tNext");
  var current = 0;
  var dots = [];

  if (dotsWrap) {
    slides.forEach(function (_, i) {
      var dot = document.createElement("button");
      dot.className = "tdot";
      dot.type = "button";
      dot.setAttribute("aria-label", "Go to testimonial " + (i + 1) + " of " + slides.length);
      dot.addEventListener("click", function () { showSlide(i); });
      dotsWrap.appendChild(dot);
      dots.push(dot);
    });
  }

  function showSlide(index) {
    if (!slides.length) return;
    current = (index + slides.length) % slides.length;
    slides.forEach(function (slide, i) {
      slide.classList.toggle("active", i === current);
    });
    dots.forEach(function (dot, i) {
      dot.classList.toggle("active", i === current);
      dot.setAttribute("aria-current", i === current ? "true" : "false");
    });
  }
  showSlide(0);

  if (prevBtn) prevBtn.addEventListener("click", function () { showSlide(current - 1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { showSlide(current + 1); });

  var testimonialWrap = document.querySelector(".testimonial-wrap");
  if (testimonialWrap) {
    testimonialWrap.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") showSlide(current - 1);
      if (e.key === "ArrowRight") showSlide(current + 1);
    });
  }

  /* ---------- newsletter form (no backend — be honest, don't fake success) ---------- */
  var newsletterForm = document.getElementById("newsletterForm");
  var newsletterStatus = document.getElementById("newsletterStatus");

  if (newsletterForm && newsletterStatus) {
    newsletterForm.addEventListener("submit", function (e) {
      e.preventDefault();
      newsletterStatus.hidden = false;
      newsletterStatus.textContent =
        "Sign-ups aren't connected yet — this form needs an email service (e.g. Mailchimp, Klaviyo, Formspree) before it can go live.";
    });
  }

  /* ---------- footer year ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());
})();
