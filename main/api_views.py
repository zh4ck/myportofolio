from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Education, Experience, Projects
from main.permissions import (
    IsEducationOwnerOrReadOnly,
    IsPortfolioOwnerOrEditorOrReadOnly,
    IsPortfolioOwnerOrReadOnly,
)
from main.serializers import EducationSerializer, ExperienceSerializer, ProjectSerializer


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        projects = Projects.objects.prefetch_related("starred_by").order_by("-date_start", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(name__icontains=title)
        serializer = ProjectSerializer(projects, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Projects.objects.prefetch_related("starred_by"), pk=project_id
    )
    if request.method in ("GET", "HEAD"):
        return Response(ProjectSerializer(project, context={"request": request}).data)
    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Projects, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    return Response(ProjectSerializer(project, context={"request": request}).data)


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experiences = Experience.objects.prefetch_related("starred_by").order_by(
            "-started_at", "id"
        )
        search = (
            request.query_params.get("q", "").strip()
            or request.query_params.get("title", "").strip()
        )
        category = request.query_params.get("category", "").strip()
        if search:
            experiences = experiences.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if category:
            experiences = experiences.filter(category=category)
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request}
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id
    )
    if request.method in ("GET", "HEAD"):
        return Response(
            ExperienceSerializer(experience, context={"request": request}).data
        )
    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)
    return Response(ExperienceSerializer(experience, context={"request": request}).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def token_logout(request):
    if request.auth is not None:
        request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsEducationOwnerOrReadOnly])
def education_list(request):
    if request.method in ("GET", "HEAD"):
        education = Education.objects.order_by("-started_at", "id")
        return Response(EducationSerializer(education, many=True).data)

    serializer = EducationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsEducationOwnerOrReadOnly])
def education_detail(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    if request.method in ("GET", "HEAD"):
        return Response(EducationSerializer(education).data)
    if request.method == "DELETE":
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = EducationSerializer(
        education, data=request.data, partial=request.method == "PATCH"
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
