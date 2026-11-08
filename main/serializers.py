from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Projects


class StarFieldsMixin:
    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return obj.starred_by.filter(pk=request.user.pk).exists()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class ProjectSerializer(StarFieldsMixin, serializers.ModelSerializer):
    title = serializers.CharField(source="name", max_length=255)
    tech_stack = serializers.ChoiceField(source="category", choices=Projects.PROJECT_TYPES)
    project_image_url = serializers.URLField(
        source="thumbnail", allow_blank=True, allow_null=True, required=False
    )
    project_url = serializers.SerializerMethodField()
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    date_display = serializers.SerializerMethodField()
    is_ongoing = serializers.BooleanField(read_only=True)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = [
            "id",
            "title",
            "description",
            "tech_stack",
            "category_display",
            "project_url",
            "project_image_url",
            "date_start",
            "date_end",
            "date_display",
            "is_ongoing",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "date_start": {"required": False},
            "date_end": {"required": False, "allow_null": True},
        }

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Judul experience tidak boleh kosong atau hanya berisi tag HTML."
            )
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def get_project_url(self, obj):
        # The existing model has one URL field, used as its image URL.
        return ""

    def get_date_display(self, obj):
        start = obj.date_start.strftime("%b %Y") if obj.date_start else ""
        end = "Present" if obj.is_ongoing else obj.date_end.strftime("%b %Y")
        return f"{start} – {end}" if start else ""


class ExperienceSerializer(StarFieldsMixin, serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    date_display = serializers.SerializerMethodField()
    is_ongoing = serializers.BooleanField(read_only=True)
    status_display = serializers.SerializerMethodField()
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "description",
            "category",
            "category_display",
            "thumbnail",
            "started_at",
            "ended_at",
            "date_display",
            "is_ongoing",
            "status_display",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id", "started_at"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Deskripsi experience tidak boleh kosong atau hanya berisi tag HTML."
            )
        return value

    def get_date_display(self, obj):
        start = obj.started_at.strftime("%b %Y") if obj.started_at else ""
        end = "Ongoing" if obj.is_ongoing else obj.ended_at.strftime("%b %Y")
        return f"{start} – {end}" if start else ""

    def get_status_display(self, obj):
        return "Ongoing" if obj.is_ongoing else "Finished"
