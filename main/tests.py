from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Projects


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Finished")
        self.assertNotContains(response, "Ongoing")

# buat test project

class ProjectTest(TestCase):
    def setUp(self):
        self.project = Projects.objects.create(
            name="Portfolio Website",
            description="My portofolio aku loh ya",
            category="web-development",
            date_start=timezone.now() - timedelta(days=30),
        )

    def test_project_url_is_accessible(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")

    def test_project_page_shows_data_when_exists(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, self.project.name)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "Web Development")

    def test_empty_project_page_shows_empty_state(self):
        Projects.objects.all().delete()
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, "Belum ada project yang ditambahkan.")
        self.assertNotContains(response, self.project.name)


class AuthTest(TestCase):
    def setUp(self):
        self.username = "whatTheSigma"
        self.password = "skibidi67$"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

    def test_register_page_accessible(self):
        response = self.client.get(reverse("main:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_login_page_accessible(self):
        response = self.client.get(reverse("main:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_success_sets_cookie_and_redirects(self):
        response = self.client.post(
            reverse("main:login"),
            {"username": self.username, "password": self.password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("last_login", response.cookies)
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_clears_cookie_and_session(self):
        self.client.login(username=self.username, password=self.password)
        self.client.cookies["last_login"] = "2026-09-28 12:00:00"
        response = self.client.get(reverse("main:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(response.cookies["last_login"].value, "")


class AuthorizationAndStarTest(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(
            username="regular_user",
            password="skibidi123!",
        )
        self.superuser = User.objects.create_superuser(
            username="admin_user",
            password="whatthesigma123!",
            email="admin@example.com",
        )
        self.project = Projects.objects.create(
            name="Testing Authorization",
            description="Testing authorization features",
            category="web-development",
        )

    def test_unauthenticated_cannot_create_project(self):
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login/"))

    def test_regular_user_cannot_create_project(self):
        self.client.login(username="regular_user", password="skibidi123!")
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_access_create_project(self):
        self.client.login(username="admin_user", password="whatthesigma123!")
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 200)

    def test_toggle_star_authenticated(self):
        self.client.login(username="regular_user", password="skibidi123!")
        response = self.client.post(
            reverse("main:toggle_star", args=[self.project.id])
        )
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertIn(self.regular_user, self.project.starred_by.all())

        response = self.client.post(
            reverse("main:toggle_star", args=[self.project.id])
        )
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertNotIn(self.regular_user, self.project.starred_by.all())

    def test_api_projects_json_uses_natural_foreign_keys(self):
        self.project.starred_by.add(self.regular_user)
        response = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '["regular_user"]')
