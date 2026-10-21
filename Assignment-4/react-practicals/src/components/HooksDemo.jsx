import React, { useState, useEffect, useRef } from "react";

/**
 * Practical 5 — React Hooks: At Least Three Hooks Demonstration
 *
 * Demonstrates:
 * 1. useState:
 *    - Manages interactive counter state (`clicks`).
 *    - Manages live text input state (`inputText`).
 * 2. useRef:
 *    - Creates a direct reference to a real DOM input node (`inputRef`).
 *    - Allows programmatic focus via `inputRef.current.focus()` without re-rendering.
 * 3. useEffect:
 *    - Performs a "side-effect" by synchronizing `document.title` with the counter state.
 *    - Includes a cleanup function that restores the original title when the component unmounts.
 */
function HooksDemo() {
  // Hook 1: useState
  const [clicks, setClicks] = useState(0);
  const [inputText, setInputText] = useState("React is declarative!");

  // Hook 2: useRef
  // Holds a mutable reference to the DOM input element
  const inputRef = useRef(null);

  // Hook 3: useEffect
  // Runs whenever the 'clicks' state variable changes
  useEffect(() => {
    const originalTitle = document.title;
    document.title = `Clicked ${clicks} times — Hooks Demo`;

    // Cleanup function: runs before next effect execution or when component unmounts
    return () => {
      document.title = originalTitle;
    };
  }, [clicks]); // Dependency array: only re-run effect when 'clicks' changes

  // Function to programmatically focus the input using the ref
  const handleFocusClick = () => {
    if (inputRef.current) {
      inputRef.current.focus();
      // Optional: select text inside the input
      inputRef.current.select();
    }
  };

  return (
    <section className="practical-section">
      <div className="practical-heading">
        <span className="pnum">Practical 5</span>
        <h2>Three Hooks: useState, useRef, useEffect</h2>
      </div>

      <p className="practical-desc">
        React Hooks let function components use state and lifecycle features. The three
        hooks below are demonstrated together in a single component.
      </p>

      {/* Part A: useState + useEffect */}
      <div className="hooks-row">
        <h3>
          Hook 1 &amp; 3 — <code>useState</code> + <code>useEffect</code> (document title)
        </h3>
        <p>
          Clicking the button increments <code>clicks</code> state. The <code>useEffect</code>{" "}
          watches <code>clicks</code> and updates the browser tab title as a side-effect.
        </p>
        <div className="click-line">
          <span className="click-count">Clicks: <span id="hooksClickCount">{clicks}</span></span>
          <button className="btn btn-accent" onClick={() => setClicks(clicks + 1)} id="increaseBtn">
            + Increase
          </button>
          <button className="btn" onClick={() => setClicks(0)}>
            Reset
          </button>
        </div>
        <p style={{ fontSize: "12px", color: "#888", marginTop: "8px" }}>
          Check the browser tab — it reads: "Clicked {clicks} times — Hooks Demo"
        </p>
      </div>

      {/* Part B: useRef */}
      <div className="hooks-row">
        <h3>
          Hook 2 — <code>useRef</code> (direct DOM focus) + <code>useState</code> (text input)
        </h3>
        <p>
          <code>inputRef.current.focus()</code> directly focuses the input element without
          triggering a re-render. The text value is kept in <code>useState</code>.
        </p>
        <div className="input-row">
          <input
            type="text"
            ref={inputRef}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            className="text-input"
            id="hooksTextInput"
            placeholder="Type something here..."
          />
          <button className="btn" onClick={handleFocusClick} id="focusInputBtn">
            Focus Input
          </button>
        </div>
        <div className="live-preview">
          <strong>useState live value:</strong> {inputText || "(empty)"}
        </div>
      </div>

      <pre className="code-box">{`// 1. useState:
const [clicks, setClicks] = useState(0);

// 2. useRef (direct DOM focus):
const inputRef = useRef(null);
inputRef.current.focus();

// 3. useEffect (side-effect on title):
useEffect(() => {
  document.title = \`Clicked \${clicks} times\`;
}, [clicks]);`}</pre>
    </section>
  );
}

export default HooksDemo;
