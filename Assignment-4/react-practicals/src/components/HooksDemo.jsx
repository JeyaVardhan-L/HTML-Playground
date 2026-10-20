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
    <div className="practical-card">
      <div className="practical-card-header">
        <div className="card-title-group">
          <h2>
            <span className="practical-pill">Practical 5</span>
            Three Hooks Demonstration (useState, useRef, useEffect)
          </h2>
        </div>
      </div>

      <div className="explanation-banner">
        <strong>The Three Essential React Hooks:</strong>
        <ul style={{ marginLeft: "18px", marginTop: "6px" }}>
          <li>
            <strong>1. <code>useState</code>:</strong> Stores and updates reactive values (like our click counter and text box value).
          </li>
          <li>
            <strong>2. <code>useRef</code>:</strong> Gives direct access to a DOM node (used to focus the input box on demand without re-rendering).
          </li>
          <li>
            <strong>3. <code>useEffect</code>:</strong> Performs side effects outside React (updating the browser tab title to reflect the click count).
          </li>
        </ul>
      </div>

      <div className="demo-box">
        {/* Hook 1 & 3: Counter + Document Title Effect */}
        <div style={{ marginBottom: "20px" }}>
          <h3 style={{ fontSize: "15px", color: "#1f2937", marginBottom: "6px" }}>
            Part A: <code>useState</code> &amp; <code>useEffect</code> (Document Title Sync)
          </h3>
          <p style={{ fontSize: "13px", color: "#6b7280", marginBottom: "8px" }}>
            Clicking the button updates the <code>clicks</code> state and causes <code>useEffect</code> to update the browser tab's title:
          </p>
          <div style={{ display: "flex", alignItems: "center", gap: "15px" }}>
            <span style={{ fontSize: "16px", fontWeight: 600, color: "#111827" }}>
              Total Clicks: <span id="hooksClickCount">{clicks}</span>
            </span>
            <button className="btn btn-primary" onClick={() => setClicks(clicks + 1)} id="increaseBtn">
              + Increase Counter
            </button>
            <button className="btn btn-secondary" onClick={() => setClicks(0)}>
              Reset
            </button>
          </div>
          <p style={{ fontSize: "12px", color: "#059669", marginTop: "6px" }}>
            Notice the browser tab title: "<em>Clicked {clicks} times — Hooks Demo</em>"
          </p>
        </div>

        <hr style={{ border: "none", borderTop: "1px solid #e2e8f0", margin: "16px 0" }} />

        {/* Hook 1 & 2: Text Input State + useRef Focus */}
        <div>
          <h3 style={{ fontSize: "15px", color: "#1f2937", marginBottom: "6px" }}>
            Part B: <code>useState</code> &amp; <code>useRef</code> (DOM Node Focus)
          </h3>
          <p style={{ fontSize: "13px", color: "#6b7280" }}>
            Clicking "Focus Input" calls <code>inputRef.current.focus()</code> to focus the text field directly:
          </p>
          <div className="hooks-input-group">
            <input
              type="text"
              ref={inputRef}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="text-input"
              id="hooksTextInput"
              placeholder="Type something here..."
            />
            <button className="btn btn-secondary" onClick={handleFocusClick} id="focusInputBtn">
              🔍 Focus Input Box
            </button>
          </div>
          <div className="live-text-preview">
            <strong>useState Live Preview:</strong> {inputText || "(empty)"}
          </div>
        </div>
      </div>

      <div className="code-box">
        {`// 1. useState:
const [clicks, setClicks] = useState(0);

// 2. useRef (direct DOM focus):
const inputRef = useRef(null);
inputRef.current.focus();

// 3. useEffect (side-effect on title):
useEffect(() => {
  document.title = \`Clicked \${clicks} times\`;
}, [clicks]);`}
      </div>
    </div>
  );
}

export default HooksDemo;
