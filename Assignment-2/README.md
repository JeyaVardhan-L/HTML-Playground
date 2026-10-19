# Web Application Frameworks (WAF) — Lab Assignment 2
## FRONTIER AI ATLAS: A Simple Guide to Modern AI Models

**Student:** Jey (Roll No: 9057)  
**Department:** Computer Science & Engineering, GITAM University  
**Subject:** Web Application Frameworks (WAF) Lab  
**Assignment:** Lab Assignment 2 — Minimalist Grayscale Interface (Mac-Inspired UI)  

---

## 1. Project Overview

**Frontier AI Atlas** is an educational reference website exploring leading artificial intelligence foundation models.

The website has been designed with a **clean, minimalist, grayscale interface inspired by Apple's design language** (macOS System Font Stack, white surfaces, light gray backgrounds `#f5f5f7`, dark charcoal text `#1d1d1f`, subtle 1px borders, rounded rectangular cards, and restrained spacing).

### Core Faculty Requirements Implemented:
1. **Frames:** Main page ([index.html](index.html)) contains a named `<iframe>` (`name="content"`) and horizontal navigation links that load subpages inside the frame using `target="content"`.
2. **Semantic Sections & Articles:** Clean document hierarchy utilizing `<header>`, `<main>`, `<section>`, `<article>`, and `<footer>` elements.
3. **Tabular Form:** A developer survey ([survey.html](survey.html)) implemented in a clean `<table>` format with client-side validation, summary feedback, and reset functionality.
4. **Hyperlinks:** Seamless internal frame routing, standalone detection links, and official external documentation links with `target="_blank" rel="noopener noreferrer"`.
5. **CSS Properties:** Grayscale custom properties, flexbox, CSS grid, system typography, subtle borders, and rounded corners without neon colors or glowing effects.
6. **Responsive Design:** Fluid layouts adapting across desktop, tablet, and mobile viewports with horizontal table scrolling and auto-resizing iframes.

---

## 2. Directory Structure

```
Assignment-2/
├── index.html       ← Main layout (compact header, horizontal nav, named iframe, understated footer)
├── home.html        ← Clean 6-card grid introducing leading AI models (OpenAI, Anthropic, DeepMind, Meta, DeepSeek, Mistral)
├── models.html      ← Straightforward 4-column comparison table with live search filter
├── survey.html      ← Tabular survey form (Student Name, Email, Model, Use Case, Radios, Checkboxes, Feedback)
├── articles.html    ← Semantic articles exploring scale, reasoning, multimodality, agents, and limitations
├── resources.html   ← Assignment compliance matrix, official documentation links, and lab viva guide
├── css/
│   └── style.css    ← Unified minimalist Mac-inspired stylesheet (light gray, white, system font stack)
├── js/
│   └── script.js    ← Simple JavaScript for iframe auto-resizing, search filtering, and form validation
└── README.md        ← Project documentation and viva voce study guide
```

---

## 3. How to Run Locally

Run the website using Python's built-in HTTP server:

```powershell
# Navigate to the assignment folder
cd Assignment-2

# Start the server on port 8000
python -m http.server 8000
```

Open your browser and navigate to:
```
http://localhost:8000
```

*(You can also open `index.html` directly in any web browser).*

---

## 4. Requirements Mapping Table

| Requirement | Implementation File | Key Feature / Code Evidence |
| :--- | :--- | :--- |
| **1. Create Frames** | `index.html` | `<iframe src="home.html" name="content" id="content-frame">` with navigation `<a href="..." target="content">`. |
| **2. Header, Footer, Articles** | All HTML files | Semantic tags: `<header role="banner">`, `<footer role="contentinfo">`, `<section>`, and `<article class="article-section">`. |
| **3. Form in Tabular Format** | `survey.html` | `<table class="form-table">` where `<tr>` structures labels on the left and form controls on the right. |
| **4. Hyperlinks** | All HTML files | Target routing (`target="content"`), standalone redirects (`target="_top"`), and external documentation links (`target="_blank"`). |
| **5. CSS Properties** | `css/style.css` | Grayscale palette (`--background: #f5f5f7; --surface: #ffffff; --border: #d2d2d7;`), Flexbox, CSS Grid, borders, and rounded corners. |
| **6. Responsive Design** | `css/style.css` | Media query `@media (max-width: 768px)` adapting tables, horizontal navigation, and inputs for mobile screens. |

---

## 5. Lab Viva Voce Cheat Sheet

Key questions and answers for lab demonstration:

1. **Why use an `<iframe>` instead of obsolete `<frameset>`?**  
   *`<frameset>` was deprecated and removed in HTML5 because it divided the entire browser window and broke browser history, search engine indexing, and mobile responsiveness. An `<iframe>` (inline frame) embeds external pages cleanly inside normal responsive layouts.*

2. **How does `target="content"` work with iframes?**  
   *When an iframe is given an identifier like `name="content"`, any link with `target="content"` instructs the browser to load that URL inside the frame without refreshing the parent page.*

3. **What is the advantage of semantic HTML5 tags?**  
   *Elements such as `<header>`, `<main>`, `<section>`, `<article>`, and `<footer>` provide structural meaning to web browsers, search engines, and screen-reading assistive technologies.*

4. **How is the tabular form made responsive on mobile?**  
   *On desktop screens, `display: table-cell` keeps labels and inputs aligned. On screens below 768px, media queries change cells to `display: block`, cleanly stacking labels above input boxes.*

5. **What does `event.preventDefault()` do in form submission?**  
   *It prevents the browser's default action of reloading the page upon form submission, allowing JavaScript to validate inputs client-side and display a dynamic summary.*

---

## 6. Official Sources
- OpenAI: [https://platform.openai.com/docs](https://platform.openai.com/docs)
- Anthropic: [https://docs.anthropic.com/](https://docs.anthropic.com/)
- Google DeepMind: [https://ai.google.dev/](https://ai.google.dev/)
- Meta Llama: [https://llama.meta.com/](https://llama.meta.com/)
- DeepSeek AI: [https://github.com/deepseek-ai](https://github.com/deepseek-ai)
- Mistral AI: [https://docs.mistral.ai/](https://docs.mistral.ai/)
