from django.contrib.auth.models import Group
from common.tests.custom_classes import LoggedInUserTestCase, LoggedInAdminTestCase
from django.urls import reverse
from job_roles.models import Competency, Job
from app.models import Skill
from super_admin.models import SkillLevel
from .utils import creates_job_competency_instances


class JobRolePageTests(LoggedInUserTestCase):
    def test_page_GET(self):
        response = self.client.get(reverse('job-roles'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/job-roles.html')


class AddJobRoleTitleTests(LoggedInUserTestCase):

    def setUp(self):
        super(AddJobRoleTitleTests, self).setUp()
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


class AddJObRoleSkillsTests(LoggedInAdminTestCase):

    def test_add_job_role_skills_GET(self):
        response = self.client.get(reverse('add-job-skills'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/add_job_role_skills.html')

    def test_add_job_role_skills_POST_saves_skill_and_skill_level_in_session(self):
        Skill.objects.create(name='test_skill', skill_type='Career skill').save()
        SkillLevel.objects.create(name='test_skill_level').save()
        self.client.post(reverse('add-job-skills'), {'job_role_skill': 'test_skill', 'job_role_skill_level':
                                                     'test_skill_level', 'addSkill': ''})
        session = self.client.session
        self.assertEquals(session['new_added_job_competencies'], [{'test_skill': 'test_skill_level'}])


class UpdateJobRolePageTests(LoggedInAdminTestCase):
    def test_edit_competency(self):
        test_instances = creates_job_competency_instances()
        Skill.objects.create(name='updated', skill_type='Career skill').save()
        SkillLevel.objects.create(name='updated').save()
        test_competency = Competency.objects.create(job_role_title=test_instances['test_job'],
                                                    job_role_skill=test_instances['test_skill'],
                                                    job_role_skill_level=test_instances['test_skill_level'])
        test_competency.save()
        self.client.post(reverse('update-job-role-view', kwargs={'job_title': 'Test Job'}), {'job_role_skill': 'updated',
                                                                      'job_role_skill_level': 'updated',
                                                                          'update_competency': test_competency.id})
        test_competency.refresh_from_db()
        assert test_competency.job_role_skill.name == 'updated'
        assert test_competency.job_role_skill_level.name == 'updated'


class AddSkillPageTests(LoggedInAdminTestCase):
    def test_admin_user_GET_returns_200_and_correct_template(self):
        Job.objects.create(job_title='Test Job')
        response = self.client.get(reverse('add-a-skill', kwargs={'job_title': 'Test Job'}))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/add_job_role_skills.html')

    def test_valid_post_request(self):
        test_competency = creates_job_competency_instances()
        self.client.post(reverse('add-a-skill', kwargs={'job_title': 'Test Job'}), {'job_role_skill': 'test_skill',
                                                                            'job_role_skill_level': 'test_skill_level'})
        assert Competency.objects.filter(job_role_title=test_competency['test_job'], job_role_skill=test_competency['test_skill'],
                          job_role_skill_level=test_competency['test_skill_level']).exists()
