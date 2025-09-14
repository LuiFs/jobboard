from django.urls import path
from .views import (
    JobsListView,
    job_detail,
    job_create,
    job_edit,
    job_delete,
    apply_job,
    reports_view,
    reports_json,
)

urlpatterns = [
    path("", JobsListView.as_view(), name="jobs"),
    path("jobs/<int:pk>/", job_detail, name="job_detail"),
    path("jobs/create/", job_create, name="job_create"),
    path("jobs/<int:pk>/edit/", job_edit, name="job_edit"),
    path("jobs/<int:pk>/delete/", job_delete, name="job_delete"),
    path("jobs/<int:pk>/apply/", apply_job, name="apply_job"),
    path("reports/", reports_view, name="reports"),
    path("reports/json/", reports_json, name="reports_json"),
]
