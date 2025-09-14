from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Job, CandidateApplication

User = get_user_model()


class ModelsTest(TestCase):
    def setUp(self):
        self.company = User.objects.create_user(
            email="empresa@example.com", password="pass", is_company=True
        )
        self.candidate = User.objects.create_user(
            email="candidato@example.com", password="pass", is_company=False
        )
        self.job = Job.objects.create(
            company=self.company,
            title="Dev",
            salary_range="1000_2000",
            min_education="superior",
        )

    def test_application_and_score(self):
        app = CandidateApplication.objects.create(
            job=self.job,
            candidate=self.candidate,
            salary_expectation=1500,
            last_education="superior",
        )
        self.assertEqual(app.score, 2)
