from datetime import date
from django.test import TestCase
from django.utils import timezone
from .models import Member, Chore, Assignment


class ChoreModelTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(name="Alice", email="alice@example.com")
        self.chore = Chore.objects.create(
            title="Clean Kitchen",
            description="Wipe counters and do dishes",
            frequency_days=7,
            effort_points=2
        )

    def test_member_string_representation(self):
        self.assertEqual(str(self.member), "Alice")

    def test_chore_string_representation(self):
        self.assertEqual(str(self.chore), "Clean Kitchen")

    def test_assignment_creation_and_completion(self):
        due = date.today()
        assignment = Assignment.objects.create(
            chore=self.chore,
            member=self.member,
            due_date=due
        )
        self.assertFalse(assignment.is_completed)
        self.assertIsNone(assignment.completed_at)

        # Mark completed
        assignment.mark_completed()
        self.assertTrue(assignment.is_completed)
        self.assertIsNotNone(assignment.completed_at)
        self.assertIn("Done", str(assignment))
