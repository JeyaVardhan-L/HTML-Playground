/**
 * FRONTIER AI ATLAS — MINIMALIST JAVASCRIPT
 * Simple, readable DOM interactions for WAF Lab Assignment 2
 */

document.addEventListener("DOMContentLoaded", function () {
  initParentNavigation();
  initSubpageFeatures();
});

/**
 * Parent Page (index.html) Navigation & Iframe Resizing
 */
function initParentNavigation() {
  const iframe = document.getElementById("content-frame");
  const navLinks = document.querySelectorAll(".nav-link");

  // Update active navigation link on click
  navLinks.forEach((link) => {
    link.addEventListener("click", function () {
      navLinks.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  // Seamless Iframe Auto-Resize
  if (iframe) {
    function resizeIframe() {
      try {
        if (iframe.contentWindow && iframe.contentWindow.document.body) {
          const doc = iframe.contentWindow.document;
          const height = Math.max(
            doc.body.scrollHeight,
            doc.documentElement.scrollHeight,
            500
          );
          iframe.style.height = height + 30 + "px";

          // Sync active nav tab based on iframe file name
          const path = iframe.contentWindow.location.pathname;
          const currentFile = path.substring(path.lastIndexOf("/") + 1) || "home.html";
          navLinks.forEach((link) => {
            if (link.getAttribute("href") === currentFile) {
              navLinks.forEach((l) => l.classList.remove("active"));
              link.classList.add("active");
            }
          });
        }
      } catch (_) {
        iframe.style.height = "100vh";
      }
    }

    iframe.addEventListener("load", resizeIframe);
    window.addEventListener("resize", resizeIframe);

    window.addEventListener("message", function (event) {
      if (event.data && event.data.type === "ATLAS_RESIZE") {
        iframe.style.height = Math.max(event.data.height, 500) + 30 + "px";
      }
    });
  }
}

/**
 * Subpage Features (Executed in both iframe and standalone modes)
 */
function initSubpageFeatures() {
  // 1. Notify parent frame of content height
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
    setTimeout(sendHeight, 200);
  } else {
    // Show banner if opened directly outside iframe
    const banner = document.getElementById("standaloneNotice");
    if (banner) banner.style.display = "flex";
  }

  // 2. Models Page Search Filter (models.html)
  const searchInput = document.getElementById("modelSearch");
  const tableRows = document.querySelectorAll("#modelTableBody tr");
  const countDisplay = document.getElementById("matchingCount");

  if (searchInput && tableRows.length > 0) {
    searchInput.addEventListener("input", function (e) {
      const query = e.target.value.toLowerCase().trim();
      let matches = 0;

      tableRows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        if (!query || text.includes(query)) {
          row.style.display = "";
          matches++;
        } else {
          row.style.display = "none";
        }
      });

      if (countDisplay) {
        countDisplay.textContent = `Showing ${matches} of ${tableRows.length} models`;
      }
    });
  }

  // 3. Survey Form Validation & Reset (survey.html)
  const surveyForm = document.getElementById("aiSurveyForm");
  const resultCard = document.getElementById("surveyResultCard");
  const summaryList = document.getElementById("summaryList");

  if (surveyForm) {
    surveyForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const name = document.getElementById("studentName").value.trim();
      const email = document.getElementById("studentEmail").value.trim();
      const model = document.getElementById("favModel").value;
      const useCase = document.getElementById("primaryUseCase").value;
      const expRadio = surveyForm.querySelector('input[name="experience"]:checked');
      const comments = document.getElementById("surveyComments").value.trim() || "None";

      const selectedCheckboxes = surveyForm.querySelectorAll('input[name="capabilities"]:checked');
      const capabilities = Array.from(selectedCheckboxes).map((cb) => cb.value);

      // Simple validation checks
      if (!name) {
        alert("Please enter your name.");
        document.getElementById("studentName").focus();
        return;
      }

      if (!email || !email.includes("@")) {
        alert("Please enter a valid email address.");
        document.getElementById("studentEmail").focus();
        return;
      }

      if (!model) {
        alert("Please select your favorite AI model.");
        document.getElementById("favModel").focus();
        return;
      }

      if (!useCase) {
        alert("Please select your primary use case.");
        document.getElementById("primaryUseCase").focus();
        return;
      }

      if (!expRadio) {
        alert("Please select your experience level.");
        return;
      }

      if (capabilities.length === 0) {
        alert("Please select at least one capability of interest.");
        return;
      }

      // Display clean summary
      if (summaryList) {
        summaryList.innerHTML = `
          <li><strong>Student Name:</strong> ${escapeText(name)}</li>
          <li><strong>Email:</strong> ${escapeText(email)}</li>
          <li><strong>Favorite Model:</strong> ${escapeText(model)}</li>
          <li><strong>Primary Use Case:</strong> ${escapeText(useCase)}</li>
          <li><strong>Experience Level:</strong> ${escapeText(expRadio.value)}</li>
          <li><strong>Capabilities:</strong> ${capabilities.map(c => escapeText(c)).join(", ")}</li>
          <li><strong>Comments:</strong> ${escapeText(comments)}</li>
        `;
      }

      if (resultCard) {
        resultCard.style.display = "block";
      }

      // Re-trigger height update after card display
      if (window.self !== window.top) {
        setTimeout(function () {
          const height = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
          window.parent.postMessage({ type: "ATLAS_RESIZE", height: height }, "*");
        }, 100);
      }
    });

    surveyForm.addEventListener("reset", function () {
      if (resultCard) {
        resultCard.style.display = "none";
      }
    });
  }
}

function escapeText(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
