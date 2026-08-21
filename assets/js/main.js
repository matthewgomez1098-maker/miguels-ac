/* Miguel's A/C — site behaviour. No dependencies. */
(function () {
  "use strict";

  var burger = document.querySelector(".burger");
  var nav = document.getElementById("primary-nav");

  /* Mobile menu */
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      nav.setAttribute("data-open", String(!open));
    });
  }

  /* Nav dropdowns — hover on desktop, tap on mobile */
  var isDesktop = function () { return window.matchMedia("(min-width: 1041px)").matches; };

  document.querySelectorAll(".nav__group").forEach(function (group) {
    var toggle = group.querySelector(".nav__toggle");
    if (!toggle) return;

    var setOpen = function (open) {
      group.setAttribute("data-open", String(open));
      toggle.setAttribute("aria-expanded", String(open));
    };

    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      setOpen(group.getAttribute("data-open") !== "true");
    });
    group.addEventListener("mouseenter", function () { if (isDesktop()) setOpen(true); });
    group.addEventListener("mouseleave", function () { if (isDesktop()) setOpen(false); });
    group.addEventListener("focusout", function (e) {
      if (isDesktop() && !group.contains(e.relatedTarget)) setOpen(false);
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    document.querySelectorAll('.nav__group[data-open="true"]').forEach(function (g) {
      g.setAttribute("data-open", "false");
      var t = g.querySelector(".nav__toggle");
      if (t) t.setAttribute("aria-expanded", "false");
    });
  });

  /* FAQ accordion — one open at a time */
  document.querySelectorAll(".faq__item").forEach(function (item) {
    var q = item.querySelector(".faq__q");
    if (!q) return;
    q.addEventListener("click", function () {
      var open = item.getAttribute("data-open") === "true";
      item.closest(".faq__list").querySelectorAll(".faq__item").forEach(function (other) {
        other.setAttribute("data-open", "false");
        other.querySelector(".faq__q").setAttribute("aria-expanded", "false");
      });
      item.setAttribute("data-open", String(!open));
      q.setAttribute("aria-expanded", String(!open));
    });
  });

  /* Reveal on scroll */
  var revealables = document.querySelectorAll("[data-reveal]");
  if (revealables.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    revealables.forEach(function (el) { io.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* Booking forms: no backend yet, so confirm inline instead of losing the lead. */
  document.querySelectorAll("form[data-lead-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status");
      if (status) {
        status.setAttribute("data-show", "true");
        status.focus();
      }
      form.reset();
    });
  });
})();
