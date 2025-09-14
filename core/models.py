from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa ter um email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    username = models.CharField("username", max_length=150, blank=True)
    is_company = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


SALARY_CHOICES = [
    ("upto_1000", "Até 1.000"),
    ("1000_2000", "De 1.000 a 2.000"),
    ("2000_3000", "De 2.000 a 3.000"),
    ("above_3000", "Acima de 3.000"),
]
EDUCATION_CHOICES = [
    ("fundamental", "Ensino fundamental"),
    ("medio", "Ensino médio"),
    ("tecnologo", "Tecnólogo"),
    ("superior", "Ensino Superior"),
    ("pos", "Pós / MBA / Mestrado"),
    ("doutorado", "Doutorado"),
]
EDUCATION_ORDER = {
    "fundamental": 0,
    "medio": 1,
    "tecnologo": 2,
    "superior": 3,
    "pos": 4,
    "doutorado": 5,
}


class Job(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=30, choices=SALARY_CHOICES)
    requirements = models.TextField(blank=True)
    min_education = models.CharField(max_length=30, choices=EDUCATION_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - {self.company.email}"

    def applicants_count(self):
        return self.applications.count()


class CandidateApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications"
    )
    salary_expectation = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.TextField(blank=True)
    last_education = models.CharField(max_length=30, choices=EDUCATION_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.candidate.email} -> {self.job.title}"

    def compute_score(self):
        points = 0

        range_key = self.job.salary_range
        exp = float(self.salary_expectation)

        if range_key == "upto_1000" and exp <= 1000:
            points += 1
        elif range_key == "1000_2000" and 1000 < exp <= 2000:
            points += 1
        elif range_key == "2000_3000" and 2000 < exp <= 3000:
            points += 1
        elif range_key == "above_3000" and exp > 3000:
            points += 1

        job_edu = EDUCATION_ORDER.get(self.job.min_education, 0)
        cand_edu = EDUCATION_ORDER.get(self.last_education, 0)

        if cand_edu >= job_edu:
            points += 1

        self.score = points
        self.save(update_fields=["score"])

        return points


@receiver(post_save, sender=CandidateApplication)
def application_saved(sender, instance, created, **kwargs):
    if not getattr(instance, "_score_computed", False):
        instance._score_computed = True
        instance.compute_score()
