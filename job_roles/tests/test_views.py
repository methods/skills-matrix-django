from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


class JobRolePageTests(TestCase):

    def setUp(self):
        User = get_user_model()
        password = make_password('password')
        User.objects.create_user('test@methods.co.uk', 'test_first_name', 'test_surname', 'OPC',
                                                  'Junior Developer', password)
        self.client.login(username='test@methods.co.uk', password='password')

    def tearDown(self):
        User = get_user_model()
        User.objects.all().delete()

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
        self.User.objects.all().delete()

    def adds_admins_group_to_users(self):
        admins_group = Group.objects.get(name='Admins')
        self.user.groups.add(admins_group)
        return self.user

    def test_page_GET_non_admin_users(self):
        response = self.client.get('/job-roles/add-job-role-title')
        assert response.status_code == 302

    def test_page_GET_admin_users(self):
        self.adds_admins_group_to_users()
        response = self.client.get('/job-roles/add-job-role-title')
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/add_job_role.html')

    def test_job_role_title_saved_in__session(self):
        self.adds_admins_group_to_users()
        self.client.post('/job-roles/add-job-role-title', {'job_role_title': 'Senior Developer'})
        session = self.client.session
        self.assertEqual(session['job_role_title'], 'Senior Developer')
