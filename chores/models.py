from django.db import models
from django.utils import timezone


class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Chore(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    frequency_days = models.PositiveIntegerField(default=7)
    effort_points = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE, related_name='assignments')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def mark_completed(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        status = "Done" if self.is_completed else "Pending"
        return f"{self.chore.title} -> {self.member.name} ({self.due_date}) [{status}]"
