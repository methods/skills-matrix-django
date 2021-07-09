from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


class JobRolePageTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        password = make_password('password')
        self.user = self.User.objects.create_user('test@methods.co.uk', 'test_first_name', 'test_surname', 'OPC',
                                                  'Junior Developer', password)
        self.client.login(username='test@methods.co.uk', password='password')

    def tearDown(self):
        self.User = get_user_model()
        self.User.objects.all().delete()

    def test_page_GET(self):
        response = self.client.get('/job-roles')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/job-roles.html')


class AddJobRolePageTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        password = make_password('password')
        self.user = self.User.objects.create_user('test@methods.co.uk', 'test_first_name', 'test_surname', 'OPC',
                                                  'Junior Developer', password)
        self.client.login(username='test@methods.co.uk', password='password')

        # Group setup
        group_name = "Admins"
        self.group = Group(name=group_name)
        self.group.save()

    def tearDown(self):
        self.User = get_user_model()
        self.User.objects.all().delete()

    def test_page_GET_non_admin_users(self):
        response = self.client.get('/job-roles/create-new-job')
        assert response.status_code == 302
    
    def test_page_GET_admin_users(self):
        admins_group = Group.objects.get(name='Admins')
        self.user.groups.add(admins_group)
        response = self.client.get('/job-roles/create-new-job')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/add_job_role.html')
