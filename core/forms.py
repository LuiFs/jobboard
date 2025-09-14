from django import forms
from .models import Job, CandidateApplication, EDUCATION_CHOICES


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "salary_range", "requirements", "min_education"]


class CandidateApplicationForm(forms.ModelForm):
    class Meta:
        model = CandidateApplication
        fields = ["salary_expectation", "experience", "last_education"]
        widgets = {"last_education": forms.Select(choices=EDUCATION_CHOICES)}
