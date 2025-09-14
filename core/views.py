from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Job, CandidateApplication
from .forms import JobForm, CandidateApplicationForm
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncMonth

User = get_user_model()


class JobsListView(ListView):
    model = Job
    template_name = "core/jobs_list.html"
    context_object_name = "jobs"


@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    applications = job.applications.select_related("candidate")
    return render(
        request, "core/job_detail.html", {"job": job, "applications": applications}
    )


@login_required
def job_create(request):
    if not request.user.is_company:
        return redirect("jobs")
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user
            job.save()
            return redirect("job_detail", pk=job.pk)
    else:
        form = JobForm()
    return render(request, "core/job_form.html", {"form": form})


@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("job_detail", pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, "core/job_form.html", {"form": form})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user)
    if request.method == "POST":
        job.delete()
        return redirect("jobs")
    return render(request, "core/job_confirm_delete.html", {"job": job})


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        form = CandidateApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.candidate = request.user
            app.save()
            return redirect("job_detail", pk=job.pk)
    else:
        form = CandidateApplicationForm()
    return render(request, "core/apply_form.html", {"form": form, "job": job})


@login_required
def reports_view(request):
    jobs = (
        Job.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    apps = (
        CandidateApplication.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    jobs_data = [
        {"month": j["month"].strftime("%Y-%m"), "count": j["count"]} for j in jobs
    ]
    apps_data = [
        {"month": a["month"].strftime("%Y-%m"), "count": a["count"]} for a in apps
    ]
    return render(
        request, "core/reports.html", {"jobs_data": jobs_data, "apps_data": apps_data}
    )


@login_required
def reports_json(request):
    jobs = (
        Job.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    apps = (
        CandidateApplication.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    jobs_data = [
        {"month": j["month"].strftime("%Y-%m"), "count": j["count"]} for j in jobs
    ]
    apps_data = [
        {"month": a["month"].strftime("%Y-%m"), "count": a["count"]} for a in apps
    ]
    return JsonResponse({"jobs": jobs_data, "applications": apps_data})
