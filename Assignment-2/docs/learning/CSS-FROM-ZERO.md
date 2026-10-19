# CSS From Zero: How Frontier AI Atlas is Styled

This guide explains how **CSS** turns our plain HTML markup into a clean, Apple-inspired, minimalist grayscale user interface. Every rule, property, and concept discussed here comes directly from `css/style.css`.

---

## 1. What is CSS?

**CSS** stands for **Cascading Style Sheets**.
- If HTML is the **skeleton** of the website, CSS is the **skin, clothes, typography, and spacing**.
- "Cascading" means rules cascade from top to bottom; later rules or more specific rules can override earlier ones.

---

## 2. Anatomy of a CSS Rule

Every CSS rule contains a **selector** and a **declaration block**:

```css
/* Example from style.css (lines 207-213) */
.page-title {
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text);
  margin-bottom: 0.35rem;
}
```

- **Selector (`.page-title`)**: Tells the browser *which* HTML elements to target.
- **Property (`font-size`)**: What aspect of the element to modify.
- **Value (`1.8rem`)**: The setting applied to that property.
- **Declaration**: A single `property: value;` statement.

---

## 3. Classes vs. IDs

In HTML, you identify elements using `class="..."` and `id="..."`. CSS selects them differently:

| Selector Type | Syntax | Purpose | Example in Our Code |
| :--- | :--- | :--- | :--- |
| **Element Selector** | `body`, `a`, `h1` | Targets all elements of that HTML tag name. | `body { font-family: var(--font-family); }` (line 40) |
| **Class Selector** | `.classname` (starts with `.`) | Reusable styles applied to multiple elements. | `.model-card` (line 241, shared by all 6 cards) |
| **ID Selector** | `#idname` (starts with `#`) | Unique identifier for a single, specific element. | `#content-frame` (line 15, `script.js`) |

> [!TIP]
> **Best Practice Rule**: In CSS, always prefer **classes** for styling. Reserve **IDs** for unique JavaScript hooks (like `#modelSearch` or `#aiSurveyForm`) and form label pairings (`for="studentName"` matching `id="studentName"`).

---

## 4. How the Stylesheet is Connected

Each HTML file in our project links to `css/style.css` inside its `<head>` tag:

```html
<link rel="stylesheet" href="css/style.css">
```

Because all subpages (`home.html`, `models.html`, etc.) link to the **same** file, any change made to `css/style.css` instantly updates the visual appearance of every single page across the website.

---

## 5. The CSS Box Model

In the browser, **every HTML element is a rectangular box**. That box is composed of four distinct layers, from inside to outside:

```text
+-------------------------------------------------+
|  MARGIN (spacing outside the border)            |
|  +-------------------------------------------+  |
|  |  BORDER (the visible line or outline)     |  |
|  |  +-------------------------------------+  |  |
|  |  |  PADDING (space inside the border)  |  |  |
|  |  |  +-------------------------------+  |  |  |
|  |  |  |  CONTENT (text, image, etc.)  |  |  |  |
|  |  |  +-------------------------------+  |  |  |
|  |  +-------------------------------------+  |  |
|  +-------------------------------------------+  |
+-------------------------------------------------+
```

Let's look at `.model-card` in `style.css` (lines 241–251):
```css
.model-card {
  background-color: var(--surface);     /* Background of the content + padding */
  border: 1px solid var(--border-light);/* The 1px perimeter box line */
  border-radius: var(--radius);         /* Curves the corners of the border */
  padding: 1.25rem;                     /* 20px internal cushion around content */
}
```

### The Crucial Reset: `box-sizing: border-box`
In older CSS, adding padding would make an element wider than its specified `width` (a 200px box with 20px padding became 240px wide!). 

In `style.css` (lines 28–32), we apply this universal reset:
```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```
`box-sizing: border-box` guarantees that `width: 100%` means **100% total width including padding and border**, eliminating horizontal scrollbar glitches.

---

## 6. Design Tokens & Grayscale Theme via CSS Variables

At the top of `style.css` (lines 6–25), we define our design palette inside the `:root` pseudo-class using **CSS Custom Properties (Variables)**:

```css
:root {
  --background: #f5f5f7;        /* Soft off-white page background */
  --surface: #ffffff;           /* Pure white card and header background */
  --surface-secondary: #fbfbfd; /* Muted background for table headers & code */
  --text: #1d1d1f;              /* Deep charcoal primary text */
  --text-secondary: #515154;    /* Medium gray for descriptions and body copy */
  --muted: #86868b;             /* Subtle gray for metadata and captions */
  --border: #d2d2d7;            /* Standard component divider */
  --border-light: #e5e5ea;      /* Very soft divider inside cards and tables */
  --radius: 12px;               /* Standard card corner curvature */
  --radius-sm: 8px;             /* Input and button corner curvature */
  --radius-pill: 999px;         /* Fully rounded pills for navigation links */
  
  --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --font-mono: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
  
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04);
  --shadow-md: 0 3px 10px rgba(0, 0, 0, 0.04);
  --transition: 0.15s ease;
}
```

### Why Use Variables?
Instead of hardcoding `#f5f5f7` or `#1d1d1f` in 50 different places, we write `color: var(--text);`. If you want to change the text color or background later, you change **one variable line in `:root`**, and the entire website updates simultaneously.

### The System Font Stack
Look at `--font-family`. Rather than downloading heavy Google Fonts over the network, it uses the **Native System Font Stack**:
- On macOS/iOS: uses **San Francisco** (`-apple-system, BlinkMacSystemFont`).
- On Windows: uses **Segoe UI**.
- On Android/Linux: uses **Roboto** or **Helvetica**.
This gives the site instant loading speeds and an authentic Mac-inspired aesthetic.

---

## 7. Flexbox: 1-Dimensional Alignment

**Flexbox** (`display: flex`) aligns elements along a single direction (either in a row or in a column).

### Where Flexbox is used in our code:

#### A. Top Header Layout (`style.css`, lines 90–98)
```css
.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}
```
- `display: flex`: Turns the container into a flex container.
- `justify-content: space-between`: Pushes the logo brand to the far left and the navigation links to the far right.
- `align-items: center`: Centers them vertically.
- `gap: 1rem`: Guarantees a minimum 16px space between items.
- `flex-wrap: wrap`: Allows items to wrap onto a second line if the browser window becomes too narrow.

#### B. Survey Action Buttons (`style.css`, lines 476–479)
```css
.form-buttons {
  display: flex;
  gap: 0.75rem;
  padding-top: 0.5rem;
}
```
Places the **"Submit Survey"** button and the **"Reset"** button neatly side by side with a 12px gap.

---

## 8. CSS Grid: 2-Dimensional Layouts

While Flexbox is 1-dimensional, **CSS Grid** (`display: grid`) organizes elements into rows and columns simultaneously.

In `home.html`, the 6 leading AI models are arranged using CSS Grid (`style.css`, lines 235–238):

```css
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
}
```

### Breaking Down this Powerful Rule:
- `grid-template-columns`: Defines how columns are sized.
- `repeat(auto-fit, ...)`: Automatically creates as many columns as will fit across the screen.
- `minmax(260px, 1fr)`: Each column must be **at least 260px wide**, but can expand to take an equal fraction (`1fr`) of any remaining space.
  - On a wide desktop screen: Renders 3 columns of cards.
  - On a tablet: Automatically collapses to 2 columns.
  - On a mobile phone: Automatically stacks into 1 single column.
All of this happens **without writing a single media query**!

---

## 9. Responsive Web Design & Media Queries

A **Media Query** applies CSS rules only when the screen meets a specific condition (such as being smaller than 768px).

In `style.css` (lines 659–693):
```css
@media (max-width: 768px) {
  /* 1. Header wraps vertically on mobile */
  .header-inner {
    flex-direction: column;
    align-items: flex-start;
  }

  /* 2. Navigation takes full width */
  .main-nav {
    width: 100%;
    justify-content: flex-start;
  }

  /* 3. Tabular form adapts into stacked mobile cards */
  .form-table tr {
    display: flex;
    flex-direction: column;
  }

  .form-table td.form-label-cell,
  .form-table td.form-input-cell {
    width: 100%;
    padding: 0.4rem 0;
  }

  .form-table td.form-label-cell {
    padding-top: 0.8rem;
  }
}
```

### How the Tabular Form becomes Responsive:
- On desktop screens: `<tr>` behaves like a table row, showing the label in the left cell and the input in the right cell.
- On screens under 768px: `.form-table tr` switches to `display: flex; flex-direction: column;`. This forces the label cell to sit **directly on top** of the input cell, providing a flawless mobile experience!

---

## 10. How to Safely Customize the Design

If you want to tweak the design without breaking the layout, here are 4 safe edits in `style.css`:

### 1. Change the Page Background
In line 7, change `--background`:
```css
/* Warmer gray / cream */
--background: #f7f6f2;

/* Cooler soft silver */
--background: #f0f2f5;
```

### 2. Change Card Corner Rounding
In line 15, change `--radius`:
```css
/* Modern rounded (default) */
--radius: 12px;

/* Boxy / Brutalist */
--radius: 4px;

/* Extra playful */
--radius: 20px;
```

### 3. Change Card Spacing
In line 238, change the gap in `.cards-grid`:
```css
.cards-grid {
  /* Increase breathing room between model cards */
  gap: 2rem; 
}
```

### 4. Change Base Font Size
In line 34, change the root `html` font size:
```css
html {
  /* Makes all rem-based typography slightly larger */
  font-size: 17px; 
}
```

Now you understand how CSS controls the visual layout of Frontier AI Atlas! Proceed to [JAVASCRIPT-FROM-ZERO.md](JAVASCRIPT-FROM-ZERO.md) to discover how we make the pages interactive.
