function StudentCard({ student }) {
  return (
    <div className="card">
      <h3>{student.name}</h3>
      <p><strong>Roll No:</strong> {student.rollNo}</p>
      <p><strong>Department:</strong> {student.department}</p>
      <p><strong>Year:</strong> Year {student.year}</p>
      <p><strong>Attendance:</strong> {student.attendance}%</p>
    </div>
  );
}

export default StudentCard;
