import uuid

from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Experience, Projects


class TokenAuthenticationTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(username="owner", password="password")
        self.visitor = User.objects.create_user(username="visitor", password="password")
        self.token_url = reverse("api:token")
        self.logout_url = reverse("api:token-logout")
        self.project_url = reverse("api:project-list")
        self.project_data = {
            "title": "Portfolio",
            "description": "A website",
            "tech_stack": "web-development",
        }

    def test_token_login_write_and_logout(self):
        response = self.client.post(
            self.token_url, {"username": "owner", "password": "password"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["token"]
        client = APIClient(enforce_csrf_checks=True)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = client.post(self.project_url, self.project_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(client.post(self.logout_url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(key=token).exists())
        self.assertEqual(
            client.post(self.project_url, self.project_data, format="json").status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(client.post(self.logout_url).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bad_login_and_invalid_token(self):
        response = self.client.post(
            self.token_url, {"username": "owner", "password": "wrong"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid")
        self.assertEqual(self.client.get(self.project_url).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_token_can_star_but_not_create(self):
        project = Projects.objects.create(name="Project", description="Description", category="others")
        experience = Experience.objects.create(title="Work", description="Description")
        token = Token.objects.create(user=self.visitor)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.post(self.project_url, self.project_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        for name, identifier in (("project-star", project.id), ("experience-star", experience.id)):
            response = self.client.post(reverse(f"api:{name}", args=[identifier]))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data["is_starred"])

    def test_session_logout_preserves_token_and_requires_csrf(self):
        token = Token.objects.create(user=self.owner)
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="password"))
        self.assertEqual(client.post(self.logout_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Token.objects.filter(key=token.key).exists())
        page = client.get(self.project_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        csrf_token = client.cookies["csrftoken"].value
        self.assertEqual(
            client.post(self.logout_url, HTTP_X_CSRFTOKEN=csrf_token).status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertTrue(Token.objects.filter(key=token.key).exists())
        response = client.post(self.project_url, self.project_data, format="json", HTTP_X_CSRFTOKEN=csrf_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProjectURLTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(username="owner", password="password")
        self.client.force_authenticate(user=self.owner)
        self.list_url = reverse("api:project-list")
        self.payload = {
            "title": "Project",
            "description": "Description",
            "tech_stack": "web-development",
            "project_url": "https://example.com/project",
            "project_image_url": "https://example.com/image.png",
        }

    def test_create_read_update_and_blank_default(self):
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project = Projects.objects.get(pk=response.data["id"])
        self.assertEqual(project.project_url, self.payload["project_url"])
        self.assertEqual(project.thumbnail, self.payload["project_image_url"])
        detail = reverse("api:project-detail", args=[project.id])
        self.assertEqual(self.client.get(detail).data["project_url"], self.payload["project_url"])
        new_url = "https://example.com/updated"
        response = self.client.patch(detail, {"project_url": new_url}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.project_url, new_url)
        self.assertEqual(self.client.get(self.list_url).data[0]["project_url"], new_url)
        response = self.client.post(
            self.list_url, {key: value for key, value in self.payload.items() if key != "project_url"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["project_url"], "")
        self.assertEqual(Projects.objects.get(pk=response.data["id"]).project_url, "")

    def test_invalid_url_is_rejected(self):
        response = self.client.post(
            self.list_url, {**self.payload, "project_url": "javascript:alert(1)"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("project_url", response.data)
        self.assertFalse(Projects.objects.exists())


class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(username="owner", password="password")
        self.visitor = User.objects.create_user(username="visitor", password="password")
        self.education = Education.objects.create(
            institution="University", major="Computer Science", started_at="2023-08-15"
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.id])
        self.payload = {"institution": "College", "major": "Physics", "started_at": "2024-01-10"}

    def test_public_list_detail_and_missing_uuid(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            "id": str(self.education.id), "institution": "University",
            "major": "Computer Science", "started_at": "2023-08-15",
        }])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        missing = reverse("api:education-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing).status_code, status.HTTP_404_NOT_FOUND)

    def test_only_owner_can_write(self):
        for user, expected in ((None, 401), (self.visitor, 403)):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, expected)
            self.assertEqual(self.client.patch(self.detail_url, {"major": "Art"}, format="json").status_code, expected)
            self.assertEqual(self.client.delete(self.detail_url).status_code, expected)
        self.assertEqual(Education.objects.count(), 1)
        self.education.refresh_from_db()
        self.assertEqual(self.education.major, "Computer Science")
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Education.objects.get(pk=response.data["id"]).institution, "College")
        response = self.client.patch(self.detail_url, {"major": "Mathematics"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.major, "Mathematics")
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(pk=self.education.id).exists())

    def test_token_creation_and_invalid_data(self):
        token = Token.objects.create(user=self.owner)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["started_at"], "2024-01-10")
        for changes in ({"started_at": "2024-02-30"}, {"institution": ""}, {"major": ""}):
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Education.objects.count(), 2)


class CORSTest(APITestCase):
    @override_settings(CORS_ALLOW_ALL_ORIGINS=True, CORS_ALLOW_CREDENTIALS=False)
    def test_local_origin_and_preflight(self):
        url = reverse("api:education-list")
        response = self.client.options(
            url, HTTP_ORIGIN="http://localhost:54321", HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS="authorization,content-type",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["access-control-allow-origin"], "*")
        self.assertNotIn("access-control-allow-credentials", response)
        self.assertIn("authorization", response["access-control-allow-headers"])

    @override_settings(CORS_ALLOW_ALL_ORIGINS=False, CORS_ALLOWED_ORIGINS=["https://app.example.com"])
    def test_production_only_allows_configured_origins(self):
        url = reverse("api:education-list")
        allowed = self.client.get(url, HTTP_ORIGIN="https://app.example.com")
        denied = self.client.get(url, HTTP_ORIGIN="https://other.example.com")
        self.assertEqual(allowed["access-control-allow-origin"], "https://app.example.com")
        self.assertNotIn("access-control-allow-origin", denied)
