from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# --------------------------------------------------
# CUSTOM USER MODEL
# --------------------------------------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('reviewer', 'Reviewer'),
        ('reader', 'Reader'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')

    def __str__(self):
        return f"{self.username} ({self.role})"


# --------------------------------------------------
# PAPER MODEL
# --------------------------------------------------
class Paper(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('revision', 'Needs Revision'),
    ]

    title = models.CharField(max_length=200)
    abstract = models.TextField(default="Abstract not provided")
    keywords = models.CharField(max_length=200, default="None")
    field = models.CharField(max_length=100, default='General')

    file = models.FileField(upload_to='papers/')

    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_papers',
        limit_choices_to={'role': 'student'},
        null=True
    )

    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teacher_papers',
        limit_choices_to={'role': 'teacher'}
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    feedback = models.TextField(blank=True, null=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
