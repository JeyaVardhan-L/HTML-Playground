/**
 * FRONTIER AI ATLAS — CORE JAVASCRIPT
 * Web Application Frameworks Lab Assignment 2
 * Author: Jey (GITAM CSE)
 */

document.addEventListener("DOMContentLoaded", function () {
  initDashboardParent();
  initSubpageFeatures();
});

/**
 * 1. Parent Dashboard (index.html) logic
 * Handles iframe auto-resizing, mobile navigation drawer, and active navigation highlighting.
 */
function initDashboardParent() {
  const iframe = document.getElementById("content-frame");
  const mobileToggle = document.getElementById("mobileToggle");
  const sidebar = document.getElementById("sidebar");
  const sidebarLinks = document.querySelectorAll(".sidebar-link");

  // Mobile drawer toggle
  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener("click", function () {
      sidebar.classList.toggle("open");
      const isOpen = sidebar.classList.contains("open");
      mobileToggle.setAttribute("aria-expanded", isOpen);
      mobileToggle.textContent = isOpen ? "✕" : "☰";
    });
  }

  // Active state highlighting on sidebar links
  sidebarLinks.forEach((link) => {
    link.addEventListener("click", function () {
      sidebarLinks.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");

      // Auto-close sidebar on mobile after clicking
      if (sidebar && sidebar.classList.contains("open")) {
        sidebar.classList.remove("open");
        if (mobileToggle) mobileToggle.textContent = "☰";
      }

      // Scroll parent window to top smoothly when new page loads
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  // Seamless iframe height adjustment (Same-Origin)
  if (iframe) {
    function resizeIframe() {
      try {
        if (iframe.contentWindow && iframe.contentWindow.document.body) {
          const doc = iframe.contentWindow.document;
          const bodyHeight = doc.body.scrollHeight;
          const docHeight = doc.documentElement.scrollHeight;
          const newHeight = Math.max(bodyHeight, docHeight, 600);
          iframe.style.height = newHeight + 40 + "px";

          // Sync active nav item with the iframe's current filename
          const currentPath = iframe.contentWindow.location.pathname;
          const currentFile = currentPath.substring(currentPath.lastIndexOf("/") + 1) || "home.html";

          sidebarLinks.forEach((link) => {
            const href = link.getAttribute("href");
            if (href === currentFile) {
              sidebarLinks.forEach((l) => l.classList.remove("active"));
              link.classList.add("active");
            }
          });
        }
      } catch (err) {
        // Fallback for security contexts if any
        iframe.style.height = "100vh";
      }
    }

    iframe.addEventListener("load", resizeIframe);
    window.addEventListener("resize", resizeIframe);

    // Listen for resize messages from child iframe pages
    window.addEventListener("message", function (event) {
      if (event.data && event.data.type === "ATLAS_RESIZE") {
        iframe.style.height = Math.max(event.data.height, 600) + 40 + "px";
      }
    });
  }
}

/**
 * 2. Sub-page Features (Executed in both iframe and standalone contexts)
 */
function initSubpageFeatures() {
  notifyParentOfHeight();
  handleStandaloneNotice();
  initModelTableFilters();
  initSurveyForm();
}

/**
 * Sends height message to parent if embedded inside an iframe
 */
function notifyParentOfHeight() {
  if (window.self !== window.top) {
    function sendHeight() {
      const height = Math.max(
        document.body.scrollHeight,
        document.documentElement.scrollHeight
      );
      window.parent.postMessage({ type: "ATLAS_RESIZE", height: height }, "*");
    }

    sendHeight();
    window.addEventListener("resize", sendHeight);

    // Periodic check during image/font render
    setTimeout(sendHeight, 250);
    setTimeout(sendHeight, 800);
  }
}

/**
 * Displays standalone indicator if child page is opened directly
 */
function handleStandaloneNotice() {
  const notice = document.getElementById("standaloneNotice");
  if (notice) {
    if (window.self === window.top) {
      notice.style.display = "flex";
    } else {
      notice.style.display = "none";
    }
  }
}

/**
 * Model Explorer (models.html) search and category filter
 */
function initModelTableFilters() {
  const searchInput = document.getElementById("modelSearch");
  const filterBtns = document.querySelectorAll(".filter-btn");
  const tableRows = document.querySelectorAll("#modelTableBody tr");
  const countBadge = document.getElementById("matchingCount");

  if (!tableRows.length) return;

  let activeCategory = "all";
  let searchQuery = "";

  function applyFilters() {
    let visibleCount = 0;

    tableRows.forEach((row) => {
      const rowCategory = row.getAttribute("data-category") || "";
      const rowText = row.innerText.toLowerCase();

      const matchesCat = activeCategory === "all" || rowCategory.includes(activeCategory);
      const matchesSearch = !searchQuery || rowText.includes(searchQuery);

      if (matchesCat && matchesSearch) {
        row.style.display = "";
        visibleCount++;
      } else {
        row.style.display = "none";
      }
    });

    if (countBadge) {
      countBadge.textContent = `${visibleCount} of ${tableRows.length} models showing`;
    }

    notifyParentOfHeight();
  }

  if (searchInput) {
    searchInput.addEventListener("input", function (e) {
      searchQuery = e.target.value.trim().toLowerCase();
      applyFilters();
    });
  }

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      filterBtns.forEach((b) => b.classList.remove("active"));
      this.classList.add("active");
      activeCategory = this.getAttribute("data-filter") || "all";
      applyFilters();
    });
  });
}

/**
 * AI Survey Form (survey.html) validation, reset, and submission summary
 */
function initSurveyForm() {
  const form = document.getElementById("aiSurveyForm");
  const resultCard = document.getElementById("surveyResultCard");
  const summaryBody = document.getElementById("summaryTableBody");

  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // 1. Gather values
    const name = document.getElementById("studentName").value.trim();
    const email = document.getElementById("studentEmail").value.trim();
    const model = document.getElementById("favModel").value;
    const useCase = document.getElementById("primaryUseCase").value;
    const comments = document.getElementById("surveyComments").value.trim() || "None provided";

    const expRadio = form.querySelector('input[name="experience"]:checked');
    const expVal = expRadio ? expRadio.value : "Not specified";

    const capabilityCheckboxes = form.querySelectorAll('input[name="capabilities"]:checked');
    const capabilities = Array.from(capabilityCheckboxes).map((cb) => cb.value);

    // 2. Client-side validation checks
    if (!name || name.length < 2) {
      alert("Please enter a valid student name (at least 2 characters).");
      document.getElementById("studentName").focus();
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
      alert("Please enter a valid university or personal email address.");
      document.getElementById("studentEmail").focus();
      return;
    }

    if (!model) {
      alert("Please select your preferred Frontier AI Model.");
      document.getElementById("favModel").focus();
      return;
    }

    if (!useCase) {
      alert("Please select your primary AI use case.");
      document.getElementById("primaryUseCase").focus();
      return;
    }

    if (!expRadio) {
      alert("Please select your experience level.");
      return;
    }

    if (capabilities.length === 0) {
      alert("Please select at least one preferred capability (e.g., Code Generation).");
      return;
    }

    // 3. Render submission summary
    if (summaryBody) {
      summaryBody.innerHTML = `
        <tr><td>Student Name:</td><td><strong>${escapeHtml(name)}</strong></td></tr>
        <tr><td>Email Address:</td><td>${escapeHtml(email)}</td></tr>
        <tr><td>Favorite Model:</td><td><span class="tag">${escapeHtml(model)}</span></td></tr>
        <tr><td>Primary Use Case:</td><td>${escapeHtml(useCase)}</td></tr>
        <tr><td>Experience Level:</td><td>${escapeHtml(expVal)}</td></tr>
        <tr><td>Desired Capabilities:</td><td>${capabilities.map(c => `<span class="tag">${escapeHtml(c)}</span>`).join(" ")}</td></tr>
        <tr><td>Feedback / Notes:</td><td><em>"${escapeHtml(comments)}"</em></td></tr>
        <tr><td>Submission Status:</td><td><span style="color:#10b981; font-weight:600;">✓ Verified Valid (Client-Side)</span></td></tr>
      `;
    }

    if (resultCard) {
      resultCard.style.display = "block";
      resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    // Optional local demonstration tally
    try {
      const tally = Number(localStorage.getItem("atlas_survey_tally") || "0") + 1;
      localStorage.setItem("atlas_survey_tally", tally.toString());
      console.log(`Local survey submission count: ${tally}`);
    } catch (_) {
      // LocalStorage optional fallback
    }

    notifyParentOfHeight();
  });

  // Reset button behavior
  form.addEventListener("reset", function () {
    if (resultCard) {
      resultCard.style.display = "none";
    }
    notifyParentOfHeight();
  });
}

/**
 * Utility: Safe HTML Escaping for rendered form feedback
 */
function escapeHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
