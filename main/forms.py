import os
from django import forms
from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    TextInput,
    Textarea,
    URLInput,
    Select,
    DateTimeInput,
    PasswordInput,
)
from django.utils import timezone
from django.utils.html import strip_tags

from main.models import Experience, Projects


class ProjectForm(ModelForm):
    admin_key = forms.CharField(
        label="Admin Key",
        widget=PasswordInput(
            attrs={
                "placeholder": "Masukkan kunci rahasia kamu cik...",
            }
        ),
        required=False,
    )

    class Meta:
        model = Projects
        fields = [
            "name",
            "description",
            "category",
            "thumbnail",
            "date_start",
            "date_end",
        ]

        labels = {
            "name": "Nama Project",
            "description": "Deskripsi Project",
            "category": "Kategori Project",
            "thumbnail": "Thumbnail Project",
            "date_start": "Tanggal mulai Project",
            "date_end": "Tanggal berakhirnya Project",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Jadi gini der",
                    "rows": 3,
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "date_start": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "date_end": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "date_start" in self.fields:
            self.fields["date_start"].required = False
        if "category" in self.fields:
            self.fields["category"].required = False

    def clean_name(self):
        name = strip_tags(self.cleaned_data.get("name", "")).strip()
        if not name:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return name

    def clean_title(self):
        title = strip_tags(str(self.cleaned_data.get("title", self.cleaned_data.get("name", "")))).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_category(self):
        val = self.cleaned_data.get("category")
        if not val:
            return "others"
        return strip_tags(str(val)).strip()

    def clean_tech_stack(self):
        return strip_tags(str(self.cleaned_data.get("tech_stack", ""))).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data.get("description", "")).strip()

    def clean_date_start(self):
        val = self.cleaned_data.get("date_start")
        if not val:
            return timezone.now()
        return val

    def clean_admin_key(self):
        key = self.cleaned_data.get("admin_key")
        expected_key = os.getenv("ADMIN_KEY")
        if expected_key and key and key != expected_key:
            raise ValidationError("Key salah! Kamu siapa loh ya >:(")
        return key


class ExperienceForm(ModelForm):
    admin_key = forms.CharField(
        label="Admin Key",
        widget=PasswordInput(
            attrs={
                "placeholder": "Masukkan kunci rahasia kamu cik...",
            }
        ),
        required=False,
    )

    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Judul Experience",
            "description": "Deskripsi Experience",
            "category": "Kategori Experience",
            "thumbnail": "Thumbnail Experience",
            "ended_at": "Tanggal berakhirnya Experience",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Internship di PT Skibidi Toilet",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Jadi gini der",
                    "rows": 3,
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def clean_admin_key(self):
        key = self.cleaned_data.get("admin_key")
        expected_key = os.getenv("ADMIN_KEY")
        if expected_key and key and key != expected_key:
            raise ValidationError("Key salah! Kamu siapa loh ya >:(")
        return key