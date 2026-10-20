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
    <tr>
      <td>{name}</td>
      <td>{rollNo}</td>
      <td>{branch}</td>
      <td>{year}</td>
    </tr>
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
    <section className="practical-section">
      <div className="practical-heading">
        <span className="pnum">Practical 4</span>
        <h2>React Props: Parent to Child Data Passing</h2>
      </div>

      <p className="practical-desc">
        <strong>Props</strong> (short for "properties") allow a parent component to pass data
        down to a child component, similar to passing arguments to a function. Props are{" "}
        <em>read-only</em>: the child cannot modify what it receives. Below, the parent maps
        over <code>studentsList</code> and renders one <code>&lt;StudentCard /&gt;</code> per entry.
      </p>

      <div className="demo-area">
        <div className="table-wrap">
          <table className="students-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Roll No.</th>
                <th>Branch</th>
                <th>Year</th>
              </tr>
            </thead>
            <tbody>
              {studentsList.map((student) => (
                <StudentCard
                  key={student.id}
                  name={student.name}
                  rollNo={student.rollNo}
                  branch={student.branch}
                  year={student.year}
                />
              ))}
            </tbody>
          </table>
        </div>
        <p className="table-note">
          Each row is a separate <code>&lt;StudentCard /&gt;</code> child component receiving
          props from the parent.
        </p>
      </div>

      <pre className="code-box">{`// Parent passes props:
<StudentCard name="Jey" branch="CSE" rollNo="9057" />

// Child receives props:
function StudentCard({ name, branch, rollNo }) {
  return <tr><td>{name}</td><td>{branch}</td></tr>;
}`}</pre>
    </section>
  );
}

export default StudentProps;
