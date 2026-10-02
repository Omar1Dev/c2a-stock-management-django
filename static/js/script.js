/* =========================================================
   Stock Management System — Main JS
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

  // ---- Active nav link highlighting ----
  const currentPath = window.location.pathname;
  document.querySelectorAll(".nav-links a").forEach(function (link) {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });

  // ---- Auto-dismiss flash messages after 4 seconds ----
  const messages = document.querySelectorAll(".message");
  messages.forEach(function (msg) {
    setTimeout(function () {
      msg.style.transition = "opacity .4s ease, max-height .4s ease";
      msg.style.opacity = "0";
      msg.style.maxHeight = "0";
      msg.style.padding = "0";
      msg.style.marginBottom = "0";
      setTimeout(function () { msg.remove(); }, 420);
    }, 4000);
  });

  // ---- product_form: sync initial_quantity to current on add ----
  const initialQtyInput = document.getElementById("id_initial_quantity");
  const currentQtyInput = document.getElementById("id_current_quantity");
  const isEditPage = document.body.dataset.formMode === "edit";

  if (initialQtyInput && currentQtyInput && !isEditPage) {
    initialQtyInput.addEventListener("input", function () {
      if (currentQtyInput.value === "" || currentQtyInput.dataset.touched !== "true") {
        currentQtyInput.value = this.value;
      }
    });
    currentQtyInput.addEventListener("input", function () {
      this.dataset.touched = "true";
    });
  }

  // ---- Toast helper ----
  window.showToast = function (text, duration) {
    duration = duration || 3000;
    let toast = document.getElementById("toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "toast";
      document.body.appendChild(toast);
    }
    toast.textContent = text;
    toast.classList.add("show");
    setTimeout(function () { toast.classList.remove("show"); }, duration);
  };

  // ---- Search: clear filter button ----
  const clearBtn = document.getElementById("clear-search");
  if (clearBtn) {
    clearBtn.addEventListener("click", function () {
      window.location.href = window.location.pathname;
    });
  }

  // ---- Auth page: rotating image slideshow ----
  const slides = document.querySelectorAll(".auth-slide");
  if (slides.length > 1) {
    let current = 0;
    setInterval(function () {
      slides[current].classList.remove("active");
      current = (current + 1) % slides.length;
      slides[current].classList.add("active");
    }, 4000);
  }

});
