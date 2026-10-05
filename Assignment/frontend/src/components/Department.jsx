import StudentInfo from "./StudentInfo";

function Department({ name }) {
  return (
    <div className="department-box">
      <h3>Department: {name}</h3>
      <StudentInfo />
    </div>
  );
}

export default Department;
