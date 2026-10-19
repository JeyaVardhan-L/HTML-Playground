# Web Application Frameworks (WAF) — Lab Assignment 2
## FRONTIER AI ATLAS: Exploring the Intelligence Frontier

**Student:** Jey (Roll No: 9057)  
**Department:** Computer Science & Engineering, GITAM University  
**Subject:** Web Application Frameworks (WAF) Lab  
**Assignment:** Lab Assignment 2 — Responsive Dynamic Web Page with Frames, Tables, and Forms  

---

## 1. Project Objective

The objective of this assignment is to design, implement, and deploy a responsive, dynamic multi-page web application using **HTML5**, **CSS3**, and **Vanilla JavaScript** that demonstrates core web fundamentals:
1. **Modern Frames:** Creating a parent layout with an embedded `<iframe>` named `content` and navigating internal subpages without full page reloads using the `target` attribute.
2. **Semantic Hierarchy:** Structuring documents using semantic HTML5 elements: `<header>`, `<footer>`, `<nav>`, `<aside>`, `<main>`, `<section>`, and `<article>`.
3. **Tabular Forms:** Implementing a user survey form formatted inside an HTML `<table>` with diverse form controls (text, email, dropdowns, radio groups, checkboxes, textarea, submit, and reset) and client-side validation.
4. **Hyperlinks:** Establishing internal frame targeting, intra-page navigation, and secure external links with `rel="noopener noreferrer"`.
5. **CSS Properties & Aesthetics:** Developing a cohesive, modern dark-technology dashboard aesthetic utilizing CSS custom properties, Flexbox, CSS Grid, Glassmorphism, glowing accents, and micro-interactions.
6. **Responsive Web Design:** Adapting fluidly across desktop (1440px), laptop (1024px), tablet (768px), and mobile (480px / 320px) viewports with responsive iframe sizing and a mobile sidebar drawer.

---

## 2. Technology Stack

- **Markup:** HTML5 (Standard Semantic Elements, Form Controls, Accessible Tables, Iframes)
- **Styling:** CSS3 (Custom Properties, Flexbox, CSS Grid, Media Queries, Transitions, Pseudo-elements)
- **Scripting:** Vanilla ECMAScript (DOM Manipulation, Event Listeners, Dynamic Iframe Resizing, Filter/Search, Form Validation)
- **Typography:** Google Fonts (`Outfit` for headings, `Inter` for body, `JetBrains Mono` for code)
- **Assets:** Original, resolution-independent SVG vector graphics authored locally
- **Server Runtime:** Any lightweight HTTP server (e.g., Python `http.server` or Node `http-server`)

*Zero external build dependencies, zero frameworks (no React/Angular/Vue), zero external CSS libraries (no Bootstrap/Tailwind).*

---

## 3. Directory Layout

```
Assignment-2/
├── index.html               ← Master Dashboard parent layout with top nav, sidebar, footer & named iframe
├── home.html                ← Landing page with hero, KPI stats, model cards grid & research spotlight
├── models.html              ← Model Explorer comparison matrix using a real HTML table with live search/filter
├── survey.html              ← AI developer survey form formatted inside an HTML table with validation & summary
├── articles.html            ← Deep-dive educational articles utilizing semantic <section> and <article> tags
├── resources.html           ← Assignment compliance matrix, official documentation links & viva preparation
├── css/
│   └── style.css            ← Master stylesheet with variables, resets, flexbox/grid layouts, and media queries
├── js/
│   └── script.js            ← Iframe height sync, active link detection, table filtering & form validation
├── assets/                  ← Locally crafted vector SVG logos and illustrations
│   ├── atlas-logo.svg       ← Frontier AI Atlas orbital brand logo
│   ├── hero-illustration.svg← Neural network synaptic layers and token flow diagram
│   ├── deepmind.svg         ← Google DeepMind / Gemini star mark
│   ├── anthropic.svg        ← Anthropic terracotta geometric emblem
│   ├── openai.svg           ← OpenAI green spiral icon
│   ├── meta.svg             ← Meta AI infinity loop
│   ├── xai.svg              ← xAI minimalist geometric mark
│   ├── deepseek.svg         ← DeepSeek ocean fin / whale emblem
│   ├── mistral.svg          ← Mistral AI stepped pixel mark
│   └── qwen.svg             ← Alibaba Qwen prism polygon
└── README.md                ← This comprehensive documentation and viva guide
```

---

## 4. How to Run the Website Locally

Because modern web browsers enforce strict security rules (CORS and origin restrictions) on `iframe` communication and local files, it is recommended to run the project via a local HTTP server:

### Option A: Using Python (Recommended)
Open a terminal in the project directory:
```bash
# Navigate to Assignment-2
cd Assignment-2

# Launch Python 3 built-in HTTP server
python -m http.server 8000
```
Open your browser and navigate to:
```
http://localhost:8000
```

### Option B: Using Node.js `npx serve`
```bash
cd Assignment-2
npx serve -l 8000 .
```

### Option C: Direct File Opening (Fallback)
You can double-click `index.html` to open it in your browser (`file:///.../Assignment-2/index.html`). Basic iframe navigation functions directly; however, local HTTP serving provides the smoothest iframe height synchronization.

---

## 5. Faculty Requirements to File Mapping

| Faculty Requirement | Curriculum Objective | Primary File(s) | Implementation Details |
| :--- | :--- | :--- | :--- |
| **1. Create Frames** | Multi-window embedded view | `index.html`, `style.css`, `script.js` | `<iframe src="home.html" name="content" id="content-frame">` embedded in parent. Sidebar links target `target="content"`. |
| **2. Header, Footer, Articles as Sections** | Semantic HTML5 structure | `index.html`, `home.html`, `articles.html` | Page structures use `<header role="banner">`, `<footer role="contentinfo">`, `<section>`, and `<article>` wrappers. |
| **3. Form Creation in Tabular Format** | HTML forms in tables | `survey.html`, `style.css`, `script.js` | `<table class="form-table">` where `<tr>` houses labels and inputs (text, email, select, radio, checkbox, textarea). |
| **4. Hyperlinks** | Internal and external navigation | All HTML pages | Internal `target="content"` routing, intra-page anchor links, and external links with `target="_blank" rel="noopener noreferrer"`. |
| **5. Adding CSS Properties** | Modern web aesthetics | `css/style.css` | CSS Custom Properties (`--bg-primary`, etc.), Flexbox, 2D CSS Grid, Glassmorphism, animations, and transitions. |
| **6. Responsive Design** | Multi-device adaptation | `css/style.css`, `js/script.js` | Media queries for 1024px, 768px, and 480px. Collapsible mobile drawer and auto-resizing iframe height. |

---

## 6. Page-by-Page Feature Tour

### Page A: Master Dashboard (`index.html`)
- **Top Navigation:** Brand logo, title, real-time "SYSTEM ONLINE" indicator, and mobile hamburger button (`#mobileToggle`).
- **Sidebar (`<aside class="sidebar">`):** Navigation links to all subpages with distinct emoji icons. Includes an academic meta card showing student name and roll number.
- **Named Frame:** `<iframe name="content">` loads `home.html` initially and seamlessly switches views when navigation links are clicked.
- **Footer:** Academic disclaimer and technical tag badges.

### Page B: Home Portal (`home.html`)
- **Hero Section:** High-impact banner with gradient typography and a locally authored SVG neural network diagram.
- **KPI Metrics:** Four stat cards highlighting global labs, 2M+ token contexts, test-time reasoning compute, and omni-modal inputs.
- **Model Family Cards:** Eight cards featuring Google Gemini, Anthropic Claude, OpenAI GPT/o-series, Meta Llama, DeepSeek, xAI Grok, Mistral, and Alibaba Qwen.
- **Research Spotlight:** Semantic `<article>` explaining the paradigm shift from next-token prediction to test-time reasoning.

### Page C: Model Explorer (`models.html`)
- **HTML Comparison Table:** Accessible table comparing 8 frontier models across Lead Lab, Context Size, Modalities, Strengths, Access Category, and Documentation.
- **Live Search & Filter:** Instant JavaScript search input (`#modelSearch`) and category buttons (Reasoning, Multimodal, Open Weights, Coding).
- **Responsive Wrapper:** `.table-responsive` enables smooth horizontal scrolling on touch devices.

### Page D: AI Developer Survey (`survey.html`)
- **Tabular Form Layout:** Strictly formatted using `<table class="form-table">`.
- **Form Controls:** Text input (Name), Email input, Select dropdowns (Model, Use Case), Radio buttons (Experience Level), Checkboxes (Key Capabilities), Textarea (Feedback), Submit and Reset buttons.
- **Validation & Dynamic Summary:** Intercepts submission via `e.preventDefault()`, validates required fields and email regex, and generates a formatted results table card without reloading the page.

### Page E: AI Articles (`articles.html`)
- **Five In-Depth Technical Essays:**
  1. *What Defines a Frontier AI Model?*
  2. *Test-Time Compute & Chain-of-Thought Reasoning*
  3. *Native Multimodality: Unified Audio, Vision, and Video Tokens*
  4. *Autonomous Agents: Tool Use, Computer Use, and MCP*
  5. *Critical Limitations: Hallucinations, Sycophancy, and Context Decay*
- Every essay is enclosed in an `<article>` with its own `<header>` and contextual callouts.

### Page F: Resources & Viva Prep (`resources.html`)
- **Faculty Compliance Matrix:** Complete audit checklist of all six requirements.
- **Viva Voce Cheat Sheet:** Eight thoroughly explained questions covering frames, semantics, tables, CSS, and responsiveness.
- **Verified References:** Direct hyperlinks to official documentation from Google DeepMind, Anthropic, OpenAI, Meta, DeepSeek, and Mistral.

---

## 7. Viva Voce Examination Cheat Sheet

Prepare these concise answers before demonstrating your lab assignment:

### 1. What is the difference between `<frameset>` and `<iframe>`?
> *`<frameset>` is an obsolete HTML4 element that divided the entire browser window into grid frames. It was deprecated and removed in HTML5 because it broke browser history, search engine indexing, and mobile responsiveness. `<iframe>` (inline frame) is the modern, standards-compliant element that embeds an external HTML page seamlessly inside a regular webpage layout.*

### 2. How do hyperlinks target an iframe?
> *By giving the `<iframe>` a `name` attribute (e.g., `<iframe name="content">`), any anchor tag on the page can target it using `<a href="page.html" target="content">`. When clicked, the browser loads `page.html` inside the frame without refreshing the parent window.*

### 3. Why are semantic HTML5 tags better than generic `<div>` tags?
> *Semantic elements like `<header>`, `<nav>`, `<main>`, `<aside>`, `<section>`, `<article>`, and `<footer>` give meaning to document structure. They improve accessibility for screen readers, enable better SEO indexing by search engines, and make code maintainable.*

### 4. What is the difference between `<section>` and `<article>`?
> *An `<article>` is a self-contained, independent piece of content that could stand alone (e.g., a blog post, news story, or model review). A `<section>` is a thematic grouping of related content, typically accompanied by a heading.*

### 5. How do you make a table-based form responsive?
> *On desktop screens, standard `display: table` and `display: table-cell` keep labels and inputs aligned. On mobile viewports (e.g., `@media (max-width: 768px)`), CSS rules convert `<td>` elements to `display: block`, stacking labels neatly above input fields so they fit narrow screens without horizontal overflow.*

### 6. What is the difference between Flexbox and CSS Grid?
> *Flexbox is **one-dimensional**—it arranges elements along a single axis (either row or column), making it ideal for toolbars, navigation bars, and buttons. CSS Grid is **two-dimensional**—it defines rows and columns simultaneously, making it ideal for complex card grids and dashboard layouts.*

### 7. Why should external links have `rel="noopener noreferrer"`?
> *When opening links in a new tab (`target="_blank"`), the target page gains a JavaScript reference to `window.opener`. Adding `rel="noopener"` severs this reference, protecting the referring page from reverse tabnabbing security exploits. `noreferrer` additionally prevents leaking the HTTP referer header.*

### 8. What does `event.preventDefault()` do in form submission?
> *By default, submitting an HTML form sends an HTTP POST/GET request and reloads the webpage. Calling `event.preventDefault()` stops this default reload, allowing client-side JavaScript to validate the inputs, display instant feedback, and update the UI smoothly.*

---

## 8. Academic Integrity & Sources

- **Official AI Research & Documentation:**
  - Google DeepMind Gemini: [https://ai.google.dev/](https://ai.google.dev/)
  - Anthropic Claude: [https://docs.anthropic.com/](https://docs.anthropic.com/)
  - OpenAI Platform: [https://platform.openai.com/docs](https://platform.openai.com/docs)
  - Meta AI Llama: [https://llama.meta.com/](https://llama.meta.com/)
  - DeepSeek AI: [https://github.com/deepseek-ai](https://github.com/deepseek-ai)
  - Mistral AI: [https://docs.mistral.ai/](https://docs.mistral.ai/)
  - Alibaba Cloud Qwen: [https://qwenlm.github.io/](https://qwenlm.github.io/)
- **Visual Assets:**
  - All SVG graphics (`atlas-logo.svg`, `hero-illustration.svg`, lab logos) were authored locally in standard SVG vector markup specifically for this project.
  - Zero copyrighted stock imagery or unauthorized commercial assets are used.
