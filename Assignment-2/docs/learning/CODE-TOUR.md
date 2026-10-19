# Code Tour: File-by-File Walkthrough

This tour walks through every key file in the **Frontier AI Atlas** project (`Assignment-2/`). For each file, we cover its responsibility, key code snippets, what happens when it loads, what to study carefully, and what you can safely ignore initially.

---

## 1. `index.html` — The Parent Shell

### Responsibility:
Acts as the persistent master frame of the application. It renders the site header, brand identity, horizontal navigation menu, the embedded `<iframe>`, and the site footer.

### Key Elements:
```html
<!-- Line 14: Header with Brand & Navigation -->
<header class="site-header" role="banner">
  <div class="header-inner">
    <div class="brand">
      <span class="brand-title">Frontier AI Atlas</span>
      <span class="brand-subtitle">A simple guide to modern AI models</span>
    </div>
    <nav class="main-nav" role="navigation" aria-label="Main navigation">
      <a href="home.html" target="content" class="nav-link active" id="nav-home">Home</a>
      <a href="models.html" target="content" class="nav-link" id="nav-models">Models</a>
      <a href="survey.html" target="content" class="nav-link" id="nav-survey">Survey</a>
      <a href="articles.html" target="content" class="nav-link" id="nav-articles">Articles</a>
      <a href="resources.html" target="content" class="nav-link" id="nav-resources">Resources</a>
    </nav>
  </div>
</header>

<!-- Line 32: Main viewport holding the named iframe -->
<main class="content-viewport" role="main">
  <iframe src="home.html" name="content" id="content-frame" title="Frontier AI Atlas Content" class="content-frame">
    <p>Your browser does not support iframes.</p>
  </iframe>
</main>
```

### Relationship to Other Files:
- Links to `css/style.css` for styling.
- Loads `home.html` initially inside its iframe via `src="home.html"`.
- Navigation links target `content`, swapping the subpages (`models.html`, `survey.html`, etc.) inside the iframe.
- Loads `js/script.js` to manage active link styling and height adjustments.

### What Happens on Load:
The browser parses `index.html`, paints the header and footer, sees the `<iframe>` with `src="home.html"`, and initiates a second request to fetch and render `home.html` inside the frame.

### What to Study Carefully:
- The pairing of `target="content"` in the links with `name="content"` on the iframe.
- The use of semantic landmark roles (`role="banner"`, `role="main"`, `role="contentinfo"`).

### What You Can Ignore Initially:
- The fallback message inside the `<iframe>` tag (only displayed on ancient browsers from 25 years ago).

---

## 2. `home.html` — The Landing Overview

### Responsibility:
Presents the initial greeting and introduces the 6 leading AI model families via a responsive card grid, followed by an overview article.

### Key Elements:
```html
<!-- Line 28: Clean Grid of 6 Model Cards -->
<div class="cards-grid">
  <!-- Card 1: OpenAI -->
  <article class="model-card">
    <div class="card-top">
      <span class="model-org">OpenAI</span>
      <h2 class="model-title">GPT &amp; o-Series</h2>
      <p class="model-desc">
        Developer of GPT-4o for real-time multimodal interaction and the o1/o3-mini series...
      </p>
    </div>
    <div class="card-bottom">
      <a href="https://platform.openai.com/docs" target="_blank" rel="noopener noreferrer" class="subtle-link">Official documentation →</a>
    </div>
  </article>
  <!-- 5 more articles for Anthropic, Google DeepMind, Meta, DeepSeek, Mistral -->
</div>
```

### Relationship to Other Files:
- Designed to be displayed inside `index.html`'s iframe, but includes a `#standaloneNotice` banner if opened directly in a browser tab.
- Styled by `.cards-grid` and `.model-card` in `css/style.css`.

### What Happens on Load:
Renders 6 `<article>` elements. CSS Grid automatically positions them into 1, 2, or 3 columns depending on the available screen width.

### What to Study Carefully:
- How each card is structured semantically using `<article class="model-card">`.
- How external links use `target="_blank"` and `rel="noopener noreferrer"`.

### What You Can Ignore Initially:
- The specific technical descriptions of each AI model; the HTML structure is what matters for your exam.

---

## 3. `models.html` — The Comparison Matrix

### Responsibility:
Fulfills the lab requirement for tabular data display. Displays a 4-column matrix of model families and provides a real-time search filter.

### Key Elements:
```html
<!-- Line 28: Search input container -->
<div class="search-container">
  <input 
    type="search" 
    id="modelSearch" 
    class="search-field" 
    placeholder="Filter by organization, model, or capability..."
  >
  <span id="matchingCount" class="search-count">Showing 6 models</span>
</div>

<!-- Line 41: Comparison Table -->
<div class="table-wrapper">
  <table class="simple-table" aria-label="Frontier AI Model Comparison">
    <thead>
      <tr>
        <th scope="col">Organization</th>
        <th scope="col">Model Family</th>
        <th scope="col">Primary Capabilities</th>
        <th scope="col">Official Documentation</th>
      </tr>
    </thead>
    <tbody id="modelTableBody">
      <!-- 6 table rows (<tr>) with 4 data cells (<td>) each -->
    </tbody>
  </table>
</div>
```

### Relationship to Other Files:
- JavaScript in `js/script.js` attaches an event listener to `#modelSearch` and searches text inside rows of `#modelTableBody`.
- Styled by `.simple-table` and `.table-wrapper` in `css/style.css`.

### What Happens on Load:
Draws the complete table. `script.js` counts the 6 initial rows and ensures the count display reads `"Showing 6 models"`.

### What to Study Carefully:
- The distinction between table headers (`<th>`) and table data (`<td>`).
- The use of `scope="col"` on header cells for accessibility.

### What You Can Ignore Initially:
- The `aria-label` attributes (they are good practice for accessibility, but not strictly required for basic functionality).

---

## 4. `survey.html` — The Tabular Form

### Responsibility:
Implements Requirement 3: *"Form created in tabular format"*. Collects user preferences and demonstrates client-side form validation and summary generation.

### Key Elements:
```html
<!-- Line 28: Form with novalidate -->
<form id="aiSurveyForm" novalidate>
  <table class="form-table">
    <tbody>
      <tr>
        <td class="form-label-cell">
          <label for="studentName">Student Name *</label>
        </td>
        <td class="form-input-cell">
          <input type="text" id="studentName" name="studentName" required>
        </td>
      </tr>
      <!-- Additional rows for Email, Model Select, Use Case, Radios, Checkboxes, Textarea -->
    </tbody>
  </table>
</form>

<!-- Line 186: Result summary card (hidden until submission) -->
<div id="surveyResultCard" class="result-notice" role="region" aria-live="polite">
  <h3>Survey Submitted Successfully</h3>
  <ul id="summaryList" class="summary-list"></ul>
</div>
```

### Relationship to Other Files:
- Validated and handled by `js/script.js` on form submit.
- Styled by `.form-table`, `.form-card`, and `.result-notice` in `css/style.css`.
- Transformed from desktop table cells to stacked mobile cards via the media query in `style.css`.

### What to Study Carefully:
- How each row (`<tr>`) pairs a label cell (`.form-label-cell`) with an input cell (`.form-input-cell`).
- The matching of `<label for="xxx">` with `<input id="xxx">`.
- How radio buttons share `name="experience"` while checkboxes share `name="capabilities"`.

### What You Can Ignore Initially:
- The `aria-live="polite"` attribute on the result card (this simply alerts screen readers when new text appears).

---

## 5. `articles.html` — Semantic Articles

### Responsibility:
Implements Requirement 2: *"Header, Footer, Articles as sections"*. Displays educational articles on frontier AI architecture and safety.

### Key Elements:
```html
<!-- Line 31: Article wrapped in a thematic Section -->
<section aria-label="What is Frontier AI">
  <article class="article-section">
    <header class="article-header">
      <span class="article-number">Article 1</span>
      <h2 class="article-headline">What Defines a Frontier AI Model?</h2>
    </header>
    <div class="article-body">
      <p>Frontier artificial intelligence refers to foundation models...</p>
      <ul>
        <li><strong>Pre-training:</strong> Ingesting massive datasets...</li>
        <li><strong>Post-training:</strong> Supervised Fine-Tuning (SFT)...</li>
      </ul>
    </div>
  </article>
</section>
```

### What to Study Carefully:
- The nesting hierarchy: `<main>` contains `<section>` tags, which contain `<article>` tags, which contain `<header>` and content blocks.

---

## 6. `resources.html` — Compliance & Viva Cheat Sheet

### Responsibility:
Serves as an in-app laboratory guide, presenting an assignment compliance matrix, viva questions, and verified external links.

### Key Elements:
```html
<!-- Line 32: Assignment Compliance Table -->
<table class="simple-table">
  <thead>
    <tr>
      <th scope="col">Requirement</th>
      <th scope="col">Files</th>
      <th scope="col">Implementation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Frames</strong></td>
      <td><code>index.html</code></td>
      <td>Embedded <code>&lt;iframe name="content"&gt;</code> with links using <code>target="content"</code>.</td>
    </tr>
    <!-- Rows for Requirements 2 through 6 -->
  </tbody>
</table>
```

---

## 7. `css/style.css` — The Design Engine

### Responsibility:
Provides all visual presentation across the entire website.

### Logical Blocks in the File:
1. **Lines 6–25 (`:root`)**: Design tokens (variables for colors, fonts, radiuses, transitions).
2. **Lines 27–72 (Reset & Base)**: `box-sizing: border-box`, typography defaults, link styling.
3. **Lines 74–190 (Shell Layout)**: Layout rules for `index.html` (header, nav, iframe, footer).
4. **Lines 192–232 (Subpage Layout)**: `.page-container`, titles, descriptions, standalone banner.
5. **Lines 235–301 (Card Grid)**: CSS Grid layout for `home.html` model cards.
6. **Lines 303–379 (Table Styles)**: Table borders, header background, hover highlights.
7. **Lines 382–547 (Form Styles)**: Tabular form layout, input borders, buttons, and summary card.
8. **Lines 549–656 (Articles & Resources)**: Styling for semantic articles, info notes, and Q&A items.
9. **Lines 659–693 (Media Queries)**: `@media (max-width: 768px)` adapting layout for mobile devices.

---

## 8. `js/script.js` — The Interactivity Engine

### Responsibility:
Manages DOM interactions, table filtering, form validation, and responsive iframe height.

### Logical Blocks in the File:
1. **Lines 6–9**: `DOMContentLoaded` listener that kicks off initialization.
2. **Lines 14–64 (`initParentNavigation`)**: Highlights active nav links and listens for iframe load events.
3. **Lines 69–86 (Standalone & Height)**: Sends height messages if inside an iframe, or reveals the standalone banner if opened directly.
4. **Lines 89–112 (Search Filter)**: Listens for typing on `#modelSearch` and hides non-matching table rows.
5. **Lines 115–199 (Form Handling)**: Intercepts form submission, validates required fields, formats responses into `#summaryList`, and handles reset.
6. **Lines 202–208 (`escapeText`)**: Protects against HTML injection by escaping `<` and `>` characters.

Now that you've completed the code tour, see how these pieces work together in [TRACE-ONE-FEATURE.md](TRACE-ONE-FEATURE.md)!
