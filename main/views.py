import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.urls import reverse

from main.models import Experience, Projects
from main.forms import ProjectForm, ExperienceForm

def show_main(request):
    context = {
        "name": "Zayyan",
        "npm": "2506550955",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            """Passionate learners, aiming to become a polymath. Very interested in tinkering electronical devices and bootlegs. I spent my days experimenting with new things and creating something to be use for.
            
            Sometimes I play guitars, capturing moments, staring into the abysmal void of the universe, and most of the time reflecting on the meaning of life itself. The other time? probably chilling out, walking around the city."""
        ),
    }
    return render(request, "index.html", context)


def get_experience_json(request):
    category_query = request.GET.get("category", "").strip()
    experiences = Experience.objects.all().order_by("-started_at")

    if category_query:
        experiences = experiences.filter(category=category_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def show_experience(request):
    experiences_json = get_experience_json(request).content
    experience_list = [
        deserialized.object
        for deserialized in serializers.deserialize("json", experiences_json)
    ]

    context = {
        "name": "Zayyan",
        "experience_list": experience_list,
        "category_query": request.GET.get("category", "").strip(),
        "experience_categories": Experience.EXPERIENCE_CHOICES,
    }
    return render(request, "experience.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Zayyan",
        "form": form,
        "form_title": "Add New Experience",
        "form_action": reverse("main:create_experience"),
        "is_update": False,
    }
    return render(request, "experience_form.html", context)


def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Zayyan",
        "form": form,
        "form_title": "Edit Experience",
        "form_action": reverse("main:update_experience", args=[experience_id]),
        "is_update": True,
    }
    return render(request, "experience_form.html", context)


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        admin_key = request.POST.get("admin_key", "").strip()
        expected_key = os.getenv("ADMIN_KEY", "")

        if not expected_key or admin_key != expected_key:
            messages.error(request, "Key salah! Kamu siapa cik!!!")
            return redirect("main:show_experience")

        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def show_project(request):
    title_query = request.GET.get("title", "").strip()
    projects = Projects.objects.all().order_by("-date_start")

    if title_query:
        projects = projects.filter(name__icontains=title_query)

    context = {
        "name": "Zayyan",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")

    context = {
        "name": "Zayyan",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Projects.objects.all()

    if title_query:
        projects = projects.filter(name__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Projects, pk=project_id)

    if request.method == "POST":
        admin_key = request.POST.get("admin_key", "").strip()
        expected_key = os.getenv("ADMIN_KEY", "")

        if not expected_key or admin_key != expected_key:
            messages.error(request, "Key salah! Kamu siapa cik!!!")
            return redirect("main:show_project")

        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")