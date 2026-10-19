# Start Here: Your Learning Roadmap

Welcome to the beginner's learning guide for **Frontier AI Atlas**!

This project was built for **Web Application Frameworks (WAF) Lab Assignment 2**. If you look at the codebase and feel a bit overwhelmed by how everything connects, that is completely normal. 

This guide will teach you how your website works from the ground up. You will learn the exact concepts, see the exact lines of code, and understand the reasoning behind every design and technical decision.

---

## 1. What We Built

**Frontier AI Atlas** is a clean, educational reference website that introduces modern Artificial Intelligence foundation models (such as OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, Google Gemini, Meta Llama, DeepSeek, and Mistral).

Visually, it is designed with an **Apple-inspired minimalist grayscale aesthetic**:
- Calm off-white background (`#f5f5f7`)
- Crisp white content cards (`#ffffff`)
- Deep charcoal headings and body text (`#1d1d1f`)
- Native system typography that looks identical to macOS/iOS interfaces
- Subtle 1-pixel borders with smooth rounded corners

Technically, it satisfies all 6 requirements for Lab Assignment 2:
1. **Frames / Iframes**: An outer shell (`index.html`) hosting a named `<iframe>` (`name="content"`) that loads pages without a full browser reload.
2. **Semantic Structure**: Proper HTML5 tags (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`).
3. **Tabular Form**: A developer survey structured inside an HTML `<table>`.
4. **Hyperlinks**: Internal navigation, standalone detection links, and external documentation references.
5. **Clean CSS**: Modern CSS with custom properties (variables), Flexbox, and CSS Grid.
6. **Responsive Design**: Adapts cleanly across laptop, tablet, and mobile screens.

---

## 2. Technologies Used

This project uses only the **foundational triad of the Web**. There are zero third-party libraries, zero external build tools, and zero npm frameworks:

| Technology | Role in This Project | Analogy |
| :--- | :--- | :--- |
| **HTML5** | Defines the structure and content (headings, tables, inputs, iframe). | The **skeleton** of the building. |
| **CSS3** | Controls colors, fonts, spacing, borders, layout, and responsiveness. | The **interior design & paint**. |
| **Vanilla JavaScript** | Handles interactivity (table search, form validation, iframe auto-height). | The **electrical wiring & sensors**. |

---

## 3. How the Files Fit Together

Here is an architectural map of how `index.html` orchestrates the entire website:

```text
+-----------------------------------------------------------------------------------+
|  BROWSER WINDOW                                                                   |
|                                                                                   |
|  index.html (Parent Shell)                                                       |
|  +-----------------------------------------------------------------------------+  |
|  | <header class="site-header">                                                |  |
|  |   [Brand: Frontier AI Atlas]       [Nav: Home | Models | Survey | ... ]     |  |
|  +-----------------------------------------------------------------------------+  |
|  |                                                                             |  |
|  |  <main class="content-viewport">                                            |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | <iframe name="content" src="home.html">                               |  |  |
|  |  |                                                                       |  |  |
|  |  |   Swaps between 5 subpages inside this frame:                         |  |  |
|  |  |     * home.html       (6 model cards + introductory article)          |  |  |
|  |  |     * models.html     (4-column comparison table + live search)       |  |  |
|  |  |     * survey.html     (tabular developer survey + summary card)       |  |  |
|  |  |     * articles.html   (5 educational articles as semantic sections)   |  |  |
|  |  |     * resources.html  (checklist, viva guide, documentation links)    |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |                                                                             |  |
|  +-----------------------------------------------------------------------------+  |
|  | <footer class="site-footer">                                                |  |
|  |   [Student Info: Jey (9057) · GITAM University]                             |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
            |                                                      |
            v                                                      v
     css/style.css                                            js/script.js
   (Shared design tokens,                                  (Iframe auto-height,
   grid, table & form styles)                             search filter, validation)
```

### The Key Architectural Insight: The Named Iframe Pattern
When you click **"Models"** in the top navigation bar:
1. The link has `href="models.html"` and `target="content"`.
2. The browser spots `target="content"` and looks for an iframe whose `name` attribute is `"content"`.
3. It loads `models.html` **inside that iframe**.
4. The parent page (`index.html`), including the header, logo, navigation buttons, and footer, **never reloads or blinks**.

---

## 4. What You Should Learn First

Before diving into lines of code, grasp these three foundational ideas:

1. **HTML is just labeled boxes**: Every tag `<tag>` tells the browser what kind of content sits inside it. An `<h1>` is a primary heading; a `<table>` is tabular data; a `<button>` is an interactive click target.
2. **CSS styles those boxes from the outside in**: CSS selects an HTML box (by tag, class, or id) and sets properties like width, background color, padding, and text size.
3. **The browser does most things automatically**: The browser already knows how to render links, submit forms, and display tables. JavaScript is only added when we want custom behavior that HTML and CSS cannot do on their own (like live filtering a table as you type).

---

## 5. Recommended Reading Order

Read the guides in this exact sequence to build your confidence step by step:

```text
1. START-HERE.md          <-- You are here
       |
       v
2. HTML-FROM-ZERO.md      <-- Master tags, semantic layout, tables, forms, and iframes
       |
       v
3. CSS-FROM-ZERO.md       <-- Understand classes, the Box Model, variables, Flexbox & Grid
       |
       v
4. JAVASCRIPT-FROM-ZERO.md<-- Learn DOM events, querySelector, table filter, and validation
       |
       v
5. CODE-TOUR.md           <-- File-by-file walkthrough of all 8 project files
       |
       v
6. TRACE-ONE-FEATURE.md   <-- Step-by-step trace of 3 real user interactions
       |
       v
7. HANDS-ON-EXERCISES.md  <-- 10 guided coding exercises (easy to advanced)
       |
       v
8. VIVA-PREP.md           <-- 15 high-yield exam questions with concise model answers
       |
       v
9. GLOSSARY.md            <-- Quick reference for web development terminology
```

---

## 6. What You Will Be Able to Explain by the End

By the time you finish working through these guides, you will be able to answer any lab examiner or faculty member with complete clarity:

- [x] Why `index.html` uses an `<iframe>` instead of obsolete HTML4 `<frameset>`.
- [x] How the navigation links talk to the iframe using `target="content"`.
- [x] The exact difference between semantic tags (`<header>`, `<main>`, `<article>`) and generic `<div>` tags.
- [x] How `survey.html` wraps form controls inside table rows (`<tr>` and `<td>`).
- [x] How CSS variables in `:root` allow instant site-wide theme adjustments.
- [x] How the media query `@media (max-width: 768px)` transforms desktop tables into mobile-friendly stacked cards.
- [x] How the JavaScript search filter hides and reveals table rows using `row.style.display`.
- [x] Why `event.preventDefault()` is mandatory in single-page form submission.

Let's begin your journey with [HTML-FROM-ZERO.md](HTML-FROM-ZERO.md)!
