from django.contrib.auth.models import Group
from common.tests.custom_classes import LoggedInUserTestCase, LoggedInAdminTestCase
from django.urls import reverse
from job_roles.models import Competency, Job
from app.models import Skill
from super_admin.models import SkillLevel
from .utils import creates_job_competency_instances
from django.utils.text import slugify


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


class AddJobRoleSkillsTests(LoggedInAdminTestCase):

    def test_add_job_role_skills_GET(self):
        response = self.client.get(reverse('add-job-skills'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/add_job_role_skills.html')

    def test_add_job_role_skills_POST_saves_skill_and_skill_level_in_session(self):
        Skill.objects.create(name='test_skill', skill_type='Career skill')
        SkillLevel.objects.create(name='test_skill_level')
        response = self.client.post(reverse('add-job-skills'), {'job_role_skill': 'test_skill', 'job_role_skill_level':
                                                                'test_skill_level', 'addSkill': ''})
        self.assertIn('test_skill', response.client.session['disabled_choices'])
        self.assertIn({'test_skill': 'test_skill_level'}, response.client.session['new_added_job_competencies'])
        self.assertContains(response, "Select a skill", count=1)

    def test_add_job_role_skills_POST_removes_skill_and_skill_level_from_the_session(self):
        session = self.client.session
        session['new_added_job_competencies'] = [{'test_skill_1_to_be_deleted': 'test_skill_level_1_to_be_deleted'},
                                                 {'test_skill_2_to_be_deleted': 'test_skill_level_2_to_be_deleted'}]
        session['disabled_choices'] = ['test_skill_1_to_be_deleted', 'test_skill_2_to_be_deleted',
                                       'test_skill_3_to_be_deleted', 'test_skill_4_to_be_deleted']
        session.save()
        response = self.client.post(reverse('add-job-skills'), {'delete': 'test_skill_2_to_be_deleted'})
        self.assertNotIn('test_skill_2_to_be_deleted', response.client.session['disabled_choices'])
        self.assertNotIn({'test_skill_2_to_be_deleted': 'test_skill_level_2_to_be_deleted'},
                         response.client.session['new_added_job_competencies'])

    def test_validation_errors_are_sent_back_to_addjobroleskills_page_template(self):
        SkillLevel.objects.create(name='test_skill_level')
        response = self.client.post(reverse('add-job-skills'), {'job_role_skill': '', 'job_role_skill_level':
                                                                'test_skill_level', 'addSkill': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/add_job_role_skills.html')
        self.assertContains(response, "Select a skill", count=2)


class ReviewJobRoleTests(LoggedInAdminTestCase):
    def test_review_job_role_GET(self):
        session = self.client.session
        session['job_role_title'] = 'Test Job Role'
        session.save()
        response = self.client.get(reverse('review-job-role-details'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/review_job_role.html')

    def test_review_job_role_POST_saves_new_job_role_to_db(self):
        session = self.client.session
        session['job_role_title'] = 'Test Job Role'
        session['new_added_job_competencies'] = [{'test_skill_1': 'test_skill_level_2'},
                                                 {'test_skill_2': 'test_skill_level_1'}, {'test_skill_3':
                                                                                          'test_skill_level_4'},
                                                 {'test_skill_4': 'test_skill_level_3'}]
        session.save()
        Skill.objects.create(name='test_skill_1', skill_type='Career skill').save()
        Skill.objects.create(name='test_skill_2', skill_type='Career skill').save()
        Skill.objects.create(name='test_skill_3', skill_type='Career skill').save()
        Skill.objects.create(name='test_skill_4', skill_type='Career skill').save()
        SkillLevel.objects.create(name='test_skill_level_2').save()
        SkillLevel.objects.create(name='test_skill_level_1').save()
        SkillLevel.objects.create(name='test_skill_level_4').save()
        SkillLevel.objects.create(name='test_skill_level_3').save()
        response = self.client.post(reverse('review-job-role-details'), {'save': 'save'})
        test_job_title = Job.objects.get(job_title=response.client.session['job_role_title'])
        self.assertTrue(Competency.objects.filter(job_role_title=test_job_title.id).exists())


class DynamicJobRoleLookUpTests(LoggedInAdminTestCase):
    def test_dynamic_job_role_lookup_view_GET(self):
        Job.objects.create(job_title='Test Job Role Title')
        response = self.client.get(reverse('job-role-view', kwargs={'job': 'Test Job Role Title'}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/job_role_detail.html')


class UpdateJobRolePageTests(LoggedInAdminTestCase):
    def test_update_job_role_detail_view_GET(self):
        Job.objects.create(job_title='Test Job Role Update View')
        response = self.client.get(reverse('update-job-role-view', kwargs={'job_title': 'Test Job Role Update View'}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/update_job_role.html')

    def test_edit_competency_renders_template_POST(self):
        test_instances = creates_job_competency_instances()
        test_competency = Competency.objects.create(job_role_title=test_instances['test_job'],
                                                    job_role_skill=test_instances['test_skill'],
                                                    job_role_skill_level=test_instances['test_skill_level'])
        response = self.client.post(reverse('update-job-role-view', kwargs={'job_title': 'Test Job'}),
                                    {'edit_competency': test_competency.id})
        self.assertTemplateUsed(response, 'job_roles/update_job_role.html')

    def test_edit_job_role_title_renders_template_POST(self):
        test_instances = creates_job_competency_instances()
        response = self.client.post(reverse('update-job-role-view', kwargs={'job_title': 'Test Job'}),
                                    {'edit_job_role_title': test_instances['test_job'].id})
        self.assertTemplateUsed(response, 'job_roles/update_job_role.html')

    def test_save_job_role_title_POST(self):
        test_job_title = Job.objects.create(job_title='Job Role Title To Be Updated')
        response = self.client.post(reverse('update-job-role-view', kwargs={'job_title': 'Job Role Title To Be Updated'}),
                         {'save_job_role_title': test_job_title.id, 'job_role_title': 'New Job Role Title'})
        test_job_title.refresh_from_db()
        self.assertEquals(test_job_title.job_title, 'New Job Role Title')
        self.assertRedirects(response, expected_url=reverse('update-job-role-view', kwargs={'job_title': slugify(test_job_title.job_title)}), status_code=302, target_status_code=200)

    def test_edit_competency_save_POST(self):
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

    def test_delete_competency_by_id_POST(self):
        test_instances = creates_job_competency_instances()
        test_competency = Competency.objects.create(job_role_title=test_instances['test_job'],
                                                    job_role_skill=test_instances['test_skill'],
                                                    job_role_skill_level=test_instances['test_skill_level'])
        self.client.post(reverse('update-job-role-view', kwargs={'job_title': 'Test Job'}), {
                                                                     'delete_competency': test_competency.id})
        self.assertFalse(Competency.objects.filter(job_role_title=test_competency.job_role_title.id,
                                                   job_role_skill=test_competency.job_role_skill.id,
                                                   job_role_skill_level=test_competency.job_role_skill_level.id).exists())


class DeleteJobRoleTitleTests(LoggedInAdminTestCase):
    def test_delete_job_role_title_view_GET(self):
        Job.objects.create(job_title='Test Job Role Title To Be Deleted')
        response = self.client.get(reverse('delete-job-role-view', kwargs={'job_title': 'Test Job Role Title To Be Deleted'}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "job_roles/delete_job_role.html")

    def test_delete_job_role_title_POST(self):
        job_title_to_be_deleted = Job.objects.create(job_title='Test Job Role Title To Be Deleted')
        response = self.client.post(reverse('delete-job-role-view', kwargs={'job_title': 'Test Job Role Title To Be Deleted'}),{'delete_job_role': job_title_to_be_deleted.id})
        self.assertTemplateUsed(response, "job_roles/delete_job_role_confirmation.html")
        self.assertFalse(Job.objects.filter(job_title=job_title_to_be_deleted.id).exists())


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
        self.assertTrue(Competency.objects.filter(job_role_title=test_competency['test_job'],
                                                  job_role_skill=test_competency['test_skill'],
                                                  job_role_skill_level=test_competency['test_skill_level']).exists())
