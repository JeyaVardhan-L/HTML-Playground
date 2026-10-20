import React from "react";

/**
 * Child Component: StudentCard
 *
 * Demonstrates:
 * 1. Receiving data from a parent component via `props`.
 * 2. `props` is a read-only object passed from parent to child (one-way data flow).
 * 3. Destructuring props in function parameters: `{ name, branch, rollNo, year }`.
 */
function StudentCard({ name, branch, rollNo, year }) {
  return (
    <div className="student-badge-card">
      <h3 style={{ color: "#1e40af" }}>{name}</h3>
      <div className="student-prop-row">
        <strong>Roll Number:</strong> <span>{rollNo}</span>
      </div>
      <div className="student-prop-row">
        <strong>Branch:</strong> <span>{branch}</span>
      </div>
      <div className="student-prop-row">
        <strong>Year:</strong> <span>{year}</span>
      </div>
    </div>
  );
}

/**
 * Parent Component: StudentProps
 *
 * Demonstrates:
 * 1. Maintaining an array of data objects in the parent component.
 * 2. Rendering child components dynamically using Array.prototype.map().
 * 3. Passing attributes (props) to each child component instance.
 */
function StudentProps() {
  // Array of student data in the parent component
  const studentsList = [
    {
      id: 1,
      name: "Jey",
      rollNo: "9057",
      branch: "Computer Science & Engineering",
      year: "3rd Year"
    },
    {
      id: 2,
      name: "Aarav Sharma",
      rollNo: "9012",
      branch: "Electronics & Communication",
      year: "3rd Year"
    },
    {
      id: 3,
      name: "Priya Nair",
      rollNo: "9084",
      branch: "Artificial Intelligence & Data Science",
      year: "2nd Year"
    }
  ];

  return (
    <div className="practical-card">
      <div className="practical-card-header">
        <div className="card-title-group">
          <h2>
            <span className="practical-pill">Practical 4</span>
            React Props: Parent to Child Data Passing
          </h2>
        </div>
      </div>

      <div className="explanation-banner">
        <strong>What are Props in React?</strong>
        <p style={{ marginTop: "4px" }}>
          <strong>Props</strong> (short for "properties") allow a <strong>Parent component</strong> to pass data down to a <strong>Child component</strong>, similar to passing arguments to a function. Props are <em>read-only</em> (immutable): a child component cannot modify the props it receives.
        </p>
      </div>

      <div className="demo-box">
        <div style={{ fontSize: "14px", fontWeight: 600, color: "#374151", marginBottom: "8px" }}>
          Parent Component rendering 3 Child <code>&lt;StudentCard /&gt;</code> components via <code>.map()</code>:
        </div>

        {/* Rendering child components with props */}
        <div className="student-list-grid">
          {studentsList.map((student) => (
            <StudentCard
              key={student.id}
              name={student.name}
              rollNo={student.rollNo}
              branch={student.branch}
              year={student.year}
            />
          ))}
        </div>
      </div>

      <div className="code-box">
        {`// Parent passes props:
<StudentCard name="Jey" branch="CSE" rollNo="9057" />

// Child receives props:
function StudentCard({ name, branch, rollNo }) {
  return <div><h3>{name}</h3><p>{branch}</p></div>;
}`}
      </div>
    </div>
  );
}

export default StudentProps;
