// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Initialize Bootstrap tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Initialize Bootstrap popovers
  var popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Auto-hide alerts after 5 seconds
  setTimeout(function () {
    var alerts = document.querySelectorAll(".alert:not(.alert-permanent)");
    alerts.forEach(function (alert) {
      var bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 5000);

  // Logout confirmation
  const logoutForms = document.querySelectorAll('form[action*="logout"]');
  logoutForms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      if (!confirm("Are you sure you want to logout?")) {
        e.preventDefault();
      }
    });
  });

  // Form validation
  const forms = document.querySelectorAll(".needs-validation");
  forms.forEach((form) => {
    form.addEventListener("submit", function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add("was-validated");
    });
  });

  // Password strength meter
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  passwordInputs.forEach((input) => {
    input.addEventListener("input", function () {
      const password = this.value;
      const strength = calculatePasswordStrength(password);
      updatePasswordStrengthMeter(this, strength);
    });
  });

  // File input custom display
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach((input) => {
    input.addEventListener("change", function () {
      const fileName = this.files[0]?.name || "No file chosen";
      const fileLabel = this.nextElementSibling;
      if (fileLabel) {
        fileLabel.textContent = fileName;
      }
    });
  });

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Back to top button
  const backToTopButton = document.getElementById("back-to-top");
  if (backToTopButton) {
    window.addEventListener("scroll", function () {
      if (window.pageYOffset > 100) {
        backToTopButton.classList.remove("d-none");
      } else {
        backToTopButton.classList.add("d-none");
      }
    });

    backToTopButton.addEventListener("click", function () {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  }

  // Mobile menu toggle
  const mobileMenuToggle = document.querySelector(".navbar-toggler");
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener("click", function () {
      document.body.classList.toggle("mobile-menu-open");
    });
  }
});

// Password strength calculator
function calculatePasswordStrength(password) {
  let strength = 0;

  // Length check
  if (password.length >= 8) strength += 1;
  if (password.length >= 12) strength += 1;

  // Character type checks
  if (/[a-z]/.test(password)) strength += 1; // lowercase
  if (/[A-Z]/.test(password)) strength += 1; // uppercase
  if (/[0-9]/.test(password)) strength += 1; // numbers
  if (/[^A-Za-z0-9]/.test(password)) strength += 1; // special characters

  return strength;
}

// Update password strength meter
function updatePasswordStrengthMeter(input, strength) {
  const meterElement = input
    .closest(".form-group")
    ?.querySelector(".password-strength-meter");
  if (!meterElement) return;

  // Update meter width and color
  const percentage = (strength / 6) * 100;
  meterElement.style.width = `${percentage}%`;

  // Update color based on strength
  let color = "bg-danger"; // very weak
  if (strength > 4) color = "bg-success"; // strong
  else if (strength > 2) color = "bg-warning"; // medium

  meterElement.className = `password-strength-meter ${color}`;
}

// Form data serializer
function serializeForm(form) {
  const formData = new FormData(form);
  const serialized = {};

  for (let [key, value] of formData.entries()) {
    serialized[key] = value;
  }

  return serialized;
}

// AJAX form submission helper
function submitFormAjax(form, url, method = "POST") {
  const formData = new FormData(form);

  return fetch(url, {
    method: method,
    body: formData,
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .catch((error) => console.error("Error:", error));
}

// Get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Debounce function for search inputs
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}
