import React, { Component } from "react";

/**
 * Practical 3 — React Class Component
 *
 * Demonstrates:
 * 1. Defining a component using an ES6 JavaScript class: `class ClassStudent extends Component`.
 * 2. Implementing the required `render()` method that returns JSX.
 * 3. Initializing state in the constructor: `this.state = { ... }`.
 * 4. The difference between legacy class components and modern function components.
 */
class ClassStudent extends Component {
  constructor(props) {
    super(props);
    // In class components, state is defined as an object in the constructor
    this.state = {
      studentName: "Jey (Roll 9057)",
      branch: "Computer Science & Engineering",
      semester: "Semester 5 (3rd Year)",
      bio: "Undergraduate student passionate about cloud systems, full-stack frameworks, and frontier artificial intelligence."
    };
  }

  // Every React class component MUST implement a render() method
  render() {
    return (
      <div className="practical-card">
        <div className="practical-card-header">
          <div className="card-title-group">
            <h2>
              <span className="practical-pill">Practical 3</span>
              React Class Component
            </h2>
          </div>
        </div>

        <div className="explanation-banner">
          <strong>Class Components vs. Function Components:</strong>
          <p style={{ marginTop: "4px" }}>
            A <strong>Class Component</strong> extends <code>React.Component</code> and requires a <code>render()</code> method to return JSX. Before React 16.8 (when Hooks were introduced), class components were the only way to manage state. Today, modern React prefers function components with hooks because they are simpler and more concise.
          </p>
        </div>

        <div className="demo-box">
          <div className="student-badge-card" style={{ maxWidth: "480px", margin: "0 auto" }}>
            <h3 style={{ color: "#3730a3" }}>🎓 Student Profile (Class Component)</h3>
            <div className="student-prop-row">
              <strong>Name:</strong> <span>{this.state.studentName}</span>
            </div>
            <div className="student-prop-row">
              <strong>Branch:</strong> <span>{this.state.branch}</span>
            </div>
            <div className="student-prop-row">
              <strong>Semester:</strong> <span>{this.state.semester}</span>
            </div>
            <div className="student-prop-row" style={{ marginTop: "10px", fontStyle: "italic", color: "#475569" }}>
              "{this.state.bio}"
            </div>
          </div>
        </div>

        <div className="code-box">
          {`// Class Component Syntax:
class ClassStudent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { studentName: "Jey" };
  }

  render() {
    return <h3>Student: {this.state.studentName}</h3>;
  }
}`}
        </div>
      </div>
    );
  }
}

export default ClassStudent;
