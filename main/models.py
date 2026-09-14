import uuid
from django.db import models
from django.db.models.functions import Now

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Projects(models.Model):
    PROJECT_TYPES = [
        ('photography', 'Photography'),
        ('web-development', 'Web Development'),
        ('video-editing', 'Video Editing'),
        ('motion-graphics', 'Motion Graphics'),
        ('graphics-design', 'Graphics Design'),
        ('others', 'Others'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    category = models.CharField(max_length=20, choices=PROJECT_TYPES, default='other')
    thumbnail = models.URLField(blank=True, null=True)
    date_start = models.DateTimeField(db_default=Now())
    date_end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def is_ongoing(self):
        return self.date_end is None