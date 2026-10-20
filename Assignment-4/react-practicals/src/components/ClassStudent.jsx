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
      <section className="practical-section">
        <div className="practical-heading">
          <span className="pnum">Practical 3</span>
          <h2>React Class Component</h2>
        </div>

        <p className="practical-desc">
          A <strong>Class Component</strong> extends <code>React.Component</code> and requires a{" "}
          <code>render()</code> method to return JSX. Before React 16.8, class components were the
          only way to manage state. Modern React prefers function components with Hooks because
          they are shorter and avoid <code>this</code> binding complexity.
        </p>

        <div className="demo-area">
          <ul className="info-list">
            <li>
              <span className="il-label">Name</span>
              <span className="il-value">{this.state.studentName}</span>
            </li>
            <li>
              <span className="il-label">Branch</span>
              <span className="il-value">{this.state.branch}</span>
            </li>
            <li>
              <span className="il-label">Semester</span>
              <span className="il-value">{this.state.semester}</span>
            </li>
            <li>
              <span className="il-label">Bio</span>
              <span className="il-value">{this.state.bio}</span>
            </li>
          </ul>
        </div>

        <pre className="code-box">{`class ClassStudent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { studentName: "Jey" };
  }

  render() {
    return <h3>Student: {this.state.studentName}</h3>;
  }
}`}</pre>
      </section>
    );
  }
}

export default ClassStudent;
