# HTML From Zero: How Frontier AI Atlas is Structured

This guide teaches the HTML foundations behind **Frontier AI Atlas**. Every concept is accompanied by a tiny example and an exact pointer to where it appears in our assignment code.

---

## 1. What is HTML?

**HTML** stands for **HyperText Markup Language**.
- **HyperText**: Text that links to other documents or media (hyperlinks).
- **Markup Language**: A system of annotating text using "tags" so a web browser knows how to structure and present content.

HTML is **not** a programming language. It does not compute math, evaluate loops, or store data in memory. Instead, it describes the **document structure**.

---

## 2. Tags, Elements, and Attributes

Understanding the anatomy of HTML code is simple once you know these three terms:

```text
       Opening Tag              Content              Closing Tag
    +---------------+   +----------------------+   +-------------+
    |               |   |                      |   |             |
    <h1 class="title">  Explore Frontier AI     </h1>
        \___________/
              |
          Attribute (name="value")
```

1. **Tag**: The keyword enclosed in angle brackets, like `<h1>` or `</h1>`.
2. **Element**: The entire package—from opening tag, through content, to closing tag.
3. **Attribute**: Extra configuration placed inside the opening tag, formatted as `name="value"`.

### Void (Self-Closing) Elements
Most HTML elements have an opening and a closing tag. However, elements that cannot hold child text or nested elements do not need a closing tag. These are called **void elements**:
- `<input>` (takes user entry)
- `<meta>` (document metadata)
- `<link>` (links an external resource like CSS)

Where it appears in our code:
- In `index.html`, lines 4-8: `<meta charset="UTF-8">` and `<link rel="stylesheet" href="css/style.css">`.
- In `survey.html`, line 40: `<input type="text" id="studentName" ...>`.

---

## 3. Basic Document Structure

Every HTML page follows a standard boilerplate:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document Title</title>
</head>
<body>
  <p>Visible content goes here.</p>
</body>
</html>
```

| Component | Purpose | Location in Our Project |
| :--- | :--- | :--- |
| `<!DOCTYPE html>` | Informs the browser to render the page using modern HTML5 standards. | Line 1 of all 6 `.html` files |
| `<html lang="en">` | Root container for the entire page, declaring English language. | Line 2 of all 6 `.html` files |
| `<head>` | Holds machine-readable metadata that is **not** rendered directly on the screen. | Lines 3–9 of `index.html` |
| `<body>` | Contains all visible text, graphics, navigation bars, and forms. | Lines 10–59 of `index.html` |

Inside the `<head>` in `index.html`:
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Frontier AI Atlas — A simple guide to modern AI models</title>
<link rel="stylesheet" href="css/style.css">
```
- `charset="UTF-8"`: Enables universal text encoding (accents, symbols, emojis).
- `viewport`: Essential for responsive design; tells mobile browsers to match the screen's native pixel width rather than shrinking a desktop view.
- `<title>`: Appears in the browser tab.
- `<link rel="stylesheet">`: Pulls in our unified CSS rules.

---

## 4. Text, Headings, Links, and Lists

### Headings and Paragraphs
HTML provides six levels of headings, from `<h1>` (most prominent) to `<h6>` (least prominent). Good accessibility requires using a single `<h1>` per page as the primary headline:

```html
<!-- Example from home.html (lines 20-23) -->
<h1 class="page-title">Explore Frontier AI</h1>
<p class="page-description">
  Frontier artificial intelligence refers to large-scale foundation models...
</p>
```

### Links (`<a>`)
The anchor element creates hyperlinks via the `href` (Hypertext Reference) attribute:
- **Internal link**: `<a href="models.html">Models</a>`
- **External link**: `<a href="https://ai.google.dev/" target="_blank" rel="noopener noreferrer">ai.google.dev ↗</a>`

> [!NOTE]
> When opening an external site in a new tab (`target="_blank"`), always include `rel="noopener noreferrer"`. This prevents the opened page from hijacking the referring page via JavaScript.

### Lists (`<ul>` and `<li>`)
Unordered lists group related bullet points:
```html
<!-- Example from articles.html (lines 43-46) -->
<ul>
  <li><strong>Pre-training:</strong> Ingesting massive datasets using self-supervised learning...</li>
  <li><strong>Post-training:</strong> Supervised Fine-Tuning (SFT) and RLHF/RLAIF...</li>
</ul>
```

---

## 5. Semantic Layout Elements

Older websites used generic `<div>` (division) tags for everything. HTML5 introduced **semantic elements**—tags whose names explain their purpose to developers, browsers, search engines, and screen readers.

```text
+-------------------------------------------------------+
|  <header>               (Logo, Title, Nav)            |
+-------------------------------------------------------+
|  <nav>                  (Navigation links)            |
+-------------------------------------------------------+
|  <main>                                               |
|    +-----------------------------------------------+  |
|    | <section>          (A thematic group)         |  |
|    |   +-----------------------------------------+ |  |
|    |   | <article>      (Self-contained content) | |  |
|    |   +-----------------------------------------+ |  |
|    +-----------------------------------------------+  |
+-------------------------------------------------------+
|  <footer>               (Copyright, Student info)     |
+-------------------------------------------------------+
```

Here is how Frontier AI Atlas uses them:

| Semantic Tag | Meaning | Exact Location in Code |
| :--- | :--- | :--- |
| `<header>` | Introductory banner or title region. | `index.html` (line 14), `home.html` (line 19), `articles.html` (line 32) |
| `<nav>` | Section containing major site navigation links. | `index.html` (line 21) |
| `<main>` | The primary, unique content of the document. | `index.html` (line 32), `articles.html` (line 27) |
| `<section>` | A thematic grouping of content, often with an aria-label. | `home.html` (line 27), `models.html` (line 27), `articles.html` (line 30) |
| `<article>` | Independent, distributable entry (cards or articles). | `home.html` (line 31 for model cards), `articles.html` (line 31) |
| `<footer>` | Closing information, metadata, or copyright. | `index.html` (line 45), `home.html` (line 136) |

---

## 6. Tables: Rows, Headers, and Cells

Tables organize data into a 2D grid of rows and columns. They should be used for **tabular data**, never for general page layouts.

An HTML table is built from these core elements:
- `<table>`: The wrapper.
- `<thead>`: The header section.
- `<tbody>`: The body data section.
- `<tr>`: Table Row.
- `<th>`: Table Header cell (bold and centered by default). Uses `scope="col"` for screen readers.
- `<td>`: Table Data cell (standard text cell).

### Where it appears: `models.html` (lines 41–56)
```html
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
    <tr>
      <td>OpenAI</td>
      <td>GPT-4o &amp; o1 / o3-mini</td>
      <td>Deliberate chain-of-thought reasoning...</td>
      <td><a href="https://platform.openai.com/docs" target="_blank" rel="noopener noreferrer">platform.openai.com ↗</a></td>
    </tr>
    <!-- More rows follow -->
  </tbody>
</table>
```

---

## 7. Forms in Tabular Format

Requirement 3 specifies: *"Form created in tabular format"*. In `survey.html`, an HTML `<form>` wraps an HTML `<table>`. Each row (`<tr>`) places the field's `<label>` in the left cell and the interactive `<input>` in the right cell.

```text
<tr>
  <td class="form-label-cell">  <label for="studentName">Student Name *</label>  </td>
  <td class="form-input-cell">  <input type="text" id="studentName" ...>        </td>
</tr>
```

### Form Elements Used in `survey.html`:
1. **`<label>`**: Accessible name for an input. Its `for` attribute must match the input's `id`.
   ```html
   <label for="studentEmail">Email Address *</label>
   ```
2. **Text & Email Inputs**:
   ```html
   <input type="text" id="studentName" name="studentName" required>
   <input type="email" id="studentEmail" name="studentEmail" required>
   ```
3. **Dropdown Selection (`<select>` and `<option>`)**:
   ```html
   <select id="favModel" name="favModel" required>
     <option value="">-- Select a model --</option>
     <option value="Anthropic Claude 3.5 Sonnet">Anthropic Claude 3.5 Sonnet</option>
     <option value="Google Gemini 1.5/2.0">Google Gemini 1.5 / 2.0</option>
   </select>
   ```
4. **Radio Buttons (`type="radio"`)**: Used for single selection from mutually exclusive choices. All radios in the group share the same `name`:
   ```html
   <input type="radio" name="experience" value="Beginner" required>
   <input type="radio" name="experience" value="Intermediate">
   <input type="radio" name="experience" value="Advanced">
   ```
5. **Checkboxes (`type="checkbox"`)**: Used for multiple independent selections:
   ```html
   <input type="checkbox" name="capabilities" value="Code Generation" checked>
   <input type="checkbox" name="capabilities" value="Long Context (1M+)">
   ```
6. **Multi-line Text (`<textarea>`)**:
   ```html
   <textarea id="surveyComments" name="surveyComments"></textarea>
   ```
7. **Action Buttons**:
   ```html
   <button type="submit" class="btn btn-primary">Submit Survey</button>
   <button type="reset" class="btn btn-secondary">Reset</button>
   ```

---

## 8. Frames vs. Iframes

In web history, there are two ways to split a window into separate documents:

### The Obsolete HTML4 Way: `<frameset>` and `<frame>`
In the late 1990s, HTML allowed splitting the browser window into a grid of distinct frames using `<frameset>`.
- **Why it died**: It completely replaced the `<body>`, broke browser bookmarking (the URL bar never updated), was disastrous for search engines, and failed on mobile devices.
- **Status**: **Removed from HTML5**. Do not use `<frameset>`.

### The Modern HTML5 Way: `<iframe>` (Inline Frame)
An `<iframe>` is an element placed **inside a normal `<body>`**, living alongside other regular HTML elements.
- It acts like an embedded browser window inside the page.
- It honors CSS positioning, Flexbox, border-radius, and media queries.
- **Status**: Standard HTML5 element.

---

## 9. How `target="content"` Works in Our Project

In `index.html`, lines 33–41 define our named iframe:

```html
<iframe 
  src="home.html" 
  name="content" 
  id="content-frame" 
  title="Frontier AI Atlas Content" 
  class="content-frame"
>
  <p>Your browser does not support iframes.</p>
</iframe>
```

Notice the attribute:
```html
name="content"
```

Now look at the navigation bar links in `index.html`, lines 22–26:
```html
<nav class="main-nav">
  <a href="home.html" target="content" class="nav-link active">Home</a>
  <a href="models.html" target="content" class="nav-link">Models</a>
  <a href="survey.html" target="content" class="nav-link">Survey</a>
  <a href="articles.html" target="content" class="nav-link">Articles</a>
  <a href="resources.html" target="content" class="nav-link">Resources</a>
</nav>
```

### The Magic Step-by-Step:
1. You click the link `<a href="models.html" target="content">`.
2. The browser inspects the `target` attribute value (`"content"`).
3. The browser searches the active page for any window or iframe with `name="content"`.
4. It finds `<iframe name="content">`.
5. It requests `models.html` and renders it **inside the iframe**.
6. The outer page (`index.html`), header, brand title, and footer remain completely undisturbed.

You now understand all the HTML fundamentals used in Frontier AI Atlas! Proceed to [CSS-FROM-ZERO.md](CSS-FROM-ZERO.md) to see how we style and lay out these elements.
