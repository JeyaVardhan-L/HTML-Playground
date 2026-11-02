from django.core.management.base import BaseCommand
from students.models import Student


class Command(BaseCommand):
    help = "Seed SQLite database with initial sample student records"

    def handle(self, *args, **options):
        sample_students = [
            {"name": "Jeyavardhan Lekkala", "department": "Computer Science & Engineering", "year": "3rd Year"},
            {"name": "Sarah Jenkins", "department": "Information Technology", "year": "3rd Year"},
            {"name": "Rahul Sharma", "department": "Computer Science & Engineering", "year": "2nd Year"},
            {"name": "Priya Patel", "department": "Electronics & Communication", "year": "4th Year"},
            {"name": "Alex Rivera", "department": "Mechanical Engineering", "year": "1st Year"},
        ]

        created_count = 0
        for data in sample_students:
            obj, created = Student.objects.get_or_create(
                name=data["name"],
                department=data["department"],
                year=data["year"],
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully initialized students table. Created {created_count} new records. "
                f"Total records in SQLite: {Student.objects.count()}"
            )
        )
