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
    <div className="practical-card">
      <div className="practical-card-header">
        <div className="card-title-group">
          <h2>
            <span className="practical-pill">Practical 6</span>
            React Function Component
          </h2>
        </div>
      </div>

      <div className="explanation-banner">
        <strong>How Function Components Produce UI:</strong>
        <p style={{ marginTop: "4px" }}>
          In modern React, a <strong>Function Component</strong> is simply a JavaScript function that takes optional <code>props</code> as input and returns <strong>JSX</strong> (JavaScript XML). React executes the function and transforms the returned JSX into real browser DOM elements.
        </p>
      </div>

      <div className="demo-box">
        <div className="student-badge-card" style={{ maxWidth: "480px", margin: "0 auto" }}>
          <h3 style={{ color: "#065f46" }}>🧑‍💻 Student Record (Function Component)</h3>
          <div className="student-prop-row">
            <strong>Full Name:</strong> <span>{student.name}</span>
          </div>
          <div className="student-prop-row">
            <strong>Roll Number:</strong> <span>{student.rollNo}</span>
          </div>
          <div className="student-prop-row">
            <strong>Branch:</strong> <span>{student.branch}</span>
          </div>
          <div className="student-prop-row">
            <strong>Year of Study:</strong> <span>{student.yearOfStudy}</span>
          </div>
          <div className="student-prop-row">
            <strong>College:</strong> <span>{student.college}</span>
          </div>
          <div className="student-prop-row">
            <strong>Specialization:</strong> <span>{student.specialization}</span>
          </div>
        </div>
      </div>

      <div className="code-box">
        {`// Function Component Syntax:
function FunctionStudent() {
  const name = "Jey";
  const branch = "CSE";

  return (
    <div>
      <h3>Name: {name}</h3>
      <p>Branch: {branch}</p>
    </div>
  );
}`}
      </div>
    </div>
  );
}

export default FunctionStudent;
