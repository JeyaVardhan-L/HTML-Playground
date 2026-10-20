import React, { useState } from "react";

/**
 * Practical 2 — React State: Increment and Decrement
 *
 * Demonstrates:
 * 1. The useState Hook to create and manage local component state.
 * 2. How calling the state setter function triggers React to re-render the UI.
 * 3. Simple event handlers (onClick) connected to buttons.
 */
function StateCounter() {
  // Declare state variable 'count' initialized to 0, and setter function 'setCount'
  const [count, setCount] = useState(0);

  // Handler functions to update state
  const handleIncrement = () => {
    setCount(count + 1);
  };

  const handleDecrement = () => {
    setCount(count - 1);
  };

  const handleReset = () => {
    setCount(0);
  };

  return (
    <section className="practical-section">
      <div className="practical-heading">
        <span className="pnum">Practical 2</span>
        <h2>React State: Increment &amp; Decrement Counter</h2>
      </div>

      <p className="practical-desc">
        <strong>State</strong> is a special variable managed within a component. Unlike ordinary
        variables, when state changes via <code>setCount(...)</code>, React automatically
        re-renders the component so the updated value appears on screen immediately.
      </p>

      <div className="demo-area">
        <span className="counter-label">Current state value</span>
        <div className="counter-value" id="stateCounterValue">{count}</div>

        <div className="counter-controls">
          <button className="btn btn-danger" onClick={handleDecrement} id="decrementBtn">
            − Decrement
          </button>
          <button className="btn" onClick={handleReset} id="resetCountBtn">
            Reset
          </button>
          <button className="btn btn-accent" onClick={handleIncrement} id="incrementBtn">
            + Increment
          </button>
        </div>
      </div>

      <pre className="code-box">{`const [count, setCount] = useState(0);

<button onClick={() => setCount(count + 1)}>+ Increment</button>
<button onClick={() => setCount(count - 1)}>− Decrement</button>
<button onClick={() => setCount(0)}>Reset</button>`}</pre>
    </section>
  );
}

export default StateCounter;
