import { useState, useEffect } from "react";
import StudentCard from "./components/StudentCard";
import Department from "./components/Department";
import StudentContext from "./context/StudentContext";
import "./App.css";

const students = [
  { id: 1, name: "Aisha Sharma",   rollNo: "CS2101", department: "Computer Science", year: 2, attendance: 88 },
  { id: 2, name: "Ravi Kumar",     rollNo: "EC2045", department: "Electronics",       year: 3, attendance: 76 },
  { id: 3, name: "Priya Nair",     rollNo: "ME3012", department: "Mechanical",        year: 4, attendance: 92 },
];

function App() {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [attendanceCount, setAttendanceCount] = useState(0);
  const [title, setTitle] = useState("Student Dashboard");

  useEffect(() => {
    document.title = title;
  }, [title]);

  const selectedStudent = students[selectedIndex];

  return (
    <StudentContext.Provider value={selectedStudent}>
      <div className="app-wrapper">
        <header className="app-header">
          <h1>{title}</h1>
          <p className="subtitle">Web Application Framework Assignment — React Demo</p>
        </header>

        <main className="app-main">

          <section className="section">
            <h2>Props Demo</h2>
            <p className="section-desc">
              The parent (<code>App</code>) passes a <code>student</code> object down to the child (<code>StudentCard</code>) as a prop.
              The child simply renders what it receives — it does not manage any state.
            </p>
            <div className="card-row">
              {students.map((s) => (
                <StudentCard key={s.id} student={s} />
              ))}
            </div>
          </section>

          <section className="section">
            <h2>State + Hooks Demo</h2>
            <p className="section-desc">
              <code>useState</code> tracks which student is selected and the attendance click counter.
              <code>useEffect</code> updates the browser tab title whenever <code>title</code> state changes.
            </p>
            <div className="controls">
              <label htmlFor="studentSelect"><strong>Select Student:</strong></label>
              <select
                id="studentSelect"
                value={selectedIndex}
                onChange={(e) => setSelectedIndex(Number(e.target.value))}
              >
                {students.map((s, i) => (
                  <option key={s.id} value={i}>{s.name}</option>
                ))}
              </select>
            </div>

            <div className="selected-info">
              <p>Selected: <strong>{selectedStudent.name}</strong> — {selectedStudent.department}</p>
            </div>

            <div className="controls">
              <button onClick={() => setAttendanceCount((c) => c + 1)}>
                Mark Attendance
              </button>
              <span className="counter-badge">{attendanceCount} click(s)</span>
              <button className="btn-secondary" onClick={() => setAttendanceCount(0)}>
                Reset
              </button>
            </div>

            <div className="controls" style={{ marginTop: "1rem" }}>
              <label htmlFor="titleInput"><strong>Page Title (useEffect demo):</strong></label>
              <input
                id="titleInput"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Type to change browser tab title"
              />
            </div>
            <p className="hint">Watch the browser tab title update as you type above.</p>
          </section>

          <section className="section">
            <h2>Context Demo</h2>
            <p className="section-desc">
              <code>StudentContext.Provider</code> wraps the whole app and supplies <code>selectedStudent</code>.
              The <code>Department</code> component sits in the middle — it does NOT receive student data as a prop.
              The inner <code>StudentInfo</code> component reads directly from context using <code>useContext()</code>.
            </p>
            <Department name={selectedStudent.department} />
          </section>

        </main>
      </div>
    </StudentContext.Provider>
  );
}

export default App;
