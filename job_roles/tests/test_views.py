from django.test import TestCase


class JobRolePageTests(TestCase):
    def test_page_GET(self):
        response = self.client.get('/job-roles')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/job-roles.html')


class AddJobRolePageTests(TestCase):
    def test_page_GET(self):
        response = self.client.get('/job-roles/create-new-job')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/add_job_role.html')
