import datetime
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from main.models import Experience, Projects
from main.forms import ProjectForm, ExperienceForm

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Zayyan",
        "npm": "2506550955",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            """Passionate learners, aiming to become a polymath. Very interested in tinkering electronical devices and bootlegs. I spent my days experimenting with new things and creating something to be use for.
            
            Sometimes I play guitars, capturing moments, staring into the abysmal void of the universe, and most of the time reflecting on the meaning of life itself. The other time? probably chilling out, walking around the city."""
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def get_experience_json(request):
    category_query = request.GET.get("category", "").strip()
    experiences = Experience.objects.all().order_by("-started_at")

    if category_query:
        experiences = experiences.filter(category=category_query)

    experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    return HttpResponse(experiences_json, content_type="application/json")


def show_experience(request):
    category_query = request.GET.get("category", "").strip()
    experiences = Experience.objects.all().order_by("-started_at")

    if category_query:
        experiences = experiences.filter(category=category_query)

    is_editor_user = request.user.is_authenticated and (
        request.user.groups.filter(name="Editor").exists()
        or request.user.has_perm("main.change_experience")
    )

    context = {
        "name": "Zayyan",
        "experience_list": experiences,
        "category_query": category_query,
        "experience_categories": Experience.EXPERIENCE_CHOICES,
        "is_editor": is_editor_user,
    }
    return render(request, "experience.html", context)


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not (
        request.user.is_superuser
        or request.user.groups.filter(name="Editor").exists()
        or request.user.has_perm("main.change_experience")
    ):
        raise PermissionDenied

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


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")


def show_project(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Zayyan",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)

show_projects = show_project


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        if not project.date_start:
            project.date_start = timezone.now()
        project.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")

    context = {
        "name": "Zayyan",
        "form": form,
    }
    return render(request, "projects_form.html", context)


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    post_data = request.POST.copy()
    if "title" in post_data and "name" not in post_data:
        post_data["name"] = post_data["title"]
    if "tech_stack" in post_data and "category" not in post_data:
        post_data["category"] = post_data["tech_stack"]
    if "project_image_url" in post_data and "thumbnail" not in post_data:
        post_data["thumbnail"] = post_data["project_image_url"]

    form = ProjectForm(post_data)
    if form.is_valid():
        project = form.save(commit=False)
        if not project.date_start:
            project.date_start = timezone.now()
        project.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    errors = form.errors.get_json_data()
    if "name" in errors and "title" not in errors:
        errors["title"] = errors["name"]
    return JsonResponse({"errors": errors}, status=400)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Projects.objects.prefetch_related("starred_by").all().order_by("-date_start")

    if title_query:
        projects = projects.filter(name__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])
        starred_by_list = [u.username for u in starred_users]

        date_start_str = project.date_start.strftime("%b %Y") if project.date_start else ""
        date_end_str = "Present" if project.is_ongoing else (project.date_end.strftime("%b %Y") if project.date_end else "")
        date_display = f"{date_start_str} – {date_end_str}" if date_start_str else ""

        data.append({
            "pk": str(project.id),
            "fields": {
                "name": project.name,
                "title": project.name,
                "description": project.description,
                "category": project.category,
                "category_display": project.get_category_display(),
                "tech_stack": project.get_category_display(),
                "thumbnail": project.thumbnail,
                "project_image_url": project.thumbnail,
                "project_url": project.thumbnail or "",
                "date_start": project.date_start.isoformat() if project.date_start else None,
                "date_end": project.date_end.isoformat() if project.date_end else None,
                "date_start_formatted": date_start_str,
                "date_end_formatted": date_end_str,
                "date_display": date_display,
                "is_ongoing": project.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
                "starred_by": starred_by_list,
            },
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Projects, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Projects, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_project")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Zayyan",
        "form": form,
    }

    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Zayyan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response