from django.contrib.auth.models import Group
from common.tests.custom_classes import LoggedInUserTestCase
from django.urls import reverse


class JobRolePageTests(LoggedInUserTestCase):
    def test_page_GET(self):
        response = self.client.get(reverse('job-roles'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/job-roles.html')


class AddJobRolePageTests(LoggedInUserTestCase):

    def setUp(self):
        super(AddJobRolePageTests, self).setUp()
        # Group setup
        group_name = "Admins"
        self.group = Group(name=group_name)
        self.group.save()

    def test_page_GET_non_admin_users(self):
        response = self.client.get(reverse('add-a-job-role'))
        assert response.status_code == 302
 
    def test_page_GET_admin_users(self):
        admins_group = Group.objects.get(name='Admins')
        self.user.groups.add(admins_group)
        response = self.client.get(reverse('add-a-job-role'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/add_job_role.html')
