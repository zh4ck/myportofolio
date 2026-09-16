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

from main.models import Experience, Projects


class ProjectForm(ModelForm):
    admin_key = forms.CharField(
        label="Admin Key",
        widget=PasswordInput(
            attrs={
                "placeholder": "Masukkan kunci rahasia kamu cik...",
            }
        ),
        required=True,
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

    def clean_admin_key(self):
        key = self.cleaned_data.get("admin_key")
        expected_key = os.getenv("ADMIN_KEY")
        if not expected_key or key != expected_key:
            raise ValidationError("Key salah! Kamu siapa loh ya >:(")
        return key


# buat nanti
# class ExperienceForm(ModelForm):
#     class Meta:
#         model = Experience
#         fields = [
#             "title",
#             "description",
#             "category",
#             "thumbnail",
#             "ended_at",
#         ]

#         labels = {
#             "title": "Judul Experience",
#             "description": "Deskripsi Experience",
#             "category": "Kategori Experience",
#             "thumbnail": "Thumbnail Experience",
#             "ended_at": "Tanggal berakhirnya Experience",
#         }

#         widgets = {
#             "title": TextInput(
#                 attrs={
#                     "placeholder": "Internship di PT Skibidi Toilet",
#                     "maxlength": 255,
#                 }
#             ),
#             "description": Textarea(
#                 attrs={
#                     "placeholder": "Jadi gini der",
#                     "rows": 3,
#                 }
#             ),
#             "category": Select(),
#             "thumbnail": URLInput(
#                 attrs={
#                     "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
#                 }
#             ),
#             "ended_at": DateTimeInput(
#                 attrs={
#                     "type": "datetime-local",
#                 },
#                 format="%Y-%m-%dT%H:%M",
#             ),
#         }