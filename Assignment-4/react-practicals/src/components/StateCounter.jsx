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
    <div className="practical-card">
      <div className="practical-card-header">
        <div className="card-title-group">
          <h2>
            <span className="practical-pill">Practical 2</span>
            React State: Increment &amp; Decrement Counter
          </h2>
        </div>
      </div>

      <div className="explanation-banner">
        <strong>What is State in React?</strong>
        <p style={{ marginTop: "4px" }}>
          <strong>State</strong> is a special JavaScript variable managed within a component. Unlike ordinary variables, when state changes using <code>setCount(...)</code>, React automatically re-renders the component so the updated value appears on the screen immediately.
        </p>
      </div>

      <div className="demo-box">
        <div style={{ textAlign: "center", fontSize: "14px", color: "#6b7280" }}>
          Current State Value:
        </div>
        <div className="counter-display" id="stateCounterValue">
          {count}
        </div>

        <div className="counter-controls">
          <button className="btn btn-secondary" onClick={handleDecrement} id="decrementBtn">
            − Decrement
          </button>
          <button className="btn btn-secondary" onClick={handleReset} id="resetCountBtn">
            Reset (0)
          </button>
          <button className="btn btn-primary" onClick={handleIncrement} id="incrementBtn">
            + Increment
          </button>
        </div>
      </div>

      <div className="code-box">
        {`// Core React useState Code:
const [count, setCount] = useState(0);

<button onClick={() => setCount(count + 1)}>+ Increment</button>
<button onClick={() => setCount(count - 1)}>− Decrement</button>`}
      </div>
    </div>
  );
}

export default StateCounter;
