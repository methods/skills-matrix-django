from django.contrib.auth.models import Group
from common.tests.custom_classes import LoggedInUserTestCase, LoggedInAdminTestCase
from django.urls import reverse
from job_roles.models import Competency, Job
from app.models import Skill
from super_admin.models import SkillLevel


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
        response = self.client.get(reverse('add-job-title'))
        assert response.status_code == 302

    def test_page_GET_admin_users(self):
        admins_group = Group.objects.get(name='Admins')
        self.user.groups.add(admins_group)
        response = self.client.get(reverse('add-job-title'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/add_job_role.html')

    def test_job_role_title_saved_in__session(self):
        admins_group = Group.objects.get(name='Admins')
        self.user.groups.add(admins_group)
        self.client.post(reverse('add-job-title'), {'job_role_title': 'Senior Developer'})
        session = self.client.session
        self.assertEqual(session['job_role_title'], 'Senior Developer')

    def test_valid_submission_redirects_to_add_job_role_skills_page(self):
        admins_group = Group.objects.get(name='Admins')
        self.user.groups.add(admins_group)
        response = self.client.post(reverse('add-job-title'), {'job_role_title': 'Lead Developer'})
        self.assertRedirects(response, '/job-roles/add-job-role-skills/')


class UpdateJobRolePageTests(LoggedInAdminTestCase):
    def test_edit_competency(self):
        test_job = Job.objects.create(job_title='test')
        test_skill = Skill.objects.create(name='test', skill_type='Career skill')
        updated_skill = Skill.objects.create(name='updated', skill_type='Career skill')
        test_skill_level = SkillLevel.objects.create(name='test')
        update_skill_level = SkillLevel.objects.create(name='updated')
        test_competency = Competency.objects.create(job_role_title=test_job, job_role_skill=test_skill,
                                  job_role_skill_level=test_skill_level)
        self.client.post(reverse('update-job-role-view', args=['test']), {'job_role_skill': 'updated',
                                                                      'job_role_skill_level': 'updated',
                                                                          'update_competency': test_competency.id})
        test_competency.refresh_from_db()
        breakpoint()
        assert test_competency.job_role_skill.name == 'updated'
        assert test_competency.job_role_skill_level.name == 'updated'
