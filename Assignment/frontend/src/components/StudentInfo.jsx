import { useContext } from "react";
import StudentContext from "../context/StudentContext";

function StudentInfo() {
  const student = useContext(StudentContext);

  if (!student) {
    return <p>No student data available.</p>;
  }

  return (
    <div className="card context-card">
      <h4>Student from Context</h4>
      <p><strong>Name:</strong> {student.name}</p>
      <p><strong>Roll No:</strong> {student.rollNo}</p>
      <p><strong>Department:</strong> {student.department}</p>
      <p><strong>Year:</strong> Year {student.year}</p>
    </div>
  );
}

export default StudentInfo;
