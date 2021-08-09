from common.tests.custom_classes import LoggedInAdminTestCase
from django.core.exceptions import ValidationError
from job_roles.models import Job


class TestJobModel(LoggedInAdminTestCase):
    def test_job_title_is_capitalised(self):
        job_role = Job.objects.create(job_title="Test Job Title Is Capitalised")
        self.assertEqual(job_role.job_title, "Test Job Title Is Capitalised")
        with self.assertRaises(ValidationError):
            Job.objects.create(job_title="test job title is Not capitalised")