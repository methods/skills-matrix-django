from django.contrib.auth.models import Group
from common.tests.custom_classes import LoggedInUserTestCase, LoggedInAdminTestCase
from django.urls import reverse
from job_roles.models import Competency, Job
from skills.models import Skill
from super_admin.models import SkillLevel
from .utils import creates_job_competency_instances, creates_job_role_skill_and_skill_level_instances, assigns_users_to_a_specific_group, saves_job_title_to_session, saves_new_added_job_competencies_to_session, saves_new_added_job_competencies_to_session_as_empty_list
from django.utils.text import slugify
from django.contrib.messages import get_messages


class JobRolePageTests(LoggedInUserTestCase):
    def test_page_GET(self):
        response = self.client.get(reverse('job-roles'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/job-roles.html')


class AddJobRoleTitleTests(LoggedInUserTestCase):

    def setUp(self):
        super(AddJobRoleTitleTests, self).setUp()
        # Group setup
        self.group_name = "Admins"
        self.group = Group(name=self.group_name)
        self.group.save()

    def test_page_GET_non_admin_users(self):
        response = self.client.get(reverse('add-job-title'))
        assert response.status_code == 302

    def test_page_GET_admin_users(self):
        assigns_users_to_a_specific_group(group_name=self.group_name, user=self.user)
        response = self.client.get(reverse('add-job-title'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'job_roles/add_job_role.html')

    def test_job_role_title_saved_in__session(self):
        assigns_users_to_a_specific_group(group_name=self.group_name, user=self.user)
        response = self.client.post(reverse('add-job-title'), {'job_role_title': 'Senior Developer'})
        self.assertEqual(response.client.session['job_role_title'], 'Senior Developer')

    def test_valid_submission_redirects_to_add_job_role_skills_page(self):
        assigns_users_to_a_specific_group(group_name=self.group_name, user=self.user)
        response = self.client.post(reverse('add-job-title'), {'job_role_title': 'Lead Developer'})
        self.assertRedirects(response, expected_url=reverse('add-job-skills'), status_code=302, target_status_code=200)

    def test_input_capitalised_validation_error__message_is_sent_back_to_addjobrole_page_template(self):
        assigns_users_to_a_specific_group(group_name=self.group_name, user=self.user)
        response = self.client.post(reverse('add-job-title'), {'job_role_title': 'Lead developer'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/add_job_role.html')
        self.assertContains(response, "The job role title should be capitalised.", count=1)

    def test_input_required_validation_error__message_is_sent_back_to_addjobrole_page_template(self):
        assigns_users_to_a_specific_group(group_name=self.group_name, user=self.user)
        response = self.client.post(reverse('add-job-title'), {'job_role_title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/add_job_role.html')
        self.assertContains(response, "Enter a job role title", count=1)


class AddJobRoleSkillsTests(LoggedInAdminTestCase):

    def test_add_job_role_skills_GET(self):
        saves_job_title_to_session(session=self.client.session)
        response = self.client.get(reverse('add-job-skills'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/add_job_role_skills.html')

    def test_add_job_role_skills_redirects_if_no_job_role_title_in_the_session(self):
        response = self.client.get(reverse('add-job-skills'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please make sure to add a job role title.')
        self.assertRedirects(response, expected_url=reverse('add-job-title'), status_code=302, target_status_code=200)

    def test_add_job_role_skills_POST_saves_skill_and_skill_level_in_session(self):
        saves_job_title_to_session(session=self.client.session)
        Skill.objects.create(name='test_skill')
        SkillLevel.objects.create(name='test_skill_level')
        response = self.client.post(reverse('add-job-skills'), {'job_role_skill': 'test_skill', 'job_role_skill_level':
                                                                'test_skill_level', 'addSkill': ''})
        self.assertIn('test_skill', response.client.session['disabled_choices'])
        self.assertIn({'test_skill': 'test_skill_level'}, response.client.session['new_added_job_competencies'])
        self.assertContains(response, "Select a skill", count=2)

    def test_add_job_role_skills_POST_removes_skill_and_skill_level_from_the_session(self):
        session = self.client.session
        session['job_role_title'] = 'Test Job Role'
        session['new_added_job_competencies'] = [{'test_skill_1_to_be_deleted': 'test_skill_level_1_to_be_deleted'},
                                                 {'test_skill_2_to_be_deleted': 'test_skill_level_2_to_be_deleted'}]
        session['disabled_choices'] = ['test_skill_1_to_be_deleted', 'test_skill_2_to_be_deleted',
                                       'test_skill_3_to_be_deleted', 'test_skill_4_to_be_deleted']
        session.save()
        response = self.client.post(reverse('add-job-skills'), {'delete': 'test_skill_2_to_be_deleted'})
        self.assertNotIn('test_skill_2_to_be_deleted', response.client.session['disabled_choices'])
        self.assertNotIn({'test_skill_2_to_be_deleted': 'test_skill_level_2_to_be_deleted'},
                         response.client.session['new_added_job_competencies'])

    def test_form_validation_errors_are_sent_back_to_addjobroleskills_page_template(self):
        saves_job_title_to_session(session=self.client.session)
        SkillLevel.objects.create(name='test_skill_level')
        response = self.client.post(reverse('add-job-skills'), {'job_role_skill': '', 'job_role_skill_level':
                                                                'test_skill_level', 'addSkill': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/add_job_role_skills.html')
        self.assertContains(response, "Select a skill", count=3)


class ReviewJobRoleTests(LoggedInAdminTestCase):
    def test_review_job_role_GET(self):
        saves_job_title_to_session(session=self.client.session)
        saves_new_added_job_competencies_to_session(session=self.client.session)
        response = self.client.get(reverse('review-job-role-details'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/review_job_role.html')

    def test_review_job_role_redirects_if_no_job_role_title_in_the_session(self):
        response = self.client.get(reverse('review-job-role-details'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please make sure to add a job role title.')
        self.assertRedirects(response, expected_url=reverse('add-job-title'), status_code=302, target_status_code=200)

    def test_review_job_role_redirects_if_no_new_added_job_competencies_in_the_session(self):
        saves_job_title_to_session(session=self.client.session)
        response = self.client.get(reverse('review-job-role-details'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please make sure to add the relevant skills to this job role.')
        self.assertRedirects(response, expected_url=reverse('add-job-skills'), status_code=302, target_status_code=200)

    def test_review_job_role_redirects_if_new_added_job_competencies_length_list_is_zero(self):
        saves_job_title_to_session(session=self.client.session)
        saves_new_added_job_competencies_to_session_as_empty_list(session=self.client.session)
        response = self.client.get(reverse('review-job-role-details'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please make sure to add the relevant skills to this job role.')
        self.assertRedirects(response, expected_url=reverse('add-job-skills'), status_code=302, target_status_code=200)

    def test_review_job_role_POST_saves_new_job_role_to_db(self):
        saves_job_title_to_session(session=self.client.session)
        saves_new_added_job_competencies_to_session(session=self.client.session)
        creates_job_role_skill_and_skill_level_instances()
        response = self.client.post(reverse('review-job-role-details'), {'save': 'save'})
        test_job_title = Job.objects.get(job_title=response.client.session['job_role_title'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'The new job role was added successfully.')
        self.assertTrue(Competency.objects.filter(job_role_title=test_job_title.id).exists())
        self.assertRedirects(response, expected_url=reverse('job-roles'), status_code=302, target_status_code=200)


class DynamicJobRoleLookUpTests(LoggedInAdminTestCase):
    def test_dynamic_job_role_lookup_view_GET(self):
        Job.objects.create(job_title='Test Job Role Title')
        response = self.client.get(reverse('job-role-view', kwargs={'job': 'Test Job Role Title'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/job_role_detail.html')


class UpdateJobRolePageTests(LoggedInAdminTestCase):
    def test_update_job_role_detail_view_GET(self):
        Job.objects.create(job_title='Test Job Role Update View')
        response = self.client.get(reverse('update-job-role-view', kwargs={'job_title': 'Test Job Role Update View'}))
        self.assertEqual(response.status_code, 200)
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
        response = self.client.post(reverse('update-job-role-view',
                                            kwargs={'job_title': 'Job Role Title To Be Updated'}),
                                    {'save_job_role_title': test_job_title.id, 'job_role_title': 'New Job Role Title'})
        test_job_title.refresh_from_db()
        self.assertEqual(test_job_title.job_title, 'New Job Role Title')
        self.assertRedirects(response, expected_url=reverse('update-job-role-view',
                                                            kwargs={'job_title': slugify(test_job_title.job_title)}),
                             status_code=302, target_status_code=200)

    def test_edit_competency_save_POST(self):
        test_instances = creates_job_competency_instances()
        Skill.objects.create(name='updated').save()
        SkillLevel.objects.create(name='updated').save()
        test_competency = Competency.objects.create(job_role_title=test_instances['test_job'],
                                                    job_role_skill=test_instances['test_skill'],
                                                    job_role_skill_level=test_instances['test_skill_level'])
        test_competency.save()
        self.client.post(reverse('update-job-role-view', kwargs={'job_title': 'Test Job'}),
                         {'job_role_skill': 'updated', 'job_role_skill_level': 'updated',
                          'save_competency': test_competency.id})
        test_competency.refresh_from_db()
        assert test_competency.job_role_skill.name == 'updated'
        assert test_competency.job_role_skill_level.name == 'updated'

    def test_delete_competency_by_id_POST(self):
        test_instances = creates_job_competency_instances()
        test_competency = Competency.objects.create(job_role_title=test_instances['test_job'],
                                                    job_role_skill=test_instances['test_skill'],
                                                    job_role_skill_level=test_instances['test_skill_level'])
        self.client.post(reverse('update-job-role-view', kwargs={'job_title': 'Test Job'}), {
                                                                     'delete': test_competency.id})
        self.assertFalse(Competency.objects.filter(job_role_title=test_competency.job_role_title.id,
                                                   job_role_skill=test_competency.job_role_skill.id,
                                                   job_role_skill_level=test_competency.job_role_skill_level.id).
                         exists())

    def test_JobTitleForm_input_required_validation_error__msg_is_sent_back_to_updatejobrole_template(self):
        test_job_title = Job.objects.create(job_title='Test Job')
        response = self.client.post(reverse('update-job-role-view', kwargs={'job_title': 'Test Job'}),
                                    {'save_job_role_title': test_job_title.id, 'job_role_title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job_roles/update_job_role.html")
        self.assertContains(response, 'Enter a job role title', count=1)

    def test_JobTitleForm_input_capitalised_validation_error__msg_is_sent_back_to_updatejobrole_template(self):
        test_job_title = Job.objects.create(job_title='Test Job')
        response = self.client.post(reverse('update-job-role-view', kwargs={'job_title': 'Test Job'}),
                                    {'save_job_role_title': test_job_title.id, 'job_role_title': 'New job Role'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job_roles/update_job_role.html")
        self.assertContains(response, 'The job role title should be capitalised.', count=1)


class DeleteJobRoleTitleTests(LoggedInAdminTestCase):
    def test_delete_job_role_title_view_GET(self):
        Job.objects.create(job_title='Test Job Role Title To Be Deleted')
        response = self.client.get(reverse('delete-job-role-view',
                                   kwargs={'job_title': 'Test Job Role Title To Be Deleted'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job_roles/delete_job_role.html")

    def test_delete_job_role_title_POST(self):
        job_title_to_be_deleted = Job.objects.create(job_title='Test Job Role Title To Be Deleted')
        response = self.client.post(reverse('delete-job-role-view',
                                    kwargs={'job_title': 'Test Job Role Title To Be Deleted'}),
                                    {'delete': job_title_to_be_deleted.id})
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
        self.client.post(reverse('add-a-skill', kwargs={'job_title': 'Test Job'}),
                         {'job_role_skill': 'test_skill',
                          'job_role_skill_level': 'test_skill_level'})
        self.assertTrue(Competency.objects.filter(job_role_title=test_competency['test_job'],
                                                  job_role_skill=test_competency['test_skill'],
                                                  job_role_skill_level=test_competency['test_skill_level']).exists())

    def test_form_validation_errors_are_sent_back_to_add_a_skill_page_template(self):
        Job.objects.create(job_title='Test Job')
        SkillLevel.objects.create(name='test_skill_level')
        response = self.client.post(reverse('add-a-skill', kwargs={'job_title': 'Test Job'}),
                                    {'job_role_skill': '',
                                     'job_role_skill_level': 'test_skill_level'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_roles/add_job_role_skills.html')
        self.assertContains(response, "Select a skill", count=3)

