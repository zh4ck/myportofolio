import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_experience_starred_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="projects",
            name="project_url",
            field=models.URLField(blank=True, default=""),
        ),
        migrations.CreateModel(
            name="Education",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("institution", models.CharField(max_length=255)),
                ("major", models.CharField(max_length=255)),
                ("started_at", models.DateField()),
            ],
        ),
    ]
