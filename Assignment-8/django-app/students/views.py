from django.shortcuts import render
from .models import Student


def student_list(request):
    """
    Retrieve student records from SQLite using Django ORM and render template.
    Automatically populates initial sample records if database is empty.
    """
    if not Student.objects.exists():
        sample_students = [
            {"name": "Jeyavardhan Lekkala", "department": "Computer Science & Engineering", "year": "3rd Year"},
            {"name": "Sarah Jenkins", "department": "Information Technology", "year": "3rd Year"},
            {"name": "Rahul Sharma", "department": "Computer Science & Engineering", "year": "2nd Year"},
            {"name": "Priya Patel", "department": "Electronics & Communication", "year": "4th Year"},
            {"name": "Alex Rivera", "department": "Mechanical Engineering", "year": "1st Year"},
        ]
        Student.objects.bulk_create([Student(**s) for s in sample_students])

    students = Student.objects.all().order_by('id')
    return render(request, 'students/student_list.html', {'students': students})
