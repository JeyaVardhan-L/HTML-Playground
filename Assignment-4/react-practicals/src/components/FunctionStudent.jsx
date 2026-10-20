import React from "react";

/**
 * Practical 6 — React Function Component
 *
 * Demonstrates:
 * 1. Defining a component as a standard JavaScript function: `function FunctionStudent()`.
 * 2. Returning JSX directly from the function body.
 * 3. Embedding JavaScript expressions inside JSX using curly braces `{}`.
 * 4. Why function components are the standard, modern way to write React components.
 */
function FunctionStudent() {
  // Student data defined within the function scope
  const student = {
    name: "Jey",
    rollNo: "9057",
    branch: "Computer Science & Engineering",
    yearOfStudy: "3rd Year (B.Tech)",
    college: "GITAM School of Technology",
    specialization: "Web Application Frameworks & AI"
  };

  return (
    <section className="practical-section">
      <div className="practical-heading">
        <span className="pnum">Practical 6</span>
        <h2>React Function Component</h2>
      </div>

      <p className="practical-desc">
        In modern React, a <strong>Function Component</strong> is a plain JavaScript function
        that takes optional <code>props</code> as input and returns <strong>JSX</strong>.
        React calls the function and turns the returned JSX into real browser DOM elements.
        Compare this layout with Practical 3 — the displayed data is similar, but the
        implementation uses no class, no constructor, and no <code>this</code>.
      </p>

      <div className="demo-area">
        <ul className="info-list">
          <li>
            <span className="il-label">Name</span>
            <span className="il-value">{student.name}</span>
          </li>
          <li>
            <span className="il-label">Roll Number</span>
            <span className="il-value">{student.rollNo}</span>
          </li>
          <li>
            <span className="il-label">Branch</span>
            <span className="il-value">{student.branch}</span>
          </li>
          <li>
            <span className="il-label">Year of Study</span>
            <span className="il-value">{student.yearOfStudy}</span>
          </li>
          <li>
            <span className="il-label">College</span>
            <span className="il-value">{student.college}</span>
          </li>
          <li>
            <span className="il-label">Specialization</span>
            <span className="il-value">{student.specialization}</span>
          </li>
        </ul>
      </div>

      <pre className="code-box">{`function FunctionStudent() {
  const name = "Jey";
  const branch = "CSE";

  return (
    <div>
      <h3>Name: {name}</h3>
      <p>Branch: {branch}</p>
    </div>
  );
}`}</pre>
    </section>
  );
}

export default FunctionStudent;
